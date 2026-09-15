# Texenda ordinary handoff

Generated navigation only; documentation is not permission or live state.

1. Read [root instructions](../../AGENTS.md) and [`.agent/START_HERE.md`](../../.agent/START_HERE.md).
2. From the repository root, run the [registered read-only validation](../validation/README.md):

   ```text
   env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
   ```

3. Inspect the active ledger without writing:

   ```text
   env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda status
   env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda ready
   env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda context WP-01
   ```

4. Prepare work with the existing [assignment](../../tooling/coordination/templates/ASSIGNMENT.md),
   [review](../../tooling/coordination/templates/REVIEW.md), or
   [resumption](../../tooling/coordination/templates/RESUME.md) template. Do not
   create dossier tasks or receipts.
5. Read the [current observed state](../current-state/README.md). Use
   [transition](../transition/README.md) or [history](../history/README.md) only
   for maintenance, provenance, or recovery work.

Source revision/tree: `7df950f841460df9c56c240a449d0233112d3acf` / `9abed8f0116a9800796f4a1caa9f7e771aebb8d8`. Live ledger hash: `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`.
