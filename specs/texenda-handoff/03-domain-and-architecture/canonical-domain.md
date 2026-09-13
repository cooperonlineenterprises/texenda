# Canonical domain and data model

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f05"></a>
## 5. Canonical domain and data model

**Decision status: AUTHORITATIVE DECISION.** The following conceptual relationships govern schema design; physical table names and indexes may vary without changing semantics.

### 5.1 Relationship map

```text
Organization
  +-- Workspace/Brand --+-- Property
  |                    +-- Publication/Purpose
  |                    +-- SenderIdentity --> ProviderAccount/qualification
  |                    +-- Segment / Content / Campaign / Workflow definitions
  |
  +-- Person -- Identity bindings
          +-- WorkspaceProfile -- Subscription -- Permission grants/withdrawals
          |                  +-- Tags / typed attributes / audience facts
          +-- Endpoint bindings --> CommunicationEndpoint (channel-specific)

Campaign or workflow node --> Communication revision + occurrence key
                              |
                 frozen recipient selection
                              |
                         DeliveryPlan
                     /                     \
          approved primary Delivery    explicit companion/follow-up Delivery
                       |                         |
                 DeliveryAttempt(s)       channel-specific behavior
                       |
              Provider observations

Every consequential decision --> DecisionReceipt + AuditRecord
```

### 5.2 Portfolio and audience entities

| Concept | Purpose, scope and authority | Key and lifecycle | Relationships |
|---|---|---|---|
| **Organization** | Top-level ownership/isolation boundary; Texenda authority | Opaque ID; active/paused/closed. One seeded organization initially | Owns brands, identity directory and organization policies |
| **Workspace / Brand** | Operational and recognizable sender boundary; organization-scoped | Opaque ID; unique slug per organization; draft/active/paused/archived | Owns properties/publications, profiles, campaigns and sender bindings |
| **Property** | Acquisition/onsite/app surface; brand-scoped | ID; unique verified origin/namespace binding; pending_verification/active/disabled | One owner workspace; multiple publications/placements allowed |
| **Publication** | Named recurring communication promise, purpose and frequency; brand-scoped | ID; unique workspace slug; draft/active/paused/retired | Versioned disclosure/cadence; channel offerings; subscriptions |
| **Person** | Canonical operational subject, not infallible proof of a human | ID; active/restricted/merged/erasure_pending/erased | Profiles and verified/pseudonymous identities; historical IDs preserved via restricted redirects |
| **Identity** | Organization-scoped identifier or trusted account subject; Texenda authority for its binding | `(organization, kind, issuer_namespace, normalized_value)` unique when applicable; unverified/verified/disputed/retired | Distinct from an endpoint; bindings have evidence and validity intervals |
| **WorkspaceProfile** | A person's relationship to one brand | Unique `(organization, workspace, person)`; active/archived/restricted | Tags, attributes, subscriptions and brand-local facts |
| **Subscription** | Current membership in one publication and one explicitly offered channel | Unique `(profile, publication, channel)`; pending/active/withdrawn/ended | Current projection of consent events; may have eligible endpoint grants; active does not imply deliverable |
| **Audience** | User-facing view of relevant profiles | **Not a second list database or independent permission object** | Publication members or a Segment result |
| **Tag** | Brand-local classification, never permission | ID + workspace-unique slug; active/retired | Unique assignment per profile/tag |
| **Attribute** | Typed, scoped data with provenance | Definition ID + version; value per subject/field; unset/value/invalid | Person-global fields explicitly allowlisted; most values brand-local |
| **Segment** | Versioned selection expression | ID + immutable revision; draft/published/retired | Workspace-local fields, subscriptions and event predicates |

### 5.3 Permission and channel entities

