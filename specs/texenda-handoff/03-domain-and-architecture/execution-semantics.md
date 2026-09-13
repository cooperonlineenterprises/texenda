# Campaign, sequence, and automation semantics

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f08"></a>
## 8. Campaign, sequence, and automation semantics

**Decision status: AUTHORITATIVE DECISION.** Durable business state is separate from queue state and provider observations. One bounded workflow executor serves sequences and automations.

### 8.1 Three independent state planes

| Plane | Authority | Examples |
|---|---|---|
| **BUSINESS STATE** | Texenda transactional domain | Campaign revision/approval; frozen selection; execution cursor; cancellation; delivery plan; occurrence claim |
| **QUEUE / WAKEUP STATE** | Replaceable execution adapter | Payload job ID, retry count, lease, next poll; not proof a campaign completed |
| **PROVIDER DELIVERY STATE** | Provider evidence normalized by Texenda | Accepted request, delivered observation, bounce, complaint, delay, unknown acceptance |

A later complaint does not erase the historical fact that a request was accepted or delivered. Store independently timestamped facts rather than a single scalar status that loses important history.

### 8.2 Campaign lifecycle and approval

```text
draft -> in_review -> approved -> scheduled -> resolving -> ready -> dispatching
                                                              |           |
                                                              +--paused<--+
                                                                          |
                                                   dispatch_complete <----+

Any eligible pre-completion state -> cancelling -> cancelled
Validation/definition fault -> failed
Uncertain effect or unresolved evidence -> needs_attention
```

`dispatch_complete` means every candidate plan is terminal for dispatch. It does not mean inbox delivery, reading, or conversion. Maintain outcome `clean` or `with_errors`. An unknown acceptance prevents clean completion. An operator may explicitly close unresolved work as `closed_with_uncertainty`; its dedup tombstones remain, late evidence can attach, and automation must not interpret this as successful delivery.

Approval binds an immutable campaign revision, communication/representation revisions, sender, publication/purpose, segment/compiler versions, schedule window, tracking, primary channel, permitted alternatives, per-recipient contact maximum, candidate ceiling, monetary ceiling and current authority epoch. Editing any bound item invalidates approval. A tighter later safety policy remains effective without reapproval; a looser policy cannot expand the approved contact/channel/spend envelope.

**REVERSIBLE DEFAULT:** scheduled broadcasts resolve audience rules near the send window. Approval explicitly states that membership is evaluated then, not fixed by the earlier preview. The initial candidate ceiling defaults to the last preview's candidate count and must be shown/accepted. If resolution exceeds it, hold for reapproval—never silently truncate, auto-expand, or choose a random subset. A fixed-snapshot mode is available for operators who need an exact approved recipient set.

Snapshot construction uses a consistent database view, stages recipient records, and atomically marks the resolution run complete. No send begins from a partial or failed resolution. A practical initial timeout is 15 minutes; a timed-out run is discarded or resumed under the same valid snapshot only when the implementation can prove consistency. Do not page a changing audience and call it an immutable snapshot.

Freeze recipient/profile/endpoint selection and personalization inputs at final resolution/preparation. Before handoff, current eligibility can remove a recipient but cannot silently add a new one or retarget a changed endpoint. Content freshness and campaign expiry are rechecked.

### 8.3 Semantic keys

```text
campaign occurrence:
  campaign_id + occurrence_id + coordination_subject

workflow communication occurrence:
  execution_id + stable_node_id + occurrence_number + coordination_subject

explicit duplicate-equivalence claim:
  organization + approved_equivalence_scope + equivalence_family
  + business_occurrence_key + coordination_subject

channel delivery:
  delivery_plan_id + channel + endpoint_binding_version + effect_role

attempt / provider request:
  delivery_id (or immutable batch_id) + qualified provider-account namespace
```

IDs are not derived from message text, queue attempts, current contact email, or renderer output. A transient retry uses the **same** logical delivery and immutable provider request key/payload. An intentional resend is a new explicitly approved occurrence, not an edit to defeat deduplication. Person merges pause affected plans and reconcile old subject aliases before another claim is admitted.

### 8.4 Dispatch protocol

