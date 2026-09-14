#!/usr/bin/env python3
"""Verified, non-copying relocation of Texenda's active local coordination state.

This helper never reads, lists, hashes, copies, or deletes private-input contents.
It writes a closed moving marker before renames and supports verified resume or
reverse-rename rollback. It performs no Git, network, provider, or product action.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HARNESS_PATH = ROOT / 'tooling/coordination/harness.py'
_spec = importlib.util.spec_from_file_location('texenda_coordination_for_relocation', HARNESS_PATH)
coordination = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(coordination)
Denied = coordination.Denied


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def regular_file(path, label, *, required=True):
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        if required:
            raise Denied(label + ' is missing')
        return False
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        raise Denied(label + ' must be a regular non-symlink file')
    return True


def directory(path, label, *, required=True):
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        if required:
            raise Denied(label + ' is missing')
        return False
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        raise Denied(label + ' must be a non-symlink directory')
    return True


def stable_bytes(path):
    regular_file(path, 'state file')
    flags = os.O_RDONLY | (getattr(os, 'O_NOFOLLOW', 0))

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
        if identity != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                        after.st_ctime_ns):
            raise Denied('state changed during relocation read')
        return b''.join(chunks), identity

    first = once()
    second = once()
    if first != second:
        raise Denied('state changed or was replaced during relocation read')
    return first[0]


def state_facts(path):
    raw = stable_bytes(path)
    state = coordination.load_json(raw)
    coordination.check_receipts(state)
    return {
        'raw': raw,
        'state_sha256': sha(raw),
        'receipt_count': len(state['events']),
        'receipt_tip': state['events'][-1]['hash'],
        'state': state,
    }


def layout(repository_root, state_root):
    repo = coordination.resolved_directory(repository_root, 'repository root')
    requested = Path(state_root)
    if not requested.is_absolute() or '..' in requested.parts:
        raise Denied('state root must be absolute and traversal-free')
    home = repo.parent
    expected = home / 'local/agent-state/texenda'
    if requested != expected:
        raise Denied('state root differs from the frozen workspace location')
    if expected.exists():
        external = coordination.resolved_directory(expected, 'state root', absolute=True,
                                                    component_symlinks=True)
    else:
        parent = coordination.resolved_directory(expected.parent, 'state-root parent', absolute=True,
                                                  component_symlinks=True)
        external = parent / expected.name
    return {
        'repo': repo,
        'home': home,
        'binding': repo / coordination.BINDING_NAME,
        'default_root': repo / '.texenda',
        'source_state': repo / '.texenda/state.json',
        'source_lock': repo / '.texenda/state.lock',
        'source_private': repo / '.texenda/private-inputs',
        'state_root': external,
        'destination_state': external / 'state.json',
        'destination_lock': external / 'state.lock',
        'destination_private': home / 'local/private-inputs',
        'rollback_records': home / 'local/logs/workspace-relocation',
    }


def write_exclusive_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False).encode() + b'\n'
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | (getattr(os, 'O_NOFOLLOW', 0))
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        raise
    directory_descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_descriptor)
    finally:
        os.close(directory_descriptor)


def replace_json(path, value):
    raw = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False).encode() + b'\n'
    descriptor, temporary = tempfile.mkstemp(prefix='.state-location-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def rename_no_replace(source, destination, label):
    if destination.exists() or destination.is_symlink():
        raise Denied(label + ' destination already exists')
    if source.is_symlink():
        raise Denied(label + ' source cannot be a symlink')
    os.rename(source, destination)


def prepare(repository_root, state_root, migration_id='state-root-20260914'):
    paths = layout(repository_root, state_root)
    ignore = paths['repo'] / '.gitignore'
    if (not ignore.is_file() or ignore.is_symlink()
            or coordination.BINDING_NAME not in ignore.read_text().splitlines()):
        raise Denied('state-location binding must have an exact repository ignore rule')
    if paths['binding'].exists() or paths['binding'].is_symlink():
        raise Denied('state-location binding already exists; verify or recover it')
    directory(paths['default_root'], 'default state directory')
    facts = state_facts(paths['source_state'])
    regular_file(paths['destination_state'], 'destination state', required=False)
    if paths['destination_state'].exists():
        raise Denied('destination state already exists')
    directory(paths['source_private'], 'private-input source directory')
    if paths['destination_private'].exists() or paths['destination_private'].is_symlink():
        raise Denied('private-input destination already exists')
    if paths['state_root'].exists():
        directory(paths['state_root'], 'state root')
        if any(paths['state_root'].iterdir()):
            raise Denied('state root must be empty before preparation')
    else:
        paths['state_root'].mkdir(mode=0o700)
    binding = {
        'schema_version': coordination.BINDING_VERSION,
        'migration_id': migration_id,
        'repository_root': str(paths['repo']),
        'state_root': str(paths['state_root']),
        'status': 'moving',
        'baseline': {key: facts[key] for key in
                     ('state_sha256', 'receipt_count', 'receipt_tip')},
    }
    write_exclusive_json(paths['binding'], binding)
    return {'status': 'moving', 'binding': str(paths['binding']), **binding['baseline']}


def read_moving(paths):
    binding = coordination.load_binding(paths['binding'], paths['repo'])
    if binding is None:
        raise Denied('state-location binding is missing')
    if binding['status'] != 'moving':
        raise Denied('relocation is not in moving status')
    if Path(binding['state_root']) != paths['state_root']:
        raise Denied('moving binding state root mismatch')
    return binding


def one_location(source, destination, label):
    source_exists = source.exists() or source.is_symlink()
    destination_exists = destination.exists() or destination.is_symlink()
    if source_exists == destination_exists:
        raise Denied(label + ' must exist at exactly one reviewed location')
    return source if source_exists else destination


def move_lock(source, destination):
    if source.exists() and destination.exists():
        raise Denied('lock exists at both locations')
    if not source.exists():
        if destination.exists():
            regular_file(destination, 'destination lock')
        return
    regular_file(source, 'source lock')
    flags = os.O_RDWR | (getattr(os, 'O_NOFOLLOW', 0))
    descriptor = os.open(source, flags)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise Denied('state lock is held; runtime-stop proof is insufficient') from exc
        rename_no_replace(source, destination, 'state lock')
        fcntl.flock(descriptor, fcntl.LOCK_UN)
    finally:
        os.close(descriptor)


def apply(repository_root, state_root, *, stop_after=None):
    paths = layout(repository_root, state_root)
    binding = read_moving(paths)
    current_state = one_location(paths['source_state'], paths['destination_state'], 'state file')
    facts = state_facts(current_state)
    if facts['state_sha256'] != binding['baseline']['state_sha256']:
        raise Denied('state bytes differ from the prepared migration boundary')
    if current_state == paths['source_state']:
        rename_no_replace(paths['source_state'], paths['destination_state'], 'state file')
    if stop_after == 'state':
        raise RuntimeError('synthetic interruption after state rename')
    move_lock(paths['source_lock'], paths['destination_lock'])
    if stop_after == 'lock':
        raise RuntimeError('synthetic interruption after lock rename')
    current_private = one_location(paths['source_private'], paths['destination_private'],
                                   'private-input directory')
    directory(current_private, 'private-input directory')
    if current_private == paths['source_private']:
        rename_no_replace(paths['source_private'], paths['destination_private'],
                          'private-input directory')
    if stop_after == 'private':
        raise RuntimeError('synthetic interruption after private-input rename')
    result = verify_layout(paths, binding, moving=True)
    active = dict(binding, status='active')
    replace_json(paths['binding'], active)
    return dict(result, status='active')


def verify_layout(paths, binding, *, moving=False):
    if not moving and binding['status'] != 'active':
        raise Denied('state relocation is not active')
    if paths['source_state'].exists() or paths['source_lock'].exists():
        raise Denied('default active state or lock remains after relocation')
    facts = state_facts(paths['destination_state'])
    baseline = binding['baseline']
    if facts['receipt_count'] < baseline['receipt_count']:
        raise Denied('receipt chain is shorter than the migration baseline')
    if facts['state']['events'][baseline['receipt_count'] - 1]['hash'] != baseline['receipt_tip']:
        raise Denied('receipt prefix differs from the migration baseline')
    if (facts['receipt_count'] == baseline['receipt_count']
            and facts['state_sha256'] != baseline['state_sha256']):
        raise Denied('unchanged receipt count has changed state bytes')
    if paths['source_private'].exists() or paths['source_private'].is_symlink():
        raise Denied('private-input source remains after relocation')
    directory(paths['destination_private'], 'private-input destination')
    return {
        'state_sha256': facts['state_sha256'],
        'receipt_count': facts['receipt_count'],
        'receipt_tip': facts['receipt_tip'],
        'private_input_check': 'location_only_no_content_access',
    }


def verify(repository_root, state_root):
    paths = layout(repository_root, state_root)
    binding = coordination.load_binding(paths['binding'], paths['repo'])
    if binding is None:
        raise Denied('state-location binding is missing')
    if Path(binding['state_root']) != paths['state_root']:
        raise Denied('active binding state root mismatch')
    return dict(verify_layout(paths, binding), status='active', migration_id=binding['migration_id'])


def rollback(repository_root, state_root):
    paths = layout(repository_root, state_root)
    binding = read_moving(paths)
    current_state = one_location(paths['source_state'], paths['destination_state'], 'state file')
    facts = state_facts(current_state)
    if facts['state_sha256'] != binding['baseline']['state_sha256']:
        raise Denied('rollback state bytes differ from the prepared boundary')
    if current_state == paths['destination_state']:
        rename_no_replace(paths['destination_state'], paths['source_state'], 'state rollback')
    move_lock(paths['destination_lock'], paths['source_lock'])
    current_private = one_location(paths['source_private'], paths['destination_private'],
                                   'private-input directory')
    directory(current_private, 'private-input directory')
    if current_private == paths['destination_private']:
        rename_no_replace(paths['destination_private'], paths['source_private'],
                          'private-input rollback')
    restored = state_facts(paths['source_state'])
    if restored['state_sha256'] != binding['baseline']['state_sha256']:
        raise Denied('restored state differs from prepared bytes')
    paths['rollback_records'].mkdir(parents=True, exist_ok=True)
    record = paths['rollback_records'] / (binding['migration_id'] + '.rolled-back.json')
    rename_no_replace(paths['binding'], record, 'rollback binding record')
    return {
        'status': 'rolled_back',
        'state_sha256': restored['state_sha256'],
        'receipt_count': restored['receipt_count'],
        'receipt_tip': restored['receipt_tip'],
        'binding_record': str(record),
        'private_input_check': 'location_only_no_content_access',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', required=True, type=Path)
    parser.add_argument('--state-root', required=True, type=Path)
    sub = parser.add_subparsers(dest='command', required=True)
    prepare_parser = sub.add_parser('prepare')
    prepare_parser.add_argument('--migration-id', default='state-root-20260914')
    sub.add_parser('apply')
    recover_parser = sub.add_parser('recover')
    recover_parser.add_argument('--direction', required=True, choices=('resume', 'rollback'))
    sub.add_parser('verify')
    args = parser.parse_args(argv)
    try:
        if args.command == 'prepare':
            result = prepare(args.repo_root, args.state_root, args.migration_id)
        elif args.command == 'apply':
            result = apply(args.repo_root, args.state_root)
        elif args.command == 'recover' and args.direction == 'resume':
            result = apply(args.repo_root, args.state_root)
        elif args.command == 'recover':
            result = rollback(args.repo_root, args.state_root)
        else:
            result = verify(args.repo_root, args.state_root)
        print(json.dumps(result, indent=2))
        return 0
    except (Denied, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
