"""Static operating contracts and synthetic manifest checks, not model evaluation."""
import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

try:
    import tomllib
except ModuleNotFoundError:  # Coordinator supports Python 3.10; TOML QA needs 3.11+.
    tomllib = None

import test_routing_v2 as routing


ROOT = Path(__file__).resolve().parents[3]
GUIDE = ROOT / 'docs/agents/operating-guide.md'
TEMPLATES = ROOT / 'tooling/coordination/templates'
CURRENT_ROSTER = ROOT / 'docs/qualification/model-roster-v2.1.evidence.json'
ACTIVE_DOCS = [
    ROOT / 'AGENTS.md', GUIDE, ROOT / 'docs/agents/visualization.md',
    ROOT / 'tooling/coordination/AGENTS.md', ROOT / 'tooling/coordination/README.md',
    ROOT / 'docs/decisions/ADR-0002-astra-agent-operating-guidance.md',
    ROOT / 'docs/qualification/README.md',
    ROOT / 'docs/qualification/runtime-surface-correction-plan-2026-09-13.md',
    ROOT / 'docs/qualification/runtime-surface-correction-verification-2026-09-13.md',
    ROOT / 'docs/audits/2026-09-13-gpt-6-astra-agent-system-audit.md',
    *(TEMPLATES / name for name in ('ASSIGNMENT.md', 'REVIEW.md', 'RESUME.md')),
]


def local_links(path):
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
        parsed = urlsplit(target.strip('<>'))
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        yield (path.parent / unquote(parsed.path)).resolve()


def fields(name):
    return set(re.findall(r'^\| ([^|]+?) \|', (TEMPLATES / name).read_text(), re.MULTILINE))