| Concept | Purpose/scope/authority | Key and lifecycle | Relationships |
|---|---|---|---|
| **Channel** | Stable family of communication semantics | Code: `email`, `onsite`, `web_push`, later qualified codes; supported/disabled | Not interchangeable transports |
| **CommunicationEndpoint** | Addressable destination or installed subscription | ID; unique channel-specific fingerprint in its valid namespace; unverified/ready/temporarily_unreachable/blocked/expired/retired | Email address; push endpoint+keys+origin; phone/program binding; app token; onsite session has different semantics |
| **EndpointBinding** | Evidence tying an endpoint to a subject/context | ID + validity interval; proposed/verified/disputed/retired/shared | A reachable endpoint alone cannot merge subjects or grant marketing permission |
| **ConsentEvent** | Append-only evidence of request, confirmation, grant, withdrawal or correction | Event ID + monotonically applied subject/scope version; recorded/invalidated-by-correction | Original source, source time, received time, disclosure version and proof reference |
| **PermissionGrant** | Effective affirmative authority for a specific brand/publication-or-purpose/channel and endpoint binding | ID; pending/granted/revoked/expired; explicit validity | Derived atomically from consent evidence; cannot be edited by raw CRUD |
| **Withdrawal** | Recipient restriction at publication, brand, organization, channel and/or endpoint scope | ID; effective from authoritative receipt/application; active; scoped fresh reconsent may supersede only explicitly acknowledged restrictions | Not the same as endpoint invalidity or a provider block |
| **Preference** | Delivery order, cadence, pause, quiet hours, language; never creates authority | Subject/context + key + revision; active/expired | Restricts eligible alternatives; more restrictive applicable limits prevail |
| **Suppression** | Operational/safety prohibition independent of subscription membership | ID; scope+reason+origin; active/released/expired for temporary holds | Endpoint invalidity, complaint safety hold, provider block, admin hold; release requires its own authorized evidence |
| **CommunicationPolicy** | Versioned rules and limits | ID/version/effective interval; draft/active/retired | Recipient restrictions and current safety rules can tighten prior campaign authority |

Opt-out state is not independently editable in both Subscription and Suppression. Recipient withdrawals belong to the consent model; suppression is for safety/transport restrictions. The UI may group both under “Do not contact,” but the records retain their different meanings.

### 5.4 Communication and execution entities

| Concept | Purpose/scope/authority | Key/lifecycle | Relationships |
|---|---|---|---|
| **CommunicationIntent / Communication** | One brand's purpose, approved facts, CTA and constraints; the brief and its concrete approved revisions are one concept | ID + immutable revision; draft/review/approved/stale/retired | One brand and publication/purpose; channel representations; equivalence family |
| **ChannelRepresentation** | Channel-specific expression of one approved communication | ID + revision + channel; draft/approved/stale/retired | Pinned content/theme/renderer/fact references; not auto-synchronized after approval |
| **Campaign** | Controlled one-time audience communication program | ID + revision; lifecycle in section 8 | Selection spec, sending authority, content, approval, schedule and recipient records |
| **Broadcast** | The V1 user-facing campaign type | **Not a second lifecycle or duplicate data model** | Campaign with one communication occurrence |
| **Sequence** | Restricted linear workflow optimized for operators | Definition ID/revision; draft/published/paused/retired | Ordered send/wait/condition steps; no separate orchestration engine |
| **SequenceEnrollment** | Membership/reentry identity for a profile in a sequence program | Unique configured enrollment key; active/completed/cancelled/held projections | Links one authoritative execution; does not own a second step cursor |
| **Automation** | Event-driven bounded workflow definition | Definition ID/revision; draft/published/paused/retired | Triggers and typed graph; sequence is a restricted definition kind |
| **AutomationExecution** | Durable authoritative cursor/context for either workflow kind | Execution ID + trigger/enrollment key; ready/running/waiting/paused/completed/cancelled/expired/quarantined | Current node, due time, pinned version, step executions, waits and delivery references |
| **CampaignRecipient** | Frozen selection evidence for an occurrence | Unique campaign occurrence/profile; selection fields immutable after finalization | Operational delivery progress is separate or an explicitly mutable projection |
| **DeliveryPlan** | One subject's coordinated communication occurrence | Unique semantic occurrence claim; candidate/ready/deferred/reserved/in_flight/satisfied/skipped/cancelled/expired/held | Approved routes, decisions, reservations, one primary outbound delivery by default |
| **Delivery** | One intended effect on one channel/endpoint | Permanent semantic key; prepared/in_flight/accepted/rejected/acceptance_unknown/cancelled | Exact payload/representation; attempts and independent outcome facts |
| **DeliveryAttempt** | One HTTP/transport interaction | Attempt ID; prepared/submitted/accepted/definitely_not_accepted/unknown | Stable request or batch key and digest; attempts are not communications |
| **SenderIdentity** | Recognizable, verified sender within a brand and channel program | ID; pending/verified/enabled/paused/revoked | From/reply-to/domain or phone program; provider qualification and legal-sender map |
| **ProviderAccount** | Credential, region/team/account and quota boundary | ID; unqualified/qualified/degraded/paused/revoked | Multiple sender bindings only if approved; does not own contact truth |
| **ProviderCapability** | Evidence of limits and behavior for a qualified route | Provider+API/version+account/region+qualification timestamp | Idempotency retention, batching, status retrieval, suppression and revocation scope, pricing, markets |

