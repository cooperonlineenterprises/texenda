#!/usr/bin/env python3
"""Read-only validation aggregator for Texenda's mapped agent facade."""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tomllib
import urllib.parse

sys.dont_write_bytecode = True
from common import (EVIDENCE_PREFIX, GENERATED_OUTPUT_PATHS, ROOT, SOURCE_SCOPE_EXCLUSIONS,
                    ValidationError, binding, candidate_paths, canonical, evidence_rows,
                    git, git_identity, ledger_facts, load_json, loads, require, resolved_directory, sha,
                    no_symlink_components, reject_private_name, revision_source_rows,
                    source_rows, scope_digest, stable_file_bytes, valid_sha)


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
    'validators.json': {'schema_version', 'authority', 'execution_context', 'commands'},
    'project.json': {'schema_version', 'project_id', 'adoption_mode', 'profile',
                     'repository_role', 'dossier', 'extensions', 'external_state'},
}
INDEX_STORES = ('tasks', 'decisions', 'evidence', 'reviews')
GENERATED_FILES = GENERATED_OUTPUT_PATHS
RECORD_ID = re.compile(r'^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]{4}$')


def strict_parsing(root=ROOT):
    counts = {'json': 0, 'toml': 0, 'python': 0}
    for name in candidate_paths(root):
        reject_private_name(name, 'parse candidate')
        path = root / name
        no_symlink_components(path.absolute(), 'parse candidate')
        if not path.is_file():
            continue
        if name.startswith('.agent/tests/fixtures/invalid/'):
            continue
        raw = stable_file_bytes(path, 'parse candidate')
        if path.suffix == '.json':
            loads(raw)
            counts['json'] += 1
        elif path.suffix == '.toml':
            tomllib.loads(raw.decode())
            counts['toml'] += 1
        elif path.suffix == '.py':
            ast.parse(raw.decode(), filename=name)
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
    for name in candidate_paths(root):
        if not name.endswith('AGENTS.md'):
            continue
        common_name = PurePosixPath(name)
        require('private-inputs' not in common_name.parts and not name.lower().endswith('.csv'),
                'private instruction path entered discovery')
        path = root / name
        no_symlink_components(path.absolute(), 'instruction file')
        require(path.is_file(), 'instruction file must be regular')
        validate_nested_instruction_text(stable_file_bytes(path, 'instruction file').decode())
        count += 1
    return count


def validate_schema_instance(value, schema, path='$'):
    if 'const' in schema:
        expected = schema['const']
        require(type(value) is type(expected) and value == expected,
                path + ' differs from schema const')
    if 'enum' in schema:
        require(any(type(value) is type(item) and value == item for item in schema['enum']),
                path + ' is outside schema enum')
    declared = schema.get('type')
    types = {
        'object': dict,
        'array': list,
        'string': str,
        'integer': int,
        'number': (int, float),
        'boolean': bool,
        'null': type(None),
    }
    if declared:
        expected_type = types.get(declared)
        require(expected_type is not None, path + ' uses unsupported schema type')
        if declared in ('integer', 'number'):
            require(type(value) in ((int,) if declared == 'integer' else (int, float)),
                    path + ' has wrong type')
        else:
            require(type(value) is expected_type, path + ' has wrong type')
    if isinstance(value, str):
        if 'minLength' in schema:
            require(len(value) >= schema['minLength'], path + ' is shorter than minLength')
        if 'maxLength' in schema:
            require(len(value) <= schema['maxLength'], path + ' exceeds maxLength')
        if 'pattern' in schema:
            require(re.search(schema['pattern'], value) is not None, path + ' fails pattern')
    if type(value) is int and 'minimum' in schema:
        require(value >= schema['minimum'], path + ' is below minimum')
    if isinstance(value, dict):
        properties = schema.get('properties', {})
        required = schema.get('required', [])
        require(all(isinstance(item, str) for item in required), path + ' has invalid required keys')
        require(set(required) <= set(value), path + ' is missing required keys')
        if schema.get('additionalProperties') is False:
            require(set(value) <= set(properties), path + ' has additional properties')
        for key, item in value.items():
            if key in properties:
                validate_schema_instance(item, properties[key], path + '.' + key)
    if isinstance(value, list) and 'items' in schema:
        for index, item in enumerate(value):
            validate_schema_instance(item, schema['items'], f'{path}[{index}]')


