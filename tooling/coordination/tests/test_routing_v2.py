"""Deterministic coordination tests only. No model calls, network, or product acceptance."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


hm = module('texenda_local_harness', Path(__file__).resolve().parents[1] / 'harness.py')
old_tests = module('sealed_lifecycle_tests', hm.PACKAGE / '08-project-harness/tests/test_harness.py')
# Reuse the identical loaded sealed module so assertRaises sees the same Denied class.
old_tests.hm = hm.legacy


def prepare(test, migrate=True, floors=None):
    old_tests.HarnessTests.setUp(test)
    test.v1 = test.h
    policy = json.loads(hm.POLICY.read_text())
    policy['work_package_digest'] = hm.file_hash(test.pkg / '05-implementation/work-packages.json')
    policy['work_package_routes'] = []
    for wp in test.plan['work_packages']:
        author, reviewer = (floors or {}).get(wp['id'], (2, 1))
        row = {'work_package_id': wp['id'], 'rationale': 'Synthetic test routing only.'}
        for role, floor in [('author', author), ('reviewer', reviewer)]:
            row[role] = {
                'capability_floor': floor, 'default_profile_id': hm.MODELS[floor] + '-max',
                'allowed_reasoning_efforts': ['max', 'high', 'medium', 'low'],
                'allowed_profile_ids': [p['profile_id'] for p in policy['profiles']
                                        if p['capability_tier'] <= floor or p['profile_id'] == 'gpt-5.6-sol-max'],
            }
        policy['work_package_routes'].append(row)
    test.policy = policy
    test.policyfile = test.base / 'routing-policy.json'
    test.policyfile.write_text(json.dumps(policy))
    test.h = hm.Harness(test.root, test.pkg, lambda: test.clock[0], test.policyfile)
    if migrate:
        test.h.migrate_v1('human:test-owner', apply=True)


def qualifications(test, pids=None, billing='subscription'):
    return [{
        'profile_id': p['profile_id'], 'capability_tier': p['capability_tier'],
        'model_id': p['model_id'], 'reasoning_effort': p['reasoning_effort'],
        'runtime_id': 'synthetic-test-runtime', 'client_version': 'test',
        'sign_in_mode': 'synthetic', 'billing_mode': billing,
        'capabilities': ['read', 'edit', 'test'],
        'verified_at': hm.utc(test.clock[0]), 'expires_at': hm.utc(test.clock[0] + 86400),
        'qualification_check_ids': ['fixture'],
    } for p in test.h.profiles.values() if pids is None or p['profile_id'] in pids]


def register(test, pids=None, billing='subscription', rows=None):
    record = test.ev('roster', schema_version='2.0', routing_policy_digest=test.h.policy_hash,
                     qualifications=rows if rows is not None else qualifications(test, pids, billing))
    test.h.roster('human:test-owner', record)
    return record


class LegacyLifecycleTests(old_tests.HarnessTests):
    """Run all 39 sealed lifecycle cases through the v2 adapter, with v2 roster data."""
    def setUp(self):
        prepare(self)

    def roster(self):
        register(self, ['gpt-5.6-sol-max'], billing='api')

    def test_qualified_model_and_budget_allow_assignment(self):
        self.roster()
        self.h.budget('human:owner', 5, self.ev('budget'))
        self.h.admit('WP-00', 'astra')
        result = self.h.assign('WP-00', 'astra', 'agent:a', 2, budget_usd=1)
        self.assertEqual(result['model'], 'gpt-5.6-sol')
        self.assertEqual(result['profile_id'], 'gpt-5.6-sol-max')


class RoutingTests(unittest.TestCase):
    ev = old_tests.HarnessTests.ev
    tearDown = old_tests.HarnessTests.tearDown

    def setUp(self):
        prepare(self, floors={'WP-00': (4, 1), 'WP-02': (3, 1), 'WP-03': (2, 1), 'WP-04': (1, 1)})

    def state(self):
        return json.loads(self.h.statefile.read_text())

    def deny(self, call, pattern=None):
        before = self.h.statefile.read_bytes()
        with self.assertRaisesRegex(hm.Denied, pattern or '.'):
            call()
        self.assertEqual(before, self.h.statefile.read_bytes(), 'denial must leave state/receipts/leases unchanged')

    def assign(self, wid='WP-00', **kwargs):
        if self.state()['tasks'][wid]['state'] == 'planned':
            self.h.admit(wid, 'astra')
        return self.h.assign(wid, 'astra', 'agent:author', **kwargs)

    def release(self, wid, assignment):
        self.h.recover(wid, 'astra', self.ev('recovery', wid, previous_fence=assignment['fence'],
                                           observed_revision=self.cand, runtime_stopped=True))

    def route(self, pid, wid='WP-00', role='author', **overrides):
        task = self.state()['tasks'][wid]
        fence = task['fence'] + (1 if role == 'author' and task['state'] in ('planned', 'admitted') else 0)
        fields = dict(schema_version='2.0', profile_id=pid, role=role,
                      capability_tier=self.h.profiles[pid]['capability_tier'],
                      routing_policy_digest=self.h.policy_hash, work_package_digest=self.h.package_hash,
                      fence=fence, expires_at=hm.utc(self.clock[0] + 3600), reasoning_demand='bounded',
                      rationale='Fixed synthetic scope and deterministic oracle.',
                      **{key: True for key in hm.CONDITIONS})
        fields.update(overrides)
        return self.ev('routing', wid, **fields)

    def submitted(self, pid=None, routing_record=None):
        result = self.assign(profile_id=pid, routing_record=routing_record)
        self.h.start('WP-00', 'agent:author', result['fence'])
        self.h.submit('WP-00', 'agent:author', result['fence'], self.cand,
                      self.ev('submission', changed_paths=['src/a/result']))
        return result

    def review_record(self, pid='gpt-6-astra-max', **overrides):
        fields = dict(schema_version='2.0', profile_id=pid, routing_policy_digest=self.h.policy_hash)
        fields.update(overrides)
        return self.ev('review', **fields)

    def test_all_four_max_defaults_and_exact_binding(self):
        register(self)
        for wid, tier in [('WP-00', 4), ('WP-02', 3), ('WP-03', 2), ('WP-04', 1)]:
            with self.subTest(tier=tier):
                assigned = self.assign(wid)
                self.assertEqual(assigned['tier'], tier)
                self.assertEqual(assigned['capability_floor'], tier)
                self.assertEqual(assigned['profile_id'], hm.MODELS[tier] + '-max')
                self.assertEqual(assigned['model'], hm.MODELS[tier])
                self.assertEqual(assigned['reasoning_effort'], 'max')
                self.assertEqual(assigned['routing_policy_digest'], self.h.policy_hash)
                self.assertEqual(assigned['qualification']['evidence']['sha256'],
                                 hm.file_hash(self.root / assigned['qualification']['evidence']['path']))
                self.release(wid, assigned)

    def test_each_allowed_lower_effort_requires_and_accepts_exact_attestation(self):
        register(self)
        self.h.admit('WP-00', 'astra')
        for profile in self.h.profiles.values():
            if profile['default']:
                continue
            pid = profile['profile_id']
            with self.subTest(profile=pid):
                self.deny(lambda: self.assign(profile_id=pid))
                assigned = self.assign(profile_id=pid, routing_record=self.route(pid))
                self.h.start('WP-00', 'agent:author', assigned['fence'])
                self.assertEqual(assigned['profile_id'], pid)
                self.assertEqual(assigned['reasoning_effort'], profile['reasoning_effort'])
                self.release('WP-00', assigned)

    def test_profile_catalog_mutations_and_duplicate_default_deny(self):
        changes = [
            lambda p: p['profiles'].pop(),
            lambda p: p['profiles'].append(copy.deepcopy(p['profiles'][0])),
            lambda p: p['profiles'].append(dict(p['profiles'][-1], profile_id='gpt-5.6-terra-low')),
            lambda p: p['profiles'][0].update(model_id='gpt-5.6-sol'),
            lambda p: p['profiles'][0].update(reasoning_effort='xhigh'),
            lambda p: p['profiles'][1].update(default=True),
            lambda p: p['profiles'][0].update(profile_id='GPT-6-astra-max'),
            lambda p: p['capability_tiers'].append(copy.deepcopy(p['capability_tiers'][0])),
            lambda p: p['capability_tiers'][0].update(default_profile_id='gpt-6-astra-high'),
            lambda p: p['work_package_routes'].pop(),
        ]
        for change in changes:
            with self.subTest(change=changes.index(change)):
                policy = copy.deepcopy(self.policy)
                change(policy)
                self.policyfile.write_text(json.dumps(policy))
                self.deny(lambda: hm.Harness(self.root, self.pkg, policy=self.policyfile))

    def test_duplicate_json_policy_keys_are_denied(self):
        self.policyfile.write_text('{"schema_version":"2.0","schema_version":"2.0"}')
        self.deny(lambda: hm.Harness(self.root, self.pkg, policy=self.policyfile), 'duplicate JSON')

    def test_missing_default_never_selects_available_downshift(self):
        register(self, ['gpt-5.6-luna-low'])
        self.h.admit('WP-00', 'astra')
        self.deny(lambda: self.assign(), 'not runtime-qualified')
        self.assertNotIn(4, self.h.status()['verified_tiers'])

    def test_unavailable_primary_never_silently_falls_back(self):
        register(self, ['gpt-5.6-sol-max'])
        self.h.admit('WP-04', 'astra')
        self.deny(lambda: self.assign('WP-04'), 'not runtime-qualified')

    def test_explicit_fallback_only_sol_max_with_flag_and_reason(self):
        for roster in [None, ['gpt-5.6-sol-max']]:
            register(self, roster)
            if self.state()['tasks']['WP-04']['state'] == 'planned':
                self.h.admit('WP-04', 'astra')
            for flags in [{}, {'fallback': True}, {'fallback_reason': 'primary unavailable'},
                          {'fallback': True, 'fallback_reason': ' '}]:
                with self.subTest(flags=flags, primary_available=roster is None):
                    self.deny(lambda: self.assign('WP-04', profile_id='gpt-5.6-sol-max', **flags))
            result = self.assign('WP-04', profile_id='gpt-5.6-sol-max', fallback=True,
                                 fallback_reason='Explicit bounded substitution approved in this task.')
            self.assertTrue(result['fallback'])
            self.assertEqual(result['tier'], 1)
            self.assertEqual(result['qualification']['capability_tier'], 2)
            self.h.start('WP-04', 'agent:author', result['fence'])
            self.release('WP-04', result)
        self.deny(lambda: self.assign('WP-04', profile_id='gpt-5.6-sol-high',
                                     fallback=True, fallback_reason='Not the accepted max fallback.'))

    def test_sol_max_is_ordinary_t2_default(self):
        register(self)
        result = self.assign('WP-03')
        self.assertFalse(result['fallback'])
        self.assertEqual(result['profile_id'], 'gpt-5.6-sol-max')

    def test_explicit_stronger_substitution_preserves_floor(self):
        register(self)
        for wid, floor, selected in [('WP-03', 2, 1), ('WP-02', 3, 1), ('WP-02', 3, 2),
                                     ('WP-00', 4, 1), ('WP-00', 4, 2), ('WP-00', 4, 3)]:
            with self.subTest(floor=floor, selected=selected):
                result = self.assign(wid, tier=floor, profile_id=hm.MODELS[selected] + '-max')
                self.assertEqual(result['tier'], selected)
                self.assertEqual(result['capability_floor'], floor)
                self.assertFalse(result['fallback'])
                self.release(wid, result)

    def test_insufficient_capability_or_unknown_profile_deny(self):
        register(self)
        for wid, weaker in [('WP-04', 2), ('WP-03', 3), ('WP-03', 4), ('WP-02', 4)]:
            if self.state()['tasks'][wid]['state'] == 'planned':
                self.h.admit(wid, 'astra')
            self.deny(lambda: self.assign(wid, profile_id=hm.MODELS[weaker] + '-max'))
        self.h.admit('WP-00', 'astra')
        self.deny(lambda: self.assign(profile_id='gpt-5.6-terra-low'))
        self.deny(lambda: self.assign(profile_id='gpt-6-astra-xhigh'))

    def test_roster_rejects_duplicate_and_mismatched_exact_profiles(self):
        rows = qualifications(self)
        bad_rows = [rows + [rows[0]], [dict(rows[0], reasoning_effort='high')],
                    [dict(rows[0], model_id='gpt-5.6-sol')], [dict(rows[0], capability_tier=2)],
                    [dict(rows[0], profile_id='unknown')], [dict(rows[0], capabilities=['read'])],
                    [dict(rows[0], qualification_check_ids=['missing'])]]
        for bad in bad_rows:
            self.deny(lambda: register(self, rows=bad))

    def test_roster_requires_owner_and_current_policy(self):
        record = self.ev('roster', schema_version='2.0', qualifications=qualifications(self),
                         routing_policy_digest='0' * 64)
        self.deny(lambda: self.h.roster('human:owner', record))
        self.deny(lambda: self.h.roster('agent:pretending-owner', record))

    def test_named_profile_check_must_pass(self):
        record = self.ev('roster', schema_version='2.0', status='NOT_RUN',
                         qualifications=qualifications(self), routing_policy_digest=self.h.policy_hash)
        self.deny(lambda: self.h.roster('human:owner', record))

    def test_attestation_fields_and_checks_are_exact(self):
        register(self)
        self.h.admit('WP-00', 'astra')
        changes = [dict(role='reviewer'), dict(profile_id='gpt-5.6-luna-high'),
                   dict(routing_policy_digest='0' * 64), dict(work_package_digest='0' * 64),
                   dict(fence=99), dict(capability_tier=3), dict(rationale=''),
                   dict(reasoning_demand='complex'), dict(expires_at=hm.utc(self.clock[0])),
                   dict(status='NOT_RUN')] + [{key: False} for key in hm.CONDITIONS]
        for fields in changes:
            with self.subTest(fields=fields):
                record = self.route('gpt-5.6-luna-low', **fields)
                self.deny(lambda: self.assign(profile_id='gpt-5.6-luna-low', routing_record=record))
        record = self.route('gpt-5.6-luna-low', wid='WP-03')
        self.deny(lambda: self.assign(profile_id='gpt-5.6-luna-low', routing_record=record))

    def test_attestation_log_and_record_tamper_deny_at_start(self):
        register(self)
        record = self.route('gpt-5.6-luna-low')
        result = self.assign(profile_id='gpt-5.6-luna-low', routing_record=record)
        original = (self.root / record).read_text()
        (self.root / record).write_text(original + ' ')
        self.deny(lambda: self.h.start('WP-00', 'agent:author', result['fence']))
        (self.root / record).write_text(original)
        check = json.loads(original)['checks'][0]
        (self.root / check['evidence_path']).write_text('Changed deterministic test log.')
        self.deny(lambda: self.h.start('WP-00', 'agent:author', result['fence']))

    def test_exact_profile_removal_or_same_tier_replacement_denies_start(self):
        register(self)
        result = self.assign('WP-02', profile_id='gpt-5.6-terra-high',
                             routing_record=self.route('gpt-5.6-terra-high', 'WP-02'))
        register(self, ['gpt-5.6-terra-medium'])
        self.deny(lambda: self.h.start('WP-02', 'agent:author', result['fence']))

    def test_renewed_same_profile_requires_new_assignment_fence(self):
        register(self)
        result = self.assign()
        register(self)
        self.deny(lambda: self.h.start('WP-00', 'agent:author', result['fence']), 'changed')

    def test_roster_bytes_and_logs_rechecked(self):
        record = register(self)
        result = self.assign()
        original = (self.root / record).read_text()
        (self.root / record).write_text(original + ' ')
        self.deny(lambda: self.h.start('WP-00', 'agent:author', result['fence']))
        self.assertFalse(any(profile['available'] for profile in self.h.status()['profiles']))
        (self.root / record).write_text(original)
        check = json.loads(original)['checks'][0]
        (self.root / check['evidence_path']).write_text('Modified qualification evidence.')
        self.deny(lambda: self.h.start('WP-00', 'agent:author', result['fence']))

    def test_profile_expiry_boundaries_and_over_age(self):
        rows = qualifications(self)
        for q in rows:
            q['expires_at'] = hm.utc(self.clock[0] + 10)
        register(self, rows=rows)
        self.clock[0] += 9
        result = self.assign()
        self.clock[0] += 1
        self.deny(lambda: self.h.start('WP-00', 'agent:author', result['fence']), 'stale')
        self.clock[0] += 1
        self.deny(lambda: self.h.start('WP-00', 'agent:author', result['fence']), 'stale')
        row = qualifications(self)[0]
        self.deny(lambda: register(self, rows=[dict(row, verified_at=hm.utc(self.clock[0] - 31 * 86400))]))
        self.deny(lambda: register(self, rows=[dict(row, verified_at=hm.utc(self.clock[0] + 61))]))

    def test_attestation_expiry_boundary_and_new_fence(self):
        register(self)
        record = self.route('gpt-5.6-luna-low', expires_at=hm.utc(self.clock[0] + 10))
        self.clock[0] += 9
        result = self.assign(profile_id='gpt-5.6-luna-low', routing_record=record)
        self.clock[0] += 1
        self.deny(lambda: self.h.start('WP-00', 'agent:author', result['fence']), 'expired')
        self.release('WP-00', result)
        self.deny(lambda: self.assign(profile_id='gpt-5.6-luna-low', routing_record=record))

    def test_review_checks_exact_author_qualification_and_independence(self):
        register(self)
        self.submitted()
        record = self.review_record()
        self.deny(lambda: self.h.review('WP-00', 'agent:author', 1, self.cand, record), 'own work')
        self.deny(lambda: self.h.review('WP-00', 'agent:reviewer', 2, self.cand, record), 'floor')
        register(self, ['gpt-6-astra-max'])
        self.deny(lambda: self.h.review('WP-00', 'agent:reviewer', 1, self.cand, record))

    def test_review_rejects_wrong_reviewer_profile_or_expired_qualification(self):
        register(self)
        self.submitted()
        wrong = self.review_record('gpt-6-astra-high')
        self.deny(lambda: self.h.review('WP-00', 'agent:reviewer', 1, self.cand, wrong))
        self.clock[0] += 86400
        self.deny(lambda: self.h.review('WP-00', 'agent:reviewer', 1, self.cand, self.review_record()))

    def test_review_downshift_requires_candidate_bound_attestation(self):
        register(self)
        self.submitted()
        pid = 'gpt-6-astra-high'
        record = self.review_record(pid)
        wrong = self.route(pid, role='reviewer', candidate_revision=self.head)
        self.deny(lambda: self.h.review('WP-00', 'agent:reviewer', 1, self.cand, record,
                                       profile_id=pid, routing_record=wrong))
        self.h.review('WP-00', 'agent:reviewer', 1, self.cand, record, profile_id=pid,
                       routing_record=self.route(pid, role='reviewer'))
        self.assertEqual(self.state()['tasks']['WP-00']['review']['profile_id'], pid)

    def test_explicit_reviewer_fallback_is_recorded(self):
        register(self)
        self.submitted()
        record = self.review_record('gpt-5.6-sol-max')
        self.deny(lambda: self.h.review('WP-00', 'agent:reviewer', 1, self.cand, record,
                                       profile_id='gpt-5.6-sol-max'))
        self.h.review('WP-00', 'agent:reviewer', 1, self.cand, record,
                       profile_id='gpt-5.6-sol-max', fallback=True, fallback_reason='Explicit reviewer fallback.')
        self.assertTrue(self.state()['tasks']['WP-00']['review']['fallback'])

    def test_full_model_lifecycle_and_dependency_release(self):
        register(self)
        result = self.submitted()
        self.h.review('WP-00', 'agent:reviewer', 1, self.cand, self.review_record())
        self.h.integrate('WP-00', 'astra', self.cand, self.head,
                         self.ev('integration', integrated_revision=self.head, runtime_stopped=True))
        self.h.complete('WP-00', 'astra')
        self.assertIn('WP-01', self.h.ready())
        self.assertIsNone(self.state()['tasks']['WP-00']['lease'])
        self.assertEqual(self.state()['tasks']['WP-00']['assignment']['profile_id'], result['profile_id'])

    def test_api_budget_is_retained_through_recovery(self):
        register(self, billing='api')
        self.h.admit('WP-00', 'astra')
        self.deny(lambda: self.assign())
        self.h.budget('human:owner', 2, self.ev('budget'))
        self.deny(lambda: self.assign())
        result = self.assign(budget_usd=2)
        self.release('WP-00', result)
        self.deny(lambda: self.assign(budget_usd=1), 'exhausted')

    def test_subscription_bounds_remain_enforced(self):
        register(self)
        self.h.admit('WP-00', 'astra')
        self.deny(lambda: self.assign(max_tokens=0))
        self.deny(lambda: self.assign(max_seconds=28801))
        self.deny(lambda: self.assign(budget_usd=1))

    def test_canonical_policy_digest_ignores_formatting_but_denies_semantic_change(self):
        register(self)
        self.policyfile.write_text(json.dumps(self.policy, sort_keys=True, indent=4))
        self.assertEqual(self.h.status()['routing_policy_digest'], hm.digest(self.policy))
        self.assign()
        policy = copy.deepcopy(self.policy)
        policy['work_package_routes'][0]['rationale'] += ' Changed decision.'
        self.policyfile.write_text(json.dumps(policy))
        self.deny(self.h.status, 'policy changed')
        self.deny(lambda: self.h.start('WP-00', 'agent:author', 1), 'policy changed')
        reloaded = hm.Harness(self.root, self.pkg, lambda: self.clock[0], self.policyfile)
        self.deny(reloaded.status, 'explicit reviewed migration')

    def test_v2_fields_cannot_be_smuggled_into_v1_evidence(self):
        record = self.ev('review', profile_id='gpt-6-astra-max')
        self.deny(lambda: self.h.evidence(record), 'unknown evidence fields')

    def test_actual_policy_covers_44_routes_and_limits_parent_downshifts(self):
        harness = hm.Harness(self.base / 'actual-policy', hm.PACKAGE)
        self.assertEqual(len(harness.routes), 44)
        counts = {tier: sum(r['author']['capability_floor'] == tier for r in harness.routes.values())
                  for tier in range(1, 5)}
        self.assertEqual(counts, {1: 13, 2: 27, 3: 4, 4: 0})
        self.assertEqual(sum(r['reviewer']['capability_floor'] == 1 for r in harness.routes.values()), 39)
        for row in harness.routes.values():
            for role in ('author', 'reviewer'):
                self.assertEqual(harness.profiles[row[role]['default_profile_id']]['reasoning_effort'], 'max')
                self.assertNotIn('gpt-5.6-luna-low', row[role]['allowed_profile_ids'])
        harness.init()
        harness.admit('WP-00', 'astra')
        with self.assertRaises(hm.Denied):
            harness.assign('WP-00', 'astra', 'human:mechanical', 4, human=True)
        with self.assertRaisesRegex(hm.Denied, 'not allowed'):
            harness.assign('WP-00', 'astra', 'agent:author', 3, profile_id='gpt-5.6-terra-medium')


class MigrationTests(unittest.TestCase):
    ev = old_tests.HarnessTests.ev
    begin = old_tests.HarnessTests.begin
    submit = old_tests.HarnessTests.submit
    reviewed = old_tests.HarnessTests.reviewed
    integrated = old_tests.HarnessTests.integrated
    tearDown = old_tests.HarnessTests.tearDown

    def setUp(self):
        prepare(self, migrate=False)
        self.v2, self.h = self.h, self.v1

    def deny(self, call):
        before = self.h.statefile.read_bytes()
        before_files = sorted(path.name for path in self.h.dir.iterdir())
        with self.assertRaises(hm.Denied):
            call()
        self.assertEqual(before, self.h.statefile.read_bytes())
        self.assertEqual(before_files, sorted(path.name for path in self.h.dir.iterdir()))

    def test_migration_dry_run_then_preserves_history_and_receipt_prefix(self):
        fence = self.begin('WP-03')
        self.h.recover('WP-03', 'astra', self.ev('recovery', 'WP-03', previous_fence=fence,
                                               runtime_stopped=True, observed_revision=self.cand))
        self.integrated()
        self.h.complete('WP-00', 'astra')
        before = self.h.statefile.read_bytes()
        old = json.loads(before)
        result = self.v2.migrate_v1('human:owner')
        self.assertTrue(result['dry_run'])
        self.assertEqual(before, self.h.statefile.read_bytes())
        self.assertFalse(Path(result['backup']).exists())
        result = self.v2.migrate_v1('human:owner', apply=True)
        new = json.loads(self.h.statefile.read_text())
        self.assertEqual(new['version'], '2.0')
        self.assertEqual(new['tasks'], old['tasks'])
        self.assertEqual(new['events'][:-1], old['events'])
        self.assertEqual(new['events'][-1]['previous_hash'], old['events'][-1]['hash'])
        self.assertEqual(new['events'][-1]['migration']['source_sha256'], hm.file_hash(Path(result['backup'])))
        self.assertEqual(before, Path(result['backup']).read_bytes())
        self.assertEqual(self.v2.status()['version'], '2.0')

    def test_migration_refuses_live_and_expired_leases(self):
        self.begin()
        self.deny(lambda: self.v2.migrate_v1('human:owner', apply=True))
        self.clock[0] += 4000
        self.deny(lambda: self.v2.migrate_v1('human:owner', apply=True))

    def test_migration_refuses_uncertain_states_even_without_lease(self):
        self.begin()
        self.h.change('fixture', 'simulate-inconsistent-stop', lambda s: s['tasks']['WP-00'].update(lease=None))
        self.deny(lambda: self.v2.migrate_v1('human:owner', apply=True))

    def test_migration_refuses_unrecovered_blocked_assignment(self):
        self.begin()
        self.h.block('WP-00', 'astra', self.ev('checkpoint'))
        self.h.change('fixture', 'simulate-lost-lease', lambda s: s['tasks']['WP-00'].update(lease=None))
        self.deny(lambda: self.v2.migrate_v1('human:owner', apply=True))

    def test_migration_refuses_corrupt_receipts_and_missing_chain(self):
        original = self.h.statefile.read_bytes()
        for mutate in [lambda s: s['events'][0].update(actor='forged'), lambda s: s.update(events=[])]:
            state = json.loads(original)
            mutate(state)
            self.h.statefile.write_text(json.dumps(state))
            self.deny(lambda: self.v2.migrate_v1('human:owner', apply=True))

    def test_old_roster_is_invalidated_not_promoted(self):
        old_tests.HarnessTests.roster(self)
        old = json.loads(self.h.statefile.read_text())
        self.v2.migrate_v1('human:owner', apply=True)
        new = json.loads(self.h.statefile.read_text())
        self.assertEqual(new['roster'], [])
        self.assertEqual(new['routing_migration']['old_roster_digest'], hm.digest(old['roster']))
        self.v2.admit('WP-00', 'astra')
        self.deny(lambda: self.v2.assign('WP-00', 'astra', 'agent:author', 2))

    def test_migration_idempotency_preserves_fresh_v2_roster(self):
        self.v2.migrate_v1('human:owner', apply=True)
        self.h = self.v2
        register(self)
        before = self.h.statefile.read_bytes()
        before_files = sorted(path.name for path in self.h.dir.iterdir())
        result = self.h.migrate_v1('human:owner', apply=True)
        self.assertTrue(result['already_current'])
        self.assertEqual(before, self.h.statefile.read_bytes())
        self.assertEqual(before_files, sorted(path.name for path in self.h.dir.iterdir()))

    def test_failed_migration_retains_exact_v1_and_checkpoint(self):
        before = self.h.statefile.read_bytes()
        with mock.patch.object(hm, 'atomic_write', side_effect=OSError('injected replace failure')):
            with self.assertRaises(OSError):
                self.v2.migrate_v1('human:owner', apply=True)
        self.assertEqual(before, self.h.statefile.read_bytes())
        self.h.status()
        backups = list(self.h.dir.glob('state.v1.*.json'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), before)
        self.assertTrue(self.v2.migrate_v1('human:owner', apply=True)['migrated'])

    def test_immediate_rollback_keeps_both_checkpoints_and_restores_exact_bytes(self):
        before = self.h.statefile.read_bytes()
        self.v2.migrate_v1('human:owner', apply=True)
        current = self.h.statefile.read_bytes()
        self.deny(lambda: self.v2.rollback_v2('human:owner', apply=True))
        dry = self.v2.rollback_v2('human:owner', runtime_stopped=True)
        self.assertTrue(dry['dry_run'])
        self.assertEqual(current, self.h.statefile.read_bytes())
        result = self.v2.rollback_v2('human:owner', apply=True, runtime_stopped=True)
        self.assertEqual(before, self.h.statefile.read_bytes())
        self.assertEqual(current, Path(result['retained_v2_checkpoint']).read_bytes())
        self.h.status()

    def test_rollback_refuses_after_any_later_v2_receipt(self):
        self.v2.migrate_v1('human:owner', apply=True)
        self.v2.admit('WP-00', 'astra')
        self.deny(lambda: self.v2.rollback_v2('human:owner', apply=True, runtime_stopped=True))

    def test_migration_boundary_proof_must_remain_present(self):
        self.v2.migrate_v1('human:owner', apply=True)
        self.v2.change('fixture', 'remove-boundary-proof', lambda s: s.pop('routing_migration'))
        self.deny(self.v2.status)

    def test_migration_refuses_changed_work_package_baseline(self):
        self.v2.package_hash = '0' * 64
        self.deny(lambda: self.v2.migrate_v1('human:owner', apply=True))

    def test_migration_refuses_non_owner_and_changed_terminal_evidence(self):
        self.deny(lambda: self.v2.migrate_v1('agent:author', apply=True))
        self.integrated()
        task = json.loads(self.h.statefile.read_text())['tasks']['WP-00']
        path = self.root / task['integration']['evidence']['path']
        path.write_text(path.read_text() + ' ')
        self.deny(lambda: self.v2.migrate_v1('human:owner', apply=True))

    def test_cli_init_context_check_and_dry_run_migration(self):
        root = self.base / 'cli-root'
        hm.legacy.Harness(root, hm.PACKAGE).init()
        command = [sys.executable, str(hm.PROJECT / 'tooling/coordination/harness.py'), '--root', str(root)]
        for arguments in [
            ['migrate-v1', '--actor', 'human:owner'],
            ['migrate-v1', '--actor', 'human:owner', '--apply'],
            ['check'], ['context', 'WP-00'], ['status'],
        ]:
            result = subprocess.run(command + arguments, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIsInstance(json.loads(result.stdout), dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
