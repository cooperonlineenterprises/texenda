"""Synthetic plan/activation tests; no live ledger, model, network or product proof."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('effective_plan_test_harness',
                                             PROJECT / 'tooling/coordination/harness.py')
hm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hm)
pm = hm.effective_plan


class PlanFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve() / 'repo'
        self.root.mkdir()
        shutil.copytree(PROJECT / 'specs/texenda-handoff', self.root / 'specs/texenda-handoff')
        shutil.copytree(PROJECT / 'tooling/coordination', self.root / 'tooling/coordination')
        for rel in (pm.DECISION, 'docs/decisions/ADR-0001-quality-first-model-routing.md'):
            destination = self.root / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(PROJECT / rel, destination)
        self.adr = self.root / pm.DECISION
        self.original_adr = self.adr.read_text()
        self.contract = pm.load_plan(self.root).contract

    def tearDown(self):
        self.temp.cleanup()

    def write_contract(self, contract):
        before, machine = self.original_adr.split(pm.MARKER)
        _old, after = machine.split('```json', 1)[1].split('```', 1)
        self.adr.write_text(before + pm.MARKER + '\n```json\n' + json.dumps(contract, indent=2) + '\n```' + after)

    def mutate(self, change):
        contract = copy.deepcopy(self.contract)
        change(contract)
        self.write_contract(contract)

    def denies(self, change, match='.'):
        self.mutate(change)
        with self.assertRaisesRegex((pm.PlanError, ValueError, OSError), match):
            pm.load_plan(self.root)
        self.adr.write_text(self.original_adr)


class PlanTests(PlanFixture):
    def test_exact_composition_and_stage_closures(self):
        plan = pm.load_plan(self.root)
        self.assertEqual(plan.digest, pm.load_plan(self.root).digest)
        self.assertEqual(set(plan.work), pm.WPS)
        self.assertEqual(len(plan.changed_work_packages), 29)
        self.assertEqual(len(plan.acceptance['criteria']), 143)
        sealed = json.loads((self.root / pm.BASES['sealed_catalog_sha256'][0]).read_text())
        self.assertEqual(plan.work['WP-00'], sealed['work_packages'][0])
        synthetic = plan.profile_closure('initial-synthetic')
        self.assertFalse(set(synthetic['work_packages']) & pm.FORBIDDEN_SYNTHETIC)
        self.assertEqual(synthetic['requires_gates'], [])
        self.assertIn('AC-IP12', synthetic['required_criteria'])
        self.assertIn('WP-18', next(row for row in plan.contract['acceptance_extensions'] if row['id'] == 'AC-IP12')['work_packages'])
        production = plan.profile_closure('initial-production')
        self.assertEqual(set(production['requires_gates']), {'VAL-02', 'VAL-03', 'VAL-04', 'VAL-05', 'VAL-06', 'VAL-08', 'VAL-09', 'VAL-10', 'VAL-11'})
        self.assertNotIn('AC-IP18', production['required_criteria'])
        self.assertNotIn('AC-IP18', plan.work['WP-17']['acceptance_ids'])
        self.assertFalse(pm.POST_ACTIVATION_CRITERIA & set(production['required_criteria']))
        self.assertTrue(pm.POST_ACTIVATION_CRITERIA <= set(plan.profile_closure('email-pilot')['required_criteria']))
        self.assertIn('WP-20', plan.profile_closure('email-pilot')['work_packages'])
        self.assertIn('WP-15', plan.work['WP-12']['dependencies'])
        self.assertEqual(plan.profile_closure('email-pilot')['requires_gates'], production['requires_gates'])
        self.assertEqual(production['evidence_status'], 'NOT_ASSESSED')
        self.assertFalse((self.root / '.texenda').exists())

    def test_closed_shape_and_types(self):
        mutations = [
            lambda c: c.update(unknown=True),
            lambda c: c.pop('authority'),
            lambda c: c.update(work_package_updates=c['work_package_updates'][:-1]),
            lambda c: c['work_package_updates'][0].update(extra='bad'),
            lambda c: c['work_package_updates'][0]['append'].update(risk_level=['low']),
            lambda c: c['work_package_updates'][0]['replace'].update(dependencies='WP-00'),
            lambda c: c['work_package_updates'][0]['append'].update(allowed_paths=[True]),
            lambda c: c['coordinator_boundary'].update(implicit_activation=0),
            lambda c: c['acceptance_extensions'][0].update(evidence_status='PASS'),
            lambda c: c['additional_profiles'][0].update(extra=True),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.denies(mutation)

    def test_missing_duplicate_blocks_and_duplicate_keys(self):
        values = [self.original_adr.replace(pm.MARKER, ''),
                  self.original_adr + pm.MARKER,
                  self.original_adr + '\n```json\n{}\n```\n',
                  self.original_adr.replace('"id": "PLAN-IP-0001",', '"id": "PLAN-IP-0001", "id": "PLAN-IP-0001",')]
        for value in values:
            self.adr.write_text(value)
            with self.assertRaises(pm.PlanError):
                pm.load_plan(self.root)

    def test_unknown_duplicate_references_and_cycles(self):
        mutations = [
            lambda c: c['work_package_updates'][0].update(id='WP-99'),
            lambda c: c['work_package_updates'][1].update(id='WP-01'),
            lambda c: c['work_package_updates'][0]['replace'].update(dependencies=['WP-99']),
            lambda c: c['work_package_updates'][0]['replace'].update(dependencies=['WP-01']),
            lambda c: c['work_package_updates'][0]['replace'].update(dependencies=['WP-02']),
            lambda c: c['work_package_updates'][0]['append'].update(acceptance_ids=['AC-NOPE']),
            lambda c: c['work_package_updates'][0]['replace'].update(external_gates_for_activation=['VAL-99']),
            lambda c: c['acceptance_extensions'][0].update(sealed_criteria=['AC-IP01']),
            lambda c: c['acceptance_extensions'][0].update(work_packages=['WP-99']),
            lambda c: c['additional_profiles'][0].update(parents=['email-pilot']),
            lambda c: c['additional_profiles'][0].update(parents=['absent-profile']),
            lambda c: c['additional_profiles'][0].update(required_criteria=['AC-UNKNOWN']),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.denies(mutation)

    def test_path_escape_base_hash_and_symlink_denied(self):
        for value in ('../outside', '/outside', 'safe/../../outside', 'safe//nested', 'safe\\nested', '.'):
            self.denies(lambda c, value=value: c['work_package_updates'][0]['append'].update(allowed_paths=[value]))
        self.denies(lambda c: c.update(sealed_catalog_sha256='0' * 64), 'hash')
        path = self.root / pm.BASES['sealed_profiles_sha256'][0]
        raw = path.read_bytes()
        path.write_bytes(raw + b'\n')
        with self.assertRaisesRegex(pm.PlanError, 'hash'):
            pm.load_plan(self.root)
        path.unlink()
        path.symlink_to(PROJECT / pm.BASES['sealed_profiles_sha256'][0])
        with self.assertRaises((pm.PlanError, OSError)):
            pm.load_plan(self.root)

    def test_stage_gate_and_acceptance_weakening_denied(self):
        def update(c, wid):
            return next(row for row in c['work_package_updates'] if row['id'] == wid)
        mutations = [
            lambda c: c['additional_profiles'][0]['requires_work_packages'].append('WP-18'),
            lambda c: c['additional_profiles'][0]['requires_gates'].append('VAL-09'),
            lambda c: c['additional_profiles'][1]['requires_gates'].remove('VAL-09'),
            lambda c: c['additional_profiles'][1]['requires_gates'].remove('VAL-04'),
            lambda c: c['additional_profiles'][1]['required_criteria'].append('AC-IP18'),
            lambda c: c['additional_profiles'][1]['required_criteria'].remove('AC-D01'),
            lambda c: c['additional_profiles'][1]['required_criteria'].append('AC-M05'),
            lambda c: c['additional_profiles'][0].update(evidence_mode='real-qualified'),
            lambda c: c['synthetic_forbidden_dependencies'].remove('WP-30'),
            lambda c: update(c, 'WP-32')['replace'].update(external_gates_for_activation=['VAL-09']),
            lambda c: update(c, 'WP-20')['replace']['external_gates_for_activation'].remove('VAL-09'),
            lambda c: update(c, 'WP-17')['replace']['external_gates_for_activation'].remove('VAL-03'),
            lambda c: update(c, 'WP-12')['replace']['dependencies'].remove('WP-15'),
            lambda c: update(c, 'WP-18')['replace']['acceptance_ids'].append('AC-M04'),
            lambda c: c['profile_updates'][0]['append'].update(requires_work_packages=[]),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.denies(mutation)


class ActivationTests(PlanFixture):
    def setUp(self):
        super().setUp()
        self.clock = 1789660800.0
        self.git('init', '-q')
        self.git('add', 'specs', 'tooling', 'docs')
        self.git('-c', 'user.name=Synthetic fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'Synthetic reviewed candidate')
        self.candidate = self.git('rev-parse', 'HEAD').strip()
        self.tree = self.git('rev-parse', 'HEAD^{tree}').strip()
        self.h = hm.Harness(self.root, clock=lambda: self.clock,
                            package=self.root / 'specs/texenda-handoff',
                            policy=self.root / 'tooling/coordination/routing-policy.json')
        self.h.init('human:fixture')
        self.count = 0
        rows = []
        for p in self.h.profiles.values():
            rows.append(dict(profile_id=p['profile_id'], capability_tier=p['capability_tier'],
                             model_id=p['model_id'], reasoning_effort=p['reasoning_effort'],
                             runtime_id='fixture-runtime', client_version='synthetic',
                             sign_in_mode='synthetic', billing_mode='subscription',
                             capabilities=['read', 'edit', 'test'], verified_at=hm.utc(self.clock),
                             expires_at=hm.utc(self.clock + 86400), qualification_check_ids=['fixture']))
        self.h.roster('human:fixture', self.ev('roster', qualifications=rows,
                                             routing_policy_digest=self.h.policy_hash))

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True,
                              text=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0')).stdout

    def ev(self, kind, wid=None, active=False, **fields):
        self.count += 1
        directory = self.root / 'evidence'
        directory.mkdir(exist_ok=True)
        log = directory / f'check-{self.count}.txt'
        log.write_text('PASS: synthetic coordinator fixture; no product qualification.\n')
        data = {'schema_version': '2.1' if active else '2.0', 'kind': kind, 'summary': 'Synthetic fixture.',
                'checks': [{'id': 'fixture', 'required': True, 'status': 'PASS',
                            'command_or_procedure': 'Deterministic local synthetic fixture',
                            'evidence_path': str(log.relative_to(self.root)), 'sha256': hm.file_hash(log)}]}
        if wid:
            data.update(task_id=wid, candidate_revision=self.candidate)
        if active:
            data['effective_plan_digest'] = self.h.effective.digest
        data.update(fields)
        path = directory / f'{kind}-{self.count}.json'
        path.write_text(json.dumps(data))
        return str(path.relative_to(self.root))

    def state(self):
        return json.loads(self.h.statefile.read_bytes())

    def activation_record(self, **overrides):
        preview = self.h.activate_plan('agent:integrator')
        q = self.h.qualified(self.state(), 'gpt-6-astra-max')
        record = self.ev('plan-activation')
        path = self.root / record
        data = json.loads(path.read_text())
        check = data['checks'][0]
        data.update(schema_version='texenda.plan-activation.v1', actor='agent:integrator',
                    authors=['agent:author', 'agent:integrator'], reviewer='agent:independent-reviewer',
                    owner_request='Explicit synthetic test authority; not a live activation.',
                    reviewer_profile_id='gpt-6-astra-max', reviewer_qualification_digest=hm.digest(q),
                    candidate_revision=self.candidate, candidate_tree=self.tree, runtime_stopped=True,
                    **{key: preview[key] for key in ('effective_plan_digest', 'source_refs',
                       'source_state_sha256', 'source_receipt_count', 'source_receipt_head')})
        data['checks'] = [dict(check, id='independent-review'), dict(check, id='runtime-stop')]
        data.update(overrides)
        path.write_text(json.dumps(data))
        return record

    def activate(self):
        record = self.activation_record()
        self.h.activate_plan('agent:integrator', record, apply=True)
        return record

    def deny(self, call, pattern='.'):
        raw = self.h.statefile.read_bytes()
        with self.assertRaisesRegex((hm.Denied, pm.PlanError, OSError, ValueError), pattern):
            call()
        self.assertEqual(raw, self.h.statefile.read_bytes())

    def lifecycle(self, wid, active=False):
        plan = self.h.effective.digest if active else None
        self.h.admit(wid, 'fixture', plan_digest=plan)
        context = self.h.context(wid) if active else {}
        result = self.h.assign(wid, 'fixture', 'human:author', human=True,
                               plan_digest=plan, context_digest=context.get('context_digest'))
        self.h.start(wid, 'human:author', result['fence'])
        path = self.h.work[wid]['allowed_paths'][0] + '/fixture.txt'
        self.h.submit(wid, 'human:author', result['fence'], self.candidate,
                      self.ev('submission', wid, active, changed_paths=[path]))
        self.h.review(wid, 'human:reviewer', 1, self.candidate,
                      self.ev('review', wid, active), human=True)
        self.h.integrate(wid, 'fixture', self.candidate, self.candidate,
                         self.ev('integration', wid, active, integrated_revision=self.candidate, runtime_stopped=True))
        self.h.complete(wid, 'fixture')

    def test_dry_run_reads_without_state_checkpoint_or_lock_write(self):
        raw = self.h.statefile.read_bytes()
        self.h.lockfile.unlink()
        preview = self.h.activate_plan('agent:integrator')
        self.assertTrue(preview['dry_run'])
        self.assertFalse(self.h.lockfile.exists())
        self.assertFalse(Path(preview['checkpoint']).exists())
        self.assertEqual(raw, self.h.statefile.read_bytes())
        context = self.h.context('WP-01')
        self.assertFalse(context['dispatch_valid'])
        self.assertEqual(context['effective_plan']['mode'], 'sealed-unbound')
        self.assertFalse(self.h.lockfile.exists())

    def test_activation_preserves_completed_history_roster_budget_and_receipts(self):
        self.lifecycle('WP-00')
        raw, old = self.h.statefile.read_bytes(), self.state()
        self.activate()
        current = self.state()
        self.assertEqual(current['version'], '2.1')
        for field in ('work_package_digest', 'tasks', 'roster', 'budget_usd', 'budget_approval', 'gates', 'routing_migration'):
            self.assertEqual(current.get(field), old.get(field), field)
        self.assertEqual(current['events'][:-1], old['events'])
        self.assertEqual((self.h.dir / current['plan_activation']['checkpoint_name']).read_bytes(), raw)
        self.assertTrue(self.h.status()['profiles'][0]['available'])
        active = self.h.statefile.read_bytes()
        self.assertTrue(self.h.activate_plan('agent:integrator', apply=True)['already_current'])
        self.assertEqual(self.h.statefile.read_bytes(), active)
        self.deny(lambda: self.h.rollback_v2('human:owner', apply=True, runtime_stopped=True), 'forward|rollback')
        self.lifecycle('WP-01', active=True)
        self.assertEqual(self.state()['tasks']['WP-00'], old['tasks']['WP-00'])
        self.assertTrue(self.h.activate_plan('agent:integrator', apply=True)['already_current'])

    def test_review_runtime_source_and_qualification_evidence_negatives(self):
        cases = [dict(reviewer='agent:author'), dict(reviewer='agent:integrator'),
                 dict(runtime_stopped=False), dict(runtime_stopped=1),
                 dict(reviewer_profile_id='gpt-6-astra-high'), dict(reviewer_qualification_digest='0' * 64),
                 dict(source_state_sha256='0' * 64), dict(source_receipt_count=1),
                 dict(source_receipt_head='0' * 64), dict(effective_plan_digest='0' * 64),
                 dict(candidate_tree='0' * 40), dict(unrecognized=True)]
        for fields in cases:
            with self.subTest(fields=fields):
                record = self.activation_record(**fields)
                self.deny(lambda: self.h.activate_plan('agent:integrator', record, apply=True))
        self.deny(lambda: self.h.activate_plan('agent:integrator', apply=True), 'evidence')

    def test_unreviewed_source_missing_log_and_stale_state_denied(self):
        record = self.activation_record()
        data = json.loads((self.root / record).read_text())
        log = self.root / data['checks'][0]['evidence_path']
        log.write_text('changed')
        self.deny(lambda: self.h.activate_plan('agent:integrator', record, apply=True), 'log')
        record = self.activation_record()
        self.h.admit('WP-00', 'fixture')
        self.deny(lambda: self.h.activate_plan('agent:integrator', record, apply=True), 'unfinished')

    def test_every_lease_and_nonplanned_changed_scope_refused(self):
        original = self.h.statefile.read_bytes()
        for state_name in ('admitted', 'assigned', 'running', 'submitted', 'reviewed', 'integrated', 'completed', 'blocked', 'cancelled'):
            modified = json.loads(original)
            modified['tasks']['WP-01']['state'] = state_name
            self.h._event(modified, 'fixture', 'fixture-only')
            self.h.statefile.write_text(json.dumps(modified))
            self.deny(lambda: self.h.activate_plan('agent:integrator'), 'unfinished|changed scope')
        for expiry in (self.clock - 1, self.clock + 10):
            modified = json.loads(original)
            modified['tasks']['WP-00']['lease'] = {'expires_at': expiry}
            self.h._event(modified, 'fixture', 'fixture-only')
            self.h.statefile.write_text(json.dumps(modified))
            self.deny(lambda: self.h.activate_plan('agent:integrator'), 'lease')

    def test_checkpoint_corruption_refused_before_and_after_activation(self):
        record = self.activation_record()
        preview = self.h.activate_plan('agent:integrator')
        checkpoint = Path(preview['checkpoint'])
        checkpoint.write_text('corrupt')
        self.deny(lambda: self.h.activate_plan('agent:integrator', record, apply=True), 'checkpoint')
        checkpoint.unlink()
        self.h.activate_plan('agent:integrator', record, apply=True)
        checkpoint.write_text('corrupt')
        self.deny(lambda: self.h.status(), 'checkpoint')

    def test_sources_and_evidence_rechecked_at_exchange_and_commit(self):
        stages = ('after_final_state_comparison_before_replacement', 'state_write_before_exchange',
                  'after_state_replacement_before_validation', 'state_write_after_commit_candidate_cleanup')
        for stage in stages:
            with self.subTest(stage=stage):
                record = self.activation_record()
                raw = self.adr.read_bytes()
                fired = []
                def swap(observed, harness, detail):
                    if (observed == stage and not fired
                            and (stage != 'after_final_state_comparison_before_replacement'
                                 or detail.get('state_transaction_started'))):
                        fired.append(True)
                        self.adr.write_bytes(raw + b'\n')
                self.h.interleave = swap
                self.deny(lambda: self.h.activate_plan('agent:integrator', record, apply=True), 'source|binding')
                self.assertEqual(fired, [True])
                self.adr.write_bytes(raw)
                self.h.interleave = None
                self.h._plan_guards = []
                self.h._plan_checkpoint_guard = None
                self.assertFalse(hm.state_transaction_blocker_names(self.h.dir))

    def test_context_admission_assignment_and_lifecycle_bind_one_plan(self):
        self.activate()
        context = self.h.context('WP-00')
        self.assertTrue(context['dispatch_valid'])
        plan = context['effective_plan_digest']
        self.deny(lambda: self.h.admit('WP-00', 'fixture'), 'digest')
        self.h.admit('WP-00', 'fixture', plan_digest=plan)
        self.deny(lambda: self.h.assign('WP-00', 'fixture', 'agent:author', plan_digest=plan), 'context')
        result = self.h.assign('WP-00', 'fixture', 'agent:author', profile_id='gpt-6-astra-max',
                               plan_digest=plan, context_digest=context['context_digest'])
        self.assertEqual(result['effective_plan_digest'], plan)
        self.h.start('WP-00', 'agent:author', result['fence'])
        self.deny(lambda: self.h.submit('WP-00', 'agent:author', result['fence'], self.candidate,
                   self.ev('submission', 'WP-00', changed_paths=['tooling/fixture.txt'])), 'lifecycle')
        self.h.submit('WP-00', 'agent:author', result['fence'], self.candidate,
                      self.ev('submission', 'WP-00', active=True, changed_paths=['tooling/fixture.txt']))
        self.assertEqual(self.state()['tasks']['WP-00']['effective_plan_digest'], plan)
        self.assertEqual(self.state()['events'][-1]['effective_plan_digest'], plan)

    def test_active_plan_rejects_old_downshift_paid_authority_and_keeps_qualification(self):
        self.activate()
        context = self.h.context('WP-00')
        plan = context['effective_plan_digest']
        self.h.admit('WP-00', 'fixture', plan_digest=plan)
        options = dict(plan_digest=plan, context_digest=context['context_digest'])
        self.deny(lambda: self.h.assign('WP-00', 'fixture', 'agent:author',
                   profile_id='gpt-6-astra-high', **options), 'max effort')
        self.deny(lambda: self.h.assign('WP-00', 'fixture', 'agent:author',
                   profile_id='gpt-6-astra-max', budget_usd=1, **options), 'paid work')
        self.assertEqual(self.h.qualified(self.state(), 'gpt-6-astra-max')['reasoning_effort'], 'max')
        self.assertFalse(self.h.status()['budget_authorization']['available_for_new_paid_work'])

    def test_effective_allowed_paths_and_dependencies_are_used(self):
        self.activate()
        self.lifecycle('WP-00', active=True)
        self.deny(lambda: self.h.admit('WP-02', 'fixture', plan_digest=self.h.effective.digest), 'prerequisites')
        self.lifecycle('WP-01', active=True)
        context = self.h.context('WP-02')
        self.h.admit('WP-02', 'fixture', plan_digest=self.h.effective.digest)
        result = self.h.assign('WP-02', 'fixture', 'human:author', human=True,
                               plan_digest=self.h.effective.digest, context_digest=context['context_digest'])
        self.assertIn('tests/dev', result['paths'])
        self.assertIn('docs/development', result['paths'])
        self.assertEqual(self.h.work['WP-19']['dependencies'], ['WP-12', 'WP-14', 'WP-07'])
        self.assertEqual(self.h.work['WP-32']['external_gates_for_activation'], [])

    def test_private_evidence_unknown_fields_and_not_run_cannot_activate(self):
        self.deny(lambda: self.h.activate_plan('agent:integrator', 'private-inputs/proof.json', apply=True), 'private')
        record = self.activation_record()
        path = self.root / record
        original = json.loads(path.read_text())
        variants = []
        value = copy.deepcopy(original)
        value['checks'][0]['status'] = 'NOT_RUN'
        variants.append(value)
        value = copy.deepcopy(original)
        value['checks'][1]['required'] = False
        variants.append(value)
        value = copy.deepcopy(original)
        value['checks'][1]['evidence_path'] = 'private-inputs/stop.txt'
        variants.append(value)
        value = copy.deepcopy(original)
        value['checks'][1]['unknown'] = True
        variants.append(value)
        for value in variants:
            path.write_text(json.dumps(value))
            self.deny(lambda: self.h.activate_plan('agent:integrator', record, apply=True))

    def test_retained_proof_and_qualification_expiry_rechecked_before_commit(self):
        record = self.activation_record()
        roster_ref = self.state()['roster'][0]['evidence']
        roster = json.loads((self.root / roster_ref['path']).read_text())
        log = self.root / roster['checks'][0]['evidence_path']
        raw = log.read_bytes()
        fired = []
        def tamper(stage, harness, detail):
            if (stage == 'after_final_state_comparison_before_replacement' and not fired
                    and detail.get('state_transaction_started')):
                fired.append(True)
                log.write_bytes(b'changed retained qualification proof')
        self.h.interleave = tamper
        self.deny(lambda: self.h.activate_plan('agent:integrator', record, apply=True), 'evidence|log')
        log.write_bytes(raw)
        self.h.interleave = None
        self.h._plan_guards = []
        self.h._plan_checkpoint_guard = None
        fired.clear()
        def expire(stage, harness, detail):
            if (stage == 'after_final_state_comparison_before_replacement' and not fired
                    and detail.get('state_transaction_started')):
                fired.append(True)
                self.clock += 86400
        self.h.interleave = expire
        self.deny(lambda: self.h.activate_plan('agent:integrator', record, apply=True), 'qualification expired')
        self.assertEqual(fired, [True])

    def test_active_checkpoint_path_escape_and_source_changes_fail_closed(self):
        self.activate()
        raw = self.h.statefile.read_bytes()
        value = json.loads(raw)
        value['plan_activation']['checkpoint_name'] = '../private-inputs/checkpoint.json'
        self.h._event(value, 'fixture', 'fixture-tamper')
        self.h.statefile.write_text(json.dumps(value))
        self.deny(lambda: self.h.status(), 'binding')
        self.h.statefile.write_bytes(raw)
        self.adr.write_bytes(self.adr.read_bytes() + b'\n')
        self.deny(lambda: self.h.context('WP-01'), 'binding')

    def test_external_bound_activation_checkpoint_and_read_only_cli(self):
        raw, old = self.h.statefile.read_bytes(), self.state()
        external = self.root.parent / 'local/agent-state/texenda'
        external.parent.mkdir(parents=True)
        shutil.move(str(self.h.dir), external)
        binding = {'schema_version': hm.BINDING_VERSION, 'migration_id': 'fixture',
                   'repository_root': str(self.root), 'state_root': str(external), 'status': 'active',
                   'baseline': {'state_sha256': hashlib.sha256(raw).hexdigest(),
                                'receipt_count': len(old['events']), 'receipt_tip': old['events'][-1]['hash']}}
        (self.root / hm.BINDING_NAME).write_text(json.dumps(binding))
        self.h = hm.Harness(self.root, clock=lambda: self.clock, state_root=external,
                            package=self.root / 'specs/texenda-handoff',
                            policy=self.root / 'tooling/coordination/routing-policy.json')
        self.activate()
        meta = self.state()['plan_activation']
        self.assertEqual((external / meta['checkpoint_name']).read_bytes(), raw)
        self.assertFalse((self.root / '.texenda').exists())
        result = subprocess.run(['python3', '-B', str(self.root / 'tooling/coordination/harness.py'),
                                 '--root', str(self.root), '--state-root', str(external), '--read-only',
                                 'activate-plan', '--actor', 'fixture', '--apply'], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'read-only', result.stderr)

    def test_activation_interruption_uses_existing_state_write_recovery(self):
        record = self.activation_record()
        old = self.h.statefile.read_bytes()
        pid = os.fork()
        if pid == 0:
            def stop(stage, harness, detail):
                if stage == 'state_write_after_exchange_before_fsync':
                    os._exit(73)
            self.h.interleave = stop
            try:
                self.h.activate_plan('agent:integrator', record, apply=True)
            except BaseException:
                os._exit(98)
            os._exit(0)
        _pid, status = os.waitpid(pid, 0)
        self.assertTrue(os.WIFEXITED(status))
        self.assertEqual(os.WEXITSTATUS(status), 73)
        with self.assertRaisesRegex(hm.Denied, 'pending'):
            hm.Harness(self.root)
        recovery = hm.Harness(self.root, allow_state_recovery=True)
        result = recovery.recover_state_write('human:fixture', runtime_stopped=True)
        self.assertEqual(result['outcome'], 'previous_state_restored')
        self.assertEqual(self.h.statefile.read_bytes(), old)
        self.assertFalse(hm.state_transaction_blocker_names(self.h.dir))

    def test_synthetic_completion_cannot_clear_real_gates(self):
        self.activate()
        def seed(wid):
            evidence = self.ev('integration', wid, active=True, integrated_revision=self.candidate, runtime_stopped=True)
            def fixture(state):
                state['tasks'][wid].update(state='integrated', effective_plan_digest=self.h.effective.digest,
                    candidate=self.candidate, integration={'evidence': {'path': evidence,
                        'sha256': hm.file_hash(self.root / evidence)}})
            self.h.change('fixture', 'fixture-isolate-completion', fixture)
        seed('WP-32')
        self.h.complete('WP-32', 'fixture')
        self.assertEqual(self.state()['gates'], {})
        seed('WP-17')
        for gid in self.h.work['WP-17']['external_gates_for_activation']:
            if gid not in ('VAL-09', 'VAL-11'):
                self.h.gate('human:fixture', self.ev('gate', gate_id=gid, scope='Synthetic fixture only',
                            expires_at=hm.utc(self.clock + 3600), work_packages=['WP-17']))
        self.deny(lambda: self.h.complete('WP-17', 'fixture'), 'VAL-09')
        self.h.gate('human:fixture', self.ev('gate', gate_id='VAL-09', scope='Synthetic fixture only',
                    expires_at=hm.utc(self.clock + 3600), work_packages=['WP-17']))
        self.deny(lambda: self.h.complete('WP-17', 'fixture'), 'VAL-11')


if __name__ == '__main__':
    unittest.main()
