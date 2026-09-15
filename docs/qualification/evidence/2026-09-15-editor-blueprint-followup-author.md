# Editor and blueprint follow-ups: author validation

Author candidate recorded 2026-09-15 04:07:10 UTC. This is evidence for
independent review, not self-approval, product qualification or upgrade authority.

## Exact candidate

- Base: `836e209020177267ccaa1c803b66779cd29d12ec`, tree
  `99fa9c7889c429b1dd28942b3f949051410bd727`.
- Source/evidence commit: `15075bcb0bdce8f6fc3f9195d01c9af67da78929`,
  tree `e1577b07582d4cc188f18a2cb0c2de56c3407fb4`.
- Tested first-refresh candidate: `d788fb7b88fb34d15f6a7167eef6dd448e81d8fc`,
  tree `75c506d8d80b906dbe80d236197c510c3c514052`.
- Canonical binary base-to-tested diff SHA-256:
  `289e5bb122b1f4c36956584fef7f1c497de1ec1cf675724dfa82067cf9ff59d9`.
- Source scope: `ed42a7f8fc518e5a111d82c10adc84278b8f0b4ff7d942bf1e54c5e48cb8ea0d`.
- Tested generation: `4e7a29d07b9d02dcc7e2bb453044abda5a93fa080cdc4606f77326b180910e5f`.

Diff serialization uses `git --no-optional-locks -c core.abbrev=40 -c color.ui=false
diff --no-ext-diff --no-textconv --full-index --binary BASE CANDIDATE`.

## Implemented scope and preserved boundaries

ADR-0005 is the sole local owner of the named reversible editor refinement.
It names the initial composer, versioned codec/document contract, approved
blocks, retained compiled outputs and fallback. Exact package version remains
null/UNVERIFIED and VAL-03 remains unpassed. Root instructions route to it.
Both handoff variants, every package byte and all eleven differences remain.

Origin v3 separates selected installed 1.0.0, exact clean committed 4.2.0
qualification failure, and historical dirty uncommitted working 4.3.0/218 entries.
Schema v2 is retained unchanged. Strict schema and evidence checks reject version
mixing, false qualification/adoption, lost FAIL checks or fabricated upgrade
seed/output/approval. Crosswalk, provenance, dossier version and affected
findings/RAIDQ reflect only those bounded facts. No 4.2.0 adoption occurred.

The five-file debug archive has its first verified current forward baseline.
The missing pre-move manifest and inability to reconstruct historical equality
remain explicit and tested. No raw debug/bytecode payload is promoted into source,
approval or readiness. Existing owner maps and historical evidence are preserved.

The coordination extension bindings are unchanged because none of their bound
files changed; its hash validation passes. No new dossier owner or file exists.
No canonical-main, live-ledger, binding, original Octon checkout, installed/global
skill, package/dependency, private-input, app or external-system write occurred.

## Upstream source qualification is still FAIL

The [observation record](2026-09-15-editor-blueprint-followup-observations.evidence.json)
and its [bound Markdown](2026-09-15-editor-blueprint-followup-observations.md)
retain the complete commands/results, exact clean source/bundle and debug hashes,
two non-mutating plan stops, and first-party retrieval dates.

Clean source contracts and acceptance pass; acceptance retains project-owned
demonstration requirements. The full clean-source validator exits 1 with exactly
one failing expired-authorization fixture, 19/20 in that sub-suite passing.
That FAIL is not converted into qualification, skipped away or fixed elsewhere.
The missing reviewed seed blocks the plan before mutation; supplied authority
arguments were not themselves validated as a grant. No upgrade apply ran.

Only the three authorized public documentation URLs were retrieved read-only
on 2026-09-15 UTC. No private GitHub repository/API or Codex UI action occurred.

## Required local commands and results

Worktree: `/Users/jamesryancooper/Projects/texenda/worktrees/editor-blueprint-followups`.
All Python commands use `PYTHONDONTWRITEBYTECODE=1`, `python3 -B`.

