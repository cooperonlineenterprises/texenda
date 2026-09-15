# ADR-0007: Standalone workspace operating contract

Status: AUTHORITATIVE LOCAL DECISION — owner-authorized remediation on 2026-09-15.
This accepts the scoped target, not its implementation candidate. A distinct
qualified reviewer binds the exact candidate; the integrator performs final
canonical validation and read-only integrated-head review.

## Scope and owners

Texenda remains a standalone mapped-existing high-assurance project. Canonical
`repo/` owns live coordination and serial integration. Linked worktrees own
candidate code. Ordinary development requires no installed Blueprint, family
repository, private input, or migration history.

This supersedes only literal host-specific ordinary-command and fixed-WP
prescriptions in [ADR-0006](ADR-0006-clean-ordinary-operating-contract.md), and
current operation/navigation implications of
[ADR-0004](ADR-0004-mapped-project-workspace.md). Preserve both accepted records
and their preservation, read-only/atime, migration, recovery, review, qualification
and external-gate boundaries. The ownership epoch remains `external_state`;
there is no physical move, state migration, receipt or product amendment.

Policy/context retain permission and precedence; validators.json owns argv.
The coordinator and bound ledger retain tasks, leases, receipts, roster and
budget. Sealed topic owners plus accepted scoped ADRs retain product authority.
Dossier records own only their declared information concerns. This operating
metadata grants no permission.

## Code and control

`validate.py --check --scope code --all` checks repository sources and eligible
synthetic suites. It rejects `--state-root` and never reads local binding/live
state, project-home sources/archive/private paths or installed skills. It labels
control, live state and generated freshness unassessed. Its PASS is candidate
code evidence only.

Default or explicit control scope requires canonical `repo/` with a regular
`.git` directory, active local binding and explicit matching absolute state
root. The complete check retains local preservation, receipt and generated
freshness checks. Missing, wrong, relative, symlinked, moving, competing and
transaction-blocked state fails closed. Coordinator pre-binding compatibility
remains for existing bootstrap and synthetic consumers, not ordinary migrated entry.

Tracked guidance uses quoted explicit parameters. Read the ignored descriptor
and set exact values deliberately; no wrapper discovers or substitutes a ledger.
Local WORKSPACE.md and generated RESUME may display expanded local paths.
Worktree live inspection invokes the canonical script and canonical `--root`;
never mix candidate script constants with canonical evidence or copy binding,
ledger or receipt inputs. A worktree does not acquire control authority.

Read live `ready`, explicitly select an ID for the current objective, then obtain
its context. Empty readiness has no fallback. Resumption uses the recorded task
and fence. Context, readiness and templates do not admit or assign work.

## Refresh, review and recovery

Refresh discovery is `python3 -B .agent/scripts/refresh.py --help`, requiring no
binding, ledger, generated output, marker, cache or local sibling. Refresh and
interrupted recovery are explicit canonical control writers; checks never
dispatch them, including under `--all`. All eleven projections remain derived
and deterministically reconstructable from source, evidence and ledger.

The author commits non-generated source in a worktree and stops. The integrator
may stage the preserved candidate branch in canonical repo while main's ref stays
unchanged, explicitly refresh, then obtain exact independent control review.
Evidence additions require explicit refresh and final read-only integrated-head
review. Preserve actual runtime-stop proof; absent/expired leases do not prove stop.

## Retention and deferred work

[Workspace retention](../../project-dossier/registers/workspace-retention.json)
owns dependency-based local retention classes and grants no deletion authority.
Keep receipt inputs and relocation records while referenced. Preserve both
packages, old ADRs, evidence, branches, bundles, archive baselines and origin
predecessors. Transient output review does not authorize automatic cleanup.
Private-input access controls and retention remain unqualified; outside Git is
placement, not proof of isolation.

