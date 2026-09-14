"""Synthetic tests for the optional external coordination-state root."""
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest import mock


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hm = load_module('texenda_state_root_harness', Path(__file__).resolve().parents[1] / 'harness.py')
relocation = load_module('texenda_state_root_relocation',
                         Path(__file__).resolve().parents[3] / 'tooling/workspace/relocate_state.py')


class StateRootTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / 'repo'
        self.root.mkdir()
        self.default = self.root / '.texenda'
        self.external = self.base / 'local/agent-state/texenda'
        self.harness = hm.Harness(self.root)
        self.harness.init('human:fixture')

    def tearDown(self):
        self.temporary.cleanup()

    def facts(self, path=None):
        raw = (path or (self.default / 'state.json')).read_bytes()
        state = json.loads(raw)
        return raw, state

    def relocate_synthetic(self, *, status='active', keep_default=False):
        self.external.mkdir(parents=True)
        raw, state = self.facts()
        (self.external / 'state.json').write_bytes(raw)
        if (self.default / 'state.lock').exists():
            (self.external / 'state.lock').write_bytes((self.default / 'state.lock').read_bytes())
        if not keep_default:
            (self.default / 'state.json').unlink()
            if (self.default / 'state.lock').exists():
                (self.default / 'state.lock').unlink()
        binding = {
            'schema_version': hm.BINDING_VERSION,
            'migration_id': 'synthetic-state-root',
            'repository_root': str(self.root),
            'state_root': str(self.external),
            'status': status,
            'baseline': {
                'state_sha256': hm.hashlib.sha256(raw).hexdigest(),
                'receipt_count': len(state['events']),
                'receipt_tip': state['events'][-1]['hash'],
            },
        }
        (self.root / hm.BINDING_NAME).write_text(json.dumps(binding))
        return binding

    def metadata(self):
        return {str(path.relative_to(self.root)): (path.stat().st_size, path.stat().st_mtime_ns,
                                                   path.stat().st_ctime_ns)
                for path in self.root.rglob('*') if path.is_file()}

    def relocation_layout(self):
        (self.root / '.gitignore').write_text('.texenda/\n.texenda-location.json\n')
        (self.base / 'local/agent-state').mkdir(parents=True, exist_ok=True)
        (self.base / 'local/logs').mkdir(parents=True, exist_ok=True)
        private = self.default / 'private-inputs/synthetic'
        private.mkdir(parents=True, exist_ok=True)
        (private / 'fixture.txt').write_text('synthetic')

    def test_default_state_location_remains_compatible_before_binding(self):
        before = self.metadata()
        self.assertEqual(self.harness.status()['version'], '2.0')
        self.assertIsInstance(self.harness.ready(), list)
        self.assertEqual(before, self.metadata())

    def test_explicit_external_state_location_works_before_binding(self):
        self.external.mkdir(parents=True)
        os.rename(self.default / 'state.json', self.external / 'state.json')
        os.rename(self.default / 'state.lock', self.external / 'state.lock')
        harness = hm.Harness(self.root, state_root=self.external)
        self.assertEqual(harness.status()['version'], '2.0')
        with self.assertRaisesRegex(hm.Denied, 'read-only'):
            harness.admit('WP-00', 'fixture')
        with self.assertRaisesRegex(hm.Denied, 'read-only'):
            harness.init('human:fixture')
        with self.assertRaisesRegex(hm.Denied, 'cannot be used with mutating'):
            harness.context('WP-00', 'context.json')

    def test_missing_external_state_fails_without_initialization(self):
        self.external.mkdir(parents=True)
        (self.default / 'state.json').unlink()
        (self.default / 'state.lock').unlink()
        harness = hm.Harness(self.root, state_root=self.external)
        with self.assertRaisesRegex(hm.Denied, 'run init first'):
            harness.status()
        self.assertFalse((self.external / 'state.json').exists())
        self.assertFalse((self.external / 'state.lock').exists())

    def test_dual_default_and_external_state_is_denied(self):
        self.relocate_synthetic(keep_default=True)
        with self.assertRaisesRegex(hm.Denied, 'competing default'):
            hm.Harness(self.root, state_root=self.external)

    def test_binding_requires_explicit_exact_state_root(self):
        self.relocate_synthetic()
        with self.assertRaisesRegex(hm.Denied, 'require explicit'):
            hm.Harness(self.root)
        wrong = self.base / 'wrong-state'
        wrong.mkdir()
        with self.assertRaisesRegex(hm.Denied, 'does not match'):
            hm.Harness(self.root, state_root=wrong)
        self.assertEqual(hm.Harness(self.root, state_root=self.external).status()['version'], '2.0')

    def test_moving_or_nonclosed_binding_fails_closed(self):
        binding = self.relocate_synthetic(status='moving')
        with self.assertRaisesRegex(hm.Denied, 'moving'):
            hm.Harness(self.root, state_root=self.external)
        binding['unexpected'] = True
        (self.root / hm.BINDING_NAME).write_text(json.dumps(binding))
        with self.assertRaisesRegex(hm.Denied, 'closed schema'):
            hm.Harness(self.root, state_root=self.external)

    def test_binding_repository_mismatch_is_denied(self):
        binding = self.relocate_synthetic()
        binding['repository_root'] = str(self.base)
        (self.root / hm.BINDING_NAME).write_text(json.dumps(binding))
        with self.assertRaisesRegex(hm.Denied, 'repository mismatch'):
            hm.Harness(self.root, state_root=self.external)

    def test_binding_cannot_redirect_to_another_external_root(self):
        binding = self.relocate_synthetic()
        wrong = self.base / 'other-state'
        wrong.mkdir()
        binding['state_root'] = str(wrong)
        (self.root / hm.BINDING_NAME).write_text(json.dumps(binding))
        with self.assertRaisesRegex(hm.Denied, 'frozen project workspace root'):
            hm.Harness(self.root, state_root=wrong)

    def test_binding_migration_id_is_a_bounded_safe_filename(self):
        binding = self.relocate_synthetic()
        for value in ('../../escaped', 'nested/name', '.', '', 'x' * 65):
            with self.subTest(value=value):
                binding['migration_id'] = value
                (self.root / hm.BINDING_NAME).write_text(json.dumps(binding))
                with self.assertRaisesRegex(hm.Denied, 'closed schema'):
                    hm.Harness(self.root, state_root=self.external)

    def test_relative_traversal_and_symlink_state_roots_are_denied(self):
        with self.assertRaisesRegex(hm.Denied, 'absolute'):
            hm.Harness(self.root, state_root=Path('external-state'))
        traversal = Path(str(self.base / 'child/../external-state'))
        with self.assertRaisesRegex(hm.Denied, 'traversal'):
            hm.Harness(self.root, state_root=traversal)
        real = self.base / 'real-state'
        real.mkdir()
        link = self.base / 'state-link'
        link.symlink_to(real, target_is_directory=True)
        with self.assertRaisesRegex(hm.Denied, 'symlink'):
            hm.Harness(self.root, state_root=link)

    def test_bound_initialization_is_always_denied(self):
        self.relocate_synthetic()
        harness = hm.Harness(self.root, state_root=self.external)
        with self.assertRaisesRegex(hm.Denied, 'initialization is denied'):
            harness.init('human:fixture')

    def test_any_pending_activation_transaction_blocks_bound_harness(self):
        self.relocate_synthetic()
        recovery = self.base / 'local/logs/workspace-relocation'
        recovery.mkdir(parents=True)
        (recovery / 'different-safe-id.activation-transaction.json').write_text('{}\n')
        with self.assertRaisesRegex(hm.Denied, 'pending recovery'):
            hm.Harness(self.root, state_root=self.external)

    def test_receipt_and_state_corruption_are_denied_external(self):
        self.relocate_synthetic()
        path = self.external / 'state.json'
        state = json.loads(path.read_text())
        state['events'][0]['actor'] = 'corrupt'
        path.write_text(json.dumps(state))
        with self.assertRaisesRegex(hm.Denied, 'receipt chain corrupt'):
            hm.Harness(self.root, state_root=self.external).status()

    def test_state_file_symlink_is_denied(self):
        self.relocate_synthetic()
        state = self.external / 'state.json'
        target = self.base / 'state-target.json'
        os.rename(state, target)
        state.symlink_to(target)
        with self.assertRaisesRegex(hm.Denied, 'symlink'):
            hm.Harness(self.root, state_root=self.external)

    def test_direct_and_ancestor_root_symlink_aliases_are_denied(self):
        root_alias = self.base / 'repo-alias'
        root_alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(hm.Denied, 'symlink'):
            hm.Harness(root_alias)
        real_parent = self.base / 'real-state-parent'
        (real_parent / 'state').mkdir(parents=True)
        parent_alias = self.base / 'state-parent-alias'
        parent_alias.symlink_to(real_parent, target_is_directory=True)
        with self.assertRaisesRegex(hm.Denied, 'symlink'):
            hm.Harness(self.root, state_root=parent_alias / 'state')

    def test_concurrent_writer_lock_denies_mutation(self):
        lock = self.default / 'state.lock'
        with lock.open('a+') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(hm.Denied, 'held by another writer'):
                self.harness.admit('WP-00', 'fixture')
            fcntl.flock(stream, fcntl.LOCK_UN)

    def test_stable_read_detects_same_byte_replacement(self):
        original = self.harness._read_state_once
        calls = [0]

        def replacing_read():
            result = original()
            calls[0] += 1
            if calls[0] == 1:
                raw = self.harness.statefile.read_bytes()
                replacement = self.default / '.replacement.json'
                replacement.write_bytes(raw)
                os.replace(replacement, self.harness.statefile)
            return result

        self.harness._read_state_once = replacing_read
        with self.assertRaisesRegex(hm.Denied, 'replaced'):
            self.harness.status()

    def test_check_cli_does_not_create_lock_when_state_has_none(self):
        (self.default / 'state.lock').unlink()
        before = self.metadata()
        self.assertEqual(hm.main(['--root', str(self.root), 'check']), 0)
        self.assertEqual(before, self.metadata())
        self.assertFalse((self.default / 'state.lock').exists())

    def test_private_inputs_cannot_be_evidence_or_context_output(self):
        with self.assertRaisesRegex(hm.Denied, 'private inputs'):
            self.harness.evidence('.texenda/private-inputs/kit/synthetic.csv')
        with self.assertRaisesRegex(hm.Denied, 'private inputs'):
            self.harness.context('WP-00', '.texenda/private-inputs/context.json')

    def test_evidence_check_logs_reject_private_csv_before_hash_or_read(self):
        private = self.default / 'private-inputs/kit/synthetic.csv'
        private.parent.mkdir(parents=True)
        private.write_text('synthetic private value')
        record = self.root / 'evidence/private-log.json'
        record.parent.mkdir()
        record.write_text(json.dumps({
            'schema_version': '1.0',
            'kind': 'checkpoint',
            'task_id': 'WP-00',
            'candidate_revision': 'a' * 40,
            'summary': 'synthetic private-log rejection',
            'checks': [{
                'id': 'private', 'required': True, 'status': 'PASS',
                'command_or_procedure': 'synthetic',
                'evidence_path': '.texenda/private-inputs/kit/synthetic.csv',
                'sha256': '0' * 64,
            }],
        }))
        with mock.patch.object(hm, 'file_hash', side_effect=AssertionError('private hash attempted')):
            with self.assertRaisesRegex(hm.Denied, 'private inputs or CSV'):
                self.harness.evidence('evidence/private-log.json')

    def test_evidence_check_log_symlink_is_denied_before_hash(self):
        target = self.root / 'evidence/target.log'
        target.parent.mkdir(exist_ok=True)
        target.write_text('synthetic')
        link = self.root / 'evidence/link.log'
        link.symlink_to(target)
        record = self.root / 'evidence/symlink-log.json'
        record.write_text(json.dumps({
            'schema_version': '1.0', 'kind': 'checkpoint', 'task_id': 'WP-00',
            'candidate_revision': 'a' * 40, 'summary': 'synthetic symlink rejection',
            'checks': [{
                'id': 'symlink', 'required': True, 'status': 'PASS',
                'command_or_procedure': 'synthetic', 'evidence_path': 'evidence/link.log',
                'sha256': '0' * 64,
            }],
        }))
        with mock.patch.object(hm, 'file_hash', side_effect=AssertionError('symlink hash attempted')):
            with self.assertRaisesRegex(hm.Denied, 'symlink'):
                self.harness.evidence('evidence/symlink-log.json')

    def test_binding_baseline_count_prefix_and_unchanged_hash_are_enforced(self):
        binding = self.relocate_synthetic()
        binding_path = self.root / hm.BINDING_NAME
        binding['baseline']['receipt_count'] += 1
        binding_path.write_text(json.dumps(binding))
        with self.assertRaisesRegex(hm.Denied, 'shorter'):
            hm.Harness(self.root, state_root=self.external).status()
        binding['baseline']['receipt_count'] -= 1
        binding['baseline']['receipt_tip'] = '0' * 64
        binding_path.write_text(json.dumps(binding))
        with self.assertRaisesRegex(hm.Denied, 'prefix'):
            hm.Harness(self.root, state_root=self.external).status()
        raw, state = self.facts(self.external / 'state.json')
        binding['baseline']['receipt_tip'] = state['events'][-1]['hash']
        binding_path.write_text(json.dumps(binding))
        (self.external / 'state.json').write_bytes(raw + b' ')
        with self.assertRaisesRegex(hm.Denied, 'bytes differ'):
            hm.Harness(self.root, state_root=self.external).status()

    def test_bound_state_permits_legitimate_appended_receipts(self):
        self.relocate_synthetic()
        harness = hm.Harness(self.root, state_root=self.external)
        harness.admit('WP-00', 'fixture')
        status = harness.status()
        self.assertEqual(status['tasks']['WP-00']['state'], 'admitted')
        self.assertEqual(status['receipt_count'], 2)

    def stale_cutover(self, operation):
        self.relocation_layout()
        entered, release = threading.Event(), threading.Event()
        outcome = []

        def hook(stage, _harness, _detail):
            if stage == 'locked_after_initial_binding_check':
                entered.set()
                if not release.wait(5):
                    raise RuntimeError('fixture interleave timeout')

        stale = hm.Harness(self.root, interleave=hook)

        def invoke():
            try:
                operation(stale)
            except BaseException as exc:
                outcome.append(exc)

        thread = threading.Thread(target=invoke, name='synthetic-stale-harness')
        thread.start()
        self.assertTrue(entered.wait(5))
        relocation.prepare(self.root, self.external, 'synthetic-stale-cutover')
        relocation.apply(self.root, self.external)
        release.set()
        thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(len(outcome), 1)
        self.assertIsInstance(outcome[0], hm.Denied)
        self.assertFalse((self.default / 'state.json').exists())
        self.assertFalse((self.default / 'state.lock').exists())
        self.assertTrue((self.external / 'state.json').is_file())

    def test_stale_init_cannot_recreate_default_ledger_after_cooperative_cutover(self):
        self.stale_cutover(lambda harness: harness.init('human:stale'))

    def test_stale_mutation_cannot_leave_competing_default_lock_after_cutover(self):
        self.stale_cutover(lambda harness: harness.admit('WP-00', 'stale'))

    def test_speculative_lock_cleanup_never_unlinks_another_actors_raced_inode(self):
        lock = self.default / 'state.lock'
        lock.unlink()
        raw = (self.default / 'state.json').read_bytes()
        state = json.loads(raw)
        self.external.mkdir(parents=True)
        observed = {}

        def hook(stage, _harness, _detail):
            if stage == 'before_lock_create':
                lock.write_text('')
                observed['inode'] = lock.stat().st_ino
            elif stage == 'locked_after_lock_acquired':
                (self.root / hm.BINDING_NAME).write_text(json.dumps({
                    'schema_version': hm.BINDING_VERSION,
                    'migration_id': 'synthetic-lock-race',
                    'repository_root': str(self.root),
                    'state_root': str(self.external),
                    'status': 'moving',
                    'baseline': {
                        'state_sha256': hm.hashlib.sha256(raw).hexdigest(),
                        'receipt_count': len(state['events']),
                        'receipt_tip': state['events'][-1]['hash'],
                    },
                }))

        harness = hm.Harness(self.root, interleave=hook)
        with self.assertRaisesRegex(hm.Denied, 'binding changed'):
            harness.admit('WP-00', 'fixture')
        self.assertTrue(lock.is_file())
        self.assertEqual(lock.stat().st_ino, observed['inode'])
        self.assertEqual((self.default / 'state.json').read_bytes(), raw)

    def test_binding_swap_at_final_state_boundary_cannot_append_receipt(self):
        self.relocate_synthetic()
        raw = (self.external / 'state.json').read_bytes()

        def hook(stage, harness, _detail):
            if stage != 'after_final_state_comparison_before_replacement':
                return
            path = self.root / hm.BINDING_NAME
            value = json.loads(path.read_text())
            value['status'] = 'moving'
            replacement = path.with_name('.binding-final-boundary')
            replacement.write_text(json.dumps(value))
            os.replace(replacement, path)

        harness = hm.Harness(self.root, state_root=self.external, interleave=hook)
        with self.assertRaisesRegex(hm.Denied, 'binding changed'):
            harness.admit('WP-00', 'fixture')
        self.assertEqual((self.external / 'state.json').read_bytes(), raw)
        self.assertEqual(json.loads((self.root / hm.BINDING_NAME).read_text())['status'], 'moving')
        self.assertFalse(any(path.name.startswith('.state-write-') for path in self.external.iterdir()))

    def test_final_boundary_denial_removes_only_its_exclusive_speculative_lock(self):
        lock = self.default / 'state.lock'
        lock.unlink()
        raw, state = self.facts()
        self.external.mkdir(parents=True)

        def hook(stage, _harness, _detail):
            if stage != 'after_final_state_comparison_before_replacement':
                return
            (self.root / hm.BINDING_NAME).write_text(json.dumps({
                'schema_version': hm.BINDING_VERSION,
                'migration_id': 'synthetic-final-lock-cleanup',
                'repository_root': str(self.root),
                'state_root': str(self.external),
                'status': 'moving',
                'baseline': {
                    'state_sha256': hm.hashlib.sha256(raw).hexdigest(),
                    'receipt_count': len(state['events']),
                    'receipt_tip': state['events'][-1]['hash'],
                },
            }))

        harness = hm.Harness(self.root, interleave=hook)
        with self.assertRaisesRegex(hm.Denied, 'binding changed'):
            harness.admit('WP-00', 'fixture')
        self.assertFalse(lock.exists())
        self.assertEqual((self.default / 'state.json').read_bytes(), raw)

    def test_post_replacement_binding_detection_atomically_restores_previous_state(self):
        self.relocate_synthetic()
        raw = (self.external / 'state.json').read_bytes()

        def hook(stage, _harness, _detail):
            if stage != 'after_state_replacement_before_validation':
                return
            path = self.root / hm.BINDING_NAME
            value = json.loads(path.read_text())
            value['status'] = 'moving'
            replacement = path.with_name('.binding-post-replacement')
            replacement.write_text(json.dumps(value))
            os.replace(replacement, path)

        harness = hm.Harness(self.root, state_root=self.external, interleave=hook)
        with self.assertRaisesRegex(hm.Denied, 'binding changed'):
            harness.admit('WP-00', 'fixture')
        self.assertEqual((self.external / 'state.json').read_bytes(), raw)
        self.assertEqual(len(json.loads(raw)['events']), 1)
        self.assertFalse(any(path.name.startswith('.state-write-') for path in self.external.iterdir()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
