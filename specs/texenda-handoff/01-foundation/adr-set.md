# Decision record / ADR set

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal roadmap v1.0; interaction additions explicitly below. Apply [package authority](../DECISION-STATUS.md).

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

#### ADR-G21 — One command model for all interaction surfaces

**Decision:** One command model for all interaction surfaces

**Status:** AUTHORITATIVE DECISION

**Context:** Later human-agent inquiry broadens interaction, not product authority.

**Chosen approach:** All visual, keyboard, conversational, voice, tool/API and computer-use actions use the same authenticated queries/commands; metadata drives tools and Inspect.

**Material alternatives:** Separate AI/voice business logic or a second agent app.

**Why chosen:** One policy and state contract prevents divergence and preserves manual fallback.

**Consequences:** Command schemas and ActorContext must precede writable assistants; direct ORM/provider access stays forbidden.

**What remains reversible:** Protocol adapters, metadata presentation and client rendering.

**Revisit trigger:** A demonstrated incompatible interaction requirement; never convenience alone.

**Dependencies:** ADR-G02, ADR-G14, ADR-G16

#### ADR-G22 — Durable objects, explicit goals and scoped memory

**Decision:** Durable objects, explicit goals and scoped memory

**Status:** AUTHORITATIVE DECISION

**Context:** Conversation is useful for intent but unsafe as an authoritative state log.

**Chosen approach:** Goal, InteractionSession, ProposalRevision and explicit assistant preferences; typed constraints promote into their existing owner. Goal achievement is not business-event evidence.

**Material alternatives:** Chat-only state; general persistent inferred memory; project-management subsystem.

**Why chosen:** Supports resumption without hidden state or inferred permission.

**Consequences:** Every consequential proposal references durable objects/revisions; workspace changes clear referents.

**What remains reversible:** Transcript summarizer/provider; retention under reviewed policy.

**Revisit trigger:** Repeated product work requires richer planning; evidence needed before new objects.

**Dependencies:** ADR-G01, ADR-G21

#### ADR-G23 — Exact proposal review and approval across modes

**Decision:** Exact proposal review and approval across modes

**Status:** AUTHORITATIVE DECISION

**Context:** Voice and agents increase ambiguity and stale-state risk.

**Chosen approach:** C0…C4 consequence classes; ProposalRevision and ApprovalRequest/Approval; immutable digest, base revisions and reviewed envelope; accessible human-only protected approval for consequential agent proposals.

**Material alternatives:** Free-form yes or standing broad chat approval; agent self-approval; separate UI authority.

**Why chosen:** Prevents misunderstood speech or browser actuation from becoming authority.

**Consequences:** Approval infra before AI writes; current stricter policy remains live; external effects not universally undoable.

**What remains reversible:** Review layout, nonbinding copy and threshold defaults per existing policy.

**Revisit trigger:** Measured usability failure with an equally safe alternative.

**Dependencies:** ADR-G08, ADR-G15, ADR-G21

#### ADR-G24 — Attributable external agents and least-privilege tools

**Decision:** Attributable external agents and least-privilege tools

**Status:** AUTHORITATIVE DECISION

**Context:** External tools and browser agents cannot be trusted extensions of human credentials.

**Chosen approach:** AgentPrincipal + DelegationGrant + AgentRun; short-lived resource/scoped credentials, current revocation checks, explicit budget and action attribution; structured tools first.

**Material alternatives:** Share owner session; trust visible button; model-controlled provider/SQL access.

**Why chosen:** Supports interoperability without authority escalation.

**Consequences:** Dedicated auth qualification and negative tests before external writes; unknown browser automation cannot claim agent attribution.

**What remains reversible:** OAuth/token mechanism and MCP adapter after validation.

**Revisit trigger:** New standard or runtime creates a verified equivalent boundary.

**Dependencies:** ADR-G16, ADR-G21, ADR-G23

#### ADR-G25 — Voice-forward and accessible shared UI

**Decision:** Voice-forward and accessible shared UI

**Status:** AUTHORITATIVE DECISION

**Context:** Small teams benefit from voice but dense review and safety require visual/structured inspection.

**Chosen approach:** Semantic human UI plus Inspect for experts/agents; PTT default, committed transcript, visual handoff; no conversational C3/C4 approval; manual and assistive modes fully supported.

**Material alternatives:** Voice-only/chat-first; always-on mic; separate privileged agent GUI.

**Why chosen:** Maintains usability, accessibility and legibility without duplicated product state.

**Consequences:** Core navigation and review ship without AI; raw audio unretained by default; vendor retention needs validation.

**What remains reversible:** Speech provider, WebRTC implementation, prominence and interaction polish.

**Revisit trigger:** Measured user/accessibility evidence supports different default without weakening authority.

**Dependencies:** ADR-G15, ADR-G21, ADR-G23

#### ADR-G26 — File-native development orchestration separate from product agents

**Decision:** File-native development orchestration separate from product agents

**Status:** AUTHORITATIVE DECISION

**Context:** An Astra implementation lead needs bounded parallel work, model routing and receipts, not another product runtime.

**Chosen approach:** Small local harness with task DAG, leases, context manifests, review/integration receipts and resumable state; no embedded model runner, deployment authority or production keys.

**Material alternatives:** A general agent framework or reuse of product AutomationExecution for engineering tasks.

**Why chosen:** Minimizes ceremony and avoids mixing developer authority with recipient-facing semantics.

**Consequences:** Filesystem coordination is not a sandbox or authenticated signature system; external runtime/Git protections enforce access.

**What remains reversible:** Agent runtime/bridge and model choices through explicit qualification.

**Revisit trigger:** Measured need for remote multi-host scheduling; migrate state with governance retained.

**Dependencies:** ADR-G01, ADR-G16, ADR-G21

#### ADR-D08 — Interaction transports and protocol adapters

**Decision:** Interaction transports and protocol adapters

**Status:** REVERSIBLE DEFAULT

**Context:** Streaming UI and optional voice/agent integrations add transport needs but not a distributed architecture requirement.

**Chosen approach:** HTTP/SSE first, optional browser WebRTC voice; thin API/MCP adapters; WebMCP deferred to support/qualification; no vector store or realtime bus by default.

**Material alternatives:** Persistent generic websocket platform, standalone agent framework, mandatory browser experimental tools.

**Why chosen:** Uses existing web/worker/database roles and provides graceful degradation.

**Consequences:** Transport interruption cannot commit partial assistant output; clients re-read current object state.

**What remains reversible:** All listed transports and model/speech providers.

**Revisit trigger:** Latency, support matrix or operational load proves an alternative materially better.

**Dependencies:** ADR-G03, ADR-G21, ADR-G25

#### ADR-D09 — Current-runtime-aware task/model routing

**Decision:** Current-runtime-aware task/model routing

**Status:** REVERSIBLE DEFAULT

**Context:** Public Codex roster is not evidence of availability in the target signed-in client.

**Chosen approach:** Three operational tiers; candidate names recorded separately; actual model/effort/tool/cost/data scope qualified in target runtime before dispatch; downshift after contracts, independent stronger review for consequential changes.

**Material alternatives:** Static role-to-model mapping; unverified names; strongest model for every edit.

**Why chosen:** Balances consequence, uncertainty, verification and cost without inventing model access.

**Consequences:** No active model bindings shipped; first bootstrap probes and validates actual capabilities.

**What remains reversible:** Exact model IDs, efforts and execution bridge.

**Revisit trigger:** Client/account/model change, retirement, qualification expiry or observed quality/cost drift.

**Dependencies:** ADR-G26
