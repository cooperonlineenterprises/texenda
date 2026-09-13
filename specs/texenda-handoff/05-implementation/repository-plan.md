# Repository layout, ownership and bootstrap plan

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Accepted interaction architecture and complete-handoff directive. Apply [package authority](../DECISION-STATUS.md).


**Decision status: REVERSIBLE DEFAULT** for file layout; **AUTHORITATIVE DECISION** for dependencies/authority. Target repository is `coe-audience-platform`. The handoff is installed under `specs/texenda-handoff/`; root `AGENTS.md` and `.texenda/` govern development. The application is not included in this ZIP.

```text
AGENTS.md
.texenda/                  local task ledger, claims, receipts, runtime qualification
specs/texenda-handoff/      versioned normative package and historical reference
apps/web/                  Next.js + Payload custom views, public ingress
apps/worker/               one codebase, safety and ordinary worker lanes
packages/contracts/        versioned command/query/event DTOs; no implementation
packages/core/
  portfolio/ identity/ audience/ permission/ segmentation/ content/
  campaign/ workflow/ coordinator/ interaction/ agent-access/ operations/
packages/persistence/      scoped Drizzle repositories and unit of work
packages/integrations/     email/storage/AI/voice/qualified-channel adapters
packages/payload-platform/ authentication/configuration/draft/admin bridge
infra/                     deployment manifests, migration ordering, recovery
 tests/                    unit, property, PostgreSQL, browser, fault, migration, agent
```

Allowed dependencies: composition roots → core+adapters; core → contracts/ports; persistence/integrations implement ports; core MUST NOT import applications, Payload or provider SDKs. Payload configuration receives handlers at composition time. No internal service HTTP just to cross a module.

Astra assigns one owner for shared contracts, lockfile and migration manifest integration. Parallel workers modify distinct directories in separate worktrees and propose shared-file changes for that owner. Schema changes require migration and handler compatibility review before consumer work begins. Initial maximum is three concurrent implementation writers, with lower concurrency around permission/execution changes; read-only review can run separately.

Bootstrap does not activate real providers, install unknown dependencies with production credentials, or create live users/subscribers. WP-000 qualifies the execution environment/model roster and package. WP-001 locks supported package versions with license/SBOM evidence. WP-002 establishes imports and contracts before product code.

No `latest` Docker tag or unbounded package range in a qualified production release. The package provides empty compatibility fields on purpose; real resolved/pinned versions are evidence produced by WP-001, not stale guesses embedded here.
