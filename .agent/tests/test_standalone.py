"""Standalone source, control-boundary and metadata mutation oracles."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.agent/scripts'))
import common
import operating
import refresh
import validate


def clone_sources(destination):
    subprocess.run(['git', 'clone', '--quiet', '--no-hardlinks', str(ROOT), str(destination)],
                   check=True)
    for name in common.candidate_paths(ROOT):
        common.reject_private_name(name, 'synthetic source fixture')
        if name in common.GENERATED_OUTPUT_PATHS:
            continue
        source = ROOT / name
        common.no_symlink_components(source.absolute(), 'synthetic source fixture')
        if source.is_file():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    subprocess.run(['git', '-c', 'user.name=Synthetic Standalone',
                    '-c', 'user.email=fixture@example.invalid', 'add', '-A'],
                   cwd=destination, check=True)
    subprocess.run(['git', '-c', 'user.name=Synthetic Standalone',
                    '-c', 'user.email=fixture@example.invalid', 'commit', '--quiet',
                    '--allow-empty', '-m', 'synthetic standalone source'],
                   cwd=destination, check=True)


def harness_module(root):
    spec = importlib.util.spec_from_file_location('standalone_fixture_harness',
                                                 root / 'tooling/coordination/harness.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bind_synthetic(root, module):
    module.Harness(root).init('human:synthetic')
    default = root / '.texenda'
    external = root.parent / 'local/agent-state/texenda'
    external.mkdir(parents=True)
    raw = (default / 'state.json').read_bytes()
    state = json.loads(raw)
    for name in ('state.json', 'state.lock'):
        os.rename(default / name, external / name)
    (root / '.texenda-location.json').write_text(json.dumps({
        'schema_version': 'texenda.state-location.v1', 'migration_id': 'synthetic-standalone',
        'repository_root': str(root), 'state_root': str(external), 'status': 'active',
        'baseline': {'state_sha256': hashlib.sha256(raw).hexdigest(),
                     'receipt_count': len(state['events']), 'receipt_tip': state['events'][-1]['hash']},
    }))
    return external


def snapshot(root):
    result = {}
    for path in [root, *sorted(root.rglob('*'))]:
        if '.git' in path.relative_to(root).parts:
            continue
        metadata = path.lstat()
        result[str(path.relative_to(root))] = (
            metadata.st_mode, metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns,
            hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None)
    return result


class StandaloneContracts(unittest.TestCase):
    def test_contract_references_existing_owners_and_required_deferrals(self):
        result = operating.validate_operating(ROOT)
        self.assertEqual(result['path_roles'], 19)
        self.assertEqual(result['remediation_items'], 18)
        self.assertEqual(result['retention_classes'], 7)

    def test_code_context_never_reads_binding_or_local_siblings(self):
        with mock.patch.object(common, 'binding', side_effect=AssertionError('binding read')), \
                mock.patch.object(common, 'ledger_facts', side_effect=AssertionError('ledger read')), \
                mock.patch.object(Path, 'is_file', side_effect=AssertionError('local sibling probe')):
            context = validate.execution_context(ROOT, scope='code')
        self.assertEqual(context['scope'], 'code')
        self.assertIsNone(context['project_home'])
        with self.assertRaisesRegex(common.ValidationError, 'rejects --state-root'):
            validate.execution_context(ROOT, Path('/unavailable/synthetic-state'), scope='code')

    def test_scope_registry_cannot_route_control_sources_or_refresh_into_code(self):
        original = common.load_json(ROOT / '.agent/validators.json')
        for target in ('source-package-checksums', 'coordination-state-check', 'facade-refresh'):
            changed = copy.deepcopy(original)
            next(row for row in changed['commands'] if row['id'] == target)['scopes'] = ['code', 'control']
            actual = validate.load_json

            def replaced(path, changed=changed):
                return changed if str(path).endswith('.agent/validators.json') else actual(path)

            with mock.patch.object(validate, 'load_json', side_effect=replaced), \
                    self.assertRaises(common.ValidationError):
                validate.validate_registry(ROOT)

    def test_discovery_cannot_be_refresh_writer_or_drift_from_registry(self):
        original = common.load_json(ROOT / '.agent/tools.json')
        for tool, command in (('facade-refresh', 'python3 -B .agent/scripts/refresh.py --refresh'),
                              ('facade-validator', 'python3 -B .agent/scripts/validate.py --check')):
            changed = copy.deepcopy(original)
            next(row for row in changed['tools'] if row['id'] == tool)['availability_check'] = command
            actual = validate.load_json

            def replaced(path, changed=changed):
                return changed if str(path).endswith('.agent/tools.json') else actual(path)

            with mock.patch.object(validate, 'load_json', side_effect=replaced), \
                    self.assertRaises(common.ValidationError):
                validate.validate_registry(ROOT)

    def test_retention_deferral_and_owner_mutations_fail(self):
        retention = common.load_json(ROOT / operating.RETENTION)
        remediation = common.load_json(ROOT / operating.REMEDIATION)
        mutations = [
            (operating.RETENTION, retention, lambda value: value.update(deletion_authority=True)),
            (operating.RETENTION, retention,
             lambda value: value.update(protected_receipt_retention_class='RET-0006')),
            (operating.RETENTION, retention, lambda value: value['classes'].pop()),
            (operating.REMEDIATION, remediation,
             lambda value: value['items'][5].update(selected_disposition='completed')),
            (operating.REMEDIATION, remediation,
             lambda value: value['items'][5]['deferred'].pop('blocker')),
            (operating.REMEDIATION, remediation, lambda value: value['items'].pop()),
        ]
        actual = operating.load_json
        for name, original, mutate in mutations:
            changed = copy.deepcopy(original)
            mutate(changed)

            def replaced(path, name=name, changed=changed):
                return changed if path == ROOT / name else actual(path)

            with self.subTest(path=name), mock.patch.object(operating, 'load_json', side_effect=replaced), \
                    self.assertRaises(common.ValidationError):
                operating.validate_operating(ROOT)
        for ref in (
            {'kind': 'repository', 'path': '../outside', 'scope': 'x', 'role': 'definition'},
            {'kind': 'repository', 'path': 'private-inputs/private.csv', 'scope': 'x', 'role': 'definition'},
            {'kind': 'bound_ledger', 'path': '.agent/project.json', 'scope': 'x', 'role': 'definition'},
        ):
            with self.assertRaises(common.ValidationError):
                operating.validate_reference(ROOT, ref)

    def test_composite_catalog_requires_all_scoped_current_sources(self):
        original = common.load_json(ROOT / 'project-dossier/ARTIFACT_CATALOG.json')
        changed = copy.deepcopy(original)
        row = next(row for row in changed['artifacts']
                   if row['owner_path'] == 'direct_git_build_and_harness_evidence')
        row['owner_refs'].pop()
        actual = operating.load_json

        def replaced(path):
            return changed if path == ROOT / 'project-dossier/ARTIFACT_CATALOG.json' else actual(path)

        with mock.patch.object(operating, 'load_json', side_effect=replaced), \
                self.assertRaisesRegex(common.ValidationError, 'complete'):
            operating.validate_operating(ROOT)
        crosswalk_path = ROOT / 'project-dossier/transition/blueprint-adoption-crosswalk.json'
        crosswalk = common.load_json(crosswalk_path)
        next(row for row in crosswalk['ownership']
             if row['concern_id'] == 'product_semantics')['owner_refs'].pop()

        def missing_amendment(path):
            return crosswalk if path == crosswalk_path else actual(path)

        with mock.patch.object(operating, 'load_json', side_effect=missing_amendment), \
                self.assertRaisesRegex(common.ValidationError, 'incomplete'):
            operating.owner_reference_sets(ROOT)

    def test_exact_supplemental_and_artifact_pair_coverage(self):
        sys.path.insert(0, str(ROOT / 'tooling/workspace'))
        import validate_contract as contract
        crosswalk, baseline, manifest = [common.load_json(ROOT / path)
                                        for path in (contract.CROSSWALK, contract.BASELINE, contract.MANIFEST)]
        for field, key in (('supplemental_mappings', 'mapped_path'),
                           ('supplemental_high_assurance_types', 'mapped_path'),
                           ('blueprint_artifact_type_inventory', 'path')):
            changed = copy.deepcopy(crosswalk)
            changed[field][0][key] = 'AGENTS.md'
            with self.subTest(field=field), self.assertRaises(contract.ContractError):
                contract.validate(changed, baseline, manifest, root=ROOT)

    def test_refresh_help_has_no_project_or_local_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / 'empty'
            scripts = root / '.agent/scripts'
            scripts.mkdir(parents=True)
            for name in ('common.py', 'operating.py', 'validate.py', 'refresh.py'):
                shutil.copy2(ROOT / '.agent/scripts' / name, scripts / name)
            before = snapshot(root)
            result = subprocess.run([sys.executable, '-B', str(scripts / 'refresh.py'), '--help'],
                                    capture_output=True, text=True, cwd=root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(before, snapshot(root))
            self.assertFalse((root / '.agent/generated').exists())
            self.assertFalse((root / '.texenda-location.json').exists())


class StandaloneEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='texenda-standalone-')
        cls.home = Path(cls.temporary.name).resolve()
        cls.root = cls.home / 'repo'
        clone_sources(cls.root)
        cls.module = harness_module(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    @unittest.skipIf(os.environ.get('TEXENDA_CHECK_ALL_ACTIVE') == '1',
                     'outer full check already runs suites; avoid recursive aggregation')
    def test_clean_clone_and_worktree_code_all_without_local_siblings(self):
        worktree = self.home / 'worktrees/source'
        subprocess.run(['git', 'worktree', 'add', '--quiet', '--detach', str(worktree), 'HEAD'],
                       cwd=self.root, check=True)
        for root in (self.root, worktree):
            before = snapshot(root)
            result = subprocess.run([sys.executable, '-B', '.agent/scripts/validate.py',
                                     '--check', '--scope', 'code', '--all'],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload['live_state_checked'])
            self.assertEqual(payload['generated_freshness'], 'unassessed')
            self.assertEqual(payload['control_validation'], 'unassessed')
            self.assertEqual(before, snapshot(root))
            self.assertFalse((root / '.texenda').exists())
            self.assertFalse((root / '.texenda-location.json').exists())
        for name in ('local', 'sources', 'archive', 'WORKSPACE.md'):
            self.assertFalse((self.home / name).exists())

    def test_control_denials_precede_ledger_read_and_preserve_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / 'repo'
            clone_sources(root)
            module = harness_module(root)
            with self.assertRaisesRegex(common.ValidationError, 'explicit'):
                common.control_context(root)
            empty = root.parent / 'empty-state'
            empty.mkdir()
            with self.assertRaisesRegex(common.ValidationError, 'binding'):
                common.control_context(root, empty)
            external = bind_synthetic(root, module)
            binding_path = root / '.texenda-location.json'
            original = binding_path.read_bytes()
            self.assertEqual(common.control_context(root, external)['scope'], 'control')
            for status in ('moving',):
                value = json.loads(original)
                value['status'] = status
                binding_path.write_text(json.dumps(value))
                with self.assertRaises(common.ValidationError):
                    common.control_context(root, external)
                binding_path.write_bytes(original)
            for state in (empty, Path('relative-state'), root.parent / 'missing-state'):
                with self.assertRaises(common.ValidationError):
                    common.control_context(root, state)
            alias = root.parent / 'state-alias'
            alias.symlink_to(external, target_is_directory=True)
            with self.assertRaises(common.ValidationError):
                common.control_context(root, alias)
            for marker in (root / '.texenda/state.json', external / '.state-write-transaction.json'):
                marker.write_text('synthetic blocker')
                before = snapshot(root.parent)
                with mock.patch.object(common, 'stable_bytes', side_effect=AssertionError('ledger read')), \
                        self.assertRaises(common.ValidationError):
                    common.control_context(root, external)
                self.assertEqual(before, snapshot(root.parent))
                marker.unlink()
            worktree = root.parent / 'worktrees/repo'
            subprocess.run(['git', 'worktree', 'add', '--quiet', '--detach', str(worktree), 'HEAD'],
                           cwd=root, check=True)
            with self.assertRaisesRegex(common.ValidationError, 'canonical'):
                common.control_context(worktree, external)
            for operation in (refresh.refresh, lambda r, s: refresh.refresh(r, s, recover_interrupted=True)):
                with self.assertRaises(common.ValidationError):
                    operation(worktree, external)
            # Canonical mutation remains valid; worktree inspection has an explicit read-only invocation.
            harness = module.Harness(root, state_root=external)
            first = harness.ready()[0]
            count = harness.status()['receipt_count']
            harness.admit(first, 'human:synthetic')
            self.assertNotIn(first, harness.ready())
            self.assertEqual(harness.status()['receipt_count'], count + 1)
            self.assertEqual(harness.ready(), [])  # Empty ready has no fallback.
            completed = json.loads((external / 'state.json').read_bytes())
            completed['tasks'][first]['state'] = 'completed'
            with mock.patch.object(harness, '_read', return_value=completed):
                ready = harness.ready()
            self.assertIn('WP-18', ready)
            self.assertEqual(harness.context(ready[-1])['routing'], harness.routes[ready[-1]])
            result = subprocess.run([sys.executable, '-B', str(root / 'tooling/coordination/harness.py'),
                                     '--root', str(root), '--state-root', str(external),
                                     '--read-only', 'ready'], cwd=worktree, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            detached = module.Harness(worktree, state_root=external)
            with self.assertRaises(module.Denied):
                detached.admit(ready[-1], 'human:synthetic')
            with self.assertRaises(module.Denied):
                detached.context(ready[-1], out='context.json')
            self.assertFalse((worktree / '.texenda').exists())
            self.assertFalse((worktree / '.texenda-location.json').exists())

    def test_read_only_flag_rejects_every_writer_before_harness_construction(self):
        revision = 'a' * 40
        commands = [
            ['init'], ['migrate-v1', '--actor', 'human:fixture'],
            ['rollback-v2', '--actor', 'human:fixture'],
            ['recover-state-write', '--actor', 'human:fixture'],
            *[[name, '--actor', 'human:fixture', '--record', 'record.json']
              + (['--usd', '0'] if name == 'set-budget' else [])
              for name in ('set-roster', 'record-gate', 'set-budget')],
            ['admit', 'WP-00'], ['assign', 'WP-00', '--agent', 'fixture'],
            ['start', 'WP-00', '--fence', '1'],
            ['checkpoint', 'WP-00', '--fence', '1', '--record', 'record.json'],
            ['submit', 'WP-00', '--fence', '1', '--record', 'record.json', '--candidate', revision],
            ['review', 'WP-00', '--record', 'record.json', '--candidate', revision],
            ['integrate', 'WP-00', '--record', 'record.json', '--candidate', revision, '--integrated', revision],
            ['complete', 'WP-00'],
            *[[name, 'WP-00', '--record', 'record.json'] for name in ('block', 'recover', 'cancel')],
            ['context', 'WP-00', '--out', 'context.json'],
        ]
        for command in commands:
            with self.subTest(command=command), \
                    mock.patch.object(self.module, 'Harness', side_effect=AssertionError('constructed')), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(self.module.main(['--root', str(self.root), '--read-only', *command]), 2)


if __name__ == '__main__':
    unittest.main()
