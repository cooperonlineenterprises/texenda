# Workspace maintenance

Ordinary work starts at [`.agent/START_HERE.md`](../../.agent/START_HERE.md).
This guide covers occasional mapped-adoption maintenance. The
[crosswalk](../../project-dossier/transition/blueprint-adoption-crosswalk.json)
owns the 85 structural mappings and compatibility dispositions; it does not
grant permission or replace product, task, receipt or evidence owners.

Validation pins the complete 85-path inventory and every mapping disposition
to `git show 7de052690bbf3e2879f375c2b2e17207c7ee5bfe`, the immutable accepted
baseline. Agreement between two edited current lists is insufficient.

## Local planner interpretation

From the repository root, this self-check validates the current crosswalk and
origin-v3 record using repository-owned validators only:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/workspace/interpret_adoption.py --root "${TEXENDA_REPOSITORY:?Set the exact repository root}" --check
```

It is included in the ordinary facade check. It does not load the installed
Blueprint or execute any source path in the origin record. It checks all 85
mapped paths and preserves selected installed 1.0.0, failed clean 4.2.0 and
dirty uncommitted 4.3.0 as distinct facts.

For deliberate maintenance, a separately inspected stock 1.0.0 planner may
produce JSON for the exact same target. Pipe its output directly into the local
interpreter; neither command writes the target:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B "${TEXENDA_BLUEPRINT_PLANNER:?Select a separately inspected planner}" --target "${TEXENDA_REPOSITORY:?Set the exact repository root}" --profile high-assurance --format json | env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/workspace/interpret_adoption.py --root "${TEXENDA_REPOSITORY:?Set the exact repository root}" --stock-plan -
```

For a worktree, supply that worktree's exact absolute path to both commands.
The default interpretation is repository-only code scope; local preservation
remains unassessed. Full canonical control validation performs that local check.
The interpreter accepts at most one MiB of strict JSON on stdin and exposes no
output-file or apply option. It rejects duplicate keys, nonfinite numbers,
wrong target/profile/version, duplicate or missing mappings, incorrect path
partitions, traversal, symlinks and private-input paths. The stock origin summary
is retained as an observation alongside the validated local v3 interpretation.
Every non-null mapped target must exist as the declared regular file or directory
(a trailing slash declares a directory). Only null mappings with `deferred` or
`not_applicable` roles may lack a target. The retained absolute checkpoint mapping is historical metadata. Code scope
validates its declared disposition without resolving that local path. Complete
canonical control validation checks the actual archive directory and ancestors
without enumerating or reading its contents.
Output is a hash-bound, point-in-time view; it grants no permission and creates
no second ledger. Operating-system access times may advance when files are read.

## Retained compatibility and source qualification

The crosswalk's `compatibility_dispositions` explain why sealed-v1 inheritance,
pre-binding defaults, four exact ignored receipt inputs, relocation recovery,
absolute state bindings and origin-v2 history remain. The active config owns
defaults, its example is a checked mirror, and `ready` reads the live ledger.
No native harness rewrite is justified by the present maintenance evidence.

The source maintainer and exact future qualification commands are in
[RAIDQ-0005](../../project-dossier/machine-readable/raidq.json). The full 4.2.0
validator failure remains a failure, and an authentic reviewed upgrade seed is
still missing. This local interpreter repairs only the presentation of known
origin fields; it cannot qualify, install, adopt, upgrade or manufacture a seed.

For a real interrupted state move, use the retained
[relocation receipt](../../project-dossier/transition/external-state-relocation-receipt.md)
and the helper's `--help` under the existing T1 review/runtime-stop contract.
Routine validation never invokes relocation writers.
