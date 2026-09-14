#!/usr/bin/env python3
"""Exclusively relocate Texenda coordination state and a private-input directory.

The helper holds the existing state lock across each prepare/apply/recovery
transaction. Private-input contents are never opened, listed, hashed, parsed, or
copied. Every move uses an OS no-replace rename primitive and fails closed when
that primitive is unavailable.
"""
from __future__ import annotations

import argparse
import contextlib
import ctypes
import errno
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HARNESS_PATH = ROOT / 'tooling/coordination/harness.py'
_spec = importlib.util.spec_from_file_location('texenda_coordination_for_relocation', HARNESS_PATH)
coordination = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(coordination)
Denied = coordination.Denied
MIGRATION_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def validate_migration_id(value):
    if not isinstance(value, str) or MIGRATION_ID.fullmatch(value) is None:
        raise Denied('migration_id must be a safe 1-64 character filename identifier')
    return value


def no_symlink_components(path, label, *, allow_missing_leaf=False):
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise Denied(label + ' must be canonical, absolute, and traversal-free')
    current = Path(path.anchor)
    parts = path.parts[1:]
    for index, part in enumerate(parts):
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            if allow_missing_leaf and index == len(parts) - 1:
                return path
            raise Denied(label + ' has a missing target or parent')
        if stat.S_ISLNK(mode):
            raise Denied(label + ' contains a symlink alias')
    return path


def regular_file(path, label, *, required=True):
    path = Path(path)
    try:
        no_symlink_components(path, label, allow_missing_leaf=not required)
        mode = path.lstat().st_mode
    except FileNotFoundError:
        if required:
            raise Denied(label + ' is missing')
        return False
    if not stat.S_ISREG(mode):
        raise Denied(label + ' must be a regular non-symlink file')
    return True


def directory(path, label, *, required=True):
    path = Path(path)
    try:
        no_symlink_components(path, label, allow_missing_leaf=not required)
        mode = path.lstat().st_mode
    except FileNotFoundError:
        if required:
            raise Denied(label + ' is missing')
        return False
    if not stat.S_ISDIR(mode):
        raise Denied(label + ' must be a non-symlink directory')
    return True


def stable_file_bytes(path, label):
    regular_file(path, label)
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)

    def once():
        no_symlink_components(path, label)
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
            current = path.lstat()
        finally:
            os.close(descriptor)
        identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
                    before.st_ctime_ns)
        if identity != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                        after.st_ctime_ns) or (after.st_dev, after.st_ino) != (current.st_dev,
                                                                            current.st_ino):
            raise Denied(label + ' changed during stable read')
        return b''.join(chunks), identity

    first, second = once(), once()
    if first != second:
        raise Denied(label + ' changed or was replaced during stable read')
    return first[0]


def state_facts(path):
    raw = stable_file_bytes(path, 'state file')
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
    coordination.resolved_directory(home, 'project home', absolute=True)
    expected = home / 'local/agent-state/texenda'
    if requested != expected:
        raise Denied('state root differs from the frozen workspace location')
    if expected.exists() or expected.is_symlink():
        external = coordination.resolved_directory(expected, 'state root', absolute=True)
    else:
        parent = coordination.resolved_directory(expected.parent, 'state-root parent', absolute=True)
        external = parent / expected.name
        no_symlink_components(external, 'state root', allow_missing_leaf=True)
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


def revalidate_parents(paths, *, state_root_may_be_missing=False):
    for key in ('repo', 'home', 'default_root'):
        directory(paths[key], key.replace('_', ' '))
    directory(paths['state_root'].parent, 'state-root parent')
    directory(paths['destination_private'].parent, 'private destination parent')
    directory(paths['rollback_records'].parent, 'rollback-record parent')
    directory(paths['state_root'], 'state root', required=not state_root_may_be_missing)
    no_symlink_components(paths['binding'], 'binding path', allow_missing_leaf=True)


def write_exclusive_json(path, value):
    directory(path.parent, 'binding parent')
    no_symlink_components(path, 'binding path', allow_missing_leaf=True)
    raw = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False).encode() + b'\n'
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(path, flags, 0o600)
    with os.fdopen(descriptor, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    parent_descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)
    return raw


