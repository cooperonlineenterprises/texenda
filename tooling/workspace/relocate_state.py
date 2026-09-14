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
import secrets
import stat
import sys


ROOT = Path(__file__).resolve().parents[2]
HARNESS_PATH = ROOT / 'tooling/coordination/harness.py'
_spec = importlib.util.spec_from_file_location('texenda_coordination_for_relocation', HARNESS_PATH)
coordination = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(coordination)
Denied = coordination.Denied
MIGRATION_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def path_identity(path):
    value = Path(path).lstat()
    return (value.st_dev, value.st_ino, value.st_mode, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns)


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


def _renameat_syscall(source_fd, source_name, destination_fd, destination_name, flag):
    libc = ctypes.CDLL(None, use_errno=True)
    source_bytes, destination_bytes = os.fsencode(source_name), os.fsencode(destination_name)
    if sys.platform == 'darwin' and hasattr(libc, 'renameatx_np'):
        operation = libc.renameatx_np
        operation.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                              ctypes.c_char_p, ctypes.c_uint)
        operation.restype = ctypes.c_int
        darwin_flag = 0x00000004 if flag == 'exclusive' else 0x00000002
        result = operation(source_fd, source_bytes, destination_fd, destination_bytes,
                           darwin_flag)
    elif sys.platform.startswith('linux') and hasattr(libc, 'renameat2'):
        operation = libc.renameat2
        operation.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                              ctypes.c_char_p, ctypes.c_uint)
        operation.restype = ctypes.c_int
        linux_flag = 1 if flag == 'exclusive' else 2
        result = operation(source_fd, source_bytes, destination_fd, destination_bytes,
                           linux_flag)
    else:
        raise Denied('platform lacks the required descriptor-relative rename primitive')
    if result != 0:
        error = ctypes.get_errno()
        if error in (errno.EEXIST, errno.ENOTEMPTY):
            raise Denied('exclusive rename destination already exists')
        raise OSError(error, os.strerror(error), str(source_name), str(destination_name))


def _exclusive_rename_syscall(source_fd, source_name, destination_fd, destination_name):
    _renameat_syscall(source_fd, source_name, destination_fd, destination_name, 'exclusive')


def _exchange_rename_syscall(first_fd, first_name, second_fd, second_name):
    _renameat_syscall(first_fd, first_name, second_fd, second_name, 'exchange')


def _fsync_rename_parents(source_fd, destination_fd):
    """Persist destination then source namespaces; sync a shared parent once."""
    destination = os.fstat(destination_fd)
    source = os.fstat(source_fd)
    os.fsync(destination_fd)
    if (source.st_dev, source.st_ino) != (destination.st_dev, destination.st_ino):
        os.fsync(source_fd)


def _exclusive_rename_durable(source_fd, source_name, destination_fd, destination_name):
    _exclusive_rename_syscall(source_fd, source_name, destination_fd, destination_name)
    _fsync_rename_parents(source_fd, destination_fd)


def _exchange_rename_durable(first_fd, first_name, second_fd, second_name):
    _exchange_rename_syscall(first_fd, first_name, second_fd, second_name)
    _fsync_rename_parents(first_fd, second_fd)


def _open_directory_fd(path, label):
    path = Path(path)
    directory(path, label)
    expected = path.lstat()
    flags = os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(path, flags)
    opened = os.fstat(descriptor)
    current = path.lstat()
    if ((opened.st_dev, opened.st_ino, stat.S_IFMT(opened.st_mode))
            != (expected.st_dev, expected.st_ino, stat.S_IFMT(expected.st_mode))
            or (current.st_dev, current.st_ino) != (opened.st_dev, opened.st_ino)):
        os.close(descriptor)
        raise Denied(label + ' changed during anchored open')
    return descriptor


def _stable_at(directory_fd, name, label):
    if '/' in name or name in ('', '.', '..'):
        raise Denied(label + ' has an unsafe descriptor-relative name')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)

    def once():
        descriptor = os.open(name, flags, dir_fd=directory_fd)
        try:
            before = os.fstat(descriptor)
            chunks = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            after = os.fstat(descriptor)
            current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        finally:
            os.close(descriptor)
        identity = (before.st_dev, before.st_ino, before.st_mode, before.st_size,
                    before.st_mtime_ns, before.st_ctime_ns)
        if (identity != (after.st_dev, after.st_ino, after.st_mode, after.st_size,
                         after.st_mtime_ns, after.st_ctime_ns)
                or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino)):
            raise Denied(label + ' changed during anchored read')
        return b''.join(chunks), identity

    first, second = once(), once()
    if first != second:
        raise Denied(label + ' changed or was replaced during anchored read')
    return first


