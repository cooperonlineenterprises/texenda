# UX and information architecture

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f11"></a>
## 11. UX and information architecture

**Decision status: AUTHORITATIVE DECISION.** Optimize common intent, not internal machinery. Brand context and consequential effects are always visible.

### 11.1 Navigation

Top-level navigation: **Home, Audience, Messages, Automations, Insights**. Settings is a persistent secondary entry. Audience contains profiles, publications, segments, tags, attributes and Forms. Messages contains Broadcasts, Templates and Calendar. Automations contains Sequences, workflow recipes and execution management. Deliverability appears as a contextual health panel and a Settings/Insights destination; Integrations and channel administration live in Settings.

The workspace selector defaults to the last authorized brand. “All brands” is an explicitly authorized portfolio view; it never becomes a send-to-all audience. Display brand identity in the composer, approval, preview and schedule confirmation. Brands not accessible to a principal are neither listed nor exposed through counts/errors.

### 11.2 Workflow contracts

| Workflow / goal | Minimum explicit decisions | Defaults and safe generation | Required interpretation/consequence preview | Advanced controls and explanation |
|---|---|---|---|---|
| Audience lookup/manage | Brand and person/query | Brand-local search, masked sensitive fields | Current subscription and safety state; distinguish endpoint from person | Consent timeline, source/evidence, permitted correction commands |
| Form / acquire subscribers | Publication/purpose, disclosure, fields, placement | Email, double opt-in, approved brand style; AI may draft copy | Exact promise, frequency, source, resulting grant and welcome behavior | Allowed origins, proof policy, rate limits, field mappings |
| Segment / select people | Brand and criteria | Common predicates; optional natural language | Human-readable definition, unknown coverage, candidate count/sample, permission exclusions | AST, compiler version and evaluated facts; editable without AI |
| Broadcast / communicate once | Audience, content, sender if nondefault, time/expiry, final approval | Email primary; brand sender; standard footer; inherited pressure policy | Channel, membership-at-send vs fixed snapshot, candidate ceiling, exclusions, cost ceiling, competing work and current approval | Tracking, precise windows, fixed-snapshot mode, rate profile; per-recipient decision reasons |
| Sequence / maintain a progression | Trigger/enrollment, content steps, waits, completion/exit | Linear recipe, no repeat enrollment, stop on opt-out/purchase/expiry | Maximum contacts, timing, reentry, pinned version and stopping rules | Step IDs, exception branches and progress history |
| Automation / respond to events | Trusted trigger, conditions, actions, expiry/exit | Approved bounded recipe, email primary | Plain-language flow, send upper bound, source-health requirements and simulation | Typed graph, wait/deadline semantics, migration between versions |
| Channel choice | Whether to activate a qualified alternative | Email unless explicitly chosen; one outbound primary | Eligibility, permission, cost, fallback/follow-up distinction | Approved preference order and exact route policy |
| Calendar / avoid conflicts | Time window and brand(s) | Group approved scheduled communications | Conflicts, predicted caps/deferrals, expiry and unpublished drafts | Source-level plans and reservations; no implied audience permission |
| Import / migrate safely | Source, mapping, consent provenance, conflict treatment | Stage/dry run, no triggers, preserve denials | Created/updated/held/invalid counts; projected subscriptions; unsupported states | Per-row evidence, source IDs, rollback constraints and downloadable rejects |
| Insights / understand outcomes | Brand/time window | Verified counts, operational exceptions first | Denominators, missing data, weak-signal limitations and estimated/actual cost | Raw normalized events within role/retention; receipt drilldown |
| Deliverability / resolve incidents | Acknowledge incident, authorized corrective action | Automatic scoped pause for qualified threshold failures | Cause, affected sender/scope, evidence, last healthy time and unsafe actions disallowed | Provider logs/qualification, suppression review, reconciliation results |
| Preferences / recipient control | Desired scope/change | Brand-branded current publication/channel | Precisely what stops/changes; no cross-brand PII disclosure | Stronger verification only for reading broader data or adding permission |
| Integrations/settings | Connector/property/sender and allowed purpose | Least privilege, disabled until qualified | Data shared, effect scope, spend, webhook/reply owner and readiness | Credential rotation, API versions, scope mappings and retention |

### 11.3 Approval and simplicity

The interaction sequence is **intent → simple configuration → plain-language interpretation → consequence preview → approval → deterministic execution → explanation**. Generated configuration stays editable in ordinary structured controls. No opaque “AI automation mode” exists.

**REVERSIBLE DEFAULT acceptance targets:** at least 90% of representative routine tasks completed without advanced controls; a prepared ordinary campaign takes no more than five meaningful configuration decisions and approximately five minutes of administration excluding writing/review; routine portfolio maintenance aims below one hour/week excluding incidents/content. Validate with actual operators under VAL-06 rather than assert these targets are already achieved.

Test send, audience review and a final explicit approval are normal even for a solopreneur. A second person may be required by an organization's optional policy, but the default high-risk self-approval route uses step-up authentication, retyped brand/count confirmation, a separate review screen and a cooling-off interval. Exact thresholds are in section 14.

Never say an AI “decided” when a deterministic rule acted. Prefer: “Held because today's contact allowance is already used” and link the rule. Every count distinguishes preview, frozen candidates, eligible dispatches, accepted requests and observed outcomes. Accessible keyboard navigation, screen-reader labels, focus management and non-color-only statuses are required for the custom views.

**Consequence:** use generated Payload UI for low-frequency drafts/settings; custom views own audience, composer, segment, sequences, imports and explanation workflows. **Revisit:** adjust navigation based on observed task failures, not feature-count pressure.

---


## Accepted interaction evolution

The current top-level navigation is **Home, Audience, Messages, Automations, Insights**; persistent workspace context is always visible. Forms/publications/segments live under Audience. Broadcasts/templates/calendar live under Messages. Sequences are a simple view under Automations. Deliverability/integrations/policies live in Settings with direct contextual links. Earlier labels in this section describe capabilities, not competing navigation requirements.

Home orients by Attention / Now / Planned / Changed / Results. Every core object has a stable URL, revision history, contextual actions and a Why view. A command/search palette gives exact object search and navigation without requiring AI. Empty states provide one safe next step; draft autosave is clearly distinguished from publication. Inspect mode exposes precision without increasing authorization.

See [interaction architecture](interaction-architecture.md) for normative multimodal handoff, approval, voice, proactivity and failure behavior. Accessibility and keyboard/direct manipulation are required for the email pilot; voice, external agents and an AI assistant are not.
