# Editor, blueprint and debug-baseline observations

Sanitized immutable observations recorded 2026-09-15 03:50:31 UTC.
These facts support a local candidate; they do not approve it, select a package
version, qualify VAL-03, upgrade Texenda or promote either source package.

## Exact clean and dirty source distinction

Clean inspected checkout: `/private/tmp/texenda-blueprint-qualification.BXFOTm/source`.
`git rev-parse HEAD HEAD^{tree} main origin/main` returned
`5e2d3025aea6b1574ab984e5ebb89b5602a38535`,
`3c732979e580c80b020d09c22ce86f5202110518`, and that same commit for both
main refs. `git show HEAD:VERSION` returned `4.2.0`.
`git status --porcelain=v1 --untracked-files=all --ignored=matching` was empty
before and after qualification. These commands read the clone only.

The original checkout's working VERSION `4.3.0` and 218 dirty entries are
retained separately from the Phase-0 observation. They are uncommitted working
state, not the VERSION of the clean commit. The original
`/Users/jamesryancooper/Projects/octon-mini` was not read or modified by this
author. Installed Project Blueprint 1.0.0 remains Texenda's selected inspected
structural reference; no source qualifies or adopts itself.

Preserved clean-source bundle:
`/Users/jamesryancooper/Projects/texenda/archive/checkpoints/blueprint-qualification-20260915/octon-mini-4.2.0-5e2d302.bundle`,
SHA-256 `d8e1471a25c5d0d20bd560d0dd33f060d6d0013aa573e3f725b2ce93639b3d7e`.
`git bundle verify` returned 0, complete history, main ref `5e2d3025...`.
The bundle is recovery/provenance evidence, not adoption or an installation.

Origin schema v2 is preserved with SHA-256
`e6ba4f8b1617b30a1aa2a130fd603e2e74f3ecdac81de5801521f526f7de63cc`.
The proposed local v3 successor separates the selected reference, exact clean
failed qualification attempt, dirty observation and blocked plan.

## Clean-source commands and actual results

All three commands ran with `PYTHONDONTWRITEBYTECODE=1` from the clean clone.
The source's root instructions/README were read. No source edit, clock
alteration, dependency installation, global-skill installation or upgrade ran.

### clean-source-contracts

Command: `env PYTHONDONTWRITEBYTECODE=1 python3 -B skills/octon-mini-project-bootstrap/scripts/validate_source_contracts.py`

Exit: 0.

```text
PASS: source-only architectural contracts are valid
- pattern records: 3 reviewed, 0 generated or automatically adopted
- semantic roles: 10 cross-walked without a universal status enum
- optional contracts: Context Pack v1 and Architecture Proof v1
- decision governance: valid baseline plus 11 fail-closed mutations
- profile manifest: v1 explicit allowlists, derived profile projections, capability-scoped degradation, and strict repository drift validation
- guided setup: one catalog, strict session/answer contracts, and 17 fail-closed mutations
```

### clean-source-acceptance

Command: `env PYTHONDONTWRITEBYTECODE=1 python3 -B skills/octon-mini-project-bootstrap/scripts/test_acceptance.py`

Exit: 0.

```text
PASS: Octon Mini acceptance suite
- profiles: minimal, standard, high-assurance
- generation: transactional, format-safe, allowlist-driven, and capability-scoped under degradation
- source-only contracts: catalog/proof assets absent from all profiles; trigger-only Context Pack schema and manifest absent from every default profile
- maintenance: derived focus/current refresh plus registered add, rename, combine, supersede, omission, and refusal paths
- migration: supported executable transitions preserve idempotence, exact rollback evidence, reviewed legacy seeding, and fail-closed ambiguity coverage
- adoption: read-only planning/checks plus separately explicit, fingerprint-bound project-check evidence
- guided setup: one catalog and shared session engine across init, adopt, and upgrade with target-read-only inspection and stale-digest refusal
- validator: adversarial authority, progressive collaboration classification, triggered Git portfolio, dependency readiness/frontier, lifecycle, reference, secret, extension, and freshness checks
- triggered packages: absent-by-default controls, strict fixture suites, content-addressed installation, decision binding, and refusal paths
ACCEPTANCE_COVERAGE_JSON={"criteria":{"1":"project_demonstration_required","10":"automated_pass","11":"project_demonstration_required","12":"automated_pass","13":"project_demonstration_required","14":"project_demonstration_required","15":"automated_pass","16":"automated_pass","17":"automated_pass","18":"automated_pass","19":"automated_pass","2":"automated_pass","20":"project_demonstration_required","21":"automated_pass","22":"project_demonstration_required","3":"project_demonstration_required","4":"automated_pass","5":"automated_pass","6":"automated_pass","7":"automated_pass","8":"automated_pass","9":"automated_pass"},"dirty_state":"not_assessed_by_acceptance_suite","external_effects":"none","failures":[],"limitations":["structural automation does not prove project readiness","runtime policy text is not an external sandbox"],"schema_version":"octon-mini.source.acceptance-coverage.v1","scope":"Octon Mini release automation","skipped_checks":["target-project human demonstrations remain project-owned"]}
criterion_01=project_demonstration_required
criterion_02=automated_pass
criterion_03=project_demonstration_required
criterion_04=automated_pass
criterion_05=automated_pass
criterion_06=automated_pass
criterion_07=automated_pass
criterion_08=automated_pass
criterion_09=automated_pass
criterion_10=automated_pass
criterion_11=project_demonstration_required
criterion_12=automated_pass
criterion_13=project_demonstration_required
criterion_14=project_demonstration_required
criterion_15=automated_pass
criterion_16=automated_pass
criterion_17=automated_pass
criterion_18=automated_pass
criterion_19=automated_pass
criterion_20=project_demonstration_required
criterion_21=automated_pass
criterion_22=project_demonstration_required
```