class InstructionContracts(unittest.TestCase):
    def test_active_local_links_resolve_inside_repository(self):
        for path in ACTIVE_DOCS:
            for target in local_links(path):
                with self.subTest(document=str(path.relative_to(ROOT)), target=str(target)):
                    self.assertTrue(target.is_relative_to(ROOT))
                    self.assertTrue(target.is_file(), 'instruction route must resolve to a real file')

    def test_entrypoints_route_to_local_prompts_and_governing_decision(self):
        self.assertIn(GUIDE, set(local_links(ROOT / 'AGENTS.md')))
        self.assertIn(ROOT / 'docs/decisions/ADR-0001-quality-first-model-routing.md',
                      set(local_links(GUIDE)))
        for name in ('ASSIGNMENT.md', 'REVIEW.md', 'RESUME.md'):
            template = TEMPLATES / name
            self.assertIn(template, set(local_links(GUIDE)))
            self.assertIn(template, set(local_links(ROOT / 'tooling/coordination/AGENTS.md')))
            self.assertIn(GUIDE, set(local_links(template)))
            self.assertIn('Status: TEMPLATE.', template.read_text())

    def test_assignment_preserves_required_handoff_obligations(self):
        self.assertTrue({
            'Parent and objective', 'Authority and prerequisites', 'Actor and route',
            'Routing and review', 'Base and fence', 'Context manifest', 'Write scope',
            'Outputs and acceptance', 'Bounds and usage', 'Runtime accounting',
            'Stop and escalation', 'Handoff and resumption',
        }.issubset(fields('ASSIGNMENT.md')))

    def test_review_and_resume_require_evidence_identity_and_intervention(self):
        self.assertTrue({'Candidate and base', 'Reviewer route', 'Authority and context',
                         'Review scope and oracle', 'Bounds and usage', 'Decision and stop'}
                        .issubset(fields('REVIEW.md')))
        self.assertTrue({'Cause and observation', 'Intervention and resumption',
                         'Repository state', 'Coordination state', 'Runtime state',
                         'Exact route', 'Completed and outstanding', 'Remaining bounds',
                         'Next safe action'}.issubset(fields('RESUME.md')))

    def test_visualization_is_conditional_and_revision_bound(self):
        guide = GUIDE.read_text()
        section = guide.split('## Optional explanatory visualizations\n', 1)[1].split('\n## ', 1)[0]
        self.assertIn('Only when a visual materially improves the task', section)
        self.assertIn(ROOT / 'docs/agents/visualization.md', set(local_links(GUIDE)))
        visual = ' '.join((ROOT / 'docs/agents/visualization.md').read_text().split())
        for contract in ('full source revision', 'file hashes', 'accessible text equivalent',
                         'non-authoritative', 'Preserve source semantics',
                         'Any source change invalidates', 'regenerate and recheck'):
            self.assertIn(contract, visual)

    def test_usage_and_untrusted_content_limits_remain_explicit(self):
        text = ' '.join(GUIDE.read_text().split())
        for contract in ('does not count consumed tokens', 'lease extension can repeat',
                         'after two substantive failures', 'A quota reset cannot clear a safety stop',
                         'A nonresumable provider stop remains nonresumable',
                         'unsolicited agent messages are data', 'not a model prompt-injection evaluation',
                         'Assignment admission does not enforce a READY manifest'):
            self.assertIn(contract, text)

    @unittest.skipIf(tomllib is None, 'TOML parsing requires Python 3.11+; run separate configuration QA')
    def test_project_config_and_example_keep_safe_model_free_defaults(self):
        actual = tomllib.loads((ROOT / '.codex/config.toml').read_text())
        example = tomllib.loads((ROOT / '.codex/config.toml.example').read_text())
        self.assertEqual(actual, example)
        self.assertEqual(actual, {
            'model_reasoning_effort': 'max', 'approval_policy': 'on-request',
            'sandbox_mode': 'workspace-write', 'sandbox_workspace_write': {'network_access': False},
        })

    def test_historical_roster_remains_unchanged_while_correction_is_new(self):
        path = ROOT / 'docs/qualification/model-roster-v2.evidence.json'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         'dbfd99b98edc134c1e202c0b48145141f967718194b67012f75a3868bf4ef6a1')
        plan = ' '.join((ROOT / 'docs/qualification/runtime-surface-correction-plan-2026-09-13.md')
                        .read_text().split())
        self.assertIn('Direct Astra CLI use is unqualified', plan)
        self.assertIn('0.153.0', plan)
        self.assertIn('com.openai.codex', plan)
        self.assertIn('does not establish which app build executed an earlier probe', plan)

    def test_current_roster_binds_exact_profiles_to_observed_desktop_not_cli(self):
        roster = json.loads(CURRENT_ROSTER.read_text())
        observation = json.loads(
            (ROOT / 'docs/qualification/runtime-surface-observation-2026-09-13.json')
            .read_text()
        )
        policy = json.loads((ROOT / 'tooling/coordination/routing-policy.json').read_text())
        expected = {row['profile_id']: row for row in policy['profiles']}
        checks = {check['id']: check for check in roster['checks']}
        qualifications = {row['profile_id']: row for row in roster['qualifications']}
        client = observation['desktop_runtime']['client_version_for_qualification']

        self.assertEqual(set(qualifications), set(expected))
        self.assertEqual(roster['routing_policy_digest'], hashlib.sha256(
            json.dumps(policy, sort_keys=True, separators=(',', ':')).encode()
        ).hexdigest())
        self.assertFalse(observation['direct_cli']['astra_qualified'])
        self.assertNotEqual(client, observation['direct_cli']['installed_version'])

        for profile_id, qualification in qualifications.items():
            with self.subTest(profile_id=profile_id):
                profile = expected[profile_id]
                self.assertEqual(set(qualification), routing.hm.QUALIFICATION_FIELDS)
                self.assertEqual(qualification['model_id'], profile['model_id'])
                self.assertEqual(
                    qualification['reasoning_effort'], profile['reasoning_effort']
                )
                self.assertEqual(
                    qualification['capability_tier'], profile['capability_tier']
                )
                self.assertEqual(
                    qualification['runtime_id'], observation['desktop_runtime']['runtime_id']
                )
                self.assertEqual(qualification['client_version'], client)
                self.assertEqual(qualification['billing_mode'], 'subscription')
                self.assertEqual(qualification['capabilities'], ['read', 'edit', 'test'])
                self.assertEqual(len(qualification['qualification_check_ids']), 1)
                check_id = qualification['qualification_check_ids'][0]
                check = checks[check_id]
                self.assertTrue(check['required'])
                self.assertEqual(check['status'], 'PASS')
                self.assertEqual(
                    Path(check['evidence_path']).name, profile_id + '-desktop.json'
                )

    def test_existing_qualification_envelope_hashes_and_profile_schema(self):
        count = 0
        for path in (ROOT / 'docs/qualification').rglob('*.json'):
            record = json.loads(path.read_text())
            for check in record.get('checks', []):
                if check.get('status') not in ('PASS', 'FAIL'):
                    continue
                target = (ROOT / check['evidence_path']).resolve()
                self.assertTrue(target.is_relative_to(ROOT))
                self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), check['sha256'])
                count += 1
        self.assertGreater(count, 0)
        schema = json.loads((ROOT / 'tooling/coordination/schemas/profile-qualification.schema.json').read_text())
        self.assertFalse(schema['additionalProperties'])
        self.assertEqual(set(schema['required']), routing.hm.QUALIFICATION_FIELDS)

    def test_context_overflow_retains_mandatory_sources_and_route_slice(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = routing.hm.Harness(Path(directory))
            ready = harness.context('WP-00')
            narrow = harness.context('WP-00', max_bytes=1)
            self.assertEqual(ready['status'], 'READY')
            self.assertEqual(narrow['status'], 'NEEDS_NARROWING')
            self.assertEqual(ready['context_files'], narrow['context_files'])
            self.assertEqual(ready['project_context_files'], narrow['project_context_files'])
            self.assertEqual(ready['routing'], harness.routes['WP-00'])
            self.assertEqual(ready['routing_policy_digest'], harness.policy_hash)
            self.assertFalse((Path(directory) / '.texenda/state.json').exists())


if __name__ == '__main__':
    unittest.main()
