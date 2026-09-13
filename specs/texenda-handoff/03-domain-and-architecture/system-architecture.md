# Product architecture

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

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

Publishing a Payload-managed content/configuration draft copies an immutable, validated revision into Texenda authority through a command. The copy and its activation/audit/outbox commit together in the domain transaction. A stale “published” UI badge is repaired from domain state, not accepted as authority. This avoids assuming that independent Payload and Drizzle calls share a transaction. Where code does use multiple Payload Local API operations transactionally, its `req` transaction context must be propagated as documented. [S01, S03](../09-reference/source-register.md#s01)

Payload permits custom PostgreSQL schema additions; validate the chosen adapter and migration integration in VAL-03. Do not maintain two uncoordinated migration systems or let development schema-push alter production. [S02](../09-reference/source-register.md#s02)

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


## 4.7 Interaction adapters and shared command registry

Add `interaction` application services within `packages/core` (or a small application package if justified), not a second agent backend. Their responsibilities are context assembly, proposals, goals, revision checks, approval requests and audit attribution. Models and speech providers remain in `packages/integrations`. API/UI/MCP/browser tools map to registered DTOs; each descriptor declares required capability, actor types, risk, preview and approval semantics.

All surface reads use authorized query handlers. All mutations use registered commands. A model returns proposed input; the server resolves the principal and scope independently. Staged proposals cannot execute until validated and, when required, approved. No shared “AI superuser” session.

Web uses HTTP request/response and SSE for scoped status/token deltas; persisted event IDs allow reconnect/refetch. Audio may use a qualified WebRTC media adapter later. Do not treat SSE, a model's conversational state or a voice connection as a durable job executor. Use the existing worker and AgentRun records for bounded long jobs.

A compound Proposal may contain several typed commands. Supported database-only changes can commit in one unit of work. Remote effects remain independent outbox deliveries with per-item results and reconciliation. Approval of a plan is not a distributed transaction. Expected revisions and idempotency cover resume after a lost HTTP response.
