"""Synthetic failure and no-write oracles for the local planner interpretation."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / 'tooling/workspace/interpret_adoption.py'
spec = importlib.util.spec_from_file_location('texenda_adoption_interpreter', SCRIPT)
interpreter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(interpreter)


class AdoptionInterpreterTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='texenda-adoption-interpreter-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / 'repo'
        self.root.mkdir()
        self.crosswalk = json.loads((ROOT / interpreter.contract.CROSSWALK).read_text())
        # Only synthetic placeholder owner files are created. Fixed JSON inputs
        # come from tracked public contracts, never private or local ledger data.
        for row in self.crosswalk['mappings']:
            name = row['mapped_path']
            if not name or name.startswith('/'):
                continue
            path = self.root / name
            if name.endswith('/'):
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('synthetic owner fixture\n')
        for name in (
            interpreter.ORIGIN, interpreter.contract.CROSSWALK,
            interpreter.contract.BASELINE, interpreter.contract.MANIFEST,
            '.agent/schemas/project-blueprint-origin.v3.schema.json',
            '.agent/schemas/project-blueprint-origin.v2.schema.json',
            'docs/qualification/evidence/2026-09-15-editor-blueprint-followup-observations.evidence.json',
            'specs/texenda-handoff/01-foundation/authority-register.json',
        ):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / name).read_bytes())
        self.plan = {
            'schema_version': 'project-blueprint.adoption-plan.v1',
            'authority': 'Read-only untrusted observation, not permission.',
            'target': str(self.root), 'requested_profile': 'high-assurance',
            'blueprint_version': '1.0.0', 'existing': {},
            'origin': {'status': 'valid_shape_not_fully_validated', 'blueprint_version': None,
                       'profile': 'high-assurance', 'harness_kernel_version': None},
            'existing_top_level_names': [], 'required_sequence': [], 'non_transfer_rules': [],
            'collisions': [], 'candidate_new_paths': [],
        }
        for name in self.crosswalk['blueprint_path_inventory']:
            field = 'collisions' if (self.root / name).exists() else 'candidate_new_paths'
            self.plan[field].append(name)

    def rewrite(self, name, mutate):
        path = self.root / name
        value = json.loads(path.read_text())
        mutate(value)
        path.write_text(json.dumps(value))

    def reject(self, plan=None):
        with self.assertRaises((interpreter.ValidationError, interpreter.contract.ContractError)):
            interpreter.interpret(self.root, self.plan if plan is None else plan)

    def run_cli(self, *args, raw=None):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), '--root', str(self.root), *args],
                              input=raw, capture_output=True, cwd=self.root)

    def snapshot(self):
        rows = []
        for path in [self.root, *sorted(self.root.rglob('*'))]:
            metadata = path.lstat()
            value = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            rows.append((str(path.relative_to(self.root)), metadata.st_mode, metadata.st_size,
                         metadata.st_mtime_ns, metadata.st_ctime_ns, value))
        return rows

    def test_self_check_and_stock_view_preserve_origin_and_all_dispositions(self):
        local = interpreter.interpret(self.root)
        result = interpreter.interpret(self.root, self.plan)
        self.assertEqual(result['counts']['mapped_paths'], 85)
        self.assertEqual(sum(result['roles'].values()), 85)
        self.assertEqual(len(result['mapped_dispositions']), 85)
        self.assertEqual(result['stock_origin_observation'], self.plan['origin'])
        self.assertIsNone(local['stock_origin_observation'])
        self.assertFalse(local['stock_plan_validated'])
        self.assertEqual(result['selected_reference']['version'], '1.0.0')
        self.assertEqual(result['clean_candidate_observation']['qualification_checks'],
                         {'source_contracts': 'PASS', 'acceptance': 'PASS', 'full_validator': 'FAIL'})
        self.assertFalse(result['dirty_candidate_observation']['version_committed'])
        self.assertTrue(all(value is False for key, value in result['boundary'].items()
                            if key != 'authority'))
        self.assertEqual(result, interpreter.interpret(self.root, copy.deepcopy(self.plan)))

    def test_current_origin_rejects_schema_qualification_adoption_descriptor_and_seed_changes(self):
        path = self.root / interpreter.ORIGIN
        original = path.read_bytes()
        mutations = [
            lambda value: value.update(schema_version='unknown'),
            lambda value: value.update(selected_version='4.2.0'),
            lambda value: value.update(adoption_mode='generated-new-project'),
            lambda value: value.update(generated_new_project=True),
            lambda value: value.update(selected_reference_descriptor_sha256='0' * 64),
            lambda value: value.update(selected_source='/outside/private-inputs/secret.csv'),
            lambda value: value['clean_candidate'].update(qualified=True),
            lambda value: value['clean_candidate'].update(adopted=True),
            lambda value: value['dirty_checkout_observation'].update(version_committed=True),
            lambda value: value['upgrade_plan'].update(reviewed_seed='invented.json'),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                path.write_bytes(original)
                self.rewrite(interpreter.ORIGIN, mutate)
                self.reject()

    def test_wrong_stock_target_profile_version_schema_or_origin_is_rejected(self):
        for key, value in (('target', str(self.root.parent)), ('requested_profile', 'standard'),
                           ('blueprint_version', '4.2.0'), ('schema_version', 'unknown'),
                           ('origin', {'status': 'qualified'})):
            with self.subTest(key=key):
                plan = copy.deepcopy(self.plan)
                plan[key] = value
                self.reject(plan)

    def test_duplicate_missing_extra_overlap_and_wrong_presence_are_rejected(self):
        for case in ('duplicate', 'missing', 'extra', 'overlap', 'wrong_presence'):
            plan = copy.deepcopy(self.plan)
            if case == 'duplicate':
                plan['collisions'].append(plan['collisions'][0])
            elif case == 'missing':
                plan['candidate_new_paths'].pop()
            elif case == 'extra':
                plan['candidate_new_paths'].append('unmapped.json')
            elif case == 'overlap':
                plan['candidate_new_paths'].append(plan['collisions'][0])
            else:
                plan['candidate_new_paths'].append(plan['collisions'].pop())
            with self.subTest(case=case):
                self.reject(plan)

    def test_missing_mapping_unknown_role_and_false_epoch_are_rejected(self):
        name = interpreter.contract.CROSSWALK
        path = self.root / name
        original = path.read_bytes()
        for mutate in (lambda value: value['mappings'].pop(),
                       lambda value: value['mappings'][0].update(role='new_authority'),
                       lambda value: value.update(current_epoch='baseline')):
            path.write_bytes(original)
            self.rewrite(name, mutate)
            self.reject()

    def test_missing_physical_mapped_file_rejected_in_both_modes(self):
        (self.root / 'tooling/coordination/templates/ASSIGNMENT.md').unlink()
        with self.assertRaisesRegex(interpreter.ValidationError, 'mapped owner is missing'):
            interpreter.interpret(self.root)
        self.reject()
        result = self.run_cli('--check')
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'mapped owner is missing', result.stderr)

    def test_missing_physical_mapped_directory_is_rejected(self):
        path = self.root / 'tooling/coordination/templates'
        path.rename(path.with_name('retained-templates'))
        self.reject()

    def test_mapped_file_cannot_be_a_directory_or_symlink(self):
        path = self.root / 'tooling/coordination/templates/ASSIGNMENT.md'
        path.unlink()
        path.mkdir()
        with self.assertRaisesRegex(interpreter.ValidationError, 'wrong file/directory type'):
            interpreter.interpret(self.root)
        path.rmdir()
        path.symlink_to(self.root / 'AGENTS.md')
        self.reject()

    def test_mapped_directory_cannot_be_a_file_or_symlink(self):
        path = self.root / '.agent/tests'
        retained = path.with_name('retained-tests')
        path.rename(retained)
        path.write_text('synthetic wrong type')
        self.reject()
        path.unlink()
        path.symlink_to(retained, target_is_directory=True)
        self.reject()

    def test_archive_index_is_control_only_metadata_without_content_read(self):
        archive = self.root.parent / 'archive/checkpoints'
        # Repository-only interpretation succeeds with local archive absent.
        self.assertEqual(interpreter.interpret(self.root)['local_obligations'], 'unassessed')
        with self.assertRaises(interpreter.ValidationError):
            interpreter.local_contract(self.root, scope='control')
        archive.mkdir(parents=True)
        (archive / 'opaque-unread-file').write_text('synthetic archive payload')
        original = os.open

        def no_archive_open(path, flags, *args, **kwargs):
            self.assertFalse(str(path).startswith(str(archive)), 'archive payload opened')
            return original(path, flags, *args, **kwargs)

        with (mock.patch.object(os, 'open', side_effect=no_archive_open),
              mock.patch.object(Path, 'iterdir', side_effect=AssertionError('archive enumeration')),
              mock.patch.object(Path, 'rglob', side_effect=AssertionError('archive traversal'))):
            interpreter.local_contract(self.root, scope='control')

    def test_stock_lexical_escape_and_private_paths_are_rejected(self):
        for name in ('../outside', '/outside', '.agent/../outside', '.agent//empty',
                     '.agent/./dot', '.git/config', '.texenda/state.json',
                     'private-inputs/secret', 'private.csv', 'a\\b', 'a:b', 'nul\x00path'):
            with self.subTest(path=name):
                with self.assertRaises(interpreter.ValidationError):
                    interpreter.relative_name(name)
                plan = copy.deepcopy(self.plan)
                plan['candidate_new_paths'][0] = name
                self.reject(plan)

    def test_relative_or_symlink_repository_root_is_rejected(self):
        with self.assertRaises(interpreter.ValidationError):
            interpreter.interpret(Path('.'))
        alias = self.root.parent / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(interpreter.ValidationError):
            interpreter.interpret(alias)

    def test_stock_target_symlink_and_broken_symlink_are_rejected(self):
        path = self.root / self.plan['candidate_new_paths'][0]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(self.root / 'AGENTS.md')
        self.reject()
        path.unlink()
        path.symlink_to(self.root / 'missing-target')
        self.reject()

    def test_symlink_parent_is_rejected_before_reading_a_mapped_owner(self):
        path = self.root / '.agent/templates'
        path.symlink_to(self.root.parent, target_is_directory=True)
        self.reject()

    def test_mapped_path_private_traversal_and_external_escape_are_rejected(self):
        name = interpreter.contract.CROSSWALK
        path = self.root / name
        original = path.read_bytes()
        for value in ('../outside', 'private-inputs/secret.csv', '/outside/archive'):
            path.write_bytes(original)
            self.rewrite(name, lambda record: record['mappings'][0].update(mapped_path=value))
            self.reject()

    def test_malformed_duplicate_key_nonfinite_and_exponent_overflow_json_fail(self):
        for raw in (b'{', b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}',
                    b'{"a":-Infinity}', b'{"a":[1e999]}'):
            with self.subTest(raw=raw), self.assertRaises((ValueError, interpreter.ValidationError)):
                interpreter.strict_json(raw)
            self.assertEqual(self.run_cli('--stock-plan', '-', raw=raw).returncode, 2)

    def test_cli_rejects_output_apply_file_input_unknown_shape_and_oversize(self):
        for args in (('--check', '--output', 'new.json'), ('--check', '--apply'),
                     ('--stock-plan', 'input.json'), ('--check', '--stock-plan', '-')):
            self.assertEqual(self.run_cli(*args).returncode, 2)
        for raw in (b'null', b'[]', b'{}', b' ' * (interpreter.MAX_STOCK_BYTES + 1)):
            self.assertEqual(self.run_cli('--stock-plan', '-', raw=raw).returncode, 2)
        plan = copy.deepcopy(self.plan)
        plan['output'] = 'new.json'
        self.reject(plan)
        self.assertFalse((self.root / 'new.json').exists())

    def test_no_write_preserves_tracked_like_untracked_ignored_cache_lock_and_generated_fixtures(self):
        for name in ('untracked.txt', '.texenda/state.json', '.texenda/state.lock',
                     '__pycache__/retained.pyc', '.agent/generated/retained.tmp'):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'synthetic retained fixture')
        before = self.snapshot()
        result = self.run_cli('--check')
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        result = self.run_cli('--stock-plan', '-', raw=json.dumps(self.plan).encode())
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(before, self.snapshot())

    def test_self_check_never_executes_installed_source_or_reads_private_content(self):
        real_open = os.open
        real_run = subprocess.run

        def guarded_open(path, flags, *args, **kwargs):
            name = str(path)
            self.assertNotIn('private-inputs', name)
            self.assertFalse(name.endswith('.csv'))
            self.assertNotIn('/.codex/skills/', name)
            self.assertEqual(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC), 0)
            return real_open(path, flags, *args, **kwargs)

        def only_accepted_git_read(argv, *args, **kwargs):
            self.assertEqual(argv, ['git', '--no-optional-locks', 'show',
                                   interpreter.contract.ACCEPTED_MAPPING_REVISION + ':'
                                   + interpreter.contract.CROSSWALK])
            self.assertEqual(kwargs['cwd'], interpreter.contract.ROOT)
            return real_run(argv, *args, **kwargs)

        with mock.patch.object(os, 'open', side_effect=guarded_open), \
                mock.patch.object(subprocess, 'run', side_effect=only_accepted_git_read):
            interpreter.interpret(self.root)


if __name__ == '__main__':
    unittest.main()
