# Texenda agent entry point

This tracked facade routes to existing authority. It creates no permission,
product readiness, task ledger or receipt chain.

## Select the operation scope

In a code worktree or clean clone, run repository-only verification:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --scope code --all
```

Its result leaves live state, control operation and generated freshness unassessed.
It never reads a local binding, ledger, project-home source/archive/private path
or installed skill. Do not provide `--state-root` to code scope.

Full ordinary validation runs in canonical `repo/`. Read the ignored
`.texenda-location.json` and deliberately set `TEXENDA_STATE_ROOT` to its verified
absolute value. The local project-home `WORKSPACE.md` and generated
[RESUME](state/RESUME.md) may show expanded local commands. No wrapper discovers,
initializes or substitutes a ledger:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}"
```

Default and explicit control scope require the active canonical binding; missing
or incorrect roots fail closed. Then inspect the canonical ledger:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" status
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" ready
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" context "${TEXENDA_WORK_PACKAGE:?Select an ID from fresh ready output}"
```

Set `TEXENDA_WORK_PACKAGE` explicitly to an ID from fresh ready output that
matches the current objective. If no work is ready, inspect status/dependencies;
there is no fallback WP. For resumption use the recorded task and fence.
Context is not admission or assignment.

## Worktree inspection and handoff

A worktree owns candidate code. For live inspection, explicitly set
`TEXENDA_REPOSITORY` to the canonical absolute repo path and use its script
and its evidence root together:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B "${TEXENDA_REPOSITORY:?Set the canonical repository}/tooling/coordination/harness.py" --root "$TEXENDA_REPOSITORY" --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" --read-only status
env PYTHONDONTWRITEBYTECODE=1 python3 -B "${TEXENDA_REPOSITORY:?Set the canonical repository}/tooling/coordination/harness.py" --root "$TEXENDA_REPOSITORY" --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" --read-only ready
env PYTHONDONTWRITEBYTECODE=1 python3 -B "${TEXENDA_REPOSITORY:?Set the canonical repository}/tooling/coordination/harness.py" --root "$TEXENDA_REPOSITORY" --state-root "${TEXENDA_STATE_ROOT:?Set the verified absolute state root}" --read-only context "${TEXENDA_WORK_PACKAGE:?Select an ID from fresh ready output}"
```

The flag enforces a read-only invocation and rejects every mutation and
`context --out` before harness construction. It does not authenticate the caller
or prevent deliberately omitting the flag; policy and assignment scope separately
prohibit worktree control mutations. Never copy a binding, ledger or ignored
receipt inputs into a worktree. Canonical mutation remains a separately scoped
coordinator operation.

Read [root instructions](../AGENTS.md), [policy](policy.json),
[precedence/trust](context.json), [project hooks](project.json), and the single
[validation registry](validators.json). Read applicable accepted
[decisions](../docs/decisions/) and sealed
[topic owners](../specs/texenda-handoff/01-foundation/authority-register.json).
[ADR-0007](../docs/decisions/ADR-0007-standalone-workspace-operating-contract.md)
defines current operating metadata.

Prepare work with the existing [assignment](../tooling/coordination/templates/ASSIGNMENT.md),
[review](../tooling/coordination/templates/REVIEW.md), or
[resumption](../tooling/coordination/templates/RESUME.md) template.
The [dossier](../project-dossier/README.md) routes information and dispositions;
it grants no authority. Refresh discovery is
`python3 -B .agent/scripts/refresh.py --help`; actual refresh/recovery is an explicit
canonical control write after source changes are understood and committed.

`.agent/` is governance/validation. Optional `.agents/` capabilities remain
deliberately omitted until a recurring need. Direct CLI remains unqualified by
the desktop roster; qualification transfers only to its exact runtime/profile.
