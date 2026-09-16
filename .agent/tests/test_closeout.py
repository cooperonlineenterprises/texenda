"""Negative oracles for reviewed-source integration and current dossier status."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.agent/scripts'))
import common
import operating


class ReviewedIntegrationCloseoutTests(unittest.TestCase):
    def reject_record(self, path, mutate):
        changed = copy.deepcopy(common.load_json(ROOT / path))
        mutate(changed)
        actual = operating.load_json

        def replaced(target):
            return changed if target == ROOT / path else actual(target)

        with mock.patch.object(operating, 'load_json', side_effect=replaced), \
                self.assertRaises(common.ValidationError):
            operating.validate_closeout(ROOT)

    @staticmethod
    def item(value, identifier, key='items'):
        return next(row for row in value[key] if row['id'] == identifier)

    def test_exact_review_and_integration_are_distinct_repository_only_observations(self):
        actual = operating.stable_file_bytes

        def no_current_projection(path, *args, **kwargs):
            self.assertNotIn(path.relative_to(ROOT).as_posix(), common.GENERATED_OUTPUT_PATHS)
            return actual(path, *args, **kwargs)

        with mock.patch.object(operating, 'stable_file_bytes', side_effect=no_current_projection), \
                mock.patch.object(common, 'binding', side_effect=AssertionError('binding read')), \
                mock.patch.object(common, 'ledger_facts', side_effect=AssertionError('ledger read')):
            result = operating.validate_closeout(ROOT)
        self.assertEqual(result['reviewed_candidate_revision'], operating.REVIEWED_CANDIDATE)
        self.assertEqual(result['observed_integration_revision'], operating.REMEDIATION_INTEGRATION)
        self.assertNotEqual(result['reviewed_candidate_revision'], result['observed_integration_revision'])
        self.assertEqual(result['completed_remediations'], 7)
        self.assertEqual(result['integrated_audit_record'], 'not_separately_committed')

    def test_current_finding_rejects_candidate_status_or_wrong_evidence_subject(self):
        for fields in (
            {'classification': 'gated'},
            {'subject': 'Standalone source remediation candidate'},
            {'disposition': 'candidate_requires_independent_source_and_control_review'},
            {'evidence': operating.REMEDIATION},
            {'reviewed_candidate_revision': operating.REMEDIATION_INTEGRATION},
            {'observed_integration_revision': operating.REVIEWED_CANDIDATE},
            {'integration_record': {'owner_path': operating.PLAN, 'record_id': 'PLAN-0005'}},
        ):
            with self.subTest(fields=fields):
                self.reject_record(operating.FINDINGS, lambda value: self.item(
                    value, 'FIND-0007', 'findings').update(fields))

    def test_completed_plans_reject_candidate_proposed_pending_and_missing_review(self):
        for identifier in ('PLAN-0005', 'PLAN-0006'):
            for fields in (
                *({'status': status} for status in ('candidate', 'proposed', 'pending')),
                {'completion_evidence': None},
                {'reviewed_candidate_revision': operating.REMEDIATION_INTEGRATION},
                {'reviewed_candidate_tree': '0' * 40},
                {'observed_integration_revision': operating.REVIEWED_CANDIDATE},
            ):
                with self.subTest(identifier=identifier, fields=fields):
                    self.reject_record(operating.PLAN, lambda value: self.item(value, identifier).update(fields))
        self.reject_record(operating.PLAN, lambda value: self.item(
            value, 'PLAN-0005')['source_revisions'].pop())

    def test_integration_cannot_relabel_candidate_approval_or_invent_final_audit(self):
        for fields in (
            {'candidate_review_scope': 'integrated_head_approved'},
            {'review_evidence_revision': operating.REVIEWED_CANDIDATE},
            {'observed_integration_tree': '0' * 40},
            {'integrated_audit_record': 'separately_committed'},
        ):
            with self.subTest(fields=fields):
                self.reject_record(operating.PLAN, lambda value: self.item(value, 'PLAN-0006').update(fields))
        generated = self.item(common.load_json(ROOT / operating.PLAN), 'PLAN-0006')['generated_evidence']
        for key in generated:
            with self.subTest(generated_field=key):
                self.reject_record(operating.PLAN, lambda value: self.item(
                    value, 'PLAN-0006')['generated_evidence'].update({key: 'incorrect'}))

    def test_every_implemented_remediation_requires_consistent_completed_disposition(self):
        for identifier in sorted(operating.REVIEWED_REMEDIATIONS):
            for mutate in (
                lambda row: row.update(still_valid=True),
                lambda row: row.update(selected_disposition='fix_in_this_candidate'),
                lambda row: row['completion_evidence'].update(status='candidate_requires_independent_review'),
                lambda row: row['completion_evidence'].update(
                    reviewed_candidate_revision=operating.REMEDIATION_INTEGRATION),
            ):
                with self.subTest(identifier=identifier, mutate=mutate):
                    self.reject_record(operating.REMEDIATION, lambda value: mutate(self.item(value, identifier)))

    def test_current_defect_text_baseline_history_and_retained_dispositions_cannot_drift(self):
        for mutate in (
            lambda row: row['current_evidence'][0].update(observation='Rewritten historical baseline'),
            lambda row: row['current_evidence'][1].update(subject='current_source_candidate'),
            lambda row: row['current_evidence'][1].update(subject_revision=operating.REVIEWED_CANDIDATE),
            lambda row: row.update(practical_impact='Availability currently calls the refresh writer.'),
            lambda row: row.update(validity_scope='Acceptance still pending.'),
            lambda row: row['completion_evidence']['integration_record'].update(record_id='PLAN-0005'),
        ):
            self.reject_record(operating.REMEDIATION, lambda value: mutate(self.item(value, 'REM-0001')))
        for identifier in ('REM-0005', 'REM-0006', 'REM-0013', 'REM-0015', 'REM-0016', 'REM-0018'):
            with self.subTest(retained_record=identifier):
                self.reject_record(operating.REMEDIATION, lambda value: self.item(
                    value, identifier)['completion_evidence'].update(status='completed'))

    def test_successor_preserves_exact_predecessor_and_all_prior_supersessions(self):
        for mutate in (
            lambda value: value.update(current_version='1.4.1-mapped-existing'),
            lambda value: value['records'].pop(),
            lambda value: value['records'][0].update(reason='rewritten history'),
            lambda value: value['records'][-1].update(prior_revision=operating.REVIEWED_CANDIDATE),
            lambda value: value['records'][-1].update(prior_sha256='0' * 64),
            lambda value: value['records'][-1].update(predecessor_status='unreviewed_candidate'),
        ):
            self.reject_record(operating.SUPERSESSION, mutate)

    def test_current_version_cannot_return_to_candidate_proposed_or_pending(self):
        actual = operating.stable_file_bytes
        for status in ('Candidate', 'Proposed', 'Pending'):
            def replaced(path, *args, **kwargs):
                raw = actual(path, *args, **kwargs)
                if path == ROOT / operating.VERSION:
                    return raw.replace(b'Current operational contract version:',
                                       (status + ' contract version:').encode())
                return raw

            with self.subTest(status=status), \
                    mock.patch.object(operating, 'stable_file_bytes', side_effect=replaced), \
                    self.assertRaises(common.ValidationError):
                operating.validate_closeout(ROOT)

    def test_wrong_parent_or_extra_post_candidate_source_change_is_rejected(self):
        actual = operating.git
        for target in ('parent', 'delta'):
            def replaced(*args, **kwargs):
                if target == 'parent' and args[:3] == ('show', '-s', '--format=%P'):
                    return '0' * 40 + '\n'
                result = actual(*args, **kwargs)
                if target == 'delta' and args[:2] == ('diff', '--name-status'):
                    return result + 'M\t.agent/scripts/validate.py\n'
                return result

            with self.subTest(target=target), mock.patch.object(operating, 'git', side_effect=replaced), \
                    self.assertRaises(common.ValidationError):
                operating.validate_closeout(ROOT)

    def test_historical_manifest_index_or_review_subject_cannot_be_substituted(self):
        actual = operating.git
        for path, revision, mutate in (
            ('.agent/generated/manifest.json', operating.REMEDIATION_INTEGRATION,
             lambda value: value['source_files'].pop()),
            ('project-dossier/machine-readable/evidence-index.json', operating.REMEDIATION_INTEGRATION,
             lambda value: value['evidence'].pop()),
            (operating.STANDALONE_REVIEW, operating.REVIEW_RECORDING,
             lambda value: value.update(candidate_revision=operating.REMEDIATION_INTEGRATION)),
        ):
            def replaced(*args, **kwargs):
                result = actual(*args, **kwargs)
                if args == ('show', revision + ':' + path):
                    value = common.loads(result)
                    mutate(value)
                    return json.dumps(value).encode()
                return result

            with self.subTest(path=path), mock.patch.object(operating, 'git', side_effect=replaced), \
                    self.assertRaises(common.ValidationError):
                operating.validate_closeout(ROOT)


if __name__ == '__main__':
    unittest.main()
