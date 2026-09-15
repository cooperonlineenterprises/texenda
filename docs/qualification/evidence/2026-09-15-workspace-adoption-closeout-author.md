# Workspace adoption status closeout: author validation

Proposed author candidate, not independent approval. Recorded 2026-09-15 01:24:35 UTC.
This corrects only the integrated-main audit's bounded P2 stale-status source
finding. The exact earlier cutover review/integration/audit milestones are
complete; this correction remains unapproved until its own review and integration.

## Exact subjects and changed scope

- Author base: `e7632cf3644a40724a22ed5d121c2ad62a557a44`, tree
  `666cf97e37305f2c433d71f96feee02b5bff67d7`; its two audit additions are preserved.
- Canonical audited main remains `14682d798faed7cd398d21be3cf8076b84d5b0fe`,
  tree `09d8475a6fc746640edef52efa7c10b340a9299e`.
- Source correction: `acde40f41ca94cf3a6fe9117e59610a76f9875cf`, tree
  `699a78a94e8186544f445717ed7dc8576117c4b9`.
- Tested first-refresh candidate: `532cc30528226cae231329e2078656cff9ae5c8c`, tree `ab2f6bff76ad3de97ece3073c6061b858ab4ba3f`.
- Base-to-tested canonical binary diff SHA-256: `a3184d4b593164350cfce92173ed53041e70baef0622311285373bbfa1691f1d`.
- Source scope: `c856f1055e329d1ba01a34ab9cb49b8aeff2762aee9df3fcd03067e866ed23fe`.
- Tested generation: `892985fdecb5d2e5b9f2ddf9043cd38f21d8c14cba06077526bc082a3354d7a3`.

Canonical diff command:

```text
git --no-optional-locks diff --no-ext-diff --no-textconv --full-index --binary e7632cf3644a40724a22ed5d121c2ad62a557a44 532cc30528226cae231329e2078656cff9ae5c8c
```

The author changed only four mutable source owners and refreshed the existing
eleven generated files. This paired Markdown/envelope is subsequent immutable
author evidence; a final index-only refresh and exact-tip verification follow
without changing that source scope. No dossier owner or file was added.

| Source | Bounded result |
|---|---|
| `project-dossier/machine-readable/plan.json` | PLAN-0003/0004 record the exact completed prior cutover review/integration/audit; explicit status scopes exclude this new correction. PLAN-0001/0002 are unchanged. |
| `project-dossier/conformance/findings.json` | Only FIND-0001/0004/0006 now state conformance for the approved exact baseline. FIND-0002/0003 deferrals and FIND-0005 remain unchanged. |
| `project-dossier/machine-readable/raidq.json` | Only RAIDQ-0003 is controlled for the prior exact milestones. Future consequential revisions and this correction retain fresh-review requirements. |
| `project-dossier/transition/README.md` | Dated evidence routing, conditional closeout publication, manual Codex reopen, deliberate deferrals and no current remote/product claim. The historical procedure is byte-identical. |

No immutable receipt, author, review or audit record was rewritten, including
the audit's historical P2 FAIL. No code, policy, harness, package, live-state,
binding, private-input or external-system change occurred. `WORKSPACE.md` was
read and verified only; the integrator owns any later local navigation update.

## Hash-bound prior evidence

| Evidence | SHA-256 |
|---|---|
| `2026-09-15-external-state-cutover-review.evidence.json` | `f0f8331828497738f49a41adca6f0b1a1ed5273e3ad742b480a15e99bb8da138` |
| `2026-09-15-external-state-cutover-independent-review.md` | `355e6df7961c3f9ce8dfec80c5316d082f0999785c789aa0535a784b4b46dab1` |
| `2026-09-15-workspace-adoption-integrated-main-audit.evidence.json` | `525aba0b9a4785450c99db807f751d8c1bd622043485b56341aed55cd48c0a1f` |
| `2026-09-15-workspace-adoption-integrated-main-audit.md` | `e0f872eecb85ea424e15b4a9a39d041338fc50997f1ef66e142d8c3ce908d614` |

