"""Synthetic interruption/recovery tests for the local state relocation helper."""
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[3]
relocation = load_module('texenda_state_relocation', ROOT / 'tooling/workspace/relocate_state.py')
hm = relocation.coordination


class StateRelocationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.home = (Path(self.temporary.name) / 'home').resolve()
        self.repo = self.home / 'repo'
        self.repo.mkdir(parents=True)
        (self.repo / '.gitignore').write_text('.texenda/\n.texenda-location.json\n')
        (self.home / 'local/agent-state').mkdir(parents=True)
        (self.home / 'local/logs').mkdir(parents=True)
        self.state_root = self.home / 'local/agent-state/texenda'
        self.harness = hm.Harness(self.repo)
        self.harness.init('human:fixture')
        self.source_state = self.repo / '.texenda/state.json'
        self.original_state = self.source_state.read_bytes()
        self.private = self.repo / '.texenda/private-inputs'
        (self.private / 'kit/example').mkdir(parents=True)
        (self.private / 'kit/example/synthetic.csv').write_text('synthetic-only\n')

    def tearDown(self):
        self.temporary.cleanup()

    def prepare(self):
        return relocation.prepare(self.repo, self.state_root, 'synthetic-migration')

    def test_prepare_writes_closed_moving_marker_before_any_rename(self):
        result = self.prepare()
        self.assertEqual(result['status'], 'moving')
        self.assertEqual(self.source_state.read_bytes(), self.original_state)
        self.assertTrue(self.private.is_dir())
        self.assertFalse((self.state_root / 'state.json').exists())
        binding = json.loads((self.repo / hm.BINDING_NAME).read_text())
        self.assertEqual(set(binding), hm.BINDING_FIELDS)
        with self.assertRaisesRegex(hm.Denied, 'moving'):
            hm.Harness(self.repo, state_root=self.state_root)

    def test_apply_preserves_state_bytes_and_relocates_private_directory(self):
        self.prepare()
        result = relocation.apply(self.repo, self.state_root)
        self.assertEqual(result['status'], 'active')
        self.assertEqual((self.state_root / 'state.json').read_bytes(), self.original_state)
        self.assertFalse(self.source_state.exists())
        self.assertFalse(self.private.exists())
        self.assertTrue((self.home / 'local/private-inputs').is_dir())
        self.assertEqual(relocation.verify(self.repo, self.state_root)['status'], 'active')
        self.assertEqual(hm.Harness(self.repo, state_root=self.state_root).status()['version'], '2.0')

    def test_interrupted_after_state_resumes_without_copy_or_rewrite(self):
        self.prepare()
        with self.assertRaisesRegex(RuntimeError, 'state rename'):
            relocation.apply(self.repo, self.state_root, stop_after='state')
        self.assertFalse(self.source_state.exists())
        self.assertEqual((self.state_root / 'state.json').read_bytes(), self.original_state)
        self.assertEqual(json.loads((self.repo / hm.BINDING_NAME).read_text())['status'], 'moving')
        result = relocation.apply(self.repo, self.state_root)
        self.assertEqual(result['state_sha256'], hm.hashlib.sha256(self.original_state).hexdigest())

    def test_interrupted_after_private_can_reverse_rename_rollback(self):
        self.prepare()
        with self.assertRaisesRegex(RuntimeError, 'private-input'):
            relocation.apply(self.repo, self.state_root, stop_after='private')
        result = relocation.rollback(self.repo, self.state_root)
        self.assertEqual(result['status'], 'rolled_back')
        self.assertEqual(self.source_state.read_bytes(), self.original_state)
        self.assertTrue(self.private.is_dir())
        self.assertFalse((self.repo / hm.BINDING_NAME).exists())
        self.assertTrue(Path(result['binding_record']).is_file())
        self.assertEqual(hm.Harness(self.repo).status()['version'], '2.0')

    def test_both_or_neither_state_locations_fail_closed(self):
        self.prepare()
        (self.state_root / 'state.json').write_bytes(self.original_state)
        with self.assertRaisesRegex(hm.Denied, 'exactly one'):
            relocation.apply(self.repo, self.state_root)
        (self.state_root / 'state.json').unlink()
        self.source_state.unlink()
        with self.assertRaisesRegex(hm.Denied, 'exactly one'):
            relocation.apply(self.repo, self.state_root)

    def test_nonempty_or_existing_destinations_are_never_overwritten(self):
        self.state_root.mkdir()
        (self.state_root / 'occupied').write_text('keep')
        with self.assertRaisesRegex(hm.Denied, 'empty'):
            self.prepare()
        (self.state_root / 'occupied').unlink()
        (self.home / 'local/private-inputs').mkdir()
        with self.assertRaisesRegex(hm.Denied, 'destination already exists'):
            self.prepare()

    def test_private_symlink_is_denied_without_following_it(self):
        target = self.home / 'private-target'
        target.mkdir()
        os.rename(self.private, self.home / 'private-preserved')
        self.private.symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(hm.Denied, 'symlink alias'):
            self.prepare()

    def test_private_contents_are_not_opened_hashed_or_listed(self):
        original_iterdir = Path.iterdir
        original_read_bytes = Path.read_bytes
        original_read_text = Path.read_text
        protected = {self.private, self.home / 'local/private-inputs'}

        def guard_iterdir(path):
            if path in protected:
                raise AssertionError('private directory was listed')
            return original_iterdir(path)

        def guard_read_bytes(path):
            if any(parent in protected for parent in (path, *path.parents)):
                raise AssertionError('private content was read')
            return original_read_bytes(path)

        def guard_read_text(path, *args, **kwargs):
            if any(parent in protected for parent in (path, *path.parents)):
                raise AssertionError('private content was read')
            return original_read_text(path, *args, **kwargs)

        with mock.patch.object(Path, 'iterdir', guard_iterdir), \
                mock.patch.object(Path, 'read_bytes', guard_read_bytes), \
                mock.patch.object(Path, 'read_text', guard_read_text):
            self.prepare()
            relocation.apply(self.repo, self.state_root)

    def test_held_lock_blocks_apply_and_leaves_moving_marker(self):
        self.prepare()
        lock = self.repo / '.texenda/state.lock'
        with lock.open('a+') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(hm.Denied, 'held'):
                relocation.apply(self.repo, self.state_root)
            fcntl.flock(stream, fcntl.LOCK_UN)
        self.assertEqual(json.loads((self.repo / hm.BINDING_NAME).read_text())['status'], 'moving')
        # The state rename completed first; resume uses the verified destination.
        self.assertEqual(relocation.apply(self.repo, self.state_root)['status'], 'active')

    def test_held_source_lock_blocks_prepare_before_baseline_marker(self):
        lock = self.repo / '.texenda/state.lock'
        with lock.open('a+') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(hm.Denied, 'held'):
                self.prepare()
            fcntl.flock(stream, fcntl.LOCK_UN)
        self.assertFalse((self.repo / hm.BINDING_NAME).exists())
        self.assertTrue(self.source_state.exists())

    def test_changed_state_after_prepare_stops_before_rename(self):
        self.prepare()
        state = json.loads(self.source_state.read_text())
        state['events'][0]['actor'] = 'tampered'
        self.source_state.write_text(json.dumps(state))
        with self.assertRaises(hm.Denied):
            relocation.apply(self.repo, self.state_root)
        self.assertTrue(self.source_state.exists())
        self.assertFalse((self.state_root / 'state.json').exists())

    def test_unsafe_migration_ids_are_rejected_before_marker_or_move(self):
        for value in ('../../escaped', 'nested/name', '.', 'a' * 65, ''):
            with self.subTest(value=value), self.assertRaisesRegex(hm.Denied, 'migration_id'):
                relocation.prepare(self.repo, self.state_root, value)
            self.assertFalse((self.repo / hm.BINDING_NAME).exists())
            self.assertTrue(self.source_state.exists())

    def test_atomic_exclusive_rename_preserves_concurrent_file_destination(self):
        source = self.home / 'source.txt'
        destination = self.home / 'destination.txt'
        source.write_text('source')

        def race(_source, target):
            target.write_text('concurrent')

        with self.assertRaisesRegex(hm.Denied, 'destination already exists'):
            relocation.rename_no_replace(source, destination, 'file race', race_hook=race)
        self.assertEqual(source.read_text(), 'source')
        self.assertEqual(destination.read_text(), 'concurrent')

    def test_atomic_exclusive_rename_preserves_concurrent_directory_destination(self):
        source = self.home / 'source-dir'
        destination = self.home / 'destination-dir'
        source.mkdir()

        def race(_source, target):
            target.mkdir()

        with self.assertRaisesRegex(hm.Denied, 'destination already exists'):
            relocation.rename_no_replace(source, destination, 'directory race', race_hook=race)
        self.assertTrue(source.is_dir())
        self.assertTrue(destination.is_dir())

    def test_missing_platform_exclusive_primitive_fails_without_move(self):
        source = self.home / 'primitive-source.txt'
        destination = self.home / 'primitive-destination.txt'
        source.write_text('preserve')
        with mock.patch.object(relocation, '_exclusive_rename_syscall',
                               side_effect=hm.Denied('platform lacks primitive')):
            with self.assertRaisesRegex(hm.Denied, 'lacks primitive'):
                relocation.rename_no_replace(source, destination, 'primitive')
        self.assertEqual(source.read_text(), 'preserve')
        self.assertFalse(destination.exists())

    def test_apply_race_never_overwrites_concurrent_state_destination(self):
        self.prepare()

        def race(_source, target):
            target.write_text('concurrent destination')

        with self.assertRaisesRegex(hm.Denied, 'destination already exists'):
            relocation.apply(self.repo, self.state_root, race_hooks={'state': race})
        self.assertEqual(self.source_state.read_bytes(), self.original_state)
        self.assertEqual((self.state_root / 'state.json').read_text(), 'concurrent destination')
        self.assertEqual(json.loads((self.repo / hm.BINDING_NAME).read_text())['status'], 'moving')

    def test_resume_rejects_a_held_destination_lock(self):
        self.prepare()
        with self.assertRaisesRegex(RuntimeError, 'lock rename'):
            relocation.apply(self.repo, self.state_root, stop_after='lock')
        destination_lock = self.state_root / 'state.lock'
        with destination_lock.open('a+') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(hm.Denied, 'held'):
                relocation.apply(self.repo, self.state_root)
            fcntl.flock(stream, fcntl.LOCK_UN)
        self.assertEqual(relocation.apply(self.repo, self.state_root)['status'], 'active')

    def test_apply_holds_destination_lock_through_private_move_and_activation(self):
        self.prepare()
        observations = []

        def probe(stage, paths, _raw):
            if stage != 'after_private':
                return
            descriptor = os.open(paths['destination_lock'], os.O_RDWR)
            try:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                observations.append('held')
            finally:
                os.close(descriptor)

        self.assertEqual(relocation.apply(self.repo, self.state_root, interleave=probe)['status'],
                         'active')
        self.assertEqual(observations, ['held'])

    def test_divergent_store_interleaving_never_activates_binding(self):
        self.prepare()

        def diverge(stage, paths, raw):
            if stage == 'after_state':
                paths['source_state'].write_bytes(raw)

        with self.assertRaisesRegex(hm.Denied, 'default active state'):
            relocation.apply(self.repo, self.state_root, interleave=diverge)
        self.assertTrue(self.source_state.exists())
        self.assertTrue((self.state_root / 'state.json').exists())
        self.assertEqual(json.loads((self.repo / hm.BINDING_NAME).read_text())['status'], 'moving')

    def test_source_and_ancestor_substitution_after_prepare_fail_closed(self):
        self.prepare()
        preserved = self.home / 'private-preserved-after-prepare'
        os.rename(self.private, preserved)
        self.private.symlink_to(preserved, target_is_directory=True)
        with self.assertRaisesRegex(hm.Denied, 'symlink alias'):
            relocation.apply(self.repo, self.state_root)

    def test_binding_substitution_before_activation_is_detected(self):
        self.prepare()

        def substitute(stage, paths, _raw):
            if stage == 'after_private':
                value = json.loads(paths['binding'].read_text())
                value['migration_id'] = 'synthetic-substitution'
                paths['binding'].write_text(json.dumps(value))

        with self.assertRaisesRegex(hm.Denied, 'binding changed'):
            relocation.apply(self.repo, self.state_root, interleave=substitute)
        self.assertEqual(json.loads((self.repo / hm.BINDING_NAME).read_text())['status'], 'moving')

    def test_binding_activation_exchange_preserves_a_raced_valid_descriptor(self):
        self.prepare()
        raced = {}

        def race(binding_path, _unused):
            value = json.loads(binding_path.read_text())
            value['migration_id'] = 'synthetic-raced-binding'
            replacement = binding_path.with_name('.synthetic-raced-binding')
            replacement.write_text(json.dumps(value))
            os.replace(replacement, binding_path)
            raced['raw'] = binding_path.read_bytes()

        with self.assertRaisesRegex(hm.Denied, 'raced state binding'):
            relocation.apply(self.repo, self.state_root, race_hooks={'binding_swap': race})
        self.assertEqual((self.repo / hm.BINDING_NAME).read_bytes(), raced['raw'])
        self.assertEqual(json.loads(raced['raw'])['status'], 'moving')
        conflicts = list((self.home / 'local/logs/workspace-relocation').glob(
            'synthetic-migration.activation-conflict.*.json'))
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(json.loads(conflicts[0].read_text())['status'], 'active')
        # Recovery uses the preserved raced moving descriptor; nothing was discarded.
        self.assertEqual(relocation.apply(self.repo, self.state_root)['status'], 'active')

    def test_binding_activation_interruption_rolls_back_and_resumes(self):
        self.prepare()
        interrupted = [False]

        def interrupt(stage, _paths, _raw):
            if stage == 'binding_after_exchange' and not interrupted[0]:
                interrupted[0] = True
                raise RuntimeError('synthetic activation interruption')

        with self.assertRaisesRegex(RuntimeError, 'activation interruption'):
            relocation.apply(self.repo, self.state_root, interleave=interrupt)
        binding = json.loads((self.repo / hm.BINDING_NAME).read_text())
        self.assertEqual(binding['status'], 'moving')
        conflicts = list((self.home / 'local/logs/workspace-relocation').glob(
            'synthetic-migration.activation-conflict.*.json'))
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(relocation.apply(self.repo, self.state_root)['status'], 'active')

    def test_persisted_post_exchange_transaction_is_recovered_under_lock(self):
        self.prepare()
        with self.assertRaisesRegex(RuntimeError, 'private-input'):
            relocation.apply(self.repo, self.state_root, stop_after='private')
        binding_path = self.repo / hm.BINDING_NAME
        moving_raw = binding_path.read_bytes()
        moving = json.loads(moving_raw)
        active_raw = (json.dumps(dict(moving, status='active'), indent=2,
                                 ensure_ascii=False, allow_nan=False).encode() + b'\n')
        token = 'a' * 16
        temporary_name = '.texenda-location.activation-' + token
        recovery = self.home / 'local/logs/workspace-relocation'
        recovery.mkdir(exist_ok=True)
        transaction = {
            'schema_version': 'texenda.state-location-activation.v1',
            'migration_id': 'synthetic-migration',
            'temporary_name': temporary_name,
            'expected_moving_sha256': relocation.sha(moving_raw),
            'candidate_active_sha256': relocation.sha(active_raw),
            'token': token,
        }
        (recovery / 'synthetic-migration.activation-transaction.json').write_text(
            json.dumps(transaction, indent=2, sort_keys=True) + '\n')
        (self.repo / temporary_name).write_bytes(active_raw)
        flags = os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0)
        descriptor = os.open(self.repo, flags)
        try:
            relocation._exchange_rename_syscall(
                descriptor, temporary_name, descriptor, hm.BINDING_NAME)
        finally:
            os.close(descriptor)
        self.assertEqual(json.loads(binding_path.read_text())['status'], 'active')
        result = relocation.apply(self.repo, self.state_root)
        self.assertEqual(result['status'], 'active')
        self.assertEqual(json.loads(binding_path.read_text())['status'], 'active')
        self.assertTrue(list(recovery.glob('synthetic-migration.activation-conflict.*.json')))

    def test_rollback_parent_symlink_substitution_is_denied_before_moves(self):
        self.prepare()
        with self.assertRaisesRegex(RuntimeError, 'private-input'):
            relocation.apply(self.repo, self.state_root, stop_after='private')
        logs = self.home / 'local/logs'
        preserved = self.home / 'logs-preserved'
        os.rename(logs, preserved)
        logs.symlink_to(preserved, target_is_directory=True)
        with self.assertRaisesRegex(hm.Denied, 'symlink'):
            relocation.rollback(self.repo, self.state_root)
        self.assertTrue((self.state_root / 'state.json').exists())

    def test_rollback_binding_record_race_preserves_concurrent_destination(self):
        self.prepare()
        with self.assertRaisesRegex(RuntimeError, 'private-input'):
            relocation.apply(self.repo, self.state_root, stop_after='private')

        def race(_source, destination):
            destination.write_text('concurrent rollback record')

        with self.assertRaisesRegex(hm.Denied, 'destination already exists'):
            relocation.rollback(self.repo, self.state_root, race_hooks={'binding': race})
        self.assertTrue((self.repo / hm.BINDING_NAME).is_file())
        record = self.home / 'local/logs/workspace-relocation/synthetic-migration.rolled-back.json'
        self.assertEqual(record.read_text(), 'concurrent rollback record')

    def test_descriptor_relative_rename_blocks_late_ancestor_redirection_for_every_type(self):
        original_syscall = relocation._exclusive_rename_syscall
        for label, is_directory in (
                ('state', False), ('lock', False), ('private', True), ('binding', False)):
            with self.subTest(label=label):
                base = self.home / ('late-' + label)
                source_parent = base / 'source'
                destination_parent = base / 'destination'
                unrelated = base / 'unrelated'
                source_parent.mkdir(parents=True)
                destination_parent.mkdir()
                unrelated.mkdir()
                source = source_parent / label
                destination = destination_parent / label
                unrelated_source = unrelated / label
                if is_directory:
                    source.mkdir()
                    (source / 'reviewed.txt').write_text('reviewed')
                    unrelated_source.mkdir()
                    (unrelated_source / 'unrelated.txt').write_text('unrelated')
                else:
                    source.write_text('reviewed')
                    unrelated_source.write_text('unrelated')
                preserved = base / 'preserved-source'

                def late_swap(*arguments):
                    os.rename(source_parent, preserved)
                    source_parent.symlink_to(unrelated, target_is_directory=True)
                    original_syscall(*arguments)

                with mock.patch.object(relocation, '_exclusive_rename_syscall',
                                       side_effect=late_swap):
                    with self.assertRaisesRegex(hm.Denied, 'syscall boundary'):
                        relocation.rename_no_replace(source, destination, label)
                if is_directory:
                    self.assertEqual((destination / 'reviewed.txt').read_text(), 'reviewed')
                    self.assertEqual((unrelated_source / 'unrelated.txt').read_text(), 'unrelated')
                else:
                    self.assertEqual(destination.read_text(), 'reviewed')
                    self.assertEqual(unrelated_source.read_text(), 'unrelated')


if __name__ == '__main__':
    unittest.main(verbosity=2)
