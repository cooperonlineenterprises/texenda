# Synthetic case preparation

Status for **every product test and observation below: NOT EXECUTED**.
These are documentation-local scenarios, not executable fixtures, a second
acceptance catalog, passed acceptance, or WP completion. `PREP-CASE-*` identifiers
only let the [journeys](journeys.md) and [WP-01 draft assignment](wp01-assignment.md)
refer to a case. Requirements remain in the linked owners and existing AC IDs.

Bound source revision: `79db6081dd929af3f46a1cc8e1eec5f8ac09e9cc`;
preparation base: `efaa8fa9772d332dd3bfb2b40bbae2110b06a5fa`.
After any governing-source change, invalidate affected mappings, regenerate and
recheck before reuse. Preserve prior evidence. No account, model, provider,
browser product session or private input belonging to the product was exercised
to prepare these cases; the development author/reviewer route is separate.

## Reuse and evidence rules

The sealed [synthetic-domain-fixtures.json](../../../specs/texenda-handoff/10-validation/synthetic-domain-fixtures.json)
is test design, not implementation. Reuse FX-01–12 unchanged: OHW/HP scope;
withdrawal before permit; narrow reconsent with safety hold; two workers/one slot;
lost acceptance response; stale purchase coverage; wait race; restore after
restriction; agent cannot approve; revision 17/18 conflict; Kit entry time with no
cursor; forwarded OHW unsubscribe link. Newly composed scenarios below supply
missing journey coverage without pretending to be new sealed fixture IDs.

New example data is invented: `reader.one@example.invalid`,
`reader.two@example.invalid`, `editor@example.invalid`, `agent@example.invalid`,
`ohw.example.invalid` and `hp.example.invalid`. These non-deliverable names do
not prove isolation; future synthetic runtime tests must deny real transport and
credentials. Use captured fake effects, not real mail. `newsletter-A`, `page-A`,
`resource-A`, `proposal-A`, `run-A` are local explanatory labels for opaque IDs.
Fixture grants are deliberately scoped examples, not a new universal policy.

<a id="shared-seeds"></a>
### Shared invented seeds

The following fixed values are test-only proposals, **NOT EXECUTED**: not
production schemas/records, policy defaults, thresholds, real facts or approved
disclosure wording. Each case runs in an isolated variant; later withdrawal,
safety-hold and failure inputs explicitly modify its own starting fixture.

| Seed | Concrete example and use |
|---|---|
| Linked newsletter draft | OHW Campaign `newsletter-A` revision 17, titled “Friday kitchen notes,” references Communication `brief-A` revision 4 and email representation `email-A` revision 9. These are separate revision bindings for cases 0002/0003, not one replacement aggregate. |
| Concurrent proposal | `proposal-A` revision 2 binds Campaign 17, Communication 4 and representation 9. The human's timing edit creates Campaign revision 18 while the content bindings stay 4/9; the old proposal is stale. |
| Approved fact / wrong output | Fixture source `fact-A` revision 1 says “The planning session is October 2, 2026.” Contrasting fake-model output says “The planning session is October 9, 2026.” The operator corrects or rejects that date in cases 0002/0005; neither date describes a real event. |
| Ambiguous draft names | Alongside “Friday kitchen notes,” OHW Campaign `newsletter-B` revision 2 is titled “Friday recipe notes.” “Send the Friday notes” does not select an exact object or approved schedule. |
| Resource | `resource-A` revision 3 is the approved synthetic “Three kitchen-planning prompts” text resource, available in fake storage. A case variant makes that resource unavailable; its old approval cannot fabricate available bytes or justify unrelated content. |
| Page / choices | `page-A` revision 2 at `ohw.example.invalid` pins test disclosure `disclosure-A` revision 1: “Email me the three kitchen-planning prompts.” A separate, initially unchecked choice says “Also subscribe me to OHW Weekly: one email each week; unsubscribe any time.” The resource-request purpose and recurring Publication promise remain distinct. |
| Request-only recipient | `reader.one@example.invalid` has verified request `request-A` for resource revision 3 and no OHW or HP marketing grant. Resource fulfillment is evaluated under that particular request; it cannot create the separate subscription. |
| Marketing-authorized recipient | `reader.two@example.invalid` explicitly selected the separate recurring opt-in and confirmed OHW Weekly/email permission bound to test disclosure revision 1, with no HP grant or starting safety hold. This supplies the FX-01 scope variant; cases can later add an explicit withdrawal or independent safety hold. |

Source keys used below:

