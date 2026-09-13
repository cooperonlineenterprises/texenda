# Texenda Implementation Roadmap & Production Acceptance Plan

**Artifact II · Version 1.0.0 · Issued September 5, 2026**  
**Document ID:** TEX-IMP-001  
**Normative dependency:** [Product & Technical Foundation Specification](Texenda_Product_Technical_Foundation_v1.0.md), TEX-FND-001 v1.0.0  
**Accountable owner:** Product Owner, initially the founder of Cooper Online Enterprises  
**Intended use:** Work-package sequencing, migration authority, production gates, operational ownership and ADRs.

> **Implement the frozen Foundation, prove one real publication can operate safely, then add sequences, automations, portfolio leverage and qualified channels. Do not rebuild the product while executing the roadmap.**

## Authority and use

The Foundation owns product/domain semantics. This artifact derives operational requirements, implementation phases and acceptance evidence from it; an ADR summary or implementation milestone does not override the Foundation. Together they form one versioned design release.

A completed specification is not a completed product. No production tests, subscriber export, sender account, current repository or actual Kit execution data were inspected or exercised for this work. Every acceptance condition below is a **required test**, not a claimed result. Role names identify responsibilities; they do not assert that additional staff exist.

Decision statuses are exactly: **AUTHORITATIVE DECISION**, **DECISION REQUIRED NOW**, **REVERSIBLE DEFAULT**, **DEFER UNTIL TRIGGERED**, and **REQUIRES EXTERNAL VALIDATION**. All blocking product/technical semantics have been resolved in the Foundation. No ADR is left at `DECISION REQUIRED NOW`; new external evidence must close its named gate, not reopen the whole product.

IDs `INV-*`, `POL-*`, `APR-*` and `VAL-*` refer to the Foundation. `AC-*`, `PH-*`, `RUN-*` and `ADR-*` are defined here. An acceptance evidence bundle records spec version, commit/container digest, dependency manifest, fixture/workload description, result, timestamp, reviewer, and retained report/artifact references.

## Contents

