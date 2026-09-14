#!/usr/bin/env python3
"""Refresh Texenda's non-authoritative generated integrity/state views."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
from common import (ROOT, SOURCE_SCOPE_EXCLUSIONS, canonical, evidence_rows, git_identity,
                    ledger_facts, load_json, require, revision_source_rows, scope_digest, sha,
                    source_rows)
import validate as checker


OUTPUTS = (
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


def json_bytes(value):
    return json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False).encode() + b'\n'


def atomic_bytes(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.refresh-write-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def source_map(crosswalk, generation_id, generated_at):
    lines = [
        '# Canonical source map',
        '',
        'Generated, non-authoritative navigation. Documentation is not permission.',
        f'Generation: `{generation_id}` at `{generated_at}`.',
        '',
        '| Concern | Baseline owner | Facade owner | External-state owner |',
        '|---|---|---|---|',
    ]
    for row in crosswalk['ownership']:
        owners = row['owner_by_epoch']
        display = lambda value: f'`{value}`' if value is not None else 'none'
        lines.append(f"| `{row['concern_id']}` | {display(owners['baseline'])} | "
                     f"{display(owners['facade'])} | {display(owners['external_state'])} |")
    lines += ['', 'Source: [reviewed adoption crosswalk](transition/blueprint-adoption-crosswalk.json).', '']
    return '\n'.join(lines).encode()


def build(root=ROOT, state_root=None, *, generated_at=None, source_identity=None,
          prevalidate=True, allow_refresh_marker=False):
    # Validate adopted authorities and all non-generated sources before any write.
    if prevalidate:
        checker.validate(root, state_root, generated=False, run_all=False,
                         allow_refresh_marker=allow_refresh_marker)
    rows = source_rows(root)
    evidence = evidence_rows(root)
    ledger = ledger_facts(root, state_root)
    revision, tree = source_identity or git_identity(root)
    require(revision_source_rows(revision, root) == rows,
            'refresh requires every non-generated non-evidence source byte at the recorded Git revision')
    generated_at = generated_at or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    scope = scope_digest(rows)
    evidence_scope = scope_digest(evidence)
    transaction_basis = {
        'source_scope_sha256': scope,
        'evidence_scope_sha256': evidence_scope,
        'ledger_sha256': ledger['ledger_sha256'],
        'receipt_count': ledger['receipt_count'],
        'receipt_tip': ledger['receipt_tip'],
    }
    generation_id = sha(canonical(transaction_basis))
    ledger_observation = {
        'state_root': ledger['state_root'],
        'state_version': ledger['state_version'],
        'lease_count': ledger['lease_count'],
        'declared_budget_usd': ledger['declared_budget_usd'],
    }
    freshness = ('Recompute the complete declared source scope, separately indexed evidence, and '
                 'stable live-ledger snapshot. Any mismatch is stale; current full HEAD/tree are '
                 'reported separately because generated/evidence-only commits may follow this source revision.')
    manifest = {
        'schema_version': 'texenda.generated-integrity.v1',
        'generation_id': generation_id,
        'generation_id_derivation': 'sha256(canonical_json(source_scope_sha256,evidence_scope_sha256,ledger_sha256,receipt_count,receipt_tip))',
        'generated_at': generated_at,
        'authority': 'generated_non_authoritative',
        'source_git_revision': revision,
        'source_git_tree': tree,
        'source_scope_sha256': scope,
        'source_scope_exclusions': SOURCE_SCOPE_EXCLUSIONS,
        'source_files': rows,
        'evidence_scope_sha256': evidence_scope,
        'evidence_files': evidence,
        'ledger_sha256': ledger['ledger_sha256'],
        'receipt_count': ledger['receipt_count'],
        'receipt_tip': ledger['receipt_tip'],
        'roster_evidence_sha256': ledger['roster_evidence_sha256'],
        'ledger_observation': ledger_observation,
        'freshness_rule': freshness,
        'generated_output_validation': 'All eleven generated outputs are byte-reconstructed from validated inputs during check.',
        'limitations': [
            'SHA-256 establishes byte identity only, not authority, correctness, approval, or product readiness.',
            'Private-input content is excluded and was not opened, listed, copied, parsed, or hashed.',
            'This projection is not the live task, receipt, roster, routing, decision, evidence, or permission owner.',
        ],
    }
    current = {
        'schema_version': 'texenda.generated-current-state.v1',
        'generation_id': generation_id,
        'generated_at': generated_at,
        'authority': 'generated_non_authoritative_projection',
        'source_git_revision': revision,
        'source_git_tree': tree,
        'source_scope_sha256': scope,
        'source_scope_exclusions': SOURCE_SCOPE_EXCLUSIONS,
        'ledger_sha256': ledger['ledger_sha256'],
        'receipt_count': ledger['receipt_count'],
        'receipt_tip': ledger['receipt_tip'],
        'roster_evidence_sha256': ledger['roster_evidence_sha256'],
        'evidence_scope_sha256': evidence_scope,
        'freshness_rule': freshness,
        'ledger_observation': ledger_observation,
    }
    catalog = load_json(root / 'project-dossier/ARTIFACT_CATALOG.json')
    path_authority = {
        'schema_version': 'texenda.dossier-path-authority.generated.v1',
        'generation_id': generation_id,
        'generated_at': generated_at,
        'authority': 'generated_from_project-dossier/ARTIFACT_CATALOG.json',
        'source_sha256': sha((root / 'project-dossier/ARTIFACT_CATALOG.json').read_bytes()),
        'paths': [{key: row[key] for key in ('path', 'classification', 'owner_path', 'concern_id')}
                  for row in catalog['artifacts']],
    }
    findings_source = root / 'project-dossier/conformance/findings.json'
    findings = load_json(findings_source)
    findings_mirror = {
        'schema_version': 'texenda.dossier-findings.generated.v1',
        'generation_id': generation_id,
        'generated_at': generated_at,
        'authority': 'generated_from_project-dossier/conformance/findings.json',
        'source_sha256': sha(findings_source.read_bytes()),
        'findings': findings['findings'],
    }
    evidence_index = {
        'schema_version': 'texenda.dossier-evidence-index.generated.v1',
        'generation_id': generation_id,
        'generated_at': generated_at,
        'authority': 'generated_hash_index_only',
        'owner_path': 'docs/qualification/evidence/',
        'evidence_scope_sha256': evidence_scope,
        'evidence': evidence,
        'limitations': ['Indexing does not copy evidence authority or make a check current forever.'],
    }
    dossier_current = dict(current, schema_version='texenda.dossier-current-state.generated.v1')
    report = {
        'schema_version': 'texenda.generated-validation-report.v1',
        'generation_id': generation_id,
        'generated_at': generated_at,
        'authority': 'generated_point_in_time_evidence',
        'result': 'PASS',
        'checks': [
            {'id': 'strict_sources', 'status': 'PASS'},
            {'id': 'single_owner_map', 'status': 'PASS'},
            {'id': 'extension_confinement', 'status': 'PASS'},
            {'id': 'receipt_integrity', 'status': 'PASS'},
            {'id': 'evidence_hash_index', 'status': 'PASS'},
        ],
        'source_scope_sha256': scope,
        'ledger_sha256': ledger['ledger_sha256'],
        'limitations': manifest['limitations'],
    }
    resume = f"""# Resume Texenda mapped workspace work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `{generation_id}` at `{generated_at}`
