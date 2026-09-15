# Dossier authority

This file governs interpretation of dossier information only. Documentation is
not permission. Agent action classes and trust precedence are owned by
[`.agent/policy.json`](../.agent/policy.json) and
[`.agent/context.json`](../.agent/context.json).

One mutable concern has one owner:

| Concern | Authoritative owner | Dossier role |
|---|---|---|
| Product semantics, invariants, external gates | [`specs/texenda-handoff/`](../specs/texenda-handoff/) plus accepted scoped ADRs | Index only |
| Model routing | [`tooling/coordination/routing-policy.json`](../tooling/coordination/routing-policy.json) | Registered restriction |
| WP lifecycle, tasks, leases, receipts, live roster | Existing coordinator and selected external `state.json` | Generated projection only |
| Agent permission classes | [`.agent/policy.json`](../.agent/policy.json) | Active machine owner |
| Precedence and trust | [`.agent/context.json`](../.agent/context.json) | Active machine owner |
| Validation commands | [`.agent/validators.json`](../.agent/validators.json) | Single registry |
| Durable decisions | [`docs/decisions/`](../docs/decisions/) | Index only |
| Qualification/review evidence | [`docs/qualification/evidence/`](../docs/qualification/evidence/) | Hash index only |
| Current implementation state | Direct Git/build/harness evidence | Generated summary |
| Conformance findings | [`conformance/findings.json`](conformance/findings.json) | New authoritative concern |
| Adoption transition | [`transition/blueprint-adoption-crosswalk.json`](transition/blueprint-adoption-crosswalk.json) | New authoritative concern |
| Adoption plan | [`machine-readable/plan.json`](machine-readable/plan.json) | Completion/dependency record; not active work |
| Adoption RAIDQ | [`machine-readable/raidq.json`](machine-readable/raidq.json) | New authoritative concern |
| Adoption provenance | [`provenance/sources.json`](provenance/sources.json) | New authoritative concern |
| Standalone operating metadata | [ADR-0007](../docs/decisions/ADR-0007-standalone-workspace-operating-contract.md) | Scoped operating contract reference |
| Remediation dispositions | [conformance/remediation-register.json](conformance/remediation-register.json) | Complete review dispositions; not active tasks |
| Workspace retention | [registers/workspace-retention.json](registers/workspace-retention.json) | Local dependency classes; no deletion authority |
| Handoff | [`handoff/START_HERE.md`](handoff/START_HERE.md) | Generated navigation |

The transition crosswalk identifies `external_state` as the current epoch and
retains prior epochs as history. Generated views must identify source hashes and
freshness; conflicts are recorded rather than silently resolved.

Structured catalog owner references resolve through the crosswalk's existing scoped
owner sets. They provide navigation; symbols and local-role locators do not copy
Git facts, ledger data, product semantics or authority.
