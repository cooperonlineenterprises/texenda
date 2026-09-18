# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `9f4c2e709b6f26322c5619ea91e788136f148289fb1f04af52139761608e76a9` at `2026-09-18T16:29:57+00:00`
- Source revision/tree: `317799fbb3ff41fa5212874a738d119846a7fa39` / `7e1b80c384943770f0f91a1d540292ae27c4fbb3`
- Source-scope SHA-256: `41bc1260d9df67c214687910a7e5bde3a89f6696ef56c47089a8b5799d28d494`
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
