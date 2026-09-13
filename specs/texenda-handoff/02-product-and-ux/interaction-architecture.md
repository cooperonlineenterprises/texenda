# Human- and agent-native interaction architecture

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Accepted interaction architecture and complete-handoff directive. Apply [package authority](../DECISION-STATUS.md).


## Decision

**Status: AUTHORITATIVE DECISION.** Texenda is object-first, voice-forward, and multimodal. Visual workspaces remain fully operable without any AI. Conversation discovers and modifies intent; structured objects preserve work. This is the canonical owner of interaction behavior; domain effects remain owned by the domain chapters.

## Surface contract

| Surface | Role | Strong tasks | Must not do |
|---|---|---|---|
| Visual/direct manipulation | Primary persistent workspace | Long-form content, audience comparison, exact rules, analytics, approvals | Reimplement policy in components |
| Keyboard/command search | Fast shared navigation | Object search, contextual actions, precise focus | Create shortcuts around approval |
| Text conversation | Complementary intent interface | Find, explain, draft, modify a proposal, summarize evidence | Store the only copy of a goal or configuration |
| Voice | Complementary, voice-forward | Goals, navigation, small edits, orientation, why-questions | Treat filler, background speech or provisional transcription as approval |
| Built-in AI | Scoped interpretation adapter | Draft typed proposals, explain records, suggest bounded improvements | Invent authority, execute arbitrary SQL/URLs or directly call providers |
| Structured external tools/API | Preferred machine surface | Precise queries, typed proposals, qualified commands | Inherit all delegator authority or return cross-brand private context |
| Inspect mode | Shared expert/agent view | IDs, revisions, rules, policy results, execution state | Grant permissions unavailable in the simple view |
| Computer use | Compatibility/fallback | Operate semantic UI when tools unavailable | Become privileged because a control is visible |

Access hierarchy: structured Texenda tool/API → optional browser-semantic tools → accessible graphical UI → screenshot/computer actuation. No second agent application.

## Shared pipeline

```text
intent → authorized context → typed proposal → deterministic validation
       → authority/policy check → consequences → approval where required
       → application command → domain transaction/outbox → execution → receipt
```

Read-only queries and reversible drafts may skip unnecessary confirmation, not authorization. User-facing mutation results link to the resulting object revision. A timeout returns a command ID and a queryable outcome, never an invitation to submit a new key blindly.

## Context continuity

The server retains session ID, authenticated actor/delegation, current workspace, optional goal, explicit active-object refs and revisions, selection refs, committed transcript turns and proposal refs. The client retains unsaved editor patches and focus. Persist resumable draft content through ordinary draft commands, not conversational memory.

Before an assistant modifies an object with unsaved visual edits, it MUST commit an explicit draft revision or request a merge/cancel decision. It MUST NOT overwrite the unsaved buffer. Remote edits invalidate the proposal's base revision. Selection is an aid to reference resolution, never authority. Workspace changes clear scope-sensitive referents. Persist `object_id + revision`, not an indefinite meaning for “that.”

“Friday morning” becomes an explicit date, local time and IANA timezone in preview. If two campaigns are plausible, consequential mutation pauses for disambiguation. Known facts, safe inferred defaults and consequential unresolved assumptions are displayed separately. Do not ask about already-known nonconsequential defaults.

## Durable work

A Goal has title, outcome statement, owner, workspace, status, optional time window, links to campaigns/automations and typed constraints. It is not a project-management board. A proposed set of commands is a Proposal, not a second workflow runtime. A published campaign/workflow remains the execution authority.

A conversational sentence can propose a policy, preference or constraint. Only the corresponding authorized command can activate it. Free-text imported instructions have no authority. General hidden AI memory and a vector database are not required.

Operator Goal achievement and the workflow's verified business-completion condition are different concepts. Marking a goal “achieved” MUST NOT synthesize a purchase, expand permission or silently cancel live work. Any goal-status-to-execution behavior must be an explicitly approved, typed binding.

## Consequence classes: five classes, not four

| Class | Behavior | Gate |
|---|---|---|
| C0 read | Search, navigate, explain | Current read authorization; immediate |
| C1 reversible draft | Create unpublished content/goal/proposal; edit draft | Authorized draft capability; revision, undo/history |
| C2 material configuration | Stage import, propose schedule or audience change | Deterministic diff and preview; commit confirmation where required |
| C3 external/ongoing effect | Schedule approved send, activate workflow, approved cross-brand plan | Exact immutable proposal/configuration plus approval envelope and ordinary domain gate |
| C4 authority/safety sensitive | Delegation expansion, permission correction, hold release, policy relaxation | Dedicated privileged evidence-backed workflow; AI forbidden to approve or originate unauthorized authority |

Creating a draft schedule is C1/C2; committing a live schedule is C3. A destructive or large draft operation can require stronger review. Static metadata is a minimum; the policy engine can raise risk, never silently lower it. No class bypasses the foundation's APR/POL controls.

