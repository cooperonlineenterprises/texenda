"""Repository-only readers for the scoped standalone operating contract."""
from __future__ import annotations

import re
import json
from pathlib import PurePosixPath

from common import (ROOT, load_json, loads, require, stable_file_bytes,
                    reject_private_name, no_symlink_components, git, sha)


ADR = 'docs/decisions/ADR-0007-standalone-workspace-operating-contract.md'
SCHEMA = '.agent/schemas/standalone-operating-contract.v1.schema.json'
RETENTION = 'project-dossier/registers/workspace-retention.json'
REMEDIATION = 'project-dossier/conformance/remediation-register.json'
RAIDQ = 'project-dossier/machine-readable/raidq.json'
DEFERRED_TOPICS = {
    'blueprint_qualification': 'RAIDQ-0005',
    'private_controls': 'RAIDQ-0006',
    'plectarium_family': 'RAIDQ-0007',
    'octon_family_migration': 'RAIDQ-0008',
    'standalone_standard_publication': 'RAIDQ-0009',
    'direct_cli_runtime': 'RAIDQ-0010',
}
DEFERRED_FIELDS = ('owner', 'blocker', 'trigger', 'risk', 'required_evidence',
                   'next_action', 'recovery')
CONTROL_COMMAND = ('env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py '
                   '--check --all --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}"')
CODE_COMMAND = ('env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py '
                '--check --scope code --all')
COORDINATOR_COMMAND = ('env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py '
                       '--root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}"')
SELECTED_CONTEXT = 'context "${TEXENDA_WORK_PACKAGE:?Select an ID from fresh ready output}"'
REFRESH_HELP = 'python3 -B .agent/scripts/refresh.py --help'

# Independent exact structural inventories from the accepted v2 baseline.
EXPECTED_SUPPLEMENTAL = [[".agent/extensions/texenda-coordination/","stable_project_hooks","adapter"],["project-dossier/transition/blueprint-adoption-crosswalk.json","adoption_transition","authoritative"],["project-dossier/conformance/findings.json","conformance_findings","authoritative"],["project-dossier/provenance/sources.json","adoption_provenance","authoritative"],["project-dossier/current-state/current.json","git_observation","generated_view"],["project-dossier/evidence/README.md","qualification_evidence","index"]]
EXPECTED_HIGH_ASSURANCE = [["SEC-0001","specs/texenda-handoff/04-security-governance-and-operations/","security_data","index"],["DAT-0001","specs/texenda-handoff/04-security-governance-and-operations/security-and-privacy.md","security_data","index"],["SUP-0001","specs/texenda-handoff/05-implementation/compatibility-manifest.template.json","supply_chain","index"],["EVA-0001",".agent/tests/","quality_rubric","adapter"],["CTX-0001","tooling/coordination/harness.py","context_routing","adapter"]]
EXPECTED_ARTIFACT_TYPES = [["DOS-0001","project-dossier/README.md"],["DOS-0002","project-dossier/AUTHORITY.md"],["DOS-0003","project-dossier/CANONICAL_SOURCE_MAP.md"],["DOS-0004","project-dossier/ARTIFACT_CATALOG.json"],["DOS-0005","project-dossier/MANIFEST.json"],["DOS-0006","project-dossier/VERSION.md"],["DOS-0007","project-dossier/SUPERSESSION.json"],["DOS-0008","project-dossier/machine-readable/path-authority.json"],["DOS-0009","project-dossier/CHECKSUMS.sha256"],["DEF-0001","project-dossier/canonical/executive-project-definition.md"],["REQ-0001","project-dossier/canonical/requirements-and-constraints.md"],["REQ-0002","project-dossier/machine-readable/requirements.json"],["ARC-0001","project-dossier/canonical/architecture-or-outcome-model.md"],["DEC-0001",".agent/decisions/README.md"],["GOV-0001","project-dossier/canonical/constraints-gates-and-readiness.md"],["CUR-0001","project-dossier/current-state/README.md"],["CNF-0001","project-dossier/conformance/README.md"],["CNF-0002","project-dossier/machine-readable/findings.json"],["PLN-0001","project-dossier/plans/README.md"],["PLN-0002","project-dossier/machine-readable/plan.json"],["REG-0001","project-dossier/registers/README.md"],["REG-0002","project-dossier/machine-readable/raidq.json"],["PRV-0001","project-dossier/provenance/README.md"],["PRV-0002","project-dossier/machine-readable/sources.json"],["VAL-0001","project-dossier/validation/README.md"],["VAL-0002","project-dossier/validation/QUALITY_GATES.json"],["VAL-0003","project-dossier/machine-readable/evidence-index.json"],["HOF-0001","project-dossier/handoff/START_HERE.md"],["HOF-0002","project-dossier/handoff/ADOPTION_CHECKLIST.md"],["GOV-0002","project-dossier/governance/README.md"],["MOD-0001","project-dossier/models/README.md"],["OPS-0001","project-dossier/operations/README.md"],["RES-0001","project-dossier/research/README.md"],["TRN-0001","project-dossier/transition/README.md"],["HIS-0001","project-dossier/history/README.md"]]