### clean-source-full-validator

Command: `env PYTHONDONTWRITEBYTECODE=1 python3 -B skills/octon-mini-project-bootstrap/scripts/validate_octon_mini.py`

Exit: 1.

```text
FAIL: 1 issue(s)
- autonomous-delivery functional and activation fixtures failed: test_changed_digest_and_confirmation_statement_are_rejected (__main__.AutonomousDeliveryTests.test_changed_digest_and_confirmation_statement_are_rejected) ... ok
test_command_line_flag_cannot_fabricate_confirmation (__main__.AutonomousDeliveryTests.test_command_line_flag_cannot_fabricate_confirmation) ... ok
test_compute_mode_is_explicit_and_subscription_never_overlaps_metered_api (__main__.AutonomousDeliveryTests.test_compute_mode_is_explicit_and_subscription_never_overlaps_metered_api) ... ok
test_confirmed_v1_metered_record_remains_valid_legacy_evidence (__main__.AutonomousDeliveryTests.test_confirmed_v1_metered_record_remains_valid_legacy_evidence) ... ok
test_contract_schema_and_duplicate_keys_fail_closed (__main__.AutonomousDeliveryTests.test_contract_schema_and_duplicate_keys_fail_closed) ... ok
test_deactivate_and_remove_retains_dormant_surface_and_external_record (__main__.AutonomousDeliveryTests.test_deactivate_and_remove_retains_dormant_surface_and_external_record) ... ok
test_draft_is_deterministic_non_authorizing_and_capped_at_ninety_days (__main__.AutonomousDeliveryTests.test_draft_is_deterministic_non_authorizing_and_capped_at_ninety_days) ... ok
test_exact_activation_installs_both_packages_and_preserves_external_authority (__main__.AutonomousDeliveryTests.test_exact_activation_installs_both_packages_and_preserves_external_authority) ... ok
test_included_subscription_activation_requires_readable_included_allowance_only (__main__.AutonomousDeliveryTests.test_included_subscription_activation_requires_readable_included_allowance_only) ... ok
test_pre_activation_surfaces_are_read_only_and_hook_free (__main__.AutonomousDeliveryTests.test_pre_activation_surfaces_are_read_only_and_hook_free) ... ok
test_profile_recommendation_never_selects_or_activates (__main__.AutonomousDeliveryTests.test_profile_recommendation_never_selects_or_activates) ... ok
test_revocation_and_emergency_stop_block_activation (__main__.AutonomousDeliveryTests.test_revocation_and_emergency_stop_block_activation) ... ok
test_source_activation_exercise_writes_only_external_receipt (__main__.AutonomousDeliveryTests.test_source_activation_exercise_writes_only_external_receipt) ... FAIL
test_source_effect_projection_binds_current_usage_digest (__main__.AutonomousDeliveryTests.test_source_effect_projection_binds_current_usage_digest) ... ok
test_source_work_completion_projection_maps_existing_owner_operations (__main__.AutonomousDeliveryTests.test_source_work_completion_projection_maps_existing_owner_operations) ... ok
test_subscription_usage_is_bound_to_current_readable_quota_windows (__main__.AutonomousDeliveryTests.test_subscription_usage_is_bound_to_current_readable_quota_windows) ... ok
test_successor_uses_new_id_and_requires_exact_predecessor_revocation (__main__.AutonomousDeliveryTests.test_successor_uses_new_id_and_requires_exact_predecessor_revocation) ... ok
test_unknown_or_unenforced_cost_blocks_activation (__main__.AutonomousDeliveryTests.test_unknown_or_unenforced_cost_blocks_activation) ... ok
test_usage_state_is_digest_bound_warned_and_stops_at_full_limit (__main__.AutonomousDeliveryTests.test_usage_state_is_digest_bound_warned_and_stops_at_full_limit) ... ok
test_warning_thresholds_and_exhaustion_are_exact (__main__.AutonomousDeliveryTests.test_warning_thresholds_and_exhaustion_are_exact) ... ok

======================================================================
FAIL: test_source_activation_exercise_writes_only_external_receipt (__main__.AutonomousDeliveryTests.test_source_activation_exercise_writes_only_external_receipt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/tmp/texenda-blueprint-qualification.BXFOTm/source/skills/octon-mini-project-bootstrap/scripts/test_autonomous_delivery.py", line 662, in test_source_activation_exercise_writes_only_external_receipt
    self.assertEqual(plan_result.returncode, 0, plan_result.stderr or plan_result.stdout)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : autonomous delivery blocked: standing authorization is not currently valid


----------------------------------------------------------------------
Ran 20 tests in 151.254s

FAILED (failures=1)
```


