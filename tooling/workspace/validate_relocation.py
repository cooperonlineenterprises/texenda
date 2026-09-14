#!/usr/bin/env python3
"""Opt-in, read-only Phase-1 physical workspace audit; no moves or approval.

This local check deliberately requires --project-home and --expected-revision.
It is not part of the portable static check or clean-clone test requirements.
Private inputs are checked only for exact-path existence, ignore and tracking.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('workspace_contract',
                                             Path(__file__).with_name('validate_contract.py'))
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)
require, sha, canonical = contract.require, contract.sha, contract.canonical
BASE = 'b99f71fbaba0183fa2857016819fb410cabc1160'
BASE_TREE = '24fdd3f5c7e9b8b1a03c854210d2cc6427620477'
FRESH_BUNDLE_SHA = 'f94b0e81858197e5d0419cf7170650f889263602aa35b1d1e7e8710468064897'
CACHES = {
    'architecture-author': '0cfaa9af2c7cfbb13b01365d9f7cdd98d8084db1d8b3cbfae98544bf0a489c5c',
    'rejected-review': '794df95a2d33a88efaf56f841ea06d35a0a789058683eb61472340470df88e25',
    'final-review': 'd5cad3c55dcf0344bfd58dca405a862f3c9a36c68e70d7f78c8a590ca4d85574',
}
PRIVATE = '.texenda/private-inputs/kit/ohw/2026-09-14/subscribers.csv'


def no_symlink(path):
    path = Path(path)
    require(path.is_absolute() and '..' not in path.parts, 'absolute non-traversing path required')
    for part in (path, *path.parents):
        require(not part.is_symlink(), 'symlink path denied: ' + str(part))
    return path


def read_bytes(path):
    """The only content reader; deny the private boundary before opening."""
    path = no_symlink(path)
    require('private-inputs' not in path.parts and path.suffix.lower() != '.csv',
            'private content is outside the audit')
    require(path.is_file(), 'required file missing: ' + str(path))
    return path.read_bytes()


def tree_rows(directory):
    no_symlink(directory)
    require(directory.is_dir(), 'required directory missing: ' + str(directory))
    rows = []
    for path in sorted(directory.rglob('*')):
        no_symlink(path)
        if path.is_file():
            rows.append({'path': path.relative_to(directory).as_posix(),
                         'sha256': sha(read_bytes(path))})
        else:
            require(path.is_dir(), 'nonregular filesystem entry denied')
    return rows


def git(root, *args, accepted=(0,)):
    result = subprocess.run(['git', '--no-optional-locks', *args], cwd=root,
                            capture_output=True, text=True, check=False)
    require(result.returncode in accepted, 'Git check failed: ' + ' '.join(args))
    return result.stdout.strip()


def verify_source(source, baseline, manifest):
    expected = baseline['filesystem']['author_source_files']
    rows = tree_rows(source)
    require(rows == expected, 'source package file inventory or bytes changed')
    require(sorted(p.name for p in source.iterdir()) ==
            sorted(row['entry'] for row in manifest['source_package_moves']),
            'source top-level entries changed')
    for entry in manifest['source_package_moves']:
        path = source / entry['entry']
        if entry['type'] == 'file':
            require(sha(read_bytes(path)) == entry['sha256'], 'source file digest changed')
        else:
            subset = tree_rows(path)
            require(len(subset) == entry['file_count'] and
                    sha(canonical(subset)) == entry['tree_sha256'], 'source tree digest changed')
    return rows


def package_summary(path, expected):
    rows = [row for row in tree_rows(path)
            if '__pycache__' not in Path(row['path']).parts and not row['path'].endswith('.pyc')]
    path_nul = ''.join(row['path'] + '\0' + row['sha256'] + '\n' for row in rows).encode()
    summary = {'file_count': len(rows), 'manifest_sha256': sha(read_bytes(path / 'manifest.json')),
               'checksums_sha256': sha(read_bytes(path / 'SHA256SUMS')),
               'path_nul_sha256': sha(path_nul), 'canonical_array_sha256': sha(canonical(rows))}
    require(len(rows) == 86, 'package artifact count changed')
    require(all(summary[key] == expected[key] for key in expected if key in summary),
            'package fingerprint changed')
    return summary, {row['path']: row['sha256'] for row in rows}


def audit_state(repo, expected):
    """Reuse unchanged validation without the legacy status() writable lock open."""
    state_path = repo / '.texenda/state.json'
    raw = read_bytes(state_path)
    require(sha(raw) == expected['sha256'], 'state bytes changed from approved boundary')
    module_spec = importlib.util.spec_from_file_location('relocation_coordination',
                                                       ROOT / 'tooling/coordination/harness.py')
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    harness = module.Harness(repo, repo / 'specs/texenda-handoff')
    state = module.load_json(raw)
    harness._check(state)
    harness._validate_retained_evidence(state)
    qualified = [harness.qualified(state, row['profile_id']) for row in state['roster']]
    summary = {'path': str(state_path), 'sha256': sha(raw), 'version': state['version'],
               'receipt_count': len(state['events']), 'receipt_tip': state['events'][-1]['hash'],
               'roster_canonical_sha256': sha(canonical(state['roster'])),
               'qualified_profile_count': len(qualified),
               'lease_count': sum(task['lease'] is not None for task in state['tasks'].values()),
               'api_budget_usd': state['budget_usd'],
               'declared_api_allocations_usd': float(harness._declared_spend(state)),
               'cleared_external_gate_count': len(state['gates']),
               'earliest_profile_expiry': min(q['expires_at'] for q in qualified),
               'latest_profile_expiry': max(q['expires_at'] for q in qualified)}
    for key in summary.keys() & expected.keys():
        require(summary[key] == expected[key], 'live state baseline mismatch: ' + key)
    author = next(q for q in qualified if q['profile_id'] == 'gpt-6-astra-max')
    summary['author_qualification'] = {
        key: author[key] for key in ('profile_id', 'model_id', 'reasoning_effort',
                                    'runtime_id', 'client_version', 'billing_mode',
                                    'verified_at', 'expires_at', 'evidence')}
    require(read_bytes(state_path) == raw, 'state changed during read-only audit')
    return summary


def audit(home, expected_revision, allowed_worktrees):
    home = no_symlink(home)
    baseline = contract.loads(read_bytes(ROOT / contract.BASELINE))
    manifest = contract.loads(read_bytes(ROOT / contract.MANIFEST))
    require(str(home) == manifest['project_home'], 'project home differs from approved manifest')
    repo, source = home / 'repo', home / 'sources/handoff-1.1.0-20260914'
    require(not (home / '.git').exists() and not (home / 'AGENTS.md').exists(),
            'project home contains repository or instruction authority')
    result = subprocess.run(['git', '--no-optional-locks', 'rev-parse', '--show-toplevel'],
                            cwd=home, capture_output=True, check=False)
    require(result.returncode != 0, 'project home is within a Git repository')
    require(not Path(manifest['old_repository']).exists(), 'old checkout path remains')
    for name in ('repo', 'worktrees', 'local/agent-state', 'local/logs', 'local/artifacts',
                 'sources', 'archive/checkpoints'):
        require(no_symlink(home / name).is_dir(), 'workspace role directory missing: ' + name)
    notice = read_bytes(home / 'WORKSPACE.md')
    require(b'repo/AGENTS.md' in notice, 'workspace navigation does not route to repository')
    require(no_symlink(repo / '.git').is_dir(), 'canonical checkout lacks ordinary Git directory')
    revision, tree = git(repo, 'rev-parse', 'HEAD', 'HEAD^{tree}').splitlines()
    require(revision == expected_revision, 'canonical revision changed')
    require(git(repo, 'branch', '--show-current') == 'main', 'canonical checkout is not main')
    require(not git(repo, 'status', '--porcelain=v1'), 'canonical checkout is dirty')
    require(git(repo, 'remote', 'get-url', 'origin') == baseline['subject']['remote'], 'remote changed')
    require(git(repo, 'remote', 'get-url', '--push', 'origin') == baseline['subject']['remote'],
            'push remote changed')
    require(not git(repo, 'ls-files', '.github/workflows'), 'tracked hosted workflow appeared')
    worktrees = [line.removeprefix('worktree ') for line in
                 git(repo, 'worktree', 'list', '--porcelain').splitlines()
                 if line.startswith('worktree ')]
    require(set(worktrees) == {str(repo), *allowed_worktrees}, 'undeclared linked worktree')
    for worktree in worktrees:
        require(no_symlink(Path(worktree)).is_dir(), 'invalid linked worktree path')
        if worktree != str(repo):
            require(Path(worktree).parent == home / 'worktrees', 'worktree outside workspace')
            require(not (Path(worktree) / '.texenda/state.json').exists(), 'second active state')
    source_rows = verify_source(source, baseline, manifest)
    source_summary, source_hashes = package_summary(source, baseline['packages']['source'])
    sealed_summary, sealed_hashes = package_summary(repo / 'specs/texenda-handoff',
                                                    baseline['packages']['sealed'])
    differences = [{'path': name, 'source_sha256': source_hashes[name],
                    'sealed_sha256': sealed_hashes[name]} for name in sorted(source_hashes)
                   if source_hashes[name] != sealed_hashes[name]]
    require(differences == baseline['packages']['differing_paths'], 'package divergence changed')
    archive = home / 'archive/checkpoints/phase-0-20260914'
    require(not Path(manifest['checkpoint_archive']['source']).exists(), 'old checkpoint path remains')
    expected_checkpoints = {row['name']: row['sha256']
                            for row in manifest['checkpoint_archive']['content_hashes']}
    expected_checkpoints['texenda-git-b99f71f.bundle'] = FRESH_BUNDLE_SHA
    expected_checkpoints.update({'reviewer-cache-artifacts/' + label + '/harness.cpython-313.pyc': value
                                 for label, value in CACHES.items()})
    checkpoints = tree_rows(archive)
    require({row['path']: row['sha256'] for row in checkpoints} == expected_checkpoints,
            'checkpoint inventory or bytes changed')
    for name in ('texenda-git-36b74e9.bundle', 'texenda-git-b99f71f.bundle'):
        git(repo, 'bundle', 'verify', str(archive / name))
    bundle_heads = git(repo, 'bundle', 'list-heads', str(archive / 'texenda-git-b99f71f.bundle'))
    require(BASE + ' refs/heads/main' in bundle_heads.splitlines(), 'checkpoint main missing')
    bundled_refs, archived_heads = {}, {}
    for line in bundle_heads.splitlines():
        value, ref = line.split(' ', 1)
        if ref == 'HEAD':
            continue
        if ref.startswith('refs/'):
            bundled_refs[ref] = value
        else:
            require(contract.re.fullmatch(r'worktrees/[^/]+/HEAD', ref) is not None,
                    'unrecognized bundle pseudo-ref')
            git(repo, 'cat-file', '-e', value + '^{commit}')
            # Detached review evidence need not be integrated into main. Its
            # commit is retained locally and explicitly by the verified bundle.
            archived_heads[ref] = value
    current_refs = {line.split(' ', 1)[1]: line.split(' ', 1)[0]
                    for line in git(repo, 'show-ref').splitlines()}
    for ref, value in bundled_refs.items():
        require(ref in current_refs, 'preserved Git ref missing: ' + ref)
        if ref == 'refs/heads/main':
            git(repo, 'merge-base', '--is-ancestor', value, current_refs[ref])
        else:
            require(current_refs[ref] == value, 'preserved Git ref changed: ' + ref)
    assigned_refs = {git(Path(path), 'symbolic-ref', 'HEAD') for path in allowed_worktrees}
    require(set(current_refs) - set(bundled_refs) <= assigned_refs, 'undeclared new Git ref')
    journal_path = home / 'local/logs/workspace-relocation/phase-1-journal.json'
    journal_raw = read_bytes(journal_path)
    journal = contract.loads(journal_raw)
    actions = ['source-' + row['entry'] for row in manifest['source_package_moves']]
    actions += ['repository', 'phase-0-checkpoints']
    require(journal['status'] == 'relocated' and journal['approved_revision'] == BASE and
            journal['approved_tree'] == BASE_TREE and journal['state_sha256'] == baseline['state']['sha256']
            and journal['receipt_tip'] == baseline['state']['receipt_tip'] and
            journal['private_input_contents_accessed'] is False and
            journal['workspace_navigation_created'] is True and
            journal['actions'] == [{'id': name, 'status': 'completed'} for name in actions],
            'journal does not establish the approved completed move list')
    for pending in ('local/agent-state/texenda', 'local/private-inputs', 'repo/.texenda-location.json'):
        require(not (home / pending).exists() and not (home / pending).is_symlink(),
                'Phase-4 cutover unexpectedly started')
    state = audit_state(repo, baseline['state'])
    private = no_symlink(repo / PRIVATE)
    require(private.is_file(), 'expected private input missing')
    ignored = git(repo, 'check-ignore', '-v', '--', PRIVATE)
    require(ignored == '.gitignore:1:.texenda/\t' + PRIVATE, 'private input ignore rule changed')
    require(not git(repo, 'ls-files', '--', PRIVATE), 'private input tracked')
    require(not git(repo, 'status', '--porcelain=v1', '--', PRIVATE), 'private input status changed')
    disk = os.statvfs(home)
    return {'observed_at': datetime.now(timezone.utc).isoformat(),
            'outcome': 'pass', 'scope': 'Phase-1 physical state at observation time only',
            'project_home': str(home), 'project_home_git_repository': False,
            'workspace_notice_sha256': sha(notice), 'free_bytes': disk.f_bavail * disk.f_frsize,
            'git': {'revision': revision, 'tree': tree, 'remote': baseline['subject']['remote'],
                    'clean': True, 'linked_worktrees': worktrees,
                    'all_refs_sha256': sha(git(repo, 'show-ref').encode()),
                    'fresh_bundle_ref_count': len(bundle_heads.splitlines()),
                    'preserved_bundled_refs': len(bundled_refs),
                    'archived_worktree_heads': archived_heads},
            'source': dict(source_summary, preserved_regular_files=len(source_rows),
                           all_files_canonical_sha256=sha(canonical(source_rows)), top_level_entries=16),
            'sealed': sealed_summary, 'differing_paths': differences,
            'checkpoints': checkpoints, 'journal_sha256': sha(journal_raw), 'completed_moves': len(actions),
            'state': state, 'private_input': {'path': str(private), 'exists': True,
                'ignored': True, 'tracked': False, 'content_accessed': False, 'content_hashed': False,
                'content_parsed': False, 'content_copied': False, 'content_logged': False},
            'approval': False, 'moves_executed': False, 'network_requests': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-home', type=Path, required=True)
    parser.add_argument('--expected-revision', required=True)
    parser.add_argument('--allowed-worktree', action='append', default=[])
    args = parser.parse_args()
    # Direct invocation also prevents imports from creating bytecode.
    sys.dont_write_bytecode = True
    try:
        report = audit(args.project_home, args.expected_revision, args.allowed_worktree)
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'outcome': 'fail', 'reason': str(exc), 'approval': False}))
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
