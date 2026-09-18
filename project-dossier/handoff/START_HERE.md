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
   [the integrated implementation path](../../docs/implementation/initial-product.md)
   for the initial synthetic product and later external qualification; its
   [ADR-0008 owner](../../docs/decisions/ADR-0008-integrated-initial-product-and-effective-plan.md)
   supersedes only named sealed plan/release/acceptance fields. Use
   [transition](../transition/README.md) or [history](../history/README.md) only
   for maintenance, provenance, or recovery work.

Source revision/tree: `317799fbb3ff41fa5212874a738d119846a7fa39` / `7e1b80c384943770f0f91a1d540292ae27c4fbb3`. Live ledger hash: `43531481205f0d410bdf12a242033823d1c66edef035e3bb0f4bd4e0d7592906`.
