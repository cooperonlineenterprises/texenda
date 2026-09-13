# Production acceptance criteria

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal roadmap v1.0; interaction additions explicitly below. Apply [package authority](../DECISION-STATUS.md).

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

## Interaction acceptance extension

| AC-I01 | Run every interaction adapter against identical synthetic inputs. | Same authorized command contract and domain result; no AI-only policy path. |
| AC-I02 | Edit a campaign visually then submit an older conversational patch. | Stale base revision rejected; unsaved local edits explicitly reconciled, never silently overwritten. |
| AC-I03 | Switch brands then use that campaign in conversation. | Old referent invalidated; scope re-resolved before any consequential mutation. |
| AC-I04 | Create goal conversationally and resume another session. | Goal and linked drafts are durable and inspectable without reconstructing transcript. |
| AC-I05 | Mark goal achieved manually. | No purchase/completion business event or send cancellation is invented. |
| AC-I06 | Import document demanding persistent instructions or export. | Data does not change system instructions, authority, grants or available tools. |
| AC-I07 | Request a material change through voice, chat and API. | Typed immutable proposal, exact diff and consequence envelope precede activation. |
| AC-I08 | Approve then modify content, audience, channel, sender or cost ceiling. | Relevant approval stale; fresh review required, stricter live policy still applies. |
| AC-I09 | Send repeated retries for a command after response loss. | Same semantic outcome returned; no duplicate product mutation or external effect. |
| AC-I10 | Let an agent control visible approval button. | Delegated agent principal cannot satisfy independent human C3/C4 approval. |
| AC-I11 | Revoke/expire delegation between proposal and commit. | Commit denied under current grant; pending effect governed by current live authority. |
| AC-I12 | Present token issued to another resource/workspace. | Token audience/resource/scope rejected; no cross-brand enumeration. |
| AC-I13 | Attempt tool discovery as restricted external agent. | Only authorized capability metadata and readable objects exposed; no credential leakage. |
| AC-I14 | Exhaust agent spend/rate/time limits. | Deterministic stop and audit; no self-expansion or fallback to human credentials. |
| AC-I15 | Stop computer-use session after it becomes lost. | Run stops with attributable checkpoint; no speculative retry clicking or permission expansion. |
| AC-I16 | Compare normal and Inspect views for restricted principal. | Inspect provides precision only, never expanded PII or command authority. |
| AC-I17 | Navigate core tasks with keyboard, screen reader and zoom. | WCAG2.2AA applicable criteria checked by automated plus manual testing; focus/labels/status meaningful. |
| AC-I18 | Disable AI/model services entirely. | Manual audience/campaign/automation management and approved deterministic executions continue. |
| AC-I19 | Interrupt streaming response then refresh object. | Uncommitted assistant text is not state; authoritative revision and proposals recover correctly. |
| AC-I20 | Use speech containing background yes, negation, similar names and dates. | No ambiguous/provisional speech causes C3/C4 approval; material entities reviewed. |
| AC-I21 | End voice session or revoke microphone permission. | Capture stops visibly; no default background listening or raw audio retention. |
| AC-I22 | Fail speech recognition or synthesis provider. | Typing/direct UI works; TTS failure does not lose authoritative work. |
| AC-I23 | Use assistive voice control to activate explicit approval. | Accessible authenticated approval works without making conversational filler an approval token. |
| AC-I24 | Inspect model/transcript logs under restrictive retention. | PII minimization, provider retention review, transcript erasure and durable action evidence separated. |
| AC-I25 | Ask why recipient was deferred and what AI changed. | Explanation cites recorded predicate/revision/actor outcomes; unavailable evidence stated, no motives invented. |
| AC-I26 | Flood routine successful events. | Proactive attention quiet/deduplicated; only meaningful thresholds create notices; notices grant no authority. |
| AC-I27 | Submit invalid or malicious structured AI output. | Closed schema/authorization validation denies before product mutation; bounded repair then manual fallback. |
| AC-I28 | Mix several dependent commands in one plan with partial failure. | Each effect state explicit; plan not falsely atomic across providers; no unsafe rollback or double commit. |
| AC-I29 | Run public tools/API across supported version matrix. | Protocol adapter is thin, result schemas/errors/capabilities versioned; no mandatory MCP/WebMCP for core. |
| AC-I30 | Complete common workflows with target small-team operators. | At least 90% defined routine tasks without advanced controls; consequence comprehension separately evaluated. |

All added tests are **NOT RUN**. The [machine acceptance catalog](acceptance-catalog.json) links each test to work packages and requirements. Profile applicability never waives an invariant for an enabled capability.
