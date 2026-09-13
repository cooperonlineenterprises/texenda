# ADR-0001: Quality-first coding model routing

Status: AUTHORITATIVE DECISION — owner accepted the routing policy on 2026-09-13.
Implementation status: candidate; independent implementation review and integrated-head
verification are separate from acceptance of this policy. Runtime activation still
requires the final accountable owner roster attestation.

The owner accepted four coding capability tiers, each defaulting to max reasoning
effort. This project calls them **T1–T4** to avoid confusion with Texenda's product
command consequence classes C0–C4. The owner discussion's capability C1–C4 maps
one-to-one to T1–T4 here; product consequence classes are unchanged.

| Capability | Default exact profile | Eligible effort downshifts |
|---|---|---|
| T1 | `gpt-6-astra-max` | `gpt-6-astra-high` |
| T2 | `gpt-5.6-sol-max` | `gpt-5.6-sol-high` |
| T3 | `gpt-5.6-terra-max` | `gpt-5.6-terra-high`, `gpt-5.6-terra-medium` |
| T4 | `gpt-5.6-luna-max` | `gpt-5.6-luna-high`, `gpt-5.6-luna-medium`, `gpt-5.6-luna-low` |

`gpt-5.6-sol-max` is also the sole explicit T1 fallback. It remains native T2
and the T2 default. A T1 use requires the exact profile, the fallback flag,
and a nonempty recorded reason, even when Astra is available. No other Sol
effort qualifies for that fallback, and unavailable Astra never selects Sol
automatically. These are allowed profiles, not a claim of current runtime access.

Capability and consequence set a model floor first. Reasoning demand selects an
allowed effort within that floor. Every normal assignment and review defaults to
max. A downshift is permitted only where the WP role explicitly allows it and
fresh evidence establishes bounded, reversible, fully specified work with a
deterministic verification oracle. Escalate effort before capability when that
floor remains sufficient; a newly discovered security, authority, recovery,
migration, or architectural consequence can require a stronger floor immediately.
Simple tool failures get a bounded deterministic repair; repeated substantive
reasoning failure, contradictory evidence, or scope expansion needs reassessment.

The reason for this amendment is to separate model capability from reasoning
effort and make quality the default. The prior three-tier routing coupled Terra
to tier 2 and Luna to tier 3, allowed one active binding per tier, and did not
retain exact effort qualification through assignment, start, and review. The new
policy records both the WP floor and the selected exact model/effort profile.
An explicit stronger profile is allowed when the WP role lists it. Qualification
is never inferred from another effort, model name, public roster, or old tier.

The [machine policy](../../tooling/coordination/routing-policy.json) supplies all
44 author and reviewer routes. The [reconciled independent analysis](../qualification/analysis/work-package-routing-review.json)
contains the per-WP reasoning: 13 T1, 27 T2, and 4 T3 authors; 39 T1 and 5 T2
reviewers. Consequential implementation stays T2 when settled contracts bound
the work, with independent T1 review. Contract, adversarial qualification,
external evidence interpretation, migration execution, and release judgment
remain T1. WP-00, WP-02, WP-13, and WP-25 permit max/high authors; WP-10 permits
max/high at T2. Those five WPs permit max/high reviewers. All other whole-parent
routes are max only. The mapper's unsupported `xhigh` proposals were normalized
to the accepted `high` profile; the original proposal remains reference evidence.

No whole parent WP is wholly mechanical enough for T4. T4 profiles are available
for later reviewed plan additions or separately fenced mechanical scopes. A
parent lease cannot be assigned to T4 to bypass its floor; the local harness
still coordinates only the admitted parent catalog. A subtask does not gain an
independent lease merely because it is described as mechanical.

This is a project-local overlay. It supersedes only model routing recommendations
and numeric tier fields from the sealed handoff's model-routing policy,
orchestrator routing instructions, WP routing fields, and harness/roster contract.
The package at `specs/texenda-handoff/` remains byte-for-byte unchanged. Its
decisions, prerequisites, bounded paths, independent review, leases, recovery,
activation gates, product invariants, and acceptance criteria still govern.
This migration changes development coordination records, not Texenda domain data.