### 5.5 Evidence and supporting records

`Event` is a typed fact envelope with event ID, type/schema version, organization, optional workspace/property, subject, source event ID, occurred/received/applied timestamps, causation/correlation, provenance and trust class. Keep raw provider payloads separate from normalized domain events. Global event arrival order is not assumed.

`AuditRecord` captures administrative intent and changes: actor/principal, operation, affected scope, revision before/after, reason and correlation. `DecisionReceipt` captures a particular evaluation: allowed/deferred/denied/held/skipped; reason codes; evidence references; policy and content versions; selected endpoint/channel; pressure and cost decisions; authority epoch. A receipt is not permission for unlimited future sends.

Supporting records include `Approval`, `SendingAuthorityLease`, `PressureReservation`, `SpendReservation`, `WorkflowWait`, `StepExecution`, `InboxEvent`, `OutboxRecord`, `ImportBatch`, `SourceMapping`, and `SourceCoverage`. These exist only because correctness or recovery needs them, not as separately branded product concepts.

### 5.6 Key, time and identity rules

- Use opaque IDs generated once; provider IDs, slugs and email addresses are never primary keys. Include organization scope everywhere and workspace scope on brand records. Enforce matching scope through composite foreign keys, not just nullable workspace filters.
- Store instants in UTC and explicit IANA timezone identifiers for civil schedules. Do not store a fixed UTC offset as a timezone. Record source time separately from authoritative received/applied time.
- Preserve submitted email spelling. Normalize surrounding whitespace and domain case/IDNA consistently. Preserve local-part case for identity matching; use a separate case-folded **conservative duplicate/block fingerprint** to avoid accidental double contact, not to infer identity or permission. Do not strip plus aliases or Gmail dots. V1 quarantines unsupported SMTPUTF8 addresses rather than mangling them.
- Reuse an exact verified identity within the organization; unresolved/ambiguous matches remain restricted. Public form submission cannot overwrite a known person's global attributes or expose whether they exist in another brand.
- An address change never retargets an already frozen delivery. Confirm the new endpoint and record an explicit scoped reauthorization; old pending deliveries are skipped/held, not silently rewritten.
- Mark known shared/reassigned endpoints explicitly. Automatic person merging is prohibited for phone-number, IP, name, or behavioral similarity. A merge is an audited restricted command that conserves withdrawals and pauses affected plans while occurrence claims are reconciled. No bulk merge UI is required for the pilot.
- Store money as integer minor units plus currency; do not compare mixed currencies without an approved conversion snapshot. Budget ceilings are explicit and default to no unapproved spend.
- Cost reservations use a qualified upper bound for the prepared request: encoding/personalization expansion, metered units, output-token bounds and relevant variable provider fees. If a safe bound cannot be established, hold or require a separately approved bounded allocation; do not treat an average estimate as a hard cap. Reconcile actual charges without erasing authorization history. A Texenda spending ceiling bounds its new authorizations; it cannot guarantee a vendor invoice never changes through taxes, fixed account fees, delayed charges or provider error. Account-level contracts/caps and overrun alerts address that external exposure.

### 5.7 Segmentation semantics

A segment is a validated, versioned expression tree using `all`, `any`, `not`, subscription, tag, typed attribute, campaign activity, source and business-event predicates. V1 supports no user SQL, regex programs, JavaScript, or unrestricted joins.

Compile parameterized SQL over authoritative scoped tables and explicitly qualified facts. Missing typed values evaluate `UNKNOWN`, including under `not`; only `TRUE` is selected. Operators use explicit `is_set` / `is_not_set` predicates. Tags and membership existence have normal boolean semantics. Define string comparison/collation once and test it; default exact normalized comparisons, not locale-dependent fuzzy matching.

Relative windows use a pinned evaluation instant. “No purchase in 30 days” means **no qualifying purchase observed in the available, healthy 30-day source coverage**, not proof no purchase occurred. If required source coverage is missing, return `UNKNOWN`/hold instead of promoting absence to evidence. Imported historical facts retain coverage limits. Cross-brand predicates are not available to ordinary campaign segments.

