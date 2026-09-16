"""Repository-only readers for the scoped standalone operating contract."""
from __future__ import annotations

import re
import json
from pathlib import PurePosixPath

from common import (ROOT, GENERATED_OUTPUT_PATHS, canonical, load_json, loads, require,
                    stable_file_bytes, reject_private_name, no_symlink_components, git, sha)


ADR = 'docs/decisions/ADR-0007-standalone-workspace-operating-contract.md'
SCHEMA = '.agent/schemas/standalone-operating-contract.v1.schema.json'
RETENTION = 'project-dossier/registers/workspace-retention.json'
REMEDIATION = 'project-dossier/conformance/remediation-register.json'
RAIDQ = 'project-dossier/machine-readable/raidq.json'
FINDINGS = 'project-dossier/conformance/findings.json'
PLAN = 'project-dossier/machine-readable/plan.json'
SUPERSESSION = 'project-dossier/SUPERSESSION.json'
VERSION = 'project-dossier/VERSION.md'
DOSSIER_VERSION = '1.4.2-mapped-existing'
REVIEWED_CANDIDATE = '82da3f644ea82d6bc7531c1711c63b54eb3b9f5b'
REVIEW_RECORDING = '1ad95e9cdd0c8d2f0e09aa5f6c14a86e055e1a0c'
REMEDIATION_INTEGRATION = '087c0d65cf97c8f553b8915dd3cc93dddc46d4c4'
STANDALONE_REVIEW = 'docs/qualification/evidence/2026-09-15-standalone-reference-review.evidence.json'
STANDALONE_REVIEW_MD = 'docs/qualification/evidence/2026-09-15-standalone-reference-independent-review.md'
REVIEWED_REMEDIATIONS = {'REM-0001', 'REM-0002', 'REM-0003', 'REM-0004',
                       'REM-0007', 'REM-0008', 'REM-0014'}
# These are byte-identity expectations for the existing bounded statements, not
# evidence of approval. The dossier remains their information owner. Pin whole
# canonical records (including nested and unknown fields) so prose cannot extend
# the exact candidate review while leaving its checked revision IDs unchanged.
# A semantic successor needs exact independent review and updated expectations.
CLOSEOUT_SCOPE_PINS = {
    FINDINGS: ('findings', '73843393b29bc943089bbfc0ab57b109a533bc52aff68aa91189d1883dc84c14', {
        'FIND-0007': '81bdc6071b4b649181b03fead5f5844ba529c8e256cde63ce29a09432f780114',
    }),
    PLAN: ('items', '61dbeab58537da5ef1bec053be6f5b9116f152cfe032068ae0305413f9c9dec5', {
        'PLAN-0005': 'a5f39a6c69bd9328733e34ddf285017036d136ce192371a082280505bf75799d',
        'PLAN-0006': '66422cd3053aeb7e8d9cb8d554b4c6075e9736d6d9db81f291a1cd80f24df4cf',
    }),
    REMEDIATION: ('items', 'cd1cbbbafdae6cb96a24eecd0025a9dd3b24a2cc5a95c87166fbf68ceccf7254', {
        'REM-0001': 'd8c1721492103124f73fedf3ca4a9dbd6d29d13e6a67aadc408c19c033be4388',
        'REM-0002': 'f165255e83c097b56b57cef92dbdb8770a77baa1032e2df0bf4922157811b080',
        'REM-0003': '7302a79cbcb0962f470b49311c036779006f81eb7dab38f0a25ccdd0ab9ecd42',
        'REM-0004': 'c33a4781d77a2b9f8da57d38f2ac017c92c47306fb5ec35ec2ad921ea14e1b46',
        'REM-0007': '3089439d410cf1744d5898fd824193138dca631664b5ca1a2784b42cc04a4c01',
        'REM-0008': '008e49878435f126a596ea0fea65362abde0461a3113b70ac30489caa571a2c0',
        'REM-0014': '5a8bbae7a318dd3ab105fa943d448f730750fe90a3e19e8ea797383d08efcab0',
    }),
}
CLOSEOUT_VERSION_SHA256 = '9b63b48badbb86adff8e9133ed358e97f9640925725d6616741f2514299c5947'
CLOSEOUT_SUPERSESSION_METADATA_SHA256 = 'ba5a169539efab6f297a91f2e71df9a2f77dc157c96b90428c2772baf19849c9'
CLOSEOUT_SUCCESSOR_SHA256 = '1d63172c75d9542054429ab81e391967a16efc33cc4372e656d60eba6a53e344'
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


