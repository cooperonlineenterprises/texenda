"""Shared read-only integrity primitives for the mapped Texenda facade."""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tarfile


ROOT = Path(__file__).resolve().parents[2]
GENERATED_OUTPUT_PATHS = (
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
EVIDENCE_PREFIX = 'docs/qualification/evidence/'
SOURCE_SCOPE_EXCLUSIONS = [
    {'path': path, 'reason': 'exact refresh-only generated output; inclusion would create a digest cycle'}
    for path in GENERATED_OUTPUT_PATHS
] + [
    {
        'path': 'docs/qualification/evidence/**',
        'reason': 'immutable validation/review evidence may be added after source validation and is hash-indexed separately',
    },
    {
        'path': '.git/** and ignored local state/private/cache paths',
        'reason': 'Git internals and nontracked operational/private material are outside the tracked source scope',
    },
]
MIGRATION_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')
STATE_TRANSACTION_PENDING = '.state-write-transaction.json'


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
    return loads(stable_file_bytes(path, 'JSON path'))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def valid_sha(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def reject_private_name(name, label='path'):
    require(isinstance(name, str) and name, label + ' must be a nonempty string')
    parts = PurePosixPath(name).parts
    require('private-inputs' not in parts and not name.lower().endswith('.csv'),
            label + ' is private/CSV and cannot enter a content-read scope')


def no_symlink_components(path, label, *, allow_missing_leaf=False):
    """Reject direct and ancestor symlink aliases before any resolution or read."""
    candidate = Path(path)
    require(candidate.is_absolute(), label + ' must be absolute')
    require('..' not in candidate.parts, label + ' traversal is forbidden')
    current = Path(candidate.anchor)
    parts = candidate.parts[1:]
    for index, part in enumerate(parts):
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            require(allow_missing_leaf and index == len(parts) - 1,
                    label + ' has a missing parent or target')
            return current
        require(not stat.S_ISLNK(mode), label + ' contains a symlink alias')
    return candidate


def resolved_directory(path, label):
    candidate = no_symlink_components(Path(path), label)
    require(candidate.is_dir(), label + ' must be a directory')
    resolved = candidate.resolve(strict=True)
    require(resolved == candidate, label + ' must use its canonical absolute path')
    return resolved


def state_transaction_blockers(state_root):
    root = Path(state_root)
    if not root.exists() and not root.is_symlink():
        return []
    root = resolved_directory(root, 'state transaction root')
    flags = os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(root, flags)
    try:
        opened = os.fstat(descriptor)
        blockers = []
        for name in os.listdir(descriptor):
            if name.startswith('.state-write-'):
                blockers.append(name)
        current = root.lstat()
        require((opened.st_dev, opened.st_ino) == (current.st_dev, current.st_ino),
                'state transaction root changed during scan')
        return sorted(blockers)
    finally:
        os.close(descriptor)


def git(*arguments, root=ROOT, text=True):
    result = subprocess.run(['git', '--no-optional-locks', *arguments], cwd=root,
                            capture_output=True, check=True)
    return result.stdout.decode() if text else result.stdout


def candidate_paths(root=ROOT):
    raw = git('ls-files', '--cached', '--others', '--exclude-standard', '-z', root=root)
    return sorted(path for path in raw.split('\0') if path)


def is_generated(path):
    return path in GENERATED_OUTPUT_PATHS


def source_rows(root=ROOT):
    rows = []
    inventory = candidate_paths(root)
    for name in inventory:
        if is_generated(name) or name.startswith(EVIDENCE_PREFIX):
            continue
        parts = PurePosixPath(name).parts
        reject_private_name(name, 'source path')
        require('.texenda' not in parts,
                'private/local input entered source fingerprint: ' + name)
        path = root / name
        no_symlink_components(path.absolute(), 'source path')
        require(path.is_file(), 'source path is not a regular file: ' + name)
        rows.append({'path': name, 'sha256': sha(stable_file_bytes(path, 'source path'))})
    require(candidate_paths(root) == inventory, 'candidate path inventory changed during source scan')
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
        reject_private_name(name, 'evidence path')
        path = root / name
        no_symlink_components(path.absolute(), 'evidence path')
        require(path.is_file(), 'evidence path is not regular: ' + name)
        rows.append({'path': name, 'sha256': sha(stable_file_bytes(path, 'evidence path'))})
    require(git('ls-files', '-z', EVIDENCE_PREFIX, root=root).split('\0') == names,
            'evidence path inventory changed during scan')
    return rows


def stable_file_bytes(path, label='file'):
    path = no_symlink_components(Path(path).absolute(), label)
    require(path.is_file(), label + ' is missing or not regular')
    flags = (os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
             | getattr(os, 'O_NONBLOCK', 0))

    def once():
        try:
            descriptor = os.open(path, flags)
        except OSError as exc:
            raise ValidationError(label + ' cannot be opened as a regular file') from exc
        try:
            before = os.fstat(descriptor)
            require(stat.S_ISREG(before.st_mode),
                    label + ' must be a regular non-symlink file')
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
                             after.st_ctime_ns), label + ' changed during read')
        current = path.lstat()
        require((after.st_dev, after.st_ino) == (current.st_dev, current.st_ino)
                and stat.S_ISREG(current.st_mode), label + ' changed after safe open')
        return b''.join(chunks), identity

    first, second = once(), once()
    require(first == second, label + ' changed or was replaced during read')
    return first[0]


