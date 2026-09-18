# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `255ea68ded71a9bec0abe06caa22eea4c771e3eb716a1bd4a92e1a82b7317ddb` at `2026-09-18T16:19:27+00:00`
- Source revision/tree: `e2c3b059256d0485a970e2a1b9775f36c5e0fb6e` / `cc05171510b7b9fcc35ebfd62752c7abdc45bb96`
- Source-scope SHA-256: `41bc1260d9df67c214687910a7e5bde3a89f6696ef56c47089a8b5799d28d494`
- Live-ledger SHA-256: `fe218fc97325d3c255825d89cc0046e6ea27d38454c2a7dd06e09c0926d19bb0`
- Receipt count/tip: `14` / `e089594d853bc93a876aef100b779ef416bfaa82e5dacff84d027c6cb3eb8266`
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
