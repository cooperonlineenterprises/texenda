"""Shared read-only integrity primitives for the mapped Texenda facade."""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile


ROOT = Path(__file__).resolve().parents[2]
GENERATED_PATHS = (
    '.agent/generated/',
    '.agent/state/current.json',
    '.agent/state/RESUME.md',
    'project-dossier/CANONICAL_SOURCE_MAP.md',
    'project-dossier/current-state/',
    'project-dossier/handoff/',
    'project-dossier/machine-readable/evidence-index.json',
    'project-dossier/machine-readable/findings.json',
    'project-dossier/machine-readable/path-authority.json',
)
EVIDENCE_PREFIX = 'docs/qualification/evidence/'
SOURCE_SCOPE_EXCLUSIONS = [
    {
        'path': '.agent/generated/**',
        'reason': 'refresh-only generated integrity outputs; containing them would create a digest cycle',
    },
    {
        'path': '.agent/state/current.json and .agent/state/RESUME.md',
        'reason': 'refresh-only generated state projections',
    },
    {
        'path': 'project-dossier generated views',
        'reason': 'refresh-only source map, current-state, handoff, and machine-readable mirrors',
    },
    {
        'path': 'docs/qualification/evidence/**',
        'reason': 'immutable validation/review evidence may be added after source validation and is hash-indexed separately',
    },
    {
        'path': '.git/** and ignored local state/private/cache paths',
        'reason': 'Git internals and nontracked operational/private material are outside the tracked source scope',
    },
]


class ValidationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def loads(raw):
    def reject(value):
        raise ValidationError('nonfinite JSON value: ' + value)
    return json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject)


def load_json(path):
    require(path.is_file() and not path.is_symlink(), 'missing/nonregular JSON: ' + str(path))
    return loads(path.read_bytes())


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def valid_sha(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def git(*arguments, root=ROOT, text=True):
    result = subprocess.run(['git', '--no-optional-locks', *arguments], cwd=root,
                            capture_output=True, check=True)
    return result.stdout.decode() if text else result.stdout


def candidate_paths(root=ROOT):
    raw = git('ls-files', '--cached', '--others', '--exclude-standard', '-z', root=root)
    return sorted(path for path in raw.split('\0') if path)


def is_generated(path):
    return any(path == prefix or path.startswith(prefix)
               for prefix in GENERATED_PATHS)


def source_rows(root=ROOT):
    rows = []
    for name in candidate_paths(root):
        if is_generated(name) or name.startswith(EVIDENCE_PREFIX):
            continue
        parts = PurePosixPath(name).parts
        require('.texenda' not in parts and 'private-inputs' not in parts
                and not name.lower().endswith('.csv'),
                'private/local input entered source fingerprint: ' + name)
        path = root / name
        require(path.is_file() and not path.is_symlink(), 'source path is not a regular file: ' + name)
        rows.append({'path': name, 'sha256': sha(path.read_bytes())})
    return rows


def revision_source_rows(revision, root=ROOT):
    archive = subprocess.run(['git', '--no-optional-locks', 'archive', '--format=tar', revision],
                             cwd=root, capture_output=True, check=True).stdout
    rows = []
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as stream:
        for member in sorted(stream.getmembers(), key=lambda item: item.name):
            name = member.name.rstrip('/')
            if not name or member.isdir() or is_generated(name) or name.startswith(EVIDENCE_PREFIX):
                continue
            require(member.isfile(), 'recorded source revision contains a non-file path: ' + name)
            extracted = stream.extractfile(member)
            require(extracted is not None, 'cannot read recorded source path: ' + name)
            rows.append({'path': name, 'sha256': sha(extracted.read())})
    return rows


def evidence_rows(root=ROOT):
    names = git('ls-files', '-z', EVIDENCE_PREFIX, root=root).split('\0')
    rows = []
    for name in sorted(filter(None, names)):
        path = root / name
        require(path.is_file() and not path.is_symlink(), 'evidence path is not regular: ' + name)
        require('private-inputs' not in PurePosixPath(name).parts and not name.lower().endswith('.csv'),
                'private input entered evidence index')
        rows.append({'path': name, 'sha256': sha(path.read_bytes())})
    return rows


def stable_bytes(path):
    require(path.is_file() and not path.is_symlink(), 'state file missing or symlinked')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)

    def once():
        descriptor = os.open(path, flags)
        try:
            before = os.fstat(descriptor)
            chunks = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
                    before.st_ctime_ns)
        require(identity == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                             after.st_ctime_ns), 'state changed during read')
        return b''.join(chunks), identity

    first, second = once(), once()
    require(first == second, 'state changed or was replaced during read')
    return first[0]