- Source revision/tree: `{revision}` / `{tree}`
- Source-scope SHA-256: `{scope}`
- Live-ledger SHA-256: `{ledger['ledger_sha256']}`
- Receipt count/tip: `{ledger['receipt_count']}` / `{ledger['receipt_tip']}`
- Live task/receipt/roster authority: `{ledger['state_root']}/state.json`

Start with [`.agent/START_HERE.md`](../START_HERE.md). Re-run the read-only check;
if any digest is stale, run refresh only after the underlying authority is understood.
""".encode()
    current_readme = f"""# Current observed state

Generated, non-authoritative view from [`current.json`](current.json). It does not
define the target, grant permission, or mark a product/external gate passed.

Generation `{generation_id}` binds source revision `{revision}`, tree `{tree}`,
source scope `{scope}`, and live ledger `{ledger['ledger_sha256']}`. Freshness is
decided by the read-only facade check, not by this prose.
""".encode()
    handoff = f"""# Texenda handoff entry point

Generated navigation only; documentation is not permission or live state.

1. Read [root instructions](../../AGENTS.md) and [`.agent/START_HERE.md`](../../.agent/START_HERE.md).
2. Confirm generation `{generation_id}` with the [read-only validation registry](../validation/README.md).
3. Read [current observed state](../current-state/README.md), then the
   [transition owner](../transition/README.md) only when migration work is in scope.
