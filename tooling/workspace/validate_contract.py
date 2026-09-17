#!/usr/bin/env python3
"""Read-only static validation of the mapped workspace transition contract.

This does not execute moves, inspect private inputs, validate live state,
activate ownership, qualify a runtime, or approve a candidate.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tomllib
import urllib.parse

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.agent/scripts'))
import operating
from common import control_context, ValidationError
BASELINE = 'docs/qualification/evidence/2026-09-14-workspace-phase-0-baseline.json'
CROSSWALK = 'project-dossier/transition/blueprint-adoption-crosswalk.json'
MANIFEST = 'project-dossier/transition/workspace-move-manifest.json'
HOME = '/Users/jamesryancooper/Projects/texenda'
OLD = '/Users/jamesryancooper/Projects/texenda-app'
ROLES = {'authoritative', 'adapter', 'index', 'generated_view',
         'historical_source', 'deferred', 'not_applicable'}
DIFFERENCES = {
    '01-foundation/adr-index.md', '01-foundation/adr-set.md',
    '03-domain-and-architecture/content.md',
    '03-domain-and-architecture/technology-baseline.md',
    '05-implementation/compatibility-manifest.template.json',
    '05-implementation/work-breakdown.md', '05-implementation/work-packages.json',
    '09-reference/source-register.json', '09-reference/source-register.md',
    'DECISION-STATUS.md', 'SHA256SUMS',
}
LEGACY = {
    '.texenda/evidence/', '.texenda/context/',
    '.texenda/state.v1.a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a.json',
}
COMPLETED_TRANSITION_HISTORY = (
    'project-dossier/history/2026-09-15-workspace-transition-completed.md'
)
COMPLETED_TRANSITION_SHA256 = (
    '1f5b0b1aa816f6bcd34f591a0b5f9f5b4e9d6e8bf35474ca77367418fb930919'
)
ORDINARY_STATE_ROOT = HOME + '/local/agent-state/texenda'
ORDINARY_VALIDATION = operating.CONTROL_COMMAND
ORDINARY_COORDINATOR = operating.COORDINATOR_COMMAND
CROSSWALK_PREDECESSOR_REVISION = '700565cd829871b04bde87e485c25d802505192c'
CROSSWALK_PREDECESSOR_SHA256 = '689d5ffedb15938b25679c0cb9215bd7cac850b3b8f09e257a0f7a0c4fade00e'
ACCEPTED_MAPPING_REVISION = '7de052690bbf3e2879f375c2b2e17207c7ee5bfe'
COMPATIBILITY_INPUTS = {
    '.texenda/context/WP-00.json',
    '.texenda/evidence/wp00-integration-verification.log',
    '.texenda/evidence/wp00-integration.evidence.json',
    '.texenda/state.v1.a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a.json',
}


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def loads(raw):
    def invalid(value):
        raise ContractError('nonfinite JSON value: ' + value)
    return json.loads(raw, object_pairs_hook=unique_object, parse_constant=invalid)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def valid_hash(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def sealed_operations_owner(root=ROOT):
    register = loads((root / 'specs/texenda-handoff/01-foundation/authority-register.json').read_text())
    owners = [row['path'] for row in register['current_normative_owners']
              if row['topic'] == 'operations-procedures']
    require(len(owners) == 1, 'sealed operations-procedures must have exactly one owner')
    require(owners[0] == '04-security-governance-and-operations/runbooks.md',
            'sealed operations-procedures baseline changed; explicit review required')
    return 'specs/texenda-handoff/' + owners[0]


def validate_accepted_mappings(crosswalk):
    """Use immutable accepted history as the oracle for all 85 dispositions."""
    raw = subprocess.check_output(
        ['git', '--no-optional-locks', 'show', ACCEPTED_MAPPING_REVISION + ':' + CROSSWALK],
        cwd=ROOT)
    accepted = loads(raw)
    require(crosswalk['blueprint_path_inventory'] == accepted['blueprint_path_inventory'],
            '85-path inventory differs from the immutable accepted baseline')
    require(crosswalk['mappings'] == accepted['mappings'],
            '85 mapping dispositions differ from the immutable accepted baseline')


def validate(crosswalk, baseline, manifest, *, root=ROOT):
    require(crosswalk['schema_version'] == 'texenda.workspace-adoption-crosswalk.v2',
            'unknown crosswalk schema')
    successor = crosswalk.get('schema_successor', {})
    require(successor.get('previous_schema') == 'texenda.workspace-adoption-crosswalk.v1'
            and successor.get('previous_revision') == CROSSWALK_PREDECESSOR_REVISION
            and successor.get('previous_path') == CROSSWALK
            and successor.get('previous_sha256') == CROSSWALK_PREDECESSOR_SHA256
            and successor.get('retention') == 'exact_predecessor_in_preserved_Git_history'
            and successor.get('field_rename') == {
                'from': 'deferred_semantic_work', 'to': 'maintenance_items'}
            and successor.get('preserved_record_ids') == ['DEFER-WSM-0001', 'DEFER-WSM-0002']
            and 'deferred_semantic_work' not in crosswalk,
            'crosswalk v2 lost its exact v1 predecessor or current field migration')
    require(baseline['schema_version'] == 'texenda.workspace-baseline.v1', 'unknown baseline schema')
    require(manifest['schema_version'] == 'texenda.workspace-move-manifest.v1', 'unknown move schema')
    require(crosswalk['adoption_mode'] == 'mapped-existing', 'false adoption mode')
    require(crosswalk['profile'] == 'high-assurance', 'required profile missing')
    require(crosswalk['status'] == 'completed_current_contract'
            and crosswalk.get('current_epoch') == 'external_state',
            'crosswalk does not identify the completed current epoch')
    source = crosswalk['blueprint']
    require(source['selected_version'] == '1.0.0' and
            source['qualification'] == 'inspected_structural_reference_only' and
            source['generated_new_project'] is False and
            source['newer_candidate_qualified'] is False and
            source['newer_candidate_version'] == '4.2.0' and
            source['newer_candidate_full_validator'] == 'FAIL' and
            source['dirty_checkout_working_version'] == '4.3.0' and
            source['dirty_checkout_version_committed'] is False and
            source['origin_record_created'] is True and
            source['origin_schema_supports_mapped_existing'] is True and
            source['origin_schema'] == '.agent/schemas/project-blueprint-origin.v3.schema.json',
            'false blueprint provenance')
    require(crosswalk.get('local_amendments') == [{
        'id': 'ADR-0005',
        'owner_path': 'docs/decisions/ADR-0005-react-email-editor-reversible-default.md',
        'scope': 'email_editor_reversible_default_only', 'package_variants_modified': False}, {
        'id': 'ADR-0006',
        'owner_path': 'docs/decisions/ADR-0006-clean-ordinary-operating-contract.md',
        'scope': 'ordinary_entry_current_epoch_and_history_routing_only',
        'package_variants_modified': False}, {
        'id': 'ADR-0007', 'owner_path': operating.ADR,
        'scope': 'portable_standalone_operation_code_control_and_retention_references_only',
        'package_variants_modified': False}, {
        'id': 'ADR-0008', 'owner_path': operating.INITIAL_PRODUCT_ADR,
        'scope': 'integrated_initial_product_scoped_plan_release_and_acceptance_delta_only',
        'package_variants_modified': False}],
        'local editor amendment scope/owner changed')
    require(set(crosswalk['roles']) == ROLES, 'role vocabulary changed')
    epochs = ['baseline', 'facade', 'external_state']
    require(crosswalk['epochs'] == epochs, 'ownership epochs missing')
    rows = crosswalk['ownership']
    owners = {row['concern_id']: row for row in rows}
    require(len(owners) == len(rows), 'duplicate canonical concern')
    for row in rows:
        require(set(row['owner_by_epoch']) == set(epochs), 'missing ownership epoch')
        require(bool(row['rule']), 'owner rule missing')
        for epoch, owner in row['owner_by_epoch'].items():
            require(owner is None or isinstance(owner, str) and bool(owner),
                    'each concern must have one owner path per epoch')
            require(epoch != 'external_state' or owner is not None, 'final owner missing')

    expected = {
        'product_semantics': 'specs/texenda-handoff/',
        'model_routing': 'tooling/coordination/routing-policy.json',
        'wp_lifecycle': 'tooling/coordination/harness.py',
        'active_tasks': HOME + '/local/agent-state/texenda/state.json',
        'receipts': HOME + '/local/agent-state/texenda/state.json',
        'live_qualification': HOME + '/local/agent-state/texenda/state.json',
        'agent_permission_classes': '.agent/policy.json',
        'precedence_trust': '.agent/context.json',
        'validation_commands': '.agent/validators.json',
        'durable_decisions': 'docs/decisions/',
        'qualification_evidence': 'docs/qualification/evidence/',
        'review_records': 'docs/qualification/evidence/',
        'conformance_findings': 'project-dossier/conformance/findings.json',
        'adoption_transition': CROSSWALK,
    }
    for concern, path in expected.items():
        require(owners.get(concern, {}).get('owner_by_epoch', {}).get('external_state') == path,
                'canonical owner changed or second store: ' + concern)
    for concern in ('agent_permission_classes', 'precedence_trust'):
        require(owners[concern]['owner_by_epoch']['baseline'] == 'AGENTS.md',
                'premature root authority cutover')
    operations_owner = sealed_operations_owner(root)
    require(all(owners['operations_recovery']['owner_by_epoch'][epoch] == operations_owner
                for epoch in epochs), 'operations recovery owner disagrees with sealed authority register')

    mappings = crosswalk['mappings']
    inventory = crosswalk['blueprint_path_inventory']
    validate_accepted_mappings(crosswalk)
    require(len(inventory) == len(set(inventory)) == 85, 'blueprint path inventory incomplete')
    require(sorted(row['blueprint_path'] for row in mappings) == sorted(inventory),
            'missing or duplicate blueprint mapping')
    origin_schema_mapping = next(row for row in mappings
                                 if row['blueprint_path']
                                 == '.agent/schemas/project-blueprint-origin.schema.json')
    require(origin_schema_mapping['mapped_path']
            == '.agent/schemas/project-blueprint-origin.v3.schema.json'
            and origin_schema_mapping['role'] == 'adapter',
            'active origin mapping is not v3')
    origin_record_mapping = next(row for row in mappings
                                 if row['blueprint_path'] == '.project-blueprint-origin.json')
    require('origin.v3 record' in origin_record_mapping['reason']
            and 'v2 predecessor' in origin_record_mapping['reason'],
            'origin record mapping lost v3/current or v2/predecessor distinction')
    history_mapping = next(row for row in mappings
                           if row['blueprint_path'] == 'project-dossier/history/README.md')
    require(history_mapping['mapped_path'] == 'project-dossier/history/README.md'
            and history_mapping['role'] == 'historical_source',
            'completed migration history is not isolated behind its tracked index')
    operations_mapping = next(row for row in mappings
                              if row['blueprint_path'] == 'project-dossier/operations/README.md')
    require(operations_mapping['mapped_path'] == operations_owner and
            operations_mapping['concern_id'] == 'operations_recovery' and
            operations_mapping['role'] == 'index',
            'OPS-0001 must index the sealed operations-procedures owner')
    artifact_types = crosswalk['blueprint_artifact_type_inventory']
    require(len({row['id'] for row in artifact_types}) == len(artifact_types) == 35,
            'artifact type coverage incomplete')
    require(all(row['path'] in inventory for row in artifact_types), 'artifact path unmapped')
    require(sorted((row['id'], row['path']) for row in artifact_types)
            == sorted(tuple(row) for row in operating.EXPECTED_ARTIFACT_TYPES),
            'exact 35 artifact type/path pairs changed')
    require(sorted((row['mapped_path'], row['concern_id'], row['role'])
                   for row in crosswalk['supplemental_mappings'])
            == sorted(tuple(row) for row in operating.EXPECTED_SUPPLEMENTAL),
            'exact six supplemental mappings changed')
    require(sorted((row['id'], row['mapped_path'], row['concern_id'], row['role'])
                   for row in crosswalk['supplemental_high_assurance_types'])
            == sorted(tuple(row) for row in operating.EXPECTED_HIGH_ASSURANCE),
            'exact five supplemental high-assurance types changed')
    require({row['id'] for row in crosswalk['supplemental_high_assurance_types']} ==
            {'SEC-0001', 'DAT-0001', 'SUP-0001', 'EVA-0001', 'CTX-0001'},
            'conditional artifact type coverage incomplete')
    authoritative = {}
    for row in mappings + crosswalk['supplemental_mappings']:
        require(row['concern_id'] in owners and row['role'] in ROLES and bool(row['reason']),
                'invalid role, concern or missing rationale')
        if row['mapped_path'] is None:
            require(row['role'] in {'deferred', 'not_applicable'}, 'unmapped required artifact')
        if row['role'] == 'authoritative':
            concern = row['concern_id']
            path = row['mapped_path']
            require(owners[concern]['owner_by_epoch']['external_state'] == path,
                    'duplicate canonical owner for ' + concern)
            require(concern not in authoritative or authoritative[concern] == path,
                    'two authoritative paths for ' + concern)
            authoritative[concern] = path
        if row.get('blueprint_path') in {'.agent/tasks/README.md', '.agent/decisions/README.md',
                                          '.agent/evidence/README.md', '.agent/reviews/README.md'}:
            require(row['role'] == 'index', 'second task/decision/evidence/review store')
    dossier_evidence = [row for row in crosswalk['supplemental_mappings']
                        if row.get('mapped_path') == 'project-dossier/evidence/README.md']
    require(len(dossier_evidence) == 1 and
            dossier_evidence[0]['concern_id'] == 'qualification_evidence' and
            dossier_evidence[0]['role'] == 'index',
            'owner-request dossier evidence index correction missing')
    projection = crosswalk['projection_contract']
    require(projection['authority'] == 'generated_non_authoritative' and
            projection['check_writes'] is False and projection['refresh_only_writer'] is True,
            'projection or check acquired write authority')
    require({'source_git_revision', 'source_git_tree', 'source_scope_sha256', 'ledger_sha256',
             'receipt_count', 'receipt_tip', 'freshness_rule'} <= set(projection['required_fields']),
            'projection source/freshness binding missing')
    acceptance = crosswalk['facade_acceptance']
    require(acceptance['new_product_canonical_files'] is False and
            acceptance['registered_extension_authority'] == 'restrictions_only' and
            acceptance['origin_schema_successor_present'] is True and
            acceptance['real_mapped_task_lifecycle_demonstrated'] is True and
            acceptance['independent_review_profile'] == 'gpt-6-astra-max' and
            acceptance['reviewer_distinct_from_author_and_integrator'] is True and
            acceptance['final_read_only_review_after_evidence_added'] is True,
            'authority or independent review boundary weakened')
    deferred = {row['id']: row for row in crosswalk['maintenance_items']}
    require(len(crosswalk['maintenance_items']) == len(deferred) == 7
            and set(deferred) == {'DEFER-WSM-0001', 'DEFER-WSM-0002',
                                  'DEFER-WSM-0003', 'DEFER-WSM-0004',
                                  'DEFER-WSM-0005', 'DEFER-WSM-0006', 'DEFER-WSM-0007'},
            'maintenance IDs were lost, duplicated or replaced')
    editor_resolution = deferred.get('DEFER-WSM-0001', {})
    require(editor_resolution.get('status') == 'resolved_scoped_by_ADR-0005'
            and editor_resolution.get('does_not_modify_packages') is True
            and 'WP-10' in editor_resolution.get('remaining_gate', '')
            and 'VAL-03' in editor_resolution.get('remaining_gate', ''),
            'editor wording resolution overclaims package or qualification scope')
    source_followup = deferred['DEFER-WSM-0002']
    require(source_followup.get('owner_path') == 'project-dossier/machine-readable/raidq.json'
            and source_followup.get('owner_record') == 'RAIDQ-0005'
            and source_followup.get('status') == 'deferred'
            and source_followup.get('does_not_import_project_facts') is True,
            'Blueprint maintenance blocker was bypassed or lost its issue owner')
    for number, record in enumerate(('RAIDQ-0005', 'RAIDQ-0006', 'RAIDQ-0007',
                                     'RAIDQ-0008', 'RAIDQ-0009', 'RAIDQ-0010'), 2):
        row = deferred['DEFER-WSM-' + str(number).zfill(4)]
        require(row['owner_path'] == operating.RAIDQ and row['owner_record'] == record
                and row['status'] == 'deferred'
                and row['trigger'] == ('Resolve current deferral details from ' + record
                                       + '; this entry owns no editable trigger detail.'),
                'crosswalk deferral reference disagrees with its sole RAIDQ owner')
    validate_compatibility_dispositions(crosswalk)

    packages = baseline['packages']
    require(packages['sealed']['role'] == 'implementation_repository_sealed_authority' and
            packages['sealed']['planned_path'] == HOME + '/repo/specs/texenda-handoff' and
            packages['source']['role'] == 'historical_source_unpromoted_variant' and
            packages['source']['planned_path'] == HOME + '/sources/handoff-1.1.0-20260914',
            'sealed/source preservation missing or authority merged')
    require({r['path'] for r in packages['differing_paths']} == DIFFERENCES and
            len(packages['differing_paths']) == 11, 'package divergence changed or omitted')
    for variant in ('sealed', 'source'):
        require(all(valid_hash(packages[variant][key]) for key in
                    ('manifest_sha256', 'checksums_sha256', 'path_nul_sha256', 'canonical_array_sha256')),
                'package fingerprint missing')
    private = baseline['private_input']
    require(all(private[key] is False for key in ('contents_accessed', 'contents_hashed',
                                                 'contents_parsed', 'contents_copied')),
            'unsafe private-input handling')
    require(set(private['permitted_verification']) ==
            {'existence', 'ignore_rule', 'tracking_status', 'eventual_location'},
            'private-input inspection broadened')
    require(not any('private-input' in row['path'] or row['path'].endswith('.csv')
                    for row in baseline['filesystem']['author_source_files']),
            'private file entered content fingerprint scope')

    require(manifest['project_home'] == HOME and manifest['old_repository'] == OLD and
            manifest['new_repository'] == HOME + '/repo' and
            manifest['keep_active_parent_root'] is True and
            manifest['parent_git_repository'] is False, 'workspace root contract changed')
    constraints = manifest['constraints']
    require(all(constraints[key] is False for key in ('overwrite', 'delete', 'symlink_bridge',
                'private_content_access', 'private_content_hash', 'private_content_copy',
                'remote_mutation', 'receipt_rewrite')) and constraints['serial_moves'] is True,
            'unsafe move or effect permission')
    top = {row['entry']: row for row in baseline['filesystem']['non_git_top_level']}
    moves = manifest['source_package_moves']
    require(len(moves) == len(top) == 16 and {row['entry'] for row in moves} == set(top),
            'top-level move coverage changed')
    for move in moves:
        entry = move['entry']
        require(move['source'] == HOME + '/' + entry and
                move['destination'] == HOME + '/sources/handoff-1.1.0-20260914/' + entry and
                move['operation'] == 'same_filesystem_rename_no_replace',
                'out-of-scope move target or unsafe operation')
        require(move['type'] == top[entry]['type'], 'source type changed')
        key = 'sha256' if move['type'] == 'file' else 'tree_sha256'
        require(move.get(key) == top[entry].get(key) and valid_hash(move.get(key)),
                'move digest changed')
    expected_dirs = {'sources', 'sources/handoff-1.1.0-20260914', 'worktrees', 'local',
                     'local/agent-state', 'local/logs', 'local/artifacts', 'archive', 'archive/checkpoints'}
    require(set(manifest['create_directories']) == {HOME + '/' + p for p in expected_dirs},
            'directory creation escapes scope or consumes rename destination')
    require(set(manifest['reserved_absent_targets']) ==
            {HOME + '/repo', HOME + '/local/private-inputs', HOME + '/local/agent-state/texenda'},
            'absent rename destination protection missing')
    move = manifest['repository_move']
    require(move['source'] == OLD and move['destination'] == HOME + '/repo' and
            move['operation'] == 'same_filesystem_rename_no_replace' and
            move['destination_must_be_absent'] is True, 'unsafe checkout move')
    cutover = manifest['external_state_cutover']
    require(cutover['binding_path'] == HOME + '/repo/.texenda-location.json' and
            cutover['explicit_state_root'] == HOME + '/local/agent-state/texenda' and
            cutover['binding_ignored'] is True and cutover['state_bytes_change_required'] is False and
            cutover['receipt_append_required'] is False, 'unsafe state binding or receipt change')
    require(set(cutover['historical_compatibility_retained']) == LEGACY,
            'historical receipt inputs would be moved or lost')
    require(len(cutover['active_moves']) == 2 and
            {(row['source'], row['destination']) for row in cutover['active_moves']} ==
            {(HOME + '/repo/.texenda/' + name, HOME + '/local/agent-state/texenda/' + name)
             for name in ('state.json', 'state.lock')}, 'out-of-scope active-state move')
    private_move = cutover['private_directory_move']
    require(private_move['source'] == HOME + '/repo/.texenda/private-inputs' and
            private_move['destination'] == HOME + '/local/private-inputs' and
            private_move['operation'] == 'same_filesystem_rename_no_replace',
            'unsafe private-directory move')
    require(manifest['recovery']['mode'] == 'resume_or_rollback_by_verified_move' and
            manifest['recovery']['never_infer_completed_from_missing_source'] is True and
            manifest['recovery']['journal_location'] == HOME + '/local/logs/workspace-relocation/',
            'unsafe interrupted-move recovery')
    archive = manifest['checkpoint_archive']
    require(archive['source'] == '/private/tmp/texenda-workspace-migration-checkpoint-20260914' and
            archive['destination'] == HOME + '/archive/checkpoints/phase-0-20260914' and
            archive['operation'] == 'same_filesystem_rename_no_replace_after_verification',
            'out-of-scope checkpoint move')
    require(manifest['workspace_notice']['path'] == HOME + '/WORKSPACE.md' and
            manifest['workspace_notice']['role'] == 'non_authoritative_navigation',
            'parent notice became an authority or escaped scope')
    return {'concerns': len(owners), 'blueprint_paths': len(mappings),
            'artifact_types': len(artifact_types), 'source_moves': len(moves)}


def validate_compatibility_dispositions(crosswalk):
    group = crosswalk['compatibility_dispositions']
    require(group['ordinary_work_requires_migration_history'] is False
            and group['assessed_on'] == '2026-09-15',
            'compatibility register became ordinary-work prerequisites')
    rows = group['items']
    by_id = {row['id']: row for row in rows}
    expected = {
        'COMPAT-0001': ('retain', 'tooling/coordination/harness.py'),
        'COMPAT-0002': ('retain', 'tooling/coordination/harness.py'),
        'COMPAT-0003': ('retain', '.texenda/'),
        'COMPAT-0004': ('retain', 'tooling/workspace/relocate_state.py'),
        'COMPAT-0005': ('retain', '.texenda-location.json'),
        'COMPAT-0006': ('retain', '.project-blueprint-origin.json'),
        'COMPAT-0007': ('isolate', 'tooling/workspace/interpret_adoption.py'),
        'COMPAT-0008': ('retain', '.codex/config.toml'),
        'COMPAT-0009': ('retain', 'tooling/coordination/harness.py'),
        'COMPAT-0010': ('retain', CROSSWALK),
    }
    require(len(rows) == len(by_id) and set(by_id) == set(expected),
            'compatibility disposition coverage is incomplete or duplicated')
    for identifier, (disposition, owner) in expected.items():
        row = by_id[identifier]
        require(row['disposition'] == disposition and row['owner_path'] == owner,
                'compatibility dependency retired or assigned a second owner: ' + identifier)
        require(all(isinstance(row.get(key), str) and row[key].strip()
                    for key in ('subject', 'record_class', 'reason', 'risk', 'trigger', 'recovery'))
                and isinstance(row.get('required_proof'), list) and row['required_proof']
                and all(isinstance(value, str) and value.strip() for value in row['required_proof'])
                and isinstance(row.get('paths'), list) and row['paths']
                and len(row['paths']) == len(set(row['paths'])),
                'compatibility disposition lacks risk, trigger, proof or recovery: ' + identifier)
    require(set(by_id['COMPAT-0003']['paths']) == COMPATIBILITY_INPUTS,
            'receipt-referenced compatibility input paths changed')
    require('226a4a14b3a795b24354eb90e51a50067fd27fe809423b30b9fa1551f3ce72d6'
            in by_id['COMPAT-0001']['reason'], 'sealed-v1 compatibility pin lost')
    return len(rows)


def verify_crosswalk_predecessor(root):
    raw = subprocess.check_output(['git', 'show', CROSSWALK_PREDECESSOR_REVISION + ':' + CROSSWALK],
                                  cwd=root)
    require(sha(raw) == CROSSWALK_PREDECESSOR_SHA256,
            'crosswalk v1 predecessor bytes changed or are unavailable')
    prior = loads(raw)
    current = loads((root / CROSSWALK).read_text())
    require(prior['schema_version'] == 'texenda.workspace-adoption-crosswalk.v1'
            and [row['id'] for row in prior['deferred_semantic_work']]
            == [row['id'] for row in current['maintenance_items'][:2]],
            'crosswalk successor changed stable maintenance IDs')
    return CROSSWALK_PREDECESSOR_SHA256


EDITOR_ADR = 'docs/decisions/ADR-0005-react-email-editor-reversible-default.md'
OBSERVATIONS = 'docs/qualification/evidence/2026-09-15-editor-blueprint-followup-observations.evidence.json'
EDITOR_FIELDS = (
    'schema_version',
    'amendment_owner',
    'status',
    'renderer',
    'composer',
    'composer_version',
    'composer_qualification',
    'observed_release',
    'host',
    'document_codec',
    'codec_versioned',
    'canonical_email_document',
    'compiled_outputs',
    'retain_hashes',
    'payload_lexical_is_canonical_email',
    'block_allowlist',
    'default_extensions_automatically_approved',
    'arbitrary_react_allowed',
    'javascript_allowed',
    'raw_executable_content_allowed',
    'fallback',
    'preserve_old_codecs',
    'preserve_compiled_outputs',
    'required_qualification',
    'qualification_gate',
    'qualification_gate_passed',
    'work_package',
    'dependencies_installed',
    'package_variants_modified',
    'source_package_promoted',
)


def load_editor_contract(root):
    path = root / EDITOR_ADR
    require(path.is_file() and not path.is_symlink(), 'editor amendment owner missing')
    text = path.read_text()
    marker = '<!-- texenda-editor-default-contract -->'
    require(text.count(marker) == 1, 'editor amendment needs exactly one owned contract')
    matches = re.findall(re.escape(marker) + r'\s*\x60\x60\x60json\n(.*?)\n\x60\x60\x60', text, re.S)
    require(len(matches) == 1, 'editor amendment contract block missing or ambiguous')
    return loads(matches[0])


def validate_followup_metadata(editor, provenance, origin):
    require(set(editor) == set(EDITOR_FIELDS), 'editor amendment contract is not closed')
    require(editor['schema_version'] == 'texenda.editor-default.v1'
            and editor['amendment_owner'] == EDITOR_ADR
            and editor['status'] == 'reversible_implementation_default'
            and editor['renderer'] == 'React Email' and editor['composer'] == '@react-email/editor'
            and editor['host'] == 'custom Payload/Next view'
            and editor['document_codec'] == 'EmailDocumentCodec'
            and editor['codec_versioned'] is True
            and editor['canonical_email_document'] == 'versioned TipTap JSON',
            'editor default/codec ownership changed')
    require(editor['composer_version'] is None and editor['composer_qualification'] == 'UNVERIFIED'
            and editor['observed_release'] == {
                'version': '1.7.7', 'retrieved_on': '2026-09-15', 'selected': False}
            and editor['qualification_gate'] == 'VAL-03'
            and editor['qualification_gate_passed'] is False
            and editor['work_package'] == 'WP-10' and editor['dependencies_installed'] is False,
            'editor version pin or VAL-03 qualification bypass')
    required = ['compatibility_manifest', 'license_and_SBOM', 'peer_dependency_closure',
                'Next_React_Payload_integration', 'JSON_round_trip', 'build_performance',
                'rendering_fixtures']
    require(editor['required_qualification'] == required, 'editor qualification evidence omitted')
    require(editor['block_allowlist'] == [
                'text', 'heading', 'image', 'button', 'divider', 'callout',
                'article/recipe card', 'immutable compliance-footer structure']
            and editor['compiled_outputs'] == ['HTML', 'plain text']
            and editor['retain_hashes'] is True
            and editor['preserve_old_codecs'] is True
            and editor['preserve_compiled_outputs'] is True
            and editor['fallback'] == 'React Email with a small fixed-block composer',
            'editor allowlist, retained outputs or fallback weakened')
    require(all(editor[key] is False for key in (
                'payload_lexical_is_canonical_email', 'default_extensions_automatically_approved',
                'arbitrary_react_allowed', 'javascript_allowed', 'raw_executable_content_allowed',
                'package_variants_modified', 'source_package_promoted')),
            'editor implementation or package authority expanded')
    sources = provenance['sources']
    by_id = {row['id']: row for row in sources}
    require(len(by_id) == len(sources) and set(by_id) == {
                'SRC-0001', 'SRC-0002', 'SRC-0003', 'SRC-0004',
                'SRC-0005', 'SRC-0006', 'SRC-0007', 'SRC-0008'}, 'follow-up provenance IDs incomplete')
    require(origin['schema_version'] == 'texenda.project-blueprint-origin.v3'
            and origin['selected_version'] == by_id['SRC-0001']['version'] == '1.0.0'
            and by_id['SRC-0001']['qualification']
            == origin['reference_qualification'] == 'inspected_structural_reference_only'
            and origin['clean_candidate']['qualified'] is False
            and origin['clean_candidate']['adopted'] is False,
            'selected blueprint structural reference changed')
    clean, dirty = by_id['SRC-0002'], by_id['SRC-0005']
    require(clean['version'] == origin['clean_candidate']['committed_version'] == '4.2.0'
            and clean['revision'] == origin['clean_candidate']['revision']
            == '5e2d3025aea6b1574ab984e5ebb89b5602a38535'
            and clean['tree'] == origin['clean_candidate']['tree']
            == '3c732979e580c80b020d09c22ce86f5202110518'
            and clean['working_tree'] == 'clean' and clean['adopted'] is False
            and clean['qualification'] == 'not_fully_qualified'
            and clean['qualification_checks'] == origin['clean_candidate']['qualification_checks']
            == {'source_contracts': 'PASS', 'acceptance': 'PASS', 'full_validator': 'FAIL'}
            and clean['failed_check'] == origin['clean_candidate']['failed_check'],
            'clean source qualification/version provenance mixed or overclaimed')
    require(dirty['working_version'] == '4.3.0' and dirty['version_committed'] is False
            and dirty['version_attributed_to_clean_revision'] is False
            and dirty['adopted'] is False and 'revision' not in dirty and 'tree' not in dirty,
            'dirty uncommitted version attributed to a clean commit')
    require(provenance['package_difference_count'] == 11
            and set(provenance['package_differing_paths']) == DIFFERENCES
            and by_id['SRC-0003']['kind'] == 'implementation_repository_sealed_authority'
            and by_id['SRC-0004']['kind'] == 'historical_source_unpromoted_variant'
            and provenance['editor_amendment'] == {
                'owner_path': EDITOR_ADR, 'status': 'resolved_by_local_amendment',
                'package_variants_modified': False, 'package_difference_count': 11,
                'qualification_gate': 'VAL-03', 'qualification_gate_passed': False},
            'editor amendment promoted or changed a preserved package')
    observed = by_id['SRC-0006']
    require(observed['observed_editor_release'] == '1.7.7'
            and observed['selected_version'] is None
            and observed['qualification'] == 'UNVERIFIED'
            and observed['local_amendment'] == EDITOR_ADR,
            'upstream editor observation became a pin or qualification')
    debug = by_id['SRC-0007']
    require(debug['manifest'] == 'CURRENT-SHA256SUMS'
            and debug['manifest_sha256'] == '8fca896ff26a00eb7d85d49fe54344a6a2d9b034d5938609ca920c3bc7ac2bd2'
            and debug['provenance'] == 'PROVENANCE.md'
            and debug['provenance_sha256'] == '5830d7d810d203a3e9e0f3fc9c2859778424be6d5bd4ccddcf512fc8699b0fa2'
            and debug['current_file_count'] == 5 and debug['current_hashes_verified'] is True
            and debug['pre_move_manifest_exists'] is False
            and debug['historical_equality_reconstructed'] is False
            and debug['authority'] == 'non_authoritative_forward_only'
            and debug['debug_payloads_promoted_to_project_evidence'] is False,
            'debug forward baseline overclaims historical equality or authority')
    archive = by_id['SRC-0008']
    require(archive['kind'] == 'archive_forward_integrity_baseline'
            and archive['observed_on'] == '2026-09-15'
            and archive['path'] == HOME + '/archive/integrity/2026-09-15-preimplementation'
            and archive['manifest'] == 'CURRENT-SHA256SUMS'
            and archive['manifest_sha256'] == 'b682602668d10e96e9c50fbf317d5e3eee4124f1db613e5c49bd86b281656fde'
            and archive['provenance'] == 'PROVENANCE.md'
            and archive['provenance_sha256'] == '32e5ee34be5482ee8da28630690cca64720371ef63ebdd84a4cfc91b29de766f'
            and archive['current_file_count'] == 5626
            and archive['current_hashes_verified'] is True
            and archive['historical_equality_reconstructed'] is False
            and archive['authority'] == 'non_authoritative_forward_only'
            and archive['raw_artifacts_promoted_to_source_or_evidence_authority'] is False
            and archive['verification_working_directory'] == HOME
            and archive['verification_command']
            == 'shasum -a 256 -c archive/integrity/2026-09-15-preimplementation/CURRENT-SHA256SUMS'
            and archive['verification_result'] == {
                'exit_code': 0, 'verified_files': 5626, 'non_success_lines': 0},
            'archive forward baseline changed or overclaims history/authority')
    return {'origin': 'separated_v3', 'editor': 'reversible_unverified_default',
            'debug_artifacts': 'forward_baseline_only', 'archive_files': 5626}


def validate_blueprint_maintenance(raidq):
    matches = [row for row in raidq['items'] if row['id'] == 'RAIDQ-0005']
    require(len(matches) == 1, 'Blueprint maintenance issue is missing or duplicated')
    row = matches[0]
    prefix = 'env PYTHONDONTWRITEBYTECODE=1 python3 -B skills/octon-mini-project-bootstrap/scripts/'
    require(row['status'] == 'gated'
            and row['owner'] == 'Octon Mini / Project Blueprint source maintainer'
            and row['project_observation_owner'] == 'project-dossier/provenance/sources.json'
            and isinstance(row['blockers'], list) and len(row['blockers']) == 2
            and 'test_source_activation_exercise_writes_only_external_receipt' in row['blockers'][0]
            and '2026-09-10T23:59:59-05:00' in row['blockers'][0]
            and '--project-blueprint-seed' in row['blockers'][1]
            and 'authentic reviewed' in row['retry_trigger']
            and 'clean committed' in row['retry_trigger']
            and row['requalification_commands'] == [
                'git rev-parse HEAD HEAD^{tree}', 'git show HEAD:VERSION',
                'git status --porcelain=v1 --untracked-files=all --ignored=matching',
                prefix + 'validate_source_contracts.py', prefix + 'test_acceptance.py',
                prefix + 'validate_octon_mini.py',
                'git status --porcelain=v1 --untracked-files=all --ignored=matching']
            and row['next_command_after_retry_trigger'] == prefix + 'validate_source_contracts.py'
            and row['planner_diagnostic_after_full_qualification']
            == 'env PYTHONDONTWRITEBYTECODE=1 python3 -B octon upgrade --help'
            and isinstance(row['required_evidence'], list) and len(row['required_evidence']) >= 4
            and all(isinstance(row.get(key), str) and row[key].strip()
                    for key in ('risk', 'control', 'command_working_directory', 'recovery')),
            'Blueprint blocker lost its external owner, complete qualification, seed or recovery boundary')
    return 'external_source_correction_and_authentic_reviewed_seed_required'


def verify_followup_records(root):
    require(EDITOR_ADR in (root / 'AGENTS.md').read_text(),
            'root router does not identify the local editor amendment owner')
    return validate_followup_metadata(
        load_editor_contract(root),
        loads((root / 'project-dossier/provenance/sources.json').read_text()),
        loads((root / '.project-blueprint-origin.json').read_text()))


def verify_clean_operating_contract(root):
    """Require current entry/status/history routing without rewriting history."""
    entry_paths = (
        'AGENTS.md', '.agent/START_HERE.md', 'docs/agents/operating-guide.md',
        'project-dossier/README.md', 'project-dossier/validation/README.md',
        'tooling/coordination/README.md',
    )
    for name in entry_paths:
        require(ORDINARY_VALIDATION in (root / name).read_text(),
                'ordinary explicit-state validation missing from ' + name)
    tools = loads((root / '.agent/tools.json').read_text())
    by_id = {row['id']: row for row in tools['tools']}
    require(by_id['facade-validator']['availability_check'] == ORDINARY_VALIDATION,
            'facade tool does not expose the ordinary validation command')
    registry = loads((root / '.agent/validators.json').read_text())
    require(registry['execution_context']['ordinary_entry_command'] == ORDINARY_VALIDATION,
            'validation registry does not expose the ordinary entry command')
    for name in ('.agent/START_HERE.md', 'docs/agents/operating-guide.md',
                 'tooling/coordination/README.md'):
        text = (root / name).read_text()
        for command in ('status', 'ready', operating.SELECTED_CONTEXT):
            require(ORDINARY_COORDINATOR + ' ' + command in text,
                    'active coordinator entry command missing from ' + name)
        require('context WP-01' not in text.split('## Pre-binding', 1)[0]
                and '/Users/' not in text.split('## Pre-binding', 1)[0],
                'current ordinary entry contains a fixed WP or host path')
        require(text.index(ORDINARY_COORDINATOR + ' status')
                < text.find('migrate-v1') if 'migrate-v1' in text else True,
                'legacy migration appears before ordinary active commands')

    current_sources = (
        'project-dossier/machine-readable/plan.json',
        'project-dossier/conformance/findings.json',
        'project-dossier/machine-readable/raidq.json',
        'project-dossier/transition/README.md',
        CROSSWALK,
    )
    stale = ('proposed source correction', 'unapproved closeout',
             'current status-correction candidate', 'reviewable_transition_contract',
             'the local origin.v2 record')
    for name in current_sources:
        normalized = ' '.join((root / name).read_text().lower().split())
        require(not any(phrase in normalized for phrase in stale),
                'stale migration status remains in current source: ' + name)

    history = root / COMPLETED_TRANSITION_HISTORY
    require(history.is_file() and not history.is_symlink()
            and sha(history.read_bytes()) == COMPLETED_TRANSITION_SHA256,
            'completed transition history bytes changed or are missing')
    original = subprocess.check_output(
        ['git', 'show', '338cd13505d6faffdb645c450b44ea9230aadd75:'
         'project-dossier/transition/README.md'], cwd=root)
    require(original == history.read_bytes(),
            'completed transition history differs from its exact source revision')
    current_transition = (root / 'project-dossier/transition/README.md').read_text()
    require(len(current_transition.splitlines()) < 80
            and 'The historical operator procedure below is preserved unchanged.'
            not in current_transition,
            'current transition entry still embeds the migration procedure')

    supersession = loads((root / 'project-dossier/SUPERSESSION.json').read_text())
    require(supersession['current_version'] == operating.DOSSIER_VERSION
            and len(supersession['records']) == 5,
            'dossier version/supersession is not current')
    record = supersession['records'][0]
    require(record['prior_sha256'] == COMPLETED_TRANSITION_SHA256
            and record['retained_history_path'] == COMPLETED_TRANSITION_HISTORY
            and record['active_successor_path'] == 'project-dossier/transition/README.md',
            'transition successor does not bind the retained history')
    crosswalk_successor = supersession['records'][1]
    require(crosswalk_successor['id'] == 'SUP-0002'
            and crosswalk_successor['prior_revision'] == CROSSWALK_PREDECESSOR_REVISION
            and crosswalk_successor['prior_sha256'] == CROSSWALK_PREDECESSOR_SHA256
            and crosswalk_successor['prior_path'] == CROSSWALK
            and crosswalk_successor['active_successor_path'] == CROSSWALK
            and crosswalk_successor['retention'] == 'exact_predecessor_in_preserved_Git_history'
            and crosswalk_successor['successor_schema'] == 'texenda.workspace-adoption-crosswalk.v2',
            'crosswalk supersession lost its exact retained predecessor')
    catalog = loads((root / 'project-dossier/ARTIFACT_CATALOG.json').read_text())
    artifacts = {row['path']: row for row in catalog['artifacts']}
    require(artifacts[COMPLETED_TRANSITION_HISTORY]['classification'] == 'history'
            and artifacts['project-dossier/history/README.md']['classification'] == 'navigation',
            'history paths have incorrect current information roles')
    return {'ordinary_entry_documents': len(entry_paths),
            'completed_transition_history_sha256': COMPLETED_TRANSITION_SHA256,
            'current_epoch': 'external_state'}


def verify_bound_inputs(root, baseline):
    """Validate immutable input bytes at the exact original Git revision."""
    revision = baseline['subject']['main_revision']
    require(re.fullmatch('[0-9a-f]{40}', revision) is not None, 'invalid source revision')
    for row in baseline['bound_source_files']:
        path = row['path']
        parts = PurePosixPath(path).parts
        require(not PurePosixPath(path).is_absolute() and '..' not in parts and
                not path.startswith('.texenda/') and not path.lower().endswith('.csv'),
                'unsafe evidence fingerprint path')
        result = subprocess.run(['git', 'show', revision + ':' + path], cwd=root,
                                capture_output=True, check=True)
        require(sha(result.stdout) == row['sha256'], 'bound source hash changed: ' + path)


def verify_actual_stores(root):
    for name in ('tasks', 'decisions', 'evidence', 'reviews'):
        store = root / '.agent' / name
        if store.exists():
            require(not store.is_symlink(), 'store index cannot be a symlink')
            for path in store.rglob('*'):
                require(not path.is_symlink(), 'store index child cannot be a symlink')
                if path.is_file():
                    require(path.name in {'README.md', 'OWNERSHIP.json'}, 'second active record store')
                    if path.suffix == '.json':
                        value = loads(path.read_text())
                        require(value.get('role') == 'index' and
                                not {'tasks', 'events', 'roster', 'decisions', 'evidence'} & set(value),
                                'index contains live records')
    require(not (root / 'project-dossier/canonical').exists(), 'copied product canonical owner')
    origin = root / '.project-blueprint-origin.json'
    if origin.exists():
        value = loads(origin.read_text())
        schema = root / '.agent/schemas/project-blueprint-origin.v3.schema.json'
        require(schema.is_file() and not schema.is_symlink(), 'origin schema successor missing')
        schema_value = loads(schema.read_text())
        require(value.get('schema_version') == 'texenda.project-blueprint-origin.v3' and
                value.get('adoption_mode') == 'mapped-existing' and
                value.get('generated_new_project') is False and
                value.get('reference_qualification') == 'inspected_structural_reference_only' and
                schema_value.get('$id') == 'urn:texenda:project-blueprint-origin:v3' and
                schema_value.get('additionalProperties') is False,
                'origin schema cannot truthfully represent mapped-existing')


def verify_qualification_check(root, check):
    """Require a confined hash-bound evidence file for both passing and failing checks."""
    if check.get('status') not in ('PASS', 'FAIL'):
        return False
    name = check.get('evidence_path')
    require(isinstance(name, str) and bool(name), 'PASS/FAIL check lacks evidence_path')
    parts = PurePosixPath(name).parts
    require(not PurePosixPath(name).is_absolute() and '\\' not in name and ':' not in name
            and not any(part in ('', '.', '..') for part in name.split('/'))
            and not any(part in ('.git', '.texenda', 'private-inputs') for part in parts)
            and not name.lower().endswith('.csv'), 'unsafe qualification evidence path')
    require(valid_hash(check.get('sha256')), 'PASS/FAIL check lacks a valid SHA-256')
    target = root
    for part in parts:
        target = target / part
        require(not target.is_symlink(), 'qualification evidence symlink denied')
    require(target.resolve().is_relative_to(root.resolve()) and target.is_file(),
            'qualification evidence file missing or outside repository')
    require(sha(target.read_bytes()) == check['sha256'], 'qualification evidence hash mismatch')
    return True


def verify_qualification_checks(root):
    count = 0
    for path in sorted((root / 'docs/qualification').rglob('*.json')):
        require(not path.is_symlink(), 'qualification record symlink denied')
        record = loads(path.read_text())
        require(isinstance(record, dict), 'qualification record must be an object')
        checks = record.get('checks', [])
        require(isinstance(checks, list), 'qualification checks must be an array')
        for check in checks:
            require(isinstance(check, dict), 'qualification check must be an object')
            count += verify_qualification_check(root, check)
    return count


def audit_candidate(root, baseline, *, scope='code'):
    """Parse candidate files and compare only the explicit public package scope."""
    names = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
        cwd=root).decode().split('\0')
    counts = {'JSON': 0, 'TOML': 0, 'Python': 0, 'new_markdown_links': 0,
              'sealed_files': 0, 'source_files': 0}
    for name in filter(None, names):
        if scope == 'code' and name in __import__('common').GENERATED_OUTPUT_PATHS:
            continue
        require(not name.startswith('.texenda/') and not name.lower().endswith('.csv'),
                'private/local input entered candidate inspection scope')
        path = root / name
        require(not path.is_symlink(), 'candidate inspection refuses symlinks')
        if name.startswith('.agent/tests/fixtures/invalid/'):
            continue
        if path.suffix == '.json':
            loads(path.read_text())
            counts['JSON'] += 1
        if path.suffix == '.toml':
            tomllib.loads(path.read_text())
            counts['TOML'] += 1
        if path.suffix == '.py':
            ast.parse(path.read_text(), filename=name)
            counts['Python'] += 1
        if name.startswith('specs/texenda-handoff/') and path.is_file():
            expected = subprocess.check_output(
                ['git', 'show', baseline['subject']['main_revision'] + ':' + name], cwd=root)
            require(path.read_bytes() == expected, 'sealed package changed: ' + name)
            counts['sealed_files'] += 1
    for name in ('docs/decisions/ADR-0004-mapped-project-workspace.md',
                 'project-dossier/transition/README.md',
                 'docs/qualification/evidence/2026-09-14-workspace-architecture-independent-review.md'):
        path = root / name
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
            target = urllib.parse.unquote(target.split('#')[0])
            if target and '://' not in target:
                require((path.parent / target).exists(), 'new local link missing: ' + target)
                counts['new_markdown_links'] += 1
    if scope == 'control':
        source = root.parent / 'sources/handoff-1.1.0-20260914'
        __import__('common').resolved_directory(source, 'preserved source package')
        for row in baseline['filesystem']['author_source_files']:
            path = source / row['path']
            raw = __import__('common').stable_file_bytes(path, 'preserved source file')
            require(sha(raw) == row['sha256'], 'source package changed: ' + row['path'])
            counts['source_files'] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--audit', action='store_true', help='Also parse candidate files, links and package bytes.')
    parser.add_argument('--scope', choices=('code', 'control'), default='code')
    parser.add_argument('--state-root', type=Path)
    args = parser.parse_args()
    try:
        if args.scope == 'control':
            control_context(ROOT, args.state_root)
        else:
            require(args.state_root is None, 'code scope rejects --state-root')
        crosswalk, baseline, manifest = [loads((ROOT / p).read_text())
                                         for p in (CROSSWALK, BASELINE, MANIFEST)]
        counts = validate(crosswalk, baseline, manifest)
        verify_bound_inputs(ROOT, baseline)
        verify_actual_stores(ROOT)
        counts['followups'] = verify_followup_records(ROOT)
        counts['crosswalk_predecessor_sha256'] = verify_crosswalk_predecessor(ROOT)
        counts['blueprint_maintenance'] = validate_blueprint_maintenance(
            loads((ROOT / 'project-dossier/machine-readable/raidq.json').read_text()))
        counts['clean_operation'] = verify_clean_operating_contract(ROOT)
        counts['qualification_checks'] = verify_qualification_checks(ROOT)
        counts['standalone_operation'] = operating.validate_operating(ROOT)
        if args.audit:
            counts['audit'] = audit_candidate(ROOT, baseline, scope=args.scope)
        if args.scope == 'control':
            import interpret_adoption
            interpret_adoption.local_contract(ROOT, scope='control')
    except (ContractError, ValidationError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'status': 'FAIL', 'reason': str(exc)}))
        return 1
    print(json.dumps({'status': 'PASS', **counts,
                      'scope': args.scope,
                      'local_preservation': 'checked' if args.scope == 'control' else 'unassessed',
                      'live_state_checked': False, 'moves_executed': False,
                      'private_input_accessed': False, 'approval': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
