# Production release and evidence plan

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Accepted interaction architecture and complete-handoff directive. Apply [package authority](../DECISION-STATUS.md).


## Release claims

The [release profiles](release-profiles.json) define what is enabled. Every enabled profile includes its parents. A mature email release does not require SMS, WhatsApp, native push or AI. A voice/agent claim does require its specific security, privacy and interaction evidence. WP-38 is a qualification study, not implementation or release of a phone/native channel; create a new bounded reviewed contract if it justifies building one.

**Five separate facts:** specified, implemented, tests executed, externally qualified, released. Do not collapse them. The handoff is specified and scaffold-tested; it has no Texenda app implementation or production qualification. All 125 product criteria begin NOT RUN.

## Release evidence packet

Record profile set, exact Git commit/build digest, compatibility manifest, database migration version, workflow-handler versions, policy versions, provider/account/sender qualification, gate owners/scope/expiry, workload profile, test results with logs/hashes, threat/restore review, change summary, rollback restrictions and named release/incident owner. Bind independent review and owner activation approval to that packet.

Use `release-evidence.template.json`. A PASS needs actual procedure, environment and output evidence. NOT RUN, UNKNOWN and blocked states cannot satisfy required criteria. N/A must identify the disabled channel/scope and reviewer; it cannot omit a difficult invariant. Packaging checksums or the harness's synthetic tests are not substitutes.

## Launch order

Synthetic unit/integration tests → no-send staging with actual provider configuration checks → owner-approved internal seed test → bounded genuine canary → observation → controlled expansion. Initial canary ≤250 recipients or the smaller genuine approved audience; do not create artificial mail merely to produce samples. Live sends need sender/legal/security/recovery/migration gates and exact approval. Candidates above the existing elevated-send threshold require the prescribed additional review/cooling-off process.

## Migration completion

A unit completes only when Texenda owns audience/consent and active sending, required sequences/automations are proved or deliberately resolved, forms/integrations point correctly, old opt-out behavior is preserved, historical data is migrated/archived intentionally, rollback is understood, and the observation period passes. Default observation is 30 days plus two ordinary publication cycles, whichever is longer. Rare publications need a reviewed alternative; never send extra messages just to pass a release clock. Critical incidents reset relevant observation.

## Revalidation

Provider contract/SDK, auth model, renderer, schema, workflow interpreter, runtime model, speech retention, channel policy or recovery changes trigger their relevant contract/security/acceptance subset. Credentials and safety restrictions are rechecked live; approval does not freeze them. A phased rollout can hold a feature independently while the email core stays operational.
