# Data/schema and application contract implementation guide

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Accepted interaction architecture and complete-handoff directive. Apply [package authority](../DECISION-STATUS.md).


## Ownership and migration decisions

**Status: AUTHORITATIVE DECISION** for transaction ownership, scoping, keys and constraints. Physical table names and index tuning are **REVERSIBLE DEFAULTS** until measured. Use one PostgreSQL database, separate Payload and domain ownership, and one ordered deployment migration manifest. Domain safety transactions MUST NOT assume independent Payload calls share a Drizzle transaction.

Payload-managed drafts and sessions are not activated domain revisions. Publishing reads a selected draft revision, verifies freshness, creates a validated immutable domain revision and activates it in one domain transaction. An outbox updates draft badges/read models after commit. Failed read-model updates cannot reverse permission or approval.

## Suggested domain aggregate layout

| Aggregate/repository | High-value records | Required keys/constraints |
|---|---|---|
| portfolio | organizations, workspaces, properties, publications, memberships | organization-scoped unique slugs; verified origin binding; scope-compatible FKs |
| identity | people, identities, endpoint_bindings, workspace_profiles | unique exact identity per issuer/org; unique person/workspace profile; valid binding intervals; distinct block fingerprint |
| permission | subscriptions, consent_events, permission_grants, withdrawals, suppressions, preferences | unique profile/publication/channel membership; immutable evidence; scoped grant supersession; versions serialize with handoff |
| segmentation | segment_revisions, typed field definitions/values, tag assignments, source_coverage | immutable AST/compiler refs; unique tag assignment; type validation; coverage watermark |
| communication | briefs/revisions, representations, protected_fact_refs, templates | immutable approved revisions; channel-specific codecs; stale dependency markers |
| campaign | campaigns/revisions, approvals, resolution_runs, recipient_snapshots | finalized consistent-snapshot run before dispatch; unique occurrence/profile; immutable selection fields |
| coordination | occurrence_claims, delivery_plans, pressure_reservations, spend_reservations | unique equivalence/occurrence/subject; atomic allowance; endpoint duplicate guard; reservation outcome history |
| execution | workflow_definitions/revisions, enrollments, executions, step_executions, waits | stable node IDs; one active enrollment/program unless approved reentry; unique step occurrence; one wait winner |
| delivery | deliveries, attempts, batch_manifests, provider_inbox, normalized_events | permanent effect key; immutable payload/key once possible handoff; per-account event dedup |
| interaction | goals, constraints, assistant_preferences, proposals/revisions, approval_requests, sessions | expected base revisions; immutable proposal digest; scoped object refs; session never authoritative |
| agent_access | agent_principals, delegation_grants, agent_runs | issuer/client identity; current grant bound to principal/resources/actions/budget/time; revocation |
| operations | command_receipts, audit_records, decision_receipts, outbox, authority_leases, journal_coverage | command idempotency principal/route/key+digest; monotonic subject sequence; independent send epoch |

## High-value indexes

Indexes SHOULD follow known reads/claims, not speculative every-field indexing:

- memberships by authenticated principal and workspace, including active/revoked state;
- grants/withdrawals/suppressions by organization, subject/endpoint, applicable scope and effective time;
- subscriptions `(workspace, publication, channel, state, profile_id)`;
- due plans/executions `(state, next_due_at, priority, id)` and leased work expiry;
- occurrence/effect semantic keys as unique constraints, not merely secondary lookup indexes;
- provider inbox `(provider_account_id, external_event_id)` unique plus pending received time;
- workflow waits by subject/event type/deadline and per-subject event sequence;
- events by workspace, subject, type, recorded time; qualified fact projections for frequent rules;
- outbox pending cursor and consumer dedup keys;
- proposals by workspace/status/updated time; approval digest and expiry;
- agent runs by grant/status; grant revocation lookup;
- migration source mapping `(source_system, account_id, object_type, external_id)` with target identity and mapping revision.