1. Claim eligible work with a short lease/fencing version; bulk workers use `SKIP LOCKED` only for work claiming. [S21](../09-reference/source-register.md#s21)
2. Under subject/scope locks, evaluate the current policy and claim semantic occurrence, pressure capacity and budget. Create a prepared Delivery with exact endpoint, payload digest and revision references. Commit.
3. Persist the handoff intent in the independent recovery journal. If this fails, do not send.
4. Acquire a short-lived final handoff permit in a second short transaction; recheck current restrictions, cancellation, expiry, deployment epoch, lease/fencing version, reservations and prepared digest. Mark in-flight and commit.
5. Call the qualified provider immediately with the immutable payload and key. No database lock is held across HTTP.
6. Record acceptance, definitive rejection, or uncertainty; append observations and outbox records. Finalize/release reservations according to proven outcome.
7. Reconcile delayed events and missing responses independently of campaign worker success.

A lease expiry is **not** proof the old worker did not call the provider. In-flight effects are never reassigned for a blind resend. Fencing protects database transitions, while qualified provider idempotency protects repeated remote requests; neither is a magical distributed transaction.

**REVERSIBLE DEFAULT:** send individual messages in the pilot. Add batches only after throughput evidence and batch contract tests. A batch freezes ordered membership, per-item digest, sender/account, and one request key. If an item is withdrawn before submission, abandon that unsubmitted batch and prepare a new one. After possible submission, do not change membership or split/reissue ambiguous items. A whole-request validation error is treated as definitely-not-accepted only when the provider contract proves that behavior.

### 8.5 Retry/error policy

| Error | Result |
|---|---|
| Invalid recipient syntax/content/schema | Permanent failure; no automatic retry |
| Verified permanent mailbox failure | Endpoint block; cancel matching pending delivery |
| Authentication, sender verification, or account policy rejection | Hold/pause route and alert; no alternative account escape |
| Rate limit | Qualified `Retry-After` or bounded backoff+jitter; recheck eligibility and expiry |
| Temporary infrastructure error | Bounded retry while still valid, using stable request identity |
| Known no-request-transmitted failure | Safe retry, still under final gate |
| Timeout/reset after request may have been accepted | `acceptance_unknown`; reconcile/reuse same qualified idempotency identity; no new payload/key |
| Conflicting idempotency payload | Quarantine programming/configuration fault; never fix by silently creating a new key |

Resend documents idempotency support for email and batch requests with a 24-hour retention window. Internal occurrence/effect deduplication must outlive that provider window. Do not retry an uncertain old request after its qualified window merely because an attempt limit remains. [S06](../09-reference/source-register.md#s06)

**REVERSIBLE DEFAULT:** maximum six automatic transient attempts with jittered increasing waits, never beyond message expiry or the provider's safe idempotency window. Retry budgets are settings, not authority to keep contacting a recipient. If evidence remains unresolved, hold and surface it. Provider-specific classifications must be contract-tested.

### 8.6 Pause, cancellation and recovery

Pausing stops new permits and claims. Cancelling marks pending plans terminal and stops further workflow actions; in-flight provider requests may complete. Resume performs live eligibility and expiry checks and preserves minimum spacing. It does not flush all overdue work.

An organization/workspace/sender/provider kill switch prevents new permits. A separate deployment send-disable gate survives restoring an old database. Safety ingestion and opt-out handling remain available when outbound sending is disabled.

A restore starts in recovery hold: compare backup time, authority epochs and independent journal coverage; replay all restrictive evidence; reconcile every possibly accepted handoff; rebuild derived counters; invalidate old leases/permits; inspect scheduled work; then issue a new live epoch after explicit approval. Unknown effects remain claimed/quarantined. No automatic provider failover exists.

### 8.7 Sequences and bounded automations

A sequence is a restricted workflow definition with linear steps; an automation adds event triggers and branches. **There is one authoritative executor and one cursor model.** `SequenceEnrollment` identifies membership/reentry; its displayed progress comes from the associated execution and step records.

V1 primitives: send approved communication; wait duration; wait until civil/absolute time; condition/branch; add/remove tag; set an allowlisted typed profile attribute; enroll/cancel a sequence; emit a typed event; wait for event with timeout; stop. Subscription changes require a valid proof-bearing permission command; there is no generic automation action “grant consent.” Approved outbound webhooks are an integration feature, not arbitrary URLs supplied by event content.

No arbitrary code, SQL, loops, unbounded recursion, parallel joins, autonomous channel selection, or cross-brand marketing triggers. Event-produced cascades have a correlation depth ceiling and unique trigger keys so tag changes cannot create an unbounded cycle.

Default reentry: one active execution per profile/program, and no automatic replay of a completed enrollment. A program may explicitly permit new executions for distinct business occurrence keys; repeatable marketing requires a visible reentry/cooldown policy. Merely publishing a new version does not restart subscribers.

Publishing creates immutable definitions with stable node IDs, schema version, handler compatibility and limits. Existing executions pin their definition/content revisions. New enrollments use the active version. Migrating existing runs requires a dry-run cursor/node mapping, dedup preservation, consent recheck and explicit approval; missing mappings are quarantined. Do not edit old definitions in place.

### 8.8 Step transitions, waits and timing

Each step transition is transactional: acquire subject coordination and execution/wait rows in the canonical lock order; verify expected cursor/revision; claim a unique step execution; apply domain changes or create a DeliveryPlan/outbox; advance cursor or establish wait; commit. Duplicate wake-ups become no-ops.

A send step advances on **qualified provider acceptance**, not a queued job, delivery observation, or email open. Acceptance uncertainty holds the run. Permanent ineligibility/expiry defaults to stopping the marketing run unless an approved explicit branch says otherwise. Pressure deferral keeps the same occurrence and does not advance.

Duration waits after a message are measured from actual acceptance, preventing a downtime catch-up burst. Absolute waits use the configured instant; if already expired, execute the explicit expired branch rather than immediately emitting multiple missed messages. Civil schedules store timezone and rule: spring-forward gaps move to the next valid instant; repeated fall-back times run once at the first occurrence. Email may use a labeled workspace-timezone fallback; regulated channels may not guess recipient jurisdiction/timezone.

To prevent lost event wake-ups, appending a subject's domain event and registering/claiming its waits use the same subject coordination lock and per-subject committed sequence. A wait records its lower event bound, predicate, deadline and timeout node. Registration checks already-recorded qualifying events before sleeping. Matching event and timeout transitions race on the same wait/execution version; exactly one branch wins. The default event deadline is based on the event's authoritative domain recording time, not an untrusted backdated timestamp. Late events remain historical facts and cannot retroactively undo an external effect.

Before handoff of goal-sensitive promotions, recheck the authoritative completion state and source-health watermark. “Has not purchased” is not true when required purchase ingestion is known stale. No response/open-based cross-channel escalation is supported.

**Consequences:** queue/workflow/provider replacement does not change progress or effect keys. **Revisit:** parallel joins, sophisticated signals, very high waiting cardinality or recurring recovery burden may justify a new execution adapter, but not moving consent or occurrence authority into it.

---
