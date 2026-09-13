# Analytics and operational observability

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal roadmap v1.0; interaction additions explicitly below. Apply [package authority](../DECISION-STATUS.md).

<a id="i15"></a>
## 15. Analytics and operational observability

**Decision status: AUTHORITATIVE DECISION.** Measure what Texenda actually knows, with explicit denominators, coverage and time semantics. PostgreSQL domain records are the initial authority for counts; dashboards are rebuildable projections.

### 15.1 Metric contract

| Metric family | Exact meaning / source | Must not be confused with |
|---|---|---|
| People and profiles | Current retained organization subjects versus current brand-local profiles | Sum of brand profiles is not unique people |
| Active subscriptions | Active publication/channel memberships | Reachable endpoints or currently eligible recipients |
| Eligible audience preview | A point-in-time query interpretation and exclusion estimate | An approved fixed recipient list or a delivery guarantee |
| Frozen candidates | Finalized CampaignRecipient rows for one resolution run | A partial paginated query or last preview count |
| Logical communications | Unique occurrence/equivalence claims per subject | Channel variants, deliveries or retries |
| Outbound interruptions | Accepted or conservatively uncertain channel handoffs under pressure accounting | Provider HTTP calls, rendered drafts, onsite impressions |
| Delivery attempts | Individual qualified transport interactions, linked to one Delivery | Unique people reached |
| Accepted | Provider acknowledged accepting the request | Inbox placement, delivery, human viewing or success of the business goal |
| Delivered observation | A qualified provider delivery event | Reading or inbox rather than spam-folder placement |
| Bounced/complained | Distinct normalized observations, with type/source/coverage | Universal mailbox complaint coverage or changes to unrelated consent |
| Clicked | Qualified tracked link event, with bot/scanner confidence where available | Proof of purchase, person identity or human attention |
| Opened | Weak remote-content observation if tracking is enabled | Dependable reading, non-reading, or trigger for another channel |
| Onsite presentation | Render decision and separately recorded impression/dismissal | Outbound message or guaranteed human attention |
| Business outcome | Verified, source-attributed purchase/completion event | Causal lift caused by the campaign |
| Cost | Reserved upper estimate, provider-reported incurred usage and reconciled invoice where available | One currency-free counter or a guessed unit price |

Apple's Mail Privacy Protection can download remote content independently of engagement. Open data is therefore diagnostic/optional, not a reliable behavioral truth. [S15](../09-reference/source-register.md#s15) A provider's missing complaint event is not proof no one complained; maintain source coverage and use external sender-health reporting separately.

### 15.2 Counts and consistency

For each finalized campaign resolution:

```text
frozen candidates = pending + deferred + held + in_flight
                  + terminal_accepted + terminal_skipped
                  + terminal_rejected + terminal_cancelled
```

These are mutually exclusive **current dispatch-plan buckets**, not overlapping provider observations. Unknown acceptance is a held/needs-attention plan and does not count as accepted until evidence supports it. A separately approved `closed_with_uncertainty` disposition remains visible. Late provider events attach without changing candidate selection history.

Report normalized delivery facts separately; a delivery can be both historically accepted and later complained. Do not force a single status to erase facts. Campaign counters are derived from plan/effect records and periodically reconciled; caches never authorize completion.

Historical growth graphs must identify whether they are event-time cohorts or current-state snapshots. Deletion/erasure may change retained current counts; do not silently rewrite a historical graph to imply the audience was always that size. Forecasts and estimated audience counts are visually distinguished from observed results.

Default engagement definition: a qualifying click or verified business completion in the selected period, with the exact rule shown. Imported events are included only within known source coverage. Absence means no observed event within that coverage; when coverage is unknown, report unknown. Disclose attribution windows, identity limits and late-data corrections. Initial attribution is descriptive last qualifying campaign interaction within an explicitly configured window, not multi-touch causation. Do not ship an opaque composite engagement score.

### 15.3 Operational telemetry

Instrument form/command requests, unit-of-work commits, outbox age, due-work claim, eligibility decisions, content render, handoff permit, provider request, webhook inbox, normalization, execution transition, reconciliation and recovery. Correlate by opaque organization/workspace/campaign/execution/delivery IDs. Per-recipient IDs are restricted trace fields, never unbounded metric labels.

Required operational views:

| View | Minimum signals | Required operator action |
|---|---|---|
| Communication operations | Upcoming sends, competing work, caps/deferrals, expiries, candidate ceiling changes | Review/approve, reschedule, pause or retire |
| Deliverability | Sender auth/readiness, provider blocks, bounce/complaint evidence, external mailbox reports | Scoped pause and evidence-based investigation |
| Runtime | Queue age, due-work lateness, webhook normalization lag, worker leases, DB saturation, outbox backlog | Scale/tune, repair or pause unsafe dispatch |
| Workflow health | Stuck cursors, quarantined definitions, overdue waits, event coverage, unknown effects | Inspect deterministic reason; reconcile without replaying known effects |
| Safety | Pending unjournaled restrictions, expired qualification, stale source authority, invalid tokens/signatures, blocked permission attempts | Hold affected traffic; restore evidence/authority |
| Cost | Campaign/account/AI reserved, estimated, incurred and reconciled spend | Stop at ceiling; explicit owner approval to change future budget |
| Portfolio | Brand-level aggregates and shared incident exposure | No unrelated profile details for brand-only operators |

### 15.4 Initial alert policy

**Decision status: REVERSIBLE DEFAULT.** Start with conservative, explicit alerts and tune from observed data. Numerical thresholds are proposed operational defaults, not inbox-provider safe harbors.

- **Immediate critical:** unauthorized handoff; duplicate primary effect not contained by qualified idempotency; cross-brand data/permission leak; provider credentials exposed; missing safety-journal coverage; restore running without a new epoch. Disable affected sending and open an incident.
- **Safety processing:** an opt-out not durably applied cannot be acknowledged successful. If authenticated restrictive provider events remain unprocessed beyond 5 seconds or unjournaled restrictions exist, prevent relevant new handoffs. If scope cannot be identified safely, hold the provider account/organization conservatively.
- **Queue:** warning when routine ready-work p95 exceeds 30 seconds for 15 minutes; incident when lateness threatens an active approved dispatch window. Safety work has a separate reserved processing lane.
- **Unknown effects:** every `acceptance_unknown` creates an operations item immediately; unresolved after 15 minutes alerts the operator. A cluster of five unknown requests or >1% of recent handoffs, whichever is first material, pauses that route pending investigation.
- **Pilot deliverability:** any complaint during a ≤250-recipient canary pauses the remaining canary. Two permanent bounces trigger review before more canary traffic. Individual addresses are blocked regardless of campaign threshold.
- **Post-pilot deliverability:** inspect every complaint; warn at observed complaint ratio ≥0.05%. For at least 1,000 accepted requests and at least two complaints, automatically pause at ≥0.08%. Warn at hard-bounce ratio ≥1%, pause at ≥2% with at least 100 accepted requests or five permanent bounces. A provider's stricter rule overrides these settings. Keep numerator, denominator, time window and coverage visible; do not compare this denominator directly to a mailbox provider's differently defined spam metric.
- **Provider/auth:** verified sender-auth failure or provider policy/account block pauses the route. Do not classify a missing optional webhook as proof of provider outage; combine ingress health, provider responses and reconciliation.
- **Source health:** stale purchase/consent source coverage holds workflows whose decisions require that data. No “not purchased” interpretation from a failed feed.

**REVERSIBLE DEFAULT:** rolling 24-hour operational ratios with short-window anomaly views; tune only through versioned policy and owner review. A warning is not automatic permission to resume a paused route.

### 15.5 Privacy and retention

Keep consent and safety evidence separate from debugging telemetry. Use structured logs with an explicit field allowlist, not raw request bodies. No raw addresses, phone numbers, tokens, provider keys, full message content or sensitive cross-brand facts in traces or alert notifications.

Proposed defaults, subject to VAL-02: operational logs 30 days; sampled traces 14 days; raw provider payloads 30 days; normalized identified activity 13 months; daily logical backups 35 days; safety recovery journal 90 days. The active consent relationship, justified withdrawal/suppression evidence and live execution/idempotency records are not expired merely by the analytics schedule. Their retention follows the approved privacy policy and necessary replay/recovery horizon. Historical message content and erasable personalization are stored separately.

A privacy erasure creates a restrictive recovery-journal entry so restoring an older backup does not silently reintroduce the person. Reapply erasure/withdrawals before dispatch resumes. Pseudonymous hashes and HMACs are still protected data. Non-identifying aggregate retention may be longer only when reidentification risk is controlled.

### 15.6 Initial analytical implementation and change triggers

**REVERSIBLE DEFAULT:** PostgreSQL normalized events, indexed facts and rollups. Add asynchronous watermarked aggregation and time partitioning when measured maintenance cost warrants it. No read replica is used for send-time permission, deduplication, pressure, cancellation or current source authority.

**DEFER UNTIL TRIGGERED:** ClickHouse when reporting p95 remains >5 seconds after indexing/rollups, or analytics consumes >25% of primary resources across two operating review periods and causes transactional interference. Event row count alone is not a migration trigger. The analytics sink may be replaced; consent, occurrence claims, workflows and pressure reservations stay transactional.

**Downstream consequences:** counters, alerts and receipts are part of the first pilot, not a final polish phase. **Validation:** metric contract tests and reconciliation tests precede production. **Revisit:** revise thresholds/retention through policy and empirical evidence, never by letting an AI reinterpret a metric.

---