The acceptance result distinguishes `automated_pass` from
`project_demonstration_required`; it does not demonstrate Texenda adoption.
The full validator FAIL is retained exactly: one issue, with
`AutonomousDeliveryTests.test_source_activation_exercise_writes_only_external_receipt`
failing. Nineteen of that sub-suite's twenty cases pass. The fixture's fixed
`--valid-until 2026-09-10T23:59:59-05:00` is expired at the real current date;
the failure says its standing authorization is not currently valid.
No source failure was relabeled PASS, skipped away, or repaired in another repo.

The full runner was long-running. A scoped approved process observation found
15:29 elapsed; a remaining stop deadline of 03:50:06Z was imposed. It finished
with the above failure before the 03:48:52Z completion observation, so no process
termination was needed. All source command sessions have ended.

## Upgrade planner: blocked before mutation

These attempts targeted the author worktree
`/Users/jamesryancooper/Projects/texenda/worktrees/editor-blueprint-followups`
at the original Texenda baseline. No apply command ran.

Command:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B /private/tmp/texenda-blueprint-qualification.BXFOTm/source/octon upgrade plan --target /Users/jamesryancooper/Projects/texenda/worktrees/editor-blueprint-followups --output /private/tmp/texenda-followup-author.EoUX4Q/upgrade-plan.json --json
```

Exit: 2. Result:

```json
{
  "artifact_kind": "blocked_operation",
  "authority_source": "reported_path_or_project_governance_source",
  "blocked_operation": "upgrade.project",
  "failure_code": "OCTON-CONT-0001",
  "invalidated": [],
  "limitations": [
    "This continuation finding is non-authorizing and does not establish adoption or readiness."
  ],
  "mutation": {
    "external_effects": [],
    "occurred": false,
    "repository_paths": [],
    "statement": "Nothing changed; the affected operation stopped before mutation."
  },
  "next_action": {
    "argv": [
      "./octon",
      "upgrade",
      "--help"
    ],
    "description": "Inspect the exact finding and run the read-only diagnostic.",
    "read_only": true,
    "requires_confirmation": false
  },
  "permission_grant": false,
  "phase": "plan",
  "preserved": [],
  "repair_class": "manual_reconciliation_required",
  "root_cause": "upgrade requires --authority-source or setup.upgrade-authority",
  "safe_read_only_actions": [
    {
      "argv": [
        "./octon",
        "check"
      ],
      "description": "Inspect the project without mutation.",
      "read_only": true,
      "requires_confirmation": false
    }
  ],
  "schema_version": "octon-mini.continuation.v1",
  "successor": {
    "plan_supported": false,
    "reason": "No automatic successor is safe for this failure.",
    "session_supported": false
  }
}
```

Command:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B /private/tmp/texenda-blueprint-qualification.BXFOTm/source/octon upgrade plan --target /Users/jamesryancooper/Projects/texenda/worktrees/editor-blueprint-followups --output /private/tmp/texenda-followup-author.EoUX4Q/upgrade-plan.json --json --authority-source user:current-followup-request --evidence-ref docs/decisions/ADR-0004-mapped-project-workspace.md
```

Exit: 2. Result:

