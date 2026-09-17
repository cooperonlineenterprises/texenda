# Texenda local coordination v2

Read [ADR-0001](../../docs/decisions/ADR-0001-quality-first-model-routing.md) and
[routing-policy.json](routing-policy.json) for current coding routing. This local
Python standard-library adapter reuses the sealed lifecycle scaffold. It does
not launch a model, call a network service, authenticate actors, enforce a
sandbox, merge Git, meter usage, or grant production authority.

## Effective implementation plan and explicit activation

[ADR-0008](../../docs/decisions/ADR-0008-integrated-initial-product-and-effective-plan.md)
owns the single marked machine contract. [The plan loader](plan.py) combines its
scoped deltas with the three exact hash-pinned sealed catalogs. It retains all
44 work-package IDs and the existing routing policy; no generated JSON becomes
another plan authority. The closed [contract schema](schemas/effective-plan.schema.json)
validates the actual ADR block. The checker rejects missing/duplicate blocks,
duplicate keys or IDs, unknown fields/references, invalid types, path escapes,
changed sealed hashes, dependency/profile cycles and weakened stage/gate bounds.

Repository-only inspection requires neither a ledger nor a lock:

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/plan.py --check --root .
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/plan.py --json --root .
```

The import API is `load_plan(root)`: its `EffectivePlan` has `contract`, `catalog`
(`work_packages`), `profiles` (`profiles`), `acceptance` (`criteria`), `digest`,
`source_refs`, `changed_work_packages`, and `profile_closure(id)`. Closure results
are requirements, with stage-specific source rows and `NOT_ASSESSED` evidence.
Initial synthetic exercises of AC-IP11/12 use local mechanics; their references
to WP-18/20 do not create synthetic dependencies or pass the real portions.
Initial production inherits synthetic requirements while retaining its own real
qualification and baseline plus VAL-09/11 gates. AC-IP18 belongs to subsequent
activation/operation, not preactivation readiness. Nothing here runs product
tests, passes product acceptance, or clears an external gate.
Actual-transfer/canary/observation AC-M04/05/06/07/09 remain in email-pilot and
WP-20/33 execution; readiness carries AC-M01/02/03/08. Email-pilot additionally
requires WP-20. Discovery and rehearsals do not satisfy completed cutover.

`status` and `context` read the current state without activating anything. A
2.0 state is explicitly `sealed-unbound`; where the ADR exists, its proposed
digest/source refs and proposed work-package context are visible separately.
After activation, both use the same effective dependencies, allowed paths,
acceptance and gates as admission, leases and completion. Active `context`
returns `effective_plan_digest` and `context_digest`. New admission requires
`--plan-digest`; assignment also requires `--context-digest`. Old unbound or stale
context cannot supply these bindings. Version-2.1 lifecycle evidence must carry
the same `effective_plan_digest`; original sealed and completed bindings remain
historical and byte-exact.

Activation is a separately reviewed forward state boundary. Use the canonical
script/root and the explicitly bound external state directory:

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" activate-plan --actor "${TEXENDA_INTEGRATOR:?Use the actual integrating actor}"
# Only after independent review and actual runtime-stop evidence are retained:
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" activate-plan --actor "$TEXENDA_INTEGRATOR" --record path/to/reviewed-plan-activation.json --apply
```

The first command is a read-only dry run: no checkpoint, lock creation, receipt,
roster or state mutation. Its exact state hash, receipt tip/count, plan digest
and source refs populate the closed
[activation evidence schema](schemas/plan-activation.schema.json). The record
also binds the exact committed candidate revision/tree (each governed source is
checked against that commit), all authors, a distinct reviewer, actual integrating
actor and explicit owner-request basis. The reviewer must retain a fresh exact
Astra/max qualification, bound by its canonical qualification digest. Required
`independent-review` and `runtime-stop` checks need actual PASS evidence files,
hashes and procedures. Actor labels and a boolean cannot themselves authenticate
reviewers or terminate runtimes; accountable external observation remains required.

