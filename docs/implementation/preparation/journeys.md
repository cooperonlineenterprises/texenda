# Initial-experience preparation: shared journeys

Status: **EXPLANATORY PREPARATION; PRODUCT NOT IMPLEMENTED OR TESTED.**
Layout, action labels and example copy are reversible proposals, not requirements
or approval. This packet explains the accepted owners at source revision
`79db6081dd929af3f46a1cc8e1eec5f8ac09e9cc`; preparation base is
`efaa8fa9772d332dd3bfb2b40bbae2110b06a5fa`. Any governing-source change invalidates
the affected sketches/cases: compare the changed owner, regenerate and recheck
before reuse, preserving prior review evidence. The prose and transition tables
are the complete accessible equivalents of the text wireframes.

Read with [synthetic cases](synthetic-cases.md), the
[prepared WP-01 assignment](wp01-assignment.md), and the future
[Kit discovery checklist](../../migration/kit-discovery-preparation.md).
[ADR-0008](../../decisions/ADR-0008-integrated-initial-product-and-effective-plan.md)
owns the integrated initial scope and AC-IP additions. The
[sealed authority register](../../../specs/texenda-handoff/01-foundation/authority-register.json)
still dispatches unchanged semantics; this document adds no acceptance catalog.

## Shared reading keys

OHW and HP reuse the existing synthetic fixture labels. All new example addresses
and origins use `.invalid`, and no real account, recipient or source data is used.
`newsletter-A`, `page-A`, `proposal-A` and `run-A` below are documentation aliases
for future opaque object IDs, not proposed production keys or routes.

| Owner shorthand | Exact governing source and relevant section |
|---|---|
| UX | [Operator workflows](../../../specs/texenda-handoff/02-product-and-ux/operator-workflows.md), §11 and Accepted interaction evolution |
| Interaction | [Interaction architecture](../../../specs/texenda-handoff/02-product-and-ux/interaction-architecture.md), Surface contract through Interaction failures |
| Domain | [Canonical domain](../../../specs/texenda-handoff/03-domain-and-architecture/canonical-domain.md), §5.2–5.8 |
| Permission | [Permission and coordination](../../../specs/texenda-handoff/03-domain-and-architecture/permission-and-coordination.md), §6.1–6.8 |
| Execution | [Execution semantics](../../../specs/texenda-handoff/03-domain-and-architecture/execution-semantics.md), §8.1–8.8 |
| Commands | [Command catalog](../../../specs/texenda-handoff/03-domain-and-architecture/command-catalog.json) and [schema/contract guide](../../../specs/texenda-handoff/03-domain-and-architecture/schema-and-contract-guide.md), Request contract envelope and Consequence propagation |
| Content | [Content](../../../specs/texenda-handoff/03-domain-and-architecture/content.md), §9, amended only as named by [ADR-0005](../../decisions/ADR-0005-react-email-editor-reversible-default.md) |
| Agent/security | [AI and agent authority](../../../specs/texenda-handoff/04-security-governance-and-operations/ai-and-agent-authority.md), §10 and extension; [security](../../../specs/texenda-handoff/04-security-governance-and-operations/security-and-privacy.md), §14 and interaction threats |
| Acceptance | [Sealed acceptance catalog](../../../specs/texenda-handoff/06-migration-and-production/acceptance-catalog.json); AC-IP rows in ADR-0008 |
| Work | [Sealed WP contracts](../../../specs/texenda-handoff/05-implementation/work-packages.json), composed with the exact ADR-0008 updates |

Every surface uses the same authorized queries, commands, revisions and receipts.
Audience is a view over profiles/publications/segments. Publication remains the
recurring promise; a native acquisition page references its Property, brand,
Publication/purpose and disclosure, and does not replace it. Conversation is not
the saved draft or an execution engine. Complete manual controls remain usable
without AI; integrated assistance is still initial-product scope.

## Shared screens and states

<a id="s1"></a>
### S1: workspace and orientation