def load_contract(root=ROOT):
    text = stable_file_bytes(root / ADR, 'standalone operating ADR').decode()
    blocks = re.findall(r'<!-- texenda-standalone-operating-contract -->\s*```json\s*(.*?)\s*```',
                        text, flags=re.DOTALL)
    require(len(blocks) == 1, 'standalone ADR must own exactly one strict JSON contract')
    value = loads(blocks[0])
    # Deferred import avoids the validator/contract reader import cycle.
    import validate
    validate.validate_schema_instance(value, load_json(root / SCHEMA))
    return value


def validate_reference(root, ref):
    require(set(ref) == {'kind', 'path', 'scope', 'role'}, 'owner reference is not closed')
    require(ref['kind'] in ('repository', 'bound_ledger', 'local_role', 'local_binding', 'direct_git'),
            'unknown owner reference kind')
    require(all(isinstance(value, str) and value for value in ref.values()),
            'owner reference lacks a scope, role or locator')
    name = ref['path']
    reject_private_name(name, 'owner reference')
    require(not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts
            and not set(PurePosixPath(name).parts) & {'.git', '.texenda'}
            and name != '.texenda-location.json', 'owner reference escapes repository source')
    target = root / name
    no_symlink_components(target.absolute(), 'owner reference')
    require(target.exists(), 'owner reference is missing: ' + name)
    routes = {'bound_ledger': '.agent/project.json',
              'local_binding': 'tooling/coordination/schemas/state-location.schema.json',
              'direct_git': 'AGENTS.md'}
    if ref['kind'] in routes:
        require(name == routes[ref['kind']] and ref['role'] == 'location_or_observation_route',
                'local or direct observation reference falsely claims definition authority')
    return ref


def owner_reference_sets(root=ROOT):
    crosswalk = load_json(root / 'project-dossier/transition/blueprint-adoption-crosswalk.json')
    result = {}
    for row in crosswalk['ownership']:
        concern = row['concern_id']
        require(concern not in result, 'duplicate owner-reference concern')
        refs = row.get('owner_refs')
        require(isinstance(refs, list) and refs, 'missing owner-reference set: ' + concern)
        path = row['owner_by_epoch'][crosswalk['current_epoch']]
        kind, role = 'repository', 'definition'
        if path.startswith('/'):
            kind = 'bound_ledger' if concern in ('active_tasks', 'receipts', 'live_qualification') else 'local_role'
            path, role = ('.agent/project.json' if kind == 'bound_ledger' else ADR), 'location_or_observation_route'
        elif path == '.git/':
            kind, path, role = 'direct_git', 'AGENTS.md', 'location_or_observation_route'
        elif path == '.texenda/':
            kind, path, role = 'local_role', 'project-dossier/transition/blueprint-adoption-crosswalk.json', 'location_or_observation_route'
        elif path == '.texenda-location.json':
            kind, path, role = 'local_binding', 'tooling/coordination/schemas/state-location.schema.json', 'location_or_observation_route'
        if concern in ('product_semantics', 'canonical_architecture', 'domain_models',
                       'security_data', 'canonical_requirements'):
            path, role = 'specs/texenda-handoff/01-foundation/authority-register.json', 'sealed_topic_dispatch'
        expected = [{'kind': kind, 'path': path, 'scope': concern, 'role': role}]
        if concern in ('product_semantics', 'canonical_architecture', 'domain_models',
                       'supply_chain', 'canonical_requirements'):
            expected.append({'kind': 'repository',
                             'path': 'docs/decisions/ADR-0005-react-email-editor-reversible-default.md',
                             'scope': 'only_ADR_0005_named_editor_fields_WP10_VAL03_retained',
                             'role': 'scoped_amendment'})
        if concern == 'model_routing':
            expected.append({'kind': 'repository',
                             'path': 'docs/decisions/ADR-0001-quality-first-model-routing.md',
                             'scope': 'local_model_and_effort_overlay_only', 'role': 'scoped_amendment'})
        if concern == 'standalone_operation':
            for path, scope in (
                ('docs/decisions/ADR-0004-mapped-project-workspace.md', 'preservation_layout_and_recovery'),
                ('docs/decisions/ADR-0006-clean-ordinary-operating-contract.md', 'read_only_atime_and_history_routing'),
            ):
                expected.append({'kind': 'repository', 'path': path, 'scope': scope,
                                 'role': 'retained_scoped_decision'})
        require(refs == expected, 'owner-reference set is incomplete or changed scope: ' + concern)
        scopes = set()
        for ref in refs:
            validate_reference(root, ref)
            require(ref['scope'] not in scopes, 'overlapping duplicate scoped owner reference')
            scopes.add(ref['scope'])
        result[concern] = refs
    return result


