#!/usr/bin/env python3
"""Project-local Texenda coordination v2. No model launch or external effects.

The sealed v1 scaffold supplies evidence, leases, lifecycle and recovery primitives.
This reviewed adapter replaces only routing, state initialization/checks and migration.
Actor labels and evidence attestations require accountable runtime/reviewer controls.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time

PROJECT = Path(__file__).resolve().parents[2]
PACKAGE = PROJECT / 'specs/texenda-handoff'
POLICY = Path(__file__).with_name('routing-policy.json')
LEGACY_PATH = PACKAGE / '08-project-harness/harness.py'
LEGACY_DIGEST = '226a4a14b3a795b24354eb90e51a50067fd27fe809423b30b9fa1551f3ce72d6'
if hashlib.sha256(LEGACY_PATH.read_bytes()).hexdigest() != LEGACY_DIGEST:
    raise RuntimeError('sealed harness baseline changed; review the local adapter')
_spec = importlib.util.spec_from_file_location('texenda_sealed_harness_v1', LEGACY_PATH)
legacy = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(legacy)
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


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Denied('duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object)


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
    def __init__(self, root, package=PACKAGE, clock=time.time, policy=POLICY):
        super().__init__(Path(root), Path(package), clock)
        self.policy_path = Path(policy)
        if self.policy_path.is_symlink():
            raise Denied('routing policy cannot be a symlink')
        self.policy = load_json(self.policy_path.read_text())
        self.policy_hash = digest(self.policy)
        self.evidence_fields = set(load_json((PACKAGE / '08-project-harness/schemas/evidence.schema.json').read_text())['properties'])
        self._validate_policy()

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
        if digest(load_json(self.policy_path.read_text())) != self.policy_hash:
            raise Denied('routing policy changed during this session; reload and explicitly migrate state')

    def evidence(self, rel, kind=None, task=None, candidate=None, require_pass=False):
        """Retain v1 lifecycle envelopes; new routing metadata uses the local v2 schema."""
        path = under(self.root, rel)
        envelope = load_json(path.read_text())
        if not isinstance(envelope, dict) or envelope.get('schema_version') not in ('1.0', '2.0'):
            raise Denied('invalid evidence envelope')
        fields = self.evidence_fields
        if envelope['schema_version'] == '2.0':
            fields = fields | {'routing_policy_digest', 'profile_id', 'role', 'capability_tier',
                               'work_package_digest', 'fence', 'rationale', 'reasoning_demand', *CONDITIONS}
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
                log = under(self.root, check.get('evidence_path', ''))
                if file_hash(log) != check.get('sha256'):
                    raise Denied('test log hash mismatch')
                if not check.get('command_or_procedure'):
                    raise Denied('test command/procedure required')
        if require_pass:
            required = [check for check in checks if check['required']]
            if not required or any(check['status'] != 'PASS' for check in required):
                raise Denied('all required checks must have PASS evidence; NOT RUN cannot pass')
        return {'path': safe_rel(rel), 'sha256': file_hash(path)}, envelope

    def _check(self, state):
        self._policy_current()
        if (state.get('version') != '2.0'
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

    def _read(self):
        if not self.statefile.is_file():
            raise Denied('run init first')
        state = load_json(self.statefile.read_text())
        self._check(state)
        return state

    def init(self, actor='human:owner'):
        with self.locked():
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
            atomic_write(self.statefile, state)
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
        if not record:
            raise Denied('lower effort requires bounded/reversible/fully specified deterministic routing evidence')
        ref, envelope = self.evidence(record, 'routing', wid, candidate, require_pass=True)
        if (envelope['schema_version'] != '2.0'
                or envelope.get('role') != role or envelope.get('profile_id') != profile_id
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
                    'routing_policy_digest': self.policy_hash}
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
                'downshift_evidence': downshift, 'routing_policy_digest': self.policy_hash}

    def _recheck_binding(self, state, wid, role, binding, candidate=None):
        ref = binding.get('downshift_evidence')
        actual = self._select(
            state, wid, role, binding['tier'], binding['human'], binding['profile_id'],
            binding['fallback'], binding['fallback_reason'], ref['path'] if ref else None, candidate,
        )
        if any(binding.get(key) != value for key, value in actual.items()):
            raise Denied('assigned exact profile/runtime/evidence changed; recover and assign a new fence')

    def assign(self, wid, actor, agent, tier=None, human=False, budget_usd=0,
               max_tokens=50000, max_seconds=3600, *, profile_id=None, fallback=False,
               fallback_reason=None, routing_record=None):
        def apply(state):
            task = self.task(state, wid, 'admitted')
            if human != agent.startswith('human:'):
                raise Denied('explicit human assignment must match human: principal')
            binding = self._select(state, wid, 'author', tier, human, profile_id,
                                   fallback, fallback_reason, routing_record)
            if (not 0 <= budget_usd <= state['budget_usd'] or not 0 < max_tokens <= 1000000
                    or not 0 < max_seconds <= 28800):
                raise Denied('invalid task budget or bounds')
            used = sum((t['assignment'] or {}).get('budget_usd', 0)
                       + sum((h.get('assignment') or {}).get('budget_usd', 0) for h in t['history'])
                       for t in state['tasks'].values())
            if used + budget_usd > state['budget_usd']:
                raise Denied('development allowance exhausted; owner must increase')
            q = binding['qualification']
            if q and q['billing_mode'] == 'api' and budget_usd <= 0:
                raise Denied('API work needs positive owner-authorized development spend allowance')
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
            task['assignment'] = dict(binding, agent=agent, budget_usd=budget_usd,
                                      max_tokens=max_tokens, max_seconds=max_seconds)
            task['state'] = 'assigned'
            return dict(binding, task=wid, fence=task['fence'], paths=paths)
        return self.change(actor, 'assign', apply, wid)

    def start(self, wid, actor, fence):
        def apply(state):
            task = self.task(state, wid, 'assigned')
            self.owned(task, actor, fence)
            self._recheck_binding(state, wid, 'author', task['assignment'])
            task['state'] = 'running'
        return self.change(actor, 'start', apply, wid)

    def review(self, wid, actor, tier, candidate, record, approve=True, human=False, *,
               profile_id=None, fallback=False, fallback_reason=None, routing_record=None):
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
            binding = self._select(state, wid, 'reviewer', tier, human, profile_id,
                                   fallback, fallback_reason, routing_record, candidate)
            self.recheck(task['submission'], kind='submission', task=wid,
                         candidate=candidate, require_pass=approve)
            ref, envelope = self.evidence(record, 'review', wid, candidate, require_pass=approve)
            if not human and (envelope['schema_version'] != '2.0'
                              or envelope.get('profile_id') != binding['profile_id']
                              or envelope.get('routing_policy_digest') != self.policy_hash):
                raise Denied('review evidence must bind the exact reviewer profile and policy')
            task['review'] = dict(binding, actor=actor, candidate=candidate, evidence=ref, approved=approve)
            task['state'] = 'reviewed' if approve else 'running'
            if not approve:
                task['review'] = None
                task['integration'] = None
        return self.change(actor, 'approve-review' if approve else 'request-changes', apply, wid)

    def status(self):
        with self.locked():
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
        tasks = {}
        for wid, task in state['tasks'].items():
            assignment = task['assignment'] or {}
            tasks[wid] = {'state': task['state'], 'fence': task['fence'], 'agent': assignment.get('agent'),
                          'profile_id': assignment.get('profile_id'),
                          'reasoning_effort': assignment.get('reasoning_effort'),
                          'fallback': assignment.get('fallback', False),
                          'expired_lease': bool(task['lease'] and task['lease']['expires_at'] <= self.clock())}
        return {'version': '2.0', 'routing_policy_digest': self.policy_hash,
                'budget_usd': state['budget_usd'], 'profiles': profiles,
                'verified_tiers': [tier for tier, row in self.tiers.items()
                                   if row['default_profile_id'] in available_ids],
                'capability_defaults': [dict(row, default_available=row['default_profile_id'] in available_ids)
                                        for row in self.tiers.values()],
                'tasks': tasks, 'receipt_count': len(state['events'])}

    def context(self, wid, out=None, max_bytes=200000):
        self._policy_current()
        pack = super().context(wid, max_bytes=max_bytes)
        pack.update(schema_version='2.0', routing_policy_digest=self.policy_hash,
                    routing_policy_path=str(self.policy_path), routing=self.routes[wid],
                    routing_decision=self.policy['decision'])
        local_files = [self.policy_path, under(PROJECT, self.policy['decision'])]
        pack['project_context_files'] = [
            {'path': str(path), 'sha256': file_hash(path), 'bytes': path.stat().st_size}
            for path in local_files
        ]
        pack['total_reference_bytes'] += sum(row['bytes'] for row in pack['project_context_files'])
        pack['status'] = 'NEEDS_NARROWING' if pack['total_reference_bytes'] > max_bytes else 'READY'
        pack['instructions'] += (' Read the local routing ADR and policy. Only the sealed numeric model-tier '
                                 'recommendations are superseded by this overlay; all other WP contracts remain binding.')
        if out:
            atomic_write(under(self.root, out, False), pack)
        return pack

    def migrate_v1(self, actor, apply=False):
        """Dry-run first; preserve old bytes, tasks and receipts, then append one receipt."""
        if not actor.startswith('human:'):
            raise Denied('an accountable owner must authorize state migration')
        with self.locked():
            self._policy_current()
            if not self.statefile.is_file():
                raise Denied('no v1 state to migrate; use init for an empty ledger')
            raw = self.statefile.read_bytes()
            old = load_json(raw)
            if old.get('version') == '2.0':
                self._check(old)
                return {'migrated': False, 'already_current': True, 'version': '2.0'}
            # Use the original validator on the original state, never on rewritten old receipts.
            legacy.Harness._check(self, old)
            check_receipts(old)
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
            }
            self._event(state, actor, 'migrate-routing-v1-to-v2')
            event = state['events'][-1]
            event['migration'] = copy.deepcopy(state['routing_migration'])
            event['hash'] = digest({key: value for key, value in event.items() if key != 'hash'})
            self._check(state)
            atomic_write(self.statefile, state)
            return dict(result, migrated=True, dry_run=False)

    def rollback_v2(self, actor, apply=False, runtime_stopped=False):
        """Only the immediate migration can be rolled back; all later v2 work is retained."""
        if not actor.startswith('human:') or runtime_stopped is not True:
            raise Denied('rollback requires accountable owner attestation that all runtimes stopped')
        with self.locked():
            state = self._read()
            migration = state.get('routing_migration')
            if (not migration or state['events'][-1]['operation'] != 'migrate-routing-v1-to-v2'
                    or len(state['events']) != migration['source_receipt_count'] + 1
                    or any(task['lease'] is not None for task in state['tasks'].values())):
                raise Denied('rollback would discard later receipts/work; reviewed forward migration required')
            raw = under(self.root, migration['backup_path']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != migration['source_sha256']:
                raise Denied('original v1 checkpoint hash mismatch')
            old = load_json(raw)
            legacy.Harness._check(self, old)
            check_receipts(old)
            if old['events'] != state['events'][:-1] or old['tasks'] != state['tasks']:
                raise Denied('checkpoint no longer matches the migration boundary')
            current_raw = self.statefile.read_bytes()
            retained = self.dir / ('state.v2.' + hashlib.sha256(current_raw).hexdigest() + '.json')
            if apply:
                checkpoint_bytes(retained, current_raw)
                restore_bytes(self.statefile, raw)
            return {'rolled_back': apply, 'dry_run': not apply, 'version': '1.0' if apply else '2.0',
                    'restored_sha256': migration['source_sha256'], 'retained_v2_checkpoint': str(retained)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--package', type=Path, default=PACKAGE)
    sub = parser.add_subparsers(dest='cmd', required=True)
    for name in ('init', 'status', 'ready', 'check'):
        command = sub.add_parser(name)
        command.add_argument('--actor', default='human:owner')
    command = sub.add_parser('migrate-v1')
    command.add_argument('--actor', required=True)
    command.add_argument('--apply', action='store_true')
    command = sub.add_parser('rollback-v2')
    command.add_argument('--actor', required=True)
    command.add_argument('--apply', action='store_true')
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
        if name in ('assign', 'review'):
            command.add_argument('--tier', type=int, choices=[1, 2, 3, 4])
            command.add_argument('--human', action='store_true')
            command.add_argument('--profile-id')
            command.add_argument('--fallback', action='store_true')
            command.add_argument('--fallback-reason')
            command.add_argument('--routing-record')
        if name == 'assign':
            command.add_argument('--agent', required=True)
            command.add_argument('--budget-usd', type=float, default=0)
            command.add_argument('--max-tokens', type=int, default=50000)
            command.add_argument('--max-seconds', type=int, default=3600)
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
            command.add_argument('--max-bytes', type=int, default=200000)
    args = parser.parse_args(argv)
    try:
        harness = Harness(args.root, args.package)
        op = args.cmd
        options = {key: getattr(args, key) for key in ('profile_id', 'fallback', 'fallback_reason', 'routing_record')} if op in ('assign', 'review') else {}
        if op == 'init': result = harness.init(args.actor)
        elif op in ('status', 'ready'): result = getattr(harness, op)()
        elif op == 'check':
            harness.status()
            result = {'integrity': 'PASS', 'meaning': 'local state/receipt/policy integrity only; not production readiness'}
        elif op == 'migrate-v1': result = harness.migrate_v1(args.actor, args.apply)
        elif op == 'rollback-v2': result = harness.rollback_v2(args.actor, args.apply, args.runtime_stopped)
        elif op == 'set-roster': result = harness.roster(args.actor, args.record)
        elif op == 'record-gate': result = harness.gate(args.actor, args.record)
        elif op == 'set-budget': result = harness.budget(args.actor, args.usd, args.record)
        elif op == 'admit': result = harness.admit(args.task, args.actor, args.trigger)
        elif op == 'assign': result = harness.assign(args.task, args.actor, args.agent, args.tier, args.human, args.budget_usd, args.max_tokens, args.max_seconds, **options)
        elif op == 'start': result = harness.start(args.task, args.actor, args.fence)
        elif op == 'checkpoint': result = harness.checkpoint(args.task, args.actor, args.fence, args.record, args.extend_seconds)
        elif op == 'submit': result = harness.submit(args.task, args.actor, args.fence, args.candidate, args.record)
        elif op == 'review': result = harness.review(args.task, args.actor, args.tier, args.candidate, args.record, not args.reject, args.human, **options)
        elif op == 'integrate': result = harness.integrate(args.task, args.actor, args.candidate, args.integrated, args.record)
        elif op == 'complete': result = harness.complete(args.task, args.actor)
        elif op == 'block': result = harness.block(args.task, args.actor, args.record)
        elif op in ('recover', 'cancel'): result = harness.recover(args.task, args.actor, args.record, op == 'cancel')
        elif op == 'context': result = harness.context(args.task, args.out, args.max_bytes)
        else: raise Denied('unknown command')
        print(json.dumps(result if result is not None else {'ok': True}, indent=2))
        return 0
    except (Denied, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
