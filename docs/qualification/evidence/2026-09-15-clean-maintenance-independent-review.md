# Independent review: clean workspace maintenance

Verdict: **APPROVE** with zero unresolved findings for corrected candidate
`59d16bc427840a3a35eaea07666eb473aacb3eda`, tree
`1124909e331b846e3bda1a60241d24451f731b74`.

This review covers the repository-local planner interpreter, current compatibility
dispositions, crosswalk v2, dossier 1.3, external Blueprint maintenance record,
forward archive provenance, validators/tests and generated views. It preserves
the rejected missing-target behavior as a finding on the earlier candidate and
records its exact correction. This is not a Blueprint upgrade, product readiness
result, external approval, or approval of a containing/future evidence head.

## Exact subject and independence

| Field | Value |
|---|---|
| Accepted base | `700565cd829871b04bde87e485c25d802505192c` |
| Base tree | `9fbc4035bbe7afe29c3682fc01387fe8282dff31` |
| Approved candidate | `59d16bc427840a3a35eaea07666eb473aacb3eda` |
| Approved tree | `1124909e331b846e3bda1a60241d24451f731b74` |
| Canonical full-index base-to-candidate diff SHA-256 | `23bb92c8c860cc4e17e290270dbc03418b53898871dad5a339fb751744f847d5` |
| Earlier candidate with P2 | `0a42d6e239133ddef9fe9499f88813d5273f2a1f` |
| Earlier candidate tree | `5d02f6a86c0d72dfb55f97616c624c58e03fec1a` |
| Canonical full-index correction diff SHA-256 | `298119b7467f71e57b21c15d441a91c2fd394fa43d78089a3dd415a54d3335a6` |
| Candidate author | `/root/clean_maintenance_author` |
| Independent reviewer | `/root/clean_setup_reviewer` |
| Integrator | `/root` |
| Reviewer worktree | `/Users/jamesryancooper/Projects/texenda/worktrees/clean-workflow-review-20260915` |
| Original review entry | `2026-09-15T17:37:25Z` |
| Corrected-review entry | `2026-09-15T17:52:48Z` |
| Evidence-only entry | `2026-09-15T17:57:33Z` |

The reviewer is distinct from the author and integrator. Parent assignments use
T1 `gpt-6-astra/max`, exact profile `gpt-6-astra-max`, desktop collaboration,
subscription billing. Bounds: initial review 50,000 tokens / 3,000 seconds;
corrected review 35,000 tokens / 2,100 seconds; this evidence-only follow-up
20,000 tokens / 1,200 seconds. API allowance and spending are USD 0. No fallback,
downshift, child agent or new live-ledger assignment was used. Provider token
measurement and independent executing-model introspection are unavailable.

The exact live profile was rechecked for each assignment; `Harness.qualified`
confirmed availability during review. It records client `26.901.41600 (build
7982)`, read/edit/test, verification `2026-09-13T21:44:31Z`, expiry
`2026-10-12T21:44:31Z`, and check `desktop-profile-gpt-6-astra-max`.
Its owner-attested roster evidence is
`docs/qualification/model-roster-v2.1.evidence.json`, SHA-256
`8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0`.
This is a dated observation, not a second roster or fresh qualification.

Routing-policy digest:
`61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0`.
Work-package digest:
`9ad162070c27e4c765ba145fc8a35d31dc288482453daaa39ec0bb6add8bd8d8`.

Canonical diff commands:

```text
git --no-optional-locks -c core.abbrev=40 -c color.ui=false diff --no-ext-diff --no-textconv --full-index --binary 700565cd829871b04bde87e485c25d802505192c 59d16bc427840a3a35eaea07666eb473aacb3eda | shasum -a 256
git --no-optional-locks -c core.abbrev=40 -c color.ui=false diff --no-ext-diff --no-textconv --full-index --binary 0a42d6e239133ddef9fe9499f88813d5273f2a1f 59d16bc427840a3a35eaea07666eb473aacb3eda | shasum -a 256
```

