# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `8fca60b8a528b424656b61fa197e3231c2766c475e70ad6e8fa66d45f47ed621` at `2026-09-15T16:19:29+00:00`
- Source revision/tree: `74c662436e8bd63ae41024fbe1968627e0305ec7` / `8b652835bd91ed332946628e2fbebce2dba8bdef`
- Source-scope SHA-256: `36d57188cfcf38cd8de13bff24f5e6d28d284157ce12d826664fc662ae39fb70`
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
