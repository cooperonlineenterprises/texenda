#!/usr/bin/env python3
"""Read-only traceability checks for ADR-0008; no task/gate/result authority."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from common import (ROOT, ValidationError, canonical, git, load_json,
                    no_symlink_components, require, sha, stable_file_bytes)

ADR = 'docs/decisions/ADR-0008-integrated-initial-product-and-effective-plan.md'
RECORD = 'docs/qualification/analysis/research-impact-dispositions.json'
RAIDQ = 'project-dossier/machine-readable/raidq.json'
BASELINE = 'docs/qualification/evidence/2026-09-17-initial-product-baseline.json'
SCHEMA = '.agent/schemas/research-dispositions.v1.schema.json'
BASE_REVISION = 'd3556d0718e558fa3a12cf628add58dd71a0008c'
DEFERRAL_IDS = {'RAIDQ-' + str(i).zfill(4) for i in range(11, 26)}
DISPOSITIONS = {
    'retained', 'resolved_by_owner_retention', 'rejected_semantic_replacement',
    'retain_pending_measured_trigger', 'superseded_by_final_owner_decision',
    'synthetic_contract_now_real_qualification_gated', 'incorporated_into_plan',
    'retained_with_explicit_acceptance', 'incorporated_into_existing_acceptance_route',
    'incorporated_into_plan_real_evidence_gated', 'retained_as_unqualified_external_lead',
    'deferred_with_precise_triggers', 'rejected_wholesale_adoption',
}


def plan_module(root):
    path = root / 'tooling/coordination/plan.py'
    no_symlink_components(path.absolute(), 'effective-plan reader')
    spec = importlib.util.spec_from_file_location('texenda_product_plan_reader', path)
    require(spec is not None and spec.loader is not None, 'effective-plan reader missing')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def source_path(root, name):
    require(isinstance(name, str) and name and not Path(name).is_absolute()
            and '..' not in name.split('/') and '\\' not in name
            and not any(p in name.split('/') for p in ('.git', '.texenda', 'private-inputs')),
            'product owner reference escapes source')
    path = root / name
    no_symlink_components(path.absolute(), 'product owner reference')
    require(path.is_file(), 'product owner reference missing: ' + name)
    return path


def validate_records(root=ROOT):
    root = Path(root)
    record = load_json(root / RECORD)
    import validate as facade
    facade.validate_schema_instance(record, load_json(root / SCHEMA))
    require(record['assessed_revision'] == BASE_REVISION and record['decision'] == ADR
            and record['owner_path'] == RECORD,
            'research dispositions changed subject or authority')
    require('no requirements' in record['authority']
            and 'permission' in record['authority'] and 'readiness' in record['authority'],
            'dispositions became a second product authority')
    rows = record['rows']
    require(len(rows) == 16 and {r['id'] for r in rows}
            == {'RI-' + str(i).zfill(4) for i in range(1, 17)},
            'research finding coverage missing or duplicated')
    module = plan_module(root)
    plan = module.load_plan(root)
    work = {w['id']: w for w in plan.catalog['work_packages']}
    criteria = {r['id'] for r in plan.contract['acceptance_extensions']}
    require(criteria == {'AC-IP' + str(i).zfill(2) for i in range(1, 19)},
            'initial acceptance extension incomplete')
    by_id = {r['id']: r for r in rows}
    for number in (5, 7):
        require(by_id['RI-' + str(number).zfill(4)]['selected_disposition']
                == 'superseded_by_final_owner_decision',
                'final owner decision was replaced by advisory recommendation')
    require('WP-27' in work['WP-29']['dependencies'],
            'external-first/deferred-embedded plan reintroduced')
    profiles = {p['id']: p for p in plan.profiles['profiles']}
    require({'WP-12', 'WP-27', 'WP-28', 'WP-29', 'WP-31', 'WP-32'}
            <= set(profiles['initial-synthetic']['requires_work_packages']),
            'initial integrated/native acquisition scope missing')
    require('AC-IP18' not in profiles['initial-production']['required_criteria']
            and 'AC-IP18' not in work['WP-17']['acceptance_ids'],
            'activation evidence was made a circular readiness prerequisite')
    require(not {'AC-M04', 'AC-M05', 'AC-M06', 'AC-M07', 'AC-M09'}
            & set(profiles['initial-production']['required_criteria'])
            and 'WP-20' in profiles['email-pilot']['requires_work_packages']
            and 'WP-15' in work['WP-12']['dependencies'],
            'reviewed acquisition/activation dependency correction regressed')
    require(profiles['assisted-workspace']['parents'] == ['initial-production']
            and profiles['external-agent']['parents'] == ['assisted-workspace'],
            'legacy interaction profile regained later rollout prerequisites')
    for row in rows:
        require(row['selected_disposition'] in DISPOSITIONS, 'unknown research disposition')
        require(set(row['work_packages']) <= set(work)
                and set(row['acceptance_refs']) <= criteria
                and set(row['deferred_refs']) <= DEFERRAL_IDS,
                'research disposition has unresolved traceability')
        require(ADR in row['authoritative_owners'], 'accepted amendment missing from disposition')
        for path in row['authoritative_owners']:
            source_path(root, path)
        require(row['completion_evidence']['contract'] == ADR
                and 'product evidence remains NOT_RUN' in row['completion_evidence']['scope'],
                'planning evidence overclaims product acceptance')
    baseline = load_json(root / BASELINE)
    require(baseline['head'] == BASE_REVISION
            and baseline['state_summary']['receipt_count'] == 13
            and baseline['maintenance']['product_implementation_authorized'] is False
            and baseline['maintenance']['external_effects_authorized'] is False,
            'baseline confused with current authorization/readiness')
    for source in record['source_packages']:
        name = source['location'].removeprefix('project-home:')
        preserved = baseline['protected'][name]
        require(preserved['files']['manifest.json'] == source['manifest_sha256']
                and preserved['count'] == source['files'],
                'research provenance differs from preserved baseline')
    raidq = load_json(root / RAIDQ)
    ids = [r['id'] for r in raidq['items']]
    require(len(ids) == len(set(ids)) and DEFERRAL_IDS <= set(ids),
            'product deferral coverage missing or duplicate')
    prior = json.loads(git('show', BASE_REVISION + ':' + RAIDQ, root=root))
    indexed = {r['id']: r for r in raidq['items']}
    require(all(indexed[r['id']] == r for r in prior['items']),
            'accepted prior RAIDQ record was rewritten')
    fields = {'id', 'type', 'status', 'statement', 'control', 'owner', 'blocker',
              'trigger', 'risk', 'required_evidence', 'next_action', 'recovery', 'dependencies'}
    gates = {g['id'] for g in load_json(
        root / 'specs/texenda-handoff/01-foundation/external-validation-gates.json')['gates']}
    for identifier in DEFERRAL_IDS:
        row = indexed[identifier]
        require(set(row) == fields and row['type'] == 'dependency'
                and row['status'] in ('gated', 'deferred'),
                'deferral malformed or falsely cleared')
        for key in ('statement', 'control', 'owner', 'blocker', 'trigger', 'risk',
                    'next_action', 'recovery'):
            require(isinstance(row[key], str) and row[key].strip(),
                    'deferral lacks ' + key)
        require(isinstance(row['required_evidence'], list) and row['required_evidence']
                and all(isinstance(x, str) and x for x in row['required_evidence']),
                'deferral lacks precise evidence')
        require(isinstance(row['dependencies'], list)
                and len(row['dependencies']) == len(set(row['dependencies']))
                and set(row['dependencies']) <= set(work) | gates | set(ids),
                'deferral dependency unresolved')
    require(set().union(*(set(r['deferred_refs']) for r in rows)) == DEFERRAL_IDS - {'RAIDQ-0024', 'RAIDQ-0025'},
            'review findings lost their precise deferral references')
    source_path(root, 'docs/implementation/initial-product.md')
    return {'status': 'PASS', 'scope': 'planning_traceability_only', 'findings': 16,
            'acceptance_extensions': 18, 'product_deferrals': len(DEFERRAL_IDS),
            'effective_plan_digest': plan.digest, 'product_acceptance': 'NOT_RUN',
            'external_gate_clearance': False, 'explicit_writes': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(validate_records(args.root), indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