The [local adapter](../../tooling/coordination/harness.py) imports the hash-pinned
sealed lifecycle primitives and uses state version `2.0`. State and roster bind
the canonical JSON policy SHA-256. Key order/whitespace changes preserve that
digest; semantic changes require a separately reviewed state/policy migration
and fresh qualifications. The adapter rejects duplicate JSON policy keys and
unrecognized, duplicate, mismatched, or unqualified exact profiles. It pins the
full qualification and its evidence reference in each assignment. Start and
review recheck the exact author profile, runtime, effort, expiry, roster bytes,
logs, and downshift attestation; review independently checks the exact reviewer
profile and candidate. Updating a qualification invalidates its old assignment
binding and requires proved recovery and a new fence.

Use version-1 envelopes for compatible lifecycle evidence. New roster, model
review, and downshift metadata use the local version-2 evidence schema, without
adding unknown fields to the sealed version-1 schema. Evidence and profile
allowlists cannot authenticate an actor, prove that a report is truthful, or
inspect the provider's actual executing model. Accountable independent review
and actual runtime controls remain necessary.

Migration is explicit and dry-run first with `migrate-v1`. It validates the v1
receipt chain and baseline, refuses every lease including expired leases and
unsafe/unfinished states, and rechecks retained integration stop evidence.
It keeps every task, fence, history item, and old receipt unchanged; writes an
exclusive byte-exact v1 checkpoint; clears the old active roster; and appends
one migration receipt linking the old tip, checkpoint hash, and new policy.
Repeated migration on valid v2 state is a no-op, including after new roster
qualification. A failed state replacement leaves the original v1 state and
its verifiable checkpoint. This candidate does not migrate the live ledger.

Before any later v2 receipt, `rollback-v2` can restore that exact v1 checkpoint
under an explicit owner runtime-stop attestation, preserving the complete v2
checkpoint as well. After any later v2 work, the rollback command refuses:
retain the ledger and use a separately reviewed forward migration. Never erase
state, rewrite historical receipts, or run the v1 harness against a v2 ledger.
The [operator guide](../../tooling/coordination/README.md) gives concrete commands.

Validation includes the [independent verification plan](../qualification/analysis/routing-v2-test-plan.md),
all unchanged sealed harness tests and package checksum checks, plus deterministic
local routing, tamper, expiry, fallback, lease, migration, fault, and rollback
tests. An independently reviewed candidate and its integrated-head results must
be retained before production of any v2 active roster. The baseline and new
profile probes prove bounded local read/edit/test activity only, with model
self-identification limitations retained.

INV-02 still forbids permission transfer from shared identity. INV-12 still
forbids blind provider/channel failover after timeout or unknown acceptance.
INV-30 still makes the harness a coordinator, with no authority to send,
deploy, provision, expose production data, read credentials, or spend.
The development API budget remains zero unless separately owner-authorized;
subscription work has explicit time/token bounds. None of the 125 product
acceptance criteria or external production gates is passed by these local tests.

Independent candidate review of `61d921aeeb7b386e442dbdf8d1db91f1d6be0a81`
identified missing reviewer-budget enforcement, incomplete historical stop-proof
validation at migration, and Python boolean/integer aliasing in routing records.
The corrective commit preserves that candidate in history. Author and reviewer
allocations now share one bounded owner-approved allowance, including rejected
reviews and recovered history, with evidence rechecks at later acceptance steps.
Migration and immediate rollback validate retained stop/recovery/candidate and
checkpoint references, reconstruct prior fences from receipts, and refuse missing
or changed proof before writing. Routing tier/fence fields require actual integers.
These corrections enforce the accepted policy; they do not change its model
matrix, production authority, or the sealed package. V1 facts that were never
recorded cannot be reconstructed or qualified by this migration.