All four paths above are under `docs/qualification/evidence/`.
The existing coordinator's read-only `evidence(..., kind="review",
task="TRN-WSM-0001", candidate=exact_subject, require_pass=True)` validates
28 required cutover checks and 29 required audit checks. Their nonrequired
historical FAIL/NOT_RUN rows are preserved. This reads prior approvals; it
does not record or extend approval to this candidate.

The dated audit binds prior runtime stop and cleanup. Fresh exact-path/Git
checks confirm the two cutover worktrees remain absent, their migration branch
and commits remain retained, and only canonical main plus the assigned closeout
worktree remain. This does not claim the still-authoring closeout actor stopped.

## Required checks and observed results

Commands ran from
`/Users/jamesryancooper/Projects/texenda/worktrees/workspace-adoption-closeout`
unless their explicit root says otherwise, with `PYTHONDONTWRITEBYTECODE=1`
and Python 3.13.9. All results below describe the tested candidate above.

| Check | Exact command | Result |
|---|---|---|
| Facade suite | `python3 -B -m unittest discover -s .agent/tests -p 'test_*.py' -v` | Exit 0; 26 tests, no skips. |
| Workspace suite | `python3 -B -m unittest discover -s tooling/workspace/tests -p 'test_*.py' -v` | Exit 0; 77 tests. |
| Coordinator suite | `python3 -B -m unittest discover -s tooling/coordination/tests -p 'test_*.py' -v` | Exit 0; 184 tests. |
| Sealed suite | `python3 -B -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -p 'test_*.py' -v` | Exit 0; 39 tests. |
| Contract | `python3 -B tooling/workspace/validate_contract.py --check --audit` | Exit 0; 42 concerns, 85 paths, 35 types, 16 moves; 86 sealed/88 source files. |
| Sealed package | `python3 -B specs/texenda-handoff/10-validation/validate_package.py --checksums` | Exit 0; 14/14, no errors/warnings. |
| Source package | `python3 -B /Users/jamesryancooper/Projects/texenda/sources/handoff-1.1.0-20260914/10-validation/validate_package.py --checksums` | Exit 0; 14/14, no errors/warnings. |
| Canonical helper | `python3 -B /Users/jamesryancooper/Projects/texenda/repo/tooling/workspace/relocate_state.py --repo-root /Users/jamesryancooper/Projects/texenda/repo --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda verify` | Exit 0; active, exact ledger/count/tip. |
| Canonical Harness | `python3 -B tooling/coordination/harness.py --root /Users/jamesryancooper/Projects/texenda/repo --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda check` | Exit 0; local integrity. |
| Refresh | `python3 -B .agent/scripts/refresh.py --refresh --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda` | Exit 0; exactly eleven existing outputs. |
| Facade check | `python3 -B .agent/scripts/validate.py --check --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda` | Exit 0; PASS. |
| Full facade check | `python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda` | Exit 0; all nine nonwriters pass; both refresh writers skipped. |
| Whitespace | `git diff --check e7632cf3644a40724a22ed5d121c2ad62a557a44 HEAD` | Exit 0; empty. |
| Immutable/code/sealed | `git diff --exit-code e7632cf3644a40724a22ed5d121c2ad62a557a44 HEAD -- docs/qualification/evidence tooling .agent/scripts .agent/policy.json .agent/context.json .agent/validators.json specs/texenda-handoff project-dossier/transition/external-state-relocation-receipt.md` | Exit 0 before this new author record; empty. |
| Candidate clean | `git status --porcelain=v1 --untracked-files=all --ignored=matching` | Exit 0; empty. |

Check-all skips only its nested recursive full-check fixture; the standalone
26-test run exercises it. Strict facade checks passed 127 JSON, one TOML,
19 Python files, 28 dossier paths, three instruction files, 108 local links and
368 safe PASS/FAIL evidence bindings before this author-envelope addition.
Schema/origin/ID, owner/extension, source/evidence freshness and all eleven
deterministically reconstructed outputs passed. Generated resume/handoff
remain 13/11 lines and route to current sources.

The complete command/output capture is retained locally at
`/private/tmp/texenda-closeout-author.CVqlU3/tested-candidate-capture.json`, SHA-256
`7ccb137d7b536fb427bf81463d77ca2a583028160dd0a2b10eab9aac1cbac2ae`. This is diagnostic author evidence,
not a task or receipt store; the durable commands/results above stand on their
exact Git subject and this paired safe repository-relative envelope.

## State, privacy and mapped replay

State SHA-256 remains
`b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`;
active binding SHA
`a92b6137856b7f9c2b3f13f69f4e6dc92ed4da1be82eec1ddf21188ebdde0365`.
The external root is
`/Users/jamesryancooper/Projects/texenda/local/agent-state/texenda`.
Version 2.0, 13 receipts, tip
`f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e`,
roster 11, leases 0, budget 0, budget approval null, gates empty. State/lock
inodes `670498844`/`670332379`, device `16777232`, modes and mtime/ctime
are unchanged from author entry. No receipt was appended.

Canonical read-only `Harness._read`, `_validate_retained_evidence` and
`recheck(..., require_pass=True)` again validated WP-00 phases at sequences
1,2,4,5,7,8,9,10 and all 8+11+5 required retained evidence checks. State stayed
byte-identical, completed fence 1/no lease. The approved mapped demonstration
remains a replay of real existing completion, not a new WP run or model
qualification. The exact prior receipt and audit retain all evidence hashes.

For the real CSV, only `test -f` at the exact final/old paths and exact-path
Git ignore/tracking scope checks ran. The final file exists; old file is absent;
old ignore succeeds; external Git tracking rejects with exit 128 because the
destination is outside Git. There was no open, parse, hash, copy, content log,
size inspection or private-directory inventory. No private-content equality is
claimed. No GitHub, app, network or other external call was made.

## Lossless no-write oracle

The two facade commands were enclosed in a snapshot of both entire worktrees
except Git internals, explicit external state/binding/recovery/journal/checkpoint
and `WORKSPACE.md` paths, and the complete preserved source package.
All 802 entries matched; snapshot SHA-256 before and after was
`dc2d0d885a17cec011c2a8a8f32679307ab08abdc525f919bb4e4a91de0bddce`. Changed paths: empty.
Hashes, mode/type, device/inode, size, directory membership and mtime/ctime match;
nanosecond timestamps are decimal strings before reporting to avoid rounding.
Atime, private paths/CSV files, Git internals and synthetic fixtures outside the
declared roots are excluded. No worktree cache appeared or needed relocation.

`WORKSPACE.md` remained
`21873739871a3e8469dd6d5134d5d0cac4ec9d02716cfc1775143a634a4b7bb5`.
The snapshot driver is outside the worktree, SHA-256
`76ea3e4cf57e55282d75ef128002e159375e0f2c05264ac9718ed3fc8e79de46`.
Its exact source is retained below for reproducibility, not execution authority.

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

WORKTREE = Path("/Users/jamesryancooper/Projects/texenda/worktrees/workspace-adoption-closeout")
PROJECT_HOME = Path("/Users/jamesryancooper/Projects/texenda")
REPO = PROJECT_HOME / "repo"
STATE = PROJECT_HOME / "local/agent-state/texenda"
EXPLICIT = [
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
    for root in [WORKTREE, REPO]:
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
    report = {"scope":"Entire closeout and canonical worktrees except .git; exact non-private live/binding/journal/completion/checkpoint and WORKSPACE.md paths; complete preserved source package",
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

## Approval control and remaining boundary

Automatic approval review rejected the first unapplied patch because its
completion/conformance wording could imply approval of this new correction.
The worktree remained unchanged. Exact 28/29-check review evidence and Git
lineage were then verified; the revised patch explicitly scopes completion to
the prior `14682d7` subjects and labels this correction proposed/unapproved.
The same patch mechanism accepted the clarified version. No control was bypassed.

Within this closeout assignment, only the proposal's independent review and
separate integration, including resulting-head validation, remain NOT_RUN.
The historical plan milestones are complete for their exact subjects. Manual
Codex reopen is a separate follow-up; blueprint/editor/generic-capability
deferrals remain deliberate. No product/external gate is a claimed result or an
unperformed closeout step. No full-adoption approval transfers from this author
record. Installed Project Blueprint 1.0.0 remains structural-reference-only
under the applied high-assurance mapped-existing workflow.

All observed test/command sessions finished; no child agent or background job
was started. Parent observation must establish this author's final stop before
scope release. Final evidence/index-only descendant HEAD/tree/diff and final-tip
read-only proof are returned separately to avoid a self-reference cycle.