def stable_bytes(path):
    return stable_file_bytes(path, 'state file')


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
    if not path.exists() and not path.is_symlink():
        return None
    value = loads(stable_file_bytes(path, 'state binding'))
    require(set(value) == {'schema_version', 'migration_id', 'repository_root', 'state_root',
                           'status', 'baseline'}, 'state binding is not closed')
    require(value['schema_version'] == 'texenda.state-location.v1', 'unknown state binding schema')
    require(isinstance(value['migration_id'], str) and MIGRATION_ID.fullmatch(value['migration_id']),
            'unsafe state binding migration_id')
    recovery = root.resolve().parent / 'local/logs/workspace-relocation'
    if recovery.exists() or recovery.is_symlink():
        recovery = resolved_directory(recovery, 'state activation recovery directory')
        flags = (os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0)
                 | getattr(os, 'O_NOFOLLOW', 0))
        recovery_fd = os.open(recovery, flags)
        try:
            opened = os.fstat(recovery_fd)
            pending = [name for name in os.listdir(recovery_fd)
                       if name.endswith('.activation-transaction.json')]
            current = recovery.lstat()
            require((opened.st_dev, opened.st_ino) == (current.st_dev, current.st_ino),
                    'state activation recovery directory changed during scan')
        finally:
            os.close(recovery_fd)
    else:
        pending = []
    require(not pending, 'state activation transaction is pending recovery')
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


def control_context(root=ROOT, state_root=None):
    """Require the explicit canonical control binding before any ledger read."""
    require(state_root is not None, 'control scope requires explicit --state-root')
    repository = resolved_directory(Path(root).absolute(), 'control repository')
    require(repository.name == 'repo', 'control scope requires the canonical repo directory')
    marker = repository / '.git'
    no_symlink_components(marker, 'canonical Git directory')
    require(marker.is_dir(), 'control scope rejects linked worktrees; use canonical repo')
    require(git('rev-parse', '--show-toplevel', root=repository).strip() == str(repository),
            'control repository differs from its Git root')
    location = binding(repository)
    require(location is not None, 'control scope requires the canonical active binding')
    require(location['status'] == 'active', 'state relocation is moving')
    requested = Path(state_root)
    require(requested.is_absolute() and '..' not in requested.parts,
            'state root must be absolute and traversal-free')
    selected = resolved_directory(requested, 'control state root')
    require(str(selected) == location['state_root'], 'state root does not match active binding')
    require(not (repository / '.texenda/state.json').exists()
            and not (repository / '.texenda/state.lock').exists(),
            'competing default state remains')
    require(not state_transaction_blockers(selected),
            'state-write transaction is pending explicit recovery')
    return {'repository_root': str(repository), 'project_home': str(repository.parent),
            'state_root': str(selected), 'scope': 'control'}


def ledger_facts(root=ROOT, state_root=None, fallback_state_root=None):
    location = binding(root)
    if location and location['status'] != 'active':
        raise ValidationError('state relocation is moving')
    if state_root is not None:
        selected = Path(state_root)
        require(selected.is_absolute() and '..' not in selected.parts,
                'state root must be absolute and traversal-free')
        selected = resolved_directory(selected, 'state root')
    elif location:
        raise ValidationError('active binding requires explicit --state-root')
    elif fallback_state_root is not None:
        selected = Path(fallback_state_root)
        require(selected.is_absolute(), 'recorded ledger root is not absolute')
        selected = resolved_directory(selected, 'recorded ledger root')
    else:
        selected = root / '.texenda'
    if location:
        require(selected == Path(location['state_root']), 'state root does not match active binding')
        require(not (root / '.texenda/state.json').exists()
                and not (root / '.texenda/state.lock').exists(), 'competing default state remains')
    require(not state_transaction_blockers(selected),
            'state-write transaction is pending explicit recovery')
    raw = stable_bytes(selected / 'state.json')
    state = loads(raw)
    check_receipts(state)
    if location:
        baseline = location['baseline']
        require(len(state['events']) >= baseline['receipt_count'],
                'bound receipt chain is shorter than its baseline')
        require(state['events'][baseline['receipt_count'] - 1]['hash'] == baseline['receipt_tip'],
                'bound receipt prefix differs from its baseline')
        if len(state['events']) == baseline['receipt_count']:
            require(sha(raw) == baseline['state_sha256'],
                    'bound state bytes differ at unchanged receipt count')
    require(not state_transaction_blockers(selected),
            'state-write transaction appeared during ledger read')
    return {
        'state_root': str(selected),
        'ledger_sha256': sha(raw),
        'receipt_count': len(state['events']),
        'receipt_tip': state['events'][-1]['hash'],
        'roster_evidence_sha256': sha(canonical(state.get('roster', []))),
        'lease_count': sum(task.get('lease') is not None for task in state.get('tasks', {}).values()),
        'declared_budget_usd': state.get('budget_usd'),
        'state_version': state.get('version'),
        'effective_plan_digest': state.get('effective_plan_digest'),
    }


def git_identity(root=ROOT):
    revision = git('rev-parse', 'HEAD', root=root).strip()
    tree = git('rev-parse', 'HEAD^{tree}', root=root).strip()
    require(re.fullmatch('[0-9a-f]{40}', revision) is not None, 'invalid Git revision')
    require(re.fullmatch('[0-9a-f]{40}', tree) is not None, 'invalid Git tree')
    return revision, tree


def scope_digest(rows):
    return sha(canonical(rows))