```text
Texenda   Workspace: OHW [change among authorized brands]   Actor / access
Home | Audience | Messages | Automations | Insights        Settings
Home
  Needs attention   Held resource request -> Why / inspect result
  Happening now     Approved work -> current execution state
  Planned           Newsletter-A -> draft / review / schedule state
  Changed           Revision and actor -> inspect diff
  Relevant results  Counts + window + coverage, or Unavailable
[Search objects / commands]  [Open saved work]  [one safe empty-state action]
```

Text equivalent: the current workspace and actor precede the five canonical
navigation entries. Home summarizes authoritative objects, with links back to
their revisions. Settings is secondary. A newcomer gets one safe next action;
a returning operator sees pending work and meaningful changes. An authorized
portfolio view is explicit and never means a send-to-all audience. Inaccessible
brands are absent from names, counts, search and errors. Home is a projection,
not another task/state authority.

<a id="s2"></a>
### S2: one persistent object workspace

```text
OHW / Messages / Newsletter-A   stable object link   revision 17   Draft
Saved revision / unsaved changes / actor              [History] [Why] [Inspect]
Publication + purpose     Content / subject / preview text     Audience / timing
Ordinary editable controls and preview
Contextual assistance: selected object + base revision + authorized context
  Draft suggestion / assumptions / sources / diff / validation
[Save draft] [Preview] [Request human review] [Cancel suggestion]
```

Text equivalent: the draft remains directly editable while a contextual panel
can propose changes to that exact object/revision. A save result links the new
revision; unsaved client patches and committed draft state are visibly distinct.
Canceling a suggestion leaves saved work intact. Inspect shows stable IDs,
validation and decision codes under the same authorization. The same shell can
hold a page, segment, recipe or automation; it does not create separate AI copies.
New page/resource/clone command names and closed DTOs are WP-01 outputs, not
invented here. These sketches refer to their required behavior.

<a id="s3"></a>
### S3: consequences and deliberate human review

```text
OHW / exact object + proposal + content revisions       Human review context
What changes: diff / facts / required disclosures / protected links
Who and when: publication, channel, sender, audience mode, date/time/IANA zone
Bounds: candidate ceiling, contact/cost ceilings, expiry, exclusions, coverage
Checks: test/preflight, conflicts, applicable policy, required assurance
Pending approval / stale / approved / expired          [Why]
[Return to edit] [Reject/cancel review] [Explicit authorized approval]
After approval: separate authorized commit/schedule action -> S4
```

Text equivalent: review shows the exact meaning and consequence envelope before
the human uses an accessible authenticated approval control. Approval is not
execution. C1 content drafts and C2 configuration previews do not authorize C3
publishing/scheduling/ongoing effects. C4 human-only authority operations stay in
their dedicated workflows; per-command rules still allow prompt recipient
withdrawal/confirmation without a campaign approval ceremony.

APR-01–06 remain controlling: required internal test/preflight, current recipient
and spending authority, hard ceilings and reapproval on material change. Elevated
solo review retains fresh MFA, the separate review step, retyped brand/count and
the existing cooling-off rule; an optional organizational second-human policy
does not become a universal requirement. The exact defaults remain in §14.3.
An agent never supplies the human challenge or inherits the human session.

<a id="s4"></a>
### S4: result, explanation and recovery

```text
OHW / object revision    command ID + original request key    receipt link
Drafted -> Proposed -> Approved by [human] -> Committed -> execution/outcomes
Current result: committed / held / denied / failed / acceptance unknown
Why: recorded rule, inputs, actor, coverage, revision and safe next action
Pending / in-flight / accepted / observed delivery shown separately
[Refresh authoritative result] [Inspect conflict] [authorized pause/cancel]
```

Text equivalent: each command and effect has its own outcome; the timeline does
not imply remote atomicity. Lost responses are resolved with the original
command/request identity. Uncertain acceptance retains the effect claim and
conservative reservation. Recovery never offers a blind new-key retry or another
provider/channel as an escape. A pause/cancel stops future permits and reports
the in-flight limitation; it cannot recall accepted mail.

