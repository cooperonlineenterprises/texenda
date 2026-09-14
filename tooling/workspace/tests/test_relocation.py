"""Portable negative tests for the opt-in physical audit's read boundary."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('relocation_audit',
                                             ROOT / 'tooling/workspace/validate_relocation.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class RelocationAuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def test_private_boundary_denied_before_content_open(self):
        for path in (self.root / 'private-inputs/opaque.txt', self.root / 'SUBSCRIBERS.CSV'):
            with self.subTest(path=path), patch.object(Path, 'read_bytes') as read:
                with self.assertRaises(audit.contract.ContractError):
                    audit.read_bytes(path)
                read.assert_not_called()

    def test_symlink_leaf_and_parent_denied_before_open(self):
        target = self.root / 'target'
        target.mkdir()
        (target / 'file').write_text('synthetic')
        (self.root / 'link').symlink_to(target, target_is_directory=True)
        for path in (self.root / 'link', self.root / 'link/file'):
            with self.subTest(path=path), patch.object(Path, 'read_bytes') as read:
                with self.assertRaises(audit.contract.ContractError):
                    audit.read_bytes(path)
                read.assert_not_called()

    def test_traversal_and_relative_path_denied(self):
        for path in (Path('relative'), self.root / 'child/../file'):
            with self.subTest(path=path), self.assertRaises(audit.contract.ContractError):
                audit.read_bytes(path)

    def test_inventory_preserves_preexisting_cache_files(self):
        (self.root / '__pycache__').mkdir()
        fixture = self.root / '__pycache__/synthetic.pyc'
        fixture.write_bytes(b'synthetic cache')
        self.assertEqual(audit.tree_rows(self.root), [{
            'path': '__pycache__/synthetic.pyc', 'sha256': audit.sha(b'synthetic cache')}])

    def test_source_byte_changes_and_extra_files_are_rejected(self):
        fixture = self.root / 'README.md'
        fixture.write_text('synthetic')
        rows = audit.tree_rows(self.root)
        baseline = {'filesystem': {'author_source_files': rows}}
        manifest = {'source_package_moves': [{
            'entry': 'README.md', 'type': 'file', 'sha256': rows[0]['sha256']}]}
        self.assertEqual(audit.verify_source(self.root, baseline, manifest), rows)
        fixture.write_text('changed')
        with self.assertRaises(audit.contract.ContractError):
            audit.verify_source(self.root, baseline, manifest)
        fixture.write_text('synthetic')
        (self.root / 'extra').write_text('synthetic')
        with self.assertRaises(audit.contract.ContractError):
            audit.verify_source(self.root, baseline, manifest)

    def test_missing_or_changed_state_denied_before_harness_import(self):
        expected = {'sha256': '0' * 64}
        with self.assertRaises(audit.contract.ContractError):
            audit.audit_state(self.root, expected)
        (self.root / '.texenda').mkdir()
        (self.root / '.texenda/state.json').write_text('{}')
        with self.assertRaises(audit.contract.ContractError):
            audit.audit_state(self.root, expected)

    def test_physical_audit_requires_explicit_local_arguments(self):
        result = subprocess.run(['python3', '-B', str(ROOT / 'tooling/workspace/validate_relocation.py')],
                                cwd=self.root, capture_output=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'--project-home', result.stderr)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