def validate_origin_evidence(record, evidence):
    """Bind the separated origin facts to the retained failed qualification."""
    require(evidence.get('schema_version') == 'texenda.followup-observations.v1',
            'origin qualification evidence has an unknown schema')
    require(evidence.get('clean_source') == record['clean_candidate'],
            'clean committed origin differs from its qualification evidence')
    require(evidence.get('dirty_checkout_observation') == record['dirty_checkout_observation'],
            'dirty checkout origin differs from its historical observation')
    expected = {
        'clean-source-contracts': 'PASS',
        'clean-source-acceptance': 'PASS',
        'clean-source-full-validator': 'FAIL',
    }
    checks = evidence.get('checks')
    require(isinstance(checks, list), 'origin qualification checks are missing')
    for identifier, status in expected.items():
        matches = [check for check in checks if isinstance(check, dict)
                   and check.get('id') == identifier]
        require(len(matches) == 1 and matches[0].get('status') == status,
                'origin qualification is missing its exact passing/failed check: ' + identifier)


def validate_origin(root=ROOT):
    schema_path = root / '.agent/schemas/project-blueprint-origin.v3.schema.json'
    schema = load_json(schema_path)
    require(schema.get('$id') == 'urn:texenda:project-blueprint-origin:v3'
            and schema.get('additionalProperties') is False,
            'origin successor schema is not strict/versioned')
    record = load_json(root / '.project-blueprint-origin.json')
    required = set(schema['required'])
    require(set(record) == required == set(schema['properties']), 'origin record is not closed')
    validate_schema_instance(record, schema)
    require(record['schema_version'] == 'texenda.project-blueprint-origin.v3'
            and record['adoption_mode'] == 'mapped-existing'
            and record['generated_new_project'] is False
            and record['reference_qualification'] == 'inspected_structural_reference_only'
            and record['selected_version'] == '1.0.0'
            and record['profile'] == 'high-assurance', 'origin record overclaims adoption')
    clean = record['clean_candidate']
    require(clean['committed_version'] == '4.2.0'
            and clean['revision'] == clean['local_main'] == clean['observed_remote_main']
            == '5e2d3025aea6b1574ab984e5ebb89b5602a38535'
            and clean['tree'] == '3c732979e580c80b020d09c22ce86f5202110518'
            and clean['working_tree'] == 'clean'
            and clean['qualified'] is False and clean['adopted'] is False
            and clean['qualification_checks'] == {
                'source_contracts': 'PASS', 'acceptance': 'PASS', 'full_validator': 'FAIL'},
            'clean committed candidate version/qualification boundary changed')
    dirty = record['dirty_checkout_observation']
    require(dirty['working_version'] == '4.3.0' and dirty['working_tree'] == 'dirty'
            and dirty['version_committed'] is False
            and dirty['version_attributed_to_clean_revision'] is False
            and 'revision' not in dirty and 'tree' not in dirty
            and dirty['qualified'] is False and dirty['adopted'] is False,
            'dirty working version was attributed to a commit or adopted')
    upgrade = record['upgrade_plan']
    require(upgrade['reviewed_seed'] is None and upgrade['applied'] is False
            and upgrade['output_written'] is False and upgrade['authority_validated'] is False
            and upgrade['continuation_id'] == 'OCTON-CONT-0001',
            'blocked upgrade acquired a seed, approval, output or adoption')
    boundary = record['transfer_boundary']
    require(all(boundary[key] is False for key in
                ('project_facts', 'permissions', 'accepted_decisions', 'evidence',
                 'status', 'readiness')), 'blueprint authority/facts were transferred')
    predecessor = record['schema_provenance']
    require(predecessor['supersedes_schema'] == 'texenda.project-blueprint-origin.v2'
            and predecessor['reason'] == 'separate_clean_committed_and_dirty_worktree_provenance'
            and predecessor['predecessor_path'] == '.agent/schemas/project-blueprint-origin.v2.schema.json'
            and predecessor['predecessor_sha256']
            == 'e6ba4f8b1617b30a1aa2a130fd603e2e74f3ecdac81de5801521f526f7de63cc',
            'origin schema successor lost the preserved v2 boundary')
    require(sha(stable_file_bytes(root / predecessor['predecessor_path'], 'origin v2 predecessor'))
            == predecessor['predecessor_sha256'], 'historical origin v2 schema changed')
    evidence_path = record['qualification_evidence']
    require(evidence_path == 'docs/qualification/evidence/2026-09-15-editor-blueprint-followup-observations.evidence.json',
            'origin qualification evidence path changed')
    validate_origin_evidence(record, load_json(root / evidence_path))
    return record


