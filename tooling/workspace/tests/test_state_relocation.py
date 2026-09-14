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
        with self.assertRaisesRegex(hm.Denied, 'non-symlink directory'):
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

    def test_changed_state_after_prepare_stops_before_rename(self):
        self.prepare()
        state = json.loads(self.source_state.read_text())
        state['events'][0]['actor'] = 'tampered'
        self.source_state.write_text(json.dumps(state))
        with self.assertRaises(hm.Denied):
            relocation.apply(self.repo, self.state_root)
        self.assertTrue(self.source_state.exists())
        self.assertFalse((self.state_root / 'state.json').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