def raw_raidq_record(raw, identifier):
    """Extract an existing indented record's exact bytes for immutable retention."""
    text = raw.decode() if isinstance(raw, bytes) else raw
    match = re.search(r'(?m)^    \{\n      "id": "' + re.escape(identifier) + r'",', text)
    require(match is not None, 'immutable RAIDQ record formatting or identity changed')
    start = match.start() + 4
    value, end = json.JSONDecoder().raw_decode(text, start)
    require(value['id'] == identifier, 'immutable RAIDQ record identity changed')
    return text[start:end].encode()


def resolve_deferral(root, reference, *, expected_record=None, raidq=None):
    """Resolve closed references into the sole RAIDQ owner's detail fields."""
    require(isinstance(reference, dict)
            and set(reference) == {'owner_path', 'record_id'},
            'deferral reference is not closed; editable detail overrides are forbidden')
    identifier = reference['record_id']
    require(reference['owner_path'] == RAIDQ and identifier in DEFERRED_TOPICS.values()
            and (expected_record is None or identifier == expected_record),
            'deferral reference disagrees with its sole owner record')
    source = load_json(root / RAIDQ) if raidq is None else raidq
    records = [row for row in source['items'] if row['id'] == identifier]
    require(len(records) == 1, 'deferral source record is missing or duplicated')
    row = records[0]
    if identifier == 'RAIDQ-0005':
        prior = loads(git('show', '7de052690bbf3e2879f375c2b2e17207c7ee5bfe:' + RAIDQ, root=root))
        require(row == next(item for item in prior['items'] if item['id'] == identifier),
                'exact retained Blueprint blocker changed')
        fields = {'owner': 'owner', 'blocker': 'blockers', 'trigger': 'retry_trigger',
                  'risk': 'risk', 'required_evidence': 'required_evidence',
                  'next_action': 'next_command_after_retry_trigger', 'recovery': 'recovery'}
    else:
        require(set(row) == {'id', 'type', 'status', 'statement', 'control', 'dependencies',
                             *DEFERRED_FIELDS}, 'deferral source record is not closed')
        require(row['status'] in ('gated', 'deferred')
                and row['type'] in ('issue', 'dependency'), 'deferral source falsely closed')
        require(isinstance(row['dependencies'], list)
                and all(isinstance(item, str) for item in row['dependencies'])
                and len(row['dependencies']) == len(set(row['dependencies'])),
                'deferral source dependencies are invalid')
        fields = {field: field for field in DEFERRED_FIELDS}
    details = {field: row[source_field] for field, source_field in fields.items()}
    require(all(details.values()), 'deferral owner lacks a required detail field')
    require(all(isinstance(details[field], str) and details[field].strip()
                for field in ('owner', 'trigger', 'risk', 'next_action', 'recovery')),
            'deferral owner detail has an invalid type')
    require((identifier == 'RAIDQ-0005' and isinstance(details['blocker'], list)
             and all(isinstance(item, str) and item.strip() for item in details['blocker']))
            or (isinstance(details['blocker'], str) and details['blocker'].strip()),
            'deferral owner lacks a typed blocker')
    require(isinstance(details['required_evidence'], list) and details['required_evidence']
            and all(isinstance(item, str) and item.strip() for item in details['required_evidence']),
            'deferral owner lacks exact required evidence')
    return details


