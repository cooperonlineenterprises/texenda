"""Planning-only owner/disposition/deferral negatives; no product acceptance."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.agent/scripts'))
import common
import product
import validate


class InitialProductRecordsTests(unittest.TestCase):
    def reject(self, relative, mutate, pattern=None):
        original = product.load_json
        changed = copy.deepcopy(original(ROOT / relative))
        mutate(changed)

        def reader(path):
            return copy.deepcopy(changed) if Path(path) == ROOT / relative else original(path)

        with mock.patch.object(product, 'load_json', side_effect=reader):
            if pattern:
                with self.assertRaisesRegex((common.ValidationError, ValueError), pattern):
                    product.validate_records(ROOT)
            else:
                with self.assertRaises((common.ValidationError, ValueError)):
                    product.validate_records(ROOT)

    def test_complete_records_are_planning_only(self):
        result = product.validate_records(ROOT)
        self.assertEqual((result['findings'], result['acceptance_extensions'],
                          result['product_deferrals']), (16, 18, 15))
        self.assertEqual(result['product_acceptance'], 'NOT_RUN')
        self.assertFalse(result['external_gate_clearance'])
        self.assertFalse(result['explicit_writes'])

    def test_missing_or_duplicate_finding_fails(self):
        self.reject(product.RECORD, lambda r: r['rows'].pop())
        self.reject(product.RECORD, lambda r: r['rows'][1].update(id='RI-0001'))

    def test_final_owner_supersession_cannot_revert_to_advice(self):
        for index in (4, 6):
            with self.subTest(index=index):
                self.reject(product.RECORD,
                            lambda r, index=index: r['rows'][index].update(
                                selected_disposition='retained'),
                            'final owner')

    def test_disposition_cannot_gain_requirement_authority_or_fields(self):
        self.reject(product.RECORD, lambda r: r.update(authority='canonical product requirements'))
        self.reject(product.RECORD, lambda r: r['rows'][0].update(product_gate_passed=True))

    def test_reference_escape_and_unknown_acceptance_fail(self):
        self.reject(product.RECORD,
                    lambda r: r['rows'][0]['authoritative_owners'].append('../outside'),
                    'escapes')
        self.reject(product.RECORD,
                    lambda r: r['rows'][0]['acceptance_refs'].append('AC-IP99'),
                    'traceability')

    def test_research_provenance_cannot_be_rebound(self):
        self.reject(product.RECORD,
                    lambda r: r['source_packages'][0].update(manifest_sha256='0' * 64),
                    'provenance')

    def test_planning_cannot_be_called_product_acceptance(self):
        self.reject(product.RECORD,
                    lambda r: r['rows'][0]['completion_evidence'].update(scope='product PASS'),
                    'overclaims')

    def test_deferred_items_need_owner_trigger_evidence_and_recovery(self):
        for field, value in (('owner', ''), ('blocker', ''), ('trigger', ''),
                             ('required_evidence', []), ('next_action', ''),
                             ('recovery', ''), ('risk', '')):
            with self.subTest(field=field):
                self.reject(product.RAIDQ,
                            lambda r, field=field, value=value: next(
                                x for x in r['items'] if x['id'] == 'RAIDQ-0011').update(
                                    {field: value}))

    def test_gate_clearance_and_unknown_dependencies_fail(self):
        self.reject(product.RAIDQ, lambda r: r['items'][-1].update(status='passed'))
        self.reject(product.RAIDQ, lambda r: r['items'][-1]['dependencies'].append('VAL-999'))

    def test_prior_accepted_raidq_records_are_preserved(self):
        self.reject(product.RAIDQ, lambda r: r['items'][4].update(status='passed'),
                    'prior RAIDQ')

    def test_required_read_only_commands_cannot_be_disabled(self):
        original = validate.load_json
        for name in ('effective-product-plan', 'initial-product-records',
                     'coordination-state-check'):
            with self.subTest(command=name):
                registry = copy.deepcopy(original(ROOT / '.agent/validators.json'))
                next(r for r in registry['commands'] if r['id'] == name)['run_in_check'] = False
                with mock.patch.object(validate, 'load_json',
                    side_effect=lambda p: registry if Path(p) == ROOT / '.agent/validators.json'
                    else original(p)):
                    with self.assertRaises(common.ValidationError):
                        validate.validate_registry(ROOT)

    def test_plan_synthetic_closure_preserves_real_boundaries(self):
        plan = product.plan_module(ROOT).load_plan(ROOT)
        # The engine tests exact dependency edges; this independently checks the
        # initial release and its honest distinction from production operation.
        profiles = {p['id']: p for p in plan.profiles['profiles']}
        summary = plan.summary()
        self.assertFalse(summary['live_state_checked'])
        self.assertEqual(summary['product_implementation'], 'NOT_ASSESSED')
        self.assertNotIn('activation_required', summary)
        self.assertNotIn('product_implemented', summary)
        synthetic = profiles['initial-synthetic']
        self.assertEqual(synthetic['requires_gates'], [])
        self.assertTrue({'WP-12', 'WP-27', 'WP-29', 'WP-31', 'WP-32'}
                        <= set(synthetic['requires_work_packages']))
        self.assertFalse(set(plan.contract['synthetic_forbidden_dependencies'])
                         & set(synthetic['requires_work_packages']))
        self.assertTrue({'VAL-09', 'VAL-11', 'VAL-10', 'VAL-08'}
                        <= set(profiles['initial-production']['requires_gates']))
        self.assertNotIn('AC-IP18', profiles['initial-production']['required_criteria'])
        self.assertFalse({'AC-M04', 'AC-M05', 'AC-M06', 'AC-M07', 'AC-M09'}
                         & set(profiles['initial-production']['required_criteria']))
        self.assertIn('WP-20', profiles['email-pilot']['requires_work_packages'])
        self.assertEqual(profiles['assisted-workspace']['parents'], ['initial-production'])
        self.assertEqual(profiles['external-agent']['parents'], ['assisted-workspace'])
        for identifier in ('assisted-workspace', 'external-agent'):
            self.assertFalse({'WP-20', 'WP-33'}
                             & set(plan.profile_closure(identifier)['work_packages']))
        work = {w['id']: w for w in plan.catalog['work_packages']}
        self.assertIn('WP-15', work['WP-12']['dependencies'])
        self.assertEqual(plan.catalog['work_packages'][0]['id'], 'WP-00')


if __name__ == '__main__':
    unittest.main()