def validate_indexes(root=ROOT):
    for name in INDEX_STORES:
        directory = root / '.agent' / name
        no_symlink_components(directory.absolute(), 'index store')
        require(directory.is_dir(), 'missing index store: ' + name)
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
        no_symlink_components(path.absolute(), 'extension binding')
        require(path.is_file() and sha(stable_file_bytes(path, 'extension binding')) == row['sha256'],
                'extension binding hash mismatch: ' + name)


def validate_registry(root=ROOT):
    registry = load_json(root / '.agent/validators.json')
    rows = registry['commands']
    require(isinstance(rows, list) and rows, 'validator registry is empty')
    ids = [row['id'] for row in rows]
    require(len(ids) == len(set(ids)), 'duplicate validator command ID')
    context = registry['execution_context']
    require(set(context) == {'shell', 'working_directory', 'repository_root', 'project_home',
                             'state_root', 'global_option_placement',
                             'ordinary_entry_command'}
            and context['shell'] is False
            and context['working_directory'] == '{repository_root}'
            and context['ordinary_entry_command']
            == ('env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py '
                '--check --all --state-root '
                '/Users/jamesryancooper/Projects/texenda/local/agent-state/texenda'),
            'validator execution context is not closed or shell-free')
    row_fields = {'id', 'argv', 'mode', 'required', 'run_in_check', 'purpose',
                  'working_directory', 'context_parameters'}
    for row in rows:
        require(set(row) == row_fields,
                'validator command is not closed: ' + row.get('id', '?'))
        require(isinstance(row['argv'], list) and row['argv']
                and all(isinstance(item, str) and item for item in row['argv']),
                'validator command argv must be a nonempty string array')
        require(row['mode'] in ('read_only', 'synthetic_writes_only', 'refresh_writer'),
                'validator mode unknown')
        require(not any(item in {'sh', 'bash', 'zsh', '-c'} for item in row['argv']),
                'shell command delegation is forbidden')
        require(row['working_directory'] == '{repository_root}'
                and isinstance(row['context_parameters'], list)
                and row['context_parameters']
                and row['context_parameters'][0] == 'repository_root'
                and len(row['context_parameters']) == len(set(row['context_parameters'])),
                'validator execution parameterization is invalid')
        tokens = {match for item in row['argv'] for match in re.findall(r'{[^}]+}', item)}
        allowed_tokens = {'{repository_root}', '{project_home}', '{state_root}'}
        require(tokens <= allowed_tokens, 'unknown validator argv token')
        if '{state_root}' in tokens:
            require('state_root_optional_before_binding' in row['context_parameters'],
                    'state-root token lacks declared parameterization')
        if '{project_home}' in tokens:
            require('project_home' in row['context_parameters'],
                    'project-home token lacks declared parameterization')
        names_refresh = any(item.endswith('.agent/scripts/refresh.py') for item in row['argv'])
        require(names_refresh is (row['mode'] == 'refresh_writer'),
                'refresh command mode is mislabeled')
        if row['mode'] == 'refresh_writer':
            require(row['id'] in {'facade-refresh', 'facade-refresh-recovery'}
                    and row['run_in_check'] is False,
                    'refresh writer cannot be registered as a check')
    check = next((row for row in rows if row['id'] == 'facade-check'), None)
    refresh = next((row for row in rows if row['id'] == 'facade-refresh'), None)
    require(check and check['mode'] == 'read_only' and refresh and refresh['mode'] == 'refresh_writer',
            'check/refresh command contract missing')
    state_check = next((row for row in rows if row['id'] == 'coordination-state-check'), None)
    require(state_check and state_check['argv'][-1] == 'check'
            and 'init' not in state_check['argv'],
            'coordination check registry could mutate state')
    return registry


def execution_context(root=ROOT, state_root=None):
    repository = resolved_directory(Path(root).absolute(), 'validator repository root')
    if repository.name == 'repo' and (repository.parent / 'WORKSPACE.md').is_file():
        project_home = repository.parent
    elif (repository.parent.name == 'worktrees'
          and (repository.parent.parent / 'WORKSPACE.md').is_file()):
        project_home = repository.parent.parent
    else:
        project_home = repository.parent
    project_home = resolved_directory(project_home.absolute(), 'validator project home')
    selected_state = None
    if state_root is not None:
        selected_state = resolved_directory(Path(state_root).absolute(), 'validator state root')
    elif binding(repository):
        raise ValidationError('active binding requires explicit --state-root for delegated checks')
    return {
        'repository_root': str(repository),
        'project_home': str(project_home),
        'state_root': str(selected_state) if selected_state else None,
    }


