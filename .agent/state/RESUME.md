# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `38d5dde278cbf8d94172c58022e698b33abfb31adbbd5cc4e53df75bc8321d45` at `2026-09-18T17:33:18+00:00`
- Source revision/tree: `07684aeb166c4be236300c61569f416d7ecb5abb` / `baadb93d6ebb505a19ea721bf84a37bf77e09aff`
- Source-scope SHA-256: `927e3e5a4c4b2550864d68b0579ba9a05534135b594606d2f81d3d4dc674a655`
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
