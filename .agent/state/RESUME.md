# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `bcba3bdc9a44be1d21366178a1992226fde0971183d47addf286e0fb17efb879` at `2026-09-16T22:59:59+00:00`
- Source revision/tree: `b29286d0343158643d5adacebbc391197910995a` / `3f19034c131d22ee566f0717d2634dc27ae3aa22`
- Source-scope SHA-256: `ef6447364e48c7cac2125609b6446cfa90e5ff7381c9bbe7b73ccb7bb8b8eec6`
- Live-ledger SHA-256: `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`
- Receipt count/tip: `13` / `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e`
- Live task/receipt/roster authority: `/Users/jamesryancooper/Projects/texenda/local/agent-state/texenda/state.json`

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