def replace_binding(path, value, expected_raw):
    directory(path.parent, 'binding parent')
    if stable_file_bytes(path, 'state binding') != expected_raw:
        raise Denied('state binding changed before activation')
    raw = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False).encode() + b'\n'
    descriptor, temporary = tempfile.mkstemp(prefix='.state-location-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        no_symlink_components(path, 'state binding')
        if stable_file_bytes(path, 'state binding') != expected_raw:
            raise Denied('state binding changed at activation boundary')
        os.replace(temporary, path)
        parent_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(parent_descriptor)
        finally:
            os.close(parent_descriptor)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _exclusive_rename_syscall(source, destination):
    libc = ctypes.CDLL(None, use_errno=True)
    source_bytes, destination_bytes = os.fsencode(source), os.fsencode(destination)
    if sys.platform == 'darwin' and hasattr(libc, 'renamex_np'):
        operation = libc.renamex_np
        operation.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint)
        operation.restype = ctypes.c_int
        result = operation(source_bytes, destination_bytes, 0x00000004)  # RENAME_EXCL
    elif sys.platform.startswith('linux') and hasattr(libc, 'renameat2'):
        operation = libc.renameat2
        operation.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                              ctypes.c_char_p, ctypes.c_uint)
        operation.restype = ctypes.c_int
        result = operation(-100, source_bytes, -100, destination_bytes, 1)  # RENAME_NOREPLACE
    else:
        raise Denied('platform lacks an atomic exclusive rename primitive')
    if result != 0:
        error = ctypes.get_errno()
        if error in (errno.EEXIST, errno.ENOTEMPTY):
            raise Denied('exclusive rename destination already exists')
        raise OSError(error, os.strerror(error), str(source), str(destination))


def rename_no_replace(source, destination, label, *, race_hook=None):
    source, destination = Path(source), Path(destination)
    no_symlink_components(source, label + ' source')
    directory(source.parent, label + ' source parent')
    directory(destination.parent, label + ' destination parent')
    source_identity = source.lstat()
    source_parent_identity = source.parent.lstat()
    destination_parent_identity = destination.parent.lstat()
    no_symlink_components(destination, label + ' destination', allow_missing_leaf=True)
    if destination.exists() or destination.is_symlink():
        raise Denied(label + ' destination already exists')
    if race_hook:
        race_hook(source, destination)
    # Parent and source may have been substituted by the hook or another actor.
    no_symlink_components(source, label + ' source')
    directory(source.parent, label + ' source parent')
    directory(destination.parent, label + ' destination parent')
    current_source = source.lstat()
    current_source_parent = source.parent.lstat()
    current_destination_parent = destination.parent.lstat()
    if ((current_source.st_dev, current_source.st_ino, stat.S_IFMT(current_source.st_mode))
            != (source_identity.st_dev, source_identity.st_ino, stat.S_IFMT(source_identity.st_mode))
            or (current_source_parent.st_dev, current_source_parent.st_ino)
            != (source_parent_identity.st_dev, source_parent_identity.st_ino)
            or (current_destination_parent.st_dev, current_destination_parent.st_ino)
            != (destination_parent_identity.st_dev, destination_parent_identity.st_ino)):
        raise Denied(label + ' source or parent was substituted before exclusive rename')
    _exclusive_rename_syscall(source, destination)


def one_location(source, destination, label):
    source_exists = source.exists() or source.is_symlink()
    destination_exists = destination.exists() or destination.is_symlink()
    if source_exists == destination_exists:
        raise Denied(label + ' must exist at exactly one reviewed location')
    selected = source if source_exists else destination
    no_symlink_components(selected, label)
    return selected


@contextlib.contextmanager
def held_relocation_lock(paths):
    lock_path = one_location(paths['source_lock'], paths['destination_lock'], 'state lock')
    regular_file(lock_path, 'state lock')
    flags = os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(lock_path, flags)
    try:
        opened = os.fstat(descriptor)
        current = lock_path.lstat()
        if (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino):
            raise Denied('state lock was substituted before acquisition')
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise Denied('state lock is held; runtime-stop proof is insufficient') from exc
        current = lock_path.lstat()
        if (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino):
            raise Denied('state lock was substituted during acquisition')
        yield lock_path, descriptor
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def require_held_lock_path(path, descriptor):
    regular_file(path, 'held state lock')
    opened = os.fstat(descriptor)
    current = path.lstat()
    if (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino):
        raise Denied('held state lock path was substituted')