[Remediation dispositions](../../project-dossier/conformance/remediation-register.json)
cover every reviewed concern without creating a task ledger.
[RAIDQ](../../project-dossier/machine-readable/raidq.json) records exact private,
Blueprint, private-control, migration, publication and runtime deferral details.
The remediation register uses closed RAIDQ references; it owns disposition,
not a second editable copy of those details. Plectarium already has an established
family contract; proposed new migration/adoption still needs accepted scope and
an accountable owner. Octon family migration and standalone-standard/upstream
generator work have separate records. Standalone publication does not depend on
Plectarium. These are not ordinary Texenda dependencies. Direct CLI remains
unqualified by desktop evidence. Hosted repository/CI creation remains WP-02 work
under existing external-effect authority.

## Machine-readable metadata

This strict JSON block belongs to this ADR; validators consume it directly.
There is no independently edited machine companion.

<!-- texenda-standalone-operating-contract -->
```json
{
  "schema_version": "texenda.standalone-operating.v1",
  "id": "OPS-WSM-0001",
  "owner_path": "docs/decisions/ADR-0007-standalone-workspace-operating-contract.md",
  "authority": "portable_workspace_operating_metadata_only",
  "permission_grant": false,
  "ownership_epoch": "external_state",
  "command_registry": ".agent/validators.json",
  "retention_policy": "project-dossier/registers/workspace-retention.json",
  "remediation_register": "project-dossier/conformance/remediation-register.json",
  "deferred_records": [
    "RAIDQ-0005",
    "RAIDQ-0006",
    "RAIDQ-0007",
    "RAIDQ-0008",
    "RAIDQ-0009",
    "RAIDQ-0010"
  ],
  "scopes": {
    "code": {
      "repository_only": true,
      "state_root_allowed": false,
      "live_state_checked": false,
      "generated_freshness": "unassessed"
    },
    "control": {
      "canonical_repository_required": true,
      "active_binding_required": true,
      "explicit_absolute_state_root_required": true,
      "implicit_discovery": false,
      "worktree_store_copy": false
    }
  },
  "ready_selection": {
    "source": "live_coordinator_ready",
    "selection": "explicit_task_consistent_with_current_objective",
    "empty_result": "inspect_status_and_dependencies_without_fallback",
    "resumption": "recorded_task_and_fence",
    "context_is_assignment": false
  },
  "path_roles": [
    {
      "id": "ROLE-0001",
      "path": "repo/",
      "anchor": "project_home",
      "information_role": "canonical_control",
      "tracking": "local",
      "requirement": "required_for_control",
      "retention_class": "RET-0001",
      "owner": "docs/decisions/ADR-0004-mapped-project-workspace.md",
      "lifecycle": "Retain current sources and preserved Git history; use reviewed successors.",
      "validation": "Source hashes, owners and supersession.",
      "recovery": "Recover preserved revision without history rewrite."
    },
    {
      "id": "ROLE-0002",
      "path": "worktrees/",
      "anchor": "project_home",
      "information_role": "candidate_code",
      "tracking": "local",
      "requirement": "conditional",
      "retention_class": "RET-0006",
      "owner": "tooling/coordination/templates/ASSIGNMENT.md",
      "lifecycle": "Keep until runtime stop and reference/evidence/recovery reconciliation.",
      "validation": "Exact paths, owner, actual stop and no retained dependencies.",
      "recovery": "Preserve unknown/referenced outputs, candidates and checkpoints."
    },
    {
      "id": "ROLE-0003",
      "path": ".agent/",
      "anchor": "repository",
      "information_role": "governance_and_derived_views",
      "tracking": "tracked",
      "requirement": "required",
      "retention_class": "RET-0001",
      "owner": ".agent/project.json",
      "lifecycle": "Retain current sources and preserved Git history; use reviewed successors.",
      "validation": "Source hashes, owners and supersession.",
      "recovery": "Recover preserved revision without history rewrite."
    },
    {
      "id": "ROLE-0004",
      "path": "docs/decisions/",
      "anchor": "repository",
      "information_role": "durable_decisions",
      "tracking": "tracked",
      "requirement": "required",
      "retention_class": "RET-0002",
      "owner": "docs/decisions/",
      "lifecycle": "Preserve decisions, sealed/source packages, evidence, archives, branches and bundles.",
      "validation": "Exact hashes, manifests and forward baselines.",
      "recovery": "Restore verified bytes; append corrections."
    },
    {
      "id": "ROLE-0005",
      "path": "docs/qualification/evidence/",
      "anchor": "repository",
      "information_role": "bounded_evidence",
      "tracking": "tracked",
      "requirement": "required",
      "retention_class": "RET-0002",
      "owner": "docs/qualification/evidence/",
      "lifecycle": "Preserve decisions, sealed/source packages, evidence, archives, branches and bundles.",
      "validation": "Exact hashes, manifests and forward baselines.",
      "recovery": "Restore verified bytes; append corrections."
    },
    {
      "id": "ROLE-0006",
      "path": "project-dossier/",
      "anchor": "repository",
      "information_role": "classified_information",
      "tracking": "tracked",
      "requirement": "required",
      "retention_class": "RET-0001",
      "owner": "project-dossier/ARTIFACT_CATALOG.json",
      "lifecycle": "Retain current sources and preserved Git history; use reviewed successors.",
      "validation": "Source hashes, owners and supersession.",
      "recovery": "Recover preserved revision without history rewrite."
    },
    {
      "id": "ROLE-0007",
      "path": "specs/texenda-handoff/",
      "anchor": "repository",
      "information_role": "sealed_product_authority",
      "tracking": "tracked",
      "requirement": "required",
      "retention_class": "RET-0002",
      "owner": "specs/texenda-handoff/01-foundation/authority-register.json",
      "lifecycle": "Preserve decisions, sealed/source packages, evidence, archives, branches and bundles.",
      "validation": "Exact hashes, manifests and forward baselines.",
      "recovery": "Restore verified bytes; append corrections."
    },
    {
      "id": "ROLE-0008",
      "path": "sources/handoff-1.1.0-20260914/",
      "anchor": "project_home",
      "information_role": "unpromoted_source_variant",
      "tracking": "local",
      "requirement": "required_for_control",
      "retention_class": "RET-0002",
      "owner": "project-dossier/provenance/sources.json",
      "lifecycle": "Preserve decisions, sealed/source packages, evidence, archives, branches and bundles.",
      "validation": "Exact hashes, manifests and forward baselines.",
      "recovery": "Restore verified bytes; append corrections."
    },
    {
      "id": "ROLE-0009",
      "path": ".texenda-location.json",
      "anchor": "repository",
      "information_role": "local_binding",
      "tracking": "ignored",
      "requirement": "required_for_control",
      "retention_class": "RET-0003",
      "owner": "tooling/coordination/schemas/state-location.schema.json",
      "lifecycle": "Retain one live ledger, binding and required lock/transaction material.",
      "validation": "Receipts, prefix, identities and pending transactions.",
      "recovery": "Existing explicit state-write/relocation recovery after proved stop."
    },
    {
      "id": "ROLE-0010",
      "path": "local/agent-state/texenda/",
      "anchor": "project_home",
      "information_role": "live_coordination",
      "tracking": "local",
      "requirement": "required_for_control",
      "retention_class": "RET-0003",
      "owner": "tooling/coordination/harness.py",
      "lifecycle": "Retain one live ledger, binding and required lock/transaction material.",
      "validation": "Receipts, prefix, identities and pending transactions.",
      "recovery": "Existing explicit state-write/relocation recovery after proved stop."
    },
    {
      "id": "ROLE-0011",
      "path": ".texenda/",
      "anchor": "repository",
      "information_role": "receipt_compatibility",
      "tracking": "ignored",
      "requirement": "required_for_control",
      "retention_class": "RET-0004",
      "owner": "project-dossier/transition/blueprint-adoption-crosswalk.json",
      "lifecycle": "Retain four receipt inputs and relocation records at referenced paths.",
      "validation": "Exact path/hash replay and recovery evidence.",
      "recovery": "Restore verified originals; never rewrite receipts."
    },
    {
      "id": "ROLE-0012",
      "path": "local/logs/workspace-relocation/",
      "anchor": "project_home",
      "information_role": "relocation_recovery",
      "tracking": "local",
      "requirement": "required_for_control",
      "retention_class": "RET-0004",
      "owner": "tooling/workspace/relocate_state.py",
      "lifecycle": "Retain four receipt inputs and relocation records at referenced paths.",
      "validation": "Exact path/hash replay and recovery evidence.",
      "recovery": "Restore verified originals; never rewrite receipts."
    },
    {
      "id": "ROLE-0013",
      "path": "archive/",
      "anchor": "project_home",
      "information_role": "retained_local_history",
      "tracking": "local",
      "requirement": "required_for_control",
      "retention_class": "RET-0002",
      "owner": "project-dossier/provenance/sources.json",
      "lifecycle": "Preserve decisions, sealed/source packages, evidence, archives, branches and bundles.",
      "validation": "Exact hashes, manifests and forward baselines.",
      "recovery": "Restore verified bytes; append corrections."
    },
    {
      "id": "ROLE-0014",
      "path": "local/private-inputs/",
      "anchor": "project_home",
      "information_role": "private_inputs",
      "tracking": "local",
      "requirement": "conditional",
      "retention_class": "RET-0007",
      "owner": "project-dossier/machine-readable/raidq.json",
      "lifecycle": "Retain placement and deny ordinary access pending RAIDQ-0006.",
      "validation": "Authorized metadata and synthetic tests; no actual content/size/hash.",
      "recovery": "No automatic chmod, copying or deletion."
    },
    {
      "id": "ROLE-0015",
      "path": "local/logs/, local/caches/, local/artifacts/",
      "anchor": "project_home",
      "information_role": "transient_run_outputs",
      "tracking": "local",
      "requirement": "conditional",
      "retention_class": "RET-0006",
      "owner": "docs/decisions/ADR-0007-standalone-workspace-operating-contract.md",
      "lifecycle": "Keep until runtime stop and reference/evidence/recovery reconciliation.",
      "validation": "Exact paths, owner, actual stop and no retained dependencies.",
      "recovery": "Preserve unknown/referenced outputs, candidates and checkpoints."
    },
    {
      "id": "ROLE-0016",
      "path": "WORKSPACE.md",
      "anchor": "project_home",
      "information_role": "machine_navigation",
      "tracking": "local",
      "requirement": "conditional",
      "retention_class": "RET-0001",
      "owner": "AGENTS.md",
      "lifecycle": "Retain current sources and preserved Git history; use reviewed successors.",
      "validation": "Source hashes, owners and supersession.",
      "recovery": "Recover preserved revision without history rewrite."
    },
    {
      "id": "ROLE-0017",
      "path": ".codex/config.toml",
      "anchor": "repository",
      "information_role": "runtime_defaults",
      "tracking": "tracked",
      "requirement": "required",
      "retention_class": "RET-0001",
      "owner": ".codex/config.toml",
      "lifecycle": "Retain current sources and preserved Git history; use reviewed successors.",
      "validation": "Source hashes, owners and supersession.",
      "recovery": "Recover preserved revision without history rewrite."
    },
    {
      "id": "ROLE-0018",
      "path": ".agents/",
      "anchor": "repository",
      "information_role": "optional_capability_packages",
      "tracking": "tracked_if_triggered",
      "requirement": "omitted_until_trigger",
      "retention_class": "RET-0001",
      "owner": "docs/agents/operating-guide.md",
      "lifecycle": "Retain current sources and preserved Git history; use reviewed successors.",
      "validation": "Source hashes, owners and supersession.",
      "recovery": "Recover preserved revision without history rewrite."
    },
    {
      "id": "ROLE-0019",
      "path": "Blueprint, Plectarium and Octon family sources",
      "anchor": "external",
      "information_role": "external_structural_sources",
      "tracking": "external",
      "requirement": "omitted_from_ordinary_dependencies",
      "retention_class": "RET-0002",
      "owner": "project-dossier/machine-readable/raidq.json",
      "lifecycle": "Preserve decisions, sealed/source packages, evidence, archives, branches and bundles.",
      "validation": "Exact hashes, manifests and forward baselines.",
      "recovery": "Restore verified bytes; append corrections."
    }
  ]
}
```
