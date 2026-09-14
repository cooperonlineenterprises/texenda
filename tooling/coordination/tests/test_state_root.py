"""Synthetic tests for the optional external coordination-state root."""
import copy
import contextlib
import fcntl
import importlib.util
import io
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

    def hard_exit_admit(self, stage, exit_code=74):
        pid = os.fork()
        if pid == 0:
            def interrupt(observed, _harness, _detail):
                if observed == stage:
                    os._exit(exit_code)
            try:
                hm.Harness(self.root, interleave=interrupt).admit('WP-00', 'fixture')
            except BaseException:
                os._exit(98)
            os._exit(0)
        _pid, status = os.waitpid(pid, 0)
        self.assertTrue(os.WIFEXITED(status))
        self.assertEqual(os.WEXITSTATUS(status), exit_code)

    def recover_state_write(self):
        harness = hm.Harness(self.root, allow_state_recovery=True)
        return harness.recover_state_write('human:owner', runtime_stopped=True)

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

    def test_post_exchange_directory_fsync_failure_restores_exact_previous_state(self):
        original_raw = (self.default / 'state.json').read_bytes()
        original_fsync = hm.os.fsync
        armed = [False]
        failed = [False]

        def interleave(stage, _harness, _detail):
            if stage == 'state_write_after_exchange_before_fsync':
                armed[0] = True

        def fail_once(descriptor):
            metadata = os.fstat(descriptor)
            if (armed[0] and not failed[0] and hm.stat.S_ISDIR(metadata.st_mode)
                    and (metadata.st_dev, metadata.st_ino)
                    == (self.default.stat().st_dev, self.default.stat().st_ino)):
                failed[0] = True
                raise OSError('synthetic post-exchange directory fsync failure')
            return original_fsync(descriptor)

        harness = hm.Harness(self.root, interleave=interleave)
        with mock.patch.object(hm.os, 'fsync', side_effect=fail_once):
            with self.assertRaisesRegex(OSError, 'post-exchange directory fsync failure'):
                harness.admit('WP-00', 'fixture')
        self.assertTrue(failed[0])
        self.assertEqual((self.default / 'state.json').read_bytes(), original_raw)
        self.assertEqual(hm.state_transaction_blocker_names(self.default), [])
        self.assertTrue(list(self.default.glob('state-write-recovered-*.json')))

    def test_post_exchange_and_rollback_fsync_failures_preserve_both_byte_sets(self):
        original_raw = (self.default / 'state.json').read_bytes()
        original_fsync = hm.os.fsync
        armed = [False]
        failures = [0]

        def interleave(stage, _harness, _detail):
            if stage == 'state_write_after_exchange_before_fsync':
                armed[0] = True

        def fail_twice(descriptor):
            metadata = os.fstat(descriptor)
            if (armed[0] and failures[0] < 2 and hm.stat.S_ISDIR(metadata.st_mode)
                    and (metadata.st_dev, metadata.st_ino)
                    == (self.default.stat().st_dev, self.default.stat().st_ino)):
                failures[0] += 1
                raise OSError('synthetic exchange/rollback fsync failure')
            return original_fsync(descriptor)

        harness = hm.Harness(self.root, interleave=interleave)
        with mock.patch.object(hm.os, 'fsync', side_effect=fail_twice):
            with self.assertRaisesRegex(hm.Denied, 'all recovery material is retained'):
                harness.admit('WP-00', 'fixture')
        self.assertEqual(failures[0], 2)
        transaction = json.loads((self.default / hm.STATE_TRANSACTION_PENDING).read_text())
        candidate = self.default / transaction['candidate_name']
        self.assertEqual((self.default / 'state.json').read_bytes(), original_raw)
        self.assertEqual(hm.hashlib.sha256(candidate.read_bytes()).hexdigest(),
                         transaction['new_state']['sha256'])
        with self.assertRaisesRegex(hm.Denied, 'pending explicit recovery'):
            hm.Harness(self.root).status()
        result = self.recover_state_write()
        self.assertEqual(result['outcome'], 'previous_state_restored')
        self.assertFalse(candidate.exists())

    def test_rollback_exchange_failure_preserves_both_ledgers_and_transaction(self):
        original_raw = (self.default / 'state.json').read_bytes()
        original_binding = None
        self.external.mkdir(parents=True)
        original_rename = hm.renameat_state
        exchanges = [0]

        def interleave(stage, _harness, _detail):
            nonlocal original_binding
            if stage != 'after_state_replacement_before_validation':
                return
            binding = {
                'schema_version': hm.BINDING_VERSION,
                'migration_id': 'synthetic-state-write-rollback-failure',
                'repository_root': str(self.root),
                'state_root': str(self.external),
                'status': 'moving',
                'baseline': {
                    'state_sha256': hm.hashlib.sha256(original_raw).hexdigest(),
                    'receipt_count': len(json.loads(original_raw)['events']),
                    'receipt_tip': json.loads(original_raw)['events'][-1]['hash'],
                },
            }
            original_binding = json.dumps(binding).encode()
            (self.root / hm.BINDING_NAME).write_bytes(original_binding)

        def fail_second_exchange(*arguments):
            if arguments[-1] == 'exchange':
                exchanges[0] += 1
                if exchanges[0] == 2:
                    raise OSError('synthetic rollback exchange failure')
            return original_rename(*arguments)

        harness = hm.Harness(self.root, interleave=interleave)
        with mock.patch.object(hm, 'renameat_state', side_effect=fail_second_exchange):
            with self.assertRaisesRegex(hm.Denied, 'all recovery material is retained'):
                harness.admit('WP-00', 'fixture')
        transaction = json.loads((self.default / hm.STATE_TRANSACTION_PENDING).read_text())
        candidate = self.default / transaction['candidate_name']
        self.assertEqual(hm.hashlib.sha256((self.default / 'state.json').read_bytes()).hexdigest(),
                         transaction['new_state']['sha256'])
        self.assertEqual(hm.hashlib.sha256(candidate.read_bytes()).hexdigest(),
                         transaction['old_state']['sha256'])
        self.assertTrue(self.default.joinpath(hm.STATE_TRANSACTION_PENDING).is_file())
        # Restore only the synthetic binding fixture, then exercise the explicit
        # lock-held rollback of the preserved transaction.
        (self.root / hm.BINDING_NAME).unlink()
        result = self.recover_state_write()
        self.assertEqual(result['outcome'], 'previous_state_restored')
        self.assertEqual((self.default / 'state.json').read_bytes(), original_raw)
        self.assertFalse(candidate.exists())

    def test_competing_valid_inode_at_exchange_is_restored_and_both_chains_survive(self):
        original_raw = (self.default / 'state.json').read_bytes()
        competing = copy.deepcopy(json.loads(original_raw))
        competing['tasks']['WP-00']['state'] = 'admitted'
        self.harness._event(competing, 'human:competing-writer', 'admit', 'WP-00')
        self.harness._check(competing)
        competing_raw = (json.dumps(competing, indent=2, ensure_ascii=False,
                                    allow_nan=False).encode() + b'\n')

        def substitute(stage, _harness, _detail):
            if stage != 'state_write_before_exchange':
                return
            replacement = self.default / '.synthetic-competing-state'
            replacement.write_bytes(competing_raw)
            os.replace(replacement, self.default / 'state.json')

        harness = hm.Harness(self.root, interleave=substitute)
        with self.assertRaisesRegex(hm.Denied, 'displaced a state other than'):
            harness.admit('WP-00', 'fixture')
        transaction = json.loads((self.default / hm.STATE_TRANSACTION_PENDING).read_text())
        candidate = self.default / transaction['candidate_name']
        self.assertEqual((self.default / 'state.json').read_bytes(), competing_raw)
        self.assertEqual(hm.hashlib.sha256(candidate.read_bytes()).hexdigest(),
                         transaction['new_state']['sha256'])
        hm.check_receipts(json.loads((self.default / 'state.json').read_bytes()))
        hm.check_receipts(json.loads(candidate.read_bytes()))
        with self.assertRaisesRegex(hm.Denied, 'missing, corrupt, or ambiguous'):
            self.recover_state_write()
        self.assertEqual((self.default / 'state.json').read_bytes(), competing_raw)
        self.assertTrue(candidate.is_file())

    def test_cleanup_atomic_capture_never_unlinks_a_raced_competing_inode(self):
        original_raw = (self.default / 'state.json').read_bytes()
        competing = copy.deepcopy(json.loads(original_raw))
        competing['tasks']['WP-01']['state'] = 'admitted'
        self.harness._event(competing, 'human:cleanup-racer', 'admit', 'WP-01')
        self.harness._check(competing)
        competing_raw = (json.dumps(competing, indent=2, ensure_ascii=False,
                                    allow_nan=False).encode() + b'\n')
        preserved = {}

        def race(stage, _harness, detail):
            if stage != 'state_write_before_candidate_capture' or detail['role'] != 'previous':
                return
            transaction = detail['transaction']
            candidate = self.default / transaction['candidate_name']
            preserved_path = self.default / ('.state-write-raced-preserved-'
                                             + transaction['token'] + '.json')
            os.rename(candidate, preserved_path)
            candidate.write_bytes(competing_raw)
            preserved['path'] = preserved_path
            preserved['checkpoint'] = self.default / detail['destination']

        harness = hm.Harness(self.root, interleave=race)
        with self.assertRaisesRegex(hm.Denied, 'all recovery material is retained'):
            harness.admit('WP-00', 'fixture')
        transaction = json.loads((self.default / hm.STATE_TRANSACTION_PENDING).read_text())
        active_raw = (self.default / 'state.json').read_bytes()
        self.assertEqual(hm.hashlib.sha256(active_raw).hexdigest(),
                         transaction['new_state']['sha256'])
        self.assertEqual(preserved['path'].read_bytes(), original_raw)
        self.assertEqual(preserved['checkpoint'].read_bytes(), competing_raw)
        hm.check_receipts(json.loads(active_raw))
        hm.check_receipts(json.loads(preserved['path'].read_bytes()))
        hm.check_receipts(json.loads(preserved['checkpoint'].read_bytes()))
        self.assertTrue(hm.state_transaction_blocker_names(self.default))

    def test_candidate_replacement_after_directory_fsync_cannot_enter_ready_record(self):
        original_raw = (self.default / 'state.json').read_bytes()
        competing = copy.deepcopy(json.loads(original_raw))
        competing['tasks']['WP-02']['state'] = 'admitted'
        self.harness._event(competing, 'human:ready-candidate-racer', 'admit', 'WP-02')
        self.harness._check(competing)
        competing_raw = (json.dumps(competing, indent=2, ensure_ascii=False,
                                    allow_nan=False).encode() + b'\n')
        preserved = {}

        def substitute(stage, _harness, preparation):
            if stage != 'state_write_after_candidate_directory_fsync':
                return
            candidate = self.default / preparation['candidate_name']
            intended = self.default / ('state-write-review-preserved-intended-'
                                       + preparation['token'] + '.json')
            os.rename(candidate, intended)
            candidate.write_bytes(competing_raw)
            preserved['intended'] = intended

        harness = hm.Harness(self.root, interleave=substitute)
        with self.assertRaisesRegex(hm.Denied, 'all recovery material is retained'):
            harness.admit('WP-00', 'fixture')
        preparation = json.loads((self.default / hm.STATE_TRANSACTION_PENDING).read_text())
        expected_intended_sha = preparation['new_state']['sha256']
        self.assertEqual((self.default / 'state.json').read_bytes(), original_raw)
        self.assertEqual(hm.hashlib.sha256(preserved['intended'].read_bytes()).hexdigest(),
                         expected_intended_sha)
        candidate = self.default / preparation['candidate_name']
        intended_checkpoint = self.default / harness._checkpoint_name(
            preparation, 'intended', preparation['new_state'])
        self.assertEqual(candidate.read_bytes(), competing_raw)
        self.assertEqual(intended_checkpoint.read_bytes(), preserved['intended'].read_bytes())
        self.assertNotEqual(hm.hashlib.sha256(competing_raw).hexdigest(),
                            expected_intended_sha)
        self.assertFalse(any(path.name.startswith('.state-write-ready-')
                             for path in self.default.iterdir()))
        self.assertTrue(hm.state_transaction_blocker_names(self.default))
        with self.assertRaises(hm.Denied):
            self.recover_state_write()
        self.assertEqual((self.default / 'state.json').read_bytes(), original_raw)
        self.assertTrue(candidate.exists())
        self.assertTrue(intended_checkpoint.exists())

    def test_preparation_checkpoint_resume_validates_exact_captured_material(self):
        def captured_fixture(root):
            harness = hm.Harness(root)
            harness.init('human:fixture')
            original = (root / '.texenda/state.json').read_bytes()
            pid = os.fork()
            if pid == 0:
                def stop_ready(stage, _harness, detail):
                    if (stage == 'state_write_after_control_staging_partial'
                            and detail['target'].startswith('.state-write-candidate-bound-')):
                        os._exit(83)
                hm.Harness(root, interleave=stop_ready).admit('WP-00', 'fixture')
                os._exit(0)
            _pid, status = os.waitpid(pid, 0)
            self.assertEqual(os.WEXITSTATUS(status), 83)
            pid = os.fork()
            if pid == 0:
                def stop_capture(stage, _harness, _detail):
                    if stage == 'state_write_after_candidate_capture':
                        os._exit(84)
                recovery = hm.Harness(root, interleave=stop_capture,
                                      allow_state_recovery=True)
                recovery.recover_state_write('human:owner', runtime_stopped=True)
                os._exit(0)
            _pid, status = os.waitpid(pid, 0)
            self.assertEqual(os.WEXITSTATUS(status), 84)
            state_root = root / '.texenda'
            preparation = json.loads((state_root / hm.STATE_TRANSACTION_PENDING).read_text())
            checkpoint_name = hm.Harness(root, allow_state_recovery=True)._checkpoint_name(
                preparation, 'attempted', preparation['new_state'])
            return original, preparation, state_root / checkpoint_name

        with tempfile.TemporaryDirectory() as directory:
            root = (Path(directory) / 'repo').resolve()
            root.mkdir()
            original, _preparation, checkpoint = captured_fixture(root)
            result = hm.Harness(root, allow_state_recovery=True).recover_state_write(
                'human:owner', runtime_stopped=True)
            self.assertEqual(result['outcome'], 'previous_state_restored')
            self.assertEqual((root / '.texenda/state.json').read_bytes(), original)
            self.assertEqual(hm.state_transaction_blocker_names(root / '.texenda'), [])

        for mutation in ('corrupt', 'missing', 'duplicate', 'wrong-type', 'fifo'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = (Path(directory) / 'repo').resolve()
                root.mkdir()
                original, preparation, checkpoint = captured_fixture(root)
                if mutation == 'corrupt':
                    checkpoint.write_text('{}\n')
                elif mutation == 'missing':
                    checkpoint.unlink()
                elif mutation == 'duplicate':
                    duplicate = checkpoint.with_name(
                        'state-write-checkpoint-previous-'
                        + preparation['new_state']['sha256'] + '-'
                        + preparation['token'] + '.json')
                    duplicate.write_bytes(checkpoint.read_bytes())
                elif mutation == 'wrong-type':
                    preserved = checkpoint.with_name(checkpoint.name + '.preserved')
                    os.rename(checkpoint, preserved)
                    checkpoint.mkdir()
                else:
                    preserved = checkpoint.with_name(checkpoint.name + '.preserved')
                    os.rename(checkpoint, preserved)
                    os.mkfifo(checkpoint)
                recovery = hm.Harness(root, allow_state_recovery=True)
                with self.assertRaises(hm.Denied):
                    recovery.recover_state_write('human:owner', runtime_stopped=True)
                self.assertEqual((root / '.texenda/state.json').read_bytes(), original)
                self.assertTrue(hm.state_transaction_blocker_names(root / '.texenda'))

    def test_preparation_capture_rejects_byte_identical_replacement_inode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = (Path(directory) / 'repo').resolve()
            root.mkdir()
            hm.Harness(root).init('human:fixture')
            original = (root / '.texenda/state.json').read_bytes()
            pid = os.fork()
            if pid == 0:
                def stop_ready(stage, _harness, detail):
                    if (stage == 'state_write_after_control_staging_partial'
                            and detail['target'].startswith('.state-write-candidate-bound-')):
                        os._exit(85)
                hm.Harness(root, interleave=stop_ready).admit('WP-00', 'fixture')
                os._exit(0)
            _pid, status = os.waitpid(pid, 0)
            self.assertEqual(os.WEXITSTATUS(status), 85)
            state_root = root / '.texenda'
            preparation = json.loads((state_root / hm.STATE_TRANSACTION_PENDING).read_text())
            candidate = state_root / preparation['candidate_name']
            intended_name = hm.Harness(root, allow_state_recovery=True)._checkpoint_name(
                preparation, 'intended', preparation['new_state'])
            intended = state_root / intended_name
            observed = {}

            def replace(stage, _harness, detail):
                if stage != 'state_write_before_candidate_capture' or detail['role'] != 'attempted':
                    return
                preserved = state_root / ('state-write-review-preserved-candidate-'
                                          + preparation['token'] + '.json')
                os.rename(candidate, preserved)
                candidate.write_bytes(preserved.read_bytes())
                observed['preserved'] = preserved

            recovery = hm.Harness(root, interleave=replace, allow_state_recovery=True)
            with self.assertRaisesRegex(hm.Denied, 'checkpoint (?:differs|is corrupt)'):
                recovery.recover_state_write('human:owner', runtime_stopped=True)
            attempted_name = recovery._checkpoint_name(
                preparation, 'attempted', preparation['new_state'])
            attempted = state_root / attempted_name
            self.assertEqual(intended.read_bytes(), attempted.read_bytes())
            self.assertNotEqual(intended.stat().st_ino, attempted.stat().st_ino)
            self.assertEqual(observed['preserved'].read_bytes(), attempted.read_bytes())
            self.assertEqual((state_root / 'state.json').read_bytes(), original)
            self.assertTrue(hm.state_transaction_blocker_names(state_root))

    def test_hard_interruptions_recover_previous_state_at_every_precleanup_phase(self):
        stages = (
            'state_write_after_preparation_control',
            'state_write_before_candidate_file_fsync',
            'state_write_after_candidate_file_fsync',
            'state_write_after_candidate_directory_fsync',
            'state_write_after_transaction_prepared',
            'state_write_after_exchange_before_fsync',
            'state_write_after_exchange_fsync',
            'state_write_after_displaced_validation',
            'after_state_replacement_before_validation',
            'state_write_after_commit_cleanup_marker',
            'state_write_before_candidate_capture',
            'state_write_after_candidate_capture_before_fsync',
            'state_write_after_candidate_capture',
        )
        original_raw = (self.default / 'state.json').read_bytes()
        for stage in stages:
            with self.subTest(stage=stage):
                self.hard_exit_admit(stage)
                with self.assertRaisesRegex(hm.Denied, 'pending explicit recovery'):
                    hm.Harness(self.root).status()
                result = self.recover_state_write()
                self.assertEqual(result['outcome'], 'previous_state_restored')
                self.assertEqual((self.default / 'state.json').read_bytes(), original_raw)
                self.assertEqual(hm.state_transaction_blocker_names(self.default), [])

    def test_hard_exit_after_commit_candidate_capture_still_restores_previous_state(self):
        self.hard_exit_admit('state_write_after_commit_candidate_cleanup')
        with self.assertRaisesRegex(hm.Denied, 'pending explicit recovery'):
            hm.Harness(self.root).status()
        result = self.recover_state_write()
        self.assertEqual(result['outcome'], 'previous_state_restored')
        status = hm.Harness(self.root).status()
        self.assertEqual(status['tasks']['WP-00']['state'], 'planned')
        self.assertEqual(status['receipt_count'], 1)
        self.assertEqual(hm.state_transaction_blocker_names(self.default), [])

    def test_hard_exit_after_commit_archive_needs_no_recovery(self):
        self.hard_exit_admit('state_write_after_commit_archive')
        status = hm.Harness(self.root).status()
        self.assertEqual(status['tasks']['WP-00']['state'], 'admitted')
        self.assertEqual(status['receipt_count'], 2)
        self.assertEqual(hm.state_transaction_blocker_names(self.default), [])

    def test_hard_exit_after_durable_outcome_archive_finishes_forward(self):
        self.hard_exit_admit('state_write_after_outcome_archive')
        with self.assertRaisesRegex(hm.Denied, 'pending explicit recovery'):
            hm.Harness(self.root).status()
        result = self.recover_state_write()
        self.assertEqual(result['outcome'], 'durable_commit_cleanup_completed')
        status = hm.Harness(self.root).status()
        self.assertEqual(status['tasks']['WP-00']['state'], 'admitted')
        self.assertEqual(status['receipt_count'], 2)

    def test_hard_interruptions_during_rollback_recovery_resume_deterministically(self):
        stages = (
            'state_write_after_rollback_exchange_before_fsync',
            'state_write_after_rollback_durable',
            'state_write_after_rollback_cleanup_marker',
            'state_write_after_candidate_capture_before_fsync',
            'state_write_after_candidate_capture',
            'state_write_after_recovery_candidate_cleanup',
            'state_write_after_outcome_archive',
            'state_write_after_preparation_archive',
            'state_write_after_recovery_archive',
        )
        for stage in stages:
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as directory:
                root = (Path(directory) / 'repo').resolve()
                root.mkdir()
                hm.Harness(root).init('human:fixture')
                original = (root / '.texenda/state.json').read_bytes()
                pid = os.fork()
                if pid == 0:
                    def stop_write(observed, _harness, _detail):
                        if observed == 'state_write_after_exchange_fsync':
                            os._exit(77)
                    try:
                        hm.Harness(root, interleave=stop_write).admit('WP-00', 'fixture')
                    except BaseException:
                        os._exit(98)
                    os._exit(0)
                _pid, status = os.waitpid(pid, 0)
                self.assertEqual(os.WEXITSTATUS(status), 77)

                pid = os.fork()
                if pid == 0:
                    def stop_recovery(observed, _harness, _detail):
                        if observed == stage:
                            os._exit(78)
                    try:
                        recovery = hm.Harness(root, interleave=stop_recovery,
                                              allow_state_recovery=True)
                        recovery.recover_state_write('human:owner', runtime_stopped=True)
                    except BaseException:
                        os._exit(99)
                    os._exit(0)
                _pid, status = os.waitpid(pid, 0)
                self.assertEqual(os.WEXITSTATUS(status), 78)
                blockers = hm.state_transaction_blocker_names(root / '.texenda')
                if blockers:
                    result = hm.Harness(root, allow_state_recovery=True).recover_state_write(
                        'human:owner', runtime_stopped=True)
                    self.assertEqual(result['outcome'], 'previous_state_restored')
                self.assertEqual((root / '.texenda/state.json').read_bytes(), original)
                self.assertEqual(hm.state_transaction_blocker_names(root / '.texenda'), [])

    def test_checkpoint_backed_rollback_resumes_after_exchange_boundaries(self):
        for stage in ('state_write_after_rollback_exchange_before_fsync',
                      'state_write_after_checkpoint_rollback_exchange_fsync'):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as directory:
                root = (Path(directory) / 'repo').resolve()
                root.mkdir()
                hm.Harness(root).init('human:fixture')
                original = (root / '.texenda/state.json').read_bytes()
                pid = os.fork()
                if pid == 0:
                    def stop_commit(observed, _harness, _detail):
                        if observed == 'state_write_after_commit_candidate_cleanup':
                            os._exit(79)
                    hm.Harness(root, interleave=stop_commit).admit('WP-00', 'fixture')
                    os._exit(0)
                _pid, status = os.waitpid(pid, 0)
                self.assertEqual(os.WEXITSTATUS(status), 79)

                pid = os.fork()
                if pid == 0:
                    def stop_rollback(observed, _harness, _detail):
                        if observed == stage:
                            os._exit(80)
                    recovery = hm.Harness(root, interleave=stop_rollback,
                                          allow_state_recovery=True)
                    recovery.recover_state_write('human:owner', runtime_stopped=True)
                    os._exit(0)
                _pid, status = os.waitpid(pid, 0)
                self.assertEqual(os.WEXITSTATUS(status), 80)
                result = hm.Harness(root, allow_state_recovery=True).recover_state_write(
                    'human:owner', runtime_stopped=True)
                self.assertEqual(result['outcome'], 'previous_state_restored')
                self.assertEqual((root / '.texenda/state.json').read_bytes(), original)
                self.assertEqual(hm.state_transaction_blocker_names(root / '.texenda'), [])

    def test_interrupted_initialization_restores_absence_then_can_reinitialize(self):
        with tempfile.TemporaryDirectory() as directory:
            root = (Path(directory) / 'repo').resolve()
            root.mkdir()
            pid = os.fork()
            if pid == 0:
                def interrupt(stage, _harness, _detail):
                    if stage == 'state_write_after_exchange_before_fsync':
                        os._exit(75)
                try:
                    hm.Harness(root, interleave=interrupt).init('human:fixture')
                except BaseException:
                    os._exit(98)
                os._exit(0)
            _pid, status = os.waitpid(pid, 0)
            self.assertEqual(os.WEXITSTATUS(status), 75)
            with self.assertRaisesRegex(hm.Denied, 'pending explicit recovery'):
                hm.Harness(root)
            recovery = hm.Harness(root, allow_state_recovery=True).recover_state_write(
                'human:owner', runtime_stopped=True)
            self.assertEqual(recovery['outcome'], 'previous_state_restored')
            self.assertFalse((root / '.texenda/state.json').exists())
            hm.Harness(root).init('human:fixture')
            self.assertEqual(hm.Harness(root).status()['receipt_count'], 1)

    def test_first_init_candidate_fsync_failure_has_a_recoverable_preparation_control(self):
        with tempfile.TemporaryDirectory() as directory:
            root = (Path(directory) / 'repo').resolve()
            root.mkdir()
            original_fsync = hm.os.fsync
            armed = [False]
            failed = [False]

            def interleave(stage, _harness, _detail):
                if stage == 'state_write_before_candidate_file_fsync':
                    armed[0] = True

            def fail_candidate_once(descriptor):
                metadata = os.fstat(descriptor)
                if armed[0] and not failed[0] and hm.stat.S_ISREG(metadata.st_mode):
                    failed[0] = True
                    raise OSError('synthetic first-init candidate fsync failure')
                return original_fsync(descriptor)

            harness = hm.Harness(root, interleave=interleave)
            with mock.patch.object(hm.os, 'fsync', side_effect=fail_candidate_once):
                with self.assertRaisesRegex(OSError, 'first-init candidate fsync failure'):
                    harness.init('human:fixture')
            self.assertTrue(failed[0])
            self.assertEqual(hm.state_transaction_blocker_names(root / '.texenda'), [])
            self.assertFalse((root / '.texenda/state.json').exists())
            self.assertFalse((root / '.texenda/state.lock').exists())
            hm.Harness(root).init('human:fixture')
            self.assertEqual(hm.Harness(root).status()['receipt_count'], 1)

    def test_partial_staging_never_publishes_a_phase_control(self):
        with tempfile.TemporaryDirectory() as directory:
            root = (Path(directory) / 'repo').resolve()
            root.mkdir()
            pid = os.fork()
            if pid == 0:
                def stop_preparation(stage, _harness, detail):
                    if (stage == 'state_write_after_control_staging_partial'
                            and detail['target'] == hm.STATE_TRANSACTION_PENDING):
                        os._exit(81)
                hm.Harness(root, interleave=stop_preparation).init('human:fixture')
                os._exit(0)
            _pid, status = os.waitpid(pid, 0)
            self.assertEqual(os.WEXITSTATUS(status), 81)
            self.assertFalse((root / '.texenda/.state-write-transaction.json').exists())
            self.assertEqual(hm.state_transaction_blocker_names(root / '.texenda'), [])
            self.assertTrue(list((root / '.texenda').glob('state-write-staging-*.tmp')))
            hm.Harness(root).init('human:fixture')
            self.assertEqual(hm.Harness(root).status()['receipt_count'], 1)

        original = (self.default / 'state.json').read_bytes()
        pid = os.fork()
        if pid == 0:
            def stop_ready(stage, _harness, detail):
                if (stage == 'state_write_after_control_staging_partial'
                        and detail['target'].startswith('.state-write-candidate-bound-')):
                    os._exit(82)
            hm.Harness(self.root, interleave=stop_ready).admit('WP-00', 'fixture')
            os._exit(0)
        _pid, status = os.waitpid(pid, 0)
        self.assertEqual(os.WEXITSTATUS(status), 82)
        blockers = hm.state_transaction_blocker_names(self.default)
        self.assertIn(hm.STATE_TRANSACTION_PENDING, blockers)
        self.assertFalse(any(name.startswith('.state-write-ready-') for name in blockers))
        result = self.recover_state_write()
        self.assertEqual(result['outcome'], 'previous_state_restored')
        self.assertEqual((self.default / 'state.json').read_bytes(), original)
        self.assertEqual(hm.state_transaction_blocker_names(self.default), [])

    def test_corrupt_missing_and_ambiguous_recovery_material_fail_closed(self):
        for mutation in ('corrupt-transaction', 'missing-candidate', 'symlink-candidate',
                         'ambiguous-control'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = (Path(directory) / 'repo').resolve()
                root.mkdir()
                harness = hm.Harness(root)
                harness.init('human:fixture')
                original = (root / '.texenda/state.json').read_bytes()
                pid = os.fork()
                if pid == 0:
                    def interrupt(stage, _harness, _detail):
                        if stage == 'state_write_after_exchange_fsync':
                            os._exit(76)
                    try:
                        hm.Harness(root, interleave=interrupt).admit('WP-00', 'fixture')
                    except BaseException:
                        os._exit(98)
                    os._exit(0)
                _pid, status = os.waitpid(pid, 0)
                self.assertEqual(os.WEXITSTATUS(status), 76)
                state_root = root / '.texenda'
                pending = state_root / hm.STATE_TRANSACTION_PENDING
                value = json.loads(pending.read_text())
                candidate = state_root / value['candidate_name']
                if mutation == 'corrupt-transaction':
                    pending.write_text('{}\n')
                elif mutation == 'missing-candidate':
                    candidate.unlink()
                elif mutation == 'symlink-candidate':
                    candidate.unlink()
                    candidate.symlink_to(state_root / 'state.json')
                else:
                    duplicate = state_root / ('.state-write-commit-cleanup-'
                                              + value['token'] + '.json')
                    duplicate.write_bytes(pending.read_bytes())
                recovery = hm.Harness(root, allow_state_recovery=True)
                with self.assertRaises(hm.Denied):
                    recovery.recover_state_write('human:owner', runtime_stopped=True)
                self.assertTrue(pending.is_file())
                self.assertNotEqual((state_root / 'state.json').read_bytes(), original)

    def test_state_transaction_schema_is_closed_and_identity_bound(self):
        self.hard_exit_admit('state_write_after_transaction_prepared')
        schema = json.loads(hm.STATE_TRANSACTION_SCHEMA.read_text())
        self.assertFalse(schema['additionalProperties'])
        self.assertEqual(set(schema['required']), hm.STATE_TRANSACTION_FIELDS)
        self.assertEqual(len(schema['allOf']), 3)
        pending = self.default / hm.STATE_TRANSACTION_PENDING
        original = json.loads(pending.read_text())
        recovery = hm.Harness(self.root, allow_state_recovery=True)
        mutations = [
            lambda value: value.update(extra='forbidden'),
            lambda value: value.update(token='../../escaped'),
            lambda value: value.update(repository_root=str(self.base)),
            lambda value: value['old_state']['identity'].update(inode=-1),
            lambda value: value['new_state'].update(sha256='0' * 63),
            lambda value: value.update(old_state=None),
            lambda value: value['binding'].update(kind='present'),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutations.index(mutate)):
                value = copy.deepcopy(original)
                mutate(value)
                with self.assertRaises(hm.Denied):
                    recovery._validate_state_transaction(value)
        result = recovery.recover_state_write('human:owner', runtime_stopped=True)
        self.assertEqual(result['outcome'], 'previous_state_restored')

    def test_recovery_cli_requires_owner_stop_and_uses_no_receipt_rewrite(self):
        original = (self.default / 'state.json').read_bytes()
        self.hard_exit_admit('state_write_after_exchange_fsync')
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(hm.main(['--root', str(self.root), 'recover-state-write',
                                     '--actor', 'human:owner']), 2)
            self.assertEqual(hm.main(['--root', str(self.root), 'recover-state-write',
                                     '--actor', 'human:owner', '--runtime-stopped']), 0)
        self.assertEqual((self.default / 'state.json').read_bytes(), original)
        self.assertEqual(len(json.loads(original)['events']), 1)

    def test_successful_state_transaction_leaves_sanitized_records_and_nonactive_checkpoint(self):
        self.harness.admit('WP-00', 'fixture')
        self.assertEqual(hm.state_transaction_blocker_names(self.default), [])
        archives = list(self.default.glob('state-write-committed-*.json'))
        self.assertGreaterEqual(len(archives), 2)  # init plus admit
        for archive in archives:
            value = json.loads(archive.read_text())
            self.assertEqual(value['schema_version'], hm.STATE_TRANSACTION_VERSION)
            self.assertNotIn('events', value)
            self.assertNotIn('tasks', value)
        checkpoints = list(self.default.glob('state-write-checkpoint-previous-*.json'))
        self.assertEqual(len(checkpoints), 1)
        self.assertEqual(len(json.loads(checkpoints[0].read_bytes())['events']), 1)
        intended = list(self.default.glob('state-write-checkpoint-intended-*.json'))
        self.assertEqual(len(intended), 2)
        active = self.default / 'state.json'
        self.assertTrue(all(path.stat().st_ino != active.stat().st_ino for path in intended))
        active_raw = active.read_bytes()
        intended[-1].write_bytes(b'synthetic non-active checkpoint mutation\n')
        self.assertEqual(active.read_bytes(), active_raw)
        self.assertFalse(any(path.name.startswith('.state-write-')
                             for path in self.default.iterdir()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