Apply refuses every lease, including expired ones; unfinished/uncertain work;
changed packages in any state other than untouched planned; missing/corrupt
evidence; stale sources; and corrupt checkpoints. It stores the exact original
bytes as `state.plan-v2.<sha256>.json` in the selected external state directory,
preserves all original tasks/history/receipts/roster/budget/gates, appends one
activation receipt, and advances the state protocol from 2.0 to 2.1. The original
`work_package_digest` stays sealed; the new `effective_plan_digest` is separate.
Sources, evidence and checkpoint are rechecked through the existing atomic
state-write commit boundary. Ordinary checks subsequently revalidate this proof.
Any interrupted replacement uses `recover-state-write`; no parallel ledger or
automatic destructive rollback is introduced. Repeated activation is a no-op,
including after later work. Preserve the checkpoint and repair forward; later
history must never be removed to undo activation. Old 2.0 lifecycle writers fail
closed on 2.1, even though their old context-only command may still emit an
unbound sealed manifest.

The active-plan coding route currently requires **max effort and subscription
work with zero new API allocation**. Previously qualified high profiles remain
runtime-qualified, but historical downshift/budget records bind only the sealed
scope and cannot authorize this enlarged plan. Lower effort or new paid coding
work needs a separately reviewed effective-bound attestation schema and explicit
authority. Existing qualifications, author/reviewer budgets and history remain
intact. This conservative coding restriction is separate from product AI/provider
qualification and spending authority.

For new dispatch prompts use the [operating guide](../../docs/agents/operating-guide.md)
and the local [assignment](templates/ASSIGNMENT.md), [review](templates/REVIEW.md)
or [resumption](templates/RESUME.md) template. The generated `context` manifest
must be supplemented with the applicable local instruction/template hashes.
The sealed generic assignment prompt remains package reference.

Context defaults to a bounded 262144-byte reference inventory so the initial
contract pack can include ADR-0008 without truncation. This is not a token count
or proof the complete prompt fits. A smaller explicit budget retains every
reference but returns NEEDS_NARROWING, dispatch_valid=false and no context digest;
the lead must prepare adequate context before dispatch.

Use Python 3.11+ on a single POSIX host. No dependency installation is needed.
A code worktree uses repository-only validation:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --scope code --all
```

In canonical `repo/`, set the exact absolute `TEXENDA_STATE_ROOT` deliberately
from its ignored binding and run ordinary control validation/inspection:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}"
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" status
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" ready
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" context "${TEXENDA_WORK_PACKAGE:?Select an ID from fresh ready output}"
```

Choose an ID explicitly from fresh ready output; empty readiness has no fallback.
For resumption use the recorded task/fence. Context is not an admission or
assignment. The [entry point](../../.agent/START_HERE.md) gives the canonical-script,
canonical-root `--read-only` invocation for worktree inspections. That flag rejects
all mutations and context output before harness construction; it is not caller
authentication and cannot prevent deliberately omitting the flag. Policy and
assignment scope separately prohibit those worktree effects. Never copy a binding,
ledger or receipt inputs to a worktree.

Every coordinator command takes `--root`; it remains the repository/evidence
root. The active ignored `.texenda-location.json` requires the exact absolute
`--state-root`; a moving, missing, wrong, relative, symlinked, traversing, or
competing root fails closed. Never initialize after binding, initialize over an
existing ledger, or use the sealed v1 CLI on a v2 ledger.

Before a state-location binding exists, omitted `--state-root` retains the
`.texenda` default. An explicit state root without an active binding is available only for detached
read-only `status`, `ready`, `check`, and context inspection. It cannot initialize,
append a receipt, acquire/create a lock, or write context output. This prevents a
second unbound active ledger while retaining review of an already relocated copy.

`status`, `ready`, and `check` use stable repeated reads and never create/open a
lock for write, initialize state, or update caches/reports. Mutations use the
selected state root's nonblocking exclusive lock and recheck the source bytes
before replacement. Lock acquisition and the final descriptor-relative state
commit recheck binding, repository/state-root/lock identity and routing policy.
Every normal content reader uses no-follow/nonblocking open flags, verifies a
regular descriptor before reading, then rechecks path/inode identity. Read-only
commands validate any existing lock as regular, non-symlink metadata without
opening it for write; a missing lock remains permitted. Writers likewise reject
a nonregular or substituted lock before `flock`.
A stale pre-cutover harness cannot recreate default state or leave a speculative
lock after a cooperative cutover; an unchanged newly-created lock inode is
removed only when acquisition or later commit continuity fails. The final state
comparison is followed by a binding/root/lock/policy identity recheck at the
replacement boundary. Existing-state writes use an atomic exchange so a
post-replacement identity failure restores the exact previous state bytes before
returning denial. Before candidate creation, the harness publishes a closed
preparation control. After exclusive candidate creation, an atomically published
candidate-bound [state-write transaction](schemas/state-write-transaction.schema.json)
binds the immutable intended hash, originally opened candidate identity,
repository/state-root/lock identities, binding identity and routing-policy digest.
Only an exact raw/hash/inode recheck promotes that same control to `ready` by
atomic rename immediately before exchange. Controls are fully
written/fsynced under a non-operational staging name before descriptor-relative
no-replace publication, so a partial file never masquerades as an active phase.
The harness validates the complete displaced old bytes and prepared inode after
exchange. Any pending state-write or
state-location activation transaction blocks all ordinary harness and facade
ledger access until its dedicated recovery path completes. Repository-relative
evidence always stays under `--root`.
Bound reads and writes also enforce the migration receipt count/prefix and exact
state bytes while the receipt count is unchanged; later valid appended receipts
remain permitted. Evidence envelopes and their PASS/FAIL log paths reject private
paths, CSVs, and symlink aliases before content reads or hashing.
The independently reviewed [state relocation helper](../workspace/relocate_state.py)
provides prepare/apply/resume/reverse-rename/verify operations; only the T1 move
lead uses it after the required freeze and exact approval.

