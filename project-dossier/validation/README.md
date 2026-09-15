# Validation

The single [registry](../../.agent/validators.json) owns all commands.

Code worktrees and clean clones run only repository-source and synthetic checks:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --scope code --all
```

Code scope rejects state-root input, does not inspect local binding/live state,
project-home source/archive/private paths or installed skills, and reports
control/live/generated freshness unassessed.

Canonical `repo/` performs complete control validation with its deliberately
selected exact absolute state root:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}"
```

The active binding is required; missing/wrong/moving/symlinked/competing roots and
pending transactions fail closed. The full control check additionally verifies
local source/archive preservation, both package variants, live receipts and all
eleven generated outputs. The source-preservation command has no path fallback.

Both scopes perform no explicit project writes and preserve content, membership,
mode, size, mtime, ctime, caches, locks and existing outputs. OS-managed access time
(`atime`) may advance on read and is outside the portable no-write guarantee.
Synthetic suites write only disposable fixtures outside measured project roots.
No timestamp restoration is attempted.

Checks skip every refresh writer even under `--all`. Only explicit canonical
refresh/recovery writes derived outputs; `refresh.py --help` is read-only discovery.
Control validation rejects interrupted refresh and deterministically reconstructs
all eleven outputs. Code validation leaves their live freshness unassessed.

The [operating contract](../../docs/decisions/ADR-0007-standalone-workspace-operating-contract.md)
and [entry point](../../.agent/START_HERE.md) define assignment/review/resumption,
current ready-to-context selection and canonical-only control effects. PASS is
bounded evidence, not permission, product readiness or external gate clearance.
