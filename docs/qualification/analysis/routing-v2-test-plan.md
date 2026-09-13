# Routing v2 independent verification plan

**Scope:** project-local routing-v2 subclass adapter and its state migration. This
is a deterministic test design, not a claim that the adapter, a model runtime, or
an external validation gate has passed.

## Evidence basis and test rig

The committed baseline is `12e19b167d7fd59722dc2a3194ce591f499de0e7`.
There is no committed live `.texenda/state.json`; the v1 fixture shape is therefore
derived only from the committed `Harness.init` implementation and its synthetic
tests: version/package/work-package digests, budget fields, writer limit, roster,
gates, events, and per-WP lifecycle records. The committed qualification evidence
confirms only sanitized subscription read/edit/test probes. It is not read as a
live credential, account, or state source.

Implement the tests with an isolated temporary root, a fixed UTC clock, a copied
synthetic work-package catalog, deterministic synthetic evidence logs, and no
network or model invocation. Capture before/after canonical state bytes, event
array, receipt tip, and checkpoint hash for every denial or migration. Unless a
test says otherwise, a denied operation must raise the adapter's denial error,
leave `state.json` byte-for-byte unchanged, append no receipt, create no lease,
and make no fallback selection. A successful operation must record an auditable
receipt and exactly the selected profile; a tier number alone is not sufficient.

The field labels below are descriptive until the adapter schema lands. Their
semantics are required: a profile binding records the profile ID, capability,
model ID, effort, profile/roster evidence reference, and routing-policy digest;
a lower-effort attestation records the task, role, profile, policy digest, and
deterministic evidence reference.

## Profile fixture and ordering oracle

Load this exact 11-profile fixture. Reject a catalog with a missing, duplicate,
case-altered, model-swapped, effort-swapped, or extra profile.

| Capability (strongest first) | Exact profiles | Default |
|---|---|---|
| C1 | `c1-max` / `gpt-6-astra` / `max`; `c1-high` / `gpt-6-astra` / `high` | `c1-max` |
| C2 | `c2-max` / `gpt-5.6-sol` / `max`; `c2-high` / `gpt-5.6-sol` / `high` | `c2-max` |
| C3 | `c3-max` / `gpt-5.6-terra` / `max`; `c3-high` / `gpt-5.6-terra` / `high`; `c3-medium` / `gpt-5.6-terra` / `medium` | `c3-max` |
| C4 | `c4-max` / `gpt-5.6-luna` / `max`; `c4-high` / `gpt-5.6-luna` / `high`; `c4-medium` / `gpt-5.6-luna` / `medium`; `c4-low` / `gpt-5.6-luna` / `low` | `c4-max` |

Normal substitution may choose a stronger capability only: C1 for C2/C3/C4,
C2 for C3/C4, and C3 for C4. It must retain the requested capability and selected
profile in the assignment receipt. C1 is stronger than C2, and so on; no lexical
or model-name ordering is accepted as a substitute for this explicit ordering.

The allowed lower-effort set is exactly `c1-high`, `c2-high`, `c3-high`,
`c3-medium`, `c4-high`, `c4-medium`, and `c4-low`. The four `*-max` profiles need
no lower-effort exception. `c2-max` is the sole C1 fallback profile, not a general
permission to route C1 work to C2 or to any Sol profile.

## Deterministic test cases