```json
{
  "artifact_kind": "blocked_operation",
  "authority_source": "reported_path_or_project_governance_source",
  "blocked_operation": "upgrade.project",
  "failure_code": "OCTON-CONT-0001",
  "invalidated": [],
  "limitations": [
    "This continuation finding is non-authorizing and does not establish adoption or readiness."
  ],
  "mutation": {
    "external_effects": [],
    "occurred": false,
    "repository_paths": [],
    "statement": "Nothing changed; the affected operation stopped before mutation."
  },
  "next_action": {
    "argv": [
      "./octon",
      "upgrade",
      "--help"
    ],
    "description": "Inspect the exact finding and run the read-only diagnostic.",
    "read_only": true,
    "requires_confirmation": false
  },
  "permission_grant": false,
  "phase": "plan",
  "preserved": [],
  "repair_class": "manual_reconciliation_required",
  "root_cause": "Project Blueprint 3.1.0 requires an exact reviewed --project-blueprint-seed",
  "safe_read_only_actions": [
    {
      "argv": [
        "./octon",
        "check"
      ],
      "description": "Inspect the project without mutation.",
      "read_only": true,
      "requires_confirmation": false
    }
  ],
  "schema_version": "octon-mini.continuation.v1",
  "successor": {
    "plan_supported": false,
    "reason": "No automatic successor is safe for this failure.",
    "session_supported": false
  }
}
```


The supplied authority/evidence arguments were not themselves validated as an
upgrade grant: the missing-seed stop occurs earlier. The planner's literal
Project Blueprint 3.1.0 message does not change Texenda's selected 1.0.0 reference.
No reviewed seed was supplied or fabricated. The proposed output
`/private/tmp/texenda-followup-author.EoUX4Q/upgrade-plan.json` remained absent; exact absence
check returned 0. Both continuations are `OCTON-CONT-0001`, mutation false.

## First-party editor observations

Read-only public GET retrieval on 2026-09-15 UTC used exactly these URLs:

- [Editor overview](https://react.email/docs/editor/overview): TipTap/ProseMirror
  architecture and the documented Prism/Next.js development compilation
  limitation. That caveat requires project build-performance testing.
- [EmailEditor API](https://react.email/docs/editor/api-reference/email-editor):
  TipTap JSON, HTML/plain-text exports and replacement of the default extension
  array support the proposed bounded codec/allowlist integration.
- [Release page](https://github.com/resend/react-email/releases):
  `@react-email/editor@1.7.7` was observed, not selected or pinned.

No login, GitHub repository mutation, settings change or external write occurred.
Public source observations do not establish package compatibility, license/SBOM,
dependency closure, integration, round trips, rendering quality or VAL-03.

## Debug archive: first forward baseline only

Archive:
`/Users/jamesryancooper/Projects/texenda/archive/reviewer-caches/pre-fix-check-all-KHHptR`.

- `CURRENT-SHA256SUMS` SHA-256:
  `8fca896ff26a00eb7d85d49fe54344a6a2d9b034d5938609ca920c3bc7ac2bd2`.
- `PROVENANCE.md` SHA-256:
  `5830d7d810d203a3e9e0f3fc9c2859778424be6d5bd4ccddcf512fc8699b0fa2`.

Command `shasum -a 256 -c CURRENT-SHA256SUMS`, run from that exact archive,
returned 0 and all five entries passed:

```text
cdc95fc381b44f2c10697d434a7313919774b1691ab8193b4a16313a31f573bb  check.out
5be4bee70be0d9b48bb4a69b95f9680050d42f868127a7b0212d28a4173b4dfc  sealed.out
e9d11720a3e68e1f0118de46020052dfccd4b30efc00db9d76f115b6855a931f  sealed-harness/harness.cpython-313.pyc
16bf765c41df02f3ca559725f2d9dde6240fb23505359399c59f6035bbf898cd  source.out
98657c4228431af626ef7d216bd23f2661f2cf3e3d327f85d2719f557c5e09cb  tooling-coordination/harness.cpython-313.pyc
```

No pre-move manifest exists. Historical equality cannot be reconstructed.
This is a non-authoritative current preservation baseline; raw debug/bytecode
payloads are not promoted into project source, approval or readiness evidence.
Both handoff variants and their eleven differences remain preserved. No private
CSV content or private-directory inventory was involved.

## Observation boundary

No prior stdout files existed; this author reran the commands and created this
record afterward. The local editor amendment and origin correction remain an
implementation candidate needing distinct review/integration. The retained
source full-validator failure blocks a blueprint upgrade. Current read-only
observations grant no model, product, gate, publication or external authority.