def resolve_command(row, context):
    argv = list(row['argv'])
    if context['state_root'] is None:
        while '{state_root}' in argv:
            index = argv.index('{state_root}')
            require(index > 0 and argv[index - 1] == '--state-root',
                    'optional state root must be a complete argv option pair')
            del argv[index - 1:index + 1]
    replacements = {f'{{{key}}}': value for key, value in context.items() if value is not None}
    resolved = []
    for item in argv:
        for token, value in replacements.items():
            item = item.replace(token, value)
        require('{' not in item and '}' not in item and '\x00' not in item and '\n' not in item,
                'unresolved or unsafe validator argv')
        resolved.append(item)
    require(resolved[0] in ('python3', 'git'), 'validator executable is not allowlisted')
    if resolved[0] == 'python3':
        require(len(resolved) >= 3 and resolved[1] == '-B',
                'Python validator commands must disable bytecode writes')
        if resolved[2] == '-m':
            require(len(resolved) > 3 and resolved[3] == 'unittest',
                    'only the standard-library unittest module may be delegated')
        else:
            script = Path(resolved[2])
            script = script if script.is_absolute() else Path(context['repository_root']) / script
            script = Path(os.path.abspath(script))
            repository = Path(context['repository_root'])
            project_home = Path(context['project_home'])
            require(script.is_relative_to(repository)
                    or script.is_relative_to(project_home / 'sources'),
                    'validator script escapes the validated repository/source roots')
            reject_private_name(script.as_posix(), 'validator script')
            no_symlink_components(script, 'validator script')
            require(script.is_file(), 'validator script is missing')
    if row['id'] == 'coordination-state-check' and context['state_root'] is not None:
        state_index = resolved.index('--state-root')
        require(state_index < resolved.index('check'),
                'harness --state-root must be a global option before the subcommand')
    return resolved


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
    actual = []
    for name in candidate_paths(root):
        if not name.startswith('project-dossier/'):
            continue
        path = root / name
        no_symlink_components(path.absolute(), 'dossier path')
        if path.is_file():
            actual.append(path.relative_to(root).as_posix())
    actual.sort()
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
    history_path = 'project-dossier/history/2026-09-15-workspace-transition-completed.md'
    history = root / history_path
    history_sha = '1f5b0b1aa816f6bcd34f591a0b5f9f5b4e9d6e8bf35474ca77367418fb930919'
    require(history.is_file()
            and sha(stable_file_bytes(history, 'transition history')) == history_sha,
            'completed transition history bytes changed')
    history_row = next((row for row in rows if row['path'] == history_path), None)
    require(history_row is not None and history_row['classification'] == 'history',
            'completed transition history is not catalogued as history')
    supersession = load_json(root / 'project-dossier/SUPERSESSION.json')
    require(supersession['current_version'] == '1.2.0-mapped-existing'
            and len(supersession['records']) == 1
            and supersession['records'][0]['prior_sha256'] == history_sha
            and supersession['records'][0]['retained_history_path'] == history_path,
            'dossier supersession does not preserve the completed transition')
    if generated:
        mirror = load_json(root / 'project-dossier/machine-readable/path-authority.json')
        expected = [{key: row[key] for key in ('path', 'classification', 'owner_path', 'concern_id')}
                    for row in rows]
        require(mirror['paths'] == expected, 'path-authority mirror differs from artifact catalog')
    return catalog


def validate_links(root=ROOT, *, allow_generated_missing=False):
    count = 0
    names = {'AGENTS.md', 'docs/agents/operating-guide.md'}
    names.update(name for name in candidate_paths(root)
                 if name.endswith('.md')
                 and (name.startswith('.agent/') or name.startswith('project-dossier/')))
    selected = [root / name for name in sorted(names)]
    for path in selected:
        if path.relative_to(root).as_posix() == (
                'project-dossier/history/2026-09-15-workspace-transition-completed.md'):
            # This exact, separately hash-validated snapshot keeps its bytes and
            # therefore its original transition/-relative links. Current
            # navigation is supplied by history/README.md; rewriting the snapshot
            # would falsify its provenance.
            continue
        no_symlink_components(path.absolute(), 'Markdown path')
        if not path.is_file():
            continue
        markdown = stable_file_bytes(path, 'Markdown path').decode()
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', markdown):
            target = urllib.parse.unquote(target.split('#', 1)[0])
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            destination = Path(target)
            if not destination.is_absolute():
                destination = path.parent / destination
            destination = Path(os.path.abspath(destination))
            try:
                relative = destination.relative_to(root.absolute()).as_posix()
            except ValueError as exc:
                raise ValidationError('local link escapes repository: ' + target) from exc
            if not destination.exists() and allow_generated_missing:
                if relative in GENERATED_FILES:
                    continue
            no_symlink_components(destination.absolute(), 'Markdown link')
            require(destination.exists(),
                    'broken or symlinked local link in ' + str(path.relative_to(root)) + ': ' + target)
            require(destination.resolve() == destination,
                    'local link uses a non-canonical or symlinked path: ' + target)
            count += 1
    return count