| Check | Exact command | Result |
|---|---|---|
| Origin negatives | `python3 -B .agent/tests/test_validate.py OriginV3Tests -v` | Exit 0; 7 targeted tests. |
| Follow-up negatives | `python3 -B tooling/workspace/tests/test_contract.py FollowupContractTests -v` | Exit 0; 8 targeted tests. |
| Facade suite | `python3 -B -m unittest discover -s .agent/tests -p 'test_*.py' -v` | Exit 0; 33 tests, no skips. |
| Workspace suite | `python3 -B -m unittest discover -s tooling/workspace/tests -p 'test_*.py' -v` | Exit 0; 85 tests. |
| Coordinator suite | `python3 -B -m unittest discover -s tooling/coordination/tests -p 'test_*.py' -v` | Exit 0; 184 tests. |
| Sealed suite | `python3 -B -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -p 'test_*.py' -v` | Exit 0; 39 tests. |
| Contract | `python3 -B tooling/workspace/validate_contract.py --check --audit` | Exit 0; 42 concerns, 85 paths, 35 types, 16 retained moves, 86 sealed/88 source files. |
| Sealed package | `python3 -B specs/texenda-handoff/10-validation/validate_package.py --checksums` | Exit 0; 14/14. |
| Source package | `python3 -B /Users/jamesryancooper/Projects/texenda/sources/handoff-1.1.0-20260914/10-validation/validate_package.py --checksums` | Exit 0; 14/14. |
| Canonical Harness | `python3 -B tooling/coordination/harness.py --root /Users/jamesryancooper/Projects/texenda/repo --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda check` | Exit 0; local integrity. |
| Refresh | `python3 -B .agent/scripts/refresh.py --refresh --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda` | Exit 0; exactly eleven existing outputs. |
| Check | `python3 -B .agent/scripts/validate.py --check --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda` | Exit 0; PASS. |
| Check all | `python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda` | Exit 0; nine nonwriters pass; two refresh writers skipped. |
| Preservation | `git diff --exit-code 836e209020177267ccaa1c803b66779cd29d12ec -- specs/texenda-handoff .agent/schemas/project-blueprint-origin.v2.schema.json .agent/extensions/texenda-coordination/extension.json tooling/coordination` | Exit 0; empty. |
| Whitespace/clean | `git diff --check`; `git status --porcelain=v1 --untracked-files=all --ignored=matching` | Exit 0; empty after source/refresh commits and checks. |

The standalone facade suite exercises its recursive check-all fixture; nested
check-all skips that one test to prevent recursive aggregation. The targeted
new tests cover origin version mixing/commit attribution, false qualification
and adoption, missing/relabelled failed checks, invented seed/apply, editor
pin/VAL-03 bypass, unsafe blocks/codecs, real synthetic byte mutation of both
package scopes, and debug historical overclaims.

Before this author-envelope addition the facade validates 131 JSON, one TOML,
19 Python files, 28 dossier paths, three instruction files, 111 links and
424 safe PASS/FAIL evidence bindings. Origin/schema/IDs, owner maps, extension
hashes and deterministic reconstruction of all eleven views pass.

Full captured commands/results are retained in
`/private/tmp/texenda-followup-author.EoUX4Q/tested-candidate-capture.json`, SHA-256
`52149759eb7f45f326408aacccad7f7a497f48e82a5f3c2d20e9567f24886a29`. This supplemental local capture is not a
second task, receipt or authority store.

## No-write, live and private boundary

The two facade commands were enclosed in a 829-entry snapshot;
all values matched before/after. Snapshot SHA-256:
`b292545d0de78e687768883e9fd80f213955fc3d0848fd3196279f438a80b394`. Changed paths: empty.

It covers both worktrees except Git internals; explicit state/binding/recovery/
journal/checkpoint/navigation files; the complete handoff source package; the
debug archive and clean-source bundle; and clean-clone Git identity/status.
Hashes, directory membership, mode/device/inode/size and lossless nanosecond
mtime/ctime match. Private directories/CSV files, atime, Git internals and
synthetic fixtures outside these roots are excluded. No worktree cache appeared
or needed relocation.

State hash remains
`b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`;
13 receipts, tip
`f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e`,
11 roster entries, zero leases/budget, null budget approval, empty gates and
WP-10 still planned. State/lock/binding metadata matches author entry. No receipt
was appended. Private verification used exact-path existence, old absence and
Git ignore/tracking scope only; no real CSV content or size was accessed.

Snapshot driver SHA-256:
`ab5040123b46d160001584a19a3e8bb01739e77436f4b82acb0629a352be043a`.
Exact source, for reproducibility rather than execution authority:

```python
#!/usr/bin/env python3
"""Read-only snapshot oracle for this bounded external-state evidence candidate."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

WORKTREE = Path("/Users/jamesryancooper/Projects/texenda/worktrees/editor-blueprint-followups")
PROJECT_HOME = Path("/Users/jamesryancooper/Projects/texenda")
REPO = PROJECT_HOME / "repo"
STATE = PROJECT_HOME / "local/agent-state/texenda"
EXPLICIT = [
    PROJECT_HOME / "archive/checkpoints/blueprint-qualification-20260915/octon-mini-4.2.0-5e2d302.bundle",
    PROJECT_HOME / "WORKSPACE.md",
    STATE / "state.json", STATE / "state.lock",
    REPO / ".texenda-location.json",
    REPO / ".texenda/state.v1.a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a.json",
    PROJECT_HOME / "local/logs/workspace-relocation/phase-4-state-relocation-journal.json",
    PROJECT_HOME / "local/logs/workspace-relocation/state-root-20260914.activated-moving.json",
    PROJECT_HOME / "local/logs/workspace-relocation/state-root-20260914.activation-complete.207c592fdadc82c9.json",
]
TREES = [
    WORKTREE,
    PROJECT_HOME / "archive/reviewer-caches/pre-fix-check-all-KHHptR",
    REPO,
    PROJECT_HOME / "sources/handoff-1.1.0-20260914",
]
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def measure(path):
    if "private-inputs" in path.parts or path.suffix.lower() == ".csv":
        raise RuntimeError("Private input excluded before metadata/content access")
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode):
        raise RuntimeError("Symlink in non-private snapshot scope")
    result = {"mode":info.st_mode, "device":info.st_dev, "inode":info.st_ino,
              "size":info.st_size, "mtime_ns":str(info.st_mtime_ns), "ctime_ns":str(info.st_ctime_ns)}
    if stat.S_ISREG(info.st_mode):
        flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
        fd = os.open(path, flags)
        try:
            opened = os.fstat(fd)
            if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                raise RuntimeError("Snapshot inode changed")
            parts = []
            while True:
                data = os.read(fd, 1024 * 1024)
                if not data:
                    break
                parts.append(data)
            result["sha256"] = digest(b"".join(parts))
        finally:
            os.close(fd)
        after = path.lstat()
        if (info.st_ino,info.st_size,info.st_mtime_ns,info.st_ctime_ns) != (after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):
            raise RuntimeError("Snapshot file changed")
    elif not stat.S_ISDIR(info.st_mode):
        raise RuntimeError("Nonregular snapshot input")
    return result
def snapshot():
    rows = {}
    for root in TREES:
        for directory, names, files in os.walk(root, followlinks=False):
            parent = Path(directory)
            names[:] = sorted(n for n in names if n != ".git")
            if "private-inputs" in names:
                raise RuntimeError("Unexpected private directory in declared non-private tree")
            rows[str(parent)] = measure(parent)
            for name in sorted(files):
                if name == ".git":
                    continue
                path = parent / name
                rows[str(path)] = measure(path)
    for path in EXPLICIT:
        rows[str(path)] = measure(path)
    for root in [WORKTREE, REPO, Path("/private/tmp/texenda-blueprint-qualification.BXFOTm/source")]:
        for arguments in [["status","--porcelain=v1","--untracked-files=all","--ignored=matching"],["rev-parse","HEAD","HEAD^{tree}"]]:
            result = subprocess.run(["git","--no-optional-locks",*arguments],cwd=root,capture_output=True,text=True,check=True)
            rows[str(root)+"/GIT:"+":".join(arguments)] = result.stdout
    return rows
def main():
    before = snapshot()
    commands = [
        ["python3","-B",".agent/scripts/validate.py","--check","--state-root",str(STATE)],
        ["python3","-B",".agent/scripts/validate.py","--check","--all","--state-root",str(STATE)],
    ]
    if len(sys.argv) > 1 and sys.argv[1] == "--check-only":
        commands = commands[:1]
    results = []
    for argv in commands:
        result = subprocess.run(argv,cwd=WORKTREE,capture_output=True,text=True,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"})
        results.append({"argv":argv,"cwd":str(WORKTREE),"exit_code":result.returncode,"stdout":result.stdout,"stderr":result.stderr})
    after = snapshot()
    changed = sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
    report = {"scope":"Entire follow-up and canonical worktrees except .git; exact non-private live/binding/journal/completion/checkpoint and WORKSPACE.md paths; complete handoff source package; debug forward archive and clean-source bundle; clean clone Git identity/status",
              "exclusions":["All private-input paths and CSV files","Git internals","atime","Temporary test fixtures outside these roots"],
              "before_entries":len(before),"after_entries":len(after),
              "before_snapshot_sha256":digest(json.dumps(before,sort_keys=True,separators=(",",":")).encode()),
              "after_snapshot_sha256":digest(json.dumps(after,sort_keys=True,separators=(",",":")).encode()),
              "changed_paths":changed,"all_equal":not changed,"commands":results,
              "private_content_accessed":False,"background_processes_started":False}
    print(json.dumps(report,indent=2))
    return 0 if not changed and all(row["exit_code"] == 0 for row in results) else 1
if __name__ == "__main__":
    raise SystemExit(main())
```

## Remaining limits and handoff

The candidate still needs distinct Astra/max review and separate integration.
Exact editor compatibility/version pinning remains WP-10/VAL-03 work. Clean
Octon source qualification and reviewed migration seeding remain blocked; no
upgrade or global change is made here. Codex UI follow-up remains root-owned.
No product/external readiness or historical debug equality is claimed.

A Python test-string escaping typo and an exact staging-path typo were corrected
before the full passing suites/commits. A sandbox-denied process query was
performed later through the normal approved scoped escalation to bound the long
source validator; no control was bypassed or source outcome weakened.
All source/test command sessions ended; no child agent or background job remains.
Parent must observe this author's final stop before scope release.

This immutable record binds the tested first-refresh subject. The subsequent
author-evidence and index-only commits retain the same source scope/ledger.
Their exact final HEAD/tree/diff and read-only checks are returned separately
to avoid a self-reference cycle. Project-bootstrap 1.0.0 was used only as the
high-assurance mapped-existing structural workflow; no stock generation ran.