## Approval and undo

Approval binds proposal revision/digest, target base revisions, command list, workspace/purpose/channel/sender, schedule, candidate/contact/spending ceilings, authority epoch, expiry and authentication assurance. It can authorize a dynamic membership calculation only inside the reviewed ceiling; it does not approve arbitrary later changes.

C3/C4 approval uses an explicit accessible control and current authenticated assurance. A spoken “yes” in assistant conversation is not that control. Keyboard, screen reader, switch access and assistive voice-control tools may operate the same deliberate review. The assistant cannot supply its own human challenge response. A registered computer-use agent cannot use its delegating human's session to evade its own limits; human-only approval uses an out-of-agent approval context.

Undo creates a new revision or compensating command. Delivered mail cannot be recalled. Pausing prevents future handoff permits; it cannot retract in-flight remote work. Bulk proposal commands default to atomic database-only mutation when supported; effects execute separately. Otherwise list independent per-command outcomes and resumable remainder—never claim all-or-nothing remote effects.

## Voice

Default push-to-talk, visible mic indicator and immediate mute/cancel. Optional continuous capture exists only within an explicitly active session; never wake-word/background capture by default. Microphone denial yields text/direct UI. Latency targets are measured in the voice pilot, not frozen without evidence.

Initial path: capture → streaming STT → shared textual assistant → typed proposal → text plus optional TTS. Streaming transcript is provisional until finalized. Critical negations, names, channels, dates, counts and money receive exact visual review. Low STT confidence or semantic uncertainty holds consequential work, even if confidence scores are absent or falsely high. Interrupting speech stops playback; cancelling a request is a separate visible command.

No raw audio retained by Texenda by default. Session capture ends on explicit end, navigation away where appropriate, expiry or tab closure. TTS does not read unnecessary PII aloud; offer silent mode. Disable private details on shared-screen/voice mode. Provider data retention, region, logging and subprocessor behavior require VAL-12; “we delete audio” is not a claim about the provider.

## Orientation and proactivity

Home groups: Needs attention / Happening now / Planned / Changed / Relevant results. These are projections over domain/execution/receipt data, not a second task authority. All object pages offer “Why?” and link to decisions, inputs and relevant revisions.

Deterministic notices detect staleness, blocked executions and conflicts. AI may summarize, recommend or prepare a draft. Deduplicate notices by cause/object, set severity, snooze and acknowledgement, and keep routine success quiet. Owner attention is a limited resource too. No self-created optimization backlog merely because the model can produce suggestions.

“What did the AI do?” separates drafted, proposed, approved-by-human and committed actions with command/receipt links. Explanations use evidence, never invented hidden reasoning or causal claims.

## Agent/expert and accessibility contract

Target WCAG 2.2 AA. Native semantic HTML first; visible labels, roles/names/states, meaningful headings, focus management, keyboard alternatives to drag, status announcements, sufficient contrast, reduced-motion support and readable errors. Test with screen readers and real keyboard workflows in addition to automated checks. [N04](../09-reference/source-register.md#n04)

Inspect mode reveals exact segment AST, stable node IDs, revision, current state, scope, validation paths and decision codes subject to the same read permissions. It is available to authorized humans too. Never hide agent-only privileged controls in DOM or trust tool annotations as authorization.

One stable URL per object. No hover/color/icon-only consequential meanings. Object IDs are available in Inspect, not required for routine conversation. Computer-use qualification tests observe actual resulting state, not just an agent's claim of clicking a button. Browser-semantic/WebMCP support is a gated progressive enhancement, never a prerequisite.

## Interaction failures

| Failure | Required response |
|---|---|
| Ambiguous object or critical speech | Clarify selected object/value; no commit |
| Model/STT/TTS outage | Keep object/draft; text/manual UI fully usable |
| Invalid typed output | Bounded correction attempt; no mutation; show error and manual path |
| Stale base revision | Mark proposal stale; diff/rebuild/reapprove, never silently rebase |
| Human/agent concurrency | Optimistic conflict, retain both intended edits, explicit merge |
| Agent lost in UI | Re-observe, stop or request help; no scope escalation |
| Request response lost | Query command result using original key |
| Execution fails after approval | Record failure/uncertainty, reconcile under approved scope |
| Delegation revoked mid-run | No new commands; terminate session; in-flight effects follow existing reconciliation |
| SSE disconnect | Reconnect using scoped event cursor or refetch authoritative objects; stream is not authority |

## Implementation order

Commands/revisions/audit and accessible human UX first. Proposal/diff/approval infrastructure precedes writable AI. Text assistant and lightweight goals then voice. External structured read/proposal access follows delegation tests. Controlled writes and computer-use qualification follow independently. Proactivity is last and exception-driven. None blocks the email pilot.