def read_moving(paths):
    raw = stable_file_bytes(paths['binding'], 'state binding')
    value = coordination.load_binding(paths['binding'], paths['repo'])
    if stable_file_bytes(paths['binding'], 'state binding') != raw:
        raise Denied('state binding changed during read')
    if value is None or value['status'] != 'moving':
        raise Denied('relocation is not in moving status')
    validate_migration_id(value['migration_id'])
    if Path(value['state_root']) != paths['state_root']:
        raise Denied('moving binding state root mismatch')
    return value, raw


def baseline_matches(facts, baseline, label):
    if (facts['state_sha256'] != baseline['state_sha256']
            or facts['receipt_count'] != baseline['receipt_count']
            or facts['receipt_tip'] != baseline['receipt_tip']):
        raise Denied(label + ' differs from the prepared state/receipt boundary')


def prepare(repository_root, state_root, migration_id='state-root-20260914'):
    migration_id = validate_migration_id(migration_id)
    paths = layout(repository_root, state_root)
    revalidate_parents(paths, state_root_may_be_missing=True)
    ignore = paths['repo'] / '.gitignore'
    regular_file(ignore, 'repository ignore file')
    if coordination.BINDING_NAME not in ignore.read_text().splitlines():
        raise Denied('state-location binding must have an exact repository ignore rule')
    if paths['binding'].exists() or paths['binding'].is_symlink():
        raise Denied('state-location binding already exists; verify or recover it')
    if paths['state_root'].exists() or paths['state_root'].is_symlink():
        directory(paths['state_root'], 'state root')
        if any(paths['state_root'].iterdir()):
            raise Denied('state root must be empty before preparation')
    else:
        directory(paths['state_root'].parent, 'state-root parent')
        os.mkdir(paths['state_root'], 0o700)
    revalidate_parents(paths)
    with held_relocation_lock(paths) as (lock_path, _descriptor):
        require_held_lock_path(lock_path, _descriptor)
        if lock_path != paths['source_lock']:
            raise Denied('prepare requires the lock at the default source')
        if any(paths['state_root'].iterdir()):
            raise Denied('state root changed or is no longer empty during preparation')
        facts = state_facts(paths['source_state'])
        if paths['destination_state'].exists() or paths['destination_state'].is_symlink():
            raise Denied('destination state already exists')
        directory(paths['source_private'], 'private-input source directory')
        if paths['destination_private'].exists() or paths['destination_private'].is_symlink():
            raise Denied('private-input destination already exists')
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


def verify_layout(paths, binding, *, moving=False):
    revalidate_parents(paths)
    if not moving and binding['status'] != 'active':
        raise Denied('state relocation is not active')
    if (paths['source_state'].exists() or paths['source_state'].is_symlink()
            or paths['source_lock'].exists() or paths['source_lock'].is_symlink()):
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


def apply(repository_root, state_root, *, stop_after=None, race_hooks=None,
          interleave=None):
    paths = layout(repository_root, state_root)
    revalidate_parents(paths)
    binding, binding_raw = read_moving(paths)
    hooks = race_hooks or {}
    with held_relocation_lock(paths) as (lock_path, _descriptor):
        require_held_lock_path(lock_path, _descriptor)
        revalidate_parents(paths)
        if stable_file_bytes(paths['binding'], 'state binding') != binding_raw:
            raise Denied('state binding changed before relocation')
        current_state = one_location(paths['source_state'], paths['destination_state'], 'state file')
        facts = state_facts(current_state)
        baseline_matches(facts, binding['baseline'], 'state')
        if current_state == paths['source_state']:
            rename_no_replace(paths['source_state'], paths['destination_state'], 'state file',
                              race_hook=hooks.get('state'))
        if interleave:
            interleave('after_state', paths, facts['raw'])
        if stop_after == 'state':
            raise RuntimeError('synthetic interruption after state rename')
        if lock_path == paths['source_lock']:
            require_held_lock_path(paths['source_lock'], _descriptor)
            rename_no_replace(paths['source_lock'], paths['destination_lock'], 'state lock',
                              race_hook=hooks.get('lock'))
            lock_path = paths['destination_lock']
        require_held_lock_path(lock_path, _descriptor)
        if interleave:
            interleave('after_lock', paths, facts['raw'])
        if stop_after == 'lock':
            raise RuntimeError('synthetic interruption after lock rename')
        current_private = one_location(paths['source_private'], paths['destination_private'],
                                       'private-input directory')
        directory(current_private, 'private-input directory')
        if current_private == paths['source_private']:
            rename_no_replace(paths['source_private'], paths['destination_private'],
                              'private-input directory', race_hook=hooks.get('private'))
        if interleave:
            interleave('after_private', paths, facts['raw'])
        if stop_after == 'private':
            raise RuntimeError('synthetic interruption after private-input rename')
        result = verify_layout(paths, binding, moving=True)
        require_held_lock_path(paths['destination_lock'], _descriptor)
        if stable_file_bytes(paths['binding'], 'state binding') != binding_raw:
            raise Denied('state binding changed at final activation boundary')
        replace_binding(paths['binding'], dict(binding, status='active'), binding_raw)
    return dict(result, status='active')