Use partial indexes for pending work where measured. Do not partition early merely because future events might be large. Unique constraints on a partitioned event/claim design require explicit review so partitioning cannot remove lifetime deduplication.

## Locking and time

Use the canonical lock order in system architecture. No network/AI/rendering operation while holding a domain transaction. Claims use queue-style locking; audience resolution uses a consistent snapshot, not `SKIP LOCKED`. Database timestamps and committed subject sequence provide authority; untrusted source timestamps are retained as evidence only.

UTC instants + IANA zones. Duration waits after a send start at actual acceptance; spring gaps advance to the next valid instant; repeated fall-back time fires once. No inferred legal geography from a timezone or IP.

## Request contract envelope

Every mutation accepts a stable request key and expected revision where relevant. The client cannot set effective principal, role, scope authority or approval assurance. Resolve those server-side. Request metadata may declare requested workspace/object; it is checked against authenticated authority.

Suggested result envelope:

```json
{"command_id":"cmd_...","disposition":"committed","object_ref":{"type":"Campaign","id":"cmp_...","revision":4},"receipt_id":"rec_...","warnings":[]}
```

Error envelope uses a stable code, retryability, safe field paths and correlation ID. Suggested codes: `UNAUTHORIZED`, `SCOPE_DENIED`, `STALE_REVISION`, `INVALID_INPUT`, `IDEMPOTENCY_CONFLICT`, `APPROVAL_REQUIRED`, `APPROVAL_STALE`, `SOURCE_COVERAGE_UNKNOWN`, `POLICY_DENIED`, `TEMPORARY_HOLD`, `PARTIAL_RESULT`. Use appropriate HTTP 401/403/409/422/429/503 semantics without disclosing unrelated records.

Same request key and digest returns the same committed result. Same key/different digest conflicts. API request TTL is not business occurrence lifetime. Imported historic commands default to no live triggers.

## Privacy and payload storage

Encrypt payload/personalization snapshots and endpoint credentials; retain digests/references separately. Deleting a chat does not erase campaign authority. Erasure journals restrictive evidence so PITR cannot resurrect sends. HMAC fingerprints are pseudonymous personal data, not guaranteed anonymous identifiers. Retention is approved per record class; avoid permanent PII in audit prose.

## Definition and handler compatibility

Published workflow, representation and predicate versions declare required handler/codec versions. Release preflight queries active references; missing handlers block rollout. Expand/contract migrations precede code changes; rollback uses compatible binaries and current state, never old permission snapshots.

## Contracts included here

`command-catalog.json` freezes command names, permissions, risk and approval boundaries. `contracts/command-envelope.schema.json` fixes transport framing. Feature WPs implement closed per-command input/output schemas from this guide before handlers. These are design contracts, not a claim that an API server already exists. `state-machines.json` records allowed lifecycle transitions and explicit guards; prose execution semantics remains normative if a generated index disagrees.

## Consequence propagation and approval executor

The command catalog's consequence class is a minimum, not a bypass. Tag or attribute changes can trigger an existing automation. Before approving a live mutation the platform MUST deterministically evaluate possible external/ongoing effects and elevate review accordingly. A built-in/external agent may prepare changes; direct authority to draft a tag update is not authority to initiate unbounded sends. A previously approved integration/workflow may mutate only within its recorded policy envelope.

`CommitProposal` does not log an agent in as the human approver. It validates the exact proposal and issues only a constrained approved-command execution capability. The deterministic executor revalidates current authorizer permissions, proposal digest, command arguments, resource revisions, ceilings and current safety. Initiator, intermediary, authorizer and executor remain distinct in the receipt. Human-only C4 commands (safety release, delegation expansion, authority transfer, recovery release) are excluded from AI-committable bundles and retain their dedicated workflows.

Restrictive C4 actions such as a valid recipient withdrawal are deliberately different: do not impose MFA or a campaign-style approval delay on an account-free opt-out. Risk classes describe consequence; per-command authorization/approval rules determine the safe interaction.