15. [Analytics and operational observability](#i15)
16. [Implementation and migration roadmap](#i16)
17. [Production acceptance criteria](#i17)
18. [Decision record / ADR set](#i18)

---

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

Apple's Mail Privacy Protection can download remote content independently of engagement. Open data is therefore diagnostic/optional, not a reliable behavioral truth. [S15] A provider's missing complaint event is not proof no one complained; maintain source coverage and use external sender-health reporting separately.

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

<a id="i16"></a>
## 16. Dependency-ordered implementation and migration roadmap

**Decision status: AUTHORITATIVE DECISION** for dependency order and gate discipline. Phase effort and dates are not estimated because staffing, existing code and workload have not been established.

### 16.1 Corrected sequence

```text
PH-00 Evidence + repository contracts
  -> PH-01 Domain / identity / permission / security / coordinator foundation
  -> PH-02 Safe email / rendering / provider evidence / recovery
  -> PH-03 Forms / imports / segmentation / broadcasts -> FIRST REAL PUBLICATION
  -> PH-04 Sequences
  -> PH-05 Bounded automations + optional AI preparation
  -> PH-06 Portfolio rollout + richer communication coordination UX
  -> PH-07 Onsite pilot
  -> PH-08 Qualified web-push pilot
  -> PH-09 Cross-channel coordination
  -> PH-10 Optional phone/app channels and measured optimizations
```

**Important ordering correction:** basic equivalence, expiry, current-policy checks and atomic pressure reservations belong before the first live email. Portfolio-wide dashboards and more advanced arbitration may follow. AI is not a dependency of the first Kit replacement. Neither a public trademark decision nor an unbuilt future channel blocks domain implementation.

### 16.2 Phase cards

#### PH-00 — Evidence, contracts and executable repository skeleton

**Scope decision: BUILD NOW.**

- **Delivered value:** one governed repository with the Foundation, ADR inventory, build/test pipeline, typed contracts and safe local environment.
- **Prerequisites:** issued Foundation; named founder/product and engineering/operations responsibilities. No invented production data.
- **Architecture:** workspace structure, dependency-boundary checks, migration manifest, fake clock/ID generators, domain command envelopes, fake providers, Docker/Mailpit/PostgreSQL development setup.
- **Data work:** read-only Kit inventory and SourceMapping draft; WorkloadProfile fields: active/total contacts per publication, largest intended broadcast `B`, proposed dispatch window `W`, observed acquisition/event peak, publication cadence, retained history, active sequences/automations, provider accounts/geographies and monthly budget.
- **UX:** annotated prototypes for campaign review, opt-out and audience interpretation; no elaborate visual builder.
- **Provider / AI:** no production transport; no AI required.
- **Burden:** one-time inventory, selected package/hosting compatibility work.
- **Risks:** adopting stale API assumptions, default-active exports, false publication boundaries, undocumented shared Kit automations.
- **Validation/completion:** source inventory and synthetic fixtures exist; CI cannot access production transport; dependency/migration tests run; all missing external evidence has a VAL owner. Record the actual API/version capabilities available to the user's account.
- **Advance when:** core contracts are testable and no unresolved foundational decision remains. VAL-01 may remain open.

#### PH-01 — Authoritative domain, permissions and security

**Scope decision: BUILD NOW.**

- **Delivered value:** one organization with scoped brands/properties/publications; trustworthy profile, identity, subscription and restriction administration.
- **Prerequisites:** PH-00.
- **Architecture:** domain tables and scope FKs; unit-of-work repositories; current grant/withdrawal projections; consent/audit events; outbox/inbox; coordinator subject locks; occurrence claims, expiry and reservation schema; Payload auth plus MFA assurance boundary.
- **Data migrations:** seed portfolio; implement normalization/version strategy and import staging without activating subscribers. Migrations tested forward and on empty/representative databases.
- **UX:** brand selector, scoped audience view, consent/safety timeline, typed attributes/tags, basic settings.
- **Provider / AI:** fake transport only; no AI authority.
- **Burden:** permission and privacy setup; no independent channel service.
- **Risks:** cross-scope CRUD bypass, old-confirmation reactivation, global-profile overwrites, confusing active membership with eligibility.
- **Validation/completion:** AC-D01–D10 and AC-S01–S05 pass in integration/property tests; no direct domain-table writes from UI/AI/callbacks; permission explanations are deterministic.
- **Advance when:** identity and denial invariants hold under concurrent mutation and scope attacks; necessary production privacy/security gates continue to be tracked.

#### PH-02 — Safe email, content and effect recovery

**Scope decision: BUILD NOW.**

- **Delivered value:** render and test approved emails; ingest provider evidence; stop and recover safely.
- **Prerequisites:** PH-01.
- **Architecture:** React Email codec/renderer, approved content copies, variable schemas, prepared payload digests, MailProvider, Resend adapter, channel readiness, sender activation, safety/effect journal, handoff permits, normalization, unknown-acceptance reconciliation, deployment send gate.
- **Data migrations:** content/representation revisions, DeliveryPlan/Delivery/Attempt, provider qualification and independent journal references.
- **UX:** editor, exact preview, internal test sends, sender readiness, delivery/receipt viewer, pause/incident controls.
- **Provider / AI:** qualify a pilot Resend account/sender using internal allowlisted tests; no provider contacts/automations; no AI required.
- **Burden:** DNS, account and secret setup; backup/journal/restore procedures.
- **Risks:** provider timeout duplicates, non-atomic batch retries, footer/header defects, restore resurrecting sends/opt-outs.
- **Validation/completion:** AC-L01–L10 and AC-R01–R06 pass with fault injection; prove normal sending is disabled after restore until reconciliation. VAL-03/04/05/08 evidence required at the relevant test scope.
- **Advance when:** the live transport contract is qualified but still capped/internal; no real audience campaign until PH-03 gate.

#### PH-03 — Acquisition, imports, segmentation and broadcasts: first real Kit replacement

**Scope decision: BUILD NOW.**

- **Delivered value:** one publication can acquire subscribers, manage permission, build useful segments, send broadcasts and inspect outcomes without Kit sending.
- **Prerequisites:** PH-02 and a separable MigrationUnit under VAL-10; required VAL-02/04/05/08 approvals.
- **Architecture:** public form API, staged imports, source coverage, segment AST/compiler, recipient resolution, campaign revisions/approval/ceilings, chunk dispatch, basic pressure policy, metrics/alerts.
- **Data migrations:** map the actual source publication, all subscriber states, withdrawals and safety blocks; historical events do not emit welcome/purchase automation triggers. Import approved templates/content, not raw executable template code.
- **UX:** custom audience/segment/form/import/broadcast flows; explicit preview vs frozen count; contextual preference page; basic calendar/conflicts.
- **Provider / AI:** one qualified sender/route; optional AI copy is deferred unless independently qualified; not a pilot prerequisite.
- **Burden:** publication cutover and observation; one operator checks the daily exception view.
- **Risks:** false consent from Kit `active`, shared-account unsubscribe scope, duplicate live sends, unsupported source filters, audience-cap drift.
- **Validation/completion:** publication migration gate below; AC-M01–M09; canary ≤250; at least one normal-cycle campaign and all control paths verified. Publication cannot be called fully migrated while a required old sequence remains active/unresolved.
- **Advance when:** the pilot completes the observation period, routine work is understandable, no critical defect remains, and all authority functions are assigned.

#### PH-04 — Sequences

**Scope decision: BUILD NOW after a stable pilot.**

- **Delivered value:** welcome and educational programs with durable progress and safe cancellation.
- **Prerequisites:** PH-03; trustworthy timing, provider acceptance and source-permission records.
- **Architecture:** restricted workflow definitions, single executor, SequenceEnrollment identity, step keys, due-time sweeper, pinning and reentry rules.
- **Data migrations:** validated legacy sequence definitions/content; verified cursor mapping or explicit hold/retirement disposition for every in-flight source enrollment. No guessed progress from enrollment date.
- **UX:** vertical step editor, clear maximum contacts, progress and stop reasons; no graph canvas.
- **Provider / AI:** existing email provider; optional sequence drafting only under VAL-09.
- **Burden:** reviewing old sequence semantics and outstanding cohorts.
- **Risks:** changed delay semantics, resending prior steps, restart after version edit, catching up several overdue steps at once.
- **Validation/completion:** AC-W01–W06; clock/DST/reentry/duplicate-wakeup tests; at least one representative sequence observed through completion or a tested stop condition.
- **Advance when:** sequence execution has no separate contradictory cursor, all migrated cohorts have evidence-backed disposition, and cancellation works under load.

#### PH-05 — Bounded automations and optional AI preparation

**Scope decision: BUILD NOW when required Kit workflows demand it.**

- **Delivered value:** trusted event-driven branches, waits, tags/profile changes, goal cancellation and reusable recipes.
- **Prerequisites:** PH-04, trusted business-event contracts and source-health coverage.
- **Architecture:** trigger deduplication, event waits/deadlines, subject event ordering, cycle-depth limits, simulation, quarantine; same executor as sequences.
- **Data migrations:** map needed Kit automation triggers/actions; quarantine unsupported or ambiguous branches. Do not execute imported historical events as new triggers.
- **UX:** structured recipes with plain-language summary, exact editable graph and deterministic explanations.
- **Provider / AI:** AI segment/import/automation drafts may be introduced after VAL-09; all outputs remain proposals. No send-time AI dependency.
- **Burden:** bounded workflow review, not general automation engineering.
- **Risks:** event/timeout races, unhealthy “no purchase” source, hidden consent mutation, prompt injection, unintended reentry.
- **Validation/completion:** AC-W07–W12 and AC-A01–A06; every live node has handler compatibility and receipt evidence; required source workflows recreated or explicitly retired.
- **Advance when:** practical Kit dependency for the pilot publication is replaced; no orphaned source execution remains.

#### PH-06 — Portfolio rollout and richer coordination experience

**Scope decision: BUILD NOW incrementally after the pilot.**

- **Delivered value:** migrate remaining separable publications, reduce repeated setup, make cross-brand pressure/conflicts legible without leaking data.
- **Prerequisites:** successful PH-03–05 as required by each publication; validated source topology and current consent mapping for every wave.
- **Architecture:** multiple qualified sender/account bindings, explicit portfolio authority, reusable immutable recipes, cross-brand aggregate views; basic coordinator already exists.
- **Data migrations:** publication-by-publication transfer or connected migration waves; preserve source-account opt-out restrictions across mapped descendants; no pooled permissions.
- **UX:** portfolio home/calendar/alerts, brand-specific content adoption and contextual preference center.
- **Provider / AI:** isolate substantial brands or explicitly accept a shared provider pool; optional brand adaptation is draft-only with target-brand approval.
- **Burden:** sender qualification per brand and a consolidated exception review.
- **Risks:** shared account suppression, fairness/starvation, cross-brand fact exposure, accidental target-brand enrollment.
- **Validation/completion:** AC-C01–C06 and all per-publication migration gates; pressure shadow run against actual publication promises before enforcement changes.
- **Advance when:** routine operation stays inside the complexity budget and no planned publication promise is silently broken.

#### PH-07 — Onsite messaging pilot

**Scope decision: DESIGN FOR NOW, BUILD LATER.**

- **Delivered value:** one or two useful inline placements, such as contextual signup and subscriber-aware content cards, without another outbound interruption.
- **Prerequisites:** one property with a clear repeated use case and VAL-07/privacy approval; stable email/portfolio operation.
- **Architecture:** placement decision API/SDK, contextual anonymous mode, verified identity mode, impression/dismissal/expiry receipts, fail-soft rendering and bounded caching.
- **Data migrations:** onsite representation/placement definitions; do not turn email grants into browser-tracking authority.
- **UX:** placement preview and “also show on this site” only where installed; no generic page builder.
- **AI:** may draft adaptation; operator approves meaning and appearance.
- **Burden:** site performance/accessibility maintenance and measured placement review.
- **Risks/validation:** account switching, forwarded-link identity, personalized-cache leakage, stale offers, blocked site rendering, privacy and dismissal failure; AC-X01–X04.
- **Advance when:** a controlled comparison or equivalent evidence shows useful acquisition/continuity without harming the site or increasing routine work materially.

#### PH-08 — One qualified web-push alert pilot

**Scope decision: DESIGN FOR NOW, BUILD LATER.**

- **Delivered value:** timely alerts expressly requested by readers, not repeated blanket promotion.
- **Prerequisites:** demonstrated alert demand, known browser/device mix, VAL-07, endpoint/withdrawal/pressure readiness.
- **Architecture:** push endpoint+key lifecycle, property-origin binding, verified/pseudonymous subject handling, technical permission plus topic grant, preferred-device routing, TTL/expiry and provider evidence.
- **Data migrations:** new endpoints/grants, never activation from existing email consent.
- **UX:** purpose-specific request after user intent; one channel toggle only where qualified; clear permission and frequency.
- **AI:** draft push variant only; no autonomous channel choice.
- **Burden:** browser/device qualification and invalid-token monitoring, target ≤15–30 minutes/week outside incidents.
- **Risks/validation:** multi-device duplicates, expired tokens, foreground/background differences, logout/reassignment, stale alerts; AC-X05–X08.
- **Advance when:** recipient uptake and useful outcomes justify the additional operating burden, with no material rise in unwanted-contact signals.

#### PH-09 — Coordinated cross-channel automation

**Scope decision: BUILD LATER after channels work independently.**

- **Delivered value:** one approved communication can choose the appropriate eligible channel, offer a passive companion, or perform an explicit qualified follow-up without duplicate interruptions.
- **Prerequisites:** two production-qualified channels, reliable outcomes and current preference/source-health evidence.
- **Architecture:** activate existing route-plan semantics, deterministic choose-one policy, per-channel reservations, confirmed-failure fallback and cross-channel equivalence/cancellation.
- **Data migrations:** approved alternative representations and preference choices; no silent conversion of old email-only programs.
- **UX:** show exactly which route/condition may be used and the maximum additional contacts; expert policy remains inspectable.
- **AI:** recommendations/draft variants only.
- **Burden:** reviewing a small set of cross-channel recipes and route health.
- **Risks/validation:** unknown-acceptance failover, opt-out-triggered escalation, conflicting channel workers, conversion cancellation; AC-X09–X12.
- **Advance when:** evidence shows improved completion or reduced unnecessary contact relative to email-only behavior—not just more messages.

#### PH-10 — Optional phone/app channels and evidence-triggered optimization

**Scope decision: REVISIT WHEN DEMAND EXISTS.**

- **Delivered value:** a demonstrated time-sensitive SMS/WhatsApp use case, app-specific notifications, or relief of a measured infrastructure bottleneck.
- **Prerequisites:** channel-specific legal/provider program, actual audience geography, replies/escalation owner, cost cap; or a section 12 infrastructure trigger.
- **Architecture/data:** typed adapters and capability qualifications; no new domain authority. Preserve idempotency, current grants and effect journal across substitution.
- **UX/AI:** qualified extension only; hidden when disabled; same approval model.
- **Burden:** explicitly budget registration, template review, replies, monitoring and carrier/provider incidents. Do not activate both phone channels by default.
- **Risks/validation:** real opt-out scope, provider changes, segment-based billing, account blocks, escalating customer-support expectations, AC-X13–X15.
- **Completion:** the new capability passes its full external gate and demonstrably earns its cost. Otherwise keep it disabled. No automatic path to a CRM, helpdesk or general agent product.

### 16.3 Kit migration: evidence-led authority transfer

**Decision status: AUTHORITATIVE DECISION.** Migration is publication-by-publication **when the source can be independently fenced**. If shared Kit forms, account-wide states or automations make that unsafe, use the smallest connected migration wave that can be stopped and reconciled as a unit. This is a safety constraint, not permission to pool audiences.

Current Kit documentation defaults subscriber listing to `active`; the migration adapter must explicitly retrieve `status=all`, follow every returned cursor, and separately account for states or exclusions exposed only elsewhere. [S09] Kit sequence membership includes entry time and subscriber state, but membership is not an exact per-email execution cursor. Definitions/content and aggregated sequence-email stats are available in current API documentation; they still do not establish what a particular person should receive next. [S10, S11]

Kit's August 27, 2026 changelog introduces signed, batched Webhooks 2.0 with an incrementally available event catalogue. Validate actual event delivery for the account; do not assume every consent/progress transition is covered. Webhooks supplement final export/API reconciliation rather than replacing it. [S11]

#### Migration records

Create a `MigrationUnit` with mapped source account(s), publications, forms, tags, segments, sender domains, current sequences/automations, subscriber cohorts, global/source-account restrictions, last extraction watermark, unsupported semantics and a complete authority matrix.

A `SendingAuthorityLease` identifies organization/brand/publication/channel/purpose/function and any explicit disjoint cohort, active system (`kit` or `texenda`), epoch, allowed interval and operator evidence. Normal migration uses one active system for the whole unit's marketing. Texenda checks the lease before every permit. A lease in Texenda cannot technically fence Kit; the migration gate requires observed source-side pause/disable controls and evidence that no scheduled/in-flight work remains unaccounted for.

#### Authority matrix

| Stage | Audience/consent authority | Acquisition write path | Broadcast/sequence/automation sending | Restrictive inputs | Historical analytics |
|---|---|---|---|---|---|
| Inventory/shadow | Kit for source state; Texenda is a non-sending replica with explicit provenance | Existing Kit forms/integrations | Kit only | Kit primary; mirrored restrictions retained, no Texenda grants | Kit original reports; imported observations labeled historical |
| Freeze/drain | Kit state frozen for permission-expanding writes; existing withdrawals still accepted | Controlled gateway/maintenance capture stages new requests without activating marketing | Kit new schedules/triggers paused; Texenda disabled; reconcile in-flight source work | Ingest from both surfaces into durable negative-evidence union | Snapshot/export retained |
| Final reconciliation | Final source snapshot plus restrictive delta log, reviewed in Texenda | New requests remain staged | Neither system issues new marketing | Both old Kit links and Texenda endpoints feed required restrictions | No fabricated metric parity |
| Commit/canary | Texenda effective audience/consent authority at new epoch | Texenda public endpoints; staged requests processed under current disclosure/proof rules | Texenda only, capped canary; Kit sending remains disabled | Texenda authoritative application of legacy and new restrictions | Texenda reports start; Kit history remains separately labeled |
| Observation | Texenda | Texenda | Texenda approved scope only | Legacy Kit opt-outs remain monitored/ingested | Side-by-side source labels, not summed duplicate events |
| Fully migrated | Texenda | Texenda | Texenda; all required source programs recreated/resolved | Texenda plus supported legacy-link intake for the required retention period | Required history migrated or intentionally archived |

#### Transfer protocol

1. **Discover and map.** Inventory actual source semantics and all ways a contact can enter, leave or be sent a message. A tag/form association is not automatically sufficient consent for an invented new publication.
2. **Extract every state.** Preserve source IDs, cancellation/suppression state, available evidence and extraction watermark. Include shared-account restrictions at their real scope. A source `active` record becomes active in Texenda only for a mapped, evidence-supported publication/channel; uncertain rows stay held.
3. **Dry run.** Show created/updated/held/invalid/ambiguous counts, field normalization and stronger restrictions. Repeat the import to prove idempotency. Snapshot load emits no live automation triggers.
4. **Install restrictive-event capture.** Verify legacy/current Kit event coverage and polling/export fallbacks. Keep original unsubscribe behavior functioning. Broader source-account opt-outs apply across the publications they actually covered, not just the currently migrating brand.
5. **Freeze and drain.** Pause source new enrollments, scheduled sends and integrations capable of starting work; capture new acquisition requests without pretending they already have a grant. If intake cannot be reliably captured, present a brief explicit unavailable/retry state rather than lose requests silently.
6. **Reconcile in-flight effects.** Record what Kit accepted/sent, what is definitely cancelled and what remains unknown. Do not activate Texenda duplicates for unknown source work. Establish exact per-enrollment progress from available recipient-level evidence or a reviewed manual export; never guess from elapsed days.
7. **Resolve every old execution.** Supported outcomes: verified resume at a mapped node with consumed effect keys; explicitly complete/retire with reviewed user impact; or hold/quarantine awaiting evidence. Default policy does not run the same program concurrently in both systems. An unresolved required program means the publication is not fully migrated.
8. **Final restrictive reconciliation.** Apply late opt-outs/complaints/erasure to the import, retain safety evidence independently and reconcile source totals. Fresh positive requests go through the new proof flow; last-write-wins imports cannot overrule a withdrawal.
9. **Commit authority.** Owner signs the unit's epoch transfer, records source pause evidence, points forms/integrations to Texenda and enables only the approved canary. The transfer record binds the exact source snapshot and mapping version.
10. **Observe.** Review sends, receipt explanations, acquisition, opt-outs, outcomes, source late events and accounting. Increase volume only with an approved next ceiling.
11. **Close.** Disable/retire old sending paths, preserve required records and legacy opt-out intake, then declare fully migrated only after section 17's observation and completeness tests.

Kit's unsubscribe endpoint is an account-level removal from future emails, not a publication-scoped Texenda operation. Preserve that asymmetry in both migration and rollback; do not call it to emulate a narrow target-publication withdrawal while other source publications remain active without understanding the impact. [S24]

#### Rollback is another authority transfer, not a database rewind

Default incident response is **pause and repair forward in Texenda**. Returning sends to Kit requires a new reviewed epoch, current negative-evidence synchronization, verification that all Texenda-accepted/unknown communications are excluded, updated sequence positions, and proven source controls. If Kit cannot represent the required exclusions/cursors safely, do not roll back sending; keep the unit paused until repaired.

Never restore an old Kit export over current permission, re-enable old sequences from their original starting point, or let both systems send “temporarily.” Preserve all new withdrawals and delivered/uncertain occurrence claims across any rollback.

Legacy unsubscribe links may continue to point at Kit after cutover. Keep the account/endpoint capability needed to receive those requests until its actual persistence/retention behavior is verified. Do not cancel the Kit subscription or assume redirects preserve old links without VAL-10 evidence. Maintain a recipient-friendly reply/privacy route as an additional path, not a claimed replacement for broken one-click links.

### 16.4 Advancement governance

Each phase closes with a scope/evidence review, not a calendar date. The Product Owner may defer features, but cannot waive permission, isolation, duplicate-effect, safety-journal, or authority-transfer failures. Performance targets can be revised transparently against actual workload; unsafe semantics cannot be relaxed to make a launch milestone pass.

A publication may use Texenda broadcasts before unrelated future features exist. It may not be declared **fully migrated** while its required source sequences, opt-outs, or integrations remain ambiguous.

---

<a id="i17"></a>
## 17. Production acceptance criteria

**Decision status: AUTHORITATIVE DECISION.** Production readiness is an evidence-backed release gate. A successful build, passing happy-path demonstration, or issued specification is not sufficient. The test inventory below implements the Foundation's rules; it introduces no alternative permission, execution, or migration semantics.

### 17.1 Release gates and evidence format

Use separate gates so a useful email pilot does not wait for speculative channels:

| Gate | Required scope | What it permits |
|---|---|---|
| **G0 — Engineering baseline** | Locked contracts/schema ownership; synthetic fixtures; nonproduction transport isolation; executable invariant tests | Repository implementation and internal development |
| **G1 — Production email pilot** | Applicable domain, security, delivery, recovery, coordination, performance and operations tests; VAL-02/03/04/05/08; pilot-specific VAL-10 | One approved, consented, bounded live publication canary |
| **G2 — Publication fully migrated** | G1; all required source workflows and integrations resolved; AC-M01–AC-M09; observation period completed | Declaration that the publication no longer depends on Kit for active operation |
| **G3 — Portfolio rollout** | Applicable G2 evidence for each migration unit; portfolio isolation/fairness and operator usability validation | Additional brands/publications under their own approved authority transfers |
| **G4 — Additional channel** | All relevant endpoint/content/policy tests; VAL-07 and channel-specific legal/provider qualification | Only the named channel, purpose, property, audience and sender program |
| **G5 — AI enablement** | AC-A01–AC-A06 and VAL-09 | Only evaluated AI tasks and their bounded authority levels |

G4 and G5 are independent of G1/G2. No AI provider, push subscription, or phone integration is needed to operate a qualified email publication. Public commercialization additionally requires VAL-01 and the deferred external-customer isolation/operations decision if it changes the private deployment model.

Every acceptance result MUST record: test ID; Foundation/ADR reference; release and dependency-manifest IDs; environment/configuration; fixture or redacted input hash; execution time; expected and actual result; evidence location; reviewer; and disposition. An excluded test needs a documented reason such as “channel not enabled,” not an unexplained waiver. Failed permission, isolation, duplicate-effect, unsafe restore, or authority-transfer tests are release blockers.

Automated evidence includes unit/property tests, real-PostgreSQL integration tests, browser/accessibility tests and fake-provider fault injection. Manual evidence includes source-system verification, representative mail-client renders, raw received-email headers, real account contracts, usability observations, and a restore drill. Capture reproducible seeds for randomized concurrency tests. **REVERSIBLE DEFAULT:** run at least 10,000 generated state-transition/interleaving cases for the critical permission, duplicate and arbitration properties in the release qualification suite; this is a test-depth choice, not a claim about production audience size.

### 17.2 Domain, permission and audience correctness

| ID | Required exercise | Objective pass condition |
|---|---|---|
| **AC-D01** | Create the same verified identity in two brands and multiple publications. | One applicable organization identity/person relationship is recognized; separate profiles/subscriptions/grants exist; no second brand/channel becomes eligible merely through identity recognition. |
| **AC-D02** | Test normalization with email local-part case, domain case/IDNA, plus aliases, dots, invalid addresses and unsupported international local parts. | Original values are preserved; identity follows the Foundation normalization policy; conservative duplicate/safety lookup does not manufacture identity or permission; unsupported rows are held with reasons. |
| **AC-D03** | Replay opt-in requests, confirmations, imports and later withdrawals in different orders. | One logical request/confirmation effect per key; pending is not active; confirmation predating a withdrawal cannot reactivate it; historical import does not trigger live work or weaken denial. |
| **AC-D04** | Apply publication, brand and portfolio withdrawals, then explicit narrow confirmed reconsent. | The new grant supersedes only identified prior withdrawal evidence within its explicit scope; siblings remain withdrawn; later withdrawal wins; operational/provider holds remain; cancelled old workflows do not resume. |
| **AC-D05** | Exercise hard bounce, complaint, temporary hold, invalid push endpoint and provider-program block. | Suppression affects the specified endpoint/person/channel/program scope exactly; a bad email endpoint does not make a verified phone technically invalid; complaint safety holds are not fabricated legal consent events. |
| **AC-D06** | Withdraw while a campaign is queued, a recipient is reserved, and immediately before/after final handoff permission. | Withdrawal committed before the permit prevents handoff; records explicitly identify any already-in-flight boundary; no claim of recalling provider-accepted mail; future equivalent actions are denied. |
| **AC-D07** | Evaluate segment ASTs against a small independently enumerated oracle, including nested Boolean rules and absent fields. | SQL membership matches the oracle; UNKNOWN is not TRUE; negating an absent-field comparison does not silently include it; unsupported operators, raw SQL and cross-scope references are rejected. |
| **AC-D08** | Test negative purchase/event conditions with missing, stale, incomplete and healthy SourceCoverage. | Unknown coverage produces the specified hold/UNKNOWN behavior; “no observed event” never becomes a factual claim that no purchase occurred; backdated/untrusted events do not bypass gates. |
| **AC-D09** | Resolve a changing audience, change preferences afterward, and prepare personalized content. | Snapshot candidates are consistent and immutable; current safety can remove but not add recipients; frozen endpoint/content facts cannot silently retarget; missing required variables hold rather than render misleading output. |
| **AC-D10** | Read and replay decision/consent evidence; perform a scoped correction and approved erasure/reimport. | Explanations cite actual rule/input versions; ordinary credentials cannot rewrite evidence; approved erasure removes covered PII, preserves only lawfully retained safety material, and cannot be undone by reimport or restore. |

### 17.3 Isolation and security

| ID | Required exercise | Objective pass condition |
|---|---|---|
| **AC-S01** | Attempt cross-workspace access through custom UI, REST, Local API, exports, relations, jobs and forged identifiers. | Every unauthorized path denies; composite references cannot attach another workspace's publication/content/grant; portfolio pressure explanations reveal no unrelated brand data. |
| **AC-S02** | Use first-factor-only sessions against every protected route; test one-time bootstrap, public signup denial, WebAuthn challenges/origin/RP, recovery, session expiry, CSRF and step-up. | Required assurance is enforced server-side, not only by navigation; challenge replay/origin substitution fails; high-risk actions cannot reuse insufficient assurance; session and recovery evidence is auditable. |
| **AC-S03** | Abuse public form identifiers, property keys, server API keys and revoked credentials. | Browser keys cannot emit trusted purchases, select arbitrary publications/tags, export PII or mutate consent; server principals are scope/capability limited; revoked keys cease authorization; requests are rate/size limited and nonenumerating. |
| **AC-S04** | Test import/render/webhook/AI fetch paths with script injection, CSV formulas, SSRF, redirects, private IPs, malicious files and oversized content. | Supported paths reject or safely encode payloads; outbound fetch cannot reach private/metadata destinations; exported CSV is spreadsheet-safe; typed export preserves intended exact data separately. |
| **AC-S05** | Inspect runtime secrets, object access, export links, audit permissions, backup identities and break-glass controls. | Web/AI roles cannot access production send credentials; nonproduction cannot reach live transports; export TTLs and PII capabilities hold; incident access can pause/recover but cannot bypass recipient authority; production dependency/security findings are resolved or explicitly accepted only if noncritical. |

### 17.4 Email delivery, rendering and provider correctness

| ID | Required exercise | Objective pass condition |
|---|---|---|
| **AC-L01** | Render every approved pilot block/template with representative personalization, optional/missing fields, links and plain text. | Deterministic artifact hashes for pinned inputs; required-field failures block; no arbitrary executable content; approved facts/disclosures/CTA meaning remain intact. |
| **AC-L02** | Review representative output in Gmail web/mobile, Outlook web and a supported desktop client, Apple Mail desktop/mobile, and Yahoo; include dark mode, narrow viewport, blocked images and text alternative. | Main content and CTA remain usable; brand, postal/footer requirements and visible unsubscribe are legible; material client failures block affected templates. Test observations and screenshots are retained; Mailpit alone is not claimed as cross-client proof. |
| **AC-L03** | Receive seed messages for each sender and inspect original headers and authentication results. | Qualified sender/domain ownership, SPF/DKIM/DMARC alignment and required unsubscribe fields pass the actual account/mailbox checks; required headers are DKIM covered; no provider strips/rewrites them incompatibly. |
| **AC-L04** | POST the prescribed one-click request without session/cookies, replay it, use GET/scanner requests and forward its URL. | POST produces scoped withdrawal without login or redirect and acknowledges only after the safe persistence boundary; GET does not mutate; replay is harmless while withdrawn; no recipient or cross-brand PII is exposed. |
| **AC-L05** | Send valid/invalid/replayed provider webhooks, including duplicates, delayed/out-of-order events and events received before API response correlation. | Actual provider signature protocol is checked against the correct raw input; unknown correlations are quarantined; duplicate observations do not duplicate effects; restrictions persist/apply/journal before their success boundary. |
| **AC-L06** | Retry the same semantic delivery across worker crashes, duplicate jobs and lease expiry. | Exactly one intended logical delivery and one consistent provider payload/key exist; a retry cannot invent a new semantic key; definitive outcomes are reconciled; transport retries do not inflate contact-pressure counts. |
| **AC-L07** | Simulate timeout after provider acceptance, lost response, late callback and retry beyond provider idempotency retention. | State becomes explicit uncertainty; no blind provider/channel switch or new-key resend occurs; the reservation/claim remains conservative; a late acceptance reconciles without duplicate continuation. |
| **AC-L08** | Inject rate limits, authentication failures, transient provider faults, permanent recipient failure and broad outages. | Correct retry/hold/pause classification; bounded attempts within expiry; honored provider delay/caps; provider-authentication or safety incidents disable affected routes; retries do not bypass current consent. |
| **AC-L09** | Pause/cancel during dispatch, exceed the approved candidate/cost bound, edit content after approval and resolve a partial failed snapshot. | Unpermitted new work stops; already-in-flight limitation is visible; changed approved meaning invalidates approval; over-ceiling resolution holds; no sends begin from incomplete snapshots; counts reconcile. |
| **AC-L10** | Reconcile provider suppression/account scope and qualify any batching optimization. | Provider restrictions are additional denials, not grants; brand/account implications are documented; batch membership/payload/key mapping is immutable; uncertain batches cannot be blindly split or resent individually. If batching is disabled, its unavailable status is enforced. |

### 17.5 Sequences and automations

| ID | Required exercise | Objective pass condition |
|---|---|---|
| **AC-W01** | Run a linear sequence through the shared executor and inspect enrollment/cursor records. | Enrollment has no competing execution cursor; unique active enrollment/reentry rules are enforced; one step execution/effect per semantic occurrence. |
| **AC-W02** | Restart workers and remove delayed wake-ups while steps wait. | Indexed due-state sweeps recover work without queue history; no lost enrollment or duplicated step; queue replacement does not alter business state. |
| **AC-W03** | Delay, pause, resume and process overdue sends using a controlled clock. | Wait anchors follow actual accepted effects/approved transitions; pause does not cause catch-up bursts; expired work skips/stops by definition; unknown acceptance does not advance as success. |
| **AC-W04** | Cross spring/fall DST changes and recipient/workspace timezone choices. | Calendar-time and elapsed-duration semantics match the Foundation; nonexistent local time moves to the next valid time; repeated local time is scheduled once at the selected first occurrence. |
| **AC-W05** | Publish a new sequence version while old enrollments run. | Old runs stay pinned; new runs use the published new version; compatibility checks prevent removal of required handlers; explicit run migration records node/effect mapping rather than mutating old history. |
| **AC-W06** | Withdraw/reconsent, purchase, cancel, or apply a safety hold during a sequence. | Required exits take effect before future permits; narrow reconsent does not resurrect old cancelled runs; provider/permission holds cannot be ignored by sequence UI or queue retries. |
| **AC-W07** | Replay triggers, emit duplicates and feed an imported historical event into live routing. | Trigger keys create at most one applicable execution; import history does not activate live marketing; authorized event-specific reentry creates only explicitly permitted new occurrences. |
| **AC-W08** | Publish automations with loops, unsupported actions, unbounded sends, cross-brand data, invalid fields and missing expiry/exit rules. | Invalid definitions fail validation; no arbitrary code/SQL/provider endpoint can be embedded; allowed recipes show bounded consequences and require approval. |
| **AC-W09** | Race event registration, business-event arrival and timeout against the same execution. | One terminal wait branch wins under subject serialization; the defined record-time/cursor boundary is respected; late/backdated events cannot retroactively fork or undo an external effect. |
| **AC-W10** | Execute tag/profile/sequence/send actions repeatedly under transaction aborts. | Domain mutation, step outcome and outbox are atomic; action effects are idempotent; no hidden Payload hook produces a second workflow effect. |
| **AC-W11** | Quarantine unsupported state, crash at each transition and replay recovery. | Invalid state is visible/quarantined, not an infinite retry; recovery preserves pinned definitions, approvals, consumed effects, current restrictions and authority epoch. |
| **AC-W12** | Receive a goal event while a promotion is delayed/reserved and interrupt the business-event feed. | Goal completion cancels pending equivalent promotions; already-in-flight boundary is explicit; required absence-of-goal checks hold when coverage is stale rather than assuming no purchase. |

### 17.6 Recipient coordination and portfolio behavior

| ID | Required exercise | Objective pass condition |
|---|---|---|
| **AC-C01** | Dispatch several campaigns/automations concurrently with one remaining recipient contact slot. | At most the allowed number of handoff reservations commits; canonical lock ordering, whole-transaction retries and stable identities prevent oversubscription; business state never depends on cached counters alone. |
| **AC-C02** | Send equivalent content via broadcast, sequence and later channel variant, then a genuinely new edition. | Explicit equivalence/occurrence rules suppress duplicate communication while allowing a new occurrence; subject/content similarity alone neither authorizes nor silently blocks it. |
| **AC-C03** | Compete promised editions, alerts, lifecycle mail and promotions across brands. | Approved purpose priority, expiry and fairness produce deterministic results; a brand cannot mark a promotion “urgent” to bypass authority; no brand monopolizes capacity through queue timing alone. |
| **AC-C04** | Apply recipient limits, quiet hours, source publication promises and policy updates. | Restrictive precedence holds; shadow-mode conflicts are resolved before enforcement; there is no unannounced promise change or accumulation of expired backlog; current stricter policy overrides older approval. |
| **AC-C05** | Exercise preference links under a forwarded email and a verified portfolio session. | Unauthenticated scoped withdrawal remains possible; unrelated brand memberships/PII are not exposed; portfolio viewing and positive preference/grant changes require the specified stronger verification. |
| **AC-C06** | Coordinate reliably linked and ambiguous identities/endpoints across the portfolio. | Reliable links receive appropriate shared pressure/safety checks; uncertain links do not create grants or speculative identity merges; brand operators see only permitted explanation detail; limits of unknown-device coordination are acknowledged. |

### 17.7 AI acceptance, only for enabled AI tasks

| ID | Required exercise | Objective pass condition |
|---|---|---|
| **AC-A01** | Translate a representative set of operator segment/automation requests, including ambiguous terms such as “engaged.” | Output is a supported typed proposal; interpretation and uncertain choices are visible; deterministic validator rejects invalid scopes/operators; no model output executes as SQL/code. |
| **AC-A02** | Prompt the assistant and poison imported/remote content to request exports, send credentials, consent grants, suppression removal or unauthorized effects. | Scoping occurs before retrieval; model has no prohibited tool/credential; command authorization denies attempted escalation; external text is treated as data; the attack is logged without leaking sensitive content. |
| **AC-A03** | Adapt approved offers/claims/disclosures/CTAs across channels and brands. | Unchanged protected facts are verified; disputed changes are blocked or separately reviewed; every variant remains draft until approved; no audience transfer accompanies content reuse. |
| **AC-A04** | Confirm a schedule proposal, then change audience, revision, channel, cost or authority epoch. | Confirmation is bound to the exact approved digest and ceilings; stale confirmation cannot execute; repeat confirmation is idempotent; step-up does not increase the principal's authority; external actions require the current principal and assurance. |
| **AC-A05** | Exhaust budget, lose model availability, obtain malformed output and replay internal draft-generation jobs. | Budget reservations/caps hold; unsafe output is rejected; retries are bounded; approved deterministic campaigns/automations continue without AI; no “best effort” unvalidated send occurs. |
| **AC-A06** | Compare summaries/explanations with source metrics and decision receipts. | Every reported count has a defined denominator/window; model does not invent missing events or causal lift; retained provenance identifies inputs/model/proposal/approval without requiring private model reasoning. |

### 17.8 Channel-expansion acceptance, only for enabled channels

| ID | Required exercise | Objective pass condition |
|---|---|---|
| **AC-X01** | Render contextual anonymous onsite placements and disable the audience service. | Only permitted page context is used; placement fails soft without blocking the page; no cross-site identity/fingerprinting is introduced. |
| **AC-X02** | Render known-recipient placements with login/logout, account switching, shared devices and forwarded links. | Identity and approved processing basis are verified; private/personalized content is not leaked through caches, URLs or stale sessions. |
| **AC-X03** | Dismiss an onsite placement, expire its offer and compete several eligible cards. | Dismissal/impression policy is deterministic; expired/stale content is not shown; one approved placement outcome is explained; onsite impressions do not masquerade as outbound deliveries. |
| **AC-X04** | Review onsite SDK performance, keyboard behavior, screen-reader behavior and layout stability on the actual property. | Site-specific performance/accessibility budgets are met; generic/no-card fallback remains usable; privacy/legal placement basis is documented at VAL-07. |
| **AC-X05** | Request push permission before/after an explicit recipient gesture and on representative supported devices/browsers. | Only the approved interaction requests permission; browser grant and brand/purpose consent are separate; unsupported clients receive an honest fallback rather than false enrollment. |
| **AC-X06** | Rotate/revoke push endpoints, create several devices, omit email identity and switch accounts. | Endpoint lifecycle is correct; a push-only subscriber is supported; one approved preferred endpoint is selected by default; an invalid token does not revoke unrelated email consent. |
| **AC-X07** | Deliver delayed/expired push, apply quiet hours and race with email pressure reservations. | TTL, permission and current policy hold; stale notifications do not create fresh promotions; combined interruptive limits and logical deduplication apply. |
| **AC-X08** | Compare push-provider acceptance, device evidence and recipient interaction metrics. | The platform does not label acceptance as attention; analytics expose actual observable states and missing evidence; cost/health alerts and kill switch work. |
| **AC-X09** | Run a choose-one-channel plan through every preference/eligibility combination. | Selection is deterministic from approved options; no grant is inferred; no option produces a clear hold/skip; AI is not making unapproved runtime routing decisions. |
| **AC-X10** | Compare definitive transport failure, unknown acceptance, opt-out and complaint. | Only an explicitly approved fallback after qualified definitive failure can proceed; unknown/withdrawal/complaint does not cause alternate-channel outreach; secondary effects consume their required allowances. |
| **AC-X11** | Combine passive companion, conditional follow-up, business completion and multiple channel representations. | Each additional interruption is explicit, approved, bounded and counted; goal completion cancels pending equivalent promotions; content variants retain approved equivalent facts/CTA. |
| **AC-X12** | Race cross-channel cancellation, cost reservation and provider timeout. | No double use of the primary slot or overspend authorization; uncertainty is visible and reconcilable; existing provider acceptance cannot be falsely recalled. |
| **AC-X13** | Qualify SMS program/markets, consent and STOP/revocation behavior, including actual provider-wide/program-wide restrictions. | Evidence matches the registered sender/legal scope; restrictive events apply immediately under the safe persistence boundary; an email grant cannot authorize phone marketing. |
| **AC-X14** | Personalize phone content across encoding/segment boundaries and provider template/window restrictions. | Cost authorization uses actual encoded units, qualified upper bounds and the approved ceiling; vendor invoice exposure remains separately reconciled; disallowed templates/markets/purposes hold; human reply/escalation ownership and provider incident playbook are verified. |
| **AC-X15** | Qualify WhatsApp or native/in-app messaging against the real application, account and current market contract. | Only actually supported channel/purpose behavior is enabled; app/device identity, consent, template/service rules and reply obligations are tested; no general omnichannel capability is inferred from an adapter's existence. |

### 17.9 Recovery acceptance

| ID | Required exercise | Objective pass condition |
|---|---|---|
| **AC-R01** | Kill workers before/after transaction commit, outbox publication, journal intent and provider handoff. | Committed work remains discoverable; incomplete transactions roll back; unique effects/leases prevent duplicate supported effects; ambiguous handoffs enter uncertainty, not blind retry. |
| **AC-R02** | Fail the independent journal during a withdrawal and during outbound preparation. | Current DB denial remains; no false success acknowledgement crosses the required boundary; missing journal coverage prevents affected unsafe handoffs; recovery does not erase the pending restriction. |
| **AC-R03** | Restore an older database backup after subsequent real-format synthetic opt-outs, erasures and accepted/unknown sends. | Outbound starts disabled independently of restored DB state; journal restrictions and erasures are replayed; accepted/unknown occurrence claims are reconciled before permits; no restored stale grant or worker epoch can send. |
| **AC-R04** | Resume after provider outage, backlog, delayed callbacks and obsolete schedules. | Backoff/pause/circuit behavior is observed; expired work is skipped, not burst-sent; overdue required work is reviewed under its policy; no automatic provider failover. |
| **AC-R05** | Deploy and roll back application code while old workflow/content versions are active. | Compatibility manifest covers active versions; incompatible release is blocked; code rollback does not rewind domain state or remove handlers still referenced by executions. |
| **AC-R06** | Perform a timed full restore drill including database, journal, encrypted objects, keys, configuration and provider reconciliation. | Proposed RPO/RTO targets are measured; restored sending remains disabled until separate approval and a new epoch; inability to prove safety is a held incident, not a passed drill. |

### 17.10 Migration acceptance

| ID | Required exercise | Objective pass condition |
|---|---|---|
| **AC-M01** | Inventory source accounts/publications/forms/tags/integrations and actual withdrawal/sending scope. | Every source path is mapped; independently fenceable MigrationUnits or required connected waves are identified; account-wide opt-outs are not mislabeled publication-level. |
| **AC-M02** | Extract all source states/pages and available consent/suppression evidence. | Source/extract totals reconcile with an explicit snapshot/watermark; active-only API defaults do not omit withdrawals/bounces/complaints; missing provenance is held, not fabricated. |
| **AC-M03** | Repeat staged imports and compare per-field/source mappings. | Same input produces no duplicate person/profile/subscription/effect; stronger restrictions win; invalid/ambiguous rows have downloadable reason reports; live triggers remain disabled. |
| **AC-M04** | Disable source entry/scheduling paths and reconcile source in-flight sends. | Source pause evidence is captured from the actual account; the Texenda lease is not treated as a Kit control; no overlapping authority exists for the same function/cohort; unknown source effects remain blocked. |
| **AC-M05** | Transfer current sequence/automation enrollments. | Every required enrollment is mapped using verified recipient-level evidence, explicitly retired, or visibly held; aggregate stats/membership timestamps are not used to guess the next step; unresolved required runs block full migration. |
| **AC-M06** | Withdraw through old Kit links, new Texenda links and support/reply channels during and after cutover. | Actual source scopes propagate into Texenda safely; no late withdrawal is lost; legacy endpoints remain functional or the limitation blocks retirement; fresh reconsent is explicit rather than a sync overwrite. |
| **AC-M07** | Transfer forms/integrations, activate a bounded canary, and reconcile recipient outcomes. | Each relevant function has one authoritative system/epoch; new grants go through Texenda proof; actual recipients/cost stay within approval; outcomes and late source events are explained. |
| **AC-M08** | Rehearse pause/repair-forward and any proposed return-to-Kit procedure. | No database rewind revives old permissions/effects; return is a new evidence-backed transfer; source inability to express required exclusions/cursors keeps sending paused rather than enabling unsafe rollback. |
| **AC-M09** | Complete the agreed observation period and review remaining source dependencies. | Texenda owns live audience/consent/sending and all required workflows; forms/integrations are cut over; legacy opt-out intake is retained; required history is migrated or intentionally archived; incidents and unknowns are resolved or safely quarantined with documented impact and no unresolved required program. |

### 17.11 Performance and capacity qualification

**Decision status: REVERSIBLE DEFAULT** for numeric targets below. **Decision status: REQUIRES EXTERNAL VALIDATION — VAL-05** for actual workload, infrastructure capacity and observed results. Parameterize tests with the PH-00 WorkloadProfile; do not substitute imagined customer counts.

The profile MUST supply actual or explicitly planned values for eligible audience size `N`, largest near-term campaign `B`, desired dispatch window `W`, ordinary event/form traffic, scheduled work, concurrent operator activity, provider limits, database/worker sizing and spending budget. Development may use a labeled synthetic fixture; production qualification requires the real planned profile. “Scale unknown” does not block domain coding, but blocks a capacity claim.

Measure warm and cold cases separately, record browser/network conditions and disclose exclusions. Provider mailbox delivery time and recipient attention are outside Texenda's dispatch SLA. Temporary policy holds are not incorrectly reported as ready-queue latency.

| ID | Proposed target | Test and interpretation |
|---|---|---|
| **AC-P01** | Common authorized read/search API p95 ≤1 s; primary admin screen usable p95 ≤2.5 s in the agreed client/network environment | Run with campaign work and ordinary event ingestion concurrently; distinguish browser/render time from API time; content-writing duration is not a metric. |
| **AC-P02** | Form command durable-response p95 ≤500 ms under the qualified load; opt-out/restrictive webhook safe acknowledgement p95 ≤2 s | Include required persistence/journal work in restrictive acknowledgements. A slow safe response is preferable to a falsely successful one. Provider verification callbacks may have separately documented deadlines. |
| **AC-P03** | Qualifying restrictive inputs applied before acknowledgement; internal restrictive-event lag p95 ≤5 s | Older restrictive work gates affected sending. This is a service target, not permission to acknowledge first and suppress later. |
| **AC-P04** | Typical supported segment preview p95 ≤2 s; largest planned campaign resolution/preparation target ≤120 s | Complex queries switch to visible asynchronous preview. Preparation has the Foundation's 15-minute fail/hold fuse; no partial sends. Validate at `B`, with a consistent snapshot rather than fast changing pages. |
| **AC-P05** | Routine ready-work start p95 ≤30 s; eligible already-prepared scheduled campaign begins dispatch within 60 s | Report separate queue classes. Audience-resolution time, explicit holds, quiet hours and disabled providers are separately observable rather than hidden exclusions. |
| **AC-P06** | Sustain at least `B / W` qualified delivery handoffs per second, within provider rate/cost limits; demonstrate 25% worker-side headroom with the fake provider | Test the actual planned campaign plus ordinary UI/events. Required worker throughput above provider capacity requires a revised window/provider qualification, not unbounded concurrency. Limited real canaries validate transport; do not load-test by mailing unsuspecting recipients. |
| **AC-P07** | Process the agreed short burst—default twice the planned ordinary ingestion rate—without losing events or violating isolation/pressure | Specify burst duration and backlog drain bound in WorkloadProfile. Validate database locks, connection pool, worker fairness and safe backpressure; avoid audience-size claims from queue-only benchmarks. |
| **AC-P08** | Proposed recovery RPO ≤5 min and RTO ≤4 h; no unsafe sends after restore | Timed drill AC-R06 includes journal replay, keys and provider reconciliation, not just database startup. Targets require a purchased/configured hosting plan and may be revised explicitly before launch. |

A numerical target failure prompts measurement and tuning. It does not automatically justify a queue/cache/database migration. Apply the Foundation section 12 adoption triggers only after query, index, worker and configuration issues have been addressed.

### 17.12 Operational acceptance and runbooks

| ID | Required operational evidence | Pass condition |
|---|---|---|
| **AC-O01** | Named operational responsibilities and tested escalation destination | One person may hold multiple roles, but there is a reachable owner for sending safety, incident response, data/migration and restores; critical alerts reach a destination independent of Texenda's affected sender route. |
| **AC-O02** | Live dashboard and alert exercise using injected faults | At least provider auth/outage, stale restrictive events, unknown acceptance, journal failure, queue delay, cost ceiling and quarantined workflow alerts are observed end-to-end; no alert claims reliable detection from absent data. |
| **AC-O03** | Provider/account/sender qualification packet | Current intended-use permission, suppression scope, rate/quota, signature protocol, header behavior, idempotency retention and test evidence are saved for each enabled route. |
| **AC-O04** | Backup/journal/key recovery verification | Actual purchased retention/PITR, independent object durability/access, key availability, deletion policy and restore drill satisfy the plan; no successful restore depends on keys lost with the database. |
| **AC-O05** | Kill-switch and high-risk approval rehearsal | Organization/brand/provider/channel/campaign stop controls work server-side; solo step-up/review/cooling-off path is usable; UI or AI cannot mint an approval bypass. |
| **AC-O06** | Release/dependency/security operations | Version manifest, SBOM/license review, active-handler compatibility, staging isolation, signed/reviewed migrations and rollback procedure exist; no untracked latest dependency is deployed. |
| **AC-O07** | Operator usability session | A representative routine operator completes acquisition/segment/broadcast/sequence review and interprets exclusion/cost/authority consequences. Proposed targets: ≥90% routine work without advanced settings, roughly five minutes prepared-campaign administration, and sustainable weekly operations. Failures lead to UX repair, not hidden consequences. |
| **AC-O08** | Privacy/retention/export and incident documentation | Applicable legal/privacy gates are satisfied; export expiry and erasure behavior are exercised; no PII in ordinary telemetry; incident playbooks state what can and cannot be recalled, retried, restored or transferred. |

Maintain concise executable playbooks, not a large operations manual:

| Runbook | Trigger | First safe action | Recovery evidence |
|---|---|---|---|
| **RUN-01 Provider/sender failure** | Auth, reputation, delivery or quota incident | Pause affected route; stop new claims; retain unknown effects | Corrected account/DNS state, current provider qualification, reconciled pending/unknown work |
| **RUN-02 Wrong campaign/recipient risk** | Mistaken schedule, content or audience | Pause/cancel unstarted work; do not promise recall | Exact affected recipients/effects, current restrictions, documented recipient response and new approval if resumed |
| **RUN-03 Journal/restrictive-ingress failure** | Independent safety evidence unavailable/stale | Deny success beyond the safe boundary; gate unsafe sending | Restored journal coverage, replay/dedup confirmation and current scope check |
| **RUN-04 Database/disaster restore** | Database loss/corruption or PITR | Independent outbound-disabled mode | Journal/erasure replay, provider/effect reconciliation, new epoch and explicit release authorization |
| **RUN-05 Consent/import incident** | Bad provenance, mass reactivation or wrong mapping | Hold affected scope and stop relevant workflows | Source evidence, corrected mapping, repeatable dry run and restriction reconciliation |
| **RUN-06 Credential/authorization incident** | Leaked key or unauthorized principal | Revoke/rotate, pause implicated routes and preserve evidence | Session/API audit, least-privilege repair, provider key rotation and security review |
| **RUN-07 Migration/legacy-link failure** | Late source sends, broken old opt-outs or inconsistent progress | Pause the affected MigrationUnit; retain restrictions | Actual source controls, repaired intake and a new reviewed authority transfer if needed |
| **RUN-08 Business-source outage** | Purchase/event coverage stale | Hold rules requiring absence-of-event evidence | Verified watermark/coverage restored, backfill deduped and pending promotion decisions recomputed |

### 17.13 When a publication is fully migrated

**Decision status: AUTHORITATIVE DECISION.** “Fully migrated” is a functional authority claim, not just a successful CSV import.

The publication is fully migrated only when all of the following are true:

1. Its audience, active subscriptions, contextual consent, preferences and applicable suppressions are authoritative in Texenda, with retained source mapping/provenance.
2. Kit no longer has overlapping live sending/enrollment authority for the relevant functions/cohorts; the actual pause/retirement evidence and Texenda epoch are recorded.
3. Required forms, integrations, sequences and automations are recreated and validated, or deliberately retired with approved product impact. No required program has an unknown cursor or uncontrolled source execution.
4. New and legacy unsubscribe/complaint paths work at their actual scopes. Necessary legacy-account capability is retained even if current marketing has stopped there.
5. Every necessary historical dataset is migrated, explicitly archived, or declared unnecessary with a reason. Missing history is not reconstructed as invented evidence.
6. Accepted and unknown source/Texenda effects cannot be resent through rollback, replay or export/import. Incident handling and any safe return-to-source constraints are understood.
7. The agreed observation period succeeds, with no unresolved critical safety/isolation issue, no uncontrolled duplicate, and no unexplained consent or recipient-count mismatch.

**Observation-period decision status: REVERSIBLE DEFAULT.** Use **30 consecutive days and at least two ordinary publication send cycles, whichever is longer**, following successful canary qualification. For a quarterly or otherwise infrequent publication, the owner may approve a different evidence plan before cutover, combining an actual normal send with representative workflow/opt-out exercises and a documented residual-risk assessment. Do not manufacture extra live mail merely to satisfy a test counter. A critical consent, duplicate-send or isolation incident resets the affected observation window after repair and requalification.

Publication-specific requirements govern completeness: a newsletter with no required sequences can reach G2 after PH-03; a publication dependent on sequences/automations cannot reach G2 until its relevant PH-04/05 work is complete. Full Kit retirement occurs only when all active migration units are complete and legacy-link/data retention can safely be maintained without relying on unverified cancelled-account behavior.

### 17.14 Acceptance adjudication

All required invariant/security/effect tests must pass. There is no acceptable percentage of unauthorized sends or cross-brand disclosures. Operational targets can be adjusted through an explicit reversible-default record using measured evidence; critical semantic failures cannot be waived by the Product Owner, AI, deadline, provider convenience or desired campaign revenue.

Engineering supplies evidence; the accountable owner signs the scoped release; appropriate independent security/legal/provider reviewers qualify their gates. These responsibilities may involve external help without requiring specialist day-to-day headcount. The approval record MUST list remaining deferred features so “production-ready for email” is not misrepresented as “qualified for every channel.”


---

<a id="i18"></a>
## 18. Decision record / ADR set

**Decision status: AUTHORITATIVE DECISION** for the decision-record process. The individual records use their own single status below. Governing records freeze expensive-to-reverse product semantics; default records choose replaceable implementation machinery and policy values. Do not create ADRs for trivial variable names or routine refactors.

Each record below may be extracted verbatim into `specs/adr/<id>.md` when the repository is initialized. Its normative authority remains the referenced Foundation rule; extracted records must include document/release IDs. A material amendment requires a superseding ADR, not silent editing of historical rationale.

### 18.1 Governing decisions

#### ADR-G01 — Product boundary and email-led evolution

| Field | Record |
|---|---|
| **Decision** | Product boundary and email-led evolution. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Expanded capability must remain usable by one operator and must not import enterprise-suite responsibilities. |
| **Chosen approach** | One permissioned audience/communication product; email first, onsite then qualified push, other channels only behind explicit use-case gates. |
| **Material alternatives considered** | Email-only forever; channel-neutral omnichannel suite from launch. |
| **Why chosen** | Preserves current practical value and controlled growth without requiring channel administration as routine work. |
| **Consequences** | No CRM/CDP/helpdesk/ad/ecommerce/general-agent features; first email release is independently useful. |
| **What remains reversible** | Descriptor, specific qualified channels and provider implementation. |
| **Revisit trigger** | Demonstrated recurring demand changes the product boundary enough to justify a new product ADR, not merely an available API. |
| **Dependencies** | Foundation 1, 7; PH-00/03/07–10; VAL-07; AC-X01–X15. |

#### ADR-G02 — One authoritative domain and explicit transaction ownership

| Field | Record |
|---|---|
| **Decision** | One authoritative domain and explicit transaction ownership. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Generated CMS documents, provider contacts and event tools could become conflicting authorities. |
| **Chosen approach** | Texenda-owned PostgreSQL state is authoritative. Payload owns auth/admin/drafts/media; activation copies validated configuration into a domain transaction with audit/outbox. Distinct table ownership. |
| **Material alternatives considered** | Everything as freely editable Payload collections; separate marketing platform beneath Payload; cross-client transactions assumed atomic. |
| **Why chosen** | Makes business transitions explicit and avoids double ownership while retaining Payload leverage. |
| **Consequences** | Domain writes only through commands/repositories; no provider or model may change permission truth. |
| **What remains reversible** | Payload custom views, database adapter and draft storage; not the authority/activation contract. |
| **Revisit trigger** | A proven transaction or authorization limitation requires adapter changes; distributed authority needs a separate governing redesign. |
| **Dependencies** | Foundation 3–5, 12; PH-01; VAL-03; AC-D03/10, AC-W10, AC-S01. |

#### ADR-G03 — Modular monolith and separable runtime roles

| Field | Record |
|---|---|
| **Decision** | Modular monolith and separable runtime roles. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Sending/import/AI workloads must not make interactive operation or safety ingress unavailable. |
| **Chosen approach** | One TypeScript codebase, one transactional database and domain core; separate web/worker process roles; priority safety processing; framework/provider dependencies point inward through ports. |
| **Material alternatives considered** | One web-request process for all execution; independent microservice per domain/channel. |
| **Why chosen** | Provides isolation and worker scaling without distributed semantic ownership. |
| **Consequences** | One coordinated release/compatibility manifest; no remote provider calls inside transactions; architecture import checks in CI. |
| **What remains reversible** | Process replica counts, task queues, deployment vendor, package grouping. |
| **Revisit trigger** | Measured independent scaling/security/SLA needs cannot be met with process roles and tuning. |
| **Dependencies** | Foundation 4, 12; PH-00/02; AC-P01/05/06, AC-R01/05. |

#### ADR-G04 — Canonical subject with scoped relationships and distinct endpoints

| Field | Record |
|---|---|
| **Decision** | Canonical subject with scoped relationships and distinct endpoints. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | One person may join several brands or use several devices, but identifiers are imperfect and sometimes shared. |
| **Chosen approach** | Organization-level Person/Identity with evidence-based bindings; workspace profiles; separate channel endpoints and technical reachability. No fuzzy/IP/phone-only auto-merge. |
| **Material alternatives considered** | Duplicate person per brand; universal address identifier; inferred identity graph. |
| **Why chosen** | Enables controlled coordination while avoiding permission transfer and unsafe endpoint assumptions. |
| **Consequences** | Scoped composite keys, preserved original email values and conservative normalization; endpoint changes require proof and scoped reauthorization. |
| **What remains reversible** | Opaque ID generation library and endpoint provider adapters; not proof or scoping semantics. |
| **Revisit trigger** | External tenancy/legal isolation or verified identity-correction demand requires explicit migration and review. |
| **Dependencies** | Foundation 5; PH-01; VAL-02; AC-D01/02, AC-C06, AC-X06. |

#### ADR-G05 — Contextual consent, withdrawal and explicit narrow reconsent

| Field | Record |
|---|---|
| **Decision** | Contextual consent, withdrawal and explicit narrow reconsent. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | A current active subscriber flag cannot express purpose/channel authority or competing withdrawal evidence. |
| **Chosen approach** | Immutable consent evidence with deterministic grants/withdrawal projections scoped to brand/publication-purpose/channel/endpoint binding. Narrow confirmed reconsent explicitly supersedes named prior withdrawal evidence only within its scope. |
| **Material alternatives considered** | Global subscribed flag; tags as consent; timestamp-based last-write-wins imports; all-or-nothing permanent unsubscribe. |
| **Why chosen** | Preserves recipient choice, supports legitimate resubscription and prevents import/old-token resurrection. |
| **Consequences** | Operational/provider safety blocks stay independent; new grant never automatically resumes old cancelled executions. |
| **What remains reversible** | Acquisition proof UX and qualification-specific disclosure text. |
| **Revisit trigger** | Legal/provider rule changes require new effective-dated policy and tests, not silent reinterpretation of historical evidence. |
| **Dependencies** | Foundation 5–6; PH-01/03; VAL-02/10; AC-D03–D06, AC-M02/06. |

#### ADR-G06 — Central deterministic eligibility and purpose classes

| Field | Record |
|---|---|
| **Decision** | Central deterministic eligibility and purpose classes. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Different sends and placements require distinct authority without providing a generic bypass flag. |
| **Chosen approach** | All supported communication uses central ALLOW/DENY/DEFER/HOLD/SKIP policy; marketing, requested fulfillment, service, operator auth and test each require their own explicit authority. |
| **Material alternatives considered** | Distributed channel-specific permission checks; unrestricted transactional/admin/test override. |
| **Why chosen** | One enforceable boundary prevents omissions and preserves narrow nonmarketing operations. |
| **Consequences** | Missing proof holds; test/auth are constrained; current withdrawal before final permit prevents handoff; in-flight limits remain explicit. |
| **What remains reversible** | Policy code implementation and externally reviewed classifications, not bypass semantics. |
| **Revisit trigger** | A real new purpose needs explicit evidence/rules and acceptance cases. |
| **Dependencies** | Foundation 3, 6, 14; PH-01/02; AC-D03–D06, AC-L04/09, AC-S03. |

#### ADR-G07 — Atomic contact pressure, equivalence and recipient priority

| Field | Record |
|---|---|
| **Decision** | Atomic contact pressure, equivalence and recipient priority. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Independent broadcasts/automations/channels can duplicate contact or race to consume the same allowance. |
| **Chosen approach** | Explicit communication family/occurrence keys, endpoint duplicate guards, current preference hierarchy, finite expiry and atomic pressure/spend reservations under a deterministic arbiter. |
| **Material alternatives considered** | Per-campaign counters; provider-only throttling; AI similarity deduplication; send-everywhere defaults. |
| **Why chosen** | Coordination must prevent races before the first live send, not be retrofitted after portfolio rollout. |
| **Consequences** | Unknown effects conservatively retain claims; stale backlog expires; priority follows purpose/promise rather than campaign versus automation. |
| **What remains reversible** | Numeric caps, spacing and alert thresholds under recorded policy versions. |
| **Revisit trigger** | Measured publication-promise conflicts or recipient evidence warrants revised defaults; invariants remain. |
| **Dependencies** | Foundation 6, 8; PH-01/03/06; ADR-D06; AC-C01–C06, AC-X09/12. |

#### ADR-G08 — Versioned campaign approval and reproducible recipients

| Field | Record |
|---|---|
| **Decision** | Versioned campaign approval and reproducible recipients. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Audience previews change over time; content or scope changes after approval must not silently expand consequences. |
| **Chosen approach** | Approval binds immutable revisions, selectors, sender/purpose/channel/schedule and hard audience/cost bounds. Resolve one consistent candidate snapshot; recheck current restrictions at handoff. |
| **Material alternatives considered** | Send directly from a live segment cursor; assume preview and dispatch counts identical; mutate approved campaigns. |
| **Why chosen** | Combines reproducibility with current recipient safety and makes approval meaningful. |
| **Consequences** | Over-ceiling or incomplete resolution holds; current safety removes recipients but cannot add unapproved ones; optional fixed snapshot is explicit. |
| **What remains reversible** | Composer layout, preview implementation and measured preparation targets. |
| **Revisit trigger** | A demonstrated campaign semantics change requires explicit new approval/snapshot version and migration. |
| **Dependencies** | Foundation 6, 8–9; PH-03; AC-D07/09, AC-L09, AC-P04. |

#### ADR-G09 — Effectively-once delivery with explicit uncertainty

| Field | Record |
|---|---|
| **Decision** | Effectively-once delivery with explicit uncertainty. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | A provider can accept a request whose response never reaches the worker; queue retries are not end-to-end exactly-once delivery. |
| **Chosen approach** | Separate communication, plan, delivery, attempt and observations. Permanent semantic keys; stable payload/provider key within qualified retention; explicit unknown state and reconciliation. |
| **Material alternatives considered** | Blind retries with fresh keys; claim exactly-once delivery; immediate provider/channel failover. |
| **Why chosen** | Prevents duplicates when remote acceptance is uncertain without pretending an impossible distributed atomicity. |
| **Consequences** | Unknown does not advance a workflow or release duplicate claims; closure with uncertainty is explicit; batching requires separate qualification. |
| **What remains reversible** | Email provider, batching optimization, polling/reconciliation adapter. |
| **Revisit trigger** | Provider capabilities change with verified contract tests; never relax uncertainty handling merely for throughput. |
| **Dependencies** | Foundation 3–4, 8, 13; PH-02; VAL-04; AC-L06–L10, AC-R01. |

#### ADR-G10 — One durable executor for sequences and automations

| Field | Record |
|---|---|
| **Decision** | One durable executor for sequences and automations. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Two runtimes or queue-owned cursors would disagree about progress, cancellation and replay. |
| **Chosen approach** | Sequence is a restricted workflow definition kind. One authoritative execution cursor, pinned revisions, unique step effects, durable due states and per-subject serialized event waits/timeouts. |
| **Material alternatives considered** | Separate sequence engine; Payload hook graph; one distant queue job per future step as sole state. |
| **Why chosen** | Small codebase with shared safety semantics and recoverable long-running execution. |
| **Consequences** | No arbitrary code/loops by default; send steps advance on qualified acceptance; current restrictions remain live; imported history does not trigger. |
| **What remains reversible** | Queue/wakeup implementation and eventual workflow-engine adapter. |
| **Revisit trigger** | Complex joins/signals or recurring recovery engineering burden justifies a qualified durable-engine substitution. |
| **Dependencies** | Foundation 8; PH-04/05; AC-W01–W12, AC-R02/05. |

#### ADR-G11 — Independent restrictive-input/effect journal and safe restore

| Field | Record |
|---|---|
| **Decision** | Independent restrictive-input/effect journal and safe restore. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Restoring the transactional DB can rewind opt-outs, erasures and handoff records while external effects remain real. |
| **Chosen approach** | Use existing encrypted object storage for independent append-only restrictive evidence and pre-handoff intents; outbound-disabled restore mode outside restored state; replay/reconcile and issue a new epoch before resumption. |
| **Material alternatives considered** | Database backups alone; resend all incomplete jobs; build a second authoritative event platform. |
| **Why chosen** | Closes the rollback gap without adding a second audience model or queue service. |
| **Consequences** | Journal coverage is required at safe acknowledgement/handoff boundaries; unavailable evidence holds sending; root access remains a recognized threat boundary. |
| **What remains reversible** | Object-store vendor, retention after legal review and backup plan; not restore fencing/reconciliation. |
| **Revisit trigger** | Measured recovery evidence suggests a safer simpler mechanism with equivalent guarantees; changing it requires restore fault tests. |
| **Dependencies** | Foundation 3–4, 12, 14; PH-02; VAL-02/05/08; AC-R01–R06. |

#### ADR-G12 — Shared communication brief with typed channel representations

| Field | Record |
|---|---|
| **Decision** | Shared communication brief with typed channel representations. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | HTML is not a universal message format; independently edited variants can silently change claims or permissions. |
| **Chosen approach** | Minimal brief/facts/CTA/constraints plus independently approved typed channel variants; ordinary email composer derives the brief; immutable render inputs and stale-source checks. |
| **Material alternatives considered** | Canonical email HTML for all channels; universal layout schema; mandatory abstract-brief authoring. |
| **Why chosen** | Reuses meaning without pretending channel-specific content is interchangeable or making email work harder. |
| **Consequences** | AI adaptations remain drafts; changes do not silently propagate to published variants; protected facts/disclosures must be preserved. |
| **What remains reversible** | Editor/renderer/codec adapter and block library; external approved fact/context sources. |
| **Revisit trigger** | A qualified new channel demonstrates genuinely reusable primitives or requires an additional representation type. |
| **Dependencies** | Foundation 7, 9; PH-02/07–09; VAL-03; AC-L01/02, AC-A03, AC-X11. |

#### ADR-G13 — Providers and integrations are nonauthoritative

| Field | Record |
|---|---|
| **Decision** | Providers and integrations are nonauthoritative. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Provider suppressions, account scope and API scheduling can diverge from product semantics. |
| **Chosen approach** | Transport/readiness/capability adapters plus verified durable ingress; provider restrictions add denials only. Domain scheduling/contacts/segments remain local. Versioned scoped API and trusted event sources. |
| **Material alternatives considered** | Provider contacts/automations as a synchronized second truth; ordinary generated CMS API as unrestricted domain access. |
| **Why chosen** | Allows replacement while preserving authority, audit and recipient safety. |
| **Consequences** | Actual account/program/legal scopes are recorded; caller idempotency does not replace permanent effect keys; remote event coverage is explicit. |
| **What remains reversible** | Provider accounts, API client libraries, outbound webhook machinery. |
| **Revisit trigger** | Contract/market changes or measured cost/isolation benefit triggers qualification of another adapter. |
| **Dependencies** | Foundation 4, 5, 13; PH-02/03; VAL-04/10; AC-L05/10, AC-S03/04. |

#### ADR-G14 — AI proposes; deterministic commands execute

| Field | Record |
|---|---|
| **Decision** | AI proposes; deterministic commands execute. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Natural-language convenience must not create an independent marketing authority or hidden targeting behavior. |
| **Chosen approach** | Typed scoped proposals, deterministic validation, exact-bound confirmation for allowed actions, drafts/advice by default, no AI permission/suppression/budget/authority override. |
| **Material alternatives considered** | Autonomous agent with direct database/provider tools; AI-selected live channels; AI-only operator UI. |
| **Why chosen** | Removes interpretation work while retaining testable truth and a complete non-AI product. |
| **Consequences** | Untrusted content remains data; model output never becomes SQL/code; failures/budget exhaustion leave approved deterministic work intact. |
| **What remains reversible** | Model/provider, prompts, task-specific evaluations and internal draft automation. |
| **Revisit trigger** | A narrow evaluated task shows useful bounded autonomy without changing the forbidden-authority set. |
| **Dependencies** | Foundation 10, 14; PH-05; VAL-09; AC-A01–A06. |

#### ADR-G15 — Small-team UX, explicit consequences and solo-safe approvals

| Field | Record |
|---|---|
| **Decision** | Small-team UX, explicit consequences and solo-safe approvals. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Enterprise role structures and exhaustive configuration would make the product unsuitable for its target operator. |
| **Chosen approach** | Five primary navigation areas, progressive disclosure, plain-language previews and receipts; one operator can perform a separate step-up review/cooling-off approval; optional second human for teams. |
| **Material alternatives considered** | Expose every control; hide all consequences in automation; mandatory two-person approval for all production use. |
| **Why chosen** | Operator simplicity and consequential control are both requirements. |
| **Consequences** | Approval binds revisions/ceilings; rare settings stay advanced; explanations derive from receipts rather than requiring AI. |
| **What remains reversible** | Navigation grouping, threshold numbers and timing targets under usability evidence. |
| **Revisit trigger** | Observed operator mistakes or task complexity require UX/policy adjustment, not weaker authority. |
| **Dependencies** | Foundation 11, 14; PH-03/05/06; VAL-06; AC-L09, AC-O05/07. |

#### ADR-G16 — Server-enforced identity, capability and environment boundaries

| Field | Record |
|---|---|
| **Decision** | Server-enforced identity, capability and environment boundaries. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | UI workspace selection, first-factor login and generic worker/admin access are insufficient protection for audience and sending data. |
| **Chosen approach** | Capability-based RBAC with scoped memberships, verified MFA assurance on protected operations, narrow API principals, worker-only transport secrets, no production routes in nonproduction and restricted incident access. |
| **Material alternatives considered** | UI-only filtering; all-powerful app API; blanket admin override; shared development/production keys. |
| **Why chosen** | Makes supported-path safety independently enforceable and testable. |
| **Consequences** | Export/consent/suppression/send approval capabilities differ; web/AI cannot directly send; privileged infrastructure is separately audited. |
| **What remains reversible** | MFA/session implementation, secret store, hosting isolation details. |
| **Revisit trigger** | External-customer tenancy or new threat evidence requires a new isolation assessment. |
| **Dependencies** | Foundation 3, 14; PH-01/02; VAL-08; AC-S01–S05, AC-O05. |

#### ADR-G17 — Publication migration as a fenced authority transfer

| Field | Record |
|---|---|
| **Decision** | Publication migration as a fenced authority transfer. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Kit accounts, opt-outs and automations may span publications; membership timestamps do not prove a recipient cursor. |
| **Chosen approach** | Migrate independently fenceable publications or the smallest connected wave; all-state staging and negative-evidence union; real source pause proof; verified progress mapping; new sending epoch; legacy opt-out capture. |
| **Material alternatives considered** | CSV import then dual-send; infer sequence position from elapsed time; rewind DB/source export on rollback. |
| **Why chosen** | Prevents overlapping authority, lost restrictions and duplicated in-flight programs. |
| **Consequences** | Pause/repair-forward is default; returning to Kit is a new proven transfer; unresolved required executions block full migration. |
| **What remains reversible** | Migration tooling, wave size when evidence allows, approved observation period. |
| **Revisit trigger** | Actual source topology/capability evidence changes the smallest safely transferable unit. |
| **Dependencies** | Foundation 6, 8, 13; PH-00/03–06; VAL-10; AC-M01–M09. |

#### ADR-G18 — Operational facts, bounded analytics and privacy-preserving history

| Field | Record |
|---|---|
| **Decision** | Operational facts, bounded analytics and privacy-preserving history. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Overlapping observations, weak open signals and indefinite personal history can produce misleading or unsafe reporting. |
| **Chosen approach** | Current domain state plus append-only evidence; distinct communication/interruption/attempt/channel metrics; explicit source coverage and attribution limits; PII-separable records and lawfully retained tombstones. |
| **Material alternatives considered** | Full event sourcing from all website behavior; provider dashboard as truth; unified engagement score; unlimited immutable PII. |
| **Why chosen** | Supports accurate explanations and recovery without becoming a CDP or inventing causality. |
| **Consequences** | PostgreSQL rollups are derived/rebuildable; opens never create permission or reliable nonengagement escalation; erasure replays after restore. |
| **What remains reversible** | Analytics storage, descriptive attribution model, reviewed retention values and observability backend. |
| **Revisit trigger** | Measured analytical load or approved privacy/jurisdiction changes justify a scoped update. |
| **Dependencies** | Foundation 5, 6, 14; Roadmap 15; PH-03/06; VAL-02; AC-D08/10, AC-A06, AC-R03. |

#### ADR-G19 — Qualified channels and bounded cross-brand reuse

| Field | Record |
|---|---|
| **Decision** | Qualified channels and bounded cross-brand reuse. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | A shared person/channel abstraction could silently become pooled consent or send-everywhere marketing. |
| **Chosen approach** | One primary outbound channel per occurrence by default; later approved choose-one/fallback/companion rules; separate channel consent and endpoint semantics; cross-brand plans consist of separately authorized brand campaigns. |
| **Material alternatives considered** | Unified channel grant; unconditional fan-out; automatic brand-event retargeting; live AI routing. |
| **Why chosen** | Extends the relationship model while preserving contextual authority and recipient attention. |
| **Consequences** | Opt-out/complaint never causes fallback; only confirmed qualified failure may enable an approved route; onsite and outbound delivery remain distinct. |
| **What remains reversible** | Which channels are enabled, specific routing preferences and optional templates. |
| **Revisit trigger** | VAL-07 proves a repeated use case; cross-brand event activation needs an explicit new authority/privacy decision. |
| **Dependencies** | Foundation 6–9, 13; PH-07–10; VAL-07; AC-C05/06, AC-X01–X15. |

#### ADR-G20 — Working brand separate from irreversible public commitment

| Field | Record |
|---|---|
| **Decision** | Working brand separate from irreversible public commitment. |
| **Status** | **AUTHORITATIVE DECISION** |
| **Context** | Texenda is the accepted working identity, but prior near-name concerns and domain/legal clearance remain unresolved. |
| **Chosen approach** | Use Texenda for internal product planning, the email-first descriptor now and a broader descriptor only when justified; descriptive repository/package identifiers remain separable. |
| **Material alternatives considered** | Restart naming before any engineering; assume public clearance from a web search. |
| **Why chosen** | Naming evidence should not reopen product semantics or block internal implementation. |
| **Consequences** | Public investment/launch waits for VAL-01; no claim of trademark or namespace availability. |
| **What remains reversible** | Master public name, descriptor, domains, parent endorsement presentation. |
| **Revisit trigger** | Formal clearance or commercialization evidence requires a brand change without changing audience semantics. |
| **Dependencies** | Foundation 2; PH-00; VAL-01. |

### 18.2 Reversible implementation defaults

#### ADR-D01 — Framework, persistence and editor implementation baseline

| Field | Record |
|---|---|
| **Decision** | Framework, persistence and editor implementation baseline. |
| **Status** | **REVERSIBLE DEFAULT** |
| **Context** | Implementation needs a coherent initial toolchain without pretending today's package versions are permanent architecture. |
| **Chosen approach** | TypeScript, Payload/Next/React, PostgreSQL and a domain Drizzle unit-of-work; React Email and editor behind a versioned codec/renderer contract. Pin a compatible tested release manifest at PH-00. |
| **Material alternatives considered** | Hand-built admin/auth; separate ORM with competing migration ownership; custom email editor. |
| **Why chosen** | Uses the established direction and delegates commodity work while isolating critical domain transitions. |
| **Consequences** | Licenses, integration transactions, codec compatibility and rendered artifacts are qualified; never assume the newest versions are compatible. |
| **What remains reversible** | Versions, adapter/editor components and UI implementation; not domain table ownership or activation semantics. |
| **Revisit trigger** | Compatibility/security/maintenance or rendering evidence warrants replacement. |
| **Dependencies** | Foundation 4, 9, 12; VAL-03; AC-L01/02, AC-R05. |

#### ADR-D02 — Resend as first qualified email transport

| Field | Record |
|---|---|
| **Decision** | Resend as first qualified email transport. |
| **Status** | **REVERSIBLE DEFAULT** |
| **Context** | An initial delivery integration is needed; source/provider rate and suppression details can change. |
| **Chosen approach** | Resend Email API transport for the pilot, behind MailProvider; use verified intended-use/account contracts, single sends first, distinct substantial-brand account scopes as qualified. SES remains deferred until benefit is demonstrated. |
| **Material alternatives considered** | SES first; provider-native broadcast/contact model; multiple live providers/failover on day one. |
| **Why chosen** | Minimizes initial integration work without outsourcing audience or scheduling truth. |
| **Consequences** | Provider may restrict more; no frozen unverified rate/domain quota; 24-hour documented idempotency is not permanent product deduplication. |
| **What remains reversible** | Provider, account topology, client library, batching after qualification. |
| **Revisit trigger** | Measured cost, reputation isolation, quotas, contract or reliability justifies SES/another provider with complete acceptance tests. |
| **Dependencies** | Foundation 12–13; VAL-04; PH-02; AC-L03–L10. |

#### ADR-D03 — Payload Jobs for coarse wake-ups

| Field | Record |
|---|---|
| **Decision** | Payload Jobs for coarse wake-ups. |
| **Status** | **REVERSIBLE DEFAULT** |
| **Context** | Delayed work needs initial scheduling, while domain state must survive queue loss/replacement. |
| **Chosen approach** | Use Payload Jobs for coarse wake-ups plus indexed domain due-state/outbox sweeps and separate safety processing; do not put the only cursor or one future job per recipient step in the queue. |
| **Material alternatives considered** | Graphile Worker/pg-boss immediately; Temporal immediately; web requests run all jobs. |
| **Why chosen** | Reuses the existing stack while retaining a clean upgrade boundary. |
| **Consequences** | Queue delivery is treated as at least once; business idempotency and reconciliation remain mandatory. |
| **What remains reversible** | JobDispatcher implementation and worker deployment. |
| **Revisit trigger** | Persistent ready latency above 30–60 seconds after tuning/scaling, job-table contention or recurring missing queue capabilities. |
| **Dependencies** | Foundation 4, 8, 12; AC-W02, AC-P05, AC-R01. |

#### ADR-D04 — Managed hosting, object storage and recoverability baseline

| Field | Record |
|---|---|
| **Decision** | Managed hosting, object storage and recoverability baseline. |
| **Status** | **REVERSIBLE DEFAULT** |
| **Context** | A small team needs managed processes/database operations but not an irreversible vendor choice. |
| **Chosen approach** | Portable containers with Render paid web/worker/PostgreSQL as the initial hosting candidate; qualified S3-compatible encrypted object storage, managed secrets, private networking and independent recovery journal. Purchase/configure the plan that meets actual targets. |
| **Material alternatives considered** | Self-managed VPS/database; serverless-only workers; another managed container/database vendor. |
| **Why chosen** | Reduces day-to-day infrastructure administration while preserving deployment portability. |
| **Consequences** | No production launch before budget, region, backups, object durability and restore evidence; journal dependency is deliberate. |
| **What remains reversible** | Hosting/storage/secret vendor, instance sizes and replica counts. |
| **Revisit trigger** | Cost, regional/privacy constraints, plan limitations or measured reliability/capacity invalidate the default. |
| **Dependencies** | Foundation 12, 14; VAL-05/08; AC-R02/03/06, AC-O04. |

#### ADR-D05 — Bounded AI provider and task budget

| Field | Record |
|---|---|
| **Decision** | Bounded AI provider and task budget. |
| **Status** | **REVERSIBLE DEFAULT** |
| **Context** | AI assistance can help operators, but selecting a model is not a governing product decision. |
| **Chosen approach** | Initial OpenAI adapter with an evaluated/pinned task model chosen at enablement; proposed USD 25 monthly and USD 1 per task caps, disabled until explicitly funded/enabled; typed outputs and all hard domain checks. |
| **Material alternatives considered** | Other hosted/local model providers; no AI initially. |
| **Why chosen** | Permits practical assistance while preserving optionality and a complete deterministic product. |
| **Consequences** | Data terms, task quality, hostile-input resilience and budget reservations are external qualification gates. |
| **What remains reversible** | Provider/model/version, prompts, task budgets and advisory features. |
| **Revisit trigger** | Quality/cost/privacy evidence supports substitution; no automatic authority expansion. |
| **Dependencies** | Foundation 10, 12; VAL-09; PH-05; AC-A01–A06. |

#### ADR-D06 — Numeric policy, approval, retention and service targets

| Field | Record |
|---|---|
| **Decision** | Numeric policy, approval, retention and service targets. |
| **Status** | **REVERSIBLE DEFAULT** |
| **Context** | Concrete defaults are needed, but publication promises, workload, legal retention and account constraints are not yet empirically established. |
| **Chosen approach** | Start with Foundation POL/APR values, shadow pressure first, explicit publication promises, pilot ceiling at most 250 consented recipients, high-review threshold 5,000, and Roadmap observation/SLO/alert defaults. Final activation depends on relevant evidence. |
| **Material alternatives considered** | No defaults; opaque optimization; universal hardcoded limits regardless of actual publication commitments. |
| **Why chosen** | Makes configuration implementable while distinguishing product policy from vendor/legal facts. |
| **Consequences** | Changes are versioned/reasoned and revalidated; no campaign can silently weaken higher policy or approvals. |
| **What remains reversible** | All listed numeric defaults within invariant/qualified legal/provider boundaries. |
| **Revisit trigger** | Measured usability, publication cadence, source data, performance or regulatory evidence requires adjustment. |
| **Dependencies** | Foundation 6, 12, 14; Roadmap 15, 17; VAL-02/04/05/06; AC-C04, AC-P01–P08, AC-M09. |

#### ADR-D07 — Testing, observability and authentication support tools

| Field | Record |
|---|---|
| **Decision** | Testing, observability and authentication support tools. |
| **Status** | **REVERSIBLE DEFAULT** |
| **Context** | Testing and operational visibility need consistent initial tools; these tools should not define authority. |
| **Chosen approach** | Vitest/fast-check, real-PostgreSQL integration tests, Playwright, Mailpit, structured logs/OpenTelemetry and a qualified SimpleWebAuthn integration. Keep specific storage/dashboard vendors substitutable. |
| **Material alternatives considered** | Equivalent maintained testing, telemetry and MFA libraries; custom auth cryptography is not preferred. |
| **Why chosen** | Delegates difficult commodity details and provides reproducible test evidence. |
| **Consequences** | MFA assurance is checked across all routes; Mailpit is isolated/maintained; telemetry excludes unnecessary PII; actual email-client tests remain required. |
| **What remains reversible** | Library/backend versions and implementation adapters. |
| **Revisit trigger** | Security, support, incompatibility or maintenance evidence justifies replacement. |
| **Dependencies** | Foundation 12, 14; VAL-03/08; AC-S02/05, AC-L01/02, AC-O02/06. |


### 18.3 Deferred changes and external qualification are not open architecture

**Decision status: DEFER UNTIL TRIGGERED** for each deferred item in Foundation sections 7/12 and its deferred register: additional channels, external-customer tenancy, broad cross-brand behavioral activation, visual freeform editor, dedicated analytical database, cache, separate workflow platform, additional services and outbound webhook infrastructure. The trigger must be met before a replacement/adoption ADR is proposed. A theoretically larger scale limit is not evidence.

**Decision status: REQUIRES EXTERNAL VALIDATION** for VAL-01–VAL-10. Their evidence/owners/blocks are defined in the Foundation validation register. Until a gate passes, its activation remains disabled, held or synthetic as specified. These gates do not authorize changing frozen consent or execution semantics to suit an account limitation.

No item retains **DECISION REQUIRED NOW** in this design release. Implementation planning starts from chosen rules and defaults. Evidence may invalidate a default or disclose a genuine incompatibility; that produces a targeted ADR and affected-test update, not an automatic reopening of all product decisions.

### 18.4 Foundation-to-execution traceability

| Foundation area | Primary ADRs | First implementation phase | Principal acceptance evidence | External gate |
|---|---|---|---|---|
| 1 Product boundary | G01 | PH-00 | Scope review, G1 versus G4/G5 release separation | VAL-06/07 when relevant |
| 2 Working name | G20 | PH-00 | Separate internal/public commitment record | VAL-01 |
| 3 Invariants | G02–G19 | PH-00/01 | AC-D/S/L/W/C/R invariant suites | VAL-08 |
| 4 Architecture/transactions | G02/03/11 | PH-01/02 | AC-W10, AC-R01–R06, architecture import/migration tests | VAL-03/05 |
| 5 Identity/domain/events | G04/05/18 | PH-01 | AC-D01–D10, AC-C06 | VAL-02 |
| 6 Permission/coordination | G05/06/07 | PH-01/03 | AC-D03–D09, AC-C01–C06, AC-L04 | VAL-02/04 |
| 7 Channels | G01/19 | PH-07–10 | AC-X01–X15 as enabled | VAL-07 |
| 8 Campaign/workflow/effects | G08/09/10 | PH-02–05 | AC-L06–L10, AC-W01–W12 | VAL-04/10 |
| 9 Content | G12, D01 | PH-02 | AC-L01/02, AC-A03, AC-X11 | VAL-03 |
| 10 AI | G14, D05 | PH-05 or later | AC-A01–A06 | VAL-09 |
| 11 UX | G15 | PH-03/05 | AC-O07, operator consequence review | VAL-06 |
| 12 Stack/hosting | G03/11, D01–D07 | PH-00/02 | AC-P01–P08, AC-R05/06, SBOM/manifest | VAL-03/05 |
| 13 Providers/APIs | G09/13 | PH-02/03 | AC-L03–L10, AC-S03/04 | VAL-04 |
| 14 Security/evidence | G05/11/16/18 | PH-01/02 | AC-S01–S05, AC-R02/03, AC-O08 | VAL-02/08 |
| 15 Analytics/operations | G18, D06/07 | PH-02/03 | Count reconciliation, AC-A06, AC-O01–O08 | VAL-02/05 |
| 16 Migration | G17 | PH-00/03–06 | AC-M01–M09, actual source stop proof | VAL-10 |
| 17 Acceptance | All applicable records | Every phase | Scoped signed evidence packet; no claimed tests without results | Applicable VAL gates |
| 18 Change control | All records | PH-00 onward | Superseding ADR + test/migration impact + paired artifact version | Depends on change |

In this compact trace table, `Gxx` expands to `ADR-Gxx` and `Dxx` to `ADR-Dxx`. Acceptance-test IDs retain their `AC-` prefix and are not ADR identifiers.

#### Invariant-to-test index

| Invariant | Minimum acceptance coverage |
|---|---|
| INV-01 | AC-D03/10, AC-W10, AC-S01/03 |
| INV-02 | AC-D01/04, AC-C06, AC-X09 |
| INV-03 | AC-D01/05, AC-X05/06/13 |
| INV-04 | AC-S03/05, AC-L09, AC-X01/02/09 |
| INV-05 | AC-D04–D06, AC-C04, AC-W06 |
| INV-06 | AC-S01–S03, AC-C05/06 |
| INV-07 | AC-W02, AC-R01/05 |
| INV-08 | AC-L01/09, AC-W05, AC-A03/04 |
| INV-09 | AC-L06/07, AC-C02, AC-X08/11 |
| INV-10 | AC-C01, AC-X12/14, AC-A05 |
| INV-11 | AC-L06/07/10, AC-R01/03 |
| INV-12 | AC-L07/08, AC-X10/12, AC-R04 |
| INV-13 | AC-D10, AC-L09, AC-A04/06 |
| INV-14 | AC-A01–A06, AC-S03/05 |
| INV-15 | AC-C01–C04, AC-W03, AC-R04 |
| INV-16 | AC-D03/04, AC-W07, AC-M03 |
| INV-17 | AC-D06, AC-L04/05, AC-R02 |
| INV-18 | AC-R01–R06, AC-M08 |
| INV-19 | AC-M01–M09 |
| INV-20 | AC-S05, AC-O06 |
| INV-21 | AC-D10, AC-R03, AC-O08 |
| INV-22 | AC-D01, AC-S01/03, AC-C06, AC-X09 |

Ranges expand within their stated `AC-` family. These are minimum mappings; one scenario may test several invariants. Each invariant must have executable evidence in the enabled product scope rather than being marked satisfied solely by a document review.

### 18.5 Cross-cutting decision-test result

| Required decision test | Closure result |
|---|---|
| **Product truth** | Email and permissioned audience operation remain the center; additional channels do not dictate the first release. |
| **Recipient trust** | Current contextual permission, explicit denials, pressure, expiry and duplicate checks remain mandatory at handoff. |
| **Small-team operation** | One operator can safely approve and operate a publication; managed infrastructure and exception-led UI reduce routine work; legal/security qualification may use outside expertise. |
| **Authority** | Domain tables/commands own active truth; drafts, queues, providers, journal, analytics and AI cannot grant audience authority. |
| **Simplicity** | One core/executor, bounded recipes, typed representations and progressive review avoid parallel overlapping systems. |
| **Recoverability** | Outbox/inbox, semantic keys, explicit uncertainty, restrictive/effect journal and disabled restore epochs make failures visible and safely reconcilable. |
| **Replaceability** | Providers, wake-ups, editor, hosting, model and reporting backends retain narrow substitution contracts. |
| **Evolution** | Endpoint/channel/purpose and communication/effect distinctions exist before expansion; actual adapters stay gated. |
| **Scope discipline** | Adjacent commercial/brand facts may be consumed without taking authority over commerce, narrative, identity design, support, ads or general agents. |

### 18.6 Immediate repository-design handoff

The first implementation planning session should produce the PH-00 WorkloadProfile and qualification manifest, initialize the repository skeleton, extract the ADR files, define scoped domain schemas/contracts, establish migration/table ownership, and create failing tests for INV-01–INV-22. Proceed with synthetic data and disabled production transports.

The first vertical correctness slice is: **workspace/publication → public request → pending subscription → explicit confirmation → scoped grant → unique approved test delivery → verified restrictive input → denied future delivery → safe replay/restore**. It precedes polished dashboards, AI, rich automation editing and additional channels.

No further broad naming, product-category or architecture-discovery exercise is required to start this work. A real incompatibility discovered during qualification is handled by a targeted decision record and impacted tests.

## Source references and evidence limits

`[S01]`–`[S24]` in this artifact refer to the full source register in [Artifact I](Texenda_Product_Technical_Foundation_v1.0.md#source-register). They identify official technical references reviewed on September 5, 2026. For migration, the especially relevant sources are Kit's subscriber listing/statuses (S09), sequence membership (S10), changelog/sequence content API (S11), and account-level unsubscribe operation (S24). Runtime safety depends on the actual qualified provider/account contract, not an unpinned web page.

All numerical service, approval, alert, budget, retention, canary and observation values are proposed **REVERSIBLE DEFAULTS** constrained by governing invariants and applicable external qualification. They are not legal requirements, vendor warranties, known current workload measurements or completed test results.

## Closure statement

**The implementation foundation is closed; production permission is not presumed.** Artifact I defines the authoritative product/domain/execution boundary. This artifact defines how to implement, migrate, test and operate it without inventing a second authority model. Remaining matters are specific external evidence gates or measurable future triggers. Repository architecture and implementation planning may begin now from these two coordinated specifications.