| ID | Setup and action | Pass oracle / failure oracle |
|---|---|---|
| RV2-01 profile catalog | Parse the exact fixture, then independently mutate one field at a time: omit `c4-low`, duplicate `c3-max`, add `c3-low`, swap Terra and Luna, or use an unknown effort. | Only the exact 11-entry catalog loads. Each mutation denies before routing and leaves state untouched. |
| RV2-02 max defaults | For a task requiring each of C1, C2, C3, and C4, omit an explicit profile. | Assignment resolves respectively to `c1-max`, `c2-max`, `c3-max`, and `c4-max`, with their exact `gpt-*` model IDs and `max` stored in the receipt. If that default is unavailable, deny; do not downshift, silently fall back, or use the former v1 tier binding. |
| RV2-03 exact profile binding | Request every explicit profile in the fixture and inspect the stored assignment. Also request a profile whose declared capability matches but model or effort does not. | The stored profile ID, model ID, effort, capability, evidence digest, and policy digest exactly equal the loaded profile. A tier-equivalent or model/effort-equivalent lookalike is denied. |
| RV2-04 lower-effort admission | Parameterize all seven allowed lower-effort profiles. Route each without an attestation, then with a valid deterministic attestation. | Missing attestation denies. A valid task/role/profile/policy-digest-bound attestation permits precisely that profile; it cannot be treated as approval for another lower effort. |
| RV2-05 attestation binding and evidence | Starting from a valid lower-effort attestation, alter one of task ID, author/reviewer role, profile ID, policy digest, expiry, log hash, or evidence content after its hash is recorded. | Every altered case denies on the eligibility boundary where it is checked. No mutable free-text rationale, unrelated task attestation, or `NOT_RUN` check can authorize the lower effort. |
| RV2-06 stronger substitution | Exercise the normal allowed pairs `(C2,c1-max)`, `(C3,c1-max)`, `(C3,c2-max)`, `(C4,c1-max)`, `(C4,c2-max)`, and `(C4,c3-max)`. | Each succeeds without being mislabeled as a fallback, and records both required capability and stronger selected profile. A selected lower-effort stronger profile additionally needs RV2-04's attestation. |
| RV2-07 insufficient capability | Exercise `(C1,c2-max)`, `(C2,c3-max)`, `(C2,c4-max)`, `(C3,c4-max)`, plus every unknown profile. | All deny except the narrowly constructed RV2-08 C1 fallback. The denial cannot mutate an existing assignment to a weaker profile. |
| RV2-08 explicit C1 Sol fallback | First leave C1's normal Astra profile available, then make it unavailable. In both states, try `c2-max` with (a) no fallback flag, (b) flag but blank reason, (c) nonempty reason but no flag, and (d) both an explicit C1-fallback flag and a nonempty reason. Repeat (d) with `c2-high`. | Only (d) using `c2-max` succeeds; primary availability must not turn an explicit fallback into a silent or undocumented rule. Its receipt states C1 requirement, `c2-max` selection, explicit fallback status, and the supplied reason. `c2-high` remains denied even with a flag/reason. A normal C1 request never auto-selects Sol merely because Astra is absent. |
| RV2-09 profile recheck | Assign `c3-high` with valid attestation. Before `start`, replace the roster/profile evidence with `c3-medium`, change Terra's model ID, change the profile evidence bytes, or remove the selected profile while retaining a valid C3 tier. | `start` denies in all cases: it must recheck the exact profile/evidence, not merely that some C3 qualification remains. Repeat at review/any later dispatch authority boundary required by the adapter. |
| RV2-10 expiry | With fixed time, test valid just before expiry, exactly at expiry, and just after expiry for a profile and for a lower-effort attestation. Include a qualification older than 30 days. | Just-before-expiry is eligible. At/after expiry and over-age qualifications deny with no automatic substitute. An assignment made before expiry cannot start or review after expiry without fresh qualifying evidence. |
| RV2-11 author/reviewer independence | Submit with stable principal `agent:author`. Review using the same stable principal under a different display label/role, then use a distinct `agent:reviewer` with a sufficient exact profile. | Any matching stable author/reviewer principal denies, regardless of capability or effort. The independent, sufficient reviewer can approve the exact candidate only. This tests declared identity comparison; it does not claim cryptographic identity proof beyond the harness boundary. |
| RV2-12 API budget | Use a synthetic API-billed profile. Attempt assignment with no owner budget, with a zero task allocation after a positive owner budget, with an allocation within the cap, and with a second allocation that exceeds the cap. Recover and try to reuse the spent allocation. Separately use a subscription profile with zero API allocation. | API work requires a positive owner-authorized task allocation and total historical allocations never exceed the approved cap; denial has no allocation/lease/receipt side effect and recovery cannot erase consumption. Subscription routing does not imply free/unbounded work, but it does not need an API-spend allocation. No test contacts an API, reads credentials, or spends money. |

## v1 to v2 migration tests

Generate v1 states through the committed v1 harness under a frozen clock rather
than hand-writing unchecked JSON. Cover a planned state, an assigned/running state,
and a completed history with a nonempty valid receipt chain. Retain the exact v1
state bytes, canonical event objects, event hashes, old tip, and v1 state digest
as fixtures.