def validate_crosswalk_correction(root=ROOT):
    crosswalk = load_json(root / 'project-dossier/transition/blueprint-adoption-crosswalk.json')
    blueprint = crosswalk['blueprint']
    require(crosswalk['status'] == 'completed_current_contract'
            and crosswalk.get('current_epoch') == 'external_state'
            and crosswalk['epochs'][-1] == crosswalk['current_epoch'],
            'crosswalk current epoch is stale or incomplete')
    require(blueprint['origin_schema_supports_mapped_existing'] is True
            and blueprint['origin_record_created'] is True
            and blueprint['origin_schema']
            == '.agent/schemas/project-blueprint-origin.v3.schema.json',
            'crosswalk does not record completed origin-schema successor')
    origin_schema = next(row for row in crosswalk['mappings']
                         if row['blueprint_path']
                         == '.agent/schemas/project-blueprint-origin.schema.json')
    require(origin_schema['mapped_path']
            == '.agent/schemas/project-blueprint-origin.v3.schema.json',
            'crosswalk still maps the active origin schema to v2')
    history = next(row for row in crosswalk['mappings']
                   if row['blueprint_path'] == 'project-dossier/history/README.md')
    require(history['mapped_path'] == 'project-dossier/history/README.md'
            and history['role'] == 'historical_source',
            'tracked transition history index is not the active mapping')
    editor = next(row for row in crosswalk['deferred_semantic_work']
                  if row['id'] == 'DEFER-WSM-0001')
    require(editor['status'] == 'resolved_scoped_by_ADR-0005'
            and editor['does_not_modify_packages'] is True
            and all(value in editor['remaining_gate'] for value in ('WP-10', 'VAL-03')),
            'editor wording resolution lost its remaining gate boundary')
    require(crosswalk['facade_acceptance']['origin_schema_successor_present'] is True
            and crosswalk['facade_acceptance']['real_mapped_task_lifecycle_demonstrated'] is True,
            'completed facade/origin demonstrations are still represented as pending')
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
            no_symlink_components(target.absolute(), 'qualification evidence path')
            require(target.is_file() and valid_sha(check.get('sha256'))
                    and sha(stable_file_bytes(target, 'qualification evidence path')) == check['sha256'],
                    'PASS/FAIL evidence hash mismatch: ' + evidence_path)
            count += 1
    return count


def ensure_no_interrupted_refresh(root=ROOT):
    generated = root / '.agent/generated'
    no_symlink_components(generated.absolute(), 'generated directory')
    markers = list(generated.glob('.refresh-*'))
    require(not markers, 'interrupted refresh marker present')


def run_registry_checks(registry, root=ROOT, state_root=None, *, all_commands=False,
                        allow_refresh_marker=False):
    results = []
    context = execution_context(root, state_root)
    for row in registry['commands']:
        # A check can never dispatch a writer, even under --all.
        if row['mode'] == 'refresh_writer':
            results.append({'id': row['id'], 'status': 'SKIPPED_WRITER'})
            continue
        if row['id'] == 'facade-check':
            continue
        if not (all_commands or row['run_in_check']):
            continue
        if not allow_refresh_marker:
            ensure_no_interrupted_refresh(root)
        argv = resolve_command(row, context)
        environment = {**dict(os.environ), 'PYTHONDONTWRITEBYTECODE': '1'}
        if all_commands:
            environment['TEXENDA_CHECK_ALL_ACTIVE'] = '1'
        result = subprocess.run(argv, cwd=context['repository_root'],
                                capture_output=True, text=True, check=False,
                                env=environment)
        require(result.returncode == 0,
                'registered command failed: ' + row['id'] + '\n' + result.stdout + result.stderr)
        results.append({'id': row['id'], 'returncode': result.returncode})
    return results