For the earlier candidate, canonical full-index serialization was
`8e38754214b6a802414dc488339b2f4b5a9378b9bb81bd5596eadb5c12247895`.
The assigned `eaf44423...` value was confirmed as the plain abbreviated-index
serialization. The metadata label was corrected; candidate identity did not
change because of that serialization distinction.

## Original P2 and verified closure

At `0a42d6e...`, `local_contract()` called `presence()` for mapped targets but
ignored a false result. Independent probes, including a physical disposable
fixture, removed only the synthetic
`tooling/coordination/templates/ASSIGNMENT.md`. Both self-check and stock-plan
interpretation could still report PASS. Stock mode returned
`stock_plan_validated: true` and continued reporting the functional mapping from
`.agent/checklists/task-closure.md` to the absent assignment template.

All real mapped targets existed; no current project file was missing. The
defect was a missing-target negative-path failure and prevented approval of that
candidate. Existing tests then covered absent mapping rows and stock partitions,
but not an absent physical mapped target. The reviewer did not edit the candidate.

The correction requires every non-null relative mapped target to exist. A
trailing slash declares a directory; otherwise a regular file is required.
Null mappings remain permitted only for deferred/not-applicable roles. The sole
absolute mapping is the exact archive checkpoint index. Its directory and
ancestors must exist without symlinks; only metadata is examined, with no archive
enumeration or content read by the interpreter.

The corrected 19-test interpreter suite passes. Independent physical-fixture
probes additionally exercised five cases in both self-check and stock modes:

- missing mapped assignment file;
- missing mapped template directory;
- directory in place of the mapped assignment file;
- regular file in place of the mapped `.agent/tests/` directory;
- symlink in place of the mapped assignment file.

All ten independent attempts were rejected with the expected missing-owner,
wrong-file/directory-type, or symlink error. Tests also reject missing, file or
symlink archive indexes and prove the valid synthetic archive is not opened or
enumerated. No project or archive payload was modified to run these probes.

## Interpreter and authority review

The complete initial 26-file candidate and the exact subsequent correction were
inspected against applicable root/nested instructions, facade contracts, accepted
ADRs, dossier owners and sealed boundaries. Existing immutable instructions and
evidence were reused only after their unchanged path scope was verified.

The normal interpreter self-check uses repository-owned validation code and an
explicit canonical root. It does not load or execute the installed Blueprint,
origin source checkout, or a command from stdin. The only permitted external
mapped index receives bounded metadata checks. It supplies no output-file,
apply, install, upgrade, qualification or seed-generation option.

Stock mode accepts at most one MiB of strict JSON from stdin. Validation rejects
duplicate keys, NaN/Infinity and exponent overflow; wrong schema/root/profile/
version/origin observation; duplicate, missing, extra, overlapping or wrongly
classified paths; invalid mapping roles; traversal, symlinks and private paths.
All 85 paths must form the exact observed partition. The stock origin summary
is retained as its limited observation while Texenda's unchanged local v3 origin
is separately validated. Output is a source-hash-bound, non-authoritative view.

The registry makes the offline interpreter required in ordinary checking. Tests
reject replacing it with installed source execution, a writing mode, or omission
from the ordinary check. The ordinary entry command and visible external state
selection remain intact. No second task, receipt, routing, decision, evidence,
permission, qualification or readiness owner is introduced.

## Crosswalk, retained compatibility and Blueprint maintenance

Crosswalk v2 retains exact v1 predecessor revision
`700565cd829871b04bde87e485c25d802505192c`, path
`project-dossier/transition/blueprint-adoption-crosswalk.json`, SHA-256
`689d5ffedb15938b25679c0cb9215bd7cac850b3b8f09e257a0f7a0c4fade00e`.
The neutral `maintenance_items` field preserves `DEFER-WSM-0001` and
`DEFER-WSM-0002`. The exact predecessor remains in Git rather than being rewritten.
Dossier 1.3 and its second supersession record agree with this transition.

All ten compatibility dispositions have an owner, reason, risk, trigger, proof
and recovery route. They retain sealed-v1 inheritance, pre-binding defaults,
four exact ignored receipt inputs, relocation recovery, explicit absolute state
binding, origin-v2 predecessor, checked config/example mirroring, live `ready`,
and intentional generic omissions. Stock origin interpretation is isolated in
the small local interpreter. None retires a receipt dependency or broadens a
named owner. Native harness consolidation is deferred until a demonstrated
defect and full behavioral/recovery proof justify it.

