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
import tomllib
import urllib.parse

ROOT = Path(__file__).resolve().parents[2]
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


def validate(crosswalk, baseline, manifest):
    require(crosswalk['schema_version'] == 'texenda.workspace-adoption-crosswalk.v1',
            'unknown crosswalk schema')
    require(baseline['schema_version'] == 'texenda.workspace-baseline.v1', 'unknown baseline schema')
    require(manifest['schema_version'] == 'texenda.workspace-move-manifest.v1', 'unknown move schema')
    require(crosswalk['adoption_mode'] == 'mapped-existing', 'false adoption mode')
    require(crosswalk['profile'] == 'high-assurance', 'required profile missing')
    source = crosswalk['blueprint']
    require(source['selected_version'] == '1.0.0' and
            source['qualification'] == 'inspected_structural_reference_only' and
            source['generated_new_project'] is False and
            source['newer_candidate_qualified'] is False and
            source['origin_record_created'] is False and
            source['origin_schema_supports_mapped_existing'] is False,
            'false blueprint provenance')
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

    mappings = crosswalk['mappings']
    inventory = crosswalk['blueprint_path_inventory']
    require(len(inventory) == len(set(inventory)) == 85, 'blueprint path inventory incomplete')
    require(sorted(row['blueprint_path'] for row in mappings) == sorted(inventory),
            'missing or duplicate blueprint mapping')
    artifact_types = crosswalk['blueprint_artifact_type_inventory']
    require(len({row['id'] for row in artifact_types}) == len(artifact_types) == 35,
            'artifact type coverage incomplete')
    require(all(row['path'] in inventory for row in artifact_types), 'artifact path unmapped')
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
            acceptance['independent_review_profile'] == 'gpt-6-astra-max' and
            acceptance['reviewer_distinct_from_author_and_integrator'] is True and
            acceptance['final_read_only_review_after_evidence_added'] is True,
            'authority or independent review boundary weakened')

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
        require(value.get('schema_version') == 'texenda.project-blueprint-origin.v2' and
                value.get('adoption_mode') == 'mapped-existing' and
                value.get('generated_new_project') is False and
                value.get('reference_qualification') == 'inspected_structural_reference_only',
                'origin schema cannot truthfully represent mapped-existing')


def audit_candidate(root, baseline):
    """Parse candidate files and compare only the explicit public package scope."""
    names = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
        cwd=root).decode().split('\0')
    counts = {'JSON': 0, 'TOML': 0, 'Python': 0, 'new_markdown_links': 0,
              'sealed_files': 0, 'source_files': 0}
    for name in filter(None, names):
        require(not name.startswith('.texenda/') and not name.lower().endswith('.csv'),
                'private/local input entered candidate inspection scope')
        path = root / name
        require(not path.is_symlink(), 'candidate inspection refuses symlinks')
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
                 'project-dossier/transition/README.md'):
        path = root / name
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
            target = urllib.parse.unquote(target.split('#')[0])
            if target and '://' not in target:
                require((path.parent / target).exists(), 'new local link missing: ' + target)
                counts['new_markdown_links'] += 1
    source = Path(HOME) / 'sources/handoff-1.1.0-20260914'
    if not source.exists():
        source = Path(HOME)
    for row in baseline['filesystem']['author_source_files']:
        path = source / row['path']
        require(not path.is_symlink(), 'source package symlink denied')
        require(sha(path.read_bytes()) == row['sha256'], 'source package changed: ' + row['path'])
        counts['source_files'] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--audit', action='store_true', help='Also parse candidate files, links and package bytes.')
    args = parser.parse_args()
    try:
        crosswalk, baseline, manifest = [loads((ROOT / p).read_text())
                                         for p in (CROSSWALK, BASELINE, MANIFEST)]
        counts = validate(crosswalk, baseline, manifest)
        verify_bound_inputs(ROOT, baseline)
        verify_actual_stores(ROOT)
        if args.audit:
            counts['audit'] = audit_candidate(ROOT, baseline)
    except (ContractError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'status': 'FAIL', 'reason': str(exc)}))
        return 1
    print(json.dumps({'status': 'PASS', **counts,
                      'scope': 'static transition contracts and original Git-bound inputs only',
                      'live_state_checked': False, 'moves_executed': False,
                      'private_input_accessed': False, 'approval': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
