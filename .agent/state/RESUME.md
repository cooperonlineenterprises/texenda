# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `47a355d965db9aaa8b3325591035921f8a1dbe03f0433cb4455038836d5ee20e` at `2026-09-17T16:37:36+00:00`
- Source revision/tree: `2cc13e3843c23f602e0af875192a43fbfacdedde` / `d4ab00be48e9d7fc86d29043a841507fba0fe08e`
- Source-scope SHA-256: `c40f765ab11112effd87a7bb7686fcd9e66beaed99dc4172431107d23c6a958b`
- Live-ledger SHA-256: `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`
- Receipt count/tip: `13` / `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e`
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