def verify(repository_root, state_root):
    paths = layout(repository_root, state_root)
    revalidate_parents(paths)
    raw = stable_file_bytes(paths['binding'], 'state binding')
    binding = coordination.load_binding(paths['binding'], paths['repo'])
    if binding is None or binding['status'] != 'active':
        raise Denied('state relocation is not active')
    if Path(binding['state_root']) != paths['state_root']:
        raise Denied('active binding state root mismatch')
    with held_relocation_lock(paths) as (lock_path, descriptor):
        require_held_lock_path(lock_path, descriptor)
        if stable_file_bytes(paths['binding'], 'state binding') != raw:
            raise Denied('state binding changed during verification')
        result = verify_layout(paths, binding)
    return dict(result, status='active', migration_id=binding['migration_id'])


def rollback(repository_root, state_root, *, race_hooks=None, interleave=None):
    paths = layout(repository_root, state_root)
    revalidate_parents(paths)
    binding, binding_raw = read_moving(paths)
    hooks = race_hooks or {}
    with held_relocation_lock(paths) as (lock_path, _descriptor):
        require_held_lock_path(lock_path, _descriptor)
        revalidate_parents(paths)
        current_state = one_location(paths['source_state'], paths['destination_state'], 'state file')
        facts = state_facts(current_state)
        baseline_matches(facts, binding['baseline'], 'rollback state')
        if current_state == paths['destination_state']:
            rename_no_replace(paths['destination_state'], paths['source_state'], 'state rollback',
                              race_hook=hooks.get('state'))
        if lock_path == paths['destination_lock']:
            require_held_lock_path(paths['destination_lock'], _descriptor)
            rename_no_replace(paths['destination_lock'], paths['source_lock'], 'lock rollback',
                              race_hook=hooks.get('lock'))
            lock_path = paths['source_lock']
        require_held_lock_path(lock_path, _descriptor)
        current_private = one_location(paths['source_private'], paths['destination_private'],
                                       'private-input directory')
        directory(current_private, 'private-input directory')
        if current_private == paths['destination_private']:
            rename_no_replace(paths['destination_private'], paths['source_private'],
                              'private-input rollback', race_hook=hooks.get('private'))
        if interleave:
            interleave('before_rollback_record', paths, facts['raw'])
        restored = state_facts(paths['source_state'])
        baseline_matches(restored, binding['baseline'], 'restored state')
        if paths['rollback_records'].exists() or paths['rollback_records'].is_symlink():
            directory(paths['rollback_records'], 'rollback records')
        else:
            directory(paths['rollback_records'].parent, 'rollback-record parent')
            os.mkdir(paths['rollback_records'], 0o700)
        directory(paths['rollback_records'], 'rollback records')
        record = paths['rollback_records'] / (validate_migration_id(binding['migration_id'])
                                               + '.rolled-back.json')
        no_symlink_components(record, 'rollback record', allow_missing_leaf=True)
        if stable_file_bytes(paths['binding'], 'state binding') != binding_raw:
            raise Denied('state binding changed at rollback archive boundary')
        require_held_lock_path(paths['source_lock'], _descriptor)
        rename_no_replace(paths['binding'], record, 'rollback binding record',
                          race_hook=hooks.get('binding'))
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
