# Texenda workspace transition

This is the operator procedure for the owner-authorized structural migration.
It routes to the [accepted structural decision](../../docs/decisions/ADR-0004-mapped-project-workspace.md),
[ownership crosswalk](blueprint-adoption-crosswalk.json),
[move manifest](workspace-move-manifest.json) and immutable
[Phase-0 baseline](../../docs/qualification/evidence/2026-09-14-workspace-phase-0-baseline.json).
Documentation is not permission, runtime-stop proof, live state or a product
readiness result. This candidate freezes contracts; it executes no move or
authority cutover.

1. Review the exact architecture candidate and evidence with a distinct
   qualified Astra/max actor. Preserve its commit, review and branch. Recheck
   main, state/package hashes, roster expiry, leases, runtimes and worktrees.
   A changed main requires a fresh independently reviewed integration
   candidate. Reconcile every linked worktree and observe its runtime stopped.
   Create and verify a fresh content-addressed all-ref checkpoint covering the
   integrated architecture/review commits before relocation.
2. Run from `/Users/jamesryancooper/Projects` or the unchanged project-home
   root. Check every manifest source/type/hash and require every destination
   absent and symlink-free. Preserve all 16 exact handoff top-level entries
   by renaming each into `sources/handoff-1.1.0-20260914/`. Create only the
   manifest directories. Reserve `repo/` and `local/private-inputs/` as absent
   rename destinations; creating either empty first would change rename
   semantics. Rename `texenda-app` to `texenda/repo` with `.texenda/` intact.
   Create the non-authoritative `WORKSPACE.md` router. Record each completed
   move locally; do not use shell globs as destructive move targets.
3. Immediately verify the exact approved Git HEAD/tree/refs/remote and clean
   status, worktree paths, unchanged state SHA/receipts/roster/budget, both
   package checksum sets and all preserved source files. Verify the CSV only
   by existence, ignore rule and untracked status. Recheck GitHub through
   read-only calls. Record sanitized relocation evidence and distinct T1
   review. Reopen/re-register `/Users/jamesryancooper/Projects/texenda/repo`
   using supported Codex UI if a safe path-update API is unavailable; record
   the precise remaining manual action without editing the app database.
4. Run the installed read-only adoption planner again against the relocated
   repository. Its changed literal collisions do not replace the reviewed
   functional crosswalk. Record the result, recheck the crosswalk and obtain
   independent approval before adding the remaining `.agent/`/dossier paths.
5. Give the bounded facade/state-root implementation to qualified Sol/max
   only after these contracts are frozen. Use disjoint paths/worktrees and
   retain current routing/harness semantics. Activate policy, context and
   command ownership one concern at a time in the same reviewed candidate
   that removes duplicated old-owner prose. Add only the mapped subset;
   never run the stock generator. Review the exact candidate and its evidence
   with a distinct Astra/max actor, integrate serially, and rerun checks.
6. Follow the external-state contract below only after exact code approval
   and a fresh runtime/lease/lock freeze. Confirm all historical references
   remain valid. Create the ignored `.texenda-location.json` in `moving`
   status before the first active-state rename. Create the explicit state
   directory; move `state.json` and any stopped `state.lock` individually.
   Move `.texenda/private-inputs` as one directory into the absent
   `local/private-inputs/` destination. Leave historical `.texenda/evidence/`,
   `.texenda/context/` and v1 checkpoint inputs untouched. Reverify exact
   state bytes, receipt prefix/tip, roster and budget. Activate the binding
   only when exactly one live state file is present at its declared root.
7. Configure the local adapter to pass the bound directory explicitly to the
   harness. Recheck old/new state locations, ignore/tracking/private location
   without content access, and negative/resumption cases. Commit sanitized
   move evidence; append no ledger event if the state bytes did not change.
   Any proposed byte mutation needs a fresh exact reviewed migration that
   appends an owner-authorized receipt and preserves the existing chain.
