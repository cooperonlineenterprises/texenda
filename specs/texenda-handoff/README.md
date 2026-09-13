# Texenda Complete Implementation Handoff

**Version 1.1.0 · 2026-09-05**

Texenda is an **email-led audience and communication platform for solopreneurs, publishers, creators and teams of five or fewer**. It supports permissioned audience relationships, relevant communication and selective qualified channels without becoming a CRM/CDP/helpdesk or enterprise marketing suite.

This package contains the normative specifications, bounded implementation plan, reference archive and executable local coordination scaffold for an Astra-led team. **It does not contain an implemented Texenda application, credentials, production test results or legal/provider clearance.**

## Start here

Read [decision status and authority](DECISION-STATUS.md), [project kernel](07-agent-orchestration/project-kernel.md), [the orchestrator start prompt](07-agent-orchestration/ORCHESTRATOR-START.md), and the [owner execution handoff](07-agent-orchestration/OWNER-EXECUTION-HANDOFF.md). Admit **WP-00** from the [work catalog](05-implementation/work-breakdown.md): inspect actual runtime/model availability, owner budget and repository state. Next, WP-01 locks implementable contracts; WP-02 creates the runnable repository. No broad product-definition exercise is needed.

```sh
python3 10-validation/validate_package.py
python3 -m unittest discover -s 08-project-harness/tests -v
python3 08-project-harness/install.py --target /absolute/path/to/new-repo
```

The installer is dry-run first. Review before `--apply`. Follow [harness instructions](08-project-harness/README.md); its CLI does not launch agents, merge/deploy, or grant production authority.

## Reading map

| Area | Entry point |
|---|---|
| Product and 30 invariants | [Foundation](01-foundation/product-and-brand.md), [invariants](01-foundation/invariants.md) |
| Human/voice/AI/external-agent UX | [Interaction architecture](02-product-and-ux/interaction-architecture.md) |
| Domain, policy and execution | [Canonical model](03-domain-and-architecture/canonical-domain.md), [permission](03-domain-and-architecture/permission-and-coordination.md), [execution](03-domain-and-architecture/execution-semantics.md) |
| Architecture/contracts/repository | [System](03-domain-and-architecture/system-architecture.md), [schema/contracts](03-domain-and-architecture/schema-and-contract-guide.md), [repo](05-implementation/repository-plan.md) |
| Security and operations | [Security](04-security-governance-and-operations/security-and-privacy.md), [runbooks](04-security-governance-and-operations/runbooks.md) |
| Build, migration, release | [44 WPs](05-implementation/work-breakdown.md), [Kit transfer](06-migration-and-production/kit-migration.md), [125 acceptance checks](06-migration-and-production/acceptance-catalog.json), [release profiles](06-migration-and-production/release-plan.md) |
| Decisions and orchestration | [35 ADRs](01-foundation/adr-index.md), [model routing](07-agent-orchestration/model-routing.md), [handoffs](07-agent-orchestration/handoff-and-review.md) |
| Sources and validation | [Source register](09-reference/source-register.md), [archive coverage](09-reference/conversation-coverage.md), [validation](10-validation/package-review.md) |

[MANIFEST.md](MANIFEST.md) lists every file, authority, consumers and dependencies. `SHA256SUMS` verifies package integrity, not product correctness.

## Boundaries that must not be reopened casually

One authoritative domain; identity ≠ permission; Withdrawal ≠ safety Suppression; current denial wins; one sequence/automation executor; shared command model across all surfaces; pressure and recovery journal before live email; no blind unknown-outcome failover; fenced Kit authority transfer; AI/agent proposals never create authority. Context packs route only relevant owners to each assignment.

## Remaining evidence

Fourteen explicit gates cover brand/legal, stack/editor, provider/sender, hosting/restore/workload, usability, channels, security, AI, Kit migration, external agents, voice/privacy, actual model roster and source-export completeness. All remain **UNVERIFIED** until applicable evidence is supplied. The public model roster was checked, but no Codex runtime or authenticated model roster exists in this packaging environment; active tier mappings are intentionally null.

The two prior closure artifacts and ZIP are preserved byte-for-byte. The conversation reference represents every recoverable substantive turn but is an **explicitly abridged reconstruction, not a complete verbatim export**. See the coverage statement; do not overstate archival completeness. This does not prevent implementing the consolidated normative model.

## First vertical slice

Subscription request → confirmation → scoped permission → approved test delivery → withdrawal → denied future delivery → safe replay/restore. Establish that slice before polished AI, voice, dashboards or additional channels.
