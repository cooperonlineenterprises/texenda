# Texenda Product & Technical Foundation Specification

**Artifact I · Version 1.0.0 · Issued September 5, 2026**  
**Document ID:** TEX-FND-001  
**Companion:** [Implementation Roadmap & Production Acceptance Plan](Texenda_Implementation_Roadmap_Acceptance_v1.0.md)  
**Accountable owner:** Product Owner, initially the founder of Cooper Online Enterprises  
**Intended use:** Normative input to repository, schema, service, interface, test, and implementation design.

> **Texenda is an email-led audience and communication platform that enables a solopreneur or very small team to maintain permissioned audience relationships through useful, coordinated communication—without operating an enterprise marketing suite.**

## Authority, interpretation, and change control

This specification consolidates the supplied project decisions and resolves the implementation-shaping gaps identified by the decision-closure request. It is the **design baseline**, not evidence that software has been implemented, security-reviewed, legally cleared, or production-qualified. No production accounts, repository, subscriber dataset, or running deployment were inspected for this work.

**MUST / MUST NOT** are binding requirements. **SHOULD** identifies a default that may be changed only with a recorded reason. **MAY** identifies a permitted option, not a V1 commitment. Product rules are Texenda decisions; citations support external technical facts, not claims that a vendor or regulator endorses this design.

Each material decision has exactly one decision status:

| Decision status | Meaning in this baseline |
|---|---|
| **AUTHORITATIVE DECISION** | Preserved from accepted direction, or explicitly resolved and frozen by this specification. |
| **DECISION REQUIRED NOW** | A blocking design question still awaiting resolution. **None remain in this issued baseline.** |
| **REVERSIBLE DEFAULT** | Implement the specified initial choice, behind its stated replacement boundary. |
| **DEFER UNTIL TRIGGERED** | Do not implement the capability before its trigger and acceptance gate. |
| **REQUIRES EXTERNAL VALIDATION** | The architecture is settled; enabling a capability or committing publicly requires specified evidence. |

The infrastructure disposition requested in section 12 and channel disposition in section 7 are **separate classification axes**, not additional decision statuses. An infrastructure item can therefore have decision status `REVERSIBLE DEFAULT` and infrastructure disposition `REVERSIBLE DEFAULT`, while a framework's architectural role can be authoritative.

The Foundation owns product and execution semantics. The Roadmap owns delivery order, test evidence, operational targets, and ADR summaries derived from those semantics. A conflict blocks release and requires correction; neither implementation convenience nor an ADR summary silently overrides the Foundation. Changes to a governing rule require a new ADR, affected-test analysis, data-migration analysis, and a coordinated revision of both artifacts. A dependency upgrade or reversible-default change requires qualification and a decision record, not another product-definition exercise.

**Evidence boundaries.** Current subscriber counts, publication cadence, Kit account topology, production budget, audience jurisdictions, and sequence progress are not established by the supplied context. They are explicit qualification inputs, not assumptions to invent. The validation register at the end assigns gates and safe behavior while evidence is missing.

## Contents

