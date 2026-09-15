# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `e393135a44b4c84896e47c90ae776f37e92866f770b3e06fcf8877c9a9fae633` at `2026-09-15T16:51:11+00:00`
- Source revision/tree: `7df950f841460df9c56c240a449d0233112d3acf` / `9abed8f0116a9800796f4a1caa9f7e771aebb8d8`
- Source-scope SHA-256: `fb2a83c6ed2e6756e078ce74a3f302b1c6bd91f81b0f334950a74e749ed3361d`
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
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda context WP-01
```

Use the [resumption template](../../tooling/coordination/templates/RESUME.md)
when prior work was interrupted. If any digest is stale, refresh only after the
underlying authority is understood.
