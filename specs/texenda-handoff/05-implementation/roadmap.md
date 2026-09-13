# Dependency-ordered implementation and migration roadmap

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal roadmap v1.0; interaction additions explicitly below. Apply [package authority](../DECISION-STATUS.md).

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

### 16.3 Kit migration authority

The sole operational migration specification is [Kit migration](../06-migration-and-production/kit-migration.md). It preserves the original §16.3 protocol and authority matrix.

### 16.4 Advancement governance

Each phase closes with a scope/evidence review, not a calendar date. The Product Owner may defer features, but cannot waive permission, isolation, duplicate-effect, safety-journal, or authority-transfer failures. Performance targets can be revised transparently against actual workload; unsafe semantics cannot be relaxed to make a launch milestone pass.

A publication may use Texenda broadcasts before unrelated future features exist. It may not be declared **fully migrated** while its required source sequences, opt-outs, or integrations remain ambiguous.

---

## Handoff 1.1 dependency refinement

**Status: AUTHORITATIVE DECISION.** The package graph in [work-packages.json](work-packages.json) is the executable planning order. The earlier PH-00…PH-10 product phases remain; interaction tracks IX-01…IX-06 add capabilities without making AI a prerequisite for the first publication.

| Track | WPs | Independently useful value | Dependencies, burden and advancement |
|---|---|---|---|
| Repository/contracts | 00–04 | Run and test a protected modular monolith | Qualify target runtime; resolve per-command closed schemas; one migration owner. No production account needed. |
| Consent/email slice | 05–12 | Subscribe → confirm → safe test delivery → withdraw → deny → replay/restore | Journal and atomic coordinator precede live mail. Synthetic/fake providers until sender gates pass. |
| First real publication | 13–20,39–41 | Forms, audience, content, reviewed broadcasts and reporting replace useful Kit core | Sender, security, workload/restore and migration proofs; sole live authority; owner-controlled canary and observation. |
| Durable relationships | 21–23 | Sequences and event-driven automations | One executor, verified waits/outcomes, versioned definitions. No AI requirement. |
| Portfolio | 24,33 | Shared administration, contextual preferences, safe per-unit migration | Basic pressure already exists; add fairness and operator views. No pooled permission. |
| Human UX and review | 25,15 | Object-first search, Inspect, attention and exact consequence review | Manual tasks work; approval/proposals precede writable AI. Accessibility is not delayed until voice. |
| Durable intent and text AI | 26–27 | Resumable goals and bounded drafting/configuration | Explicit context, factual evidence and budget; AI cannot grant authority. Qualify before production data use. |
| External agents | 28–29,31 | Scoped tools and computer-use compatibility | Distinct principal/grant, independent human approval, negative security/eval tests. No new general agent platform. |
| Voice | 30 | PTT goals/questions/corrections with visual handoff | Built on same textual commands; audio/transcript privacy gate; no voice approval shortcut. |
| Interaction qualification | 32 | Measured safe multimodal use | All relevant AI/voice/agent/accessibility gates. Can release narrower text-only profile before optional voice. |
| Onsite/push | 34–37 | Less redundant signup prompts and requested alerts | Independent channel value/reliability before coordinated routing; small-team operating budget remains binding. |
| Conditional channels/optimization | 38,43 | Only measured, justified incremental capability | No automatic scope commitment. Fresh provider/legal/workload qualification; new bounded WP required after study. |
| Mature release | 42 | Proven email/portfolio plus declared qualified interaction profile | Actual must-pass evidence, no claimed unavailable channel, accountable owner. Optional channels are not completion prerequisites. |

**Parallelism:** identity/contracts/auth/content/provider work may proceed in separate worktrees once their dependencies and edit leases permit. Schema migrations, generated contracts, lockfiles, shared UI primitives and integration root have one writer per integration window. Downstream agents implement against frozen interfaces and synthetic fixtures, not another agent's unreviewed branch. Astra MUST serialize integration, rerun affected tests at the integrated head, and revalidate receipts after any conflict resolution.

**Milestone distinction:** `email-pilot` excludes AI and optional channels; `mature-email` requires sequences/automations, portfolio operations and human UX; `assisted-workspace`, `external-agent`, `voice`, `onsite`, `push`, and `cross-channel` are separately gated capability profiles. Packaging these plans does not claim any profile is implemented or qualified.

### Selected-profile release clarification

WP-42 releases an explicitly selected profile set. It does not require WP-32/voice/AI merely to release mature email. The additional profile dependencies are recorded in WP-42 and [release-profiles.json](../06-migration-and-production/release-profiles.json). A full interaction-suite claim does require WP-32 and its prerequisites. No optional capability may be claimed through the base release gate.