`status` reports the policy digest, all exact profiles with availability/reasons,
default availability per capability tier, active assignment effort/fallback, and
lease/fence state. `declared_spend_usd` and `remaining_budget_usd` include author
and reviewer allocations across current tasks and retained history; these are
declared allowances, not measured provider charges. A missing default does not
select a downshift or fallback.
`budget_authorization.available_for_new_paid_work` separately reports whether
the current budget is usable; a positive remaining amount alone is not permission.
Capabilities use T1–T4, strongest first; they are distinct from product command
consequence classes C0–C4. Use the canonical digest printed by the harness,
not a raw `shasum` of the policy file.

## Pre-binding and legacy-ledger maintenance

These commands are not ordinary project entry. For a new pre-binding empty
ledger, `init` is non-overwriting and starts with no qualified profiles:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . init
```

For an existing v1 ledger, stop and reconcile all author runtimes with the v1
recovery protocol first. Even an expired lease blocks migration. Retain the
existing state and its evidence; do not copy arbitrary state from a worktree.
The owner-authorized migration workflow is:

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . migrate-v1 --actor human:owner
# Review the dry run, source receipt tip, checkpoint path, and policy digest.
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . migrate-v1 --actor human:owner --apply
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . check
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

For positive v1 allocations that lack per-allocation budget fields, migration
binds the original verified global budget reference and amount in
`routing_migration.legacy_budget_authorization` and the migration receipt. Its
manifest identifies each eligible original record by WP, role, fence, record
digest, amount, and source checkpoint path. This preserves every original task,
history item, and receipt. Completion/recovery of matching retained v1 work
rechecks the original checkpoint and budget evidence; changing the current v2
budget does not replace that historical proof. It cannot expand an allocation,
fund another fence, or authorize any new v2 author/reviewer work. Missing or
changed legacy proof blocks the compatibility path. Historical compatibility
does not qualify a model or clear a product gate.

Immediate rollback is limited to the migration with no later v2 receipts or
leases, and requires the owner's actual runtime-stop attestation:

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . rollback-v2 --actor human:owner --runtime-stopped
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . rollback-v2 --actor human:owner --runtime-stopped --apply
```

Rollback restores exact v1 bytes and retains a content-addressed v2 checkpoint.
Any later v2 operation blocks rollback so it cannot discard audit history or
work. Use a separately reviewed forward migration then. Neither command proves
runtime termination itself. After safe rollback, use the v1 CLI for that v1
ledger until the amendment is reapplied. Never delete `.texenda/` to clear state.

A process or durability failure during a local state replacement is recovered
separately from WP lifecycle recovery. Stop every runtime and use the exact
selected state root:

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" \
  recover-state-write --actor human:owner --runtime-stopped