def check_receipts(state):
    events = state.get('events')
    require(isinstance(events, list) and events, 'state must retain a receipt chain')
    previous = '0' * 64
    for sequence, event in enumerate(events, 1):
        require(isinstance(event, dict), 'receipt must be an object')
        body = {key: value for key, value in event.items() if key != 'hash'}
        require(event.get('sequence') == sequence and event.get('previous_hash') == previous
                and sha(canonical(body)) == event.get('hash'), 'receipt chain corrupt')
        previous = event['hash']
    state_body = {key: value for key, value in state.items() if key != 'events'}
    require(events[-1].get('state_digest') == sha(canonical(state_body)),
            'state differs from last receipt')


def binding(root=ROOT):
    path = root / '.texenda-location.json'
    if not path.exists():
        return None
    value = load_json(path)
    require(set(value) == {'schema_version', 'migration_id', 'repository_root', 'state_root',
                           'status', 'baseline'}, 'state binding is not closed')
    require(value['schema_version'] == 'texenda.state-location.v1', 'unknown state binding schema')
    require(value['status'] in ('moving', 'active'), 'invalid state binding status')
    require(Path(value['repository_root']) == root.resolve(), 'state binding repository mismatch')
    require(Path(value['state_root']) == root.resolve().parent / 'local/agent-state/texenda',
            'state binding differs from the frozen workspace root')
    require(set(value['baseline']) == {'state_sha256', 'receipt_count', 'receipt_tip'}
            and valid_sha(value['baseline']['state_sha256'])
            and type(value['baseline']['receipt_count']) is int
            and value['baseline']['receipt_count'] > 0
            and valid_sha(value['baseline']['receipt_tip']), 'state binding baseline is invalid')
    return value


def ledger_facts(root=ROOT, state_root=None, fallback_state_root=None):
    location = binding(root)
    if location and location['status'] != 'active':
        raise ValidationError('state relocation is moving')
    if state_root is not None:
        selected = Path(state_root)
        require(selected.is_absolute() and '..' not in selected.parts,
                'state root must be absolute and traversal-free')
        selected = selected.resolve(strict=True)
        require(selected.is_dir() and not selected.is_symlink(), 'state root must be a real directory')
    elif location:
        raise ValidationError('active binding requires explicit --state-root')
    elif fallback_state_root is not None:
        selected = Path(fallback_state_root)
        require(selected.is_absolute(), 'recorded ledger root is not absolute')
        selected = selected.resolve(strict=True)
    else:
        selected = root / '.texenda'
    if location:
        require(selected == Path(location['state_root']), 'state root does not match active binding')
        require(not (root / '.texenda/state.json').exists()
                and not (root / '.texenda/state.lock').exists(), 'competing default state remains')
    raw = stable_bytes(selected / 'state.json')
    state = loads(raw)
    check_receipts(state)
    return {
        'state_root': str(selected),
        'ledger_sha256': sha(raw),
        'receipt_count': len(state['events']),
        'receipt_tip': state['events'][-1]['hash'],
        'roster_evidence_sha256': sha(canonical(state.get('roster', []))),
        'lease_count': sum(task.get('lease') is not None for task in state.get('tasks', {}).values()),
        'declared_budget_usd': state.get('budget_usd'),
        'state_version': state.get('version'),
    }


def git_identity(root=ROOT):
    revision = git('rev-parse', 'HEAD', root=root).strip()
    tree = git('rev-parse', 'HEAD^{tree}', root=root).strip()
    require(re.fullmatch('[0-9a-f]{40}', revision) is not None, 'invalid Git revision')
    require(re.fullmatch('[0-9a-f]{40}', tree) is not None, 'invalid Git tree')
    return revision, tree


def scope_digest(rows):
    return sha(canonical(rows))
