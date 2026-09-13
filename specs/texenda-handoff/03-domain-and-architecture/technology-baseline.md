# Technology stack and infrastructure baseline

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

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
| Mailpit | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Local/CI email capture; private network, no live relay, pinned maintained version [S23](../09-reference/source-register.md#s23) |
| OpenTelemetry + structured logs | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Instrumentation vendor-neutral; log/trace backend replaceable; PII allowlist |
| S3-compatible object storage | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Assets, expiring exports, immutable approved artifacts and independent encrypted safety journal; separate buckets/access policies |
| Render paid web + background worker + managed PostgreSQL | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Initial hosting candidate; portable containers, explicit commands, co-located DB, no local durable state; VAL-05 qualifies plan/region/security/backup capabilities |
| Hosting secret manager/environment secret injection | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Per-runtime credentials; encrypted key references, rotatable and absent from browser/build outputs |
| Unit/integration/property/E2E tools | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Vitest, fast-check, Playwright and containerized real PostgreSQL; versions pinned, tools not product authority |
| SimpleWebAuthn-backed operator second factor | **REVERSIBLE DEFAULT** | **REVERSIBLE DEFAULT** | Application-enforced verified WebAuthn ceremony with recovery; VAL-08 checks every access path [S19](../09-reference/source-register.md#s19) |
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

Render documents background workers and paid PostgreSQL point-in-time recovery, but plan limits and recovery windows must be verified for the selected account. A paid plan's existence is not evidence that this installation meets recovery targets. [S20](../09-reference/source-register.md#s20)

### 12.2 Backups and deployment

Require encrypted managed PITR, daily encrypted logical backup in an independent failure domain, object versioning for approved assets, safety-journal coverage, and a tested restore procedure. **REVERSIBLE DEFAULT targets:** database RPO ≤5 minutes and service RTO ≤4 hours under the qualified load/plan. Journaled safety/effect evidence must prevent unsafe resumption even when ordinary state is lost within the RPO. These are acceptance targets, not provider guarantees.

A proposed initial backup policy is seven days PITR, 35 days daily logical backups, and 90 days independent safety journal, with personal-data minimization and VAL-02 retention approval. Never restore a backup older than available safety evidence and then automatically send. Object/journal unavailability prevents new effect handoffs; this intentionally trades sending availability for recoverability.

Use one migration leader and expand/contract schema changes. No destructive column removal while an active binary or pinned workflow handler requires it. On rollback, revert compatible application code, not the database to an older permission state. Deployed worker handlers declare supported definition/representation schema versions; releases fail preflight if active runs cannot resume.

**REQUIRES EXTERNAL VALIDATION — VAL-03/VAL-05/VAL-08:** exact package compatibility, licensing, hosting security/PITR, export/storage properties, MFA integration and load/restore tests. Failure changes the relevant adapter/vendor, not the accepted architecture.

---


## Interaction implementation dispositions

| Capability | Decision status | Infrastructure disposition | Boundary/trigger |
|---|---|---|---|
| Command/query registry, object revisions, actor attribution | AUTHORITATIVE DECISION | AUTHORITATIVE BASELINE | Before all writable interaction adapters |
| Proposal/diff/approval contracts | AUTHORITATIVE DECISION | AUTHORITATIVE BASELINE | Before writable AI; existing email approvals use the same record |
| Semantic HTML/WCAG 2.2 AA and Inspect mode | AUTHORITATIVE DECISION | AUTHORITATIVE BASELINE | Accessible human UI first; no agent-only privileged application |
| SSE/streamed HTTP | REVERSIBLE DEFAULT | REVERSIBLE DEFAULT | Scoped UI/status transport; domain state is durable |
| STT/TTS and browser WebRTC | REVERSIBLE DEFAULT | REVERSIBLE DEFAULT | VoiceProvider port; enable only after VAL-12 and task usability tests |
| MCP adapter | DEFER UNTIL TRIGGERED | DEFER UNTIL TRIGGERED | Authorized external integration demand plus VAL-11 |
| Browser-semantic/WebMCP adapter | DEFER UNTIL TRIGGERED | DEFER UNTIL TRIGGERED | Supported target browsers/agents and measured advantage; never a core dependency |
| General vector memory, separate agent framework, realtime platform | AUTHORITATIVE DECISION | UNNECESSARY | Structured objects and current application runtime suffice |
| CRDT/live collaborative editing | DEFER UNTIL TRIGGERED | DEFER UNTIL TRIGGERED | Repeated simultaneous editing friction exceeds revision/diff recovery cost |

Exact vendor/model versions remain qualification outputs, not guessed package pins. The development model roster is owned by `07-agent-orchestration/model-routing.md`, not this product runtime table.