```

The command acquires the preserved state lock and uses only descriptor-relative
operations. For each still-pending exchange it validates the immutable
transaction, environment and both byte sets, then restores the previous state as
the safest default without reserializing receipts. A fully archived durable commit
outcome can finish forward; earlier commit-cleanup phases still restore the prior
checkpoint. Missing, corrupt, ambiguous or substituted recovery material fails
closed. If rollback exchange or directory sync cannot be proved, the active and
candidate/checkpoint bytes plus both blocking controls remain. Candidate cleanup
is an atomic no-replace capture into a content-addressed, non-active checkpoint;
the harness never unlinks ledger bytes. The intended-content checkpoint is an
independent inode, so it cannot alias or mutate active `state.json`. Preparation
capture persists the original candidate identity and requires the exact intended
and attempted checkpoint set, equal bytes/hashes on distinct inodes, and the exact
attempted inode. Completed/recovered transaction records
retain sanitized hashes and identities. Ordinary success leaves no hidden
candidate or cleanup control and exactly one active `state.json` ledger.

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
# Replace the example path with the separately reviewed, owner-attested record:
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" set-roster --actor human:owner --record path/to/reviewed-roster.evidence.json
```

For the installed roster's dated history, see the
[activation receipt](../../docs/qualification/routing-v2-activation-receipt.md);
inspect live `status` rather than assuming that snapshot is current. Before any
roster replacement, follow the [runtime correction plan](../../docs/qualification/runtime-surface-correction-plan-2026-09-13.md):
desktop collaboration and direct CLI execution require separate qualification,
and the historical CLI 0.149.0 field does not identify the desktop app version.
Direct CLI remains unqualified by the desktop roster; that dated version is not
a durable requirement or a qualification for the currently installed CLI.
The source workspace installed a v2 roster; a fresh Git worktree carries these
committed evidence files but no ignored `.texenda/` ledger. Do not initialize or
copy state merely to make a read-only audit's `status` succeed.
The old `docs/qualification/model-roster.evidence.json` is historical v1 evidence and is
refused as a v2 roster. In v2 a Sol/max qualification has native capability 2,
whether it is used as the T2 default or explicitly selected as the T1 fallback.

Assignment defaults to the WP's listed profile at max. `--tier` may select a
stronger allowed tier. An explicitly named stronger `--profile-id` also records
its selected tier while retaining the WP capability floor. Unlisted profiles or
efforts, or weaker whole-parent assignments, are denied.

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" admit WP-01 --actor astra
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" assign WP-01 --actor astra --agent agent:contract-author --profile-id gpt-6-astra-max --max-seconds 3600 --max-tokens 50000
# Explicit T1 fallback; only Sol/max is eligible:
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" assign WP-01 --actor astra --agent agent:contract-author --tier 1 --profile-id gpt-5.6-sol-max --fallback --fallback-reason 'Owner-approved bounded fallback for this assignment'
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

Use [templates/budget.json](templates/budget.json) and the v2 evidence schema for
all new paid work. The closed record requires `owner` (matching the `human:`
actor), `approved_budget_usd` (exactly equal to `set-budget --usd`), a nonempty
descriptive `scope`, explicit `work_packages` and `roles` (`author`/`reviewer`),
the current policy/catalog digests, `issued_at`, `expires_at`, summary, and
required PASS checks. Only `notes` is optional. Amounts must be finite numbers
from zero through 100000; booleans are invalid. Both timestamps require explicit
timezones, with `issued_at <= now < expires_at` and a positive validity window
no longer than 30 days. The template is deliberately expired and NOT_RUN.

```sh
# Only with separately obtained owner approval; the evidence amount must equal --usd.
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" set-budget --actor human:owner --usd 1 --record docs/qualification/development-budget.evidence.json
```

Each positive allocation binds its exact budget reference and approved cap.
New allocations enforce WP/role scope; start, review, integration, and completion
recheck the same unexpired v2 authorization. Equality at expiry denies. A newer
global budget does not silently renew an old v2 allocation. Expired spending
remains in the cumulative ledger; stopping/recovering work does not refund or
renew it. Use proved recovery, a new fence, and explicit fresh authorization
when paid v2 work must be reassigned. Legacy compatibility is limited to the
exact already retained v1 records and never supplies this new authorization.

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

The authoritative project validation commands now live in the single
[`.agent/validators.json`](../../.agent/validators.json) registry. Execute its
exact argv entries with `PYTHONDONTWRITEBYTECODE=1` where shown; this guide does
not independently own or redefine the suite.

The [independent test plan](../../docs/qualification/analysis/routing-v2-test-plan.md)
is a design input. Its illustrative C labels and short profile IDs map to T1–T4
and the exact model-effort IDs in this policy. Tests use only temporary synthetic
ledgers and a fixed clock; passing them does not qualify product behavior or
external services. The sealed package, historical probes, and v1 evidence stay
intact. Model self-identification, provider billing telemetry, account policy,
sandbox enforcement, and actual author/reviewer identity remain external checks.
