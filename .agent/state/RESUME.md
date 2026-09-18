# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `0a3c09c535e99e3534ed8e20809f0ec3602ba73d783b883f527c422bf3818c42` at `2026-09-18T16:14:56+00:00`
- Source revision/tree: `2c96699dadd4318df28c3ff1254b0ca1f903e817` / `2560c943617576ed7b4a4686d29981a3ac3483fc`
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