def _write_at_exclusive(directory_fd, name, raw, label):
    if '/' in name or name in ('', '.', '..'):
        raise Denied(label + ' has an unsafe descriptor-relative name')
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(name, flags, 0o600, dir_fd=directory_fd)
    with os.fdopen(descriptor, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.fsync(directory_fd)


def _exists_at(directory_fd, name):
    try:
        os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        return True
    except FileNotFoundError:
        return False


def _ensure_recovery_directory(paths):
    if paths['rollback_records'].exists() or paths['rollback_records'].is_symlink():
        directory(paths['rollback_records'], 'rollback records')
    else:
        directory(paths['rollback_records'].parent, 'rollback-record parent')
        parent_fd = _open_directory_fd(paths['rollback_records'].parent,
                                       'rollback-record parent')
        try:
            os.mkdir(paths['rollback_records'].name, 0o700, dir_fd=parent_fd)
            os.fsync(parent_fd)
        finally:
            os.close(parent_fd)
    directory(paths['rollback_records'], 'rollback records')


def _complete_activation_transaction(recovery_fd, transaction_name, completed_name):
    """Durably complete, or restore the pending name before propagating failure."""
    _exclusive_rename_syscall(recovery_fd, transaction_name, recovery_fd,
                              completed_name)
    try:
        _fsync_rename_parents(recovery_fd, recovery_fd)
    except BaseException as sync_error:
        try:
            _exclusive_rename_syscall(recovery_fd, completed_name, recovery_fd,
                                      transaction_name)
            _fsync_rename_parents(recovery_fd, recovery_fd)
        except BaseException as rollback_error:
            raise Denied(
                'activation completion durability failed; recovery layout is ambiguous'
            ) from rollback_error
        raise sync_error


def activate_binding(paths, binding, binding_raw, binding_identity, *, race_hook=None,
                     interleave=None):
    """CAS activation by atomic exchange; never discard a raced descriptor."""
    _ensure_recovery_directory(paths)
    migration_id = validate_migration_id(binding['migration_id'])
    active_raw = json.dumps(dict(binding, status='active'), indent=2,
                            ensure_ascii=False, allow_nan=False).encode() + b'\n'
    token = secrets.token_hex(8)
    temporary_name = '.texenda-location.activation-' + token
    transaction_name = migration_id + '.activation-transaction.json'
    completed_name = migration_id + '.activation-complete.' + token + '.json'
    moving_archive = migration_id + '.activated-moving.json'
    conflict_name = migration_id + '.activation-conflict.' + token + '.json'
    transaction = {
        'schema_version': 'texenda.state-location-activation.v1',
        'migration_id': migration_id,
        'temporary_name': temporary_name,
        'expected_moving_sha256': sha(binding_raw),
        'candidate_active_sha256': sha(active_raw),
        'token': token,
    }
    transaction_raw = json.dumps(transaction, indent=2, sort_keys=True).encode() + b'\n'
    repo_fd = _open_directory_fd(paths['repo'], 'repository root')
    recovery_fd = _open_directory_fd(paths['rollback_records'], 'rollback records')
    exchanged = False
    committed = False
    try:
        _write_at_exclusive(recovery_fd, transaction_name, transaction_raw,
                            'activation transaction')
        _write_at_exclusive(repo_fd, temporary_name, active_raw, 'active binding candidate')
        current_raw, current_identity = _stable_at(repo_fd, coordination.BINDING_NAME,
                                                   'moving binding')
        current_inode = (current_identity[0], current_identity[1],
                         stat.S_IFMT(current_identity[2]))
        if current_raw != binding_raw or current_inode != binding_identity:
            raise Denied('state binding changed before atomic activation exchange')
        if race_hook:
            race_hook(paths['binding'], paths['binding'])
        _exchange_rename_syscall(repo_fd, temporary_name, repo_fd,
                                 coordination.BINDING_NAME)
        exchanged = True
        _fsync_rename_parents(repo_fd, repo_fd)
        if interleave:
            interleave('binding_after_exchange', paths, active_raw)
        displaced_raw, displaced_identity = _stable_at(repo_fd, temporary_name,
                                                        'displaced moving binding')
        displaced_inode = (displaced_identity[0], displaced_identity[1],
                           stat.S_IFMT(displaced_identity[2]))
        if displaced_raw != binding_raw or displaced_inode != binding_identity:
            raise Denied('raced state binding detected by atomic activation exchange')
        _exclusive_rename_syscall(repo_fd, temporary_name, recovery_fd, moving_archive)
        committed = True
        _fsync_rename_parents(repo_fd, recovery_fd)
        if interleave:
            interleave('binding_after_moving_archive', paths, active_raw)
        _complete_activation_transaction(recovery_fd, transaction_name, completed_name)
        if interleave:
            interleave('binding_after_completion_before_return', paths, active_raw)
    except BaseException as exc:
        if exchanged and not committed:
            try:
                _exchange_rename_durable(repo_fd, temporary_name, repo_fd,
                                         coordination.BINDING_NAME)
                exchanged = False
            except BaseException as rollback_error:
                raise Denied('activation exchange could not be rolled back; transaction record retained') from rollback_error
        if not committed:
            try:
                _exclusive_rename_durable(repo_fd, temporary_name, recovery_fd,
                                          conflict_name)
            except (FileNotFoundError, Denied, OSError):
                pass
            try:
                recovered_name = migration_id + '.activation-recovered.' + token + '.json'
                _exclusive_rename_durable(recovery_fd, transaction_name, recovery_fd,
                                          recovered_name)
            except (FileNotFoundError, Denied, OSError):
                pass
        raise exc
    finally:
        os.close(recovery_fd)
        os.close(repo_fd)


def validate_activation_transaction(transaction, migration_id):
    required = {'schema_version', 'migration_id', 'temporary_name',
                'expected_moving_sha256', 'candidate_active_sha256', 'token'}
    if (not isinstance(transaction, dict) or set(transaction) != required
            or transaction.get('schema_version') != 'texenda.state-location-activation.v1'
            or transaction.get('migration_id') != migration_id
            or not re.fullmatch(r'[0-9a-f]{16}', transaction.get('token', ''))
            or transaction.get('temporary_name') != '.texenda-location.activation-'
            + transaction.get('token', '')
            or not re.fullmatch(r'[0-9a-f]{64}', transaction.get('expected_moving_sha256', ''))
            or not re.fullmatch(r'[0-9a-f]{64}', transaction.get('candidate_active_sha256', ''))):
        raise Denied('activation transaction record is invalid')
    return transaction


def validate_moving_archive(recovery_fd, name, transaction, active_binding, active_raw):
    try:
        archived_stat = os.stat(name, dir_fd=recovery_fd, follow_symlinks=False)
    except FileNotFoundError as exc:
        raise Denied('archived moving binding is missing') from exc
    if not stat.S_ISREG(archived_stat.st_mode):
        raise Denied('archived moving binding must be a regular non-symlink file')
    try:
        archive_raw, _archive_identity = _stable_at(recovery_fd, name,
                                                    'archived moving binding')
    except OSError as exc:
        raise Denied('archived moving binding cannot be opened safely') from exc
    if sha(archive_raw) != transaction['expected_moving_sha256']:
        raise Denied('archived moving binding hash differs from activation transaction')
    archived = coordination.load_json(archive_raw)
    if (not isinstance(archived, dict) or archived.get('status') != 'moving'
            or archived.get('migration_id') != transaction['migration_id']
            or dict(archived, status='active') != active_binding
            or sha(active_raw) != transaction['candidate_active_sha256']):
        raise Denied('archived moving binding content does not match active transaction')
    return archived


def recover_activation_transaction(paths):
    """Restore/finish an interrupted activation transaction while state lock is held."""
    _ensure_recovery_directory(paths)
    binding_raw = stable_file_bytes(paths['binding'], 'state binding')
    binding = coordination.load_binding(paths['binding'], paths['repo'])
    migration_id = validate_migration_id(binding['migration_id'])
    transaction_name = migration_id + '.activation-transaction.json'
    recovery_fd = _open_directory_fd(paths['rollback_records'], 'rollback records')
    repo_fd = None
    try:
        pending_names = sorted(name for name in os.listdir(recovery_fd)
                               if name.endswith('.activation-transaction.json'))
        if not pending_names:
            return {'status': 'none'}
        if pending_names != [transaction_name]:
            raise Denied('activation recovery has an ambiguous pending transaction set')
        transaction_stat = os.stat(transaction_name, dir_fd=recovery_fd,
                                   follow_symlinks=False)
        if not stat.S_ISREG(transaction_stat.st_mode):
            raise Denied('activation transaction must be a regular non-symlink file')
        transaction_raw = _stable_at(recovery_fd, transaction_name,
                                     'activation transaction')[0]
        transaction = coordination.load_json(transaction_raw)
        validate_activation_transaction(transaction, migration_id)
        token = transaction['token']
        temporary_name = transaction['temporary_name']
        completed_name = migration_id + '.activation-complete.' + token + '.json'
        recovered_name = migration_id + '.activation-recovered.' + token + '.json'
        conflict_name = migration_id + '.activation-conflict.' + token + '.json'
        moving_archive = migration_id + '.activated-moving.json'
        repo_fd = _open_directory_fd(paths['repo'], 'repository root')
        binding_hash = sha(binding_raw)
        temporary_exists = _exists_at(repo_fd, temporary_name)
        archive_exists = _exists_at(recovery_fd, moving_archive)
        if (binding_hash == transaction['candidate_active_sha256']
                and not temporary_exists and archive_exists):
            # Exchange and moving-descriptor archival committed; only the
            # transaction-record rename was interrupted.
            validate_moving_archive(recovery_fd, moving_archive, transaction,
                                    binding, binding_raw)
            _complete_activation_transaction(recovery_fd, transaction_name,
                                             completed_name)
            return {'status': 'active_committed', 'binding': binding}
        if (binding_hash == transaction['expected_moving_sha256'] and not temporary_exists):
            # Interrupted before candidate creation/exchange. Preserve the
            # transaction as an aborted recovery record and continue moving.
            aborted_name = migration_id + '.activation-aborted.' + token + '.json'
            _exclusive_rename_durable(recovery_fd, transaction_name, recovery_fd,
                                      aborted_name)
            return {'status': 'moving_restored', 'binding': binding}
        if not temporary_exists:
            raise Denied('activation transaction lacks its preserved exchange descriptor')
        temporary_raw, _temporary_identity = _stable_at(repo_fd, temporary_name,
                                                         'activation temporary descriptor')
        if binding_hash == transaction['candidate_active_sha256']:
            # Post-exchange interruption or raced displaced descriptor: restore
            # whatever descriptor was displaced without discarding either file.
            _exchange_rename_durable(repo_fd, temporary_name, repo_fd,
                                     coordination.BINDING_NAME)
            binding_raw = stable_file_bytes(paths['binding'], 'restored state binding')
            temporary_raw, _temporary_identity = _stable_at(
                repo_fd, temporary_name, 'restored active candidate')
        if sha(temporary_raw) != transaction['candidate_active_sha256']:
            raise Denied('activation recovery cannot identify the preserved active candidate')
        _exclusive_rename_durable(repo_fd, temporary_name, recovery_fd, conflict_name)
        _exclusive_rename_durable(recovery_fd, transaction_name, recovery_fd,
                                  recovered_name)
        restored = coordination.load_binding(paths['binding'], paths['repo'])
        if restored['status'] != 'moving':
            raise Denied('activation recovery did not restore a moving binding')
        return {'status': 'moving_restored', 'binding': restored}
    finally:
        os.close(recovery_fd)
        if repo_fd is not None:
            os.close(repo_fd)


def validate_completed_activation(paths):
    binding_raw = stable_file_bytes(paths['binding'], 'state binding')
    binding = coordination.load_binding(paths['binding'], paths['repo'])
    migration_id = validate_migration_id(binding['migration_id'])
    directory(paths['rollback_records'], 'rollback records')
    recovery_fd = _open_directory_fd(paths['rollback_records'], 'rollback records')
    completed_names = sorted(
        name for name in os.listdir(recovery_fd)
        if re.fullmatch(re.escape(migration_id)
                        + r'\.activation-complete\.[0-9a-f]{16}\.json', name)
    )
    if binding['status'] != 'active':
        os.close(recovery_fd)
        if completed_names:
            raise Denied('completed activation evidence conflicts with a non-active binding')
        return None
    if len(completed_names) != 1:
        os.close(recovery_fd)
        raise Denied('active binding requires exactly one completed activation transaction')
    try:
        completed_name = completed_names[0]
        completed_stat = os.stat(completed_name, dir_fd=recovery_fd,
                                 follow_symlinks=False)
        if not stat.S_ISREG(completed_stat.st_mode):
            raise Denied('completed activation transaction must be a regular file')
        transaction = coordination.load_json(_stable_at(
            recovery_fd, completed_name, 'completed activation transaction')[0])
        validate_activation_transaction(transaction, migration_id)
        if sha(binding_raw) != transaction['candidate_active_sha256']:
            raise Denied('completed transaction does not bind the active descriptor')
        validate_moving_archive(recovery_fd, migration_id + '.activated-moving.json',
                                transaction, binding, binding_raw)
    finally:
        os.close(recovery_fd)
    return {'binding': binding, 'transaction': transaction,
            'completed_path': str(paths['rollback_records'] / completed_name)}


def rename_no_replace(source, destination, label, *, race_hook=None):
    source, destination = Path(source), Path(destination)
    no_symlink_components(source, label + ' source')
    directory(source.parent, label + ' source parent')
    directory(destination.parent, label + ' destination parent')
    flags = os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    source_parent_fd = os.open(source.parent, flags)
    destination_parent_fd = os.open(destination.parent, flags)
    try:
        source_identity = os.stat(source.name, dir_fd=source_parent_fd, follow_symlinks=False)
        source_parent_identity = os.fstat(source_parent_fd)
        destination_parent_identity = os.fstat(destination_parent_fd)
        try:
            os.stat(destination.name, dir_fd=destination_parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Denied(label + ' destination already exists')
        if race_hook:
            race_hook(source, destination)
        # Absolute names are now diagnostic only. Directory descriptors anchor
        # the syscall and prevent a late ancestor substitution from redirecting it.
        current_source_parent = source.parent.lstat()
        current_destination_parent = destination.parent.lstat()
        if ((current_source_parent.st_dev, current_source_parent.st_ino)
                != (source_parent_identity.st_dev, source_parent_identity.st_ino)
                or (current_destination_parent.st_dev, current_destination_parent.st_ino)
                != (destination_parent_identity.st_dev, destination_parent_identity.st_ino)):
            raise Denied(label + ' parent was substituted before descriptor-relative rename')
        current_source = os.stat(source.name, dir_fd=source_parent_fd, follow_symlinks=False)
        if ((current_source.st_dev, current_source.st_ino, stat.S_IFMT(current_source.st_mode))
                != (source_identity.st_dev, source_identity.st_ino,
                    stat.S_IFMT(source_identity.st_mode))):
            raise Denied(label + ' source was substituted before descriptor-relative rename')
        _exclusive_rename_durable(source_parent_fd, source.name,
                                  destination_parent_fd, destination.name)
        moved = os.stat(destination.name, dir_fd=destination_parent_fd, follow_symlinks=False)
        if (moved.st_dev, moved.st_ino) != (source_identity.st_dev, source_identity.st_ino):
            raise Denied(label + ' destination identity mismatch after rename')
        final_source_parent = source.parent.lstat()
        final_destination_parent = destination.parent.lstat()
        if ((final_source_parent.st_dev, final_source_parent.st_ino)
                != (source_parent_identity.st_dev, source_parent_identity.st_ino)
                or (final_destination_parent.st_dev, final_destination_parent.st_ino)
                != (destination_parent_identity.st_dev, destination_parent_identity.st_ino)):
            raise Denied(label + ' parent changed at descriptor-relative syscall boundary')
    finally:
        os.close(destination_parent_fd)
        os.close(source_parent_fd)


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
    observed = paths['binding'].lstat()
    identity = (observed.st_dev, observed.st_ino, stat.S_IFMT(observed.st_mode))
    value = coordination.load_binding(paths['binding'], paths['repo'])
    if stable_file_bytes(paths['binding'], 'state binding') != raw:
        raise Denied('state binding changed during read')
    if value is None or value['status'] != 'moving':
        raise Denied('relocation is not in moving status')
    validate_migration_id(value['migration_id'])
    if Path(value['state_root']) != paths['state_root']:
        raise Denied('moving binding state root mismatch')
    return value, raw, identity


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
        parent_fd = _open_directory_fd(paths['state_root'].parent, 'state-root parent')
        try:
            os.mkdir(paths['state_root'].name, 0o700, dir_fd=parent_fd)
            os.fsync(parent_fd)
        finally:
            os.close(parent_fd)
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
    hooks = race_hooks or {}
    with held_relocation_lock(paths) as (lock_path, _descriptor):
        require_held_lock_path(lock_path, _descriptor)
        revalidate_parents(paths)
        recovery = recover_activation_transaction(paths)
        completed = validate_completed_activation(paths)
        if completed is not None:
            require_held_lock_path(paths['destination_lock'], _descriptor)
            result = verify_layout(paths, completed['binding'])
            require_held_lock_path(paths['destination_lock'], _descriptor)
            if validate_completed_activation(paths) != completed:
                raise Denied('completed activation evidence changed during idempotent resume')
            return dict(result, status='active', already_completed=True,
                        recovered_activation=recovery['status'] == 'active_committed',
                        completion_evidence=completed['completed_path'])
        binding, binding_raw, binding_identity = read_moving(paths)
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
        activate_binding(paths, binding, binding_raw, binding_identity,
                         race_hook=hooks.get('binding_swap'), interleave=interleave)
    return dict(result, status='active', already_completed=False,
                recovered_activation=recovery['status'] != 'none')


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
    binding, binding_raw, _binding_identity = read_moving(paths)
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
        _ensure_recovery_directory(paths)
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