RAIDQ-0005 identifies the external Octon Mini / Project Blueprint source
maintainer, exact expired-fixture and missing-seed blockers, risk, retry trigger,
required evidence, intended clean working directory and all requalification
commands. The selected installed 1.0.0 remains structural only. Clean committed
4.2.0 retains source-contract/acceptance PASS and full-validator FAIL; dirty
uncommitted 4.3.0 remains separate. No authentic reviewed seed exists, no failure
is relabelled PASS, and no upstream modification or upgrade is authorized here.
The earlier source qualification was not rerun as part of this local review.

## Exact corrected-candidate validation

Commands ran in the detached reviewer worktree with
`PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`.

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s .agent/tests -p 'test_*.py' -v
env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tooling/workspace/tests -p 'test_adoption_interpreter.py' -v
git --no-optional-locks diff --check 700565cd829871b04bde87e485c25d802505192c..59d16bc427840a3a35eaea07666eb473aacb3eda
```

| Check | Corrected result |
|---|---|
| Exact ordinary complete check | PASS, exit 0, 19.888 seconds |
| Ten dispatched registry commands | All exit 0; both refresh writers skipped |
| Standalone facade suite | 36 tests, 50.265 seconds, PASS without skips |
| Standalone interpreter suite | 19 tests, 1.357 seconds, PASS |
| Independent mapped-target negatives | Ten denials across five cases/two modes |
| Registered workspace/coordinator/sealed suites | PASS |
| Both package checksum validators | PASS, 14/14 each |
| Parsing | 135 JSON, 1 TOML, 21 Python |
| Dossier/instruction/links | 30 paths, 3 instruction files, 130 links |
| Hash-bound PASS/FAIL checks | 514 |
| Generated reconstruction | All eleven outputs match |
| Diff/protected/history checks | PASS |

The registered run includes the full workspace suite, including the new five
mapped-target tests. On the earlier candidate the standalone workspace suite
had 110 passing tests in 2.008 seconds, and the standalone facade had 36 in
50.149 seconds; those passes did not conceal the independently discovered P2.
The corrected facade standalone run includes the full-check fixture skipped
during recursive aggregation.

Corrected generation:
`9a5278da0c9541cd4db75517f8268489350dfa3b391325808dff77a4366b12d4`.
Source-scope SHA-256:
`b3adced634a9d427f3cb4b25cf350cf64a67fee52bbcf2aa04ae00e9471cdfe6`.

Actual installed-planner JSON was piped directly to the corrected interpreter
using subprocess stdin, preserving bytes and checking both exit codes:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B /Users/jamesryancooper/.codex/skills/project-bootstrap/scripts/plan_adoption.py --target /Users/jamesryancooper/Projects/texenda/worktrees/clean-workflow-review-20260915 --profile high-assurance --format json | env PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/workspace/interpret_adoption.py --root /Users/jamesryancooper/Projects/texenda/worktrees/clean-workflow-review-20260915 --stock-plan -
```

Both exited 0 with empty stderr. The partition has 45 collisions and 40 candidate
paths. The stock origin retains `valid_shape_not_fully_validated`, null generic
version/kernel fields, and the high-assurance profile. All permission/write/
execution/qualification/upgrade/seed/private-content boundary flags remain false.

