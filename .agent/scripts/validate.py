#!/usr/bin/env python3
"""Read-only validation aggregator for Texenda's mapped agent facade."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tomllib
import urllib.parse

sys.dont_write_bytecode = True
from common import (EVIDENCE_PREFIX, GENERATED_PATHS, ROOT, SOURCE_SCOPE_EXCLUSIONS,
                    ValidationError, binding, candidate_paths, canonical, evidence_rows,
                    git, git_identity, ledger_facts, load_json, loads, require, sha,
                    revision_source_rows, source_rows, scope_digest, valid_sha)


KERNEL_KEYS = {
    'policy.json': {'schema_version', 'authority', 'default_posture', 'action_classes',
                    'hard_denials', 'escalation', 'enforcement'},
    'context.json': {'schema_version', 'authority', 'precedence', 'trust_classes',
                     'conflict_rules', 'current_state_rule'},
    'schema.json': {'schema_version', 'authority', 'record_ids', 'status_vocabularies',
                    'compatibility'},
    'lifecycle.json': {'schema_version', 'authority', 'scope', 'transitions', 'exclusions'},
    'tools.json': {'schema_version', 'authority', 'availability_source', 'permission_source',
                   'tools'},
    'validators.json': {'schema_version', 'authority', 'commands'},
    'project.json': {'schema_version', 'project_id', 'adoption_mode', 'profile',
                     'repository_role', 'dossier', 'extensions', 'external_state'},
}
INDEX_STORES = ('tasks', 'decisions', 'evidence', 'reviews')
GENERATED_FILES = (
    '.agent/generated/manifest.json',
    '.agent/generated/validation-report.json',
    '.agent/state/current.json',
    '.agent/state/RESUME.md',
    'project-dossier/CANONICAL_SOURCE_MAP.md',
    'project-dossier/current-state/current.json',
    'project-dossier/current-state/README.md',
    'project-dossier/handoff/START_HERE.md',
    'project-dossier/machine-readable/evidence-index.json',
    'project-dossier/machine-readable/findings.json',
    'project-dossier/machine-readable/path-authority.json',
)
RECORD_ID = re.compile(r'^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]{4}$')


def strict_parsing(root=ROOT):
    counts = {'json': 0, 'toml': 0, 'python': 0}
    for name in candidate_paths(root):
        path = root / name
        if not path.is_file() or path.is_symlink():
            continue
        if name.startswith('.agent/tests/fixtures/invalid/'):
            continue
        if path.suffix == '.json':
            loads(path.read_bytes())
            counts['json'] += 1
        elif path.suffix == '.toml':
            tomllib.loads(path.read_text())
            counts['toml'] += 1
        elif path.suffix == '.py':
            ast.parse(path.read_text(), filename=name)
            counts['python'] += 1
    return counts


def validate_kernel(root=ROOT):
    values = {}
    for name, keys in KERNEL_KEYS.items():
        value = load_json(root / '.agent' / name)
        require(isinstance(value, dict) and set(value) == keys, name + ' is not closed')
        require(value.get('schema_version') == 'texenda.agent.v1', name + ' schema mismatch')
        values[name] = value
    policy = values['policy.json']
    require(policy['default_posture'] == 'deny_unless_current_higher_authority_and_scope_allow',
            'policy is not deny-by-default')
    denied = set(policy['hard_denials'])
    require({'push_or_remote_branch', 'github_or_actions_mutation', 'external_spend',
             'deployment_publication_or_sending', 'private_input_content_access',
             'receipt_or_git_history_rewrite', 'destructive_cleanup'} <= denied,
            'hard external/private/history denials are incomplete')
    context = values['context.json']
    require(context['precedence'][:2] == ['platform_system_sandbox_tool',
                                          'current_operator_instruction'],
            'context precedence weakened')
    require(context['trust_classes']['retrieved_or_generated']['instruction_authority'] is False,
            'untrusted content acquired authority')
    lifecycle = values['lifecycle.json']
    require(lifecycle['scope'] == 'generic_record_metadata_only'
            and 'texenda_wp_state_machine' in lifecycle['exclusions'],
            'generic lifecycle duplicates the Texenda WP lifecycle')
    tools = values['tools.json']
    require(tools['availability_source'] == 'live_coordination_status'
            and tools['permission_source'] == '.agent/policy.json'
            and 'roster' not in tools, 'tool file copied availability or roster authority')
    project = values['project.json']
    require(project['adoption_mode'] == 'mapped-existing' and project['profile'] == 'high-assurance',
            'project adoption profile is false')
    extensions = project['extensions']
    require(len(extensions) == 1 and extensions[0]['id'] == 'texenda-coordination'
            and extensions[0]['authority_effect'] == 'restrictions_only',
            'coordination extension is missing or expansive')
    return values


def validate_nested_instruction_text(text):
    normalized = ' '.join(text.lower().split())
    forbidden = ('ignore the root instructions', 'override higher authority',
                 'may weaken the root policy', 'expand its own authority')
    require(not any(phrase in normalized for phrase in forbidden),
            'nested instruction attempts to weaken higher authority')


def validate_instruction_scope(root=ROOT):
    count = 0
    for path in sorted(root.rglob('AGENTS.md')):
        if '.git' in path.relative_to(root).parts:
            continue
        require(path.is_file() and not path.is_symlink(), 'instruction file must be regular')
        validate_nested_instruction_text(path.read_text())
        count += 1
    return count


def validate_origin(root=ROOT):
    schema_path = root / '.agent/schemas/project-blueprint-origin.v2.schema.json'
    schema = load_json(schema_path)
    require(schema.get('$id') == 'urn:texenda:project-blueprint-origin:v2'
            and schema.get('additionalProperties') is False,
            'origin successor schema is not strict/versioned')
    record = load_json(root / '.project-blueprint-origin.json')
    required = set(schema['required'])
    require(set(record) == required == set(schema['properties']), 'origin record is not closed')
    require(record['schema_version'] == 'texenda.project-blueprint-origin.v2'
            and record['adoption_mode'] == 'mapped-existing'
            and record['generated_new_project'] is False
            and record['reference_qualification'] == 'inspected_structural_reference_only'
            and record['selected_version'] == '1.0.0'
            and record['profile'] == 'high-assurance', 'origin record overclaims adoption')
    newer = record['newer_candidate']
    require(newer['declared_version'] == '4.3.0' and newer['qualified'] is False
            and newer['working_tree'] == 'dirty', 'newer blueprint limitation was lost')
    boundary = record['transfer_boundary']
    require(all(boundary[key] is False for key in
                ('project_facts', 'permissions', 'accepted_decisions', 'evidence',
                 'status', 'readiness')), 'blueprint authority/facts were transferred')
    predecessor = record['schema_provenance']
    require(predecessor['supersedes_schema'] == 'project-blueprint-origin.v1'
            and predecessor['reason'] == 'add_mapped_existing_without_generation_claim',
            'origin schema successor is not deliberate')
    return record


def validate_indexes(root=ROOT):
    for name in INDEX_STORES:
        directory = root / '.agent' / name
        require(directory.is_dir() and not directory.is_symlink(), 'missing index store: ' + name)
        files = sorted(path.name for path in directory.iterdir() if path.is_file())
        require(files == ['README.md'], 'second active record store under .agent/' + name)
    require(not (root / '.agent/events').exists(), 'second receipt/event store exists')
    require(not (root / 'project-dossier/canonical').exists(), 'copied canonical product owner exists')


def validate_extension(root=ROOT):
    extension = load_json(root / '.agent/extensions/texenda-coordination/extension.json')
    require(extension['authority_effect'] == 'restrictions_only'
            and extension['may_expand_authority'] is False
            and extension['live_roster_copied'] is False,
            'extension can expand authority or copied the live roster')
    allowed = ('tooling/coordination/', 'docs/decisions/ADR-0001-',
               'docs/decisions/ADR-0004-', 'tooling/workspace/relocate_state.py')
    for row in extension['bindings']:
        name = row['path']
        require(any(name.startswith(prefix) for prefix in allowed),
                'extension binding escapes confined paths: ' + name)
        path = root / name
        require(path.is_file() and not path.is_symlink() and sha(path.read_bytes()) == row['sha256'],
                'extension binding hash mismatch: ' + name)


def validate_registry(root=ROOT):
    registry = load_json(root / '.agent/validators.json')
    rows = registry['commands']
    require(isinstance(rows, list) and rows, 'validator registry is empty')
    ids = [row['id'] for row in rows]
    require(len(ids) == len(set(ids)), 'duplicate validator command ID')
    for row in rows:
        require(set(row) == {'id', 'argv', 'mode', 'required', 'run_in_check', 'purpose'},
                'validator command is not closed: ' + row.get('id', '?'))
        require(isinstance(row['argv'], list) and row['argv']
                and all(isinstance(item, str) and item for item in row['argv']),
                'validator command argv must be a nonempty string array')
        require(row['mode'] in ('read_only', 'synthetic_writes_only', 'refresh_writer'),
                'validator mode unknown')
        require(not any(item in {'sh', 'bash', 'zsh', '-c'} for item in row['argv']),
                'shell command delegation is forbidden')
    check = next((row for row in rows if row['id'] == 'facade-check'), None)
    refresh = next((row for row in rows if row['id'] == 'facade-refresh'), None)
    require(check and check['mode'] == 'read_only' and refresh and refresh['mode'] == 'refresh_writer',
            'check/refresh command contract missing')
    return registry


def validate_dossier(root=ROOT, *, generated=True):
    catalog = load_json(root / 'project-dossier/ARTIFACT_CATALOG.json')
    require(catalog['schema_version'] == 'texenda.dossier-artifact-catalog.v1'
            and catalog['authority'] == 'authoritative_inventory_metadata_only',
            'artifact catalog authority is invalid')
    rows = catalog['artifacts']
    paths = [row['path'] for row in rows]
    ids = [row['id'] for row in rows]
    require(len(paths) == len(set(paths)) and len(ids) == len(set(ids)),
            'duplicate dossier path or artifact ID')
    require(all(RECORD_ID.fullmatch(identifier) for identifier in ids),
            'invalid dossier artifact ID')
    classes = {'authoritative', 'navigation', 'generated_view', 'evidence', 'plan', 'history'}
    require(all(row['classification'] in classes for row in rows),
            'unknown dossier path classification')
    actual = sorted(path.relative_to(root).as_posix()
                    for path in (root / 'project-dossier').rglob('*') if path.is_file())
    if generated:
        require(sorted(paths) == actual, 'artifact catalog does not cover every dossier file')
    else:
        missing = set(paths) - set(actual)
        generated_catalog_paths = {row['path'] for row in rows
                                   if row['classification'] == 'generated_view'}
        require(not (set(actual) - set(paths)) and missing <= generated_catalog_paths,
                'artifact catalog does not cover non-generated dossier files')
    for row in rows:
        if row['classification'] == 'authoritative':
            require(row['owner_path'] == row['path'], 'authoritative dossier path is not its one owner')
        else:
            require(row['owner_path'] != row['path']
                    or row['classification'] in ('evidence', 'plan', 'history'),
                    'non-authoritative dossier view claims ownership')
    if generated:
        mirror = load_json(root / 'project-dossier/machine-readable/path-authority.json')
        expected = [{key: row[key] for key in ('path', 'classification', 'owner_path', 'concern_id')}
                    for row in rows]
        require(mirror['paths'] == expected, 'path-authority mirror differs from artifact catalog')
    return catalog


def validate_links(root=ROOT, *, allow_generated_missing=False):
    count = 0
    selected = [root / 'AGENTS.md', root / 'docs/agents/operating-guide.md']
    selected += sorted((root / '.agent').rglob('*.md'))
    selected += sorted((root / 'project-dossier').rglob('*.md'))
    for path in selected:
        if not path.is_file() or path.is_symlink():
            continue
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
            target = urllib.parse.unquote(target.split('#', 1)[0])
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            destination = Path(target)
            if not destination.is_absolute():
                destination = path.parent / destination
            if not destination.exists() and allow_generated_missing:
                try:
                    relative = destination.resolve(strict=False).relative_to(root.resolve()).as_posix()
                except ValueError:
                    relative = None
                if relative in GENERATED_FILES:
                    continue
            require(destination.exists() and not destination.is_symlink(),
                    'broken or symlinked local link in ' + str(path.relative_to(root)) + ': ' + target)
            try:
                destination.resolve().relative_to(root.resolve())
            except ValueError as exc:
                raise ValidationError('local link escapes repository: ' + target) from exc
            count += 1
    return count


def validate_crosswalk_correction(root=ROOT):
    crosswalk = load_json(root / 'project-dossier/transition/blueprint-adoption-crosswalk.json')
    blueprint = crosswalk['blueprint']
    require(blueprint['origin_schema_supports_mapped_existing'] is True
            and blueprint['origin_record_created'] is True,
            'crosswalk does not record completed origin-schema successor')
    evidence_rows_ = [row for row in crosswalk['supplemental_mappings']
                      if row.get('mapped_path') == 'project-dossier/evidence/README.md']
    require(len(evidence_rows_) == 1 and evidence_rows_[0]['role'] == 'index'
            and evidence_rows_[0]['concern_id'] == 'qualification_evidence',
            'owner-request dossier evidence index correction missing')
    ownership = crosswalk['ownership']
    for epoch in crosswalk['epochs']:
        owners = {}
        for row in ownership:
            owner = row['owner_by_epoch'][epoch]
            require(row['concern_id'] not in owners, 'duplicate mutable concern: ' + row['concern_id'])
            owners[row['concern_id']] = owner
    return crosswalk


def validate_evidence_records(root=ROOT):
    count = 0
    for name in git('ls-files', '-z', 'docs/qualification', root=root).split('\0'):
        if not name or not name.endswith('.json'):
            continue
        record = load_json(root / name)
        if not isinstance(record, dict):
            continue
        for check in record.get('checks', []):
            if check.get('status') not in ('PASS', 'FAIL'):
                continue
            evidence_path = check.get('evidence_path')
            require(isinstance(evidence_path, str) and evidence_path
                    and not PurePosixPath(evidence_path).is_absolute()
                    and '..' not in PurePosixPath(evidence_path).parts
                    and 'private-inputs' not in PurePosixPath(evidence_path).parts
                    and not evidence_path.lower().endswith('.csv'),
                    'PASS/FAIL evidence path is missing or unsafe')
            target = root / evidence_path
            require(target.is_file() and not target.is_symlink() and valid_sha(check.get('sha256'))
                    and sha(target.read_bytes()) == check['sha256'],
                    'PASS/FAIL evidence hash mismatch: ' + evidence_path)
            count += 1
    return count


def run_registry_checks(registry, root=ROOT, *, all_commands=False):
    results = []
    for row in registry['commands']:
        if row['id'] in ('facade-check', 'facade-refresh'):
            continue
        if not (all_commands or row['run_in_check']):
            continue
        result = subprocess.run(row['argv'], cwd=root, capture_output=True, text=True, check=False,
                                env={**dict(__import__('os').environ), 'PYTHONDONTWRITEBYTECODE': '1'})
        require(result.returncode == 0,
                'registered command failed: ' + row['id'] + '\n' + result.stdout + result.stderr)
        results.append({'id': row['id'], 'returncode': result.returncode})
    return results


def validate_generated(root=ROOT, state_root=None):
    markers = list((root / '.agent/generated').glob('.refresh-*'))
    require(not markers, 'interrupted refresh marker present')
    for name in GENERATED_FILES:
        path = root / name
        require(path.is_file() and not path.is_symlink(), 'generated output missing: ' + name)
    manifest = load_json(root / '.agent/generated/manifest.json')
    generation_id = manifest['generation_id']
    require(valid_sha(generation_id), 'invalid generated transaction ID')
    rows = source_rows(root)
    require(manifest['source_files'] == rows
            and manifest['source_scope_sha256'] == scope_digest(rows)
            and manifest['source_scope_exclusions'] == SOURCE_SCOPE_EXCLUSIONS,
            'generated source scope is stale')
    evidence = evidence_rows(root)
    require(manifest['evidence_files'] == evidence
            and manifest['evidence_scope_sha256'] == scope_digest(evidence),
            'generated evidence index is stale')
    revision = manifest['source_git_revision']
    recorded_tree = git('rev-parse', revision + '^{tree}', root=root).strip()
    require(recorded_tree == manifest['source_git_tree'], 'generated source Git identity is invalid')
    require(revision_source_rows(revision, root) == manifest['source_files'],
            'recorded source revision does not match the declared source scope')
    facts = ledger_facts(root, state_root,
                         fallback_state_root=manifest['ledger_observation']['state_root'])
    for key in ('ledger_sha256', 'receipt_count', 'receipt_tip', 'roster_evidence_sha256'):
        require(manifest[key] == facts[key], 'generated ledger projection is stale: ' + key)
    require(manifest['ledger_observation']['state_root'] == facts['state_root'],
            'generated state-root observation is stale')
    current = load_json(root / '.agent/state/current.json')
    required = {'schema_version', 'generation_id', 'generated_at', 'authority',
                'source_git_revision', 'source_git_tree', 'source_scope_sha256',
                'source_scope_exclusions', 'ledger_sha256', 'receipt_count', 'receipt_tip',
                'roster_evidence_sha256', 'evidence_scope_sha256', 'freshness_rule',
                'ledger_observation'}
    require(set(current) == required and current['generation_id'] == generation_id,
            'current-state projection is not closed or transaction-consistent')
    report = load_json(root / '.agent/generated/validation-report.json')
    require(report['generation_id'] == generation_id and report['result'] == 'PASS',
            'generated validation report is partial or failed')
    for name in ('project-dossier/current-state/current.json',
                 'project-dossier/machine-readable/evidence-index.json',
                 'project-dossier/machine-readable/findings.json',
                 'project-dossier/machine-readable/path-authority.json'):
        value = load_json(root / name)
        require(value['generation_id'] == generation_id, 'partial generation: ' + name)
    evidence_index = load_json(root / 'project-dossier/machine-readable/evidence-index.json')
    require(evidence_index['evidence'] == evidence
            and evidence_index['evidence_scope_sha256'] == scope_digest(evidence),
            'evidence mirror is stale')
    findings = load_json(root / 'project-dossier/conformance/findings.json')
    findings_mirror = load_json(root / 'project-dossier/machine-readable/findings.json')
    require(findings_mirror['source_sha256'] == sha((root / 'project-dossier/conformance/findings.json').read_bytes())
            and findings_mirror['findings'] == findings['findings'], 'findings mirror is stale')
    head, tree = git_identity(root)
    return {'generation_id': generation_id, 'current_git_revision': head,
            'current_git_tree': tree, 'source_scope_sha256': manifest['source_scope_sha256'],
            'ledger_sha256': facts['ledger_sha256']}


def validate(root=ROOT, state_root=None, *, generated=True, run_all=False):
    require(sys.version_info >= (3, 11), 'Python 3.11 or newer is required')
    parsing = strict_parsing(root)
    validate_kernel(root)
    instruction_files = validate_instruction_scope(root)
    validate_origin(root)
    validate_indexes(root)
    validate_extension(root)
    registry = validate_registry(root)
    validate_crosswalk_correction(root)
    catalog = validate_dossier(root, generated=generated)
    links = validate_links(root, allow_generated_missing=not generated)
    evidence_checks = validate_evidence_records(root)
    registered = run_registry_checks(registry, root, all_commands=run_all)
    result = {
        'status': 'PASS',
        'mode': 'read_only',
        'parsing': parsing,
        'dossier_paths': len(catalog['artifacts']),
        'instruction_files': instruction_files,
        'local_links': links,
        'bound_pass_fail_evidence_checks': evidence_checks,
        'registered_commands_run': registered,
        'private_input_content_accessed': False,
        'external_effects': False,
        'product_or_external_gate': 'none',
    }
    if generated:
        result['generated'] = validate_generated(root, state_root)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--state-root', type=Path)
    parser.add_argument('--all', action='store_true', help='run every registered non-refresh command')
    args = parser.parse_args(argv)
    try:
        print(json.dumps(validate(ROOT, args.state_root, run_all=args.all), indent=2))
        return 0
    except (ValidationError, OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
