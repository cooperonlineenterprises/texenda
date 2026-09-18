# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `565a5a940bcab1a87b2a08e74786f742ecee10bdd92ec7edc409c539905c111f` at `2026-09-18T16:11:28+00:00`
- Source revision/tree: `82c51a338ceacff0c4b7f688c6c34e8a1494a899` / `f584de3282477ab636a68db3dc563b30acae9ee7`
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
