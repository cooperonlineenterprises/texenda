# Phase-1 workspace relocation receipt

Information role: navigation to immutable observation evidence. Documentation
is not permission, live coordination state, review approval or product readiness.

The [sanitized relocation evidence](../../docs/qualification/evidence/2026-09-14-workspace-relocation.json)
records the independently rechecked physical result of the lead's serial moves.
The reviewed execution revision was `b99f71fbaba0183fa2857016819fb410cabc1160`,
tree `24fdd3f5c7e9b8b1a03c854210d2cc6427620477`. The parent remains non-Git;
`repo/` is the canonical checkout. `worktrees/` holds declared temporary work,
`local/` holds local operational material, `sources/` preserves imports, and
`archive/checkpoints/phase-0-20260914/` retains both bundles, state checkpoints
and three preserved reviewer caches. No checkpoint or package was deleted.

`repo/specs/texenda-handoff/` remains the sealed implementation authority.
`sources/handoff-1.1.0-20260914/` retains all sixteen original top-level entries
and 88 files, including two preexisting caches. Both 1.1.0 checksum sets pass;
the same eleven differing files remain distinct. The evidence binds every
manifest/checksum set and the complete source inventory. The editor wording
requires its separate future project-local amendment if reconciliation is pursued.

Phase 1 retained the entire ignored `.texenda/` inside `repo/`. Its live state
hash, receipt sequence/tip, qualification roster and zero budget/leases are
unchanged. The private CSV remains at its original repository-relative path,
verified only through existence, ignore and tracking checks. Its contents were
not opened, hashed, parsed, copied or logged. External state/private-input
relocation still requires the independently reviewed Phase-4 implementation.

The [exact adoption planner result](post-relocation-adoption-plan.json) reports
installed blueprint 1.0.0, high-assurance, with two literal collisions. The
[reviewed functional crosswalk](blueprint-adoption-crosswalk.json) continues to
govern `mapped-existing` adoption. Blueprint qualification limits and the
deliberate origin-schema successor remain unchanged; the stock generator did
not run.

The saved Codex project still targets `/Users/jamesryancooper/Projects/texenda`.
The exposed app tools provide no safe saved-project path-update operation.
Manual action: use Codex's project open/add action to select
`/Users/jamesryancooper/Projects/texenda/repo`, then start repository work there.
Keep the parent available for workspace navigation. No app database edit or
symlink substitutes for reopening the canonical checkout.

Run the local physical audit explicitly while Phase 1 is the live layout:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/workspace/validate_relocation.py --project-home /Users/jamesryancooper/Projects/texenda --expected-revision <exact-current-main> --allowed-worktree <each-declared-temporary-worktree>
```

Repeat `--allowed-worktree` for each temporary checkout; omit it when none
exists. This opt-in local audit is not a clean-clone CI dependency and is not
a final external-state validator. It reuses unchanged ledger validation with
stable byte checks because the current CLI `status`/`check` opens a writable
lock. The complete command results and read-only scope are retained in the
evidence. No product or external gate is passed by these structural checks.

Next: distinct Astra/max review of the exact receipt/validator candidate,
observed author/reviewer stop, serial local integration, then the bounded
facade and state-root work under the existing transition contract.
