# Texenda local coordination v2

Read [ADR-0001](../../docs/decisions/ADR-0001-quality-first-model-routing.md) and
[routing-policy.json](routing-policy.json) for current coding routing. This local
Python standard-library adapter reuses the sealed lifecycle scaffold. It does
not launch a model, call a network service, authenticate actors, enforce a
sandbox, merge Git, meter usage, or grant production authority.

Use Python 3.10+ on a single POSIX host. No dependency installation is needed.
Every command takes `--root`; the normal target is the repository root. Never
initialize over an existing ledger or use the sealed v1 CLI on a v2 ledger.

```sh
# Empty ledger only; init is non-overwriting and starts with no qualified profiles.
python3 tooling/coordination/harness.py --root . init
python3 tooling/coordination/harness.py --root . status
python3 tooling/coordination/harness.py --root . check
python3 tooling/coordination/harness.py --root . context WP-00
```

`status` reports the policy digest, all exact profiles with availability/reasons,
default availability per capability tier, active assignment effort/fallback, and
lease/fence state. `declared_spend_usd` and `remaining_budget_usd` include author
and reviewer allocations across current tasks and retained history; these are
declared allowances, not measured provider charges. A missing default does not
select a downshift or fallback.
Capabilities use T1–T4, strongest first; they are distinct from product command
consequence classes C0–C4. Use the canonical digest printed by the harness,
not a raw `shasum` of the policy file.

For an existing v1 ledger, stop and reconcile all author runtimes with the v1
recovery protocol first. Even an expired lease blocks migration. Retain the
existing state and its evidence; do not copy arbitrary state from a worktree.
The owner-authorized migration workflow is:

```sh
python3 tooling/coordination/harness.py --root . migrate-v1 --actor human:owner
# Review the dry run, source receipt tip, checkpoint path, and policy digest.
python3 tooling/coordination/harness.py --root . migrate-v1 --actor human:owner --apply
python3 tooling/coordination/harness.py --root . check
```

Migration preserves task/history records and all old receipt objects/hashes.
It stores the byte-exact source in `.texenda/state.v1.<sha256>.json`, records the
source hash/tip and old-roster invalidation reason, clears the active roster,
and adds one boundary receipt. No old effort is promoted to max. Idempotent
repetition does not touch state or a newly qualified v2 roster. The migration
does not reassign tasks, complete work, clear external gates, or execute models.

Before writing, migration rechecks every retained recovery and relevant
checkpoint, submission, review, integration, trigger, and budget reference and
its logs. Recovery must retain required PASS checks, exact boolean stop proof,
and the integer previous fence derived from the receipt sequence. Integration
must retain its approved candidate, matching integrated head, and exact stop
proof. Missing/tampered history blocks migration with the v1 bytes unchanged.
Rollback revalidates the source evidence too. V1 did not archive every superseded
checkpoint; the adapter validates all retained references and cannot reconstruct
records the old harness never retained. V2 recovery preserves checkpoint and
fence references with the candidate history going forward.

Immediate rollback is limited to the migration with no later v2 receipts or
leases, and requires the owner's actual runtime-stop attestation:

```sh
python3 tooling/coordination/harness.py --root . rollback-v2 --actor human:owner --runtime-stopped
python3 tooling/coordination/harness.py --root . rollback-v2 --actor human:owner --runtime-stopped --apply
```

Rollback restores exact v1 bytes and retains a content-addressed v2 checkpoint.
Any later v2 operation blocks rollback so it cannot discard audit history or
work. Use a separately reviewed forward migration then. Neither command proves
runtime termination itself. After safe rollback, use the v1 CLI for that v1
ledger until the amendment is reapplied. Never delete `.texenda/` to clear state.

Exact runtime qualification uses [schemas/evidence.schema.json](schemas/evidence.schema.json)
and [templates/roster.json](templates/roster.json). Version-2 roster records must
include `routing_policy_digest`. Each unique qualification carries `profile_id`,
native numeric `capability_tier`, exact `model_id` and `reasoning_effort`,
`runtime_id`, `client_version`, `sign_in_mode`, `billing_mode`, demonstrated
`capabilities` including read/edit/test, `verified_at`, `expires_at`, and
`qualification_check_ids`. Those IDs must name required PASS checks in the same
envelope, with relative evidence paths, SHA-256 hashes, and exact procedures.
The owner/reviewer must verify each linked probe is for the claimed exact model
and effort and recheck relevant runtime/account/client/policy changes. Availability
never follows merely from a policy entry or a template. Validity is at most 30
days; stale or changed evidence makes the profile unavailable.