- [ADR-0008](../../decisions/ADR-0008-integrated-initial-product-and-effective-plan.md)
  owns AC-IP additions and amended WP fields; [sealed acceptance](../../../specs/texenda-handoff/06-migration-and-production/acceptance-catalog.json)
  owns the referenced original criteria.
- [Interaction](../../../specs/texenda-handoff/02-product-and-ux/interaction-architecture.md),
  [UX](../../../specs/texenda-handoff/02-product-and-ux/operator-workflows.md),
  [Domain](../../../specs/texenda-handoff/03-domain-and-architecture/canonical-domain.md),
  [Permission](../../../specs/texenda-handoff/03-domain-and-architecture/permission-and-coordination.md),
  [Execution](../../../specs/texenda-handoff/03-domain-and-architecture/execution-semantics.md),
  [Content](../../../specs/texenda-handoff/03-domain-and-architecture/content.md),
  [Commands](../../../specs/texenda-handoff/03-domain-and-architecture/command-catalog.json),
  [AI authority](../../../specs/texenda-handoff/04-security-governance-and-operations/ai-and-agent-authority.md),
  and [Security](../../../specs/texenda-handoff/04-security-governance-and-operations/security-and-privacy.md)
  retain their topic boundaries.

For each future automated exercise, preserve revision/configuration, fixture
version, actor/grant, input, command and resulting object/revision/receipt,
expected-versus-observed result, effect count and actual command/exit/log.
Assertions must inspect durable state and denied effects; clicks, canned text or
a model narrative are insufficient. WP-01 can establish contract examples and
oracles; later owners must exercise real handlers and persistent worker state.

<a id="prep-case-0001"></a>
## PREP-CASE-0001 — orientation and wrong-brand denial

