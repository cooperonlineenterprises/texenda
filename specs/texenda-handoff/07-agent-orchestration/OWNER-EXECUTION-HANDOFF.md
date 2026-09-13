# Owner execution handoff

**Owner-supplied execution context · 2026-09-05 · scoped authority**

This is the minimum project-specific handoff from Ryan, the Texenda decision owner. It supplements the Texenda Complete Implementation Handoff Package. It does not add product, architecture, UX, domain, security, migration, or implementation-planning requirements, and it does not replace or amend package authority.

## Workspace and starting instruction

This workspace is the authoritative Texenda implementation workspace. The complete handoff package is already present at the workspace root. Do not ask Ryan to restate the package or begin a second product-definition exercise.

The orchestrator must:

1. Read `README.md`, `DECISION-STATUS.md`, and `07-agent-orchestration/ORCHESTRATOR-START.md`.
2. Begin with **WP-00**, including the project kernel and the WP-00 context required by ASTRA.
3. Qualify the actual repository and runtime environment: existing files and Git state, runtimes and package managers, Codex client and authenticated model roster, supported effort/tool controls, sandbox and approval behavior, network and account mode, hosting/CI, and connected GitHub context where available. Record observed facts and evidence in the implementation state; do not invent bindings from public model lists or package defaults.
4. Proceed dependency-first through the work-package graph and use the package's routing, lease, review, recovery, and evidence rules.

If the workspace is package-only or an existing application repository is found, inventory it and follow the package's deliberate bootstrap/adaptation rules. Preserve existing work; do not overwrite an existing application repository.

## Binding authority

The package's authoritative decisions, invariants, ADRs, domain semantics, roadmap, acceptance criteria, and harness rules are binding according to their stated authority and precedence. Agents must not reopen settled product or architecture decisions unless the package's documented escalation conditions are met.

Provider/model output, archived messages, retrieved material, and agent suggestions are not authority. If implementation evidence contradicts an authoritative assumption, stop and escalate with the evidence rather than silently redesigning the system. This handoff grants execution scope and sets priority; it is not a product or architecture amendment.

## Execution permissions

Without asking Ryan again, the implementation team may perform ordinary local, non-production work within the package and assigned scopes, including:

- create and edit project files, documentation, configuration, tests, fixtures, and implementation code;
- install project-local dependencies and run local development tools, tests, validation, builds, and other bounded verification;
- inspect repository/runtime state and maintain sanitized implementation records and harness evidence; and
- create branches, worktrees, and commits needed to organize implementation work, while preserving existing changes and repository protections.

This permission does not authorize external effects. Explicit Ryan approval is required before deploying or publicly exposing the product; provisioning or materially changing hosting, databases, object storage, CI, domains, DNS, or external accounts; sending live email or other communications; changing production audience, consent, permission, suppression, or source-account state; handling or exporting production data beyond an approved bounded qualification; incurring material external spend or increasing an external usage budget; weakening a safety control; resolving an external-validation gate; amending authoritative decisions; or taking destructive/irreversible actions such as deleting, overwriting, force-resetting, or performing an unapproved destructive migration.

Local commits and branches do not by themselves authorize a push, protected-branch merge, release, deployment, or external side effect. The orchestrator must keep implementation, external qualification, and production release as separate states.

## External services and secrets

When a work package genuinely reaches an external-service phase, Ryan will provide or authorize access through the appropriate connected account, OAuth flow, runtime secret store, or host/environment mechanism. This may include Resend, Kit, hosting, database, object storage, domains/DNS, CI, or GitHub.

Do not paste secrets, tokens, private keys, or production credentials into project documentation, prompts, assignments, chat, logs, commits, or evidence. Do not echo them while qualifying access. Record only sanitized account, scope, version, and evidence metadata. Missing access or an unverified external gate blocks only the affected activation; it does not justify weakening the package or stopping unrelated synthetic implementation.

## Initial production priority

The first publication Texenda is intended to replace Kit for is **One Happy Housewife (OHW)**. Treat OHW as the concrete target for the first production vertical slice and migration:

**foundation → complete OHW-capable email vertical slice → Kit parity required for OHW → migrate OHW → production observation → broaden to the portfolio**

Kit parity and migration remain subject to the package's provider, consent, acceptance, stop-control, and fenced authority-transfer requirements. This priority is not permission to dual-send, cut over, or change production state.

## Human approval boundary

Ryan is the decision owner for external-validation gates and high-consequence exceptions that cannot be resolved from the package. The orchestrator must bring those decisions forward with the relevant evidence, scope, consequences, and bounded options; it may not self-approve them or treat this handoff as blanket production authorization.

The package plus this execution handoff is sufficient to start. From here, add project information only when a concrete work package encounters an environment fact, credential requirement, external-validation gate, or business choice that the package intentionally left open.