8. Demonstrate one real mapped maintenance task through assignment,
   validation, independent review, integration and handoff using existing
   coordination/evidence owners. A synthetic lifecycle fixture alone is not
   operational adoption. Refresh derived integrity explicitly, run all
   registered checks on integrated main, and obtain final distinct Astra/max
   read-only review after the review evidence commit. Observe all reviewers
   stopped; remove only clean temporary worktrees, retaining branches/commits.
   Retain all checkpoints/source variants. Do not delete an old path while
   an active tool or saved project still uses it.

The installed planner command, rerun after relocation, is:

```text
python3 -B /Users/jamesryancooper/.codex/skills/project-bootstrap/scripts/plan_adoption.py --target /Users/jamesryancooper/Projects/texenda/repo --profile high-assurance --format json
```

The frozen external-state interface is deliberately narrow:

- `--root` continues to identify the repository and repository-relative,
  hash-bound evidence. Optional `--state-root` independently identifies the
  explicit state directory. Existing default operation works before a
  location binding exists. No command implicitly initializes state.
- Validate both roots, every binding/path component and every state/lock
  location; reject traversal, symlinks, nonexistent required paths and
  competing stores. An external state root must match the ignored root
  binding. After binding, missing `--state-root` and default `init` fail
  closed. A `moving` binding blocks ledger operations until verified recovery.
  Locking/writing is confined to the selected external state directory.
- The binding schema is project-local and closed. It contains only its
  schema version, migration ID, exact repository/state roots, `moving` or
  `active` status and historical baseline hash/count/tip. It never contains
  task records, events, roster rows, budget state, secrets or input metadata.
  Baseline fields describe the preserved migration boundary; they do not
  pretend subsequent authorized receipts must keep the same whole-file hash.
- Keep the current receipt-validation algorithm and all existing evidence
  rechecks. The exact `.texenda/` historical paths in the baseline stay valid
  relative to the repository; externalizing active state cannot redirect
  evidence lookup outside the repository or silently remap old receipts.
- Read-only commands must not create/open-for-write lockfiles, initialize
  directories, refresh projections or write bytecode/cache/report/timestamps.
  Read a stable snapshot and fail closed on concurrent changes. Mutating
  commands retain serialized locking and recheck state before replacement.
- A interrupted move is not a new ledger. The local move record and `moving`
  binding let T1 recovery determine which exact source/destination exists.
  Both present, both absent or mismatched state bytes stop recovery. Resume
  the remaining reviewed rename, or reverse completed renames into absent
  original paths. Preserve records/directories; no deletion or symlink bridge.

The implementation's required test contract includes default/external roots,
missing state, conflicting roots/bindings, symlink and traversal escapes,
receipt/hash corruption, concurrent locks, stale projections, private-input
exclusion and interrupted relocation rollback/resumption. Each deny must
have a meaningful negative case. The facade adds owner-map/no-second-ledger,
strict JSON/ID/reference/link/evidence-hash checks and refresh interruption
tests. Reuse the local/sealed suites and package validators.

Prove the final `.agent/scripts/validate.py --check` leaves tracked, untracked,
ignored, generated, cache, lock and timestamp state unchanged. Use complete
synthetic fixtures for private-input mutation/instrumentation tests; the real
CSV is never opened, parsed, hashed, copied or logged. Any live snapshot
exclusion required by that privacy boundary is named precisely; do not claim
an unobserved private-file content comparison. A permission/sandbox/runtime
control rejection is a finding, never a reason to bypass it.

Run this candidate's static contracts with:

```text
python3 -B tooling/workspace/validate_contract.py --check --audit
python3 -B -m unittest discover -s tooling/workspace/tests -v
python3 -B -m unittest discover -s tooling/coordination/tests -v
python3 -B -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -v
python3 -B specs/texenda-handoff/10-validation/validate_package.py --checksums
python3 -B /Users/jamesryancooper/Projects/texenda/10-validation/validate_package.py --checksums
git diff --check
```

The final source-validator command uses
`../sources/handoff-1.1.0-20260914/10-validation/validate_package.py` from
`repo/`. JSON/TOML/Python parsing, new local links, bound evidence hashes,
sealed byte comparison and exact Git status/worktree checks are also required.
Record each command, environment, exit result, scope and limitation. Passing
these structural checks clears no product or external gate. The editor
wording divergence and newer-blueprint qualification remain separate work.