**NOT EXECUTED.** Journeys [J1](journeys.md#j1), [J2](journeys.md#j2).
Requirements: UX §11; Domain §5.2; Permission §6.1/6.5; Interaction Context
continuity; AC-IP04/09/10/15, AC-D01, AC-S01, AC-I03/04/12.
Owners: WP-01 contract cases; WP-03/13/24/25/26/31/40 implementation/evaluation.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Reuse FX-01: one verified endpoint, OHW/HP profiles, grant only OHW/email. Separately give the operator OHW-only access; retain an old HP object reference in a prior session fixture. |
| Actor / action | New operator authenticates through operator access, opens S1 and searches. Returning operator reopens saved OHW work, switches allowed scope, then follows the stale HP reference. An actor authorized for both brands separately previews the FX-01 HP recipient. |
| Visible / persistent result | Correct actor/brand and saved OHW revision appear. Unauthorized HP reads expose no names/counts/PII. Authorized HP preview excludes the recipient for missing HP permission. No HP grant/delivery is created. Scope-sensitive referents are cleared. |
| Denial / recovery | Server rejects wrong-scope URL, relationship and token independently of UI filtering. Cancel switch keeps authorized work. Reauthenticate/refetch after revocation; no fallback to broader credentials. |
| Verification / limit | Future scoped-query/relationship tests plus semantic navigation compare response, store and zero effects. Proves these fixture boundaries only; actual new/returning comprehension requires case 0011 and VAL-06. |

<a id="prep-case-0002"></a>
## PREP-CASE-0002 — one newsletter through creation, correction and review

**NOT EXECUTED.** Journeys [J2](journeys.md#j2), [J5](journeys.md#j5).
Requirements: Content §9 + [ADR-0005](../../decisions/ADR-0005-react-email-editor-reversible-default.md);
Commands draft/preview/publication/approval/scheduling rows; Interaction Shared
pipeline/Approval; AC-IP04/06/14, AC-I01/04/07/18/19, AC-A03/04/06.
Owners: WP-01/10/13/14/15/26/27/29; WP-25/31 observation.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | OHW editor has C1 draft and relevant C2 configuration capability; human approver has bounded approval capability. Use the [shared newsletter and fact seeds](#shared-seeds), with no Offer/commerce object. Fake AI substitutes October 9 for the source's October 2. |
| Actor / action | Run two creation variants: direct controls, and contextual fake AI through the same draft commands. In each, keep one resulting newsletter, alternate manual/assisted edits, reject/correct the date, save, preview, test/preflight and request human review. |
| Visible / persistent result | One campaign with linked communication/representation revisions, sources, diff and attributed commands survives handoff. Draft save/accepting copy is not C3 approval. Human approval binds the exact immutable content, audience/timing and ceilings; explicit authorized scheduling is a separate result. |
| Denial / recovery | Draft-only actor cannot approve/publish/schedule. Cancel suggestion/review retains saved work. Changed bound content invalidates approval. With AI disabled, repeat the complete manual path; deterministic approved work remains operable. |
| Verification / limit | Future handler/contract tests compare both routes' object references and authority checks, serialized content/HTML/plain-text bindings and receipts. No duplicate draft truth or effect. Fake AI proves integration, not model accuracy, editing quality or operator effort. |

<a id="prep-case-0003"></a>
## PREP-CASE-0003 — concurrent edits, stale approval and resumption

**NOT EXECUTED.** Journeys [J2](journeys.md#j2), [J5](journeys.md#j5).
Requirements: Interaction Context continuity/Failures; Execution §8.2;
AC-IP04/07, AC-I02/03/08/19/27. Owners: WP-01/13/15/26/27.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Reuse FX-10 and the [shared proposal bindings](#shared-seeds): proposal references Campaign 17; human saves Campaign 18 while Communication 4/representation 9 stay separately bound. Also retain an unsaved local patch and a prior approval envelope. |
| Actor / action | Assistant attempts the old patch while the human edits. Interrupt the response stream, change workspace, reconnect and reopen the object through its stable reference. |
| Visible / persistent result | Stale result and both intended edits remain inspectable; revision 18 is not overwritten. Unsaved patch is explicitly saved, reconciled or cancelled. Provisional text does not mutate state. Old scope referents/approval cannot carry across changed scope or meaning. |
| Denial / recovery | Deny stale expected revision/digest. Human chooses merge into a new draft or discard; re-preview/reapprove if consequential. Cancel proposal preserves existing authoritative content. |
| Verification / limit | Future ordered/concurrent handler tests assert stored revision/digest, absence of stale writes and correct refetch after stream loss. This proves deterministic conflict handling, not that an actual agent notices the conflict without VAL-11 evaluation. |

<a id="prep-case-0004"></a>
## PREP-CASE-0004 — constrained agents, revocation and human-only approval

**NOT EXECUTED.** Journeys [J2](journeys.md#j2), [J5](journeys.md#j5).
Requirements: AI authority extension; Security §14/interaction threats; Commands
ApproveProposal/CommitProposal/ScheduleCampaign and human-only C4 rows;
AC-IP08/09, AC-A02/04, AC-I10/11/12/13/14/15/16/29.
Owners: WP-15/28/29/31/40.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Reuse FX-09 with separate human and external-agent sessions. Grant one fixture agent OHW read/draft only. A second fixture has an explicit current grant for one exact human-approved C3 envelope. |
| Actor / action | Agent drafts, attempts another brand and human-only approval, then encounters grant revocation/expiry and rate/time/spend exhaustion. Separately execute the exact already-approved allowed envelope, then vary its digest/ceiling. |
| Visible / persistent result | Reads/drafts and permitted exact execution are attributable to initiator/intermediary/authorizer/executor with object/result receipts. No agent approval, new permission or broad human session appears. The valid C3 example is not globally forbidden by the draft-only fixture. |
| Denial / recovery | Reject wrong scope, revoked grant, insufficient assurance and altered envelope before access/mutation. Stop lost sessions/runs; no human-cookie or provider-token fallback. In-flight effects reconcile under current domain rules. Human reviews in an independent context; new authority requires proper explicit authorization. |
| Verification / limit | Future server authorization and browser-isolation tests inspect denied access/effect logs plus the permitted exact result. Tests of token boundaries do not qualify real OAuth/client/model behavior or prove actual human identity; VAL-08/11 remains separate. |

<a id="prep-case-0005"></a>
## PREP-CASE-0005 — incorrect, ambiguous, unavailable and manipulated AI

**NOT EXECUTED.** Journeys [J2](journeys.md#j2), [J4](journeys.md#j4), [J5](journeys.md#j5).
Requirements: AI authority §10; Interaction Context/Failures; Commands validation;
AC-IP07/08/14, AC-A01/02/05/06, AC-I06/18/27.
Owners: WP-15/26/27/29/40.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Same saved newsletter and [shared fact/ambiguous-name seeds](#shared-seeds). Fake AI variants: false protected date; “send the Friday notes” with two plausible targets; unsupported schema/operator; unavailable response; untrusted text saying to disclose another brand or ignore approval. |
| Actor / action | Operator requests bounded drafting/explanation; adapter feeds each response through normal authorized context, typed validation and consequence preview. Operator corrects a fact, clarifies target/time or cancels and resumes manually. |
| Visible / persistent result | Known inputs, assumptions and unresolved critical choices are separate. Invalid/manipulated output makes no mutation, grant, credential retrieval, provider call or hidden policy. Valid corrected draft is saved as a revision with provenance. Outage leaves full manual work and approved deterministic execution intact. |
| Denial / recovery | Bound correction attempts; exhausted limit surfaces error/manual path without model/budget/authority expansion. Ambiguity pauses consequential work. Stream cancellation cannot convert unfinished text to a command. |
| Verification / limit | Future scripted adapter/validation tests assert authorized retrieval precedes the model and no rejected-input effects occur. Later adversarial real-model evaluation must measure actual injection/quality/failure behavior under VAL-09; fixture rejection is not prompt-injection immunity. |

<a id="prep-case-0006"></a>
## PREP-CASE-0006 — native page lifecycle and access boundaries

**NOT EXECUTED.** Journey [J3](journeys.md#j3).
Requirements: ADR-0008 ownership and WP-10/12; Security §14.1/14.4;
AC-IP02/15, AC-S01/02/03/04. Owners: WP-01 contracts; WP-03/10/12/15/40.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Use the [shared page/disclosure/resource seeds](#shared-seeds), with OHW Property/publication references, fixed signup/thank-you blocks and synthetic local origin; authorized operator and separate recipient capability. |
| Actor / action | Author/preview, human-review and simulate publication; edit a new revision, remove an asset, fail publication, then unpublish through the approved path. Try script/unsafe URL, cross-brand reference and public operator provisioning. |
| Visible / persistent result | Page lifecycle/version and current last-good publication are explicit. Brand/purpose/disclosure/resource are pinned. Failed new revision never partially replaces the good page. Native standalone page remains supported, independent of optional embedding. |
| Denial / recovery | Invalid or removed resource holds/invalidate affected stale/unpublished revision. Unsafe content and unauthorized effects deny. Correct/review a new revision or cancel it; unpublishing preserves prior evidence and reports actual state. Recipient signup cannot establish operator membership. |
| Verification / limit | Future lifecycle/atomicity and renderer/security tests inspect page references and fake-origin state, plus keyboard semantics. Proves synthetic lifecycle only; real publication/DNS/privacy/branding/accessibility evidence and approvals remain required. |

<a id="prep-case-0007"></a>
## PREP-CASE-0007 — confirmation and resource fulfillment without extra consent

**NOT EXECUTED.** Journeys [J3](journeys.md#j3), [J4](journeys.md#j4), [J5](journeys.md#j5).
Requirements: Permission §6.1–6.6; Execution §8.3–8.6; ADR-0008 WP-12;
AC-IP03, AC-D03, AC-L06/07. Owners: WP-05/10/11/12.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Use the [shared request-only and marketing-authorized seeds](#shared-seeds), keeping the resource request and explicitly chosen OHW signup distinct. Reuse FX-02/03 for later withdrawal and independent safety hold; use fake storage/mail with success, definite failure and unknown acceptance. |
| Actor / action | Recipient submits, confirms where required, repeats same request key/confirmation, expires a link, requests a missing asset and exceeds a bounded abuse limit. Operator observes fulfillment and tries a safe reconciliation after failure. |
| Visible / persistent result | Request/pending/confirmed/resource and per-effect outcomes are truthful/non-enumerating. Same-key replay yields one outcome; valid confirmation creates only its scoped grant and no duplicate welcome. Resource-only access creates no unrelated marketing grant. |
| Denial / recovery | Stale confirmation after withdrawal cannot revive authority; narrow reconsent does not clear safety Suppression. Missing/changed asset holds. Expired-link recovery uses the approved verified-request path. Known safe retries retain identity; unknown acceptance retains claim and reconciles without new payload/key or provider/channel. |
| Verification / limit | Future handler and worker failure tests inspect request, disclosure, grants, effect keys, fake call count and current denial. Proves synthetic policy/dedup/recovery, not real inbox delivery, legal consent wording or provider idempotency. |

<a id="prep-case-0008"></a>
## PREP-CASE-0008 — welcome/nurture, hygiene and truthful unavailable sources

**NOT EXECUTED.** Journeys [J1](journeys.md#j1), [J4](journeys.md#j4).
Requirements: Domain §5.7; Execution §8.7–8.8; ADR-0008 WP-14/16/22/23;
AC-IP06/10/13/14, AC-D07/08, AC-W01/02/03/05/08/09, AC-A06, AC-I25/26.
Owners: WP-06/14/16/21/22/23/27.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Confirmed OHW profile; welcome/nurture with approved content, finite waits/expiry/reentry rules; no Offer. Reuse FX-06 stale purchase coverage and FX-07 event-before-wait race. Include noisy opens and missing revenue/event feeds. |
| Actor / action | Human configures/simulates/reviews through ordinary controls with AI off; worker enrolls once, restarts and races wait/timeout. Operator edits prospectively and reviews a re-engagement/sunset proposal with explanations. |
| Visible / persistent result | One authoritative cursor and semantic occurrence; accepted send anchors wait, one wait branch wins, old runs remain pinned. Metrics cite denominator/window/coverage. Missing purchase/revenue sources show UNKNOWN/unavailable, never zero, a nonpurchase assertion, causal lift or forced experiment winner. |
| Denial / recovery | Duplicate confirmation/historical import does not restart welcome. Stale required coverage holds affected condition. No automatic erase/repermission, nonopen-only sunset or blanket resend. Cancel stops pending actions; restart respects spacing/expiry and current denials. |
| Verification / limit | Future executor concurrency/restart tests compare cursor/step/effect identities and source-health oracle; reporting tests inspect source labels and counts. Does not prove actual engagement quality or operator burden; case 0011 and later source qualification remain required. |

<a id="prep-case-0009"></a>
## PREP-CASE-0009 — fresh draft cloning

**NOT EXECUTED.** Journeys [J2](journeys.md#j2), [J4](journeys.md#j4).
Requirements: ADR-0008 WP-10/14/22 and AC-IP05; Content §9;
Execution §8.7; AC-W05, AC-A03. Owners: WP-01 contracts; WP-10/14/22.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Source campaign previously approved/sent and recipe with active/completed executions, recipients, schedule and effect history. Human may read source and draft in the explicitly authorized target brand. |
| Actor / action | Clone content/structure, adjust dates/brand/protected facts and inspect resulting draft and unchanged source. Cancel edits; later request fresh review. |
| Visible / persistent result | New draft identities only. No inherited approval, recipient snapshot, current schedule/activation, enrollment, cursor/progress or delivery/effect history. Reuse source references/provenance only where appropriate; these cannot act as live authority. |
| Denial / recovery | Unreadable source/unauthorized target denied without leak. Stale protected facts block approval; explicit target-brand adoption never transfers audience. Cancelling the clone leaves source records intact; new effects require fresh review. |
| Verification / limit | Future clone contract/handler tests compare source and result field-by-field, including forbidden inherited records and zero effects. Proves isolation of the specified clone, not copy quality or that real recipients would welcome repetition. |

<a id="prep-case-0010"></a>
## PREP-CASE-0010 — cancellation, unknown outcome and recovery

**NOT EXECUTED.** Journeys [J2](journeys.md#j2), [J3](journeys.md#j3), [J5](journeys.md#j5).
Requirements: Permission §6.5/6.7; Execution §8.3–8.8;
AC-IP13, AC-L06/07/09, AC-R01/03/06, AC-I09/28.
Owners: WP-07/11/14/21/23/39/41.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Reuse FX-02/04/05/08: queued work, two workers/one slot, accepted-but-response-lost fake mail, backup before restriction/possible acceptance with surviving independent journal. |
| Actor / action | Race withdrawal/cancel against final permit; lose command response; query original key; restart/restore; deliver delayed callback. Separately fail before known transmission and exercise bounded qualified retry. |
| Visible / persistent result | At most one reservation/permit for the slot; denial before final permit prevents handoff. In-flight possibility remains visible after cancel. `acceptance_unknown` preserves claim/reservation and blocks clean completion/cursor success. Same-key command query returns actual result. |
| Denial / recovery | No blind new-key retry or provider/channel failover. Restored outbound stays independently fenced; replay withdrawals/erasures and reconcile claims. Release requires the privileged human workflow/new epoch. Missing evidence stays held; no unsafe rollback or overdue burst. |
| Verification / limit | Future boundary fault injection with fake provider logs and durable-state/journal assertions proves modeled races and recovery only. Real account idempotency windows, remote cancellation limits, storage durability and host RPO/RTO require later VAL-04/05 evidence. |

<a id="prep-case-0011"></a>
## PREP-CASE-0011 — semantic access, operator observation and actual agent evaluation

**NOT EXECUTED.** All [five journeys](journeys.md#j1).
Requirements: Interaction accessibility/Orientation/Failures; UX §11.3;
AC-IP04/09/10/14, AC-O07, AC-I15/16/17/25/26/29/30.
Owners: WP-13/16/25/31; WP-17 carries later qualification.

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Representative saved/empty/held/stale fixtures from cases 0001–0010. Separate new operator, returning operator and human-agent handoff protocols; no assumed participant results. |
| Actor / action | Navigate by headings/labels/keyboard, operate modal focus and status/error announcements, follow stable object refs, inspect a result and recover after losing place/session. Use normal manual, contextual assistance, structured-tool and constrained computer-use variants. |
| Visible / persistent result | Same authorized object/revision and real command/receipt outcome across surfaces. Inspect improves precision only. Lost agent stops/reobserves; no speculative click retry. Non-color statuses and direct controls remain understandable without speech/AI. |
| Denial / recovery | Wrong-scope/expired session denies; focus returns meaningfully after error/cancel; saved state is refetched. Failure to understand consequences is recorded for repair, not hidden by fewer steps. |
| Automated specification / limit | Future accessibility/semantic/keyboard driver checks inspect roles, focus, labels and resulting state. They prove tested interface conformance, not screen-reader/operator usability or an actual external agent's success. |
| Operator observation / limit | Later observe actual new/returning participants completing the same tasks; record task/variant, assistance, completion/errors, prompts, navigation, meaningful decisions, review/correction edits, exceptional recovery and separate writing/review/administration elapsed time. Ask them to explain brand, audience, permission and effect boundaries; record their answers and observed misunderstandings. Compare raw observations with existing AC-O07/I30 targets; invent no score, threshold or passing result. |
| Real agent / provider evidence | Separately observe the actual qualified client/model under its constrained principal, grant/revocation and stop behavior, then independently inspect durable outcomes. Record exact model/client/configuration, interventions and failures. Coding-model qualification and scripted adapters cannot substitute for VAL-09/11 or VAL-06 operator evidence. |

<a id="prep-case-0012"></a>
## PREP-CASE-0012 — synthetic Kit completeness and unproved continuity

**NOT EXECUTED.** Journeys [J3](journeys.md#j3), [J4](journeys.md#j4), [J5](journeys.md#j5).
Requirements: [Kit migration](../../../specs/texenda-handoff/06-migration-and-production/kit-migration.md), §16.3;
ADR-0008 WP-12/18/19 and AC-IP11/12/16; AC-M01/02/03/04/05/06/08/09.
Owners: WP-12/19 synthetic mechanics; WP-18 real discovery, WP-17 qualification,
WP-20/33 later authorized transfer. See [preparation checklist](../../migration/kit-discovery-preparation.md).

| Field | Prepared scenario |
|---|---|
| Preconditions / inputs | Reuse FX-11 and FX-12; invented paginated source rows include all represented status classes, absent/explicit blank/value fields, shared-account restriction, historical event and unknown next-unsent step. No actual Kit account facts. |
| Actor / action | Synthetic importer follows every cursor and reconciles totals, previews per-field preserve/clear/quarantine mapping, replays twice in historical mode, then attempts resume from entry timestamp alone. Exercise legacy restriction intake and a simulated connected migration wave. |
| Visible / persistent result | Counts/coverage/mappings/holds are explicit; stronger denials persist, no import enrollment trigger or duplicate records/effects. Next-unsent-step remains unproved, so enrollment holds or receives an explicit reviewed retirement disposition. Forwarded opt-out permits scoped stop without unrelated profile disclosure. |
| Denial / recovery | Missing page/status/source evidence blocks completeness; unknown cursor cannot restart or skip guessed steps. A target lease does not fence Kit. Hold/drain/verified-resume/approved-retire/recreate dispositions require appropriate evidence; no dual sending or unsupported retirement claim. |
| Verification / limit | Future fake-reader/import/state-machine tests prove synthetic extraction/mapping/hold logic. They do not prove actual source topology, pagination completeness, working legacy links, source pause or recipient continuity. Read-only discovery and later control operation require separate authority and actual evidence under RAIDQ-0011/VAL-10. |

## Handoff into implementation

WP-01 uses these cases to close contracts and meaningful rejection examples.
Later feature owners implement executable tests beside actual handlers; WP-32
assembles exact synthetic evidence. Real operator observation, real AI/agent
evaluation and real provider/staging qualification remain separate records.
No product command is claimed available or successful by this document.