def validate_closeout(root=ROOT):
    """Bind current completion to immutable review and separate historical Git facts.

    This reads no current generated output, branch-name assumption, conversation,
    binding or ledger. It neither replays nor invents an integrated-head approval.
    """
    def historical(path, revision=REMEDIATION_INTEGRATION):
        return git('show', revision + ':' + path, root=root, text=False)

    def indexed(rows, label):
        result = {row['id']: row for row in rows}
        require(len(result) == len(rows), 'duplicate closeout ' + label)
        return result

    scoped_sources = {}
    for path, (records_key, metadata_digest, record_digests) in CLOSEOUT_SCOPE_PINS.items():
        source = load_json(root / path)
        metadata = {key: value for key, value in source.items() if key != records_key}
        require(sha(canonical(metadata)) == metadata_digest,
                'closeout source scope or authority metadata changed: ' + path)
        records = indexed(source[records_key], 'scope record ID')
        for identifier, digest in record_digests.items():
            require(identifier in records and sha(canonical(records[identifier])) == digest,
                    'closed closeout scope record changed: ' + identifier)
        scoped_sources[path] = source

    review_raw = historical(STANDALONE_REVIEW, REVIEW_RECORDING)
    review = loads(review_raw)
    require(review['kind'] == 'review' and review['task_id'] == 'OPS-WSM-0001'
            and review['candidate_revision'] == review['observed_revision'] == REVIEWED_CANDIDATE
            and review['checks'] and all(row['status'] == 'PASS' for row in review['checks']),
            'standalone completion lacks exact passing candidate review')
    review_hashes = {}
    for path in (STANDALONE_REVIEW, STANDALONE_REVIEW_MD):
        raw = historical(path, REVIEW_RECORDING)
        require(stable_file_bytes(root / path, 'retained standalone review') == raw,
                'immutable standalone review evidence changed')
        review_hashes[path] = sha(raw)
    require(all(row['evidence_path'] == STANDALONE_REVIEW_MD
                and row['sha256'] == review_hashes[STANDALONE_REVIEW_MD]
                for row in review['checks']), 'candidate review lost its exact bound report')
    for parent, revision, expected in (
        (REVIEWED_CANDIDATE, REVIEW_RECORDING, ['A\t' + path for path in review_hashes]),
        (REVIEW_RECORDING, REMEDIATION_INTEGRATION,
         ['M\t' + path for path in GENERATED_OUTPUT_PATHS]),
    ):
        require(git('show', '-s', '--format=%P', revision, root=root).strip() == parent,
                'reviewed integration parent chain changed')
        changed = git('diff', '--name-status', '--no-renames', parent, revision,
                      root=root).splitlines()
        require(sorted(changed) == sorted(expected),
                'post-candidate integration delta exceeds its declared evidence/generated scope')
    git('merge-base', '--is-ancestor', REMEDIATION_INTEGRATION, 'HEAD', root=root)

    plan = scoped_sources[PLAN]
    require(plan['authority'] == loads(historical(PLAN))['authority'],
            'completion record acquired task or permission authority')
    plans = indexed(plan['items'], 'plan ID')
    for identifier in ('PLAN-0005', 'PLAN-0006'):
        row = plans[identifier]
        require(row['status'] == 'completed' and row['completion_evidence'] == STANDALONE_REVIEW
                and row['reviewed_candidate_revision'] == REVIEWED_CANDIDATE
                and row['reviewed_candidate_tree']
                == git('rev-parse', REVIEWED_CANDIDATE + '^{tree}', root=root).strip()
                and row['observed_integration_revision'] == REMEDIATION_INTEGRATION,
                'reviewed integrated adoption plan regressed or lost exact completion evidence')
    source_revisions = re.findall(
        r'\| (?:Initial source commit/tree|First corrected source commit/tree|'
        r'Final scope-correction source commit/tree) \| `([0-9a-f]{40})`',
        historical(STANDALONE_REVIEW_MD, REVIEW_RECORDING).decode())
    require(len(source_revisions) == 3 and plans['PLAN-0005']['source_revisions'] == source_revisions,
            'source completion revisions differ from the immutable candidate review')
    integrated = plans['PLAN-0006']
    require(integrated['candidate_review_scope'] == 'exact_candidate_only'
            and integrated['review_evidence_revision'] == REVIEW_RECORDING
            and integrated['observed_integration_tree']
            == git('rev-parse', REMEDIATION_INTEGRATION + '^{tree}', root=root).strip()
            and integrated['integrated_audit_record'] == 'not_separately_committed',
            'integration record extends candidate approval or invents durable final-audit evidence')
    manifest_path = '.agent/generated/manifest.json'
    index_path = 'project-dossier/machine-readable/evidence-index.json'
    manifest = loads(historical(manifest_path))
    candidate_manifest = loads(historical(manifest_path, REVIEWED_CANDIDATE))
    evidence_index = loads(historical(index_path))
    generated_keys = ('generation_id', 'source_git_revision', 'source_git_tree',
                      'source_scope_sha256', 'evidence_scope_sha256')
    require(integrated['generated_evidence'] == {
        'revision': REMEDIATION_INTEGRATION, 'manifest_path': manifest_path,
        'evidence_index_path': index_path, **{key: manifest[key] for key in generated_keys}},
        'completion generated evidence differs from the exact integration revision')
    require(manifest['source_git_revision'] == REVIEW_RECORDING
            and manifest['source_git_tree']
            == git('rev-parse', REVIEW_RECORDING + '^{tree}', root=root).strip()
            and manifest['source_files'] == candidate_manifest['source_files']
            and manifest['source_scope_sha256'] == candidate_manifest['source_scope_sha256']
            == sha(canonical(manifest['source_files']))
            and manifest['evidence_scope_sha256'] == evidence_index['evidence_scope_sha256']
            == sha(canonical(manifest['evidence_files']))
            and evidence_index['evidence'] == manifest['evidence_files']
            and evidence_index['generation_id'] == manifest['generation_id'],
            'historical generated source/evidence identity does not preserve the reviewed source')
    generation_basis = {key: manifest[key] for key in (
        'source_scope_sha256', 'evidence_scope_sha256', 'ledger_sha256', 'receipt_count', 'receipt_tip')}
    require(manifest['generation_id'] == sha(canonical(generation_basis))
            and all({'path': path, 'sha256': digest} in evidence_index['evidence']
                    for path, digest in review_hashes.items()),
            'historical generation or review evidence index is inconsistent')

    integration_ref = {'owner_path': PLAN, 'record_id': 'PLAN-0006'}
    findings = indexed(scoped_sources[FINDINGS]['findings'], 'finding ID')
    finding = findings['FIND-0007']
    require(finding['classification'] == 'conformant'
            and finding['subject'] == 'Reviewed integrated standalone workspace remediation'
            and finding['disposition'] == 'operational_reviewed_source_at_recorded_integration'
            and finding['evidence'] == STANDALONE_REVIEW
            and finding['reviewed_candidate_revision'] == REVIEWED_CANDIDATE
            and finding['observed_integration_revision'] == REMEDIATION_INTEGRATION
            and finding['integration_record'] == integration_ref,
            'current standalone finding regressed or lost its bounded reviewed integration')
    current_rows = indexed(scoped_sources[REMEDIATION]['items'], 'remediation ID')
    prior_rows = indexed(loads(historical(REMEDIATION))['items'], 'historical remediation ID')
    require(set(current_rows) == set(prior_rows), 'closeout lost remediation coverage')
    stale = ('current source candidate', 'current_source_candidate',
             'acceptance still pending', 'acceptance remains outstanding',
             'candidate_requires_independent', 'fix_in_this_candidate',
             'currently calls the refresh writer')
    for identifier, row in current_rows.items():
        prior = prior_rows[identifier]
        if identifier not in REVIEWED_REMEDIATIONS:
            require(row == prior, 'closeout changed a retained, resolved, omitted or deferred disposition')
            continue
        completion = row['completion_evidence']
        require(row['still_valid'] is False
                and row['selected_disposition'] == 'completed_reviewed_and_integrated'
                and completion['status'] == 'reviewed_and_integrated'
                and completion['reference'] == STANDALONE_REVIEW
                and completion['reviewed_candidate_revision'] == REVIEWED_CANDIDATE
                and completion['observed_integration_revision'] == REMEDIATION_INTEGRATION
                and completion['integration_record'] == integration_ref,
                'implemented remediation regressed or lost its exact reviewed completion')
        require(len(row['current_evidence']) == 2
                and row['current_evidence'][0] == prior['current_evidence'][0],
                'closeout changed the exact historical baseline finding')
        observation = row['current_evidence'][1]
        require(observation['subject'] == 'reviewed_integrated_remediation'
                and observation['subject_revision'] == REMEDIATION_INTEGRATION
                and observation['reviewed_candidate_revision'] == REVIEWED_CANDIDATE
                and observation['review_reference'] == STANDALONE_REVIEW
                and row['practical_impact'] == observation['observation']
                and row['practical_impact'] != prior['practical_impact'],
                'implemented remediation still describes its historical defect as current')
        active = {key: value for key, value in row.items() if key != 'current_evidence'}
        active['current_evidence'] = [observation]
        normalized = ' '.join(json.dumps(active).lower().split())
        require(not any(phrase in normalized for phrase in stale),
                'stale candidate status remains in active remediation text')

    supersession = load_json(root / SUPERSESSION)
    supersession_metadata = {key: value for key, value in supersession.items() if key != 'records'}
    require(sha(canonical(supersession_metadata)) == CLOSEOUT_SUPERSESSION_METADATA_SHA256,
            'closeout supersession scope or authority metadata changed')
    prior_supersession = loads(historical(SUPERSESSION))
    require(supersession['current_version'] == DOSSIER_VERSION
            and len(supersession['records']) == 5
            and supersession['records'][:4] == prior_supersession['records'],
            'closeout supersession regressed or rewrote prior records')
    successor = supersession['records'][-1]
    require(sha(canonical(successor)) == CLOSEOUT_SUCCESSOR_SHA256,
            'closeout successor scope statement changed')
    require(successor['id'] == 'SUP-0005'
            and successor['prior_version'] == prior_supersession['current_version']
            == '1.4.1-mapped-existing'
            and successor['prior_revision'] == REMEDIATION_INTEGRATION
            and successor['prior_path'] == successor['active_successor_path'] == VERSION
            and successor['prior_sha256'] == sha(historical(VERSION))
            and successor['retention'] == 'exact_predecessor_in_preserved_Git_history'
            and successor['predecessor_status'] == 'reviewed_source_integrated_with_stale_candidate_metadata'
            and successor['successor_version'] == DOSSIER_VERSION
            and successor['affected_current_sources'] == [FINDINGS, PLAN, REMEDIATION],
            'closeout successor lost the exact integrated 1.4.1 predecessor')
    version_raw = stable_file_bytes(root / VERSION, 'current dossier version')
    require(sha(version_raw) == CLOSEOUT_VERSION_SHA256,
            'current dossier version scope statement changed')
    version = version_raw.decode()
    require(version.splitlines()[2] == 'Current operational contract version: `' + DOSSIER_VERSION + '`.'
            and 'Candidate contract version:' not in version,
            'current dossier version regressed to candidate or pending operation')
    return {'reviewed_candidate_revision': REVIEWED_CANDIDATE,
            'observed_integration_revision': REMEDIATION_INTEGRATION,
            'completed_remediations': len(REVIEWED_REMEDIATIONS),
            'integrated_audit_record': integrated['integrated_audit_record']}


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
    closeout = validate_closeout(root)
    return {'path_roles': len(roles), 'retention_classes': len(classes),
            'remediation_items': len(rows), 'owner_reference_sets': len(refs),
            'reviewed_integration_closeout': closeout}
