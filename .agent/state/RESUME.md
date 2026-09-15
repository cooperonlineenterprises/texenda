# Resume ordinary Texenda work

Generated, non-authoritative projection. Documentation is not permission.

- Generation: `6918b3222b1b8a17e1e99ded9d17ed68edd511a901f70ee009b36541e6218927` at `2026-09-15T23:29:59+00:00`
- Source revision/tree: `385ce8eddef06fdc0ab9d46222e4c347fa1c11bd` / `6b57fa35b5afb7c00c2eb119b53ee1d0a524b3e8`
- Source-scope SHA-256: `4b9b92e7ba4983752abf7e110731e9202e49fbbc5e65d992acbf0ffe9c9afa2a`
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