<a id="s5"></a>
### S5: native recipient page

```text
OHW identity / fixed accessible layout / relevant promise and disclosure
Requested resource, if any: what it is and the applicable access terms
Email [                         ]    separately explicit choices if applicable
[Request / subscribe as described]   understandable errors / request status
Thank-you: confirmation needed, completed, resource available, or safe recovery
```

Text equivalent: a recipient sees the specific publication/purpose and request,
not operator controls. The thank-you view reflects actual confirmation and
fulfillment state with non-enumerating copy. A resource request or confirmation
does not grant unrelated marketing. Keyboard focus and status announcements
cover submission, error and recovery. Only fixed signup/thank-you layouts are
proposed; no blog, archive, general site builder or arbitrary scripts.

<a id="j1"></a>
## J1: new and returning orientation in the correct brand

Start: an authenticated, scoped operator opens Home without an active object, or
returns with a saved object/session reference. S1 identifies the last authorized
brand; if it is no longer authorized, scope is reselected from allowed choices.

| Action and visible information | Saved state, boundary and recovery |
|---|---|
| Open Home or keyboard search; inspect Attention/Now/Planned/Changed/Results. | Queries expose only current authorized scope. No send or publication follows navigation. No data is presented as zero merely because its source is unavailable. |
| Select OHW and open Newsletter-A from its stable link. | Session scope/object reference is explicit; S2 refetches the current revision. Switching workspace clears scope-sensitive referents such as “that newsletter.” |
| Return after interruption to draft, pending review or held work. | Saved draft/proposal/approval/result survives; expired approval remains expired. Unsaved patches require save/reconcile/cancel, not silent replacement. |
| Attempt an HP URL with OHW-only authority, or cancel a workspace switch. | Server denies without HP enumeration; OHW saved work remains. Cancel preserves the current authorized context. Restore access through the proper human workflow, never an AI shortcut. |
| Read “Why held?” or an outcome. | Evidence links distinguish preview, eligible dispatch, acceptance and observed delivery. Missing evidence is stated. Routine success stays quiet; notices deduplicate by cause/object. |