The clean generator dry run also exited 0 with 85 intended paths exactly matching
the crosswalk; its target remained absent:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B /Users/jamesryancooper/.codex/skills/project-bootstrap/scripts/scaffold_project.py --target /private/tmp/texenda-candidate2-review-dryrun-20260915 --project-name Texenda --profile high-assurance --dry-run
```

## Archive forward baseline

SRC-0008 matches the external forward baseline at
`archive/integrity/2026-09-15-preimplementation`:

- manifest SHA-256:
  `b682602668d10e96e9c50fbf317d5e3eee4124f1db613e5c49bd86b281656fde`;
- provenance SHA-256:
  `32e5ee34be5482ee8da28630690cca64720371ef63ebdd84a4cfc91b29de766f`;
- 5,626 recorded regular files, excluding `archive/integrity/` itself.

Before hashing archive payloads, the reviewer verified the exact manifest hash,
unique entry count, relative archive-only paths, absence of traversal/private
components/CSV suffixes, symlink-free ancestors and regular file types. From the
project home the recorded command was then run with captured output:

```text
shasum -a 256 -c archive/integrity/2026-09-15-preimplementation/CURRENT-SHA256SUMS
```

All 5,626 checks passed; zero non-success lines and empty stderr. The corrected
review run took 0.696 seconds. Before/after comparison of 6,081 covered file and
directory metadata entries preserved mode, device/inode, size, mtime and ctime.
OS-managed atime was outside that guarantee. Raw payload contents were not
displayed. No archive file, manifest or provenance record was changed.

This is a dated forward-only baseline. It cannot reconstruct historical equality
where pre-migration hashes do not exist; future archive additions require a new
baseline. Raw logs, bytecode, Git objects, sessions and bundles do not become
project source, evidence authority, permission, approval or readiness.

## Project, state and private preservation

A 367-path before/after snapshot surrounding the corrected full-check interval
found no changes to content, path membership, mode, device/inode, size, mtime or
ctime in the review worktree and external-state directory. Manifest atime advanced
as disclosed by the current portable contract. Concurrent read-only tests were
also active during the interval; no individual access-time update is attributed
to one reader. Shared Git internals beyond the worktree pointer, other worktrees,
private inputs and disposable fixtures outside the measured roots were excluded.

| State observation | Value |
|---|---|
| SHA-256 | `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235` |
| Receipts | 13 |
| Tip | `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e` |
| Profiles / leases | 11 / 0 |
| Budget / cleared gates | USD 0 / empty gate map |

Protected comparisons preserve existing review evidence, origin schemas/record,
`.codex`, harness/routing/relocation code, permission/context, accepted ADRs,
transition history and the sealed package. Both preserved package checksum
validators and workspace byte audit pass; all eleven variant differences remain.
The four ignored canonical receipt inputs retain these SHA-256 values:

- `.texenda/context/WP-00.json`:
  `e13a3eded54663caeb3c3d84ad1a968dde0a9b8eb247be8f6b73350ca8e5435e`;
- `.texenda/evidence/wp00-integration-verification.log`:
  `be034ce2eb69d9f943a2f78ded7915237c1abb4927335c8dd780f52da1f54e23`;
- `.texenda/evidence/wp00-integration.evidence.json`:
  `ba2c632509b41aae33f7efb02e2d07cff5d39882ec876b0bd9d860f02d42042e`;
- `.texenda/state.v1.a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a.json`:
  `a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a`.

Private handling was limited to exact final-file existence and Git ignore/tracking
checks. The final CSV exists under `local/private-inputs/kit/ohw/2026-09-14/`,
outside Git; its old repository-relative path remains ignored and untracked.
No private content, size, hash, copy, parse or directory listing was accessed.
No equality claim follows from those checks.

## Evidence-only handoff and limits

The worktree remained clean at the exact corrected candidate/tree. No project,
archive, package, private-input or live-state file was edited during review;
only disposable synthetic fixtures were modified for tests. No source upgrade,
global-skill change, external repository edit, network effect, push, deployment,
publication, spending, hosted workflow or product/external gate clearance occurred.
GitHub and Codex registration were not freshly queried by this reviewer.

All command sessions completed; no child agent or background job remains. The
parent must observe this evidence-authoring task's final stop before releasing
the worktree. This record does not claim its writer is stopped while authoring it.

Only this Markdown and the paired closed v2 review envelope may be added in this
follow-up, with exact parent `59d16bc427840a3a35eaea07666eb473aacb3eda`.
Every PASS/FAIL envelope row binds this Markdown's exact hash. `TRN-WSM-0001`
is the existing transition reference, not a new task ledger or receipt. The
containing commit/tree and file hashes are reported separately to avoid a hash
cycle. After preservation, the integrator must explicitly refresh declared views
and obtain an independent audit of that exact evidence-bearing head before local
integration and final main verification.