def validate_generated(root=ROOT, state_root=None):
    ensure_no_interrupted_refresh(root)
    for name in GENERATED_FILES:
        path = root / name
        require(path.is_file() and not path.is_symlink(), 'generated output missing: ' + name)
    manifest = load_json(root / '.agent/generated/manifest.json')
    generation_id = manifest['generation_id']
    require(valid_sha(generation_id), 'invalid generated transaction ID')
    generated_at = manifest.get('generated_at')
    require(isinstance(generated_at, str)
            and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00', generated_at),
            'generated timestamp must be second-precision UTC ISO-8601')
    parsed_time = dt.datetime.fromisoformat(generated_at)
    require(parsed_time.tzinfo == dt.timezone.utc, 'generated timestamp is not UTC')
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
    basis = {
        'source_scope_sha256': manifest['source_scope_sha256'],
        'evidence_scope_sha256': manifest['evidence_scope_sha256'],
        'ledger_sha256': manifest['ledger_sha256'],
        'receipt_count': manifest['receipt_count'],
        'receipt_tip': manifest['receipt_tip'],
    }
    require(sha(canonical(basis)) == generation_id,
            'generated transaction ID does not match its declared derivation')
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
    require(findings_mirror['source_sha256'] == sha(stable_file_bytes(
                root / 'project-dossier/conformance/findings.json', 'conformance findings'))
            and findings_mirror['findings'] == findings['findings'], 'findings mirror is stale')
    state_root_text = facts['state_root']
    validation_command = (
        'env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py '
        '--check --all --state-root ' + state_root_text
    )
    coordinator_command = (
        'env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py '
        '--root . --state-root ' + state_root_text
    )
    source_map_text = stable_file_bytes(
        root / 'project-dossier/CANONICAL_SOURCE_MAP.md', 'canonical source map').decode()
    require('Current ownership epoch: `external_state`.' in source_map_text
            and '| Concern | Current owner | Rule |' in source_map_text
            and '| Baseline owner |' not in source_map_text,
            'canonical source map does not lead with current ownership')
    resume_text = stable_file_bytes(root / '.agent/state/RESUME.md', 'resume view').decode()
    require(resume_text.startswith('# Resume ordinary Texenda work\n')
            and validation_command in resume_text,
            'resume view does not route ordinary work through explicit validation')
    handoff_text = stable_file_bytes(
        root / 'project-dossier/handoff/START_HERE.md', 'handoff view').decode()
    require(handoff_text.startswith('# Texenda ordinary handoff\n')
            and validation_command in handoff_text
            and all(coordinator_command + ' ' + command in handoff_text
                    for command in ('status', 'ready', 'context WP-01'))
            and handoff_text.index(validation_command) < handoff_text.index('[transition]'),
            'handoff is missing ordinary commands or leads with migration history')
    # Reconstruct every generated byte from validated sources, the recorded
    # source identity/time, and the stable ledger. This covers all eleven
    # outputs, including every Markdown byte and all manifest/report claims.
    import refresh as generator
    require(tuple(generator.OUTPUTS) == GENERATED_FILES,
            'generated output registry differs between check and refresh')
    effective_state_root = state_root or Path(manifest['ledger_observation']['state_root'])
    expected = generator.build(root, effective_state_root, generated_at=generated_at,
                               source_identity=(revision, manifest['source_git_tree']),
                               prevalidate=False)
    require(set(expected) == set(GENERATED_FILES), 'generated reconstruction scope is incomplete')
    for name in GENERATED_FILES:
        require(stable_file_bytes(root / name, 'generated output') == expected[name],
                'generated output bytes differ from deterministic reconstruction: ' + name)
    head, tree = git_identity(root)
    return {'generation_id': generation_id, 'current_git_revision': head,
            'current_git_tree': tree, 'source_scope_sha256': manifest['source_scope_sha256'],
            'ledger_sha256': facts['ledger_sha256']}


def validate(root=ROOT, state_root=None, *, generated=True, run_all=False,
             allow_refresh_marker=False):
    require(sys.version_info >= (3, 11), 'Python 3.11 or newer is required')
    if not allow_refresh_marker:
        ensure_no_interrupted_refresh(root)
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
    generated_result = validate_generated(root, state_root) if generated else None
    registered = run_registry_checks(registry, root, state_root, all_commands=run_all,
                                     allow_refresh_marker=allow_refresh_marker)
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
        result['generated'] = generated_result
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
