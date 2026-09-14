"""Mapped-facade mutation, freshness, and read-only acceptance tests."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / '.agent/scripts'
sys.path.insert(0, str(SCRIPTS))
import common
import refresh
import validate


class FacadeUnitTests(unittest.TestCase):
    def test_duplicate_key_fixture_is_rejected(self):
        raw = (ROOT / '.agent/tests/fixtures/invalid/duplicate-key.json').read_bytes()
        with self.assertRaisesRegex(common.ValidationError, 'duplicate JSON key'):
            common.loads(raw)

    def test_nested_instruction_weakening_fixture_is_rejected(self):
        text = (ROOT / '.agent/tests/fixtures/invalid/nested-agent-weakening.md').read_text()
        with self.assertRaisesRegex(common.ValidationError, 'weaken'):
            validate.validate_nested_instruction_text(text)

    def test_kernel_and_origin_are_closed_and_truthful(self):
        values = validate.validate_kernel(ROOT)
        self.assertEqual(values['lifecycle.json']['scope'], 'generic_record_metadata_only')
        origin = validate.validate_origin(ROOT)
        self.assertEqual(origin['adoption_mode'], 'mapped-existing')
        self.assertFalse(origin['generated_new_project'])
        self.assertFalse(origin['newer_candidate']['qualified'])

    def test_no_second_task_decision_evidence_review_or_event_store(self):
        validate.validate_indexes(ROOT)
        self.assertFalse((ROOT / '.agent/events').exists())

    def test_extension_is_restrictions_only_and_hash_bound(self):
        validate.validate_extension(ROOT)
        extension = common.load_json(ROOT / '.agent/extensions/texenda-coordination/extension.json')
        self.assertFalse(extension['may_expand_authority'])
        self.assertFalse(extension['live_roster_copied'])

    def test_validation_registry_delegates_all_existing_suites(self):
        registry = validate.validate_registry(ROOT)
        ids = {row['id'] for row in registry['commands']}
        self.assertTrue({'workspace-contract', 'workspace-tests', 'coordination-tests',
                         'sealed-harness-tests', 'sealed-package-checksums',
                         'source-package-checksums', 'coordination-state-check'} <= ids)

    def test_crosswalk_has_single_owner_and_dossier_evidence_correction(self):
        crosswalk = validate.validate_crosswalk_correction(ROOT)
        self.assertTrue(crosswalk['blueprint']['origin_record_created'])
        self.assertEqual(len({row['concern_id'] for row in crosswalk['ownership']}),
                         len(crosswalk['ownership']))


class FacadeIntegratedFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.fixture = Path(cls.temporary.name).resolve() / 'repo'
        subprocess.run(['git', 'clone', '--quiet', '--no-hardlinks', str(ROOT), str(cls.fixture)],
                       check=True)
        for name in common.candidate_paths(ROOT):
            source = ROOT / name
            if not source.is_file() or source.is_symlink() or name.startswith('.agent/generated/'):
                continue
            destination = cls.fixture / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        subprocess.run(['git', 'config', 'user.name', 'Synthetic Facade Test'], cwd=cls.fixture, check=True)
        subprocess.run(['git', 'config', 'user.email', 'fixture@example.invalid'], cwd=cls.fixture, check=True)
        subprocess.run(['git', 'add', '-A'], cwd=cls.fixture, check=True)
        # The source may already be a fully committed final tip. An empty commit still
        # provides a deterministic fixture revision without weakening any copied-byte
        # or generated-source-scope assertion.
        subprocess.run(['git', 'commit', '--quiet', '--allow-empty',
                        '-m', 'synthetic mapped facade fixture'],
                       cwd=cls.fixture, check=True)
        harness_spec = importlib.util.spec_from_file_location(
            'fixture_harness', cls.fixture / 'tooling/coordination/harness.py')
        cls.harness_module = importlib.util.module_from_spec(harness_spec)
        harness_spec.loader.exec_module(cls.harness_module)
        cls.harness_module.Harness(cls.fixture).init('human:synthetic-fixture')
        refresh.refresh(cls.fixture)
        subprocess.run(['git', 'add', '-A'], cwd=cls.fixture, check=True)
        subprocess.run(['git', 'commit', '--quiet', '-m', 'synthetic generated baseline'],
                       cwd=cls.fixture, check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def setUp(self):
        subprocess.run(['git', 'reset', '--hard', '--quiet', 'HEAD'], cwd=self.fixture, check=True)
        marker = self.fixture / '.agent/generated/.refresh-in-progress'
        if marker.exists():
            marker.unlink()

    def tearDown(self):
        for name in ('.agent/tasks/active.json',
                     'docs/qualification/evidence/synthetic-untracked.tmp',
                     'synthetic-cache.pyc'):
            path = self.fixture / name
            if path.exists():
                path.unlink()

    def run_check(self):
        return subprocess.run(
            [sys.executable, '-B', '.agent/scripts/validate.py', '--check'],
            cwd=self.fixture, capture_output=True, text=True, check=False,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})

    def snapshot(self):
        rows = {}
        for path in sorted(self.fixture.rglob('*')):
            if '.git' in path.relative_to(self.fixture).parts or not path.is_file():
                continue
            raw = path.read_bytes()
            metadata = path.stat()
            rows[path.relative_to(self.fixture).as_posix()] = {
                'sha256': hashlib.sha256(raw).hexdigest(),
                'size': metadata.st_size,
                'mtime_ns': metadata.st_mtime_ns,
                'ctime_ns': metadata.st_ctime_ns,
            }
        return rows

    def test_check_is_read_only_for_tracked_untracked_ignored_generated_cache_lock_and_timestamps(self):
        (self.fixture / 'docs/qualification/evidence/synthetic-untracked.tmp').write_text(
            'synthetic untracked evidence-only file\n')
        cache = self.fixture / 'synthetic-cache.pyc'
        cache.write_bytes(b'synthetic ignored cache')
        before = self.snapshot()
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, self.snapshot())
        self.assertFalse(any(path.name == '__pycache__' for path in self.fixture.rglob('*')))

    def test_source_change_invalidates_generated_projection(self):
        policy = self.fixture / '.agent/policy.json'
        policy.write_text(policy.read_text() + '\n')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('stale', result.stderr)

    def test_interrupted_refresh_is_detected_and_recoverable(self):
        with self.assertRaisesRegex(RuntimeError, 'interrupted refresh'):
            refresh.refresh(self.fixture, fail_after=2)
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('interrupted refresh marker', result.stderr)
        refresh.refresh(self.fixture, recover_interrupted=True)
        self.assertEqual(self.run_check().returncode, 0)

    def test_private_fixture_is_excluded_without_content_fingerprinting(self):
        private = self.fixture / '.texenda/private-inputs/kit/synthetic.csv'
        private.parent.mkdir(parents=True)
        private.write_text('synthetic private fixture\n')
        names = {row['path'] for row in common.source_rows(self.fixture)}
        evidence_names = {row['path'] for row in common.evidence_rows(self.fixture)}
        self.assertNotIn(private.relative_to(self.fixture).as_posix(), names | evidence_names)

    def test_duplicate_owner_and_origin_overclaim_are_rejected(self):
        crosswalk_path = self.fixture / 'project-dossier/transition/blueprint-adoption-crosswalk.json'
        crosswalk = json.loads(crosswalk_path.read_text())
        crosswalk['ownership'].append(crosswalk['ownership'][0])
        crosswalk_path.write_text(json.dumps(crosswalk))
        with self.assertRaisesRegex(common.ValidationError, 'duplicate mutable concern'):
            validate.validate_crosswalk_correction(self.fixture)
        subprocess.run(['git', 'checkout', '--quiet', '--', str(crosswalk_path.relative_to(self.fixture))],
                       cwd=self.fixture, check=True)
        origin_path = self.fixture / '.project-blueprint-origin.json'
        origin = json.loads(origin_path.read_text())
        origin['generated_new_project'] = True
        origin_path.write_text(json.dumps(origin))
        with self.assertRaisesRegex(common.ValidationError, 'overclaims'):
            validate.validate_origin(self.fixture)

    def test_extension_escape_and_second_ledger_are_rejected(self):
        extension_path = self.fixture / '.agent/extensions/texenda-coordination/extension.json'
        extension = json.loads(extension_path.read_text())
        extension['bindings'][0]['path'] = '../outside'
        extension_path.write_text(json.dumps(extension))
        with self.assertRaisesRegex(common.ValidationError, 'escapes confined'):
            validate.validate_extension(self.fixture)
        (self.fixture / '.agent/tasks/active.json').write_text('{}')
        with self.assertRaisesRegex(common.ValidationError, 'second active record store'):
            validate.validate_indexes(self.fixture)


if __name__ == '__main__':
    unittest.main(verbosity=2)