Preview returns interpretation, evaluation time, coverage, sample, candidate count and exclusion estimate. At send resolution, pin segment/compiler versions and use one consistent PostgreSQL snapshot to create recipient rows. Do not use `SKIP LOCKED` to silently omit locked audience members; that construct is for queue consumers. [S21](../09-reference/source-register.md#s21)

For repeatable expensive queries, add indexed fact projections first. A projection carries a source watermark; current grants, withdrawals and safety restrictions always come from the primary authority. Raw provider JSON is not the segmentation API. Segment materialization is deferred until repeated preview/resolution latency or database load crosses Roadmap section 15 thresholds.

**Consequences:** schema/service design can proceed without adopting a provider's subscriber model or inventing a universal endpoint type. **Revisit:** major identity isolation changes, external multi-organization use, unsupported address families, or a new channel require scoped ADRs and tests, not a new master data model.

---


## 5.8 Interaction and delegated-work extensions (later accepted direction)

| Concept | Purpose and authority | Scope / key | Lifecycle | Explicit non-meaning |
|---|---|---|---|---|
| Goal | Human-owned durable outcome and related-object context | Organization/workspace + opaque ID + revision | active/paused/achieved/abandoned/superseded | Not permission, workflow cursor, verified purchase or autonomous mission |
| GoalConstraint | Typed bounds of an intended goal or proposal | Goal revision + constraint key | proposed/active/retired | Free text is not executable policy |
| AssistantPreference | Explicit user preference for explanation/style/defaults | Principal + optional workspace + key/revision | active/retired | Cannot weaken organization or recipient policy |
| Proposal | Reviewable non-authoritative command candidates | ID + immutable ProposalRevision; author/initiator/context | draft/ready_for_review/stale/approved/rejected/superseded | “Approved” does not mean executed or indefinitely authorized |
| ApprovalRequest | Required approver, scope and immutable candidate envelope | Proposal revision + request ID | pending/satisfied/expired/cancelled | Not an approval record |
| Approval / ApprovalRecord | Actual authenticated authority grant bound to a digest/envelope | ID; principal, assurance, time, expiry, use policy | granted/consumed/invalidated/expired | AI or chat history cannot create it; same Approval concept as campaigns |
| InteractionSession | Scoped conversational continuity and object refs | Principal + session ID | active/ended/expired | Not domain truth or long-lived delegation |
| AgentPrincipal | Identifiable built-in intermediary or external machine principal | Organization + opaque ID + issuer/client binding | pending/active/suspended/revoked | Not the human, not a recipient Person, not a provider credential |
| DelegationGrant | Narrow authorization from a human/authority to an agent | ID + revision, principal chain, workspace/resources/commands, budget/time | proposed/active/expired/revoked | Cannot exceed delegator's current effective authority or approve itself |
| AgentRun | Bounded operational run and checkpoints under a grant | ID + delegation ID + invocation key | admitted/running/waiting_approval/paused/completed/failed/cancelled/expired | Not AutomationExecution; no second messaging workflow runtime |
| Task/ProposedAction | A typed command item inside Proposal or an attention item | Proposal revision + item ID | derived from proposal/command result | Not a new project-management task system |
| Plan | Ordered proposal commands and linked goal artifacts | Versioned proposal data initially | proposal lifecycle | A general planning subsystem is deferred |
| Result/Outcome | Recorded command/execution result or observed business outcome | Command/run/receipt/event IDs | facts plus correction events | Observation is not causation |

`Approval` and `ApprovalRecord` are names for one authority record, not competing tables. `Communication` and `CommunicationIntent` remain one brief/revision aggregate. `Sequence` is a workflow-definition kind and `Broadcast` a campaign kind. `Person` never represents an administrative user or coding agent. Astra's development tasks live in the local harness, not in Texenda's product database.

Instruction promotion uses dedicated typed commands: explanation depth → AssistantPreference; send-day rule → publication policy; budget → approved spending policy; campaign exclusion → selection constraint. Imported or generated instructions never promote themselves. Active constraints are deterministic; prose remains explanatory.

A ProposalRevision pins base object revisions and a canonical command-list digest. Approved revisions cannot be edited; correction creates a new revision. Current stricter policy and revocation remain live. An AgentRun does not resume with expired authority; reauthorization creates a new attributable grant/run continuation.
