#!/usr/bin/env python3
"""Project-local Texenda coordination v2. No model launch or external effects.

The sealed v1 scaffold supplies evidence, leases, lifecycle and recovery primitives.
This reviewed adapter replaces only routing, state initialization/checks and migration.
Actor labels and evidence attestations require accountable runtime/reviewer controls.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import ctypes
from decimal import Decimal
import errno
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import re
import secrets
import stat
import subprocess
import sys
import tempfile
import time

PROJECT = Path(__file__).resolve().parents[2]
PACKAGE = PROJECT / 'specs/texenda-handoff'
POLICY = Path(__file__).with_name('routing-policy.json')
BINDING_NAME = '.texenda-location.json'
BINDING_SCHEMA = Path(__file__).with_name('schemas') / 'state-location.schema.json'
BINDING_VERSION = 'texenda.state-location.v1'
STATE_TRANSACTION_SCHEMA = (Path(__file__).with_name('schemas')
                            / 'state-write-transaction.schema.json')
STATE_TRANSACTION_VERSION = 'texenda.state-write-transaction.v1'
STATE_TRANSACTION_PENDING = '.state-write-transaction.json'
STATE_TRANSACTION_TOKEN = re.compile(r'^[0-9a-f]{24}$')
STATE_IDENTITY_FIELDS = {'device', 'inode', 'file_type', 'size', 'mtime_ns',
                         'observed_ctime_ns'}
STATE_TRANSACTION_FIELDS = {
    'schema_version', 'phase', 'token', 'operation', 'state_name', 'candidate_name',
    'repository_root', 'state_root', 'repository_identity', 'state_root_identity',
    'lock_identity', 'binding', 'routing_policy_digest', 'old_state', 'new_state',
}
LEGACY_PATH = PACKAGE / '08-project-harness/harness.py'
LEGACY_DIGEST = '226a4a14b3a795b24354eb90e51a50067fd27fe809423b30b9fa1551f3ce72d6'
if hashlib.sha256(LEGACY_PATH.read_bytes()).hexdigest() != LEGACY_DIGEST:
    raise RuntimeError('sealed harness baseline changed; review the local adapter')
_spec = importlib.util.spec_from_file_location('texenda_sealed_harness_v1', LEGACY_PATH)
legacy = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(legacy)
_plan_spec = importlib.util.spec_from_file_location('texenda_effective_plan', Path(__file__).with_name('plan.py'))
effective_plan = importlib.util.module_from_spec(_plan_spec)
_plan_spec.loader.exec_module(effective_plan)
Denied = legacy.Denied
canonical, digest, file_hash = legacy.canonical, legacy.digest, legacy.file_hash
utc, parse_time = legacy.utc, legacy.parse_time
under, safe_rel, overlap = legacy.under, legacy.safe_rel, legacy.overlap
atomic_write, revision = legacy.atomic_write, legacy.revision

# These are the accepted routing contract, not an observed availability roster.
MODELS = {1: 'gpt-6-astra', 2: 'gpt-5.6-sol', 3: 'gpt-5.6-terra', 4: 'gpt-5.6-luna'}
DOWNSHIFTS = {1: ['high'], 2: ['high'], 3: ['high', 'medium'], 4: ['high', 'medium', 'low']}
CONDITIONS = ['bounded', 'reversible', 'fully_specified', 'deterministic_verification']
QUALIFICATION_FIELDS = {'profile_id', 'capability_tier', 'model_id', 'reasoning_effort',
                        'runtime_id', 'client_version', 'sign_in_mode', 'billing_mode',
                        'capabilities', 'verified_at', 'expires_at', 'qualification_check_ids'}
SAFE_MIGRATION_STATES = {'planned', 'admitted', 'blocked', 'integrated', 'completed', 'cancelled'}
BUDGET_MAX_AGE_SECONDS = 30 * 86400
BUDGET_FIELDS = {'schema_version', 'kind', 'summary', 'checks', 'owner', 'approved_budget_usd',
                 'scope', 'work_packages', 'roles', 'issued_at', 'expires_at',
                 'routing_policy_digest', 'work_package_digest'}
BINDING_FIELDS = {'schema_version', 'migration_id', 'repository_root', 'state_root',
                  'status', 'baseline'}
BINDING_BASELINE_FIELDS = {'state_sha256', 'receipt_count', 'receipt_tip'}
MIGRATION_ID_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')
PLAN_ACTIVATION_SCHEMA = 'tooling/coordination/schemas/plan-activation.schema.json'
PLAN_ENGINE_PATHS = ('tooling/coordination/harness.py', 'tooling/coordination/plan.py',
                     PLAN_ACTIVATION_SCHEMA, 'tooling/coordination/schemas/evidence.schema.json',
                     'tooling/coordination/schemas/state-write-transaction.schema.json',
                     'tooling/coordination/schemas/state-location.schema.json',
                     'tooling/coordination/routing-policy.json')
RUNNING_ENGINE_HASHES = {
    'tooling/coordination/harness.py': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'tooling/coordination/plan.py': hashlib.sha256(Path(__file__).with_name('plan.py').read_bytes()).hexdigest(),
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Denied('duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object)


def amount(value):
    if type(value) not in (int, float):
        raise Denied('development allocation must be a finite number')
    result = Decimal(str(value))
    if not result.is_finite() or not Decimal(0) <= result <= Decimal(100000):
        raise Denied('development allocation must be bounded and nonnegative')
    return result


def resolved_directory(value, label, *, absolute=False, component_symlinks=True):
    """Resolve an existing directory while rejecting lexical and symlink escapes."""
    path = Path(value)
    if absolute and not path.is_absolute():
        raise Denied(label + ' must be absolute')
    if '..' in path.parts:
        raise Denied(label + ' traversal is forbidden')
    candidate = path if path.is_absolute() else Path.cwd() / path
    # Resolve only after proving that no supplied path component is a symlink.
    current = Path(candidate.anchor)
    for part in candidate.parts[1:] if candidate.is_absolute() else candidate.parts:
        current = current / part
        try:
            if current.is_symlink():
                raise Denied(label + ' symlink path is forbidden')
        except OSError as exc:
            raise Denied(label + ' path cannot be inspected') from exc
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise Denied(label + ' directory is missing') from exc
    if not resolved.is_dir():
        raise Denied(label + ' must be a directory')
    if resolved != candidate:
        raise Denied(label + ' must use its canonical path')
    return resolved


def stable_file_bytes(path, label, *, missing_ok=False):
    path = Path(path)
    try:
        resolved_directory(path.parent, label + ' parent', absolute=True)
    except Denied:
        raise
    if path.is_symlink():
        raise Denied(label + ' cannot be a symlink')
    flags = (os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
             | getattr(os, 'O_NONBLOCK', 0))

    def once():
        try:
            descriptor = os.open(path, flags)
        except FileNotFoundError:
            if missing_ok:
                return None
            raise Denied(label + ' is missing')
        except OSError as exc:
            raise Denied(label + ' cannot be opened as a regular file') from exc
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise Denied(label + ' must be a regular non-symlink file')
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
        if (identity != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                         after.st_ctime_ns)
                or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino)):
            raise Denied(label + ' changed during read')
        return b''.join(chunks), identity

    first = once()
    if first is None:
        return None
    second = once()
    if first != second:
        raise Denied(label + ' changed or was replaced during read')
    return first[0]


def load_binding(path, repository_root):
    """Load the ignored, closed state-location descriptor without broadening it."""
    schema = load_json(stable_file_bytes(BINDING_SCHEMA, 'state-location schema'))
    if (schema.get('additionalProperties') is not False
            or set(schema.get('properties', {})) != BINDING_FIELDS):
        raise Denied('state-location binding schema changed; explicit review required')
    raw = stable_file_bytes(path, 'state-location binding', missing_ok=True)
    if raw is None:
        return None
    value = load_json(raw)
    if (not isinstance(value, dict) or set(value) != BINDING_FIELDS
            or value.get('schema_version') != BINDING_VERSION
            or not isinstance(value.get('migration_id'), str)
            or MIGRATION_ID_PATTERN.fullmatch(value['migration_id']) is None
            or value.get('status') not in ('moving', 'active')
            or not isinstance(value.get('baseline'), dict)
            or set(value['baseline']) != BINDING_BASELINE_FIELDS):
        raise Denied('state-location binding violates the closed schema')
    baseline = value['baseline']
    if (not isinstance(baseline['state_sha256'], str) or len(baseline['state_sha256']) != 64
            or any(char not in '0123456789abcdef' for char in baseline['state_sha256'])
            or type(baseline['receipt_count']) is not int or baseline['receipt_count'] < 1
            or not isinstance(baseline['receipt_tip'], str) or len(baseline['receipt_tip']) != 64
            or any(char not in '0123456789abcdef' for char in baseline['receipt_tip'])):
        raise Denied('state-location binding baseline is invalid')
    try:
        recorded_repository = Path(value['repository_root'])
        recorded_state = Path(value['state_root'])
    except TypeError as exc:
        raise Denied('state-location binding paths must be strings') from exc
    if (not recorded_repository.is_absolute() or '..' in recorded_repository.parts
            or not recorded_state.is_absolute() or '..' in recorded_state.parts):
        raise Denied('state-location binding paths must be absolute and traversal-free')
    if recorded_repository != repository_root:
        raise Denied('state-location binding repository mismatch')
    expected_state = repository_root.parent / 'local/agent-state/texenda'
    if recorded_state != expected_state:
        raise Denied('state-location binding differs from the frozen project workspace root')
    return value


def safe_public_rel(value, label):
    rel = safe_rel(value)
    parts = PurePosixPath(rel).parts
    if 'private-inputs' in parts or rel.lower().endswith('.csv'):
        raise Denied(label + ' cannot reference private inputs or CSV')
    return rel


def path_identity(path):
    value = Path(path).lstat()
    return (value.st_dev, value.st_ino, value.st_mode, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns)


def inode_identity(path):
    value = Path(path).lstat()
    return (value.st_dev, value.st_ino, value.st_mode & 0o170000)


def binding_snapshot(path, repository_root):
    raw = stable_file_bytes(path, 'state-location binding', missing_ok=True)
    if raw is None:
        return None, ('absent',)
    value = load_binding(path, repository_root)
    if stable_file_bytes(path, 'state-location binding') != raw:
        raise Denied('state-location binding changed during snapshot')
    recovery = repository_root.parent / 'local/logs/workspace-relocation'
    if recovery.exists() or recovery.is_symlink():
        resolved_directory(recovery, 'state-location recovery directory', absolute=True)
        flags = (os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0)
                 | getattr(os, 'O_NOFOLLOW', 0))
        recovery_fd = os.open(recovery, flags)
        try:
            opened = os.fstat(recovery_fd)
            pending = [name for name in os.listdir(recovery_fd)
                       if name.endswith('.activation-transaction.json')]
            current = recovery.lstat()
            if (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino):
                raise Denied('state-location recovery directory changed during scan')
        finally:
            os.close(recovery_fd)
    else:
        pending = []
    if pending:
        raise Denied('state-location activation transaction is pending recovery')
    return value, (*path_identity(path), hashlib.sha256(raw).hexdigest())


def renameat_state(source_fd, source_name, destination_fd, destination_name, flag):
    libc = ctypes.CDLL(None, use_errno=True)
    source_bytes, destination_bytes = os.fsencode(source_name), os.fsencode(destination_name)
    if sys.platform == 'darwin' and hasattr(libc, 'renameatx_np'):
        operation = libc.renameatx_np
        operation.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                              ctypes.c_char_p, ctypes.c_uint)
        operation.restype = ctypes.c_int
        platform_flag = 0x00000004 if flag == 'exclusive' else 0x00000002
        result = operation(source_fd, source_bytes, destination_fd, destination_bytes,
                           platform_flag)
    elif sys.platform.startswith('linux') and hasattr(libc, 'renameat2'):
        operation = libc.renameat2
        operation.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                              ctypes.c_char_p, ctypes.c_uint)
        operation.restype = ctypes.c_int
        platform_flag = 1 if flag == 'exclusive' else 2
        result = operation(source_fd, source_bytes, destination_fd, destination_bytes,
                           platform_flag)
    else:
        raise Denied('platform lacks descriptor-relative state transaction primitives')
    if result != 0:
        error = ctypes.get_errno()
        if error in (errno.EEXIST, errno.ENOTEMPTY):
            raise Denied('state transaction destination already exists')
        raise OSError(error, os.strerror(error), source_name, destination_name)


def state_identity_record(signature):
    """Closed exact identity observed before a namespace transition."""
    return {
        'device': signature[0],
        'inode': signature[1],
        'file_type': stat.S_IFMT(signature[2]),
        'size': signature[3],
        'mtime_ns': signature[4],
        'observed_ctime_ns': signature[5],
    }


def stat_signature(value):
    return (value.st_dev, value.st_ino, value.st_mode, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns)


def valid_identity_record(value, *, file_type=None):
    return (isinstance(value, dict) and set(value) == STATE_IDENTITY_FIELDS
            and all(type(value[key]) is int and value[key] >= 0
                    for key in STATE_IDENTITY_FIELDS)
            and (file_type is None or value['file_type'] == file_type))


def identity_matches(signature, recorded, *, observed_ctime=False, inode_only=False):
    actual = state_identity_record(signature)
    if inode_only:
        fields = {'device', 'inode', 'file_type'}
    else:
        fields = STATE_IDENTITY_FIELDS if observed_ctime else (
            STATE_IDENTITY_FIELDS - {'observed_ctime_ns'})
    return all(actual[key] == recorded[key] for key in fields)


def stable_at(directory_fd, name, label, *, missing_ok=False):
    """Read a descriptor-relative regular file twice without following aliases."""
    if not isinstance(name, str) or not name or '/' in name or name in ('.', '..'):
        raise Denied(label + ' has an unsafe descriptor-relative name')
    flags = (os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
             | getattr(os, 'O_NONBLOCK', 0))

    def once():
        try:
            descriptor = os.open(name, flags, dir_fd=directory_fd)
        except FileNotFoundError:
            if missing_ok:
                return None
            raise Denied(label + ' is missing')
        except OSError as exc:
            raise Denied(label + ' cannot be opened without following an alias') from exc
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise Denied(label + ' must be a regular non-symlink file')
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
        before_signature = stat_signature(before)
        if (before_signature != stat_signature(after)
                or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino)):
            raise Denied(label + ' changed during anchored read')
        return b''.join(chunks), before_signature

    first = once()
    if first is None:
        return None
    second = once()
    if first != second:
        raise Denied(label + ' changed or was replaced during anchored read')
    return first


def write_at_exclusive(directory_fd, name, raw, label, *, interleave=None):
    if not isinstance(name, str) or not name or '/' in name or name in ('.', '..'):
        raise Denied(label + ' has an unsafe descriptor-relative name')
    staging = 'state-write-staging-' + secrets.token_hex(12) + '.tmp'
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(staging, flags, 0o600, dir_fd=directory_fd)
    try:
        midpoint = max(1, len(raw) // 2)
        for index, chunk in enumerate((raw[:midpoint], raw[midpoint:])):
            offset = 0
            while offset < len(chunk):
                written = os.write(descriptor, chunk[offset:])
                if written <= 0:
                    raise OSError('state-write control staging made no write progress')
                offset += written
            if index == 0 and interleave:
                interleave('state_write_after_control_staging_partial',
                           {'target': name, 'staging': staging})
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        os.fsync(directory_fd)
        renameat_state(directory_fd, staging, directory_fd, name, 'exclusive')
        if interleave:
            interleave('state_write_after_control_publish_before_fsync',
                       {'target': name, 'staging': staging})
        os.fsync(directory_fd)
    except BaseException:
        # An incomplete non-operational staging file never masquerades as a
        # published phase. A published target is always complete and parseable.
        raise
    finally:
        if descriptor is not None:
            os.close(descriptor)


def state_transaction_blocker_names(state_root):
    """Return operational state-write material; archives are non-blocking history."""
    root = Path(state_root)
    if not root.exists() and not root.is_symlink():
        return []
    resolved_directory(root, 'state transaction root', absolute=True)
    flags = os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(root, flags)
    try:
        opened = os.fstat(descriptor)
        names = os.listdir(descriptor)
        blockers = []
        for name in names:
            if name.startswith('.state-write-'):
                blockers.append(name)
        current = root.lstat()
        if (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino):
            raise Denied('state transaction root changed during recovery scan')
        return sorted(blockers)
    finally:
        os.close(descriptor)


def check_receipts(state):
    events = state.get('events')
    if not isinstance(events, list) or not events:
        raise Denied('state must retain its receipt chain')
    previous = '0' * 64
    for sequence, event in enumerate(events, 1):
        body = {key: value for key, value in event.items() if key != 'hash'}
        if (event.get('sequence') != sequence or event.get('previous_hash') != previous
                or digest(body) != event.get('hash')):
            raise Denied('receipt chain corrupt')
        previous = event['hash']
    if events[-1]['state_digest'] != digest({k: v for k, v in state.items() if k != 'events'}):
        raise Denied('state differs from last receipt')


def checkpoint_bytes(path, raw):
    if path.is_symlink():
        raise Denied('checkpoint cannot be a symlink')
    if path.exists():
        if path.read_bytes() != raw:
            raise Denied('existing checkpoint differs; never overwrite')
        return
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def restore_bytes(path, raw):
    """Restore exact validated checkpoint bytes atomically, without reserializing receipts."""
    fd, temporary = tempfile.mkstemp(prefix='.restore-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
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


class Harness(legacy.Harness):
    def __init__(self, root, package=PACKAGE, clock=time.time, policy=POLICY, state_root=None,
                 interleave=None, allow_state_recovery=False):
        repository_root = resolved_directory(root, 'repository root')
        super().__init__(repository_root, Path(package), clock)
        self.sealed_plan = copy.deepcopy(self.plan)
        self.sealed_work = copy.deepcopy(self.work)
        self.effective = None
        self._plan_guards = []
        self._plan_checkpoint_guard = None
        self._active_evidence_task = None
        self._activation_qualification_expiry = None
        self.interleave = interleave
        self.allow_state_recovery = allow_state_recovery
        self.root_identity = inode_identity(self.root)
        self.binding_path = self.root / BINDING_NAME
        self.binding, self.binding_identity = binding_snapshot(self.binding_path, self.root)
        requested_state_root = None
        if state_root is not None:
            raw_state_root = Path(state_root)
            if not raw_state_root.is_absolute() or '..' in raw_state_root.parts:
                raise Denied('state root must be absolute and traversal-free')
            requested_state_root = resolved_directory(raw_state_root, 'state root', absolute=True,
                                                       component_symlinks=True)
            if requested_state_root == self.root or self.root in requested_state_root.parents:
                raise Denied('explicit state root must be external to the repository')
        self.unbound_external = self.binding is None and requested_state_root is not None
        default_root = self.root / '.texenda'
        if self.binding:
            if (self.binding['status'] != 'active'
                    and not (allow_state_recovery and self.binding['status'] == 'moving')):
                raise Denied('state relocation is moving; verified recovery is required')
            if requested_state_root is None:
                raise Denied('bound projects require explicit --state-root')
            bound = Path(self.binding['state_root'])
            if requested_state_root != bound:
                raise Denied('explicit state root does not match the active binding')
            if (default_root / 'state.json').exists() or (default_root / 'state.lock').exists():
                raise Denied('competing default and external state stores are forbidden')
            self.dir = requested_state_root
        elif requested_state_root is not None:
            if (default_root / 'state.json').exists() or (default_root / 'state.lock').exists():
                raise Denied('competing default and explicit state stores are forbidden')
            self.dir = requested_state_root
        else:
            if default_root.is_symlink():
                raise Denied('state directory cannot be a symlink')
            self.dir = default_root
        self.statefile = self.dir / 'state.json'
        self.lockfile = self.dir / 'state.lock'
        self.state_root_identity = inode_identity(self.dir) if self.dir.exists() else None
        if self.statefile.is_symlink() or self.lockfile.is_symlink():
            raise Denied('state files cannot be symlinks')
        if self.lockfile.exists():
            lock_metadata = self.lockfile.lstat()
            if not stat.S_ISREG(lock_metadata.st_mode):
                raise Denied('existing state lock must be a regular non-symlink file')
        blockers = state_transaction_blocker_names(self.dir)
        if blockers and not allow_state_recovery:
            raise Denied('state-write transaction is pending explicit recovery')
        self.policy_path = Path(policy)
        self.policy = load_json(stable_file_bytes(self.policy_path, 'routing policy'))
        self.policy_hash = digest(self.policy)
        evidence_schema = PACKAGE / '08-project-harness/schemas/evidence.schema.json'
        self.evidence_fields = set(load_json(stable_file_bytes(evidence_schema,
                                                               'sealed evidence schema'))['properties'])
        self._validate_policy()

    def _binding_current(self):
        current, identity = binding_snapshot(self.binding_path, self.root)
        if current != self.binding or identity != self.binding_identity:
            raise Denied('state-location binding changed during this session; reload safely')

    def _interleave(self, stage, detail=None):
        if self.interleave:
            self.interleave(stage, self, detail)

    def _validate_state_root_current(self):
        if inode_identity(self.root) != self.root_identity:
            raise Denied('repository root identity changed during this session')
        current = resolved_directory(self.dir, 'state root', absolute=True)
        if current != self.dir:
            raise Denied('state root changed during this session')
        identity = inode_identity(self.dir)
        if self.state_root_identity is None:
            self.state_root_identity = identity
        elif identity != self.state_root_identity:
            raise Denied('state root identity changed during this session')

    def _state_transaction_clear(self):
        if state_transaction_blocker_names(self.dir):
            raise Denied('state-write transaction is pending explicit recovery')

    def _read_state_once(self):
        """Return bytes and an identity signature from one no-follow read."""
        self._validate_state_root_current()
        if self.statefile.is_symlink():
            raise Denied('state file cannot be a symlink')
        flags = (os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
                 | getattr(os, 'O_NONBLOCK', 0))
        try:
            descriptor = os.open(self.statefile, flags)
        except FileNotFoundError as exc:
            raise Denied('run init first') from exc
        except OSError as exc:
            raise Denied('state file cannot be opened as a regular file') from exc
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise Denied('state file must be a regular non-symlink file')
            chunks = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        signature = stat_signature(before)
        after_signature = stat_signature(after)
        if signature != after_signature:
            raise Denied('state changed during read')
        return b''.join(chunks), signature

    def _stable_state_snapshot(self):
        first, first_signature = self._read_state_once()
        second, second_signature = self._read_state_once()
        if first_signature != second_signature or first != second:
            raise Denied('state changed or was replaced during read')
        return first, first_signature

    def _stable_state_bytes(self):
        return self._stable_state_snapshot()[0]

    @contextlib.contextmanager
    def locked(self, *, allow_state_recovery=False):
        """Serialize mutations only; read-only commands never create/open a lock for write."""
        self._binding_current()
        self._interleave('locked_after_initial_binding_check')
        if not allow_state_recovery:
            self._state_transaction_clear()
        if self.unbound_external:
            raise Denied('an unbound explicit state root is read-only')
        self._validate_state_root_current()
        if not self.dir.is_dir():
            raise Denied('state root is missing')
        if self.dir.is_symlink() or self.lockfile.is_symlink() or self.statefile.is_symlink():
            raise Denied('state paths cannot be symlinks')
        directory_flags = os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0)
        root_descriptor = os.open(self.root, directory_flags)
        directory_descriptor = os.open(self.dir, directory_flags)
        self._interleave('before_lock_create')
        descriptor = None
        created = False
        nofollow = getattr(os, 'O_NOFOLLOW', 0)
        nonblock = getattr(os, 'O_NONBLOCK', 0)
        for _attempt in range(3):
            try:
                descriptor = os.open('state.lock', os.O_RDWR | os.O_CREAT | os.O_EXCL
                                     | nofollow | nonblock, 0o600,
                                     dir_fd=directory_descriptor)
                created = True
                break
            except FileExistsError:
                try:
                    descriptor = os.open('state.lock', os.O_RDONLY | nofollow | nonblock,
                                         dir_fd=directory_descriptor)
                    created = False
                    break
                except FileNotFoundError:
                    continue
        if descriptor is None:
            os.close(directory_descriptor)
            os.close(root_descriptor)
            raise Denied('state lock namespace changed repeatedly during acquisition')
        opened_at_creation = os.fstat(descriptor)
        if not stat.S_ISREG(opened_at_creation.st_mode):
            os.close(descriptor)
            os.close(directory_descriptor)
            os.close(root_descriptor)
            raise Denied('opened state lock must be a regular non-symlink file')
        current_lock = os.stat('state.lock', dir_fd=directory_descriptor,
                               follow_symlinks=False)
        if ((opened_at_creation.st_dev, opened_at_creation.st_ino)
                != (current_lock.st_dev, current_lock.st_ino)
                or not stat.S_ISREG(current_lock.st_mode)):
            os.close(descriptor)
            os.close(directory_descriptor)
            os.close(root_descriptor)
            raise Denied('state lock changed during safe open')
        created_identity = ((opened_at_creation.st_dev, opened_at_creation.st_ino,
                             opened_at_creation.st_mode, opened_at_creation.st_size,
                             opened_at_creation.st_mtime_ns, opened_at_creation.st_ctime_ns)
                            if created else None)
        acquired = False
        try:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except BlockingIOError as exc:
                raise Denied('state lock is held by another writer') from exc
            token = {
                'root_fd': root_descriptor,
                'dir_fd': directory_descriptor,
                'lock_fd': descriptor,
                'lock_identity': inode_identity(self.lockfile),
                'lock_created': created,
                'lock_created_identity': created_identity,
                'state_transaction_started': False,
            }
            if allow_state_recovery and created:
                self._cleanup_speculative_lock(token)
                raise Denied('state-write recovery requires the preserved existing lock')
            try:
                self._interleave('locked_after_lock_acquired', token)
                self._continuity(token)
            except BaseException:
                self._cleanup_speculative_lock(token)
                raise
            try:
                yield token
            except BaseException:
                # A lock created by this invocation is still speculative until
                # the mutation commits. Remove only that exact unchanged inode
                # when any later continuity/transaction boundary fails.
                self._cleanup_speculative_lock(token)
                raise
        finally:
            if acquired:
                fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)
            os.close(directory_descriptor)
            os.close(root_descriptor)

    def _cleanup_speculative_lock(self, token):
        if not token['lock_created'] or token.get('state_transaction_started'):
            return
        try:
            current = os.stat('state.lock', dir_fd=token['dir_fd'], follow_symlinks=False)
        except FileNotFoundError:
            return
        opened = os.fstat(token['lock_fd'])
        current_identity = (current.st_dev, current.st_ino, current.st_mode, current.st_size,
                            current.st_mtime_ns, current.st_ctime_ns)
        if (current_identity == token['lock_created_identity']
                and (opened.st_dev, opened.st_ino) == (current.st_dev, current.st_ino)
                and current.st_size == 0):
            os.unlink('state.lock', dir_fd=token['dir_fd'])
            os.fsync(token['dir_fd'])

    def _identity_continuity(self, token):
        self._binding_current()
        self._policy_current()
        self._plan_current()
        self._validate_state_root_current()
        root_now = os.fstat(token['root_fd'])
        dir_now = os.fstat(token['dir_fd'])
        lock_now = os.fstat(token['lock_fd'])
        lock_path = os.stat('state.lock', dir_fd=token['dir_fd'], follow_symlinks=False)
        if ((root_now.st_dev, root_now.st_ino, root_now.st_mode & 0o170000) != self.root_identity
                or (dir_now.st_dev, dir_now.st_ino, dir_now.st_mode & 0o170000)
                != self.state_root_identity
                or (lock_now.st_dev, lock_now.st_ino, lock_now.st_mode & 0o170000)
                != token['lock_identity']
                or (lock_path.st_dev, lock_path.st_ino) != (lock_now.st_dev, lock_now.st_ino)):
            raise Denied('repository/state/lock identity changed during mutation')

    def _continuity(self, token, expected_state=None, expect_state_absent=False):
        self._identity_continuity(token)
        if expect_state_absent:
            try:
                os.stat('state.json', dir_fd=token['dir_fd'], follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise Denied('state appeared before initialization commit')
        if expected_state is not None and self._stable_state_snapshot() != expected_state:
            raise Denied('state changed or was replaced before commit')
        self._interleave('after_final_state_comparison_before_replacement', token)
        # This check is intentionally after the final state comparison so a
        # binding/root/lock/policy change at that exact boundary cannot commit.
        self._identity_continuity(token)

    def _binding_transaction_record(self):
        if self.binding_identity == ('absent',):
            return {'kind': 'absent', 'sha256': None, 'identity': None}
        raw = stable_file_bytes(self.binding_path, 'state-location binding')
        observed = (*path_identity(self.binding_path), hashlib.sha256(raw).hexdigest())
        if observed != self.binding_identity:
            raise Denied('state-location binding changed before state transaction preparation')
        return {
            'kind': 'present',
            'sha256': hashlib.sha256(raw).hexdigest(),
            'identity': state_identity_record(stat_signature(self.binding_path.lstat())),
        }

    def _state_value_record(self, raw, signature):
        return {'sha256': hashlib.sha256(raw).hexdigest(),
                'identity': state_identity_record(signature)}

    def _validate_state_value_record(self, value, label, *, preparing=False):
        if (not isinstance(value, dict) or set(value) != {'sha256', 'identity'}
                or not isinstance(value.get('sha256'), str)
                or re.fullmatch(r'[0-9a-f]{64}', value['sha256']) is None):
            raise Denied(label + ' state transaction value is invalid')
        if preparing:
            if value.get('identity') is not None:
                raise Denied(label + ' preparation identity must not be guessed')
        elif not valid_identity_record(value.get('identity'), file_type=stat.S_IFREG):
            raise Denied(label + ' state transaction identity is invalid')

    def _validate_state_transaction(self, value):
        schema = load_json(stable_file_bytes(STATE_TRANSACTION_SCHEMA,
                                             'state-write transaction schema'))
        if (schema.get('additionalProperties') is not False
                or set(schema.get('required', [])) != STATE_TRANSACTION_FIELDS
                or set(schema.get('properties', {})) != STATE_TRANSACTION_FIELDS):
            raise Denied('state-write transaction schema changed; explicit review required')
        if (not isinstance(value, dict) or set(value) != STATE_TRANSACTION_FIELDS
                or value.get('schema_version') != STATE_TRANSACTION_VERSION
                or value.get('phase') not in ('preparing', 'ready')
                or not isinstance(value.get('token'), str)
                or STATE_TRANSACTION_TOKEN.fullmatch(value['token']) is None
                or value.get('operation') not in ('initialize', 'replace')
                or value.get('state_name') != 'state.json'
                or value.get('candidate_name') != '.state-write-candidate-'
                + value.get('token', '') + '.json'
                or value.get('repository_root') != str(self.root)
                or value.get('state_root') != str(self.dir)
                or value.get('routing_policy_digest') != self.policy_hash
                or not valid_identity_record(value.get('repository_identity'),
                                             file_type=stat.S_IFDIR)
                or not valid_identity_record(value.get('state_root_identity'),
                                             file_type=stat.S_IFDIR)
                or not valid_identity_record(value.get('lock_identity'),
                                             file_type=stat.S_IFREG)):
            raise Denied('state-write transaction violates its closed contract')
        binding = value.get('binding')
        if (not isinstance(binding, dict) or set(binding) != {'kind', 'sha256', 'identity'}
                or binding.get('kind') not in ('absent', 'present')):
            raise Denied('state-write transaction binding identity is invalid')
        if binding['kind'] == 'absent':
            if binding['sha256'] is not None or binding['identity'] is not None:
                raise Denied('absent transaction binding carries an identity')
        elif (not isinstance(binding['sha256'], str)
              or re.fullmatch(r'[0-9a-f]{64}', binding['sha256']) is None
              or not valid_identity_record(binding['identity'], file_type=stat.S_IFREG)):
            raise Denied('present transaction binding identity is invalid')
        self._validate_state_value_record(value.get('new_state'), 'new',
                                          preparing=value['phase'] == 'preparing')
        if value['operation'] == 'initialize':
            if value.get('old_state') is not None:
                raise Denied('initialization transaction cannot claim previous state bytes')
        else:
            self._validate_state_value_record(value.get('old_state'), 'old')
        return value

    def _transaction_environment(self, token, transaction):
        for signature, recorded, label in (
                (stat_signature(os.fstat(token['root_fd'])),
                 transaction['repository_identity'], 'repository'),
                (stat_signature(os.fstat(token['dir_fd'])),
                 transaction['state_root_identity'], 'state root'),
                (stat_signature(os.fstat(token['lock_fd'])),
                 transaction['lock_identity'], 'state lock')):
            if not identity_matches(signature, recorded,
                                    inode_only=label in ('repository', 'state root')):
                raise Denied(label + ' identity differs from state-write transaction')
        if self.policy_hash != transaction['routing_policy_digest']:
            raise Denied('routing policy differs from state-write transaction')
        binding = transaction['binding']
        raw = stable_file_bytes(self.binding_path, 'state-location binding', missing_ok=True)
        if binding['kind'] == 'absent':
            return raw is None
        if raw is None:
            return False
        signature = stat_signature(self.binding_path.lstat())
        return (hashlib.sha256(raw).hexdigest() == binding['sha256']
                and identity_matches(signature, binding['identity']))

    def _transaction_controls(self, directory_fd):
        names = os.listdir(directory_fd)
        sentinel = STATE_TRANSACTION_PENDING in names
        controls = []
        candidates = []
        extras = []
        for name in names:
            if re.fullmatch(r'\.state-write-(?:preparation-capture|candidate-bound|ready|commit-cleanup|rollback-cleanup)-[0-9a-f]{24}\.json', name):
                controls.append(name)
            elif re.fullmatch(r'\.state-write-candidate-[0-9a-f]{24}\.json', name):
                candidates.append(name)
            elif name.startswith('.state-write-') and name != STATE_TRANSACTION_PENDING:
                extras.append(name)
        return sentinel, sorted(controls), sorted(candidates), sorted(extras)

    def _preparation_matches_ready(self, preparation, ready):
        projected = copy.deepcopy(ready)
        projected['phase'] = 'preparing'
        projected['new_state']['identity'] = None
        return projected == preparation

    def _load_state_transaction(self, token):
        sentinel, controls, candidates, extras = self._transaction_controls(token['dir_fd'])
        if not sentinel:
            raise Denied('state-write recovery preparation control is missing')
        if extras:
            raise Denied('state-write recovery material is missing, corrupt, or ambiguous: '
                         'unresolved operational material')
        preparation_raw, _signature = stable_at(
            token['dir_fd'], STATE_TRANSACTION_PENDING,
            'state-write preparation control')
        preparation = self._validate_state_transaction(load_json(preparation_raw))
        if preparation['phase'] != 'preparing':
            raise Denied('fixed state-write control is not a preparation record')
        token_value = preparation['token']
        expected_candidate = preparation['candidate_name']
        if any(name != expected_candidate for name in candidates):
            raise Denied('state-write recovery has ambiguous candidate material')
        if len(controls) > 1:
            raise Denied('state-write recovery has ambiguous phase controls')
        archive_names = [name for name in os.listdir(token['dir_fd'])
                         if name in {
                             'state-write-committed-' + token_value + '.json',
                             'state-write-recovered-' + token_value + '.json',
                         }]
        preparation_capture_archive = ('state-write-preparation-capture-recovered-'
                                       + token_value + '.json')
        capture_archive_exists = preparation_capture_archive in os.listdir(token['dir_fd'])
        if (len(archive_names) > 1 or (controls and archive_names)
                or (controls and capture_archive_exists)
                or (archive_names and capture_archive_exists)):
            raise Denied('state-write recovery has ambiguous archived outcomes')
        if not controls:
            if capture_archive_exists:
                archived_raw, _archived_signature = stable_at(
                    token['dir_fd'], preparation_capture_archive,
                    'archived preparation capture control')
                archived = self._validate_state_transaction(load_json(archived_raw))
                if (archived['phase'] != 'ready'
                        or not self._preparation_matches_ready(preparation, archived)):
                    raise Denied('archived preparation capture differs from preparation')
                return archived, preparation_capture_archive, preparation
            if archive_names:
                archived_raw, _archived_signature = stable_at(
                    token['dir_fd'], archive_names[0], 'archived state-write transaction')
                ready = self._validate_state_transaction(load_json(archived_raw))
                if ready['phase'] != 'ready' or not self._preparation_matches_ready(
                        preparation, ready):
                    raise Denied('archived state-write outcome differs from preparation')
                return ready, archive_names[0], preparation
            return preparation, STATE_TRANSACTION_PENDING, preparation
        control = controls[0]
        raw, _signature = stable_at(token['dir_fd'], control,
                                    'state-write phase control')
        transaction = self._validate_state_transaction(load_json(raw))
        preparation_capture = '.state-write-preparation-capture-' + token_value + '.json'
        if control == preparation_capture:
            if (transaction['phase'] != 'ready'
                    or not self._preparation_matches_ready(preparation, transaction)):
                raise Denied('preparation capture control differs from fixed preparation')
            return transaction, control, preparation
        if transaction['phase'] != 'ready' or not self._preparation_matches_ready(
                preparation, transaction):
            raise Denied('state-write ready record differs from preparation')
        allowed_controls = {
            '.state-write-candidate-bound-' + token_value + '.json',
            '.state-write-ready-' + token_value + '.json',
            '.state-write-commit-cleanup-' + token_value + '.json',
            '.state-write-rollback-cleanup-' + token_value + '.json',
        }
        if control not in allowed_controls:
            raise Denied('state-write recovery control does not match its transaction')
        return transaction, control, preparation

    def _entry(self, token, name, label):
        return stable_at(token['dir_fd'], name, label, missing_ok=True)

    def _entry_matches(self, entry, record):
        return (entry is not None
                and hashlib.sha256(entry[0]).hexdigest() == record['sha256']
                and identity_matches(entry[1], record['identity']))

    def _rename_transaction_entry(self, token, source, destination):
        renameat_state(token['dir_fd'], source, token['dir_fd'], destination, 'exclusive')
        os.fsync(token['dir_fd'])

    def _checkpoint_name(self, transaction, role, expected):
        return ('state-write-checkpoint-' + role + '-' + expected['sha256'] + '-'
                + transaction['token'] + '.json')

    def _checkpoint_names_for_transaction(self, token, transaction):
        suffix = '-' + transaction['token'] + '.json'
        return sorted(name for name in os.listdir(token['dir_fd'])
                      if name.startswith('state-write-checkpoint-')
                      and name.endswith(suffix))

    def _ensure_intended_checkpoint(self, token, transaction, candidate_entry):
        expected = transaction['new_state']
        intended_name = self._checkpoint_name(transaction, 'intended', expected)
        intended = self._entry(token, intended_name, 'intended state checkpoint')
        if intended is None:
            if candidate_entry is None:
                raise Denied('intended state checkpoint and candidate are both missing')
            write_at_exclusive(token['dir_fd'], intended_name, candidate_entry[0],
                               'independent intended state checkpoint')
            intended = self._entry(token, intended_name, 'intended state checkpoint')
        if (intended is None
                or hashlib.sha256(intended[0]).hexdigest() != expected['sha256']
                or not stat.S_ISREG(intended[1][2])):
            raise Denied('intended state checkpoint content is invalid')
        if expected.get('identity') is not None:
            if candidate_entry is None or not identity_matches(
                    candidate_entry[1], expected['identity']):
                raise Denied('candidate identity differs from its bound creation identity')
        if (candidate_entry is not None
                and (candidate_entry[1][0], candidate_entry[1][1])
                == (intended[1][0], intended[1][1])):
            raise Denied('intended checkpoint must not alias the candidate inode')
        return intended_name, intended

    def _capture_transaction_candidate(self, token, transaction, expected, role, label):
        source = transaction['candidate_name']
        destination = self._checkpoint_name(transaction, role, expected)
        source_entry = self._entry(token, source, label)
        checkpoint_entry = self._entry(token, destination, label + ' checkpoint')
        if source_entry is not None and checkpoint_entry is not None:
            raise Denied(label + ' exists at both candidate and checkpoint names')
        if source_entry is not None:
            self._interleave('state_write_before_candidate_capture',
                             {'transaction': transaction, 'role': role,
                              'destination': destination})
            renameat_state(token['dir_fd'], source, token['dir_fd'], destination,
                           'exclusive')
            self._interleave('state_write_after_candidate_capture_before_fsync',
                             {'transaction': transaction, 'role': role,
                              'destination': destination})
            os.fsync(token['dir_fd'])
            checkpoint_entry = self._entry(token, destination, label + ' checkpoint')
        if checkpoint_entry is None:
            raise Denied(label + ' recovery checkpoint is missing')
        matches = hashlib.sha256(checkpoint_entry[0]).hexdigest() == expected['sha256']
        if expected.get('identity') is not None:
            matches = matches and identity_matches(checkpoint_entry[1], expected['identity'])
        if not matches:
            self._record_state_conflict(token, transaction, self._entry(
                token, 'state.json', 'active state during cleanup'), checkpoint_entry)
            raise Denied(label + ' checkpoint differs after atomic capture')
        self._interleave('state_write_after_candidate_capture',
                         {'transaction': transaction, 'role': role,
                          'destination': destination})
        return destination

    def _archive_state_transaction(self, token, control, transaction, outcome):
        destination = 'state-write-' + outcome + '-' + transaction['token'] + '.json'
        if control != destination:
            self._rename_transaction_entry(token, control, destination)
        self._interleave('state_write_after_outcome_archive', transaction)
        preparation_archive = ('state-write-preparation-' + outcome + '-'
                               + transaction['token'] + '.json')
        self._rename_transaction_entry(token, STATE_TRANSACTION_PENDING,
                                       preparation_archive)
        self._interleave('state_write_after_preparation_archive', transaction)
        return destination

    def _begin_rollback_cleanup(self, token, control, transaction):
        rollback = '.state-write-rollback-cleanup-' + transaction['token'] + '.json'
        if control != rollback:
            self._rename_transaction_entry(token, control, rollback)
        self._interleave('state_write_after_rollback_cleanup_marker', transaction)
        return rollback

    def _finish_rollback_cleanup(self, token, control, transaction):
        state_entry = self._entry(token, 'state.json', 'restored state')
        old = transaction['old_state']
        if transaction['operation'] == 'initialize':
            if state_entry is not None:
                raise Denied('initialization rollback did not restore state absence')
        elif not self._entry_matches(state_entry, old):
            raise Denied('rollback did not restore the exact previous state')
        self._capture_transaction_candidate(token, transaction, transaction['new_state'],
                                            'attempted', 'rolled-back new state')
        self._interleave('state_write_after_recovery_candidate_cleanup', transaction)
        archived = self._archive_state_transaction(token, control, transaction, 'recovered')
        self._interleave('state_write_after_recovery_archive', transaction)
        token['state_transaction_started'] = False
        return {
            'recovered': True,
            'outcome': 'previous_state_restored',
            'previous_state_sha256': old['sha256'] if old else None,
            'attempted_state_sha256': transaction['new_state']['sha256'],
            'receipt_bytes_rewritten': False,
            'transaction_archive': str(self.dir / archived),
        }

    def _finish_commit_cleanup(self, token, control, transaction):
        self._plan_current()
        state_entry = self._entry(token, 'state.json', 'committed state')
        if not self._entry_matches(state_entry, transaction['new_state']):
            raise Denied('commit cleanup cannot validate the exact new state')
        candidate = self._entry(token, transaction['candidate_name'],
                                'displaced previous state')
        if transaction['operation'] == 'replace':
            self._capture_transaction_candidate(token, transaction,
                                                transaction['old_state'], 'previous',
                                                'displaced previous state')
        elif candidate is not None:
            raise Denied('initialization commit has unexpected candidate material')
        self._interleave('state_write_after_commit_candidate_cleanup', transaction)
        self._plan_current()
        archived = self._archive_state_transaction(token, control, transaction, 'committed')
        self._interleave('state_write_after_commit_archive', transaction)
        token['state_transaction_started'] = False
        return {
            'recovered': True,
            'outcome': 'durable_commit_cleanup_completed',
            'previous_state_sha256': (transaction['old_state']['sha256']
                                      if transaction['old_state'] else None),
            'attempted_state_sha256': transaction['new_state']['sha256'],
            'receipt_bytes_rewritten': False,
            'transaction_archive': str(self.dir / archived),
        }

    def _record_state_conflict(self, token, transaction, state_entry, candidate_entry):
        name = '.state-write-conflict-' + transaction['token'] + '.json'
        value = {
            'schema_version': 'texenda.state-write-conflict.v1',
            'token': transaction['token'],
            'reason': 'displaced_state_differs_from_prepared_previous_state',
            'observed_state_sha256': (hashlib.sha256(state_entry[0]).hexdigest()
                                      if state_entry else None),
            'observed_candidate_sha256': (hashlib.sha256(candidate_entry[0]).hexdigest()
                                          if candidate_entry else None),
        }
        raw = json.dumps(value, indent=2, sort_keys=True, allow_nan=False).encode() + b'\n'
        try:
            write_at_exclusive(token['dir_fd'], name, raw, 'state-write conflict record')
        except (FileExistsError, OSError, Denied):
            pass

    def _recover_state_write_transaction(self, token, *, prefer_previous=True):
        transaction, control, preparation = self._load_state_transaction(token)
        token['state_transaction_started'] = True
        binding_same = self._transaction_environment(token, transaction)
        state_entry = self._entry(token, 'state.json', 'active state')
        candidate_entry = self._entry(token, transaction['candidate_name'],
                                      'state transaction candidate')
        old, new = transaction['old_state'], transaction['new_state']
        rollback_control = '.state-write-rollback-cleanup-' + transaction['token'] + '.json'
        commit_control = '.state-write-commit-cleanup-' + transaction['token'] + '.json'

        capture_control = ('.state-write-preparation-capture-'
                           + transaction['token'] + '.json')
        capture_archive = ('state-write-preparation-capture-recovered-'
                           + transaction['token'] + '.json')
        if transaction['phase'] == 'preparing' or control in (capture_control,
                                                               capture_archive):
            previous_old = preparation['old_state']
            previous_layout = ((preparation['operation'] == 'initialize'
                                and state_entry is None)
                               or (preparation['operation'] == 'replace'
                                   and self._entry_matches(state_entry, previous_old)))
            if not previous_layout or not binding_same:
                raise Denied('state-write preparation environment changed before recovery')
            expected_checkpoint = self._checkpoint_name(
                preparation, 'attempted', preparation['new_state'])
            intended_checkpoint = self._checkpoint_name(
                preparation, 'intended', preparation['new_state'])
            checkpoints = self._checkpoint_names_for_transaction(token, preparation)
            allowed_checkpoints = {expected_checkpoint, intended_checkpoint}
            if any(name not in allowed_checkpoints for name in checkpoints):
                raise Denied('preparation recovery has duplicate or unexpected checkpoints')
            if control == STATE_TRANSACTION_PENDING and candidate_entry is not None:
                self._ensure_intended_checkpoint(token, preparation, candidate_entry)
                checkpoints = self._checkpoint_names_for_transaction(token, preparation)
                if checkpoints != [intended_checkpoint]:
                    raise Denied('preparation intended-checkpoint set is not exact')
                capture_transaction = copy.deepcopy(preparation)
                capture_transaction['phase'] = 'ready'
                capture_transaction['new_state']['identity'] = state_identity_record(
                    candidate_entry[1])
                self._validate_state_transaction(capture_transaction)
                capture_raw = json.dumps(
                    capture_transaction, indent=2, sort_keys=True,
                    ensure_ascii=False, allow_nan=False).encode() + b'\n'
                write_at_exclusive(token['dir_fd'], capture_control, capture_raw,
                                   'preparation capture control',
                                   interleave=self._interleave)
                transaction = capture_transaction
                new = transaction['new_state']
                control = capture_control
            if control in (capture_control, capture_archive):
                if transaction['phase'] != 'ready':
                    raise Denied('preparation capture lacks a bound candidate identity')
                candidate_entry = self._entry(token, transaction['candidate_name'],
                                              'state transaction candidate')
                if candidate_entry is not None:
                    self._ensure_intended_checkpoint(token, transaction, candidate_entry)
                checkpoints = self._checkpoint_names_for_transaction(token, transaction)
                if (candidate_entry is None
                        and checkpoints != sorted([expected_checkpoint,
                                                  intended_checkpoint])):
                    raise Denied('captured preparation checkpoint is missing')
                self._capture_transaction_candidate(token, transaction, new, 'attempted',
                                                    'incomplete prepared state')
                checkpoints = self._checkpoint_names_for_transaction(token, transaction)
                if checkpoints != sorted([expected_checkpoint, intended_checkpoint]):
                    raise Denied('captured preparation checkpoint set is not exact')
                checkpoint = self._entry(token, expected_checkpoint,
                                         'captured preparation checkpoint')
                intended = self._entry(token, intended_checkpoint,
                                       'intended preparation checkpoint')
                if (checkpoint is None
                        or hashlib.sha256(checkpoint[0]).hexdigest() != new['sha256']
                        or not stat.S_ISREG(checkpoint[1][2])
                        or intended is None
                        or hashlib.sha256(intended[0]).hexdigest() != new['sha256']
                        or not stat.S_ISREG(intended[1][2])
                        or not identity_matches(checkpoint[1], new['identity'])
                        or (checkpoint[1][0], checkpoint[1][1])
                        == (intended[1][0], intended[1][1])):
                    raise Denied('captured preparation checkpoint is corrupt')
                if control == capture_control:
                    self._rename_transaction_entry(token, capture_control, capture_archive)
            elif checkpoints:
                raise Denied('preparation checkpoint exists without capture control')
            archive = ('state-write-preparation-recovered-' + transaction['token']
                       + '.json')
            self._rename_transaction_entry(token, STATE_TRANSACTION_PENDING, archive)
            token['state_transaction_started'] = False
            return {
                'recovered': True,
                'outcome': 'previous_state_restored',
                'previous_state_sha256': (previous_old['sha256']
                                          if previous_old else None),
                'attempted_state_sha256': preparation['new_state']['sha256'],
                'receipt_bytes_rewritten': False,
                'transaction_archive': str(self.dir / archive),
            }

        if control == 'state-write-recovered-' + transaction['token'] + '.json':
            return self._finish_rollback_cleanup(token, control, transaction)
        if control == 'state-write-committed-' + transaction['token'] + '.json':
            return self._finish_commit_cleanup(token, control, transaction)

        if control == rollback_control:
            return self._finish_rollback_cleanup(token, control, transaction)

        if transaction['operation'] == 'initialize':
            previous_layout = state_entry is None and self._entry_matches(candidate_entry, new)
            exchanged_layout = (self._entry_matches(state_entry, new)
                                and candidate_entry is None)
            if previous_layout:
                rollback = self._begin_rollback_cleanup(token, control, transaction)
                return self._finish_rollback_cleanup(token, rollback, transaction)
            if exchanged_layout and (prefer_previous or control != commit_control
                                     or not binding_same):
                renameat_state(token['dir_fd'], 'state.json', token['dir_fd'],
                               transaction['candidate_name'], 'exclusive')
                self._interleave('state_write_after_rollback_exchange_before_fsync', transaction)
                os.fsync(token['dir_fd'])
                self._interleave('state_write_after_rollback_durable', transaction)
                rollback = self._begin_rollback_cleanup(token, control, transaction)
                return self._finish_rollback_cleanup(token, rollback, transaction)
            if exchanged_layout and control == commit_control and binding_same:
                return self._finish_commit_cleanup(token, control, transaction)
            raise Denied('initialization recovery material is missing, corrupt, or ambiguous')

        previous_layout = (self._entry_matches(state_entry, old)
                           and self._entry_matches(candidate_entry, new))
        exchanged_layout = (self._entry_matches(state_entry, new)
                            and self._entry_matches(candidate_entry, old))
        previous_checkpoint_name = self._checkpoint_name(
            transaction, 'previous', old)
        previous_checkpoint = self._entry(token, previous_checkpoint_name,
                                          'preserved previous-state checkpoint')
        checkpoint_rollback_layout = (
            self._entry_matches(state_entry, old) and candidate_entry is None
            and self._entry_matches(previous_checkpoint, new))
        if checkpoint_rollback_layout:
            renameat_state(token['dir_fd'], previous_checkpoint_name, token['dir_fd'],
                           transaction['candidate_name'], 'exclusive')
            self._interleave('state_write_after_checkpoint_rollback_restore_before_fsync',
                             transaction)
            os.fsync(token['dir_fd'])
            candidate_entry = self._entry(token, transaction['candidate_name'],
                                          'checkpoint-restored attempted state')
            if not self._entry_matches(candidate_entry, new):
                raise Denied('checkpoint-backed rollback candidate could not be restored')
            rollback = self._begin_rollback_cleanup(token, control, transaction)
            return self._finish_rollback_cleanup(token, rollback, transaction)
        if previous_layout:
            rollback = self._begin_rollback_cleanup(token, control, transaction)
            return self._finish_rollback_cleanup(token, rollback, transaction)
        if exchanged_layout and (prefer_previous or control != commit_control
                                 or not binding_same):
            renameat_state(token['dir_fd'], 'state.json', token['dir_fd'],
                           transaction['candidate_name'], 'exchange')
            self._interleave('state_write_after_rollback_exchange_before_fsync', transaction)
            os.fsync(token['dir_fd'])
            self._interleave('state_write_after_rollback_durable', transaction)
            restored = self._entry(token, 'state.json', 'restored previous state')
            attempted = self._entry(token, transaction['candidate_name'],
                                    'rolled-back attempted state')
            if (not self._entry_matches(restored, old)
                    or not self._entry_matches(attempted, new)):
                raise Denied('state-write rollback exchange could not be validated')
            rollback = self._begin_rollback_cleanup(token, control, transaction)
            return self._finish_rollback_cleanup(token, rollback, transaction)
        if (control == commit_control and prefer_previous
                and self._entry_matches(state_entry, new) and candidate_entry is None
                and self._entry_matches(previous_checkpoint, old)):
            renameat_state(token['dir_fd'], 'state.json', token['dir_fd'],
                           previous_checkpoint_name, 'exchange')
            self._interleave('state_write_after_rollback_exchange_before_fsync', transaction)
            os.fsync(token['dir_fd'])
            self._interleave('state_write_after_checkpoint_rollback_exchange_fsync',
                             transaction)
            renameat_state(token['dir_fd'], previous_checkpoint_name, token['dir_fd'],
                           transaction['candidate_name'], 'exclusive')
            os.fsync(token['dir_fd'])
            restored = self._entry(token, 'state.json', 'restored previous state')
            attempted = self._entry(token, transaction['candidate_name'],
                                    'rolled-back attempted state')
            if (not self._entry_matches(restored, old)
                    or not self._entry_matches(attempted, new)):
                raise Denied('checkpoint-backed state rollback could not be validated')
            rollback = self._begin_rollback_cleanup(token, control, transaction)
            return self._finish_rollback_cleanup(token, rollback, transaction)
        if control == commit_control and binding_same:
            # Forward cleanup is allowed only when recovery was explicitly invoked
            # for a previously archived commit decision.
            if self._entry_matches(state_entry, new) and candidate_entry is None:
                return self._finish_commit_cleanup(token, control, transaction)
        raise Denied('state-write recovery material is missing, corrupt, or ambiguous')

    def _atomic_state_bytes(self, token, raw, *, expected_state=None,
                            expect_state_absent=False):
        transaction_token = secrets.token_hex(12)
        temporary = '.state-write-candidate-' + transaction_token + '.json'
        transaction_started = False
        preserve_conflict = False
        try:
            old_record = None
            if expected_state is not None:
                current = stable_at(token['dir_fd'], 'state.json', 'previous state')
                if current[0] != expected_state[0] or current[1] != expected_state[1]:
                    raise Denied('previous state identity changed before transaction preparation')
                old_record = self._state_value_record(*current)
            preparation = {
                'schema_version': STATE_TRANSACTION_VERSION,
                'phase': 'preparing',
                'token': transaction_token,
                'operation': 'replace' if expected_state is not None else 'initialize',
                'state_name': 'state.json',
                'candidate_name': temporary,
                'repository_root': str(self.root),
                'state_root': str(self.dir),
                'repository_identity': state_identity_record(
                    stat_signature(os.fstat(token['root_fd']))),
                'state_root_identity': state_identity_record(
                    stat_signature(os.fstat(token['dir_fd']))),
                'lock_identity': state_identity_record(
                    stat_signature(os.fstat(token['lock_fd']))),
                'binding': self._binding_transaction_record(),
                'routing_policy_digest': self.policy_hash,
                'old_state': old_record,
                'new_state': {
                    'sha256': hashlib.sha256(raw).hexdigest(),
                    'identity': None,
                },
            }
            self._validate_state_transaction(preparation)
            preparation_raw = json.dumps(preparation, indent=2, sort_keys=True,
                                         ensure_ascii=False, allow_nan=False).encode() + b'\n'
            write_at_exclusive(token['dir_fd'], STATE_TRANSACTION_PENDING,
                               preparation_raw, 'state-write preparation control',
                               interleave=self._interleave)
            transaction_started = True
            token['state_transaction_started'] = True
            self._interleave('state_write_after_preparation_control', preparation)

            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0)
            descriptor = os.open(temporary, flags, 0o600, dir_fd=token['dir_fd'])
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(raw)
                stream.flush()
                self._interleave('state_write_before_candidate_file_fsync', preparation)
                os.fsync(stream.fileno())
                created_candidate_signature = stat_signature(os.fstat(stream.fileno()))
            candidate_before_checkpoint = stable_at(
                token['dir_fd'], temporary, 'originally created state candidate')
            preparation_with_identity = copy.deepcopy(preparation)
            preparation_with_identity['new_state']['identity'] = state_identity_record(
                created_candidate_signature)
            self._ensure_intended_checkpoint(token, preparation_with_identity,
                                             candidate_before_checkpoint)
            candidate_record = {
                'sha256': preparation['new_state']['sha256'],
                'identity': state_identity_record(created_candidate_signature),
            }
            transaction = copy.deepcopy(preparation)
            transaction['phase'] = 'ready'
            transaction['new_state'] = candidate_record
            self._validate_state_transaction(transaction)
            transaction_raw = json.dumps(transaction, indent=2, sort_keys=True,
                                         ensure_ascii=False, allow_nan=False).encode() + b'\n'
            candidate_bound_control = ('.state-write-candidate-bound-'
                                       + transaction_token + '.json')
            write_at_exclusive(token['dir_fd'], candidate_bound_control,
                               transaction_raw, 'state-write candidate identity control',
                               interleave=self._interleave)
            self._interleave('state_write_after_candidate_file_fsync', preparation)
            os.fsync(token['dir_fd'])
            self._interleave('state_write_after_candidate_directory_fsync', preparation)
            candidate_entry = stable_at(token['dir_fd'], temporary,
                                        'new state transaction candidate')
            if (candidate_entry[0] != raw
                    or hashlib.sha256(candidate_entry[0]).hexdigest()
                    != preparation['new_state']['sha256']
                    or not identity_matches(candidate_entry[1], state_identity_record(
                        created_candidate_signature))):
                raise Denied('new state candidate differs from the originally created bytes/inode')
            ready_control = '.state-write-ready-' + transaction_token + '.json'
            self._rename_transaction_entry(token, candidate_bound_control, ready_control)
            self._interleave('state_write_after_transaction_prepared', transaction)
            self._interleave('before_state_commit', token)
            self._continuity(token, expected_state, expect_state_absent)
            if not self._transaction_environment(token, transaction):
                raise Denied('state-location binding differs at state exchange boundary')
            self._interleave('state_write_before_exchange', transaction)
            candidate_entry = self._entry(token, temporary,
                                          'candidate at state exchange boundary')
            if (candidate_entry is None or candidate_entry[0] != raw
                    or hashlib.sha256(candidate_entry[0]).hexdigest()
                    != preparation['new_state']['sha256']
                    or not identity_matches(candidate_entry[1],
                                            candidate_record['identity'])):
                raise Denied('new state candidate changed immediately before exchange')
            if expected_state is None:
                renameat_state(token['dir_fd'], temporary, token['dir_fd'],
                               'state.json', 'exclusive')
            else:
                renameat_state(token['dir_fd'], temporary, token['dir_fd'],
                               'state.json', 'exchange')
            self._interleave('state_write_after_exchange_before_fsync', transaction)
            os.fsync(token['dir_fd'])
            self._interleave('state_write_after_exchange_fsync', transaction)
            state_entry = self._entry(token, 'state.json', 'new active state')
            displaced_entry = self._entry(token, temporary, 'displaced previous state')
            if not self._entry_matches(state_entry, transaction['new_state']):
                preserve_conflict = True
                self._record_state_conflict(token, transaction, state_entry, displaced_entry)
                raise Denied('new state identity differs after atomic exchange')
            if expected_state is not None and not self._entry_matches(displaced_entry, old_record):
                # The syscall displaced a different valid/invalid inode than the
                # prepared old state. Restore it atomically and retain both it and
                # the attempted new ledger under the still-pending transaction.
                try:
                    renameat_state(token['dir_fd'], temporary, token['dir_fd'],
                                   'state.json', 'exchange')
                    os.fsync(token['dir_fd'])
                    state_entry = self._entry(token, 'state.json', 'restored competing state')
                    displaced_entry = self._entry(token, temporary,
                                                  'preserved attempted state')
                finally:
                    preserve_conflict = True
                    self._record_state_conflict(token, transaction,
                                                state_entry, displaced_entry)
                raise Denied('atomic exchange displaced a state other than the prepared previous state')
            if expected_state is None and displaced_entry is not None:
                preserve_conflict = True
                self._record_state_conflict(token, transaction, state_entry, displaced_entry)
                raise Denied('initialization exchange produced unexpected displaced material')
            self._interleave('state_write_after_displaced_validation', transaction)
            self._interleave('after_state_replacement_before_validation', token)
            self._identity_continuity(token)
            if not self._transaction_environment(token, transaction):
                raise Denied('state-location binding differs after state exchange')
            commit_control = '.state-write-commit-cleanup-' + transaction_token + '.json'
            self._rename_transaction_entry(token, ready_control, commit_control)
            self._interleave('state_write_after_commit_cleanup_marker', transaction)
            self._finish_commit_cleanup(token, commit_control, transaction)
        except BaseException as original_error:
            sentinel, _controls, _candidates, _extras = self._transaction_controls(
                token['dir_fd'])
            transaction_started = transaction_started or sentinel
            token['state_transaction_started'] = transaction_started
            if transaction_started and not preserve_conflict:
                try:
                    self._recover_state_write_transaction(token, prefer_previous=True)
                except BaseException as recovery_error:
                    raise Denied(
                        'state write failed and recovery could not be proved; all recovery material is retained'
                    ) from recovery_error
            raise original_error
        else:
            token['state_transaction_started'] = False

    def recover_state_write(self, actor, runtime_stopped=False):
        if (not isinstance(actor, str) or not actor.startswith('human:')
                or runtime_stopped is not True):
            raise Denied('state-write recovery requires owner authority and runtime-stop attestation')
        blockers = state_transaction_blocker_names(self.dir)
        if not blockers:
            raise Denied('no state-write transaction requires recovery')
        with self.locked(allow_state_recovery=True) as token:
            result = self._recover_state_write_transaction(token, prefer_previous=True)
        return result

    def _atomic_state_json(self, token, value, **continuity):
        raw = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False).encode() + b'\n'
        self._atomic_state_bytes(token, raw, **continuity)

    def _validate_policy(self):
        p = self.policy
        if p.get('schema_version') != '2.0' or p.get('work_package_digest') != self.package_hash:
            raise Denied('routing policy format or work-package baseline mismatch')
        if (p.get('qualification_max_age_days') != 30
                or p.get('new_api_spend_authorized_usd') != 0
                or p.get('default_max_concurrent_writers') != 2
                or p.get('never_silently_substitute') is not True
                or p.get('downshift_conditions') != CONDITIONS
                or p.get('escalation_order') != ['effort', 'capability']):
            raise Denied('routing safety contract changed; explicit amendment required')
        rows = p.get('capability_tiers', [])
        if any(type(row.get('tier')) is not int for row in rows):
            raise Denied('capability tiers must be integers')
        self.tiers = {row['tier']: row for row in rows}
        if len(rows) != 4 or set(self.tiers) != set(MODELS):
            raise Denied('exactly four unique capability tiers required')
        rows = p.get('profiles', [])
        self.profiles = {row['profile_id']: row for row in rows}
        if len(rows) != len(self.profiles):
            raise Denied('duplicate profile_id')
        expected_ids = set()
        for tier, model in MODELS.items():
            row = self.tiers[tier]
            default = model + '-max'
            downshifts = [model + '-' + effort for effort in DOWNSHIFTS[tier]]
            fallback = ['gpt-5.6-sol-max'] if tier == 1 else []
            if (row.get('id') != 'T' + str(tier) or row.get('model_id') != model
                    or row.get('default_profile_id') != default
                    or row.get('downshift_profile_ids') != downshifts
                    or row.get('fallback_profile_ids') != fallback):
                raise Denied('capability model/default/downshift/fallback contract mismatch')
            for effort in ['max'] + DOWNSHIFTS[tier]:
                pid = model + '-' + effort
                expected_ids.add(pid)
                profile = self.profiles.get(pid, {})
                if (set(profile) != {'profile_id', 'capability_tier', 'model_id', 'reasoning_effort', 'default'}
                        or type(profile.get('capability_tier')) is not int
                        or profile.get('capability_tier') != tier or profile.get('model_id') != model
                        or profile.get('reasoning_effort') != effort
                        or profile.get('default') is not (effort == 'max')):
                    raise Denied('profile effort/model/default contract mismatch')
            defaults = [r for r in rows if r.get('capability_tier') == tier and r.get('default') is True]
            if len(defaults) != 1:
                raise Denied('exactly one default profile per capability tier required')
        if set(self.profiles) != expected_ids:
            raise Denied('unknown or disallowed effort profile')
        rows = p.get('work_package_routes', [])
        self.routes = {row['work_package_id']: row for row in rows}
        if len(rows) != len(self.routes) or set(self.routes) != set(self.work):
            raise Denied('exactly one author/reviewer route required for every work package')
        for wid, row in self.routes.items():
            if not row.get('rationale'):
                raise Denied('route rationale required')
            for role in ('author', 'reviewer'):
                route = row[role]
                floor = route.get('capability_floor')
                if type(floor) is not int or floor not in self.tiers:
                    raise Denied('invalid capability floor')
                if route.get('default_profile_id') != self.tiers[floor]['default_profile_id']:
                    raise Denied('WP default must use its capability floor at max')
                efforts, ids = route.get('allowed_reasoning_efforts'), route.get('allowed_profile_ids')
                if (not isinstance(efforts, list) or not efforts or len(set(efforts)) != len(efforts)
                        or 'max' not in efforts or any(e not in ('max', 'high', 'medium', 'low') for e in efforts)
                        or not isinstance(ids, list) or len(set(ids)) != len(ids)
                        or route['default_profile_id'] not in ids):
                    raise Denied('explicit unique WP allowed efforts/profiles required')
                for pid in ids:
                    profile = self.profiles.get(pid)
                    if (not profile or profile['reasoning_effort'] not in efforts
                            or (profile['capability_tier'] > floor and pid != 'gpt-5.6-sol-max')):
                        raise Denied('WP allowed profile exceeds its capability/effort contract')
            if (self.work[wid].get('risk_level') in ('high', 'critical')
                    and row['reviewer']['capability_floor'] != 1):
                raise Denied('high/critical work retains independent T1 review')
            if (self.work[wid].get('recommended_model_tier') == 1
                    and row['author']['capability_floor'] != 1):
                raise Denied('existing architecture/qualification author floor remains T1')

    def _policy_current(self):
        if digest(load_json(stable_file_bytes(self.policy_path, 'routing policy'))) != self.policy_hash:
            raise Denied('routing policy changed during this session; reload and explicitly migrate state')

    def evidence(self, rel, kind=None, task=None, candidate=None, require_pass=False):
        """Retain v1 lifecycle envelopes; new routing metadata uses the local v2 schema."""
        safe = safe_public_rel(rel, 'coordination evidence')
        path = under(self.root, safe)
        envelope_raw = stable_file_bytes(path, 'coordination evidence')
        envelope = load_json(envelope_raw)
        if not isinstance(envelope, dict) or envelope.get('schema_version') not in ('1.0', '2.0', '2.1'):
            raise Denied('invalid evidence envelope')
        fields = self.evidence_fields
        if envelope['schema_version'] in ('2.0', '2.1'):
            fields = fields | {'routing_policy_digest', 'profile_id', 'role', 'capability_tier',
                               'work_package_digest', 'fence', 'rationale', 'reasoning_demand',
                               'owner', 'approved_budget_usd', 'issued_at', 'roles', *CONDITIONS}
        if envelope['schema_version'] == '2.1':
            fields = fields | {'effective_plan_digest'}
        if (self._active_evidence_task is not None and task == self._active_evidence_task
                and kind in ('submission', 'review', 'integration', 'checkpoint', 'recovery', 'trigger')
                and (envelope['schema_version'] != '2.1'
                     or envelope.get('effective_plan_digest') != self.effective.digest)):
            raise Denied('future lifecycle evidence must bind the active effective plan')
        if envelope['schema_version'] == '2.1':
            if (not isinstance(envelope.get('effective_plan_digest'), str)
                    or re.fullmatch(r'[0-9a-f]{64}', envelope['effective_plan_digest']) is None
                    or any(key in envelope and type(envelope[key]) is not bool
                           for key in ('runtime_stopped', 'conflict_resolution_changed_semantics'))):
                raise Denied('version-2.1 evidence requires an exact digest and boolean stop/merge flags')
        if set(envelope) - fields:
            raise Denied('unknown evidence fields; use the local v2 schema for routing metadata')
        if kind and envelope.get('kind') != kind:
            raise Denied('wrong evidence kind')
        if task and envelope.get('task_id') != task:
            raise Denied('evidence task mismatch')
        if candidate and envelope.get('candidate_revision') != candidate:
            raise Denied('evidence candidate mismatch')
        if not isinstance(envelope.get('summary'), str) or not envelope['summary'].strip():
            raise Denied('evidence summary required')
        checks = envelope.get('checks', [])
        if not isinstance(checks, list):
            raise Denied('checks must be a list')
        ids = set()
        for check in checks:
            if not isinstance(check, dict) or not check.get('id') or check['id'] in ids:
                raise Denied('invalid/duplicate evidence check')
            ids.add(check['id'])
            if check.get('status') not in ('PASS', 'FAIL', 'NOT_RUN', 'NOT_APPLICABLE'):
                raise Denied('invalid check status')
            if not isinstance(check.get('required'), bool):
                raise Denied('check required flag must be boolean')
            if check['status'] in ('PASS', 'FAIL'):
                log_rel = safe_public_rel(check.get('evidence_path', ''), 'evidence check log')
                log = under(self.root, log_rel)
                log_raw = stable_file_bytes(log, 'evidence check log')
                if hashlib.sha256(log_raw).hexdigest() != check.get('sha256'):
                    raise Denied('test log hash mismatch')
                if not check.get('command_or_procedure'):
                    raise Denied('test command/procedure required')
        if require_pass:
            required = [check for check in checks if check['required']]
            if not required or any(check['status'] != 'PASS' for check in required):
                raise Denied('all required checks must have PASS evidence; NOT RUN cannot pass')
        return {'path': safe, 'sha256': hashlib.sha256(envelope_raw).hexdigest()}, envelope

    def _check(self, state):
        self._policy_current()
        if (state.get('version') not in ('2.0', '2.1')
                or state.get('work_package_digest') != self.package_hash
                or state.get('routing_policy_digest') != self.policy_hash):
            raise Denied('state format/baseline/policy changed; use the explicit reviewed migration')
        if set(state.get('tasks', {})) != set(self.work):
            raise Denied('state task catalog mismatch')
        check_receipts(state)
        boundaries = [event for event in state['events'] if event['operation'] == 'migrate-routing-v1-to-v2']
        migration = state.get('routing_migration')
        if migration or boundaries:
            if (not migration or len(boundaries) != 1 or boundaries[0].get('migration') != migration
                    or boundaries[0]['sequence'] != migration['source_receipt_count'] + 1
                    or boundaries[0]['previous_hash'] != migration['source_receipt_head']
                    or migration['policy_digest'] != self.policy_hash):
                raise Denied('migration boundary proof missing or inconsistent')
        if state['version'] == '2.1':
            self._check_plan_state(state)
        else:
            if ('effective_plan_digest' in state or 'plan_activation' in state
                    or any(event['operation'] == 'activate-plan' for event in state['events'])):
                raise Denied('base state contains an unactivated effective-plan binding')
            self.plan, self.work = self.sealed_plan, self.sealed_work
            self.effective = None

    def _check_binding_baseline(self, state, raw):
        if not self.binding:
            return
        baseline = self.binding['baseline']
        if len(state['events']) < baseline['receipt_count']:
            raise Denied('bound receipt chain is shorter than its baseline')
        if state['events'][baseline['receipt_count'] - 1]['hash'] != baseline['receipt_tip']:
            raise Denied('bound receipt prefix differs from its baseline')
        if (len(state['events']) == baseline['receipt_count']
                and hashlib.sha256(raw).hexdigest() != baseline['state_sha256']):
            raise Denied('bound state bytes differ at unchanged receipt count')

    def _read(self):
        self._binding_current()
        self._state_transaction_clear()
        raw = self._stable_state_bytes()
        state = load_json(raw)
        self._check(state)
        self._check_binding_baseline(state, raw)
        self._state_transaction_clear()
        self._binding_current()
        return state

    def init(self, actor='human:owner'):
        self._binding_current()
        if self.binding:
            raise Denied('default or external initialization is denied after state binding')
        if self.unbound_external:
            raise Denied('unbound explicit state roots are read-only and cannot be initialized')
        if not self.dir.is_dir():
            if self.dir == self.root / '.texenda':
                self.dir.mkdir(mode=0o700)
            else:
                raise Denied('explicit state root must exist before init')
        with self.locked() as token:
            self._policy_current()
            if self.statefile.exists():
                raise Denied('state already exists; never overwrite to resume')
            state = {
                'version': '2.0', 'package_version': self.plan['package_version'],
                'work_package_digest': self.package_hash, 'routing_policy_digest': self.policy_hash,
                'budget_usd': 0.0, 'budget_approval': None,
                'max_concurrent_writers': 2, 'roster': [], 'gates': {}, 'events': [],
                'tasks': {wid: {
                    'state': 'planned', 'fence': 0, 'lease': None, 'assignment': None,
                    'candidate': None, 'submission': None, 'review': None,
                    'integration': None, 'checkpoint': None, 'trigger': None, 'history': []
                } for wid in self.work},
            }
            self._event(state, actor, 'init')
            self._atomic_state_json(token, state, expect_state_absent=True)
        return {'initialized': str(self.statefile), 'version': '2.0',
                'tasks': len(self.work), 'routing_policy_digest': self.policy_hash, 'models_verified': False}

    def _validate_qualification(self, q, envelope):
        # Stored snapshots add only the evidence reference; roster rows must be closed.
        if set(q) - {'evidence'} != QUALIFICATION_FIELDS or type(q.get('capability_tier')) is not int:
            raise Denied('qualification requires the closed exact-profile field set')
        pid = q.get('profile_id')
        if pid not in self.profiles:
            raise Denied('unknown profile_id; an allowed effort still needs exact qualification')
        profile = self.profiles[pid]
        for key in ('model_id', 'capability_tier', 'reasoning_effort'):
            if q.get(key) != profile[key]:
                raise Denied('qualification does not match the exact profile: ' + key)
        for key in ('runtime_id', 'client_version', 'sign_in_mode', 'billing_mode'):
            if not isinstance(q.get(key), str) or not q[key].strip():
                raise Denied('missing runtime qualification ' + key)
        if q['billing_mode'] not in ('subscription', 'api'):
            raise Denied('unknown billing mode')
        capabilities = q.get('capabilities')
        if (not isinstance(capabilities, list) or not all(isinstance(c, str) for c in capabilities)
                or len(set(capabilities)) != len(capabilities)
                or not {'read', 'edit', 'test'}.issubset(capabilities)):
            raise Denied('read/edit/test qualification required for this coding profile')
        verified, expires = parse_time(q.get('verified_at')), parse_time(q.get('expires_at'))
        if verified > self.clock() + 60 or expires <= self.clock() or expires <= verified:
            raise Denied('qualification stale/future')
        if expires - verified > self.policy['qualification_max_age_days'] * 86400:
            raise Denied('qualification valid at most 30 days')
        ids = q.get('qualification_check_ids')
        checks = {check['id']: check for check in envelope['checks']}
        if (not isinstance(ids, list) or not ids or not all(isinstance(i, str) for i in ids)
                or len(ids) != len(set(ids))):
            raise Denied('exact profile qualification check IDs required')
        if any(i not in checks or checks[i]['required'] is not True or checks[i]['status'] != 'PASS' for i in ids):
            raise Denied('profile qualification requires named required PASS evidence')

    def roster(self, actor, record):
        if not actor.startswith('human:'):
            raise Denied('owner must attest actual runtime qualification')

        def apply(state):
            ref, envelope = self.evidence(record, 'roster', require_pass=True)
            if envelope['schema_version'] != '2.0' or envelope.get('routing_policy_digest') != self.policy_hash:
                raise Denied('roster must attest the current routing policy digest')
            qualifications = envelope.get('qualifications', [])
            if not isinstance(qualifications, list) or not qualifications:
                raise Denied('no qualified profiles')
            seen = set()
            for q in qualifications:
                if set(q) != QUALIFICATION_FIELDS:
                    raise Denied('roster qualification has missing/unknown fields')
                self._validate_qualification(q, envelope)
                if q['profile_id'] in seen:
                    raise Denied('one qualification per exact profile_id; duplicate profile')
                seen.add(q['profile_id'])
            state['roster'] = [dict(q, evidence=ref) for q in qualifications]

        return self.change(actor, 'set-roster', apply)

    def qualified(self, state, profile_id, human=False):
        if human:
            return None
        rows = [q for q in state['roster'] if q['profile_id'] == profile_id]
        if len(rows) != 1:
            raise Denied('exact profile not runtime-qualified: ' + str(profile_id))
        q = rows[0]
        envelope = self.recheck(q['evidence'], kind='roster', require_pass=True)
        if envelope.get('routing_policy_digest') != self.policy_hash:
            raise Denied('qualification policy is stale')
        self._validate_qualification(q, envelope)
        recorded = {key: value for key, value in q.items() if key != 'evidence'}
        if [row for row in envelope.get('qualifications', []) if row.get('profile_id') == profile_id] != [recorded]:
            raise Denied('qualification differs from attested exact profile')
        return q

    def _downshift(self, wid, role, tier, profile_id, record, fence, candidate=None):
        if self.effective:
            raise Denied('effective-plan work requires max effort until a separately reviewed effective-bound attestation schema exists')
        if not record:
            raise Denied('lower effort requires bounded/reversible/fully specified deterministic routing evidence')
        ref, envelope = self.evidence(record, 'routing', wid, candidate, require_pass=True)
        if (envelope['schema_version'] != '2.0'
                or envelope.get('role') != role or envelope.get('profile_id') != profile_id
                or type(envelope.get('capability_tier')) is not int
                or type(envelope.get('fence')) is not int
                or envelope.get('capability_tier') != tier
                or envelope.get('work_package_digest') != self.package_hash
                or envelope.get('fence') != fence
                or envelope.get('routing_policy_digest') != self.policy_hash
                or not isinstance(envelope.get('rationale'), str) or not envelope['rationale'].strip()
                or envelope.get('reasoning_demand') not in ('bounded', 'mechanical')
                or any(envelope.get(key) is not True for key in CONDITIONS)):
            raise Denied('downshift evidence must bind this task, role, policy, profile and all four conditions')
        expiry = parse_time(envelope.get('expires_at'))
        if not self.clock() < expiry <= self.clock() + 30 * 86400:
            raise Denied('routing attestation expired or exceeds 30 days')
        return ref

    def _select(self, state, wid, role, tier, human, profile_id, fallback, fallback_reason,
                routing_record, candidate=None):
        floor = self.routes[wid][role]['capability_floor']
        tier = floor if tier is None else tier
        if type(tier) is not int or tier not in self.tiers or tier > floor:
            raise Denied('capability below work-package ' + role + ' floor; reviewed decomposition required')
        if human:
            if profile_id or fallback or fallback_reason or routing_record:
                raise Denied('human work must not claim a model profile or fallback')
            return {'tier': tier, 'capability_floor': floor, 'human': True, 'profile_id': None, 'model': None,
                    'reasoning_effort': None, 'runtime': None, 'qualification': None,
                    'fallback': False, 'fallback_reason': None, 'downshift_evidence': None,
                    'routing_policy_digest': self.policy_hash,
                    **({'effective_plan_digest': self.effective.digest} if self.effective else {})}
        pid = profile_id or self.tiers[tier]['default_profile_id']
        profile = self.profiles.get(pid)
        if not profile:
            raise Denied('unknown or disallowed effort profile')
        route = self.routes[wid][role]
        if pid not in route['allowed_profile_ids'] or profile['reasoning_effort'] not in route['allowed_reasoning_efforts']:
            raise Denied('exact profile/effort not allowed for this work-package role')
        # An explicitly named stronger profile is permitted; no automatic model choice occurs.
        tier = min(tier, profile['capability_tier'])
        is_fallback = pid in self.tiers[tier]['fallback_profile_ids']
        if is_fallback:
            if fallback is not True or not isinstance(fallback_reason, str) or not fallback_reason.strip():
                raise Denied('T1 fallback requires explicit selection and a recorded reason; never silent')
        elif fallback or fallback_reason or profile['capability_tier'] != tier:
            raise Denied('profile does not satisfy the selected capability; invalid fallback')
        q = self.qualified(state, pid)
        downshift = None
        if profile['reasoning_effort'] != 'max':
            task = state['tasks'][wid]
            fence = task['fence'] + (1 if role == 'author' and task['state'] == 'admitted' else 0)
            downshift = self._downshift(wid, role, tier, pid, routing_record, fence, candidate)
        elif routing_record:
            raise Denied('routing downshift record is only for lower effort')
        return {'tier': tier, 'capability_floor': floor, 'human': False, 'profile_id': pid, 'model': profile['model_id'],
                'reasoning_effort': profile['reasoning_effort'], 'runtime': q['runtime_id'],
                'qualification': copy.deepcopy(q), 'fallback': is_fallback,
                'fallback_reason': fallback_reason if is_fallback else None,
                'downshift_evidence': downshift, 'routing_policy_digest': self.policy_hash,
                **({'effective_plan_digest': self.effective.digest} if self.effective else {})}

    def _recheck_binding(self, state, wid, role, binding, candidate=None):
        if self.effective and role == 'author' and binding.get('context_digest') != self._context_binding(wid):
            raise Denied('assigned effective-plan context is stale')
        ref = binding.get('downshift_evidence')
        actual = self._select(
            state, wid, role, binding['tier'], binding['human'], binding['profile_id'],
            binding['fallback'], binding['fallback_reason'], ref['path'] if ref else None, candidate,
        )
        if any(binding.get(key) != value for key, value in actual.items()):
            raise Denied('assigned exact profile/runtime/evidence changed; recover and assign a new fence')

    def _declared_spend(self, state):
        used = Decimal(0)
        for task in state['tasks'].values():
            for bundle in [task, *task['history']]:
                records = [bundle.get('assignment'), bundle.get('review'), *bundle.get('review_history', [])]
                for record in records:
                    if record:
                        allocated = amount(record.get('budget_usd', 0))
                        if (record.get('qualification') or {}).get('billing_mode') == 'api' and allocated <= 0:
                            raise Denied('retained API work lacks a positive allocation; reviewed accounting repair required')
                        used += allocated
        return used

    def _budget_authorization(self, envelope, approved_usd, wid=None, role=None, owner=None):
        if (envelope.get('schema_version') != '2.0' or envelope.get('kind') != 'budget'
                or set(envelope) - {'notes'} != BUDGET_FIELDS):
            raise Denied('paid v2 work requires a closed version-2 budget authorization')
        if amount(envelope['approved_budget_usd']) != amount(approved_usd):
            raise Denied('budget authorization amount differs from the exact approved USD')
        principal = envelope['owner']
        if (not isinstance(principal, str) or not principal.startswith('human:')
                or not principal[6:].strip() or (owner is not None and principal != owner)):
            raise Denied('budget authorization must bind the accountable owner')
        if not isinstance(envelope['scope'], str) or not envelope['scope'].strip():
            raise Denied('nonempty budget scope required')
        if (envelope['work_package_digest'] != self.package_hash
                or envelope['routing_policy_digest'] != self.policy_hash):
            raise Denied('budget authorization baseline/policy mismatch')
        wps, roles = envelope['work_packages'], envelope['roles']
        if (not isinstance(wps, list) or not wps or not all(isinstance(w, str) for w in wps)
                or len(set(wps)) != len(wps) or not set(wps).issubset(self.work)
                or not isinstance(roles, list) or not roles or not all(isinstance(r, str) for r in roles)
                or len(set(roles)) != len(roles) or not set(roles).issubset({'author', 'reviewer'})
                or (wid is not None and wid not in wps) or (role is not None and role not in roles)):
            raise Denied('budget authorization does not cover the exact task/role scope')
        issued, expires = parse_time(envelope['issued_at']), parse_time(envelope['expires_at'])
        if not 0 < expires - issued <= BUDGET_MAX_AGE_SECONDS:
            raise Denied('budget validity must be positive and at most 30 days')
        if not issued <= self.clock() < expires:
            raise Denied('budget authorization not yet valid or expired')
        check_fields = {'id', 'required', 'status', 'command_or_procedure', 'evidence_path', 'sha256'}
        if ('notes' in envelope and not isinstance(envelope['notes'], str)):
            raise Denied('budget notes must be text')
        if any(set(check) - check_fields or not isinstance(check['id'], str) or not check['id'].strip()
               or any(key in check and not isinstance(check[key], str)
                      for key in ('command_or_procedure', 'evidence_path', 'sha256'))
               for check in envelope['checks']):
            raise Denied('unknown budget evidence check fields')
        return envelope

    def _legacy_allocation(self, state, wid, role, fence, record):
        if type(fence) is not int:
            raise Denied('legacy allocation requires its exact integer task fence')
        migration = state.get('routing_migration') or {}
        authorization = migration.get('legacy_budget_authorization') or {}
        matches = [entry for entry in authorization.get('allocations', [])
                   if entry.get('work_package_id') == wid and entry.get('role') == role
                   and type(entry.get('fence')) is int and entry['fence'] == fence
                   and entry.get('record_digest') == digest(record)]
        if len(matches) != 1 or 'budget_approval' in record:
            raise Denied('allocation is not an exact retained v1 record; fresh v2 authorization required')
        raw = under(self.root, migration.get('backup_path', '')).read_bytes()
        if hashlib.sha256(raw).hexdigest() != migration.get('source_sha256'):
            raise Denied('legacy budget source checkpoint hash mismatch')
        source = load_json(raw)
        legacy.Harness._check(self, source)
        check_receipts(source)
        if (source.get('budget_approval') != authorization.get('evidence')
                or amount(source['budget_usd']) != amount(authorization.get('approved_budget_usd'))):
            raise Denied('legacy budget authority differs from the migration source')
        entry = matches[0]
        path = entry.get('source_path', [])
        if path[:2] != ['tasks', wid]:
            raise Denied('legacy allocation source task mismatch')
        original = source
        for part in path:
            original = original[part]
        if original != record or amount(entry['budget_usd']) != amount(record['budget_usd']):
            raise Denied('legacy allocation differs from its preserved source record')
        if amount(record['budget_usd']) > amount(authorization['approved_budget_usd']):
            raise Denied('legacy allocation exceeds its retained authorization')
        evidence = self.recheck(authorization.get('evidence'), kind='budget', require_pass=True)
        if evidence['schema_version'] != '1.0':
            raise Denied('legacy budget compatibility requires its original v1 evidence')
        # This is historical proof for an already retained allocation, never a new grant.

    def _recheck_allocation(self, state, wid, role, fence, record):
        allocated = amount(record.get('budget_usd', 0))
        if (record.get('qualification') or {}).get('billing_mode') == 'api' and allocated <= 0:
            raise Denied('API work requires a positive owner-authorized allocation')
        if allocated:
            if 'budget_approval' not in record:
                self._legacy_allocation(state, wid, role, fence, record)
                return
            evidence = self.recheck(record['budget_approval'], kind='budget', require_pass=True)
            approved = record.get('budget_approved_usd')
            self._budget_authorization(evidence, approved, wid, role)
            if allocated > amount(approved):
                raise Denied('allocation exceeds its exact approved budget')

    def _allocate(self, state, wid, role, binding, budget_usd, max_tokens, max_seconds):
        requested, approved = amount(budget_usd), amount(state['budget_usd'])
        if self.effective and (requested or (binding.get('qualification') or {}).get('billing_mode') == 'api'):
            raise Denied('new paid work requires a separately reviewed effective-bound budget schema')
        if (type(max_tokens) is not int or not 0 < max_tokens <= 1000000
                or type(max_seconds) is not int or not 0 < max_seconds <= 28800):
            raise Denied('invalid task budget or bounds')
        if self._declared_spend(state) + requested > approved:
            raise Denied('development allowance exhausted; owner must increase')
        allocation = {'budget_usd': budget_usd, 'max_tokens': max_tokens, 'max_seconds': max_seconds,
                      'budget_approval': copy.deepcopy(state['budget_approval']) if requested else None,
                      'budget_approved_usd': state['budget_usd'] if requested else None}
        # Always use the current exact v2 record for new allocations. No legacy fallback.
        self._recheck_allocation(state, wid, role, None, dict(binding, **allocation))
        return allocation

    def budget(self, actor, usd, record):
        if not actor.startswith('human:'):
            raise Denied('bounded owner-approved development budget required')
        approved = amount(usd)

        def apply(state):
            if self.effective:
                raise Denied('effective-plan activation preserves historic budget; new authority needs a reviewed effective-bound schema')
            ref, envelope = self.evidence(record, 'budget', require_pass=True)
            self._budget_authorization(envelope, usd, owner=actor)
            if approved < self._declared_spend(state):
                raise Denied('budget cannot be reduced below retained author/reviewer allocations')
            state.update(budget_usd=usd, budget_approval=ref)
        return self.change(actor, 'set-budget', apply)

    def change(self, actor, op, fn, task=None):
        def guarded(state):
            if self.effective and task is not None and op != 'admit':
                current = self.task(state, task)
                if current.get('effective_plan_digest') != self.effective.digest:
                    raise Denied('task has no current effective-plan admission; historical work is immutable')
            if op in ('record-integration', 'complete'):
                current = self.task(state, task)
                if self._declared_spend(state) > amount(state['budget_usd']):
                    raise Denied('retained allocations exceed the owner development allowance')
                for role, record in (('author', current.get('assignment')), ('reviewer', current.get('review'))):
                    if record:
                        self._recheck_allocation(state, task, role, current['fence'], record)
            self._active_evidence_task = task if self.effective else None
            try:
                result = fn(state)
            finally:
                self._active_evidence_task = None
            if self.effective and task is not None:
                self.task(state, task)['effective_plan_digest'] = self.effective.digest
            return result
        with self.locked() as token:
            source_snapshot = self._stable_state_snapshot()
            source = source_snapshot[0]
            state = load_json(source)
            self._check(state)
            self._check_binding_baseline(state, source)
            updated = copy.deepcopy(state)
            result = guarded(updated)
            self._event(updated, actor, op, task)
            self._atomic_state_json(token, updated, expected_state=source_snapshot)
            return result

    def _event(self, state, actor, op, task=None):
        super()._event(state, actor, op, task)
        if state.get('version') == '2.1':
            event = state['events'][-1]
            event['effective_plan_digest'] = state['effective_plan_digest']
            event['hash'] = digest({key: value for key, value in event.items() if key != 'hash'})

    def admit(self, wid, actor, trigger=None, *, plan_digest=None):
        def apply(state):
            task = self.task(state, wid, 'planned')
            if self.effective and plan_digest != self.effective.digest:
                raise Denied('admission requires the current effective-plan digest from bound context')
            if any(state['tasks'][dep]['state'] != 'completed' for dep in self.work[wid]['dependencies']):
                raise Denied('incomplete prerequisites')
            if self.work[wid]['activation'] == 'DEFER UNTIL TRIGGERED':
                if not trigger:
                    raise Denied('deferred work needs observed trigger evidence')
                ref, _envelope = self.evidence(trigger, 'trigger', wid, require_pass=True)
                task['trigger'] = ref
            task['state'] = 'admitted'
        return self.change(actor, 'admit', apply, wid)

    def assign(self, wid, actor, agent, tier=None, human=False, budget_usd=0,
               max_tokens=50000, max_seconds=3600, *, profile_id=None, fallback=False,
               fallback_reason=None, routing_record=None, plan_digest=None, context_digest=None):
        def apply(state):
            task = self.task(state, wid, 'admitted')
            if self.effective and (plan_digest != self.effective.digest or context_digest != self._context_binding(wid)):
                raise Denied('assignment requires current plan/context digests; unbound or stale context is invalid')
            if human != agent.startswith('human:'):
                raise Denied('explicit human assignment must match human: principal')
            binding = self._select(state, wid, 'author', tier, human, profile_id,
                                   fallback, fallback_reason, routing_record)
            allocation = self._allocate(state, wid, 'author', binding, budget_usd, max_tokens, max_seconds)
            if sum(bool(t['lease']) for t in state['tasks'].values()) >= state['max_concurrent_writers']:
                raise Denied('writer concurrency limit reached')
            paths = [safe_rel(path) for path in self.work[wid]['allowed_paths']]
            for other, previous in state['tasks'].items():
                if other != wid and previous['lease']:
                    if any(overlap(path, old) for path in paths for old in previous['lease']['paths']):
                        raise Denied('edit lease conflicts with ' + other + '; expired leases require proved recovery')
            task['fence'] += 1
            task['lease'] = {'paths': paths, 'owner': agent,
                             'expires_at': self.clock() + max_seconds, 'fence': task['fence']}
            task['assignment'] = dict(binding, agent=agent, **allocation)
            if self.effective:
                task['assignment']['context_digest'] = context_digest
            task['state'] = 'assigned'
            return dict(binding, task=wid, fence=task['fence'], paths=paths)
        return self.change(actor, 'assign', apply, wid)

    def start(self, wid, actor, fence):
        def apply(state):
            task = self.task(state, wid, 'assigned')
            self.owned(task, actor, fence)
            self._recheck_binding(state, wid, 'author', task['assignment'])
            self._recheck_allocation(state, wid, 'author', task['fence'], task['assignment'])
            task['state'] = 'running'
        return self.change(actor, 'start', apply, wid)

    def review(self, wid, actor, tier, candidate, record, approve=True, human=False, *,
               profile_id=None, fallback=False, fallback_reason=None, routing_record=None,
               budget_usd=0, max_tokens=50000, max_seconds=3600):
        candidate = revision(candidate)

        def apply(state):
            task = self.task(state, wid, 'submitted')
            if task['candidate'] != candidate:
                raise Denied('stale review candidate')
            if actor == task['assignment']['agent']:
                raise Denied('author cannot independently review own work')
            if human != actor.startswith('human:'):
                raise Denied('human review flag/principal mismatch')
            self._recheck_binding(state, wid, 'author', task['assignment'])
            self._recheck_allocation(state, wid, 'author', task['fence'], task['assignment'])
            binding = self._select(state, wid, 'reviewer', tier, human, profile_id,
                                   fallback, fallback_reason, routing_record, candidate)
            allocation = self._allocate(state, wid, 'reviewer', binding, budget_usd, max_tokens, max_seconds)
            self.recheck(task['submission'], kind='submission', task=wid,
                         candidate=candidate, require_pass=approve)
            ref, envelope = self.evidence(record, 'review', wid, candidate, require_pass=approve)
            if not human and (envelope['schema_version'] not in ('2.0', '2.1')
                              or envelope.get('profile_id') != binding['profile_id']
                              or envelope.get('routing_policy_digest') != self.policy_hash):
                raise Denied('review evidence must bind the exact reviewer profile and policy')
            task['review'] = dict(binding, actor=actor, candidate=candidate, evidence=ref,
                                  approved=approve, fence=task['fence'], **allocation)
            task['state'] = 'reviewed' if approve else 'running'
            if not approve:
                task.setdefault('review_history', []).append(task['review'])
                task['review'] = None
                task['integration'] = None
        return self.change(actor, 'approve-review' if approve else 'request-changes', apply, wid)

    def recover(self, wid, actor, record, cancel=False):
        def apply(state):
            task = self.task(state, wid)
            if task['state'] in ('completed', 'cancelled', 'planned'):
                raise Denied('cannot recover terminal or never-admitted task')
            ref, evidence = self.evidence(record, 'recovery', wid, require_pass=True)
            if (evidence.get('runtime_stopped') is not True
                    or type(evidence.get('previous_fence')) is not int
                    or evidence['previous_fence'] != task['fence']):
                raise Denied('recovery requires current fence and actual runtime-stop evidence')
            revision(evidence.get('observed_revision', ''))
            for role, allocation in (('author', task.get('assignment')), ('reviewer', task.get('review'))):
                if allocation and amount(allocation.get('budget_usd', 0)) and 'budget_approval' not in allocation:
                    self._legacy_allocation(state, wid, role, task['fence'], allocation)
            task['history'].append({key: task.get(key) for key in
                                    ('candidate', 'assignment', 'submission', 'review', 'integration', 'checkpoint', 'fence')}
                                   | {'review_history': task.get('review_history', []), 'recovery': ref})
            task.update(state='cancelled' if cancel else 'admitted', lease=None, assignment=None,
                        candidate=None, submission=None, review=None, integration=None, review_history=[])
            task['fence'] += 1
        return self.change(actor, 'cancel' if cancel else 'recover', apply, wid)

    def _load_effective(self):
        try:
            plan = effective_plan.load_plan(self.root)
            if self.package_hash != plan.contract['sealed_catalog_sha256']:
                raise Denied('effective plan requires the exact sealed catalog')
            for path, expected in RUNNING_ENGINE_HASHES.items():
                if hashlib.sha256(effective_plan.read_source(self.root, path)).hexdigest() != expected:
                    raise Denied('executing coordinator differs from repository source: ' + path)
            return plan
        except effective_plan.PlanError as exc:
            raise Denied(str(exc)) from exc

    def _plan_source_refs(self, plan):
        refs = copy.deepcopy(plan.source_refs)
        for path in PLAN_ENGINE_PATHS:
            raw = effective_plan.read_source(self.root, path)
            refs.append({'path': path, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
        return refs

    def _plan_current(self):
        if self._activation_qualification_expiry is not None and self.clock() >= self._activation_qualification_expiry:
            raise Denied('activation reviewer qualification expired before commit')
        for ref in self._plan_guards:
            raw = effective_plan.read_source(self.root, ref['path'])
            if hashlib.sha256(raw).hexdigest() != ref['sha256']:
                raise Denied('effective-plan source/evidence changed during operation: ' + ref['path'])
        if self._plan_checkpoint_guard:
            name, expected = self._plan_checkpoint_guard
            raw = stable_file_bytes(self.dir / name, 'effective-plan preactivation checkpoint')
            if hashlib.sha256(raw).hexdigest() != expected:
                raise Denied('effective-plan preactivation checkpoint changed')

    def _source_evidence_guards(self, state):
        """Pin retained state evidence and its logs through the replacement boundary."""
        refs = {}
        def collect(value):
            if isinstance(value, dict):
                if set(value) == {'path', 'sha256'}:
                    path = safe_public_rel(value['path'], 'retained state evidence')
                    if path in refs and refs[path]['sha256'] != value['sha256']:
                        raise Denied('retained evidence has competing hashes: ' + path)
                    refs[path] = dict(value)
                else:
                    for child in value.values():
                        collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)
        collect(state)
        guards = list(refs.values())
        for ref in list(guards):
            envelope = self.recheck(ref)
            for check in envelope['checks']:
                if check['status'] in ('PASS', 'FAIL'):
                    guards.append({'path': safe_public_rel(check['evidence_path'], 'retained evidence log'),
                                   'sha256': check['sha256']})
        return guards

    def _plan_evidence(self, record, actor, source, plan, source_refs, *, fresh):
        safe = safe_public_rel(record, 'plan activation evidence')
        raw = stable_file_bytes(under(self.root, safe), 'plan activation evidence')
        envelope = load_json(raw)
        schema = load_json(effective_plan.read_source(self.root, PLAN_ACTIVATION_SCHEMA))
        try:
            effective_plan.validate_schema(envelope, schema)
        except effective_plan.PlanError as exc:
            raise Denied(str(exc)) from exc
        if (envelope['actor'] != actor or envelope['reviewer'] in envelope['authors']
                or envelope['reviewer'] == actor
                or envelope['effective_plan_digest'] != plan.digest
                or envelope['source_refs'] != source_refs
                or envelope['source_state_sha256'] != hashlib.sha256(source).hexdigest()):
            raise Denied('activation requires exact independent review of sources, state and plan')
        old = load_json(source)
        if (envelope['source_receipt_count'] != len(old['events'])
                or envelope['source_receipt_head'] != old['events'][-1]['hash']):
            raise Denied('activation review receipt boundary is stale')
        candidate = revision(envelope['candidate_revision'])
        command = ['git', '-C', str(self.root)]
        env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
        tree = subprocess.run([*command, 'rev-parse', candidate + '^{tree}'], env=env,
                              check=True, capture_output=True, text=True).stdout.strip()
        if tree != envelope['candidate_tree']:
            raise Denied('activation candidate tree mismatch')
        for ref in source_refs:
            committed = subprocess.run([*command, 'show', candidate + ':' + ref['path']],
                                       env=env, check=True, capture_output=True).stdout
            if hashlib.sha256(committed).hexdigest() != ref['sha256']:
                raise Denied('reviewed candidate source differs: ' + ref['path'])
        checks, ids = envelope['checks'], set()
        required = [check for check in checks if check['required']]
        if not required or any(check['status'] != 'PASS' for check in required):
            raise Denied('activation requires independent PASS checks and runtime-stop evidence')
        guards = [{'path': safe, 'sha256': hashlib.sha256(raw).hexdigest()}]
        for check in checks:
            if check['id'] in ids:
                raise Denied('duplicate activation check')
            ids.add(check['id'])
            if check['status'] in ('PASS', 'FAIL'):
                path = safe_public_rel(check.get('evidence_path', ''), 'activation check log')
                log = stable_file_bytes(under(self.root, path), 'activation check log')
                if not check.get('command_or_procedure') or hashlib.sha256(log).hexdigest() != check.get('sha256'):
                    raise Denied('activation evidence log mismatch')
                guards.append({'path': path, 'sha256': check['sha256']})
        if not {'independent-review', 'runtime-stop'} <= {check['id'] for check in required}:
            raise Denied('activation needs named independent-review and runtime-stop PASS checks')
        if fresh:
            q = self.qualified(old, envelope['reviewer_profile_id'])
            if digest(q) != envelope['reviewer_qualification_digest']:
                raise Denied('activation reviewer exact qualification mismatch')
            self._activation_qualification_expiry = parse_time(q['expires_at'])
        self._plan_guards = copy.deepcopy(source_refs) + guards + self._source_evidence_guards(old)
        self._plan_current()
        return guards[0], envelope

    def _safe_plan_source(self, state, plan):
        for wid, task in state['tasks'].items():
            if task.get('lease') is not None:
                raise Denied('plan activation refuses every lease, including expired: ' + wid)
            if task.get('state') not in ('planned', 'completed', 'cancelled'):
                raise Denied('plan activation refuses unfinished/uncertain work: ' + wid)
            if wid in plan.changed_work_packages and task['state'] != 'planned':
                raise Denied('changed scope must still be planned: ' + wid)
            if task['state'] == 'planned':
                if (task.get('fence') != 0 or task.get('history')
                        or any(task.get(key) is not None for key in ('assignment', 'candidate', 'submission',
                               'review', 'integration', 'checkpoint', 'trigger'))):
                    raise Denied('planned task contains prior or unfinished work: ' + wid)
            elif task['state'] == 'completed':
                if not task.get('integration') or not task.get('assignment') or not task.get('review'):
                    raise Denied('completed task lacks integration/runtime-stop chain: ' + wid)
            elif any(task.get(key) is not None for key in ('assignment', 'candidate', 'submission', 'review', 'integration')):
                raise Denied('cancelled task contains unfinished work: ' + wid)
        self._validate_retained_evidence(state)

    def _check_plan_state(self, state):
        plan = self._load_effective()
        refs = self._plan_source_refs(plan)
        meta = state.get('plan_activation')
        fields = {'from_version', 'effective_plan_digest', 'source_refs', 'source_sha256',
                  'source_receipt_count', 'source_receipt_head', 'checkpoint_name',
                  'evidence', 'actor', 'reviewer', 'candidate_revision', 'candidate_tree',
                  'reviewer_qualification_digest', 'owner_request'}
        if (not isinstance(meta, dict) or set(meta) != fields or meta['from_version'] != '2.0'
                or state.get('effective_plan_digest') != plan.digest
                or meta['effective_plan_digest'] != plan.digest or meta['source_refs'] != refs
                or type(meta['source_receipt_count']) is not int or meta['source_receipt_count'] < 1
                or re.fullmatch(r'[0-9a-f]{64}', meta['source_sha256']) is None
                or meta['checkpoint_name'] != 'state.plan-v2.' + meta['source_sha256'] + '.json'):
            raise Denied('active effective-plan binding is missing, changed or malformed')
        checkpoint = stable_file_bytes(self.dir / meta['checkpoint_name'], 'effective-plan preactivation checkpoint')
        if hashlib.sha256(checkpoint).hexdigest() != meta['source_sha256']:
            raise Denied('preactivation checkpoint hash mismatch')
        old = load_json(checkpoint)
        if (old.get('version') != '2.0' or old.get('work_package_digest') != self.package_hash
                or old.get('routing_policy_digest') != self.policy_hash
                or set(old.get('tasks', {})) != set(self.sealed_work)):
            raise Denied('preactivation checkpoint baseline mismatch')
        check_receipts(old)
        count = meta['source_receipt_count']
        boundaries = [event for event in state['events'] if event['operation'] == 'activate-plan']
        if (len(old['events']) != count or old['events'][-1]['hash'] != meta['source_receipt_head']
                or state['events'][:count] != old['events'] or len(boundaries) != 1
                or len(state['events']) <= count or state['events'][count] != boundaries[0]
                or boundaries[0].get('plan_activation') != meta):
            raise Denied('effective-plan activation receipt/checkpoint prefix mismatch')
        self._safe_plan_source(old, plan)
        projected = copy.deepcopy(old)
        projected.update(version='2.1', effective_plan_digest=plan.digest, plan_activation=meta)
        if boundaries[0]['state_digest'] != digest({key: value for key, value in projected.items() if key != 'events'}):
            raise Denied('activation rewrote source tasks, roster, gates, budget or history')
        ref, envelope = self._plan_evidence(meta['evidence']['path'], meta['actor'], checkpoint,
                                          plan, refs, fresh=False)
        if ref != meta['evidence'] or any(meta[key] != envelope[key] for key in
                ('reviewer', 'candidate_revision', 'candidate_tree', 'reviewer_qualification_digest', 'owner_request')):
            raise Denied('activation evidence no longer matches its receipt')
        self._plan_checkpoint_guard = (meta['checkpoint_name'], meta['source_sha256'])
        for wid, original in old['tasks'].items():
            current = state['tasks'][wid]
            if original['state'] in ('completed', 'cancelled'):
                if current != original:
                    raise Denied('historical terminal work cannot be reinterpreted: ' + wid)
            elif current != original and current.get('effective_plan_digest') != plan.digest:
                raise Denied('future task lacks its effective-plan binding: ' + wid)
            for key in ('assignment', 'review'):
                if current != original and current.get(key) and current[key].get('effective_plan_digest') != plan.digest:
                    raise Denied('future role binding is stale: ' + wid)
        self.effective = plan
        self.plan, self.work = plan.catalog, plan.work
        self._plan_current()

    def activate_plan(self, actor, record=None, apply=False):
        """Explicit forward boundary; the dry run is a read-only preview."""
        def prepare(source_snapshot):
            raw = source_snapshot[0]
            old = load_json(raw)
            self._check(old)
            self._check_binding_baseline(old, raw)
            if old['version'] == '2.1':
                return None, {'activated': False, 'already_current': True, 'version': '2.1',
                              'effective_plan_digest': old['effective_plan_digest']}
            plan = self._load_effective()
            refs = self._plan_source_refs(plan)
            self._safe_plan_source(old, plan)
            source_hash = hashlib.sha256(raw).hexdigest()
            name = 'state.plan-v2.' + source_hash + '.json'
            existing = stable_file_bytes(self.dir / name, 'preactivation checkpoint', missing_ok=True)
            if existing is not None and existing != raw:
                raise Denied('preactivation checkpoint differs; never overwrite')
            result = {'activated': False, 'dry_run': not apply, 'from_version': '2.0', 'to_version': '2.1',
                      'effective_plan_digest': plan.digest, 'source_refs': refs,
                      'source_state_sha256': source_hash, 'source_receipt_count': len(old['events']),
                      'source_receipt_head': old['events'][-1]['hash'], 'checkpoint': str(self.dir / name)}
            if not record:
                if apply:
                    raise Denied('apply requires exact independent review and runtime-stop evidence')
                result['review_evidence'] = 'REQUIRED_BEFORE_APPLY'
                return None, result
            ref, envelope = self._plan_evidence(record, actor, raw, plan, refs, fresh=True)
            meta = {'from_version': '2.0', 'effective_plan_digest': plan.digest, 'source_refs': refs,
                    'source_sha256': source_hash, 'source_receipt_count': len(old['events']),
                    'source_receipt_head': old['events'][-1]['hash'], 'checkpoint_name': name,
                    'evidence': ref, **{key: envelope[key] for key in ('actor', 'reviewer',
                        'candidate_revision', 'candidate_tree', 'reviewer_qualification_digest', 'owner_request')}}
            updated = copy.deepcopy(old)
            updated.update(version='2.1', effective_plan_digest=plan.digest, plan_activation=meta)
            self._event(updated, actor, 'activate-plan')
            event = updated['events'][-1]
            event['plan_activation'] = copy.deepcopy(meta)
            event['hash'] = digest({key: value for key, value in event.items() if key != 'hash'})
            return (updated, name), result
        if not apply:
            try:
                _candidate, result = prepare(self._stable_state_snapshot())
                self._binding_current()
                return result
            finally:
                self._activation_qualification_expiry = None
        try:
            with self.locked() as token:
                snapshot = self._stable_state_snapshot()
                candidate, result = prepare(snapshot)
                if candidate is None:
                    return result
                updated, name = candidate
                existing = stable_at(token['dir_fd'], name, 'preactivation checkpoint', missing_ok=True)
                if existing is None:
                    write_at_exclusive(token['dir_fd'], name, snapshot[0], 'preactivation checkpoint')
                    os.fsync(token['dir_fd'])
                elif existing[0] != snapshot[0]:
                    raise Denied('preactivation checkpoint changed before apply')
                self._plan_checkpoint_guard = (name, hashlib.sha256(snapshot[0]).hexdigest())
                self._check(updated)
                self._atomic_state_json(token, updated, expected_state=snapshot)
                return dict(result, activated=True, dry_run=False)
        finally:
            self._activation_qualification_expiry = None

    def _context_binding(self, wid):
        if not self.effective:
            raise Denied('effective dispatch requires explicit plan activation')
        return digest({'effective_plan_digest': self.effective.digest, 'work_package': self.work[wid],
                       'source_refs': self.effective.source_refs, 'routing_policy_digest': self.policy_hash,
                       'routing': self.routes[wid]})

    def status(self):
        state = self._read()
        profiles = []
        for pid, profile in self.profiles.items():
            try:
                q = self.qualified(state, pid)
                available, reason = True, None
            except (Denied, OSError, ValueError, KeyError, TypeError) as exc:
                q, available, reason = None, False, str(exc)
            profiles.append(dict(profile, available=available, unavailable_reason=reason,
                                 expires_at=q['expires_at'] if q else None))
        available_ids = {row['profile_id'] for row in profiles if row['available']}
        try:
            authorization = self.recheck(state['budget_approval'], kind='budget', require_pass=True)
            self._budget_authorization(authorization, state['budget_usd'])
            budget_status = {'available_for_new_paid_work': True, 'scope': authorization['scope'],
                             'expires_at': authorization['expires_at'], 'unavailable_reason': None}
        except (Denied, OSError, ValueError, KeyError, TypeError) as exc:
            budget_status = {'available_for_new_paid_work': False, 'unavailable_reason': str(exc)}
        tasks = {}
        for wid, task in state['tasks'].items():
            assignment = task['assignment'] or {}
            tasks[wid] = {'state': task['state'], 'fence': task['fence'], 'agent': assignment.get('agent'),
                          'profile_id': assignment.get('profile_id'),
                          'reasoning_effort': assignment.get('reasoning_effort'),
                          'fallback': assignment.get('fallback', False),
                          'expired_lease': bool(task['lease'] and task['lease']['expires_at'] <= self.clock())}
        if self.effective:
            budget_status = {'available_for_new_paid_work': False,
                             'unavailable_reason': 'Historic budgets do not authorize effective-plan work.'}
        return {'version': state['version'], 'routing_policy_digest': self.policy_hash,
                'work_package_digest': self.package_hash,
                'effective_plan': self._plan_context_status(),
                'active_plan_coding_limits': ({'reasoning_efforts': ['max'],
                    'billing_modes': ['subscription'], 'new_api_allocation_usd': 0,
                    'meaning': 'Execution scope restriction; existing profile qualification is unchanged.'}
                    if self.effective else None),
                'budget_usd': state['budget_usd'], 'declared_spend_usd': float(self._declared_spend(state)),
                'remaining_budget_usd': float(amount(state['budget_usd']) - self._declared_spend(state)),
                'budget_authorization': budget_status,
                'profiles': profiles,
                'verified_tiers': [tier for tier, row in self.tiers.items()
                                   if row['default_profile_id'] in available_ids],
                'capability_defaults': [dict(row, default_available=row['default_profile_id'] in available_ids)
                                        for row in self.tiers.values()],
                'tasks': tasks, 'receipt_count': len(state['events'])}

    def ready(self):
        state = self._read()
        return [wid for wid, task in state['tasks'].items()
                if task['state'] == 'planned'
                and all(state['tasks'][dependency]['state'] == 'completed'
                        for dependency in self.work[wid]['dependencies'])
                and self.work[wid]['activation'] != 'DEFER UNTIL TRIGGERED']

    def context(self, wid, out=None, max_bytes=262144):
        self._policy_current()
        if self.statefile.exists():
            self._read()
        elif self.binding:
            raise Denied('bound context requires its live state; no sealed fallback')
        if out:
            if self.unbound_external:
                raise Denied('an unbound explicit state root cannot be used with mutating context output')
            safe_public_rel(out, 'context output')
        pack = super().context(wid, max_bytes=max_bytes)
        pack.update(schema_version='2.0', work_package_digest=self.package_hash,
                    routing_policy_digest=self.policy_hash,
                    routing_policy_path=str(self.policy_path), routing=self.routes[wid],
                    routing_decision=self.policy['decision'])
        pack['effective_plan'] = self._plan_context_status()
        pack['dispatch_valid'] = self.effective is not None
        if self.effective:
            pack.update(schema_version='2.1', effective_plan_digest=self.effective.digest,
                        context_digest=self._context_binding(wid),
                        effective_acceptance=[row for row in self.effective.contract['acceptance_extensions']
                                              if row['id'] in self.work[wid]['acceptance_ids']])
        elif pack['effective_plan'].get('proposed_digest'):
            pack['proposed_work_package'] = self._load_effective().work[wid]
        local_files = [self.policy_path, under(PROJECT, self.policy['decision'])]
        if self.effective:
            local_files.append(self.root / effective_plan.DECISION)
        pack['project_context_files'] = [
            {'path': str(path), 'sha256': file_hash(path), 'bytes': path.stat().st_size}
            for path in local_files
        ]
        pack['total_reference_bytes'] += sum(row['bytes'] for row in pack['project_context_files'])
        pack['status'] = 'NEEDS_NARROWING' if pack['total_reference_bytes'] > max_bytes else 'READY'
        if pack['status'] != 'READY':
            pack['dispatch_valid'] = False
            pack.pop('context_digest', None)
        pack['instructions'] += (' Read the local routing ADR/policy and any effective-plan ADR. '
                                 'Only explicitly amended fields are superseded. Sealed unbound contexts are '
                                 'not valid for effective-plan dispatch; admission and assignment require current digests.')
        if out:
            atomic_write(under(self.root, out, False), pack)
        return pack

    def _plan_context_status(self):
        if self.effective:
            return {'mode': 'active', 'digest': self.effective.digest,
                    'source_refs': self.effective.source_refs, 'activation_required': False}
        result = {'mode': 'sealed-unbound', 'digest': None, 'source_refs': [],
                  'activation_required': True,
                  'meaning': 'Sealed baseline inspection only; invalid for amended-plan dispatch.'}
        if (self.root / effective_plan.DECISION).exists():
            proposed = self._load_effective()
            result.update(proposed_digest=proposed.digest, source_refs=proposed.source_refs)
        return result

    def _retained_review(self, wid, review, candidate=None):
        reviewed = revision(review.get('candidate', ''))
        if candidate is not None and reviewed != candidate:
            raise Denied('retained review candidate mismatch: ' + wid)
        self.recheck(review.get('evidence'), kind='review', task=wid, candidate=reviewed,
                     require_pass=review.get('approved') is True)
        if review.get('budget_approval'):
            self.recheck(review['budget_approval'], kind='budget', require_pass=True)

    def _retained_bundle(self, wid, bundle):
        candidate = revision(bundle['candidate']) if bundle.get('candidate') is not None else None
        review, integration = bundle.get('review'), bundle.get('integration')
        if bundle.get('checkpoint'):
            # A checkpoint may truthfully report NOT_RUN; its file/log integrity is still required.
            self.recheck(bundle['checkpoint'], kind='checkpoint', task=wid)
        if bundle.get('submission'):
            if candidate is None:
                raise Denied('retained submission lacks a candidate: ' + wid)
            self.recheck(bundle['submission'], kind='submission', task=wid, candidate=candidate,
                         require_pass=bool(integration or (review and review.get('approved') is True)))
        if review:
            if candidate is None:
                raise Denied('retained review lacks a candidate: ' + wid)
            self._retained_review(wid, review, candidate)
        for previous_review in bundle.get('review_history', []):
            self._retained_review(wid, previous_review)
        assignment = bundle.get('assignment')
        if assignment and assignment.get('budget_approval'):
            self.recheck(assignment['budget_approval'], kind='budget', require_pass=True)
        if integration:
            if (candidate is None or integration.get('candidate') != candidate
                    or not bundle.get('submission') or not review or review.get('approved') is not True):
                raise Denied('retained integration lacks its approved candidate chain: ' + wid)
            evidence = self.recheck(integration.get('evidence'), kind='integration', task=wid,
                                    candidate=candidate, require_pass=True)
            if (evidence.get('runtime_stopped') is not True
                    or evidence.get('integrated_revision') != revision(integration.get('integrated_revision', ''))
                    or evidence.get('conflict_resolution_changed_semantics', False)):
                raise Denied('retained integration stop/head evidence is unsafe: ' + wid)

    def _validate_retained_evidence(self, state):
        # In v1, init starts at zero and only assign/recover/cancel increment a task fence.
        # Its receipts therefore recover exact previous_fence values without rewriting history.
        fences = {wid: 0 for wid in self.work}
        recoveries = {wid: [] for wid in self.work}
        for event in state['events']:
            if event['operation'] in ('assign', 'recover', 'cancel'):
                wid = event.get('task_id')
                if wid not in fences:
                    raise Denied('receipt references an unknown task fence')
                if event['operation'] in ('recover', 'cancel'):
                    recoveries[wid].append(fences[wid])
                fences[wid] += 1
        if state.get('budget_approval'):
            self.recheck(state['budget_approval'], kind='budget', require_pass=True)
        if self._declared_spend(state) > amount(state['budget_usd']):
            raise Denied('retained allocations exceed the owner development allowance')
        for wid, task in state['tasks'].items():
            if type(task.get('fence')) is not int or task['fence'] != fences[wid]:
                raise Denied('task fence differs from retained receipt operations: ' + wid)
            history = task.get('history')
            if not isinstance(history, list) or len(history) != len(recoveries[wid]):
                raise Denied('retained recovery history differs from receipts: ' + wid)
            self._retained_bundle(wid, task)
            if task.get('trigger'):
                self.recheck(task['trigger'], kind='trigger', task=wid, require_pass=True)
            for previous_fence, entry in zip(recoveries[wid], history):
                evidence = self.recheck(entry.get('recovery'), kind='recovery', task=wid, require_pass=True)
                if (evidence.get('runtime_stopped') is not True
                        or type(evidence.get('previous_fence')) is not int
                        or evidence['previous_fence'] != previous_fence
                        or ('fence' in entry and (type(entry['fence']) is not int or entry['fence'] != previous_fence))):
                    raise Denied('retained recovery stop/fence evidence is unsafe: ' + wid)
                revision(evidence.get('observed_revision', ''))
                self._retained_bundle(wid, entry)

    def _capture_legacy_budget(self, state):
        approved = amount(state['budget_usd'])
        ref = state.get('budget_approval')
        if ref:
            envelope = self.recheck(ref, kind='budget', require_pass=True)
            if envelope['schema_version'] != '1.0':
                raise Denied('v1 migration must retain its original legacy budget envelope')
        elif approved or self._declared_spend(state):
            raise Denied('legacy paid work requires its retained global budget approval')
        allocations = []
        for wid, task in state['tasks'].items():
            bundles = [(task, task['fence'], ['tasks', wid])]
            for index, previous in enumerate(task['history']):
                recovery = self.recheck(previous['recovery'], kind='recovery', task=wid, require_pass=True)
                bundles.append((previous, recovery['previous_fence'], ['tasks', wid, 'history', index]))
            for bundle, fence, path in bundles:
                records = [('author', bundle.get('assignment'), path + ['assignment']),
                           ('reviewer', bundle.get('review'), path + ['review'])]
                records += [('reviewer', review, path + ['review_history', index])
                            for index, review in enumerate(bundle.get('review_history', []))]
                for role, record, source_path in records:
                    if record and amount(record.get('budget_usd', 0)) and 'budget_approval' not in record:
                        allocations.append({'work_package_id': wid, 'role': role, 'fence': fence,
                                            'record_digest': digest(record), 'budget_usd': record['budget_usd'],
                                            'source_path': source_path})
        return {'evidence': copy.deepcopy(ref), 'approved_budget_usd': state['budget_usd'],
                'scope': 'retained-v1-allocations-only', 'allocations': allocations}

    def migrate_v1(self, actor, apply=False):
        """Dry-run first; preserve old bytes, tasks and receipts, then append one receipt."""
        if not actor.startswith('human:'):
            raise Denied('an accountable owner must authorize state migration')
        with self.locked() as token:
            self._policy_current()
            if not self.statefile.is_file():
                raise Denied('no v1 state to migrate; use init for an empty ledger')
            source_snapshot = self._stable_state_snapshot()
            raw = source_snapshot[0]
            old = load_json(raw)
            if old.get('version') == '2.0':
                self._check(old)
                self._check_binding_baseline(old, raw)
                return {'migrated': False, 'already_current': True, 'version': '2.0'}
            # Use the original validator on the original state, never on rewritten old receipts.
            legacy.Harness._check(self, old)
            check_receipts(old)
            self._check_binding_baseline(old, raw)
            if set(old.get('tasks', {})) != set(self.work) or old.get('package_version') != self.plan['package_version']:
                raise Denied('v1 task/package baseline mismatch')
            for wid, task in old['tasks'].items():
                if task.get('lease') is not None or task.get('state') not in SAFE_MIGRATION_STATES:
                    raise Denied('migration requires no leases or active/uncertain task states: ' + wid)
                if task['state'] in ('planned', 'admitted', 'blocked', 'cancelled'):
                    if any(task.get(k) is not None for k in ('assignment', 'candidate', 'submission', 'review', 'integration')):
                        raise Denied('unfinished task data requires proved v1 recovery before migration: ' + wid)
                if task['state'] in ('integrated', 'completed'):
                    integration = task.get('integration')
                    if not integration or not task.get('assignment') or not task.get('review'):
                        raise Denied('terminal task lacks integration/stop evidence: ' + wid)
                    evidence = self.recheck(integration['evidence'], kind='integration', task=wid,
                                            candidate=task['candidate'], require_pass=True)
                    if evidence.get('runtime_stopped') is not True:
                        raise Denied('migration requires retained runtime-stop evidence: ' + wid)
            self._validate_retained_evidence(old)
            legacy_budget = self._capture_legacy_budget(old)
            source_hash = hashlib.sha256(raw).hexdigest()
            backup = self.dir / ('state.v1.' + source_hash + '.json')
            result = {'migrated': False, 'dry_run': not apply, 'from_version': '1.0', 'to_version': '2.0',
                      'source_sha256': source_hash, 'old_receipt_count': len(old['events']),
                      'old_receipt_head': old['events'][-1]['hash'], 'backup': str(backup),
                      'routing_policy_digest': self.policy_hash, 'roster_cleared': True,
                      'tasks_and_history_preserved': True}
            if not apply:
                return result
            checkpoint_bytes(backup, raw)
            state = copy.deepcopy(old)
            state['version'] = '2.0'
            state['routing_policy_digest'] = self.policy_hash
            state['roster'] = []
            state['routing_migration'] = {
                'from_version': '1.0', 'source_sha256': source_hash,
                'source_receipt_head': old['events'][-1]['hash'], 'source_receipt_count': len(old['events']),
                'backup_path': str(backup.relative_to(self.root)), 'old_roster_digest': digest(old['roster']),
                'policy_digest': self.policy_hash,
                'roster_invalidation_reason': 'v1 tier bindings do not qualify exact v2 model/effort profiles',
                'legacy_budget_authorization': legacy_budget,
            }
            self._event(state, actor, 'migrate-routing-v1-to-v2')
            event = state['events'][-1]
            event['migration'] = copy.deepcopy(state['routing_migration'])
            event['hash'] = digest({key: value for key, value in event.items() if key != 'hash'})
            self._check(state)
            self._atomic_state_json(token, state, expected_state=source_snapshot)
            return dict(result, migrated=True, dry_run=False)

    def rollback_v2(self, actor, apply=False, runtime_stopped=False):
        """Only the immediate migration can be rolled back; all later v2 work is retained."""
        if not actor.startswith('human:') or runtime_stopped is not True:
            raise Denied('rollback requires accountable owner attestation that all runtimes stopped')
        with self.locked() as token:
            state = self._read()
            migration = state.get('routing_migration')
            if (not migration or state['events'][-1]['operation'] != 'migrate-routing-v1-to-v2'
                    or len(state['events']) != migration['source_receipt_count'] + 1
                    or any(task['lease'] is not None for task in state['tasks'].values())):
                raise Denied('rollback would discard later receipts/work; reviewed forward migration required')
            backup_path = under(self.root, migration['backup_path'])
            raw = stable_file_bytes(backup_path, 'v1 rollback checkpoint')
            if hashlib.sha256(raw).hexdigest() != migration['source_sha256']:
                raise Denied('original v1 checkpoint hash mismatch')
            old = load_json(raw)
            legacy.Harness._check(self, old)
            check_receipts(old)
            self._validate_retained_evidence(old)
            if old['events'] != state['events'][:-1] or old['tasks'] != state['tasks']:
                raise Denied('checkpoint no longer matches the migration boundary')
            current_snapshot = self._stable_state_snapshot()
            current_raw = current_snapshot[0]
            retained = self.dir / ('state.v2.' + hashlib.sha256(current_raw).hexdigest() + '.json')
            if apply:
                checkpoint_bytes(retained, current_raw)
                self._atomic_state_bytes(token, raw, expected_state=current_snapshot)
            return {'rolled_back': apply, 'dry_run': not apply, 'version': '1.0' if apply else '2.0',
                    'restored_sha256': migration['source_sha256'], 'retained_v2_checkpoint': str(retained)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--state-root', type=Path,
                        help='absolute external state directory; required by an active binding')
    parser.add_argument('--package', type=Path, default=PACKAGE)
    parser.add_argument('--read-only', action='store_true',
                        help='Inspection only; reject mutations and context output before state access.')
    sub = parser.add_subparsers(dest='cmd', required=True)
    for name in ('init', 'status', 'ready', 'check'):
        command = sub.add_parser(name)
        command.add_argument('--actor', default='human:owner')
    command = sub.add_parser('migrate-v1')
    command.add_argument('--actor', required=True)
    command.add_argument('--apply', action='store_true')
    command = sub.add_parser('activate-plan')
    command.add_argument('--actor', required=True)
    command.add_argument('--record')
    command.add_argument('--apply', action='store_true')
    sub.add_parser('plan', help='read-only effective-plan projection; never activates state')
    command = sub.add_parser('rollback-v2')
    command.add_argument('--actor', required=True)
    command.add_argument('--apply', action='store_true')
    command.add_argument('--runtime-stopped', action='store_true')
    command = sub.add_parser('recover-state-write')
    command.add_argument('--actor', required=True)
    command.add_argument('--runtime-stopped', action='store_true')
    for name in ('set-roster', 'record-gate', 'set-budget'):
        command = sub.add_parser(name)
        command.add_argument('--actor', required=True)
        command.add_argument('--record', required=True)
        if name == 'set-budget':
            command.add_argument('--usd', type=float, required=True)
    for name in ('admit', 'assign', 'start', 'checkpoint', 'submit', 'review', 'integrate',
                 'complete', 'block', 'recover', 'cancel', 'context'):
        command = sub.add_parser(name)
        command.add_argument('task')
        command.add_argument('--actor', default='astra')
        if name == 'admit':
            command.add_argument('--trigger')
            command.add_argument('--plan-digest')
        if name in ('assign', 'review'):
            command.add_argument('--tier', type=int, choices=[1, 2, 3, 4])
            command.add_argument('--human', action='store_true')
            command.add_argument('--profile-id')
            command.add_argument('--fallback', action='store_true')
            command.add_argument('--fallback-reason')
            command.add_argument('--routing-record')
            command.add_argument('--budget-usd', type=float, default=0)
            command.add_argument('--max-tokens', type=int, default=50000)
            command.add_argument('--max-seconds', type=int, default=3600)
        if name == 'assign':
            command.add_argument('--agent', required=True)
            command.add_argument('--plan-digest')
            command.add_argument('--context-digest')
        if name in ('start', 'checkpoint', 'submit'):
            command.add_argument('--fence', type=int, required=True)
        if name in ('checkpoint', 'submit', 'review', 'integrate', 'block', 'recover', 'cancel'):
            command.add_argument('--record', required=True)
        if name in ('submit', 'review', 'integrate'):
            command.add_argument('--candidate', required=True)
        if name == 'checkpoint':
            command.add_argument('--extend-seconds', type=int, default=0)
        if name == 'review':
            command.add_argument('--reject', action='store_true')
        if name == 'integrate':
            command.add_argument('--integrated', required=True)
        if name == 'context':
            command.add_argument('--out')
            command.add_argument('--max-bytes', type=int, default=262144)
    args = parser.parse_args(argv)
    try:
        if args.read_only and (args.cmd not in ('status', 'ready', 'check', 'context', 'plan', 'activate-plan')
                              or (args.cmd == 'activate-plan' and args.apply)
                              or getattr(args, 'out', None) is not None):
            raise Denied('read-only inspection rejects mutations and context output')
        if args.cmd == 'plan':
            print(json.dumps(effective_plan.load_plan(args.root).summary(), indent=2, sort_keys=True))
            return 0
        harness = Harness(args.root, args.package, state_root=args.state_root,
                          allow_state_recovery=args.cmd == 'recover-state-write')
        op = args.cmd
        options = {key: getattr(args, key) for key in ('profile_id', 'fallback', 'fallback_reason', 'routing_record')} if op in ('assign', 'review') else {}
        if op == 'init': result = harness.init(args.actor)
        elif op in ('status', 'ready'): result = getattr(harness, op)()
        elif op == 'check':
            harness.status()
            result = {'integrity': 'PASS', 'meaning': 'local state/receipt/policy integrity only; not production readiness'}
        elif op == 'migrate-v1': result = harness.migrate_v1(args.actor, args.apply)
        elif op == 'activate-plan': result = harness.activate_plan(args.actor, args.record, args.apply)
        elif op == 'rollback-v2': result = harness.rollback_v2(args.actor, args.apply, args.runtime_stopped)
        elif op == 'recover-state-write': result = harness.recover_state_write(
            args.actor, args.runtime_stopped)
        elif op == 'set-roster': result = harness.roster(args.actor, args.record)
        elif op == 'record-gate': result = harness.gate(args.actor, args.record)
        elif op == 'set-budget': result = harness.budget(args.actor, args.usd, args.record)
        elif op == 'admit': result = harness.admit(args.task, args.actor, args.trigger, plan_digest=args.plan_digest)
        elif op == 'assign': result = harness.assign(args.task, args.actor, args.agent, args.tier, args.human, args.budget_usd, args.max_tokens, args.max_seconds, plan_digest=args.plan_digest, context_digest=args.context_digest, **options)
        elif op == 'start': result = harness.start(args.task, args.actor, args.fence)
        elif op == 'checkpoint': result = harness.checkpoint(args.task, args.actor, args.fence, args.record, args.extend_seconds)
        elif op == 'submit': result = harness.submit(args.task, args.actor, args.fence, args.candidate, args.record)
        elif op == 'review': result = harness.review(args.task, args.actor, args.tier, args.candidate, args.record, not args.reject, args.human, budget_usd=args.budget_usd, max_tokens=args.max_tokens, max_seconds=args.max_seconds, **options)
        elif op == 'integrate': result = harness.integrate(args.task, args.actor, args.candidate, args.integrated, args.record)
        elif op == 'complete': result = harness.complete(args.task, args.actor)
        elif op == 'block': result = harness.block(args.task, args.actor, args.record)
        elif op in ('recover', 'cancel'): result = harness.recover(args.task, args.actor, args.record, op == 'cancel')
        elif op == 'context': result = harness.context(args.task, args.out, args.max_bytes)
        else: raise Denied('unknown command')
        print(json.dumps(result if result is not None else {'ok': True}, indent=2))
        return 0
    except (Denied, OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