def validate_operating(root=ROOT):
    contract = load_contract(root)
    roles = contract['path_roles']
    require(len(roles) == 19 and {row['id'] for row in roles}
            == {'ROLE-' + str(i).zfill(4) for i in range(1, 20)},
            'workspace path-role inventory is incomplete or duplicated')
    require(len({row['path'] for row in roles}) == len(roles), 'duplicate workspace role path')
    requirements = {'required', 'required_for_control', 'conditional',
                    'omitted_until_trigger', 'omitted_from_ordinary_dependencies'}
    for row in roles:
        require(row['requirement'] in requirements
                and row['anchor'] in ('repository', 'project_home', 'external'),
                'unclassified workspace role or anchor')
        require(not row['path'].startswith('/'), 'current role embeds a host-specific path')
        # Role locators are metadata. Never resolve project-home/private paths.
        no_symlink_components((root / row['owner']).absolute(), 'role owner')
        require((root / row['owner']).exists(), 'workspace role owner is missing')
    retention = load_json(root / RETENTION)
    require(retention['schema_version'] == 'texenda.workspace-retention.v1'
            and retention['authority'] == 'local_workspace_retention_metadata_only'
            and retention['owner_path'] == RETENTION
            and retention['decision'] == ADR and retention['deletion_authority'] is False
            and retention['private_content_or_size_access'] is False,
            'retention metadata gained deletion or private access authority')
    classes = retention['classes']
    require(len(classes) == 7 and {row['id'] for row in classes}
            == {'RET-' + str(i).zfill(4) for i in range(1, 8)},
            'retention classes are incomplete or duplicated')
    for row in classes:
        require(set(row) == {'id', 'classification', 'owner', 'retention',
                             'retirement_trigger', 'validation', 'recovery'}
                and all(isinstance(value, str) and value.strip() for value in row.values()),
                'retention class lacks owner, dependency trigger, validation or recovery')
    class_ids = {row['id'] for row in classes}
    require(all(row['retention_class'] in class_ids for row in roles),
            'unclassified role retention')
    by_role = {row['information_role']: row for row in roles}
    require(by_role['receipt_compatibility']['retention_class'] == 'RET-0004'
            and by_role['relocation_recovery']['retention_class'] == 'RET-0004'
            and retention['protected_receipt_retention_class'] == 'RET-0004',
            'receipt or recovery input classified disposable')
    from common import GENERATED_OUTPUT_PATHS
    require(len(GENERATED_OUTPUT_PATHS) == 11, 'generated retention scope changed')
    require(retention['generated_retention_class'] == 'RET-0005',
            'exact generated outputs lack their derived retention class')
    import sys
    workspace = root / 'tooling/workspace'
    if str(workspace) not in sys.path:
        sys.path.insert(0, str(workspace))
    import validate_contract as workspace_contract
    require(set(retention['protected_receipt_inputs']) == workspace_contract.COMPATIBILITY_INPUTS
            and len(retention['protected_receipt_inputs']) == 4,
            'retention lost exact receipt dependencies')
    refs = owner_reference_sets(root)
    catalog = load_json(root / 'project-dossier/ARTIFACT_CATALOG.json')
    for row in catalog['artifacts']:
        expected = {
            'direct_git_build_and_harness_evidence': [
                'git_observation', 'build_observation', 'active_tasks', 'receipts', 'live_qualification'],
            'external_live_state_and_direct_evidence': [
                'active_tasks', 'git_observation', 'build_observation'],
        }.get(row['owner_path'], [row['concern_id']])
        require(row.get('owner_refs') == [{'concern_id': concern} for concern in expected]
                and all(concern in refs for concern in expected),
                'catalog owner symbols are not navigable or complete')
    register = load_json(root / REMEDIATION)
    require(register['schema_version'] == 'texenda.workspace-remediation.v2'
            and register['authority'] == 'authoritative_remediation_dispositions_only_not_task_ledger'
            and register['owner_path'] == REMEDIATION,
            'remediation register became another task or permission owner')
    rows = register['items']
    require(len(rows) == 18 and {row['id'] for row in rows}
            == {'REM-' + str(i).zfill(4) for i in range(1, 19)},
            'remediation coverage is incomplete or duplicated')
    required = {'id', 'original_classification', 'affected_concern', 'current_evidence',
                'still_valid', 'practical_impact', 'dependencies', 'selected_disposition',
                'implementation_scope', 'validation_method', 'completion_evidence'}
    raidq = load_json(root / RAIDQ)
    issues = {row['id']: row for row in raidq['items']}
    require(len(issues) == len(raidq['items']), 'duplicate RAIDQ detail owner')
    for row in rows:
        require(required <= set(row) <= required | {'validity_scope', 'deferred_ref'}
                and type(row['still_valid']) is bool
                and row['current_evidence'] and row['completion_evidence']
                and all(row[key] for key in ('original_classification', 'affected_concern',
                                            'practical_impact', 'implementation_scope',
                                            'validation_method')),
                'remediation row lacks a required review disposition field')
        if row['selected_disposition'] == 'deferred':
            identifier = DEFERRED_TOPICS.get(row['affected_concern']['id'])
            require(identifier is not None and row['dependencies'] == [identifier],
                    'deferral disposition dependencies disagree with the sole detail owner')
            resolve_deferral(root, row.get('deferred_ref'), expected_record=identifier, raidq=raidq)
        else:
            require('deferred_ref' not in row, 'nondeferred disposition has a deferral override')
    topics = {row['affected_concern']['id']: row for row in rows}
    for topic in ('private_controls', 'blueprint_qualification', 'plectarium_family',
                  'octon_family_migration', 'standalone_standard_publication', 'direct_cli_runtime'):
        require(topics[topic]['selected_disposition'] == 'deferred'
                and topics[topic]['completion_evidence']['status'] == 'not_complete',
                'unqualified external/private/runtime concern falsely closed')
    require(topics['codex_registration']['still_valid'] is False
            and topics['codex_registration']['selected_disposition'] == 'already_resolved',
            'current app observation was replaced by stale historical registration')
    workspace_contract.validate_blueprint_maintenance(raidq)
    baseline = '7de052690bbf3e2879f375c2b2e17207c7ee5bfe'
    prior_raidq = loads(git('show', baseline + ':project-dossier/machine-readable/raidq.json', root=root))
    require(issues['RAIDQ-0005'] == next(row for row in prior_raidq['items']
                                       if row['id'] == 'RAIDQ-0005'),
            'exact retained Blueprint blocker changed')
    require(raw_raidq_record(stable_file_bytes(root / RAIDQ), 'RAIDQ-0005')
            == raw_raidq_record(git('show', baseline + ':' + RAIDQ, root=root, text=False),
                                'RAIDQ-0005'), 'retained RAIDQ-0005 bytes changed')
    supersession = load_json(root / 'project-dossier/SUPERSESSION.json')
    successor = next(row for row in supersession['records'] if row['id'] == 'SUP-0003')
    crosswalk_path = 'project-dossier/transition/blueprint-adoption-crosswalk.json'
    require(successor['prior_revision'] == baseline
            and successor['prior_path'] == successor['active_successor_path'] == crosswalk_path
            and successor['retention'] == 'exact_predecessor_in_preserved_Git_history'
            and successor['successor_schema'] == 'texenda.workspace-adoption-crosswalk.v2'
            and successor['prior_sha256'] == sha(git('show', baseline + ':' + crosswalk_path,
                                                    root=root, text=False)),
            'standalone compatible successor lost its exact v2 predecessor')
    detail_successor = next(row for row in supersession['records'] if row['id'] == 'SUP-0004')
    rejected = 'a0bdca755d1df6f7c1cf791d9d1f7641c2baa107'
    require(detail_successor['prior_revision'] == rejected
            and detail_successor['prior_path'] == detail_successor['active_successor_path'] == REMEDIATION
            and detail_successor['previous_schema'] == 'texenda.workspace-remediation.v1'
            and detail_successor['successor_schema'] == 'texenda.workspace-remediation.v2'
            and detail_successor['predecessor_status'] == 'rejected_candidate_not_accepted_or_integrated'
            and detail_successor['prior_sha256'] == sha(git('show', rejected + ':' + REMEDIATION,
                                                           root=root, text=False)),
            'closed deferral-reference successor lost its rejected predecessor')
    require(set(contract['deferred_records']) == set(DEFERRED_TOPICS.values())
            and len(contract['deferred_records']) == len(DEFERRED_TOPICS),
            'operating contract deferral references are incomplete')
    require(issues['RAIDQ-0007']['dependencies'] == []
            and issues['RAIDQ-0008']['dependencies'] == []
            and issues['RAIDQ-0009']['dependencies'] == [],
            'external family work or standalone publication acquired a Texenda dependency')
    for identifier, family in (('RAIDQ-0007', 'plectarium'), ('RAIDQ-0008', 'octon')):
        row = issues[identifier]
        require(family in row['owner'].lower() and 'texenda' not in row['owner'].lower()
                and 'own independent repositories' in row['statement']
                and 'advisory reference evidence only' in row['control'],
                'external family scope acquired a Texenda subject or owner')
        for field in ('blocker', 'trigger', 'risk', 'next_action', 'recovery'):
            require('texenda' not in row[field].lower(),
                    'external family action details acquired a Texenda migration scope')
    require(all(name in issues['RAIDQ-0008']['statement'] for name in ('octon', 'octonos', 'octon-mini'))
            and 'Blueprint qualification is separate from family layout authority'
            in issues['RAIDQ-0008']['control'],
            'Octon repository scope or separate qualification boundary is missing')
    return {'path_roles': len(roles), 'retention_classes': len(classes),
            'remediation_items': len(rows), 'owner_reference_sets': len(refs)}
