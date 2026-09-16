# Texenda ordinary handoff

Generated navigation only; documentation is not permission or live state.

1. Read [root instructions](../../AGENTS.md) and [`.agent/START_HERE.md`](../../.agent/START_HERE.md).
2. From the repository root, run the [registered read-only validation](../validation/README.md):

   ```text
   env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}"
   ```

3. Inspect the active ledger without writing:

   ```text
   env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" status
   env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" ready
   env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" context "${TEXENDA_WORK_PACKAGE:?Select an ID from fresh ready output}"
   ```

4. Explicitly select an ID from fresh ready output; empty readiness has no fallback.
   For a code worktree use the [repository-only check](../../.agent/START_HERE.md).
   Prepare work with the existing [assignment](../../tooling/coordination/templates/ASSIGNMENT.md),
   [review](../../tooling/coordination/templates/REVIEW.md), or
   [resumption](../../tooling/coordination/templates/RESUME.md) template. Do not
   create dossier tasks or receipts.
5. Read the [current observed state](../current-state/README.md). Use
   [transition](../transition/README.md) or [history](../history/README.md) only
   for maintenance, provenance, or recovery work.

Source revision/tree: `8a3920e6c4fdb7a738b7044e56b3d48b7f918e52` / `ce8bf52393f4b00be8f2d27a1d1efbf1eb2c982b`. Live ledger hash: `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`.
