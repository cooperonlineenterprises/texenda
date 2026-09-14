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


if __name__ == '__main__':
    unittest.main(verbosity=2)