```sh
# Only after integrated verification and accountable owner attestation:
python3 tooling/coordination/harness.py --root . set-roster --actor human:owner --record docs/qualification/model-roster-v2.evidence.json
```

No active v2 roster is shipped with this candidate. The old
`docs/qualification/model-roster.evidence.json` is historical v1 evidence and is
refused as a v2 roster. In v2 a Sol/max qualification has native capability 2,
whether it is used as the T2 default or explicitly selected as the T1 fallback.

Assignment defaults to the WP's listed profile at max. `--tier` may select a
stronger allowed tier. An explicitly named stronger `--profile-id` also records
its selected tier while retaining the WP capability floor. Unlisted profiles or
efforts, or weaker whole-parent assignments, are denied.

```sh
python3 tooling/coordination/harness.py --root . admit WP-01 --actor astra
python3 tooling/coordination/harness.py --root . assign WP-01 --actor astra --agent agent:contract-author --profile-id gpt-6-astra-max --max-seconds 3600 --max-tokens 50000
# Explicit T1 fallback; only Sol/max is eligible:
python3 tooling/coordination/harness.py --root . assign WP-01 --actor astra --agent agent:contract-author --tier 1 --profile-id gpt-5.6-sol-max --fallback --fallback-reason 'Owner-approved bounded fallback for this assignment'
```

The two assignment examples are alternatives, not sequential operations. Run
only one when prerequisites are complete and the task is admitted. Actual
runtime dispatch must request the returned exact model and effort; this CLI does
not dispatch. Human bootstrap remains explicit through `--agent human:owner
--human` and cannot claim a model profile or fallback.

Author and reviewer allocations share the same owner-approved development cap.
Any API-billed assignment or review requires a positive `--budget-usd`; model
review also accepts `--max-tokens` and `--max-seconds`, with the same bounded
defaults as author work. Subscription review can allocate zero. Each allocation
retains the owner budget evidence; changed or missing authorization blocks paid
work and later approval/integration/completion. A rejected review still consumes
its allocation. Recovery moves rejected and accepted reviews into history once,
so reassigning or resubmitting cannot erase spending or charge an allocation
twice. The owner cannot lower the cap below retained allocations. An older
API-tagged review with no positive allocation requires reviewed accounting
repair; its missing amount is never inferred as zero or erased by recovery.

A lower effort also requires `--routing-record`, using
[templates/routing.json](templates/routing.json). The record binds the task,
author/reviewer role, profile, selected capability tier, current policy and WP
digests, assignment fence, expiry, bounded reasoning demand, rationale, four
boolean conditions, and deterministic PASS evidence. An author record uses the
next assignment fence; a reviewer record uses the current fence and exact
candidate revision. The current whole-parent policy permits high only for
WP-00/02/10/13/25; all other parents remain max. Globally allowed medium/low
profiles still need a reviewed WP role that allows them. T4 cannot take a parent
lease whose floor is stronger.

Start and review pin the full qualification/evidence snapshot. A renewal,
changed runtime, selected-profile removal, expired evidence, or modified
attestation invalidates the existing assignment; preserve work, prove stop,
recover, and obtain a new fence. Model review uses the v2 envelope with
`profile_id` and `routing_policy_digest` and a distinct actor. Human review and
other compatible lifecycle envelopes can remain v1. Candidate hashes, required
PASS checks, semantic-merge rejection, scoped external gates, and integration
runtime-stop evidence retain their sealed behavior. V2 approvals are recorded
at the review boundary; integration rechecks the approved candidate and evidence
but does not launch/requalify an already completed reviewer runtime.

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tooling/coordination/tests -v
env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -v
env PYTHONDONTWRITEBYTECODE=1 python3 specs/texenda-handoff/10-validation/validate_package.py --checksums
git diff --check
```

The [independent test plan](../../docs/qualification/analysis/routing-v2-test-plan.md)
is a design input. Its illustrative C labels and short profile IDs map to T1–T4
and the exact model-effort IDs in this policy. Tests use only temporary synthetic
ledgers and a fixed clock; passing them does not qualify product behavior or
external services. The sealed package, historical probes, and v1 evidence stay
intact. Model self-identification, provider billing telemetry, account policy,
sandbox enforcement, and actual author/reviewer identity remain external checks.
