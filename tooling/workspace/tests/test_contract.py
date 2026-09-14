"""Mutation oracles for consequential adoption and move-plan boundaries."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('workspace_contract', ROOT / 'tooling/workspace/validate_contract.py')
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)


class WorkspaceContractTests(unittest.TestCase):
    def setUp(self):
        self.crosswalk, self.baseline, self.manifest = [
            contract.loads((ROOT / p).read_text())
            for p in (contract.CROSSWALK, contract.BASELINE, contract.MANIFEST)]

    def reject(self):
        with self.assertRaises(contract.ContractError):
            contract.validate(self.crosswalk, self.baseline, self.manifest)

    def test_complete_mapped_contract(self):
        result = contract.validate(self.crosswalk, self.baseline, self.manifest)
        self.assertEqual((result['blueprint_paths'], result['source_moves']), (85, 16))

    def test_all_qualification_pass_fail_checks_have_evidence_hashes(self):
        self.assertGreater(contract.verify_qualification_checks(ROOT), 0)

    def test_review_successor_preserves_exact_rejected_json_and_review_semantics(self):
        name = 'docs/qualification/evidence/2026-09-14-workspace-architecture-review.evidence.json'
        archived = ROOT / 'docs/qualification/evidence/history/2026-09-14-workspace-architecture-review.rejected.json.txt'
        original = subprocess.check_output(['git', 'show',
            '666b6da286bacbd7e02d6d3ca27b3e6c2aa81b1a:' + name], cwd=ROOT)
        self.assertEqual(archived.read_bytes(), original)
        successor = contract.loads((ROOT / name).read_text())
        metadata = successor.pop('compatibility_correction')
        self.assertEqual(metadata['prior_record']['sha256'], contract.sha(original))
        self.assertFalse(metadata['this_successor_or_containing_commit_independently_approved'])
        self.assertEqual(len(successor['checks']), 15)
        for check in successor['checks']:
            self.assertEqual(check.pop('evidence_path'), successor['review_document']['path'])
            self.assertEqual(check.pop('sha256'), successor['review_document']['sha256'])
        self.assertEqual(successor, contract.loads(original))
        self.assertEqual(contract.sha((ROOT / successor['review_document']['path']).read_bytes()),
                         '29f8e8ed2c6bee02abcfd49697ac5656b41cbb1519285121654b16cebc5500be')

    def test_qualification_pass_and_fail_require_path_and_hash(self):
        for status in ('PASS', 'FAIL'):
            with self.subTest(status=status):
                with self.assertRaises(contract.ContractError):
                    contract.verify_qualification_check(ROOT, {'status': status})
                with self.assertRaises(contract.ContractError):
                    contract.verify_qualification_check(ROOT, {'status': status, 'evidence_path': 'AGENTS.md'})

    def test_qualification_evidence_hash_mismatch_rejected(self):
        with self.assertRaises(contract.ContractError):
            contract.verify_qualification_check(ROOT, {
                'status': 'PASS', 'evidence_path': 'AGENTS.md', 'sha256': '0' * 64})

    def test_qualification_missing_file_rejected(self):
        with self.assertRaises(contract.ContractError):
            contract.verify_qualification_check(ROOT, {
                'status': 'FAIL', 'evidence_path': 'docs/qualification/missing-evidence.fixture',
                'sha256': '0' * 64})

    def test_qualification_absolute_traversal_and_private_paths_rejected(self):
        for path in ('/private/tmp/outside', '../outside', '.texenda/private-inputs/example.csv'):
            with self.subTest(path=path), self.assertRaises(contract.ContractError):
                contract.verify_qualification_check(ROOT, {
                    'status': 'PASS', 'evidence_path': path, 'sha256': '0' * 64})

    def test_operations_owner_matches_sealed_authority_register(self):
        register = contract.loads((ROOT / 'specs/texenda-handoff/01-foundation/authority-register.json').read_text())
        owners = [row['path'] for row in register['current_normative_owners']
                  if row['topic'] == 'operations-procedures']
        self.assertEqual(owners, ['04-security-governance-and-operations/runbooks.md'])
        expected = 'specs/texenda-handoff/' + owners[0]
        concern = next(row for row in self.crosswalk['ownership']
                       if row['concern_id'] == 'operations_recovery')
        self.assertEqual(set(concern['owner_by_epoch'].values()), {expected})
        artifact = next(row for row in self.crosswalk['blueprint_artifact_type_inventory']
                        if row['id'] == 'OPS-0001')
        mapping = next(row for row in self.crosswalk['mappings']
                       if row['blueprint_path'] == artifact['path'])
        self.assertEqual((mapping['mapped_path'], mapping['role']), (expected, 'index'))

    def test_operations_owner_rejects_migration_directory_in_every_epoch(self):
        concern = next(row for row in self.crosswalk['ownership']
                       if row['concern_id'] == 'operations_recovery')
        for epoch in self.crosswalk['epochs']:
            with self.subTest(epoch=epoch):
                original = concern['owner_by_epoch'][epoch]
                concern['owner_by_epoch'][epoch] = 'specs/texenda-handoff/06-migration-and-production/'
                self.reject()
                concern['owner_by_epoch'][epoch] = original

    def test_ops_artifact_rejects_migration_directory(self):
        mapping = next(row for row in self.crosswalk['mappings']
                       if row['blueprint_path'] == 'project-dossier/operations/README.md')
        mapping['mapped_path'] = 'specs/texenda-handoff/06-migration-and-production/'
        self.reject()

    def test_duplicate_json_keys(self):
        with self.assertRaises(contract.ContractError):
            contract.loads('{"owner":"a","owner":"b"}')

    def test_nonfinite_json(self):
        with self.assertRaises(contract.ContractError):
            contract.loads('{"budget":NaN}')

    def test_duplicate_concern_owner(self):
        self.crosswalk['ownership'].append(copy.deepcopy(self.crosswalk['ownership'][0]))
        self.reject()

    def test_two_owner_paths_in_one_epoch(self):
        self.crosswalk['ownership'][0]['owner_by_epoch']['facade'] = ['specs/', 'project-dossier/canonical/']
        self.reject()

    def test_second_authoritative_path(self):
        row = next(r for r in self.crosswalk['mappings'] if r['blueprint_path'] == '.agent/tasks/README.md')
        row['role'] = 'authoritative'
        self.reject()

    def test_second_live_task_roster_receipt_decision_evidence_owner(self):
        for concern in ('active_tasks', 'live_qualification', 'receipts', 'durable_decisions',
                        'qualification_evidence', 'review_records', 'model_routing'):
            with self.subTest(concern=concern):
                original = copy.deepcopy(self.crosswalk)
                row = next(r for r in self.crosswalk['ownership'] if r['concern_id'] == concern)
                row['owner_by_epoch']['external_state'] = '.agent/' + concern + '.json'
                self.reject()
                self.crosswalk = original

    def test_missing_artifact_mapping(self):
        self.crosswalk['mappings'].pop()
        self.reject()

    def test_false_generated_adoption(self):
        self.crosswalk['adoption_mode'] = 'generated-new-project'
        self.reject()

    def test_false_source_qualification(self):
        self.crosswalk['blueprint']['newer_candidate_qualified'] = True
        self.reject()

    def test_premature_root_cutover(self):
        row = next(r for r in self.crosswalk['ownership'] if r['concern_id'] == 'precedence_trust')
        row['owner_by_epoch']['baseline'] = '.agent/context.json'
        self.reject()

    def test_unbound_projection(self):
        self.crosswalk['projection_contract']['required_fields'].remove('ledger_sha256')
        self.reject()

    def test_check_cannot_refresh(self):
        self.crosswalk['projection_contract']['check_writes'] = True
        self.reject()

    def test_source_variant_cannot_replace_sealed_authority(self):
        self.baseline['packages']['source']['role'] = 'implementation_repository_sealed_authority'
        self.reject()

    def test_source_difference_cannot_be_erased(self):
        self.baseline['packages']['differing_paths'].pop()
        self.reject()

    def test_private_content_access_hash_parse_copy_denied(self):
        for key in ('contents_accessed', 'contents_hashed', 'contents_parsed', 'contents_copied'):
            with self.subTest(key=key):
                self.baseline['private_input'][key] = True
                self.reject()
                self.baseline['private_input'][key] = False

    def test_private_file_cannot_enter_hash_scope(self):
        self.baseline['filesystem']['author_source_files'].append(
            {'path': '.texenda/private-inputs/subscribers.csv', 'sha256': '0' * 64})
        self.reject()

    def test_every_source_top_level_entry_preserved(self):
        self.manifest['source_package_moves'].pop()
        self.reject()

    def test_move_target_traversal_or_other_project_denied(self):
        for path in ('/Users/jamesryancooper/Projects/other', contract.HOME + '/sources/../../other'):
            with self.subTest(path=path):
                self.manifest['source_package_moves'][0]['destination'] = path
                self.reject()

    def test_no_delete_overwrite_symlink_or_external_effect(self):
        for key in ('delete', 'overwrite', 'symlink_bridge', 'remote_mutation', 'receipt_rewrite'):
            with self.subTest(key=key):
                self.manifest['constraints'][key] = True
                self.reject()
                self.manifest['constraints'][key] = False

    def test_repo_destination_not_created_first(self):
        self.manifest['create_directories'].append(contract.HOME + '/repo')
        self.reject()

    def test_legacy_receipt_inputs_retained(self):
        self.manifest['external_state_cutover']['historical_compatibility_retained'].pop()
        self.reject()

    def test_active_state_move_cannot_take_whole_legacy_directory(self):
        self.manifest['external_state_cutover']['active_moves'][0]['source'] = contract.HOME + '/repo/.texenda'
        self.reject()

    def test_missing_source_not_treated_as_completed_move(self):
        self.manifest['recovery']['never_infer_completed_from_missing_source'] = False
        self.reject()

    def test_checkpoint_move_cannot_escape_scope(self):
        self.manifest['checkpoint_archive']['destination'] = '/Users/jamesryancooper/Projects/other'
        self.reject()

    def test_state_binding_cannot_select_another_root(self):
        self.manifest['external_state_cutover']['explicit_state_root'] = '/private/tmp/other-state'
        self.reject()

    def test_author_cannot_be_own_required_reviewer(self):
        self.crosswalk['facade_acceptance']['reviewer_distinct_from_author_and_integrator'] = False
        self.reject()


if __name__ == '__main__':
    unittest.main()