4. Use the existing coordination ledger and templates; do not create dossier tasks or receipts.

Source revision/tree: `{revision}` / `{tree}`. Live ledger hash: `{ledger['ledger_sha256']}`.
""".encode()
    crosswalk = load_json(root / 'project-dossier/transition/blueprint-adoption-crosswalk.json')
    return {
        '.agent/generated/manifest.json': json_bytes(manifest),
        '.agent/generated/validation-report.json': json_bytes(report),
        '.agent/state/current.json': json_bytes(current),
        '.agent/state/RESUME.md': resume,
        'project-dossier/CANONICAL_SOURCE_MAP.md': source_map(crosswalk, generation_id, generated_at),
        'project-dossier/current-state/current.json': json_bytes(dossier_current),
        'project-dossier/current-state/README.md': current_readme,
        'project-dossier/handoff/START_HERE.md': handoff,
        'project-dossier/machine-readable/evidence-index.json': json_bytes(evidence_index),
        'project-dossier/machine-readable/findings.json': json_bytes(findings_mirror),
        'project-dossier/machine-readable/path-authority.json': json_bytes(path_authority),
    }


def refresh(root=ROOT, state_root=None, *, fail_after=None, recover_interrupted=False):
    outputs = build(root, state_root, allow_refresh_marker=recover_interrupted)
    marker = root / '.agent/generated/.refresh-in-progress'
    marker.parent.mkdir(parents=True, exist_ok=True)
    if marker.exists():
        if marker.is_symlink() or not recover_interrupted:
            raise checker.ValidationError('interrupted refresh marker present; use explicit verified recovery')
    else:
        if recover_interrupted:
            raise checker.ValidationError('no interrupted refresh marker exists to recover')
        descriptor = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, 'w') as stream:
            stream.write('incomplete generated-integrity transaction\n')
            stream.flush()
            os.fsync(stream.fileno())
    completed = 0
    try:
        for name in OUTPUTS:
            atomic_bytes(root / name, outputs[name])
            completed += 1
            if fail_after is not None and completed == fail_after:
                raise RuntimeError('synthetic interrupted refresh')
        marker.unlink()
        return {
            'status': 'REFRESHED',
            'outputs': len(outputs),
            'generation_id': load_json(root / '.agent/generated/manifest.json')['generation_id'],
            'next': 'python3 -B .agent/scripts/validate.py --check',
        }
    except BaseException:
        # Preserve the marker so check fails closed on any partial replacement.
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--refresh', action='store_true')
    mode.add_argument('--recover-interrupted', action='store_true')
    parser.add_argument('--state-root', type=Path)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(refresh(ROOT, args.state_root,
                                 recover_interrupted=args.recover_interrupted), indent=2))
        return 0
    except (checker.ValidationError, OSError, ValueError, KeyError, TypeError,
            __import__('subprocess').CalledProcessError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
