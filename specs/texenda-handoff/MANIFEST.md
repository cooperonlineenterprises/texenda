# Artifact manifest

**Texenda implementation handoff 1.1.0 · 86 files.** Every path is relative to the package root. Normative owners define requirements; derived/index files organize them; templates are unfilled; executable scaffolds govern local work only; reference files are not competing authority. Dependencies below are document dependencies, not the implementation DAG.

| Path | Purpose | Authority | Primary consumers | Dependencies |
|---|---|---|---|---|
| [01-foundation/adr-index.md](01-foundation/adr-index.md) | ADR index | DERIVED | Astra; implementation/review agents | 01-foundation/adr-set.md |
| [01-foundation/adr-set.md](01-foundation/adr-set.md) | Decision record / ADR set | NORMATIVE | Astra; implementation/review agents | — |
| [01-foundation/authority-register.json](01-foundation/authority-register.json) | authority-register | NORMATIVE | Astra; validators | — |
| [01-foundation/external-validation-gates.json](01-foundation/external-validation-gates.json) | external-validation-gates | NORMATIVE | Astra; validators | — |
| [01-foundation/invariant-index.json](01-foundation/invariant-index.json) | invariant-index | DERIVED | Astra; validators | 01-foundation/invariants.md |
| [01-foundation/invariants.md](01-foundation/invariants.md) | Governing principles and non-bypassable invariants | NORMATIVE | Astra; implementation/review agents | — |
| [01-foundation/product-and-brand.md](01-foundation/product-and-brand.md) | Product definition and boundary | NORMATIVE | Astra; implementation/review agents | — |
| [01-foundation/section-map.md](01-foundation/section-map.md) | Foundation and roadmap section map | NORMATIVE | Astra; implementation/review agents | — |
| [02-product-and-ux/interaction-architecture.md](02-product-and-ux/interaction-architecture.md) | Human- and agent-native interaction architecture | NORMATIVE | Astra; implementation/review agents | — |
| [02-product-and-ux/operator-workflows.md](02-product-and-ux/operator-workflows.md) | UX and information architecture | NORMATIVE | Astra; implementation/review agents | — |
| [03-domain-and-architecture/canonical-domain.md](03-domain-and-architecture/canonical-domain.md) | Canonical domain and data model | NORMATIVE | Astra; implementation/review agents | — |
| [03-domain-and-architecture/channels.md](03-domain-and-architecture/channels.md) | Channel strategy and abstraction | NORMATIVE | Astra; implementation/review agents | — |
| [03-domain-and-architecture/command-catalog.json](03-domain-and-architecture/command-catalog.json) | command-catalog | NORMATIVE | Astra; validators | — |
| [03-domain-and-architecture/content.md](03-domain-and-architecture/content.md) | Content and message model | NORMATIVE | Astra; implementation/review agents | — |
| [03-domain-and-architecture/contracts/command-envelope.schema.json](03-domain-and-architecture/contracts/command-envelope.schema.json) | command-envelope.schema | NORMATIVE | Astra; validators | — |
| [03-domain-and-architecture/contracts/example-command.json](03-domain-and-architecture/contracts/example-command.json) | example-command | ILLUSTRATIVE SYNTHETIC EXAMPLE | Astra; validators | — |
| [03-domain-and-architecture/domain-catalog.json](03-domain-and-architecture/domain-catalog.json) | domain-catalog | DERIVED INDEX | Astra; validators | — |
| [03-domain-and-architecture/execution-semantics.md](03-domain-and-architecture/execution-semantics.md) | Campaign, sequence, and automation semantics | NORMATIVE | Astra; implementation/review agents | — |
| [03-domain-and-architecture/permission-and-coordination.md](03-domain-and-architecture/permission-and-coordination.md) | Consent, eligibility, suppression, preferences, and recipient experience | NORMATIVE | Astra; implementation/review agents | — |
| [03-domain-and-architecture/provider-integrations.md](03-domain-and-architecture/provider-integrations.md) | Provider and integration architecture | NORMATIVE | Astra; implementation/review agents | — |
| [03-domain-and-architecture/schema-and-contract-guide.md](03-domain-and-architecture/schema-and-contract-guide.md) | Data/schema and application contract implementation guide | NORMATIVE | Astra; implementation/review agents | — |
| [03-domain-and-architecture/state-machines.json](03-domain-and-architecture/state-machines.json) | state-machines | DERIVED INDEX | Astra; validators | — |
| [03-domain-and-architecture/system-architecture.md](03-domain-and-architecture/system-architecture.md) | Product architecture | NORMATIVE | Astra; implementation/review agents | — |
| [03-domain-and-architecture/technology-baseline.md](03-domain-and-architecture/technology-baseline.md) | Technology stack and infrastructure baseline | NORMATIVE | Astra; implementation/review agents | — |
| [04-security-governance-and-operations/ai-and-agent-authority.md](04-security-governance-and-operations/ai-and-agent-authority.md) | AI operating model | NORMATIVE | Astra; implementation/review agents | — |
| [04-security-governance-and-operations/observability.md](04-security-governance-and-operations/observability.md) | Analytics and operational observability | NORMATIVE | Astra; implementation/review agents | — |
| [04-security-governance-and-operations/runbooks.md](04-security-governance-and-operations/runbooks.md) | Operational runbooks and accountable ownership | NORMATIVE | Astra; implementation/review agents | — |
| [04-security-governance-and-operations/security-and-privacy.md](04-security-governance-and-operations/security-and-privacy.md) | Security, permissions, and governance | NORMATIVE | Astra; implementation/review agents | — |
| [05-implementation/compatibility-manifest.template.json](05-implementation/compatibility-manifest.template.json) | compatibility-manifest.template | TEMPLATE; NOT QUALIFICATION | Astra; validators | — |
| [05-implementation/repository-plan.md](05-implementation/repository-plan.md) | Repository layout, ownership and bootstrap plan | NORMATIVE | Astra; implementation/review agents | — |
| [05-implementation/roadmap.md](05-implementation/roadmap.md) | Dependency-ordered implementation and migration roadmap | NORMATIVE | Astra; implementation/review agents | — |
| [05-implementation/work-breakdown.md](05-implementation/work-breakdown.md) | Work-package catalog and dependency graph | DERIVED | Astra; implementation/review agents | 05-implementation/work-packages.json |
| [05-implementation/work-packages.json](05-implementation/work-packages.json) | work-packages | NORMATIVE | Astra; validators | — |
| [06-migration-and-production/acceptance-catalog.json](06-migration-and-production/acceptance-catalog.json) | acceptance-catalog | NORMATIVE | Astra; validators | — |
| [06-migration-and-production/acceptance-plan.md](06-migration-and-production/acceptance-plan.md) | Production acceptance criteria | NORMATIVE | Astra; implementation/review agents | — |
| [06-migration-and-production/kit-migration.md](06-migration-and-production/kit-migration.md) | Kit migration: fenced authority transfer | NORMATIVE | Astra; implementation/review agents | — |
| [06-migration-and-production/migration-unit.template.json](06-migration-and-production/migration-unit.template.json) | migration-unit.template | TEMPLATE | Astra; validators | — |
| [06-migration-and-production/release-evidence.template.json](06-migration-and-production/release-evidence.template.json) | release-evidence.template | TEMPLATE | Astra; validators | — |
| [06-migration-and-production/release-plan.md](06-migration-and-production/release-plan.md) | Production release and evidence plan | NORMATIVE | Astra; implementation/review agents | — |
| [06-migration-and-production/release-profiles.json](06-migration-and-production/release-profiles.json) | release-profiles | NORMATIVE | Astra; validators | — |
| [06-migration-and-production/workload-profile.template.json](06-migration-and-production/workload-profile.template.json) | workload-profile.template | TEMPLATE | Astra; validators | — |
| [07-agent-orchestration/ASSIGNMENT.template.md](07-agent-orchestration/ASSIGNMENT.template.md) | Assignment — <WP-ID / bounded child> | TEMPLATE | Astra; implementation/review agents | — |
| [07-agent-orchestration/ORCHESTRATOR-START.md](07-agent-orchestration/ORCHESTRATOR-START.md) | Orchestrator team-lead start prompt | NORMATIVE | Astra lead; accountable human | — |
| [07-agent-orchestration/context-routing.json](07-agent-orchestration/context-routing.json) | context-routing | NORMATIVE | Astra; validators | — |
| [07-agent-orchestration/handoff-and-review.md](07-agent-orchestration/handoff-and-review.md) | Agent handoff, verification and recovery protocol | NORMATIVE | Astra; implementation/review agents | — |
| [07-agent-orchestration/model-routing.json](07-agent-orchestration/model-routing.json) | model-routing | NORMATIVE | Astra; validators | — |
| [07-agent-orchestration/model-routing.md](07-agent-orchestration/model-routing.md) | Operational model-routing policy | NORMATIVE | Astra; implementation/review agents | — |
| [07-agent-orchestration/OWNER-EXECUTION-HANDOFF.md](07-agent-orchestration/OWNER-EXECUTION-HANDOFF.md) | Owner execution-environment, permissions and initial production-priority handoff | OWNER-SUPPLIED EXECUTION CONTEXT | Astra; accountable human; implementation/review agents | README.md, DECISION-STATUS.md, 07-agent-orchestration/ORCHESTRATOR-START.md |
| [07-agent-orchestration/project-kernel.md](07-agent-orchestration/project-kernel.md) | Project kernel — always read | NORMATIVE | Every agent and reviewer | — |
| [08-project-harness/README.md](08-project-harness/README.md) | Project-local harness — executable coordination scaffold | NORMATIVE | Astra; implementation/review agents | — |
| [08-project-harness/codex-config.toml.example](08-project-harness/codex-config.toml.example) | REVERSIBLE DEFAULT. Review against the actual installed client before copying. | TEMPLATE | Runtime owner; Astra | — |
| [08-project-harness/harness.py](08-project-harness/harness.py) | Executable local task/dependency/lease/evidence coordinator; no agent runner or production authority | EXECUTABLE SCAFFOLD | Astra; human implementation lead | 05-implementation/work-packages.json, 07-agent-orchestration/context-routing.json |
| [08-project-harness/install.py](08-project-harness/install.py) | Safe local installer | EXECUTABLE SCAFFOLD | Astra; runtime owner | — |
| [08-project-harness/probe_runtime.py](08-project-harness/probe_runtime.py) | Safe local runtime presence/version probe; not authenticated roster | EXECUTABLE SCAFFOLD | Astra; runtime owner | — |
| [08-project-harness/root-AGENTS.md.template](08-project-harness/root-AGENTS.md.template) | Texenda implementation instructions | TEMPLATE | Astra; implementation/review agents | — |
| [08-project-harness/schemas/evidence.schema.json](08-project-harness/schemas/evidence.schema.json) | evidence.schema | NORMATIVE | Astra; validators | — |
| [08-project-harness/schemas/work-package.schema.json](08-project-harness/schemas/work-package.schema.json) | work-package.schema | NORMATIVE | Astra; validators | — |
| [08-project-harness/templates/evidence.json](08-project-harness/templates/evidence.json) | evidence | TEMPLATE | Astra; validators | — |
| [08-project-harness/templates/roster.json](08-project-harness/templates/roster.json) | roster | TEMPLATE | Astra; validators | — |
| [08-project-harness/tests/test_harness.py](08-project-harness/tests/test_harness.py) | Synthetic unit tests for file-native coordinator, not product acceptance | EXECUTABLE SCAFFOLD | Astra; quality reviewers | 08-project-harness/harness.py |
| [09-reference/conversation-coverage.md](09-reference/conversation-coverage.md) | Conversation archive coverage and limitations | REFERENCE | Astra; implementation/review agents | — |
| [09-reference/conversation-record.json](09-reference/conversation-record.json) | conversation-record | REFERENCE | Astra; validators | — |
| [09-reference/conversation-record.md](09-reference/conversation-record.md) | Accessible conversation record | REFERENCE | Astra; implementation/review agents | 09-reference/conversation-record.json |
| [09-reference/original-artifact-integrity.json](09-reference/original-artifact-integrity.json) | original-artifact-integrity | DERIVED SOURCE INTEGRITY | Astra; validators | — |
| [09-reference/prior-artifacts/Texenda_Decision_Closure_v1.0.zip](09-reference/prior-artifacts/Texenda_Decision_Closure_v1.0.zip) | Original delivered ZIP, preserved unchanged | HISTORICAL SOURCE | Source archivist | — |
| [09-reference/prior-artifacts/Texenda_Implementation_Roadmap_Acceptance_v1.0.md](09-reference/prior-artifacts/Texenda_Implementation_Roadmap_Acceptance_v1.0.md) | Byte-preserved original Texenda_Implementation_Roadmap_Acceptance_v1.0 | HISTORICAL SOURCE; superseded by indexed normative package chapters | Astra; audit/recovery reviewers | — |
| [09-reference/prior-artifacts/Texenda_Product_Technical_Foundation_v1.0.md](09-reference/prior-artifacts/Texenda_Product_Technical_Foundation_v1.0.md) | Byte-preserved original Texenda_Product_Technical_Foundation_v1.0 | HISTORICAL SOURCE; superseded by indexed normative package chapters | Astra; audit/recovery reviewers | — |
| [09-reference/source-register.json](09-reference/source-register.json) | source-register | REFERENCE | Astra; qualification owners | — |
| [09-reference/source-register.md](09-reference/source-register.md) | External source register | REFERENCE | Qualification owners; reviewers | 09-reference/source-register.json |
| [09-reference/supersession-and-traceability.md](09-reference/supersession-and-traceability.md) | Decision lineage and supersession | REFERENCE | Astra; implementation/review agents | — |
| [10-validation/clean-install-smoke.json](10-validation/clean-install-smoke.json) | Actual clean-install/CLI/JSON-schema packaging smoke test; not app qualification | VALIDATION RECORD | Astra; reviewer | 08-project-harness/install.py, 08-project-harness/harness.py |
| [10-validation/harness-test-map.json](10-validation/harness-test-map.json) | harness-test-map | VALIDATION RECORD | Astra; validators | — |
| [10-validation/harness-tests.log](10-validation/harness-tests.log) | Actual synthetic local-harness unit-test output | VALIDATION RECORD | Astra; reviewers | — |
| [10-validation/package-review.md](10-validation/package-review.md) | Cross-artifact review and validation record | VALIDATION RECORD | Astra; owner; reviewers | — |
| [10-validation/packaging-runtime-probe.json](10-validation/packaging-runtime-probe.json) | Observed packaging tools; not target model availability | VALIDATION RECORD | Astra; reviewers | — |
| [10-validation/requirement-traceability.json](10-validation/requirement-traceability.json) | requirement-traceability | DERIVED | Astra; validators | — |
| [10-validation/synthetic-domain-fixtures.json](10-validation/synthetic-domain-fixtures.json) | synthetic-domain-fixtures | NORMATIVE | Astra; validators | — |
| [10-validation/traceability-index.md](10-validation/traceability-index.md) | Requirement and decision traceability | DERIVED | Astra; implementation/review agents | — |
| [10-validation/validate_package.py](10-validation/validate_package.py) | Offline structural, link and traceability validator | EXECUTABLE SCAFFOLD | Astra; reviewers | — |
| [10-validation/validation-report.json](10-validation/validation-report.json) | validation-report | VALIDATION RECORD | Astra; validators | — |
| [AGENTS.md](AGENTS.md) | Instructions for agents reading this handoff | NORMATIVE | Coding agents; Astra | — |
| [DECISION-STATUS.md](DECISION-STATUS.md) | Decision status and authority | NORMATIVE | All agents; owner; release reviewers | 01-foundation/authority-register.json, 01-foundation/external-validation-gates.json |
| [MANIFEST.md](MANIFEST.md) | Complete navigable artifact inventory | INDEX | All readers | — |
| [README.md](README.md) | Texenda Complete Implementation Handoff | NORMATIVE | Astra; all implementation and review agents; owner | — |
| [SHA256SUMS](SHA256SUMS) | Generated at finalization; excludes itself. | INTEGRITY | Recipients; validators | — |
| [manifest.json](manifest.json) | Machine-readable inventory with ownership and dependencies | INDEX | Validators; Astra | — |
