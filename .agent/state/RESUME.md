# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `70a52880aa8c83af252140bd432492a3ad91b69a3e63e02e595b81268a0d9018` at `2026-09-18T17:13:31+00:00`
- Source revision/tree: `c1503e4c41cce5236f209849e228d37532f015d2` / `88d2b8944573e48b80b885b2b0626f7a54da975f`
- Source-scope SHA-256: `123084d348e22aed29466cc1751583ecd76f2126279ec9317bd461347b6e5be0`
- Live-ledger SHA-256: `43531481205f0d410bdf12a242033823d1c66edef035e3bb0f4bd4e0d7592906`
- Receipt count/tip: `15` / `0a01ea216c946654105b4eb23a1b312ca45694ecbc27e9fecf1877cc3548605d`
- Live task/receipt/roster authority: `/Users/jamesryancooper/Projects/texenda/local/agent-state/texenda/state.json`

For intended product scope and stage separation, use the
[integrated implementation path](../../docs/implementation/initial-product.md)
and [ADR-0008](../../docs/decisions/ADR-0008-integrated-initial-product-and-effective-plan.md).
Fresh coordinator status/context must bind the active effective plan; this view
is not a task ledger or a product acceptance result.

From the repository root, start with [`.agent/START_HERE.md`](../START_HERE.md)
and run:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
```

Then inspect the active ledger without writing:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda status
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda ready
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda context "${TEXENDA_WORK_PACKAGE:?Select an ID from fresh ready output}"
```

Select an ID explicitly from fresh ready output; empty readiness has no fallback.
For interrupted work use its recorded task and fence, then the
[resumption template](../../tooling/coordination/templates/RESUME.md)
when prior work was interrupted. If any digest is stale, refresh only after the
underlying authority is understood.
