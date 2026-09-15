# Texenda agent entry point

This tracked facade routes to existing Texenda authority; it does not create
permission, product semantics, readiness, a second task ledger, or a second
receipt chain.

From `/Users/jamesryancooper/Projects/texenda/repo`, run the complete ordinary
read-only validation:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
```

Then inspect the active ledger without changing it:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda status
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda ready
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda context WP-01
```

Continue in this order:

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
6. Prepare work with the local [assignment](../tooling/coordination/templates/ASSIGNMENT.md),
   [review](../tooling/coordination/templates/REVIEW.md), or
   [resumption](../tooling/coordination/templates/RESUME.md) template.

`.agent/` is governance and validation. Project-local `.agents/` capability
packages remain deliberately deferred by the reviewed adoption crosswalk.
Direct CLI model execution is not qualified by the desktop roster; qualification
evidence transfers only to the exact runtime/profile it names.
