# Texenda repository router

Start with [`.agent/START_HERE.md`](.agent/START_HERE.md). The reviewed facade's
[policy](.agent/policy.json) owns project-wide agent action classes and deny
boundaries; its [context contract](.agent/context.json) owns precedence and trust.
Both remain subordinate to current platform, sandbox, tool, and operator authority.

Texenda product semantics and topic ownership remain in the sealed
[handoff package](specs/texenda-handoff/README.md) and accepted scoped
[mapped-workspace ADR](docs/decisions/ADR-0004-mapped-project-workspace.md) plus
the other records it routes to. Preserve the sealed package byte-for-byte.
Read nested `AGENTS.md` files for affected paths; child instructions may narrow,
never weaken.

For assignments, review, interruption, or resumption, use the
[operating guide](docs/agents/operating-guide.md), existing
[coordinator](tooling/coordination/README.md), and current
[routing policy](tooling/coordination/routing-policy.json). Live tasks, leases,
receipts, roster, and budget remain in the selected external ledger—not `.agent`
or the dossier.

The GitHub repository remains private under
[ADR-0003](docs/decisions/ADR-0003-private-repository-and-bounded-github-actions.md)
and the [GitHub/CI policy](docs/operations/github-ci-policy.md). These links route
to their owners; this file does not duplicate or expand their authority.

Use the single [validation registry](.agent/validators.json). Report exact checks,
failures, limitations, runtime-stop state, and external effects without treating a
passing structural check as product readiness or gate clearance.