Success: the operator can identify the brand, object, saved state and safe next
action without reconstructing chat. A lost/revoked session stops protected work,
then reauthentication and refetch restore only still-authorized context.
Continue to [J2](#j2), [J3](#j3) or [J4](#j4); shared interruption is [J5](#j5).

Trace: UX §11/Accepted evolution; Interaction Context continuity, Orientation,
accessibility and failures; Domain §5.2/5.8; ADR-0008 WP-13/25/26/31.
Owners: WP-13/25/26/31 (WP-01 foundational cases).
AC-IP04/09/10/14/15; AC-I03/04/17/19/25/26/30; AC-S01.
Cases: [0001](synthetic-cases.md#prep-case-0001),
[0011](synthetic-cases.md#prep-case-0011).

<a id="j2"></a>
## J2: one newsletter from manual or embedded AI creation to human approval

Start: an OHW editor with draft capability wants an educational newsletter for
the OHW publication. No Offer, course, commerce connection or model is required.
Use S1 → S2 → S3 → S4; both creation routes converge on the same saved object.

| Action and visible information | Saved state, boundary and recovery |
|---|---|
| Manual: create content/campaign and enter subject/body. Assisted alternative: ask in context for the same draft. | `CreateCommunicationDraft`/`CreateCampaignDraft` return persistent references. The assistant supplies validated proposed inputs, never its own store. Draft-capable actors may invoke the authorized C1 path; draft creation is not `CommitProposal` C3 authority. |
| Continue manually, then ask for a shorter introduction on that saved draft. | `UpdateRepresentationDraft` requires the expected revision. Unsaved visual edits are explicitly committed as a draft or reconciled/cancelled before assistance edits. A suggestion is visibly proposed until the appropriate draft command saves it. |
| Correct a fabricated date/claim or wrong tone; inspect sources and diff. | Human correction creates a new draft revision. Protected facts, CTA meaning, brand, disclosures and content hashes remain bound. Reject/cancel leaves the prior saved revision available. Invalid output produces no mutation; outage retains ordinary editing. |
| Select the audience and propose timing, then preview HTML/plain text and audience consequences. | `UpdateCampaignDraft` is C2; `PreviewCampaign` is a read. Preview shows evaluation time/coverage, rule-vs-fixed audience mode, ceiling, exclusions, sender, expiry and explicit timezone. It grants no delivery authority. |
| Complete internal test/preflight and human content/campaign review in S3. | `PublishCommunication` and `ApproveCampaign`, or exact proposal approval where applicable, retain their human-only controls. Approval binds immutable revisions and envelope. A stale dependency or changed audience/schedule/content returns to review. |
| Save approved work or deliberately schedule the exact approved envelope. | Approval alone does not send. `ScheduleCampaign` runs only as an authorized human or constrained approved-command executor; resulting revision/receipt appears in S4. Actual effects still require current domain gates. |

Success: one newsletter and its linked communication/representation history survive
manual ↔ assistant ↔ tool handoff; no second AI draft truth exists. Ambiguous
“send that Friday” pauses for exact object/time clarification. Denied approval
does not destroy the draft; cancel review or scheduling through the authorized
control. Concurrent edits and unknown results follow [J5](#j5).

Trace: Content §9 + ADR-0005; Commands named above; Execution §8.2; Interaction
Shared pipeline/Context/Approval; Agent/security §10/14.3; ADR-0008 WP-01/13/15/27/29.
Owners: WP-01/10/13/14/15/25/26/27/29/31.
AC-IP04/06/07/08/14; AC-I01/02/04/07/08/18/19/27;
AC-A01/03/04/05/06; AC-L09.
Cases: [0002](synthetic-cases.md#prep-case-0002)–[0005](synthetic-cases.md#prep-case-0005).

<a id="j3"></a>
## J3: native signup, thank-you, confirmation and requested resource

Start: an OHW operator drafts `page-A` for a scoped Property and publication;
a separate synthetic recipient requests `resource-A` at `ohw.example.invalid`.
Operator work uses S2/S3/S4; the recipient uses S5, never the operator session.

| Action and visible information | Saved state, boundary and recovery |
|---|---|
| Author and preview fixed signup/thank-you layouts, promise, frequency, fields, disclosure and resource reference. | AcquisitionPage revisions pin Property/brand/Publication-or-purpose/disclosure; content owns versioned resource manifests. Asset storage owns bytes only. Draft autosave is not publication. |
| Human reviews and explicitly publishes a revision on a synthetic local origin; later revises/unpublishes. | Atomic activation preserves the last good revision on failure. Invalid or removed assets block/invalidate affected unpublished or stale revisions. Publication/unpublication/domain effects need their separate approval; drafting grants none. |
| Recipient submits the disclosed subscription request. | `RequestSubscription` records a pending request with actual disclosure/proof context and bounded confirmation effect. Generic response avoids enumeration. No operator account or marketing enrollment is created by the form. |
| Recipient completes valid confirmation; reloads or repeats it. | `ConfirmSubscription` uses the scoped recipient capability: one valid grant/subscription and no repeat welcome trigger. Old confirmation after withdrawal is stale; new scoped reconsent cannot release a safety hold. |
| Recipient requests/receives the approved resource under its verified request policy. | ResourceRequest and shared delivery state link request, purpose, endpoint, resource revision and effect identity. Fulfillment may be authorized without unrelated marketing permission; confirmation for one purpose cannot create another grant. |
| Missing asset, expired link, repeated request, abusive input or failed/unknown fulfillment. | Visible bounded held/error/recovery state; non-enumerating responses and rate/size/dedup limits. Revalidate resource/current denial before a safe retry. Unknown acceptance follows original effect reconciliation, never a new-key duplicate. |
| Recipient withdraws or operator cancels/unpublishes. | Withdrawal remains consent evidence, distinct from safety Suppression; pending marketing stops under current policy. Unpublishing does not erase prior requests/evidence or recall in-flight fulfillment. Cancelled work is reported truthfully. |

Success: actual saved page/request/confirmation/resource states explain the
thank-you result; access is not sold as automatic enrollment. Existing sites may
link/embed this page, but cannot substitute for Texenda's native lifecycle.
Continue to [J4](#j4) only through a qualified scoped enrollment trigger.

Trace: ADR-0008 Decision/ownership and WP-01/10/12; Permission §6.1–6.6;
Content §9; Execution §8.3–8.6; Agent/security §14.1/14.4.
Owners: WP-01/03/05/10/11/12/15/40.
AC-IP02/03/15; AC-D03; AC-S01/02/03/04; AC-L06/07.
Cases: [0006](synthetic-cases.md#prep-case-0006),
[0007](synthetic-cases.md#prep-case-0007), [0010](synthetic-cases.md#prep-case-0010).

<a id="j4"></a>
## J4: welcome, nurture, reviewable hygiene and safe reuse

Start: an OHW operator opens Automations with draft capability and a scoped
confirmed synthetic subscription. A welcome recipe and educational nurture need
no commerce object. S2/S3/S4 also support this workflow through manual controls.

| Action and visible information | Saved state, boundary and recovery |
|---|---|
| Choose/edit a welcome or nurture recipe; optionally ask assistance for a draft. | `CreateWorkflowDraft` stores a bounded sequence/automation definition with stable nodes. Show enrollment, waits, maximum contacts, expiry, reentry and stopping rules. AI adds no executor. |
| Simulate, review and publish through authorized approval. | `SimulateWorkflow` precedes `PublishAutomation`; exact content/revision/ceilings are reviewed. Authorized activation is distinct from draft save and simulation. |
| Observe enrollment, acceptance and waits; edit for future entrants. | SequenceEnrollment identifies membership; AutomationExecution owns the sole cursor. Acceptance anchors a send wait; uncertainty holds it. Existing runs remain pinned; new revision alone neither restarts nor migrates them. |
| Review a re-engagement/sunset candidate set and its evidence. | Missing required event coverage returns UNKNOWN/HOLD. Opens are weak evidence; no blanket resend/nonopen-only sunset, automatic erasure or repermission. Explicit stopping rules, consequences and human review precede effects. |
| Clone previously approved/sent content or a recipe for another issue. | New draft identities contain reusable content/structure only: no approval, frozen recipients, live schedule/activation, enrollment, cursor, delivery/effect history. Source history remains intact. Target-brand adaptation requires authorized context and review, never audience transfer. |
| Pause/cancel or recover after restart. | Pending actions stop through authorized commands; no catch-up burst or blind continuation. Correct the draft prospectively or use an explicit reviewed run migration; missing mapping stays held. |

Success: a representative sequence completes with explainable state and bounded
contact, and reusable work starts safely as a fresh draft. Optional purchaser
exit is unavailable without a qualified source; “no observed purchase” cannot
become proof of nonpurchase or fabricated revenue. S4 shows the limits.

Trace: Execution §8.7–8.8; Domain §5.7; Permission §6.7–6.8; Interaction Durable
work/Orientation; ADR-0008 WP-14/16/22/23.
Owners: WP-06/14/16/21/22/23; WP-10 content reuse, WP-25/31 observation.
AC-IP05/06/10/13/14; AC-W01/02/03/05/08/09; AC-D07/08;
AC-A03/06; AC-O07; AC-I25/26/30.
Cases: [0008](synthetic-cases.md#prep-case-0008),
[0009](synthetic-cases.md#prep-case-0009), [0011](synthetic-cases.md#prep-case-0011).

<a id="j5"></a>
## J5: interruption, handoff, stale work and uncertain delivery

Start: an operator, built-in intermediary, explicitly delegated external agent
or deterministic worker resumes an existing J2/J3/J4 object. Each retains its
own actor and authority; an external agent never receives the human session.
S2 preserves draft work, S3 isolates human approval, and S4 explains recovery.

| Trigger / permitted action | Visible and persistent outcome; denial/cancel/recovery |
|---|---|
| Human hands Newsletter-A to a scoped tool/agent and later resumes. | Object + revision + scope + pending proposal/result are persisted. Commands record initiator, intermediary, human authorizer and executor distinctly. Revalidate grant/current membership; revoked/expired scope stops new commands without deleting the draft. |
| Human saves revision 18 while the agent references revision 17; local edits also exist. | Mark proposal stale and retain intended edits. Show current diff and explicit merge/cancel choice. No silent rebase or overwrite; material changes invalidate approval and require fresh review. |
| AI returns incorrect/ambiguous/invalid/manipulated output, loses streaming connection or goes offline. | Provisional text never commits. Deterministic schemas, scope and policy reject unsafe proposals; a bounded correction or clarification precedes manual recovery. Authorized manual drafts and approved deterministic execution remain complete. |
| Agent loses its UI/session or tries a human-only approval control. | Stop/reobserve with attributable checkpoint; actual result is queried. No guessed clicks, human-cookie fallback or self-approval. The human resumes through an independent authorized review context. |
| Client response disappears after a command. | Query the original command/request identity; return committed/failed/pending result. Do not create a new key to “try again.” Cancellation itself has an observable command/result. |
| Delivery is definitely rejected, acceptance is unknown, or cancellation/withdrawal races handoff. | Show failure versus `acceptance_unknown`, hold uncertain claims and reconcile. Denial committed before final permit prevents handoff; already permitted in-flight work may finish. No alternate-provider/channel escape. |
| Restart or restore follows accepted/unknown effects and later restrictions. | Drafts/cursors/claims remain durable; restored outbound starts fenced. Replay restrictive/erasure evidence and reconcile effects before a privileged human releases recovery under a new epoch. No stale grant revival or duplicate continuation. |

Success is either a verified current result or a truthful hold with a safe next
action; uncertainty is not converted to completion. Cancel stops future work
within its actual boundary and preserves audit/history. Return through [J1](#j1)
to the current object, not a replay of conversational instructions.

Trace: Interaction Context/Approval/Failures; Commands idempotency/approved
executor; Agent/security extension/threats; Execution §8.3–8.8; Permission §6.5;
ADR-0008 WP-15/26–29/31/39/41.
Owners: WP-07/11/15/21/23/26/27/28/29/31/39/41.
AC-IP04/07/08/09/13; AC-I02/03/08/09/10/11/12/13/14/15/16/19/27/28/29;
AC-L07/09; AC-W08/09; AC-R01/03/06.
Cases: [0003](synthetic-cases.md#prep-case-0003)–[0005](synthetic-cases.md#prep-case-0005),
[0010](synthetic-cases.md#prep-case-0010), [0011](synthetic-cases.md#prep-case-0011).

## What still needs evidence

No foundational product question is reopened. WP-01 still has to close exact
page/resource/clone DTOs, lifecycle guards and error/result contracts within the
accepted ownership; these sketches do not preselect an unsupported command.
WP-25/31 and VAL-06 must observe whether new/returning operators can find scope,
understand consequences and recover with acceptable prompting/review/correction
effort. [Case 0011](synthetic-cases.md#prep-case-0011) defines how to observe that
without inventing scores. Actual provider, AI and external-agent quality remain
separate qualifications, not open product-definition choices.

Voice remains the accepted direction: explicit push-to-talk/visible capture,
mute/cancel, text/manual fallback and no conversational approval. WP-30 and
VAL-12 are separately triggered by owner selection of the voice profile. No
always-on listening or new prerequisite is added to these non-voice journeys.