1. [Product definition and boundary](#f01)
2. [Naming and brand architecture](#f02)
3. [Governing principles and invariants](#f03)
4. [Product architecture](#f04)
5. [Canonical domain and data model](#f05)
6. [Consent, eligibility, preferences, suppression, and recipient experience](#f06)
7. [Channel strategy and abstraction](#f07)
8. [Campaign, sequence, and automation semantics](#f08)
9. [Content and message model](#f09)
10. [AI operating model](#f10)
11. [UX and information architecture](#f11)
12. [Technology and infrastructure baseline](#f12)
13. [Provider and integration architecture](#f13)
14. [Security, permissions, and governance](#f14)

---

<a id="f01"></a>
## 1. Product definition and boundary

**Decision status: AUTHORITATIVE DECISION.** Preserve the email-led, small-team product. Selective channels extend its communication model; they do not redefine it as an omnichannel suite.

### 1.1 Users and jobs

The primary users are publishers, creators, owner-operated brands, solopreneurs, and approximately five or fewer routine operators. Technical administrators are secondary users. One person may perform several operational roles; safe operation MUST NOT require a permanent two-person approval staff.

Primary jobs are to acquire subscribers; understand and organize a permissioned audience; compose and publish email; run welcome and follow-up sequences; configure bounded event-driven communication; manage preferences and suppression; understand observed results; and coordinate work across owned brands without pooling their permissions.

The operator should decide **intent, audience, content, and timing**. Texenda absorbs repetitive administration, policy evaluation, duplicate prevention, scheduling, execution, and explanations. It does not remove human responsibility for claims, brand judgment, consent provenance, incidents, or channel suitability.

### 1.2 Scope

| Product classification | Included capability | Boundary |
|---|---|---|
| **CORE PRODUCT** | Audience identities/profiles; subscriptions; consent; preferences; suppressions; tags/attributes; segments; forms; imports/exports; email; broadcasts; sequences; bounded automations; performance reporting | These together replace the useful core of Kit. The first production pilot may precede sequences and automations, but complete Kit retirement may not. |
| **CORE PRODUCT** | Multi-workspace administration, communication equivalence/expiry, basic pressure enforcement, decision receipts, audit, recovery | Correctness foundations exist before the first real send. Rich portfolio views can follow. |
| **NATURAL EXPANSION** | Reusable recipes/templates; AI preparation; communication calendar; contextual onsite placements; qualified web push; cross-channel choose-one policies | Add in dependency order and only behind the same permission and execution model. |
| **OPTIONAL ADJACENCY** | SMS, WhatsApp, native/in-app messaging, narrowly authorized service notifications, joint-brand planning, experimentation | A use-case, legal/provider, cost, and operations gate is required. |
| **OUT OF SCOPE** | Sales pipelines, prospect scraping, cold outreach, CDP-scale behavioral collection, support ticketing, ad buying, ecommerce authority, social publishing, site building, arbitrary workflow code, autonomous marketing agents | Integrate a narrow fact or effect when needed; do not become the adjacent category. |

### 1.3 Portfolio and category

Seed one Organization: **Cooper Online Enterprises**. Initial Workspaces are One Happy Housewife, Homeschool Pickle, Endless Popcorn, Brewologist, Stavium, and Cooper Online Enterprises. Their initially associated properties are respectively `onehappyhousewife.com`, `homeschoolpickle.com`, `endlesspopcorn.com`, `brewologist.com`, `stavium.ai`, and `cooperonlineenterprises.com`. A brand can own multiple properties and publications. These domain names are context, not evidence that DNS ownership has been verified.

Initial operation is a private, single-organization installation. Preserve `organization_id` in data boundaries, but do not ship external-customer tenancy, customer billing, or self-service organization provisioning. Commercial multi-organization operation requires a separate isolation and operations qualification.

Present category: **Email Audience & Automation Platform**. Future category, only when multiple channels are actually useful: **Audience & Communication Platform**.

### 1.4 Durable product truth

Changing a database driver, provider, UI, queue, or AI model must not change who may be contacted, which brand is speaking, what a subscription means, how duplicate effects are prevented, or why an automation continued. Identity recognition is not permission. A successful product increases communication usefulness, not merely send volume.

**Alternatives rejected:** a channel-neutral UI from day one; a wrapper around several independent marketing systems; a generic engagement suite. All increase conceptual or authority ambiguity without serving current routine work.

**Downstream consequences:** section 5 is the sole conceptual vocabulary; email gets the richest first implementation; all future channels qualify against sections 6–8. **Revisit:** only an explicit product-boundary ADR supported by recurring user demand, not a provider's feature release.

---

<a id="f02"></a>
## 2. Naming and brand architecture

| Topic | Decision status | Resolution |
|---|---|---|
| Working master identity | **AUTHORITATIVE DECISION** | Use **Texenda** in design and internal product work. Naming uncertainty does not reopen audience or architecture decisions. |
| Initial descriptor | **AUTHORITATIVE DECISION** | **Email Audience & Automation Platform**. |
| Later descriptor | **DEFER UNTIL TRIGGERED** | Use **Audience & Communication Platform** when non-email surfaces are production-qualified and materially used. |
| Parent endorsement | **AUTHORITATIVE DECISION** | `Texenda by Cooper Online Enterprises` on ownership/about/legal surfaces; ordinary product conversation uses Texenda. |
| Public adoption/registration | **REQUIRES EXTERNAL VALIDATION** | VAL-01: trademark/common-law, similar-mark, domain, registry, linguistic, and market review before irreversible public branding. |
| Technical names | **REVERSIBLE DEFAULT** | Repository `coe-audience-platform`; descriptive internal package/runtime names. Branding is configuration, not a database-key namespace. |

Previously identified **Xenda / PiXENDA** concerns remain part of the clearance brief; this specification neither establishes their legal rights nor declares Texenda clear. Formal review must consider similarity and related goods/services, not exact spelling alone. USPTO guidance explicitly recognizes confusing similarity in sound, appearance, meaning, and related commercial fields. [S22]

Use ordinary product surfaces: Audience, Forms, Messages, Broadcasts, Sequences, Automations, Calendar, Insights, Deliverability, Integrations, Settings. Do not create branded subproducts merely to label navigation.

**Consequence:** internal development may proceed under Texenda while the public brand gate remains closed. URLs, sender identities, RP IDs for authentication, and legal disclosures must be configured independently of the master name. **Revisit:** a clearance result changes presentation and identifiers where necessary, not product semantics.

---

<a id="f03"></a>
## 3. Governing principles and non-bypassable invariants

**Decision status: AUTHORITATIVE DECISION.** The following requirements apply through every supported UI, API, import, administrative action, integration, worker, and AI tool.

| ID | Normative invariant | Implementation/test implication |
|---|---|---|
| **INV-01** | One Texenda domain model owns audience and communication truth. | Provider contacts, analytics, CMS documents, and model output cannot independently grant communication authority. |
| **INV-02** | Shared identity never creates shared permission. | A profile/endpoint match cannot activate another publication, brand, purpose, or channel. |
| **INV-03** | Reachability, identity proof, consent, and preference are distinct facts. | A phone number, browser permission, or successful prior delivery is not a marketing grant. |
| **INV-04** | Every proactive message and personalized placement passes the applicable central policy. | No direct provider-send endpoint; service/auth/test classes use narrow policy branches, not bypass flags. |
| **INV-05** | Applicable denials dominate preferences and historical approvals. | Current opt-outs, blocks, safety holds, authority leases, and expired content are checked at final handoff. |
| **INV-06** | Scope is enforced server-side and structurally in relationships. | Composite scope keys/FKs, authorized repositories, and adversarial endpoint tests; UI filtering is insufficient. |
| **INV-07** | Queues wake work; business state is durable in PostgreSQL. | Dropped/duplicated jobs cannot lose an execution or create another logical effect. |
| **INV-08** | Published campaigns/content/workflows are versioned and immutable. | Edits create revisions; active runs pin versions; approved changes require explicit activation/migration. |
| **INV-09** | Logical occurrences, channel deliveries, attempts, and observations are different objects. | Retries do not create new communications; follow-ups consume additional interruption allowance. |
| **INV-10** | Admission, deduplication, and pressure/spend reservations are atomic. | Two workers cannot independently consume the same remaining slot. |
| **INV-11** | External effects are effectively-once where qualified, otherwise explicitly uncertain and reconcilable. | Unique semantic keys, stable payloads, provider idempotency, and `acceptance_unknown`; never claim universal exactly-once email. |
| **INV-12** | A timeout or outage never authorizes blind provider/channel failover. | Reconcile before another effect; a block or opt-out cannot trigger escape to another channel. |
| **INV-13** | Every consequential effect has a decision receipt and approved authority chain. | Record actor/configuration, revisions, eligibility evidence references, policy version, route, and timing. |
| **INV-14** | AI translates intent; deterministic systems enforce truth. | Models return typed proposals; never direct SQL, provider credentials, consent grants, or policy override. |
| **INV-15** | Recipient trust outranks communication volume. | Expire stale work; suppress duplicates; enforce caps; never flush a deferred backlog in a burst. |
| **INV-16** | Imports/replays do not silently activate automations or weaken denials. | Default `trigger_mode=historical`; negative evidence wins until an explicit valid reconsent. |
| **INV-17** | Successful opt-out acknowledgment means the restriction is durably recorded and applied. | No success response before authoritative mutation and the recovery safety evidence are durable. |
| **INV-18** | Restore/recovery cannot silently revive prior permissions or repeat uncertain effects. | Independent safety journal, deployment send gate, reconciliation, and new execution epoch before resuming. |
| **INV-19** | Publication migration has one active sending authority for each scoped function/cohort. | A Texenda worker checks an authority lease; Kit-side controls must be verified, not assumed enforceable by Texenda. |
| **INV-20** | Test/development environments cannot reach real recipients through production transport. | No production credentials, egress controls, fake providers/Mailpit; `NODE_ENV` alone is not a safety boundary. |
| **INV-21** | Audit immutability is not indefinite retention of personal data. | Append corrections; separate erasable PII; lawful retention/erasure process preserves only justified evidence. |
| **INV-22** | No automatic cross-brand marketing action derives from another brand's behavior. | Shared coordination may delay a send, but cannot supply missing permission, targeting authority, or disclosure. |

“Non-bypassable” describes enforcement through supported application paths and runtime identities. An infrastructure root/DBA compromise is outside that guarantee; least privilege, independent evidence, monitoring, and break-glass controls address that threat. The product must not advertise immunity to a compromised administrator or vendor.

**Revisit:** changes require a governing ADR, failure-mode review, and migration/acceptance impact assessment. No reversible-default change may weaken an invariant.

---

<a id="f04"></a>
## 4. Product architecture

**Decision status: AUTHORITATIVE DECISION.** One modular monolith, one transactional authority, two production execution roles. Separate processes are not separate domain services.

### 4.1 Components and flow

```text
Owned properties / operator UI / trusted integrations
                      |
           authenticated application commands
                      |
  Portfolio -- Identity/Audience -- Permission/Policy -- Content
                      |                    |
       Segmentation -- Campaign/Workflow -- Communication Coordinator
                      |
           PostgreSQL unit of work
      state + evidence + outbox + decision receipt
                      |
         due-work/outbox reconciliation
                      |
                  Worker role
       eligibility + preparation + reservations
                      |
          independent safety/effect journal
                      |
           final current-state handoff permit
                      |
         qualified channel/provider adapter
                      |
             external delivery provider
                      |
     authenticated durable webhook inbox --> normalization
                      |
        delivery facts / safety holds / outcomes / rollups
```

Onsite placements later use a request/decision/render path, not an artificial outbound-send job. They share authorization, content, policy, and explanation concepts where applicable.

### 4.2 Modules and ownership

| Module | Owns | Does not own |
|---|---|---|
| Portfolio/access | Organization, workspaces, properties, publications, memberships, effective principals | Contact consent |
| Identity/audience | People, identities, bindings, profiles, fields, tags, import mapping | Permission inference |
| Permission/policy | Grants, withdrawals, preferences, suppressions, eligibility, pressure-policy definitions | Provider transport |
| Content | Communication briefs, protected facts, approved representations, template revisions | Product/price truth from external systems |
| Segmentation | Typed expressions, compiler, preview, frozen selection evidence | Communication permission |
| Campaign | Broadcast lifecycle, approved selection specification, recipient resolution | Per-recipient provider calls |
| Workflow | Sequence/automation definitions, executions, waits, reentry and cancellation | Queue truth or unrestricted scripts |
| Coordinator | Logical occurrence claims, route plans, priorities, pressure/spend reservations | New consent or speculative identity |
| Delivery/integrations | Provider requests, raw inbox, normalization, reconciliation, property APIs/webhooks | Competing contact/automation database |
| Insights/operations | Derived rollups, observability, evidence views, recovery controls | Send-time eligibility or consent |
| AI assistance | Typed proposals, drafts, explanations, provenance | Policy, facts, or external-effect authority |

Modules communicate through typed commands, query interfaces, and events. The domain depends on ports/types, not Payload, provider SDKs, or an analytics database. Cross-module transactions are allowed because this is one application. Enforce ownership through repository APIs and static dependency tests rather than artificial HTTP calls between modules.

### 4.3 Repository baseline

**Decision status: REVERSIBLE DEFAULT.** Use a pnpm workspace, one lockfile and one coordinated release:

```text
apps/web/                  Next.js + custom Payload operator views + ingress
apps/worker/               due work, delivery, normalization, imports, reconciliation
packages/contracts/       public API/event schemas; versioned command DTOs
packages/core/            domain modules, commands, policies, port definitions
packages/persistence/     Drizzle domain repositories, transactions, migrations
packages/integrations/    providers, storage, AI and external adapters
packages/payload-platform/ Payload config factory, auth/config adapters, coarse jobs
specs/                    these two documents; future accepted revisions
infra/                    container/PaaS manifests, deployment and recovery scripts
tests/                    contract, integration, property, failure, migration, UX tests
```

Both applications are composition roots. `core` imports `contracts` but never an application. Infrastructure implements core ports. Payload configuration receives command handlers rather than importing application startup code. Shared UI is extracted only when actual reuse warrants it. Do not create an internal package for every entity.

### 4.4 Payload and persistence: close the transaction ambiguity

Payload owns operator authentication/session records, its administrative shell, ordinary non-authoritative configuration drafts, media metadata, and generated views where useful. **Safety-critical current state and activated configurations are Texenda-owned transactional tables.** A Payload draft is not an active sender policy, campaign approval, subscription, or automation cursor.

Use distinct migration/table ownership for Payload-managed tables and Texenda-owned tables in the same PostgreSQL database. All domain commands requiring atomicity use one explicit Drizzle unit of work over Texenda tables. Payload authentication is resolved before the command and mapped to a current domain principal/membership; disabling a member in the domain immediately removes command authority.

Publishing a Payload-managed content/configuration draft copies an immutable, validated revision into Texenda authority through a command. The copy and its activation/audit/outbox commit together in the domain transaction. A stale “published” UI badge is repaired from domain state, not accepted as authority. This avoids assuming that independent Payload and Drizzle calls share a transaction. Where code does use multiple Payload Local API operations transactionally, its `req` transaction context must be propagated as documented. [S01, S03]

Payload permits custom PostgreSQL schema additions; validate the chosen adapter and migration integration in VAL-03. Do not maintain two uncoordinated migration systems or let development schema-push alter production. [S02]

**Forbidden direct access:** UI/server-action handlers, AI tools, SDK callers, provider callbacks, and ordinary Payload hooks must not mutate domain tables directly. They invoke commands. Authorized read models may query through scoped repository interfaces. DDL/data-repair scripts use a separate migration or break-glass role.

### 4.5 Commands, events and transaction boundaries

Representative commands include `RequestSubscription`, `ConfirmSubscription`, `WithdrawPermission`, `PlaceSafetyHold`, `PublishCommunication`, `ApproveCampaign`, `ScheduleCampaign`, `ResolveCampaign`, `EnrollSequence`, `PublishAutomation`, `RecordBusinessEvent`, `DecideDelivery`, `PrepareHandoff`, `RecordProviderOutcome`, `PauseScope`, and `TransferSendingAuthority`.

Every command carries a principal, organization/workspace context, command ID, idempotency key where externally retried, expected revision where relevant, and correlation/causation IDs. Authorization is derived from the principal, not accepted from user-supplied workspace claims.

Within one domain transaction: validate authority and inputs; lock/version-check affected rows; change authoritative state; append the relevant evidence; create outbox records; commit. No provider request, AI call, file fetch, or external webhook runs inside that transaction.

Compound mutations use a canonical lock order: applicable authorization/budget rows first, then coordination-subject rows, endpoint-safety rows, execution/wait rows, and delivery-plan/effect rows; sort multiple keys within a class. Acquire only the classes needed by the command. A worker's initial queue/lease claim commits before entering a domain transaction. Do not acquire an earlier class after a later class; abort and retry the entire transaction with the same command/effect identities when a new dependency or serialization conflict is discovered. Expensive reads/rendering occur outside lock-held sections and are version-rechecked. Permission mutations and goal-event/wait transitions serialize through the same applicable subject/endpoint safety boundary as final permits. This order is an implementation constraint, not a reason to hold a global lock across network work.

A **domain event** records an accepted internal fact. An **integration event** is a minimized, versioned projection deliberately exposed externally. A **provider event** is externally supplied evidence, authenticated and normalized before it can change internal state. An arbitrary browser event must not become a trusted purchase or consent event.

The outbox and inbox are at-least-once mechanisms. Consumer-specific deduplication is required. Side effects are disabled during historical replay unless an explicit, authorized backfill specifies them. Recovery sweepers find due executions, undispatched outbox records, and expired leases independently of queue contents.

### 4.6 Independent safety journal and restoration boundary

A PostgreSQL point-in-time restore can rewind a legitimate opt-out or a send accepted after the restored timestamp. Provider idempotency windows do not solve that indefinitely. Therefore **an independent, append-only recovery journal is required before production sending**, using the object storage already needed by the platform, not a new messaging service.

Journal two classes synchronously at their safety boundary: (a) accepted restrictive inputs—opt-outs, complaints, erasure/safety restrictions—and (b) outbound handoff intents with stable semantic/provider keys and payload digest. Provider outcomes and other audit records may follow asynchronously. Encrypt sensitive reconciliation fields; retain only what recovery needs. A journal intent alone never authorizes sending and may conservatively indicate an unknown effect.

For revocation, apply the database denial immediately; journal it idempotently before acknowledging success. If journal persistence fails, keep the denial, return a retryable failure, and hold outbound sending until pending restrictive entries are durably covered. Provider safety webhooks likewise require durable recovery evidence before acknowledgment. For outbound work, no HTTP handoff occurs until its intent is journaled and a current permit is acquired. A journal entry whose database transaction never completed is harmlessly conservative during recovery.

The journal is recovery evidence, **not a second audience source of truth**. Recovery replays restrictive evidence into the restored authority, reconciles uncertain effects, and requires an explicit new deployment execution epoch. An external deployment-level send-disable control is not stored solely in the database being restored. If evidence is incomplete, sending remains held. See Roadmap section 17 for restore tests.

**Downstream consequences:** both processes use the same module contracts; safe mutations and effect evidence precede queue sophistication. **Revisit:** process/service extraction only after measured independent scaling, isolation, or availability needs; never to make the diagram look distributed.

---

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

Preview returns interpretation, evaluation time, coverage, sample, candidate count and exclusion estimate. At send resolution, pin segment/compiler versions and use one consistent PostgreSQL snapshot to create recipient rows. Do not use `SKIP LOCKED` to silently omit locked audience members; that construct is for queue consumers. [S21]

For repeatable expensive queries, add indexed fact projections first. A projection carries a source watermark; current grants, withdrawals and safety restrictions always come from the primary authority. Raw provider JSON is not the segmentation API. Segment materialization is deferred until repeated preview/resolution latency or database load crosses Roadmap section 15 thresholds.

**Consequences:** schema/service design can proceed without adopting a provider's subscriber model or inventing a universal endpoint type. **Revisit:** major identity isolation changes, external multi-organization use, unsupported address families, or a new channel require scoped ADRs and tests, not a new master data model.

---

<a id="f06"></a>
## 6. Consent, eligibility, suppression, preferences, and recipient experience

**Decision status: AUTHORITATIVE DECISION.** Communication authority is explicit, contextual, revocable, and evaluated independently of transport reachability.

### 6.1 Permission tuple and evidence

For marketing, an effective grant identifies:

```text
organization + workspace + publication/purpose + channel
+ subject/profile + authorized endpoint binding + disclosure version
+ proof/source + validity + consent revision
```

Email subscriptions imported from Kit remain **email-only**. A web-push permission prompt, an SMS number, a purchased product, a tag, and a successful previous delivery do not grant unrelated marketing authority. Service messages use a separate, allowlisted resource/purpose authorization, not an active marketing subscription.

Consent evidence records the actual displayed disclosure, form/variant, source property, request/confirmation times, source-system identifiers, principal, proof method and processing purpose. Store only justified network evidence. Never backfill missing historical proof with a current disclosure or manufacture an opt-in timestamp from an import date.

**REVERSIBLE DEFAULT:** new public email subscriptions use double opt-in. A qualified publication may use another expressly approved policy after VAL-02 review. Public subscription requests are non-enumerating and abuse-limited; confirmation messages themselves pass the system/fulfillment policy and do not contain unrelated marketing.

### 6.2 Subscription and reconsent transitions

| Input | Authoritative result | Prohibited side effect |
|---|---|---|
| Public signup with required confirmation | Pending request; bounded confirmation message | No marketing enrollment before confirmation |
| Valid confirmation | Scoped grant and active channel subscription | No grants for other publications/brands/channels |
| Duplicate confirmation | Return current result; no extra grant or trigger | No repeat welcome |
| Publication/channel opt-out | Withdrawal and withdrawn current membership; cancel affected pending marketing | No alternate-channel escalation |
| Brand/portfolio stop | Broader withdrawal across the covered known scope | Do not invent unknown identity bindings |
| Ordinary signup after broad stop | Pending fresh reconsent with the prior restriction explicitly acknowledged in the confirmation context | Do not remove broad restrictions for sibling subscriptions |
| Fresh confirmed reconsent | A narrowly scoped grant may explicitly supersede specified recipient withdrawals for that same endpoint/purpose | Never releases complaint, endpoint-invalidity, or provider safety holds |
| Old confirmation issued before a later withdrawal | Reject as stale | Never resurrect authority through an old token |
| Safety-hold release | Removes only that named operational block after review | Does not manufacture a fresh consent or reactivate unrelated subscriptions |

To permit a person to rejoin one publication after a brand-wide opt-out without reviving every old subscription, a fresh grant may record **explicitly acknowledged withdrawal IDs it supersedes only within its own narrow scope**. Later withdrawals still win. This exception mechanism applies to recipient choice only, never to safety/provider restrictions.

A removed/revoked grant is never silently reactivated by import, API upsert, a provider suppression removal, or an operator changing a tag. Existing cancelled workflows do not resume on reconsent; a new qualified trigger or explicit enrollment creates a new execution identity.

### 6.3 Message classes

| Class | Required authority | Pressure treatment |
|---|---|---|
| `marketing` | Active scoped subscription/grant and all applicable safety checks | Full brand/portfolio/channel caps |
| `requested_fulfillment` | A particular recent authenticated or verified request, approved resource and endpoint | Separate bounded abuse/dedup limits; cannot carry unrelated promotions |
| `service` | Allowlisted resource relationship and approved message purpose | Service policy and rate limits; no arbitrary “urgent” bypass |
| `operator_auth` | Account-specific login/recovery/verification request, approved template and sender | Strict account/endpoint abuse limits; no marketing |
| `test` | Authorized operator, approved test purpose and preverified internal allowlist | Test quota; conspicuous marker; no audience-wide addressing |

All classes use the same entry point. Payload's automatic email adapter must route auth/recovery through the corresponding domain command and worker; the web process has no email-provider credentials. Classification of mixed commercial/service content is a legal/policy matter under VAL-02; labeling a campaign `service` does not make it so. FTC guidance distinguishes messages by primary purpose and requires clear commercial opt-out behavior. [S14]

### 6.4 Suppression and propagation

| Restriction | Default scope and behavior |
|---|---|
| Confirmed permanent email-address failure | Block that endpoint across the organization; retain subscriptions as historical facts. Do not mark phone/push endpoints invalid. |
| Temporary/ambiguous bounce | Retry or hold according to the qualified error class; never convert a transient code to permanent invalidity by convenience. |
| Spam complaint | Block marketing on the email endpoint organization-wide. Where the identity is reliable, add a conservative person-level marketing safety hold. Preserve the source and reason; this is not fabricated revocation of every other legal consent. |
| Provider suppression | Mirror its actual account/team/region/program scope as an additional denial. Never remove it merely because a local subscription is active. |
| Publication withdrawal | Blocks the specified publication/channel/endpoint authority; presentation may offer a broader stop. |
| Brand stop / portfolio stop | Blocks covered marketing across the chosen scope and reliably linked endpoints. New later identity bindings inherit relevant known broad restrictions conservatively, not new permissions. |
| Push invalidation or device logout | Retire/disable the binding; shared devices must not continue receiving prior-user personalized notifications. |
| SMS/WhatsApp opt-out | Enforce the qualified legal and provider-program scope, which may exceed a Texenda workspace; acknowledge only as permitted by that channel's rules. |
| Administrative investigation/unknown imported proof | Scoped safety hold until evidence is reviewed; no automatic alternate route. |

An endpoint block, recipient withdrawal, and complaint are materially different; retain separate reason types. No routine “send anyway” action exists. A correction requires elevated rights, step-up authentication, evidence, and audit, and cannot overrule a recipient's current refusal.

**REQUIRES EXTERNAL VALIDATION — VAL-02/VAL-04/VAL-07:** jurisdictions, legal-sender scope, retention, channel disclosures, and provider revocation rules. Store effective-dated policy and sender-program mappings. Twilio's current policy is an example of sender/purpose-specific consent and opt-out obligations that a phone adapter must implement; it is not a generic consent source. [S16]

### 6.5 Eligibility decision contract

```text
EvaluateCommunication(input, current_primary_state) ->
  ALLOW   { short_lived_permit, evidence_refs, reservations }
  DENY    { reason_codes, terminal_for_this_occurrence }
  DEFER   { reason_codes, next_eligible_at, expires_at }
  HOLD    { reason_codes, required_resolution }
  SKIP    { reason_codes: duplicate | expired | completed_goal | ... }
```

Evaluate in this order: principal and migration authority; scope and publication/purpose; approved/current content; endpoint binding/reachability; current grants/withdrawals; safety/provider holds; goal/cancellation state; equivalence claim; recipient preferences/quiet hours; pressure/priority; sender/provider readiness; spend/rate constraints. Collect all safe-to-disclose reasons, but do not leak unrelated brand information. Previews have no sending authority.

Unknown required proof, unknown source coverage for a safety-sensitive exclusion, or uncertain provider acceptance returns HOLD, not ALLOW. Provider outages and temporary limits return HOLD/DEFER. Retrying a permanently ineligible occurrence cannot turn it eligible without a legitimate state transition and, when necessary, new approval.

A final permit is acquired under a short transaction using current primary state and a deployment execution epoch. **If a withdrawal commits before permit acquisition, handoff is denied. If withdrawal commits after a valid handoff permit, the in-flight request may complete.** Workers revalidate immediately before calling the provider and cancel anything not yet handed off, but Texenda cannot make a remote provider call atomic with a local opt-out or recall an accepted message. This is the explicit linearization boundary, not a promise of impossible zero-race delivery.

### 6.6 Preferences and unsubscribe experience

Preference precedence is the restrictive intersection of law/provider rules, organization safety policy, recipient broad limits, brand policy, publication promise, recipient specific preferences, and campaign/workflow configuration. Recipient channel ranking orders only already-eligible options. An invalid preferred channel does not authorize another channel unless the recipient and approved plan permit it.

Use a brand-branded page from each message. It must identify the publication/channel and offer an immediate scoped stop, plus a plainly labeled brand-wide marketing stop. Portfolio-wide stop is available with explicit scope wording. **Stopping marketing must not require login or extra identity verification.** Authentication may be required to reveal cross-brand subscriptions, add permission, expose PII, or change unrelated settings—not to obstruct an opt-out. An opaque recipient-bound capability can authorize a blind broader denial without revealing the recipient's other relationships.

Email headers implement RFC 8058: HTTPS endpoint, prescribed POST value, DKIM coverage of both unsubscribe headers, no login/cookies requirement, no redirect. GET displays a safe confirmation/preferences page and does not change state merely because a scanner followed the link. POST applies the named denial idempotently while already withdrawn. A later valid request after fresh reconsent can withdraw again. Unsubscribe tokens remain usable for the justified life of the message/retained subscription; they do not expire after a short login-token window. [S12] Do not use the token itself as a permanent request-idempotency key that would prevent a later valid withdrawal after reconsent. Deduplicate an already-applied request/current denial while preserving the ability to record a new withdrawal.

Tokens disclose no plaintext personal data, are purpose-bound, and survive key rotation through retained verification keys or opaque server-side lookup. Forwarded messages can permit an opt-out; they must not permit reading profile data or granting consent. Export/portfolio-edit capabilities are separate.

### 6.7 Frequency, priorities and expiry

**Decision status: AUTHORITATIVE DECISION** for layered coordination, atomicity and precedence. **The numeric defaults below each have decision status REVERSIBLE DEFAULT.** They are initial safety settings, not empirically optimal frequencies or legal safe harbors.

| Default ID | Initial setting | Revision boundary |
|---|---|---|
| **POL-01** | Maximum one discretionary marketing interruption per brand per rolling 24 hours | Organization-approved policy; no per-campaign bypass |
| **POL-02** | Maximum two marketing interruptions per known person across the portfolio per rolling 24 hours; minimum four-hour spacing | Explicit organization/recipient policy; first run in shadow against actual publication promises |
| **POL-03** | Additional interruptive-channel bucket: maximum one combined push/SMS/WhatsApp interruption per rolling 24 hours | Qualify before those channels go live; may be tightened by recipient |
| **POL-04** | Every publication records its promised cadence; missing cadence blocks activation | Daily/weekly promise can have an explicit approved civil-calendar schedule; cannot silently bypass portfolio policy |
| **POL-05** | Discretionary email defaults to a 24-hour dispatch window; it expires rather than backlogs after that | Operator may approve a different finite window; offer validity is always an upper bound |
| **POL-06** | Default preferred marketing hours: 08:00–20:00 in a recipient-supplied timezone, otherwise the configured workspace timezone for email | Labeled fallback, not an inferred location; regulated channels require a separately qualified rule |

Before enforcing inherited caps, replay real intended publication schedules in shadow mode. A recipient's deliberately chosen daily publications must not be quietly broken by a new default. Resolve conflicts through an explicit organization/recipient cadence policy; do not secretly raise limits or silently drop promised editions. Until resolved, hold the affected schedule at approval and explain the conflict.

Priority classes: requested/service fulfillment under its own authority; promised scheduled publications; explicitly requested time-sensitive alerts; ordinary lifecycle marketing; discretionary promotion. Campaign versus automation is **not** a priority distinction. Within a class, use a deterministic ordering of expiry, ready time, least recently served eligible brand, and stable ID. Fairness prevents a busy brand from indefinitely starving another. Operators cannot relabel promotion as service to win arbitration.

Reservations count provisionally until acceptance or definitive non-acceptance. Accepted sends consume interruption allowance; unknown acceptance consumes it conservatively. Provider retries reuse a delivery and reservation; a genuine follow-up adds an interruption. A confirmed failure can release the transport interruption reservation where qualified, but the logical occurrence and dedup trail remain. Passive onsite impressions use separate impression/dismissal caps; they do not reset outbound allowance.

Global coordination is limited to reliably known identities. It does not justify fingerprinting anonymous devices. A brand operator receives “deferred under portfolio policy,” not another brand's interests, purchase history, or campaign details.

### 6.8 Equivalence and cross-brand safeguards

An equivalence family means several approved representations express the same underlying communication. Its occurrence key distinguishes a particular issue, purchase event, guide request or reminder opportunity. Editorially similar copy does not by itself imply equivalence; an AI similarity score cannot create or remove a claim.

Default occurrence uniqueness is organization + brand + equivalence family + occurrence key + coordination subject. A protected endpoint fingerprint additionally prevents duplicate contact to a shared/aliased destination. A planned email and push share a logical occurrence but still have distinct effect keys and interruption accounting. Multi-device push defaults to one verified preferred device, not all devices.

Portfolio planning may link separate brand campaigns with an explicitly approved cross-brand equivalence group. Each child retains its own permission, sender, audience, content and approval. No pooled audience or automatic source-brand-event-to-target-brand-send exists in V1. An invitation to another brand is not enrollment in it.

**Consequences:** the basic coordinator precedes pilot delivery, not merely multichannel rollout. **Revisit:** numeric policy changes are reversible, versioned and previewed; consent/authority semantics require a governing ADR. Legal uncertainty blocks the affected channel/use case rather than broadening permission.

---

<a id="f07"></a>
## 7. Channel strategy and abstraction

**Decision status: AUTHORITATIVE DECISION.** One audience/workflow system may use several qualified channels; channels retain their distinct permission, delivery, content and observation semantics.

| Channel/purpose | Channel disposition | Decision status | Required qualification |
|---|---|---|---|
| Email | **FIRST-CLASS NOW** | **AUTHORITATIVE DECISION** | Core end-to-end safety, rendering, sender and provider gates |
| Contextual onsite messaging | **DESIGN FOR NOW, BUILD LATER** | **DEFER UNTIL TRIGGERED** | One property with a defined placement/use case, privacy basis, accessibility/performance test and fail-soft behavior |
| Web push | **DESIGN FOR NOW, BUILD LATER** | **DEFER UNTIL TRIGGERED** | Recipients request a timely alert; browser/origin/device tests; endpoint lifecycle; purpose consent; interruption caps |
| SMS | **REVISIT WHEN DEMAND EXISTS** | **DEFER UNTIL TRIGGERED** | High-value repeated use case, actual geography, consent evidence, registered sender program, STOP/reply operations, explicit spend ceiling |
| WhatsApp | **REVISIT WHEN DEMAND EXISTS** | **DEFER UNTIL TRIGGERED** | Supported market/category, templates/service-window policies, permission, reply ownership and provider qualification |
| Native push/in-app | **REVISIT WHEN DEMAND EXISTS** | **DEFER UNTIL TRIGGERED** | An actual app/account lifecycle; authenticated subject/device bindings; logout/reassignment testing |
| Cold outreach, social DMs, voice campaigns, ad audiences | **DO NOT PURSUE** | **AUTHORITATIVE DECISION** | Outside the product boundary |
| Transactional/service | Not a channel | **AUTHORITATIVE DECISION** | Purpose/resource authorization applied to an eligible channel; only narrow approved uses |

Push must not require an email address. Technical browser permission and the chosen brand/topic are separate facts. Apple's documented iOS/iPadOS Web Push behavior involves Home Screen web apps and direct user interaction; pilot the actual audience/browser mix rather than assume universal support. [S17]

Onsite has two modes: anonymous contextual selection from the current page, and known-recipient personalization under approved processing/identity rules. Email consent alone does not authorize browser tracking. Use defined inline/dismissible placements, not a site builder or aggressive overlay system. The website continues normally if Texenda fails.

Every new channel has a qualification record: approved use case; geography; purpose/consent wording; sender/program ownership; supported capabilities; content limits; cost/rate behavior; inbound opt-out and replies; monitoring owner; retention; incident plan; tested adapter version. Without qualification its configuration may be drafted but its dispatch is disabled.

### Supported coordination semantics

1. **Single outbound channel:** the default for each occurrence.
2. **Passive onsite companion:** optional and independently impression-limited; no automatic extra outbound contact.
3. **Choose one approved channel:** later, deterministic preference/policy selection among eligible representations. AI may recommend the policy but does not select a route at runtime.
4. **Confirmed-failure fallback:** later, only from definitive non-acceptance, with separate valid channel permission and explicit plan authority.
5. **Outcome-based follow-up:** a separately approved step/occurrence with its own count, spacing, expiry and cancellation. It is not a provider retry.

Never use non-opening as proof of non-receipt, and never escalate because of unsubscribe, complaint, invalid consent, or a provider policy block. Unknown acceptance pauses a plan. A business outcome such as verified purchase can cancel all equivalent pending promotions.

**Consequences:** email-only implementations populate shared identifiers now but do not build empty channel administration screens. **Revisit:** a channel moves to first-class only after VAL-07 and its Roadmap gate; lack of demand is a valid reason never to implement it.

---

<a id="f08"></a>
## 8. Campaign, sequence, and automation semantics

**Decision status: AUTHORITATIVE DECISION.** Durable business state is separate from queue state and provider observations. One bounded workflow executor serves sequences and automations.

### 8.1 Three independent state planes

| Plane | Authority | Examples |
|---|---|---|
| **BUSINESS STATE** | Texenda transactional domain | Campaign revision/approval; frozen selection; execution cursor; cancellation; delivery plan; occurrence claim |
| **QUEUE / WAKEUP STATE** | Replaceable execution adapter | Payload job ID, retry count, lease, next poll; not proof a campaign completed |
| **PROVIDER DELIVERY STATE** | Provider evidence normalized by Texenda | Accepted request, delivered observation, bounce, complaint, delay, unknown acceptance |

A later complaint does not erase the historical fact that a request was accepted or delivered. Store independently timestamped facts rather than a single scalar status that loses important history.

### 8.2 Campaign lifecycle and approval

```text
draft -> in_review -> approved -> scheduled -> resolving -> ready -> dispatching
                                                              |           |
                                                              +--paused<--+
                                                                          |
                                                   dispatch_complete <----+

Any eligible pre-completion state -> cancelling -> cancelled
Validation/definition fault -> failed
Uncertain effect or unresolved evidence -> needs_attention
```

`dispatch_complete` means every candidate plan is terminal for dispatch. It does not mean inbox delivery, reading, or conversion. Maintain outcome `clean` or `with_errors`. An unknown acceptance prevents clean completion. An operator may explicitly close unresolved work as `closed_with_uncertainty`; its dedup tombstones remain, late evidence can attach, and automation must not interpret this as successful delivery.

Approval binds an immutable campaign revision, communication/representation revisions, sender, publication/purpose, segment/compiler versions, schedule window, tracking, primary channel, permitted alternatives, per-recipient contact maximum, candidate ceiling, monetary ceiling and current authority epoch. Editing any bound item invalidates approval. A tighter later safety policy remains effective without reapproval; a looser policy cannot expand the approved contact/channel/spend envelope.

**REVERSIBLE DEFAULT:** scheduled broadcasts resolve audience rules near the send window. Approval explicitly states that membership is evaluated then, not fixed by the earlier preview. The initial candidate ceiling defaults to the last preview's candidate count and must be shown/accepted. If resolution exceeds it, hold for reapproval—never silently truncate, auto-expand, or choose a random subset. A fixed-snapshot mode is available for operators who need an exact approved recipient set.

Snapshot construction uses a consistent database view, stages recipient records, and atomically marks the resolution run complete. No send begins from a partial or failed resolution. A practical initial timeout is 15 minutes; a timed-out run is discarded or resumed under the same valid snapshot only when the implementation can prove consistency. Do not page a changing audience and call it an immutable snapshot.

Freeze recipient/profile/endpoint selection and personalization inputs at final resolution/preparation. Before handoff, current eligibility can remove a recipient but cannot silently add a new one or retarget a changed endpoint. Content freshness and campaign expiry are rechecked.

### 8.3 Semantic keys

```text
campaign occurrence:
  campaign_id + occurrence_id + coordination_subject

workflow communication occurrence:
  execution_id + stable_node_id + occurrence_number + coordination_subject

explicit duplicate-equivalence claim:
  organization + approved_equivalence_scope + equivalence_family
  + business_occurrence_key + coordination_subject

channel delivery:
  delivery_plan_id + channel + endpoint_binding_version + effect_role

attempt / provider request:
  delivery_id (or immutable batch_id) + qualified provider-account namespace
```

IDs are not derived from message text, queue attempts, current contact email, or renderer output. A transient retry uses the **same** logical delivery and immutable provider request key/payload. An intentional resend is a new explicitly approved occurrence, not an edit to defeat deduplication. Person merges pause affected plans and reconcile old subject aliases before another claim is admitted.

### 8.4 Dispatch protocol

1. Claim eligible work with a short lease/fencing version; bulk workers use `SKIP LOCKED` only for work claiming. [S21]
2. Under subject/scope locks, evaluate the current policy and claim semantic occurrence, pressure capacity and budget. Create a prepared Delivery with exact endpoint, payload digest and revision references. Commit.
3. Persist the handoff intent in the independent recovery journal. If this fails, do not send.
4. Acquire a short-lived final handoff permit in a second short transaction; recheck current restrictions, cancellation, expiry, deployment epoch, lease/fencing version, reservations and prepared digest. Mark in-flight and commit.
5. Call the qualified provider immediately with the immutable payload and key. No database lock is held across HTTP.
6. Record acceptance, definitive rejection, or uncertainty; append observations and outbox records. Finalize/release reservations according to proven outcome.
7. Reconcile delayed events and missing responses independently of campaign worker success.

A lease expiry is **not** proof the old worker did not call the provider. In-flight effects are never reassigned for a blind resend. Fencing protects database transitions, while qualified provider idempotency protects repeated remote requests; neither is a magical distributed transaction.

**REVERSIBLE DEFAULT:** send individual messages in the pilot. Add batches only after throughput evidence and batch contract tests. A batch freezes ordered membership, per-item digest, sender/account, and one request key. If an item is withdrawn before submission, abandon that unsubmitted batch and prepare a new one. After possible submission, do not change membership or split/reissue ambiguous items. A whole-request validation error is treated as definitely-not-accepted only when the provider contract proves that behavior.

### 8.5 Retry/error policy

| Error | Result |
|---|---|
| Invalid recipient syntax/content/schema | Permanent failure; no automatic retry |
| Verified permanent mailbox failure | Endpoint block; cancel matching pending delivery |
| Authentication, sender verification, or account policy rejection | Hold/pause route and alert; no alternative account escape |
| Rate limit | Qualified `Retry-After` or bounded backoff+jitter; recheck eligibility and expiry |
| Temporary infrastructure error | Bounded retry while still valid, using stable request identity |
| Known no-request-transmitted failure | Safe retry, still under final gate |
| Timeout/reset after request may have been accepted | `acceptance_unknown`; reconcile/reuse same qualified idempotency identity; no new payload/key |
| Conflicting idempotency payload | Quarantine programming/configuration fault; never fix by silently creating a new key |

Resend documents idempotency support for email and batch requests with a 24-hour retention window. Internal occurrence/effect deduplication must outlive that provider window. Do not retry an uncertain old request after its qualified window merely because an attempt limit remains. [S06]

**REVERSIBLE DEFAULT:** maximum six automatic transient attempts with jittered increasing waits, never beyond message expiry or the provider's safe idempotency window. Retry budgets are settings, not authority to keep contacting a recipient. If evidence remains unresolved, hold and surface it. Provider-specific classifications must be contract-tested.

### 8.6 Pause, cancellation and recovery

Pausing stops new permits and claims. Cancelling marks pending plans terminal and stops further workflow actions; in-flight provider requests may complete. Resume performs live eligibility and expiry checks and preserves minimum spacing. It does not flush all overdue work.

An organization/workspace/sender/provider kill switch prevents new permits. A separate deployment send-disable gate survives restoring an old database. Safety ingestion and opt-out handling remain available when outbound sending is disabled.

A restore starts in recovery hold: compare backup time, authority epochs and independent journal coverage; replay all restrictive evidence; reconcile every possibly accepted handoff; rebuild derived counters; invalidate old leases/permits; inspect scheduled work; then issue a new live epoch after explicit approval. Unknown effects remain claimed/quarantined. No automatic provider failover exists.

### 8.7 Sequences and bounded automations

A sequence is a restricted workflow definition with linear steps; an automation adds event triggers and branches. **There is one authoritative executor and one cursor model.** `SequenceEnrollment` identifies membership/reentry; its displayed progress comes from the associated execution and step records.

V1 primitives: send approved communication; wait duration; wait until civil/absolute time; condition/branch; add/remove tag; set an allowlisted typed profile attribute; enroll/cancel a sequence; emit a typed event; wait for event with timeout; stop. Subscription changes require a valid proof-bearing permission command; there is no generic automation action “grant consent.” Approved outbound webhooks are an integration feature, not arbitrary URLs supplied by event content.

No arbitrary code, SQL, loops, unbounded recursion, parallel joins, autonomous channel selection, or cross-brand marketing triggers. Event-produced cascades have a correlation depth ceiling and unique trigger keys so tag changes cannot create an unbounded cycle.

Default reentry: one active execution per profile/program, and no automatic replay of a completed enrollment. A program may explicitly permit new executions for distinct business occurrence keys; repeatable marketing requires a visible reentry/cooldown policy. Merely publishing a new version does not restart subscribers.

Publishing creates immutable definitions with stable node IDs, schema version, handler compatibility and limits. Existing executions pin their definition/content revisions. New enrollments use the active version. Migrating existing runs requires a dry-run cursor/node mapping, dedup preservation, consent recheck and explicit approval; missing mappings are quarantined. Do not edit old definitions in place.

### 8.8 Step transitions, waits and timing

Each step transition is transactional: acquire subject coordination and execution/wait rows in the canonical lock order; verify expected cursor/revision; claim a unique step execution; apply domain changes or create a DeliveryPlan/outbox; advance cursor or establish wait; commit. Duplicate wake-ups become no-ops.

A send step advances on **qualified provider acceptance**, not a queued job, delivery observation, or email open. Acceptance uncertainty holds the run. Permanent ineligibility/expiry defaults to stopping the marketing run unless an approved explicit branch says otherwise. Pressure deferral keeps the same occurrence and does not advance.

Duration waits after a message are measured from actual acceptance, preventing a downtime catch-up burst. Absolute waits use the configured instant; if already expired, execute the explicit expired branch rather than immediately emitting multiple missed messages. Civil schedules store timezone and rule: spring-forward gaps move to the next valid instant; repeated fall-back times run once at the first occurrence. Email may use a labeled workspace-timezone fallback; regulated channels may not guess recipient jurisdiction/timezone.

To prevent lost event wake-ups, appending a subject's domain event and registering/claiming its waits use the same subject coordination lock and per-subject committed sequence. A wait records its lower event bound, predicate, deadline and timeout node. Registration checks already-recorded qualifying events before sleeping. Matching event and timeout transitions race on the same wait/execution version; exactly one branch wins. The default event deadline is based on the event's authoritative domain recording time, not an untrusted backdated timestamp. Late events remain historical facts and cannot retroactively undo an external effect.

Before handoff of goal-sensitive promotions, recheck the authoritative completion state and source-health watermark. “Has not purchased” is not true when required purchase ingestion is known stale. No response/open-based cross-channel escalation is supported.

**Consequences:** queue/workflow/provider replacement does not change progress or effect keys. **Revisit:** parallel joins, sophisticated signals, very high waiting cardinality or recurring recovery burden may justify a new execution adapter, but not moving consent or occurrence authority into it.

---

<a id="f09"></a>
## 9. Content and message model

**Decision status: AUTHORITATIVE DECISION.** Use a lightweight communication brief plus independently approved, typed channel representations. Keep ordinary email authoring direct.

```text
Communication intent / purpose
     + approved facts, offer, CTA, validity and disclosures
     + brand-context revision
                 |
        channel-specific representation revisions
        email | onsite | push | qualified future channels
```

An operator may start in the email editor. Texenda derives the minimum brief from the draft: purpose, publication, approved links/offers, required variables, expiry and brand. Do not force a second abstract authoring exercise for a newsletter.

**REVERSIBLE DEFAULT:** React Email renders email; its editor is the initial visual-authoring dependency behind `EmailDocumentCodec`. The official editor exposes structured JSON and email-oriented rendering/export facilities, but its exact package version, license/dependencies, Payload integration and rendering fidelity require VAL-03 qualification. [S05] If qualification fails, retain React Email with a small fixed-block composer; do not replace the content/approval model or stall identity work for a visual editor.

Store editor JSON with its schema/codec version, plus compiled HTML/plain-text template, subject/preview templates, renderer version, asset/link manifest and hashes. Do not execute arbitrary uploaded React/JavaScript or template code. Templates contain approved blocks: text, heading, image, button, divider, callout, article/recipe card, and immutable compliance-footer structure. Raw imported HTML is sanitized and quarantined for review; it never becomes executable UI.

A published representation pins template/theme, brand-context and protected-fact revisions. Protected facts include prices, dates, offer terms, claims, disclosures and canonical CTA destination/meaning. External systems remain authoritative for their facts; Texenda stores approved snapshots/references. A fact change/withdrawal marks affected unsent representations stale. A send must not continue using a known-withdrawn offer just because it was previously approved.

Personalization uses an allowlisted variable schema with type, source, escaping, required/optional status and explicit default. Missing required values hold the affected recipient; optional values use approved fallback text. URLs are validated separately from text. Compile and retain the resolved recipient payload/digest before an uncertain attempt; retries use exactly the same bytes and provider key. A new privacy withdrawal prevents retry even if the payload was prepared earlier.

Shared brand components may be reused across brands only through explicit target-brand adoption. Updating a shared source does not mutate published messages. AI channel/brand adaptation creates a draft with a difference view; required facts/claims/disclosures/CTA meaning cannot be silently changed. Each channel representation requires approval before it becomes sendable. SMS encoding, WhatsApp template variables, push lengths/deep links, and onsite placement/accessibility rules remain channel-specific.

**Downstream consequences:** editor replacement preserves old document codecs or compiled immutable versions; adding a channel does not turn email HTML into a universal content model. **Revisit:** add blocks or codecs for demonstrated content needs, with backward-compatibility tests and no expansion into general site building.

---

<a id="f10"></a>
## 10. AI operating model

**Decision status: AUTHORITATIVE DECISION.** AI prepares and explains. Deterministic commands, current permission, and approved revisions remain the only execution authority.

| Capability | Role | Maximum authority | Required validation and review |
|---|---|---|---|
| Natural-language segment | INTERPRET, CONFIGURE | **MAY CONFIGURE WITH PREVIEW** | Schema/compiler, workspace scope, source coverage, plain-language criteria, count/sample; operator accepts before use |
| Automation or sequence creation | GENERATE, CONFIGURE | **MAY PREPARE DRAFT** | Supported graph, bounded sends, no consent mutation, exits/expiry, simulation; publish approval |
| Campaign/sequence copy | GENERATE | **MAY PREPARE DRAFT** | Human verifies facts, offer, tone, CTA and disclosures |
| Channel adaptation | GENERATE | **MAY PREPARE DRAFT** | Typed representation, protected-fact equivalence, channel limits; per-variant approval |
| Brand adaptation | GENERATE | **MAY PREPARE DRAFT** | Access to source/target context and target-brand review; no audience transfer |
| Import mapping | INTERPRET, CONFIGURE | **MAY CONFIGURE WITH PREVIEW** | Dry run and provenance; uncertain consent held, never guessed |
| Performance summary | INTERPRET, EXPLAIN | **ADVISORY ONLY** | Computed metric references, windows/denominators/coverage; no fabricated causal claims |
| Anomaly explanation | MONITOR, EXPLAIN | **ADVISORY ONLY** | Deterministic threshold and evidence; AI cannot release a pause |
| Audience/timing/channel recommendation | RECOMMEND | **ADVISORY ONLY** | Show eligible options, evidence, uncertainty, cost and policy consequences |
| Product/settings assistance | EXPLAIN | **ADVISORY ONLY** | Version-correct documentation and role-scoped evidence |
| Schedule an already approved campaign through natural language | EXECUTE | **MAY EXECUTE WITH CONFIRMATION** | Confirmation binds exact approved revision, audience contract, schedule, ceiling and principal; normal command executes |
| Bounded internal draft/summary jobs | GENERATE, MONITOR | **MAY EXECUTE AUTONOMOUSLY WITHIN EXPLICIT POLICY** | Internal-only output, allowlisted sources, task/model/token budget; no outgoing recipient messages |
| Create consent, clear suppression, expand authorization/budget, override policy, invent live campaigns | CONFIGURE, EXECUTE | **NOT PERMITTED** | No tool/capability exists for these operations |

Structured output is a required interface, not proof of correctness. Models return proposed DTOs, never raw SQL, arbitrary URLs to invoke, or an imperative script. Run normal validation and authorization after model output exactly as for a human-created draft. A confirmation token is short-lived, single-use, digest-bound and invalidated by changes; the UI shows what the token authorizes.

Data minimization occurs before model access: schema, approved brand context, aggregates and necessary redacted examples. Raw contact export, other brands' data, credentials and unrestricted event history are not model context. Retrieved documents, emails, imports, website text and tool results are untrusted data, not instructions. Tool allowlists, typed boundaries, isolation and approvals reduce risk; they do not prove prompt-injection immunity. [S18]

Record task ID, initiating principal, allowed scope, input-document revisions, model/provider/version, prompt-template version, structured proposal, validator results, operator changes/approval, token/cost usage and resulting command IDs. Do not collect hidden model reasoning. Retain only task-relevant data under the telemetry/PII schedule.

**REVERSIBLE DEFAULT:** use an `AIProvider` adapter with OpenAI API as the first integration candidate; do not freeze a specific model name. Bind an exact evaluated model snapshot where available, not an unreviewed “latest” alias. Select a lower-cost qualified model per task and escalate only within the same budget and authority. An initial internal ceiling of **USD 25/month and USD 1/task** is a proposed reversible cap, disabled until the owner activates billing. Hard ceilings include reservations and estimated output cost. No automatic credit reload or budget expansion.

**REQUIRES EXTERNAL VALIDATION — VAL-09:** provider data terms, retention, model evaluations, injection tests, cost behavior and operator acceptance. An unavailable or invalid AI response leaves a visible draft/task error. Deterministic builders and all approved live automations continue without AI. No AI call is required in the send-policy path.

**Consequences:** ordinary UI and source-of-truth calculations must be complete without AI. **Revisit:** additional internal autonomy may be added only with a bounded capability and evaluation; autonomous marketing send invention remains out of scope.

---

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

<a id="f12"></a>
## 12. Technology stack and infrastructure baseline

The column **Decision status** uses the five closure statuses. **Infrastructure disposition** is the separate four-value classification requested for this section. “Authoritative baseline” freezes an architectural role, not every dependency patch version.

| Component | Decision status | Infrastructure disposition | Initial implementation / replaceability |
|---|---|---|---|
| TypeScript, React, Next.js | **AUTHORITATIVE DECISION** | **AUTHORITATIVE BASELINE** | One application language and React operator UI; supported versions pinned in one lockfile after compatibility checks |
| Payload | **AUTHORITATIVE DECISION** | **AUTHORITATIVE BASELINE** | Auth/admin/configuration platform, not implicit audience authority; framework APIs isolated from core |
| PostgreSQL | **AUTHORITATIVE DECISION** | **AUTHORITATIVE BASELINE** | Single transactional authority; do not build a speculative database-agnostic core |
| Drizzle for domain tables | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Explicit unit-of-work repositories; Payload owns only its tables; one ordered deployment migration manifest |
| React Email + editor | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Versioned codec/render port; fall back to a small block editor if qualification fails |
| Resend | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Email transport only through `MailProvider`; no provider contacts, campaigns, schedules, or automations as authority |
| Payload Jobs | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Coarse wakeups/control jobs; business due state and campaign recipients remain domain records |
| Mailpit | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Local/CI email capture; private network, no live relay, pinned maintained version [S23] |
| OpenTelemetry + structured logs | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Instrumentation vendor-neutral; log/trace backend replaceable; PII allowlist |
| S3-compatible object storage | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Assets, expiring exports, immutable approved artifacts and independent encrypted safety journal; separate buckets/access policies |
| Render paid web + background worker + managed PostgreSQL | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Initial hosting candidate; portable containers, explicit commands, co-located DB, no local durable state; VAL-05 qualifies plan/region/security/backup capabilities |
| Hosting secret manager/environment secret injection | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Per-runtime credentials; encrypted key references, rotatable and absent from browser/build outputs |
| Unit/integration/property/E2E tools | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Vitest, fast-check, Playwright and containerized real PostgreSQL; versions pinned, tools not product authority |
| SimpleWebAuthn-backed operator second factor | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Application-enforced verified WebAuthn ceremony with recovery; VAL-08 checks every access path [S19] |
| SES | **DEFER UNTIL TRIGGERED** | **DEFER UNTIL TRIGGERED** | Implement when cost/availability/isolation requirements justify a second qualified adapter; contract shape exists now, no speculative production account |
| Graphile Worker / alternative job runner | **DEFER UNTIL TRIGGERED** | **DEFER UNTIL TRIGGERED** | Persistent ready-job p95 >30–60s after tuning/scaling, or recurring queue-maintenance burden |
| ClickHouse | **DEFER UNTIL TRIGGERED** | **DEFER UNTIL TRIGGERED** | Reporting p95 >5s after indexes/rollups, or analytics >25% of primary resources for two review periods with interactive impact |
| Valkey | **DEFER UNTIL TRIGGERED** | **DEFER UNTIL TRIGGERED** | Measured hot-cache/rate-limit contention remains after Postgres tuning; never sole consent/occurrence state |
| Temporal / durable workflow service | **DEFER UNTIL TRIGGERED** | **DEFER UNTIL TRIGGERED** | Approved parallel joins/signals or repeated recovery work exceeds internal executor cost; adapter migration preserves business keys |
| Svix / webhook infrastructure | **DEFER UNTIL TRIGGERED** | **DEFER UNTIL TRIGGERED** | Roughly 10+ independent consumers, sustained 100k+ attempts/day, or recurring replay/signing operations justify it |
| Umami / anonymous web analytics | **DEFER UNTIL TRIGGERED** | **DEFER UNTIL TRIGGERED** | Demonstrated separate anonymous-site reporting need; never an identified consent/event authority |
| Microservices, Kafka, CDP, general integration middleware, self-hosted outbound MTA | **AUTHORITATIVE DECISION** | **UNNECESSARY** | Excluded from this baseline; require a new justified architecture/product ADR |

Numerical trigger values are proposed operating thresholds, not claims about product capacity. Do not migrate because a table crosses an arbitrary row count alone.

### 12.1 Runtime and version qualification

Use a currently supported Node LTS compatible with the selected Payload/Next/React packages. Pin exact versions, container digest, operating-system image, database major/minor, renderer and migrations in a compatibility manifest before the first integration milestone. Dependency lockfiles freeze a build; this document need not pretend one remembered patch version is current indefinitely.

Production has at least a web role and a continuously available worker role from one release. A reserved safety-processing lane/worker process prevents imports, AI calls or bulk campaigns starving opt-outs and provider evidence. The deployment may add another process of the same codebase; it need not add a service boundary. Use advisory leadership/leases for sweepers and concurrent idempotent handlers, not a single fragile in-memory scheduler.

Render documents background workers and paid PostgreSQL point-in-time recovery, but plan limits and recovery windows must be verified for the selected account. A paid plan's existence is not evidence that this installation meets recovery targets. [S20]

### 12.2 Backups and deployment

Require encrypted managed PITR, daily encrypted logical backup in an independent failure domain, object versioning for approved assets, safety-journal coverage, and a tested restore procedure. **REVERSIBLE DEFAULT targets:** database RPO ≤5 minutes and service RTO ≤4 hours under the qualified load/plan. Journaled safety/effect evidence must prevent unsafe resumption even when ordinary state is lost within the RPO. These are acceptance targets, not provider guarantees.

A proposed initial backup policy is seven days PITR, 35 days daily logical backups, and 90 days independent safety journal, with personal-data minimization and VAL-02 retention approval. Never restore a backup older than available safety evidence and then automatically send. Object/journal unavailability prevents new effect handoffs; this intentionally trades sending availability for recoverability.

Use one migration leader and expand/contract schema changes. No destructive column removal while an active binary or pinned workflow handler requires it. On rollback, revert compatible application code, not the database to an older permission state. Deployed worker handlers declare supported definition/representation schema versions; releases fail preflight if active runs cannot resume.

**REQUIRES EXTERNAL VALIDATION — VAL-03/VAL-05/VAL-08:** exact package compatibility, licensing, hosting security/PITR, export/storage properties, MFA integration and load/restore tests. Failure changes the relevant adapter/vendor, not the accepted architecture.

---

<a id="f13"></a>
## 13. Provider and integration architecture

**Decision status: AUTHORITATIVE DECISION.** External systems impose additional constraints and return evidence; they cannot supply audience, consent, campaign, or workflow truth.

### 13.1 Transport contracts

The following is an interface sketch, not a promise that providers implement every capability:

```typescript
interface MailProvider {
  capabilities(route: QualifiedRoute): ProviderCapabilities;
  validatePrepared(request: PreparedEmail): ValidationResult;
  estimateCost(request: PreparedEmail): CostEstimate;
  send(request: PreparedEmail, permit: DispatchPermit): Promise<AcceptanceResult>;
  reconcile(reference: ProviderReference): Promise<ReconciliationResult>;
}
// A separate verified ingress adapter authenticates the original request bytes,
// retains evidence and returns normalized observations. It never calls send().
```

`AcceptanceResult` distinguishes accepted, definitely-not-accepted and unknown. Unsupported status retrieval is explicit; it does not default to not-sent. A provider-capability record includes API/account/region, idempotency scope/window, batch atomicity, item response correlation, status/event coverage, authentication, suppression scope, allowable headers, quotas, costs and qualification freshness.

The broader channel interface shares validation/readiness/cost/outcome vocabulary. It does not force onsite rendering into `MailProvider.send`, or map push/browser state into email bounce semantics. Channel adapters cannot construct unapproved recipients or grant fallback authority.

### 13.2 Resend baseline and sender isolation

**REVERSIBLE DEFAULT:** one qualified Resend account/team for the initial pilot brand. For additional substantial brands, prefer independently qualified teams/accounts or another proven isolation mechanism; a shared pool requires explicit acceptance of coupled limits and suppression. Record sender → provider account → team/region/program → legal sender mappings.

Do not assume domain-specific keys provide independent quotas or suppression. Resend's directly retrieved documentation describes team-wide suppression and team-level rate limits. Retrieved search summaries showed differing snapshots of some operational values; therefore **do not hard-code a remembered rate, domain count, price, or suppression geography**. Capture the live account's approved limits and verify behavior in VAL-04 before activation. [S07, S08]

Texenda uses ordinary email sending APIs, not provider audience/automation features. A provider endpoint or plan labeled “transactional” is not a legal classification or permission to send marketing; confirm the selected plan permits the intended newsletter traffic. Provider scheduled-send features are not used initially—Texenda owns timing and cancellation.

Sender activation requires demonstrated domain control, allowed From/reply-to addresses, SPF/DKIM/DMARC configuration and alignment, test-message authentication results, functioning visible/one-click opt-out, provider feedback, and a named incident owner. Brand display identity remains clear. Shared IP pools and vendor reputation may still couple brands; domain separation is not a guarantee of complete deliverability isolation.

### 13.3 Webhook ingress and reconciliation

Authenticate the raw bytes according to the specific provider scheme, including its real timestamp/replay rules. Do not invent one universal signing method. Use separate endpoint secrets/account binding, size/content-type limits and constant-time verification where appropriate. Persist raw signed input and dedup ID before successful response; restrictive inputs additionally meet the safety-journal boundary. Do not execute a workflow in the HTTP callback.

Deduplicate `(provider_account, provider_event_id)` where supplied; use a qualified fallback identity only when necessary, preserving legitimately repeated distinct observations. A webhook may arrive before the API response: correlate by known provider/custom metadata or quarantine until the delivery is identifiable. It must not be attached to a guessed person by email alone.

Normalize into facts with source time, received time, confidence/coverage and source reference. Process safety events ahead of ordinary analytics. Unknown/contradictory events are visible and replayable. Poll/retrieve provider status or suppression exports when supported; APIs that cannot answer are marked inconclusive. Provider suppression removal never clears an independent Texenda withdrawal or safety hold.

### 13.4 Property API, event ingestion and SDK

Public API namespace is `/api/v1`, with explicit OpenAPI/JSON schemas, bounded pagination, stable opaque IDs, consistent errors and deprecation windows. Generated Payload REST/GraphQL is **not** the public audience API. Disable GraphQL unless a concrete internal requirement is qualified.

A publishable form identifier only submits to one preconfigured form. It is not a secret and cannot assign arbitrary tags, publications or purchases. Browser origin checks reduce accidental misuse but are not authentication. Rate limits, bot controls, verification and non-enumerating responses protect public acquisition.

Server API credentials are hashed/rotatable and scoped to organization, brand, property, allowed command/event types, rate and budget. Trusted purchase events require an authorized server integration and stable business event ID. Preserve original source IDs, schema version and source health. An integration may request a subscription only with required consent proof; no “add contact = active subscriber” shortcut exists.

Mutation idempotency is scoped by principal/route and a stable client key plus request digest. Same key/different request returns conflict. Keep transport-request deduplication and permanent business-occurrence constraints separate; a short API-idempotency TTL must not allow a duplicate purchase/welcome after it expires. Bulk APIs return per-item results and never conceal partial failure.

### 13.5 Outbound integrations and failure boundaries

Initially provide outbound webhooks only for a real integration need, using the existing outbox, signed minimized payloads, stable event IDs, bounded retry, endpoint pause and manual replay. Recipient identity is shared only by explicit scope. Protect outbound fetches from SSRF: approved HTTPS endpoints, controlled redirects, private-address denial and DNS/rebinding protections in the HTTP client/network policy.

Never let a failed webhook roll back consent or a completed campaign. Replays are tagged and idempotent; consumers must deduplicate. A later Svix adapter replaces delivery operations, not event semantics.

No automatic live failover to SES or another channel. Planned provider migration pauses, drains/reconciles outstanding work, preserves semantic keys, qualifies the new route, and explicitly activates it. Unknown effects remain on the old route's reconciliation path.

**Consequences:** one stable property API and permission model survive provider changes. **Revisit:** new integration types add schemas and capabilities under least privilege; no connector marketplace or general automation system is implied.

---

<a id="f14"></a>
## 14. Security, permissions, and governance

**Decision status: AUTHORITATIVE DECISION.** Security enforcement belongs in principal resolution, domain authorization, scoped repositories, final handoff and runtime credentials—not merely navigation or a hidden button.

### 14.1 Authentication and authorization

Payload remains the operator authentication foundation. Require MFA before production administration; the initial implementation is a verified WebAuthn second factor/passkey ceremony integrated with Payload sessions through a role-independent assurance check. Recovery codes are single-use and hashed; registering/replacing factors requires step-up or a controlled recovery procedure. User-verification, RP ID/origin and challenge checks are mandatory. SimpleWebAuthn supplies the ceremony primitives, not Texenda's authorization policy. [S19]

Enforce the resulting authenticated assurance on **all** protected generated/custom reads and mutations, server actions and job administration. A valid first-factor Payload session without MFA cannot access protected data. Revalidate domain membership at command time. Cookie/CSRF/origin protections, session expiry/revocation, login throttles, generic recovery responses and audit are required. Machine principals use separately scoped server credentials, not copied operator sessions.

Payload Local API and job operations can bypass access controls by default. Safe wrappers must explicitly apply the authenticated user and `overrideAccess: false` on request-driven operations; privileged internal calls are allowlisted and still enter authorized domain commands. `overrideLock: false` is used for editorial writes when applicable. Do not treat a request-supplied user/context object as trusted. [S01, S04]

**Initial owner bootstrap:** disable public first-user registration and self-service organization creation. Use a one-time deployment-console command with a short-lived bootstrap capability to create the initial auth identity and activate its domain owner membership; a partially created auth record has no owner authority until the domain activation commits. Record the bootstrap actor/evidence, require MFA enrollment before general administration, then revoke the capability. Subsequent operator provisioning is owner-invited and scoped. Bootstrap/recovery can establish operator access but cannot create audience consent or bypass sending policy. Test reuse, concurrent bootstrap attempts and access before factor enrollment.

### 14.2 Role and capability model

| Role | Allowed core responsibilities | Sensitive capabilities not implied |
|---|---|---|
| Portfolio owner/admin | Organization settings, authorized brands, policy activation, migration authority | Cannot bypass recipient refusal or invent consent |
| Brand admin | One or more explicitly granted brands, publications, content and routine operations | No other-brand identity/history or organization limit override |
| Editor/marketer | Audience reads within scope, draft content/segments/workflows | No high-risk live approval or PII export unless separately granted |
| Approver | Approve/schedule within explicit recipient/spend limits | No automatic policy/sender/consent administration |
| Analyst | Scoped aggregates and approved read models | No unmasked exports or mutations |
| Support/privacy operator | Locate a scoped profile and apply recipient-requested restrictions | No unrestricted reconsent, broader identity view or safety-hold release |
| Deliverability/security operator | Sender health, incident holds, evidence-based corrections | No arbitrary marketing content or targeting authority |
| Integration principal | Enumerated commands/events/property scopes | No raw database/API wildcard, provider keys or live-send bypass |
| Worker principal | Execute approved domain work within current policies/leases | Cannot approve new campaigns or expand scope |

Capabilities separately control PII export, portfolio identity inspection, sender changes, permission correction, safety-hold release, policy activation and large-send approval. Audit both allowed sensitive operations and denied attempts. UI roles are presentations of these capabilities, not a second authority system.

### 14.3 Initial mass-send and approval safeguards

The following numeric settings are **REVERSIBLE DEFAULTS**; their enforcement is authoritative:

| Default ID | Pilot/initial rule |
|---|---|
| **APR-01** | Every new representation/sender combination requires a successful internal test and preflight before live use. |
| **APR-02** | The first live canary per publication is explicitly approved and capped at **250 eligible, genuinely subscribed recipients or the smaller actual audience**. It is not a synthetic permission grant. |
| **APR-03** | After pilot qualification, campaigns above **5,000 candidates** require elevated review. A campaign above an operator's recipient/spend authority must be approved by a principal with sufficient authority; step-up alone does not increase permissions or organization budget. The 5,000 figure is a safety default, not an assumed audience size. |
| **APR-04** | A solopreneur may perform elevated review using fresh MFA, a separate review step, retyped brand/count confirmation and a **10-minute cooling-off interval**. Organizations may require a second human instead. |
| **APR-05** | Approved candidate and cost ceilings are hard ceilings. Any change to bound content/audience/channel/sender/schedule requires reapproval. |
| **APR-06** | New provider accounts/senders and organization-wide policy relaxations require owner-level activation, even below recipient thresholds. |

Kill switches exist for deployment, organization, provider account, sender, brand, campaign and execution. A safety pause is immediate for future permits and does not wait behind bulk queue work. Workers use rate profiles and spend reservations. No positive metered sending budget means no live paid-channel activation; the owner records explicit ceilings before a canary.

### 14.4 Data, secrets and environment boundaries

Provider credentials exist only in authorized worker/runtime secret scopes. Web roles hold only ingress verification keys and the secrets necessary for their approved work. AI receives no provider or database credentials. Separate production, staging and development databases/buckets/keys; do not copy production contact data into tests except a documented minimized, protected dataset approved for that purpose.

Use TLS, managed encryption at rest, private database networking, least-privilege DB roles, per-runtime credentials, tested key rotation and redacted logs. Public media assets are separate from private imports/exports and safety evidence. Imported/rendered HTML is sanitized and isolated in preview; arbitrary URL fetching, header injection, template execution, malicious CSVs and oversized inputs are tested.

Exports require explicit capability and current MFA, create an audit record, use encrypted storage and short-lived access. **REVERSIBLE DEFAULT:** signed download links expire in 15 minutes; export files in 24 hours. Spreadsheet-friendly CSV neutralizes formula-leading cells; a separate typed JSON export preserves exact values. Exporting data is not permission to market through another system.

Consent/audit evidence is append-only under ordinary application credentials, with corrections as new records. Strong tamper resistance comes from restricted roles and independent versioned journal copies, not the word “immutable.” PII is separable/encrypted so authorized erasure/retention can remove personal content without rewriting every operational fact. HMAC lookup/dedup values remain potentially personal/pseudonymous data, not automatically anonymous. A minimal do-not-contact tombstone is retained only under an approved legal basis; reimport must not erase it.

### 14.5 Overrides, incidents and external review

There is no administrative command that simply ignores recipient permission. Break-glass access is time-bound, reasoned, logged and scoped to pause, inspect, recover or make evidence-based corrections. Infrastructure administrators are recognized as a separate threat boundary. An emergency incident does not authorize a promotional campaign.

**REQUIRES EXTERNAL VALIDATION — VAL-02/VAL-08:** privacy/retention, sender obligations, MFA/session access coverage, dependency vulnerabilities, hostile-input tests, transport qualification, and backup/restore safety. Unresolved findings block the affected activation gate. No claim of legal compliance or production security is made by issuing this specification.

---

## External validation register

All rows below have **Decision status: REQUIRES EXTERNAL VALIDATION**. These are explicit evidence gates, not unresolved foundational design choices.

| Gate | Accountable owner | Evidence required | Blocks | Safe behavior / does not block |
|---|---|---|---|---|
| **VAL-01 Brand clearance** | Product Owner + trademark counsel | Exact/similar marks, prior Xenda/PiXENDA concerns, common-law/domain/linguistic/registry review | Irreversible public Texenda branding | Internal descriptive repository and product implementation continue |
| **VAL-02 Legal/privacy/source proof** | Product Owner + qualified counsel/privacy reviewer | Actual jurisdictions, audience/children-related collection policy if relevant, sender identity, purpose classes, consent wording, import provenance, retention/erasure basis | Production handling/sending for unapproved use cases | Build/test with synthetic data; hold uncertain imports; do not infer audience age/location |
| **VAL-03 Stack/editor compatibility** | Engineering owner | Locked version manifest, licenses/SBOM, Payload/domain transaction tests, migrations, editor codec/render fixtures | First integration release and affected dependency activation | Domain work continues; replace editor/adapter if needed |
| **VAL-04 Email provider/sender** | Deliverability owner, initially founder | Intended marketing use allowed, account quotas/scope, idempotency/batch/webhook tests, DNS and raw test-message auth, suppression/reconciliation capabilities | First real email handoff | Mailpit/fake transport; route remains disabled |
| **VAL-05 Hosting/recovery/workload** | Engineering/operations owner | Account/region/budget, measured workload profile, private networking, PITR/export/journal configuration, load and restore drill | Production infrastructure qualification | Portable container/dev work continues; no invented scale claims |
| **VAL-06 Operator usability** | Product Owner + routine operator | Representative tasks, consequence comprehension, timing/error observations, accessibility checks | Wider rollout if targets materially fail | Improve views/recipes; no change to permission semantics |
| **VAL-07 New channel** | Product Owner + channel operations owner | Demand, markets, consent, sender program, replies, cost, provider limits, device/site/privacy tests | Only that channel's live activation | Core email is unaffected |
| **VAL-08 Security readiness** | Engineering owner + competent independent review before broad production | Threat model, authorization/MFA paths, secrets, SSRF/injection/IDOR tests, vulnerabilities, incident and recovery evidence | Production/broad rollout at stated gates | No public/live audience processing until required findings close |
| **VAL-09 AI qualification** | Engineering/Product Owner | Data terms, task evaluations, prompt-injection tests, accuracy/cost caps, failure behavior | AI feature enablement | Deterministic product remains complete |
| **VAL-10 Kit migration evidence** | Migration owner, initially founder | Real account topology, all statuses, publications mapped, source coverage, active progress/exports, stop controls and authority transfer evidence | Each publication/cohort's cutover | Shadow read-only staging; never dual live sending or guessed progress |

## Deferred capability register

All rows have **Decision status: DEFER UNTIL TRIGGERED**.

| Capability | Reopen only when |
|---|---|
| External-customer multi-organization SaaS | A committed commercial use case justifies stronger tenant isolation, privacy contracts, billing and abuse operations |
| Cross-brand event-driven marketing | Repeated explicitly authorized use with target-brand consent and reviewed source-data use—not merely shared identity |
| Visual freeform automation canvas | Operators cannot accomplish routine approved workflows with recipe/structured editing; same underlying definitions remain |
| Materialized segments / analytics store | Measured repeated query latency/resource pressure after indexes and rollups |
| Provider/queue/workflow/cache substitution | The specific section 12 operating or contractual trigger is met |
| SMS/WhatsApp/native app channels | The corresponding section 7 use-case and VAL-07 gate is met |
| General identity merge UI | Repeated verified merge/correction work justifies it; restricted audited correction tooling suffices first |
| Advanced attribution/experimentation | Stable business outcomes and sufficient measured usage justify causal testing; never infer causation from opens |

<a id="source-register"></a>
## Source register

External references were checked during this decision-closure work on September 5, 2026. Vendor documentation may change or differ between indexed and directly retrieved snapshots; production qualification must preserve the exact contract and account evidence used. Product defaults and targets in this specification are recommendations, not copied vendor guarantees.

- **[S01] Payload Local API and access control:** https://payloadcms.com/docs/local-api/overview ; https://payloadcms.com/docs/local-api/access-control
- **[S02] Payload PostgreSQL adapter/custom schema:** https://payloadcms.com/docs/database/postgres
- **[S03] Payload transaction context:** https://payloadcms.com/docs/database/transactions
- **[S04] Payload Jobs and access control:** https://payloadcms.com/docs/jobs-queue/jobs
- **[S05] React Email editor architecture/API:** https://react.email/docs/editor/overview ; https://react.email/docs/editor/api-reference/email-editor
- **[S06] Resend idempotency:** https://resend.com/docs/dashboard/emails/idempotency-keys
- **[S07] Resend suppression semantics:** https://resend.com/docs/dashboard/emails/email-suppressions
- **[S08] Resend account rate/quota behavior:** https://resend.com/docs/api-reference/rate-limit
- **[S09] Kit subscriber listing and statuses:** https://developers.kit.com/api-reference/subscribers/list-subscribers
- **[S10] Kit sequence subscribers:** https://developers.kit.com/api-reference/sequences/list-subscribers-for-a-sequence
- **[S11] Kit API changelog and sequence content:** https://developers.kit.com/changelog ; https://developers.kit.com/api-reference/sequence-emails/list-sequence-emails
- **[S12] RFC 8058 one-click unsubscribe:** https://www.rfc-editor.org/rfc/rfc8058.html
- **[S13] Gmail sender-guideline reference for live qualification:** https://support.google.com/mail/answer/81126 (direct retrieval was rate-limited; verify current requirements at VAL-04 rather than relying on an unchecked threshold)
- **[S14] FTC commercial-email guidance:** https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- **[S15] Apple Mail Privacy Protection:** https://www.apple.com/legal/privacy/data/en/mail-privacy-protection/
- **[S16] Twilio Messaging Policy:** https://www.twilio.com/en-us/legal/messaging-policy
- **[S17] WebKit Web Push implementation context:** https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
- **[S18] OpenAI agent-safety guidance:** https://developers.openai.com/api/docs/guides/agent-builder-safety
- **[S19] SimpleWebAuthn server documentation:** https://simplewebauthn.dev/docs/packages/server
- **[S20] Render worker and backup documentation:** https://render.com/docs/background-workers ; https://render.com/docs/postgresql-backups
- **[S21] PostgreSQL SELECT/locking semantics:** https://www.postgresql.org/docs/current/sql-select.html
- **[S22] USPTO confusing-similarity guidance:** https://www.uspto.gov/trademarks/search/likelihood-confusion
- **[S23] Mailpit documentation:** https://mailpit.axllent.org/docs/
- **[S24] Kit unsubscribe endpoint:** https://developers.kit.com/api-reference/subscribers/unsubscribe-subscriber

## Closure statement

**Repository and implementation design may proceed from this baseline.** Foundational product, authority, domain, policy, execution, content, AI and security semantics are closed here. Remaining uncertainty is confined to explicit external validation gates and triggered capability/infrastructure decisions. Neither an unselected future channel nor unresolved public trademark clearance requires another broad product-definition exercise.
