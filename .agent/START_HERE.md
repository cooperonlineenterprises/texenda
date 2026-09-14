# Texenda agent entry point

This tracked facade routes to existing Texenda authority; it does not create
permission, product semantics, readiness, a second task ledger, or a second
receipt chain.

1. Read [root instructions](../AGENTS.md), then the machine-readable
   [permission classes](policy.json) and [precedence/trust rules](context.json).
2. Use [project hooks](project.json) and the single [validation registry](validators.json).
3. Inspect live task/receipt/roster state only through the
   [existing coordinator](../tooling/coordination/README.md). The files under
   [`state/`](state/RESUME.md) are generated projections.
4. Read only the applicable accepted [ADRs](../docs/decisions/) and sealed
   [topic owners](../specs/texenda-handoff/01-foundation/authority-register.json).
5. Use the [dossier](../project-dossier/README.md) for information routing,
   conformance, transition, provenance, and handoff—not authorization.

`.agent/` is governance and validation. Project-local `.agents/` capability
packages remain deliberately deferred by the reviewed adoption crosswalk.