| ID | Setup and action | Pass oracle / failure oracle |
|---|---|---|
| RV2-M01 receipt-chain conversion | Migrate a valid, lease-free v1 state. | State becomes `2.0`; every pre-migration event object/hash is unchanged; the first v2 migration receipt links `previous_hash` to the old tip and identifies the v1 source digest/tip, v2 policy digest, and checkpoint hash. The v2 verifier accepts the preserved v1 prefix at the migration boundary and the new v2 suffix. Any rewritten historical event/hash, broken link, or missing boundary proof fails. |
| RV2-M02 active-lease refusal | Generate an assigned/running v1 task with an unexpired lease; repeat with an expired lease that lacks proved stop/recovery evidence. Invoke migration. | Both cases deny before checkpoint/write/receipt creation. Existing lifecycle semantics say an expired lease stays blocking until recovery, so migration must not use expiry as permission to rewrite state. |
| RV2-M03 old-roster invalidation | Seed a valid v1 roster with a formerly qualified tier binding and migrate a lease-free state. Attempt automated assignment before loading fresh v2 profile qualification. | Migration records/retains an auditable invalidation reason but cannot translate a v1 tier to a `*-max` profile. Automated assignment fails closed until a fresh exact v2 roster/profile record is installed. |
| RV2-M04 idempotency | Complete RV2-M01, snapshot bytes/tip, then invoke migration a second time. | The second call is a no-op success (or explicit already-migrated result) with identical state bytes/tip and no duplicate migration receipt/checkpoint. It must not re-invalidate a freshly qualified v2 roster. |
| RV2-M05 checkpoint and fault rollback | Inject a write failure after the v1 checkpoint is safely created but before the v2 state replacement. Then execute a successful migration and exercise the documented rollback path before any subsequent v2 work. | Failure leaves the original v1 state byte-for-byte valid and leaves only a verifiable original checkpoint, never a partial v2 file. A successful conversion retains an immutable checkpoint whose hash matches the original v1 bytes. Safe rollback restores that exact checkpoint and passes the v1 verifier. If later v2 receipts/leases exist, rollback must refuse rather than discard audit history or active work. |

## Policy digest and lifecycle/evidence compatibility

**RV2-P01 — policy digest mismatch.** Initialize/migrate with a canonical routing
policy digest. Reorder semantically identical JSON keys (must remain eligible),
then change a default, profile-to-model/effort binding, capability ordering, or the
allowed lower-effort set (must fail closed). `status`, assignment, start, and review
must not silently replace the stored digest, reinterpret the roster, or add a
receipt on mismatch. Recovery requires an explicit reviewed policy/state migration
and fresh qualification as the adapter specifies.

**RV2-P02 — retained lifecycle behavior.** With a max profile, execute the full
existing path: `init → admit → assign → start → checkpoint → submit → independent
review → integrate → complete`. Verify the existing candidate/evidence hash
rechecks, required-PASS behavior, fence and lease ownership, dependency release,
runtime-stop integration proof, semantic-merge rejection, activation-gate scope,
and recovery fence increment still work. Run the existing test suite unchanged;
all baseline tests must remain green.

**RV2-P03 — evidence compatibility.** Feed unmodified v1-shaped submission,
review, integration, checkpoint, recovery, roster, budget, gate, and trigger
evidence into the compatible lifecycle cases. Evidence tampering, a changed
candidate, missing log, or required `NOT_RUN` must still deny. Lower-effort routing
may require an additional versioned/evidence-hashed record, but must not smuggle
unvalidated fields into the current `additionalProperties: false` evidence envelope
or weaken its file-hash recheck.

## Required execution and report

Run the new adapter tests plus these unchanged offline baseline commands:

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 specs/texenda-handoff/10-validation/validate_package.py
env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -v
```

The result packet must list every test ID, frozen timestamp, fixture/state/checkpoint
hashes, candidate and policy digest, exact commands/output/exit codes, and all
NOT RUN cases. The highest-value unsafe-behavior mutations are the silent C1→Sol
path, same-tier-but-different-profile recheck, tampered lower-effort attestation,
expired lease migration, old-roster auto-promotion, post-migration rollback that
would erase receipts, and a policy digest rewrite. Passing local tests remains
only harness/adapter evidence and does not clear VAL-13 or any product, provider,
security, legal, deployment, sending, or spending gate.
