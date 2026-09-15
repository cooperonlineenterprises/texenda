# Independent integrated-main audit: clean pre-implementation workspace

Verdict: **APPROVE the integrated repository outcome** at
`2ff536f5435ea32ec03c687adecae0a6f74da81b`, tree
`2f28c815f7a00c452b1997fb113a3918e553f1d2`.

Normal repository work is functionally equivalent to a clean setup using the
intended mapped architecture. Instructions, current ownership, ordinary checking,
ready-work inspection, assignment, review and resumption are discoverable without
learning migration history. Intentional history and recovery dependencies remain.

The complete owner request still has one manual app step: Codex's saved project
points to the non-Git project home. Open/add the canonical `repo/` folder and use
that project for future development. This audit does not claim that registration
has changed or that product/production readiness has been established.

## Exact integrated subject and reviewer

| Field | Observed value |
|---|---|
| Canonical repository | `/Users/jamesryancooper/Projects/texenda/repo` |
| Branch / revision | `main` / `2ff536f5435ea32ec03c687adecae0a6f74da81b` |
| Tree | `2f28c815f7a00c452b1997fb113a3918e553f1d2` |
| Origin | `https://github.com/cooperonlineenterprises/texenda.git` |
| Project home | `/Users/jamesryancooper/Projects/texenda`, not a Git repository |
| Independent reviewer | `/root/clean_setup_reviewer` |
| Integrator | `/root` |
| Candidate authors | `/root/clean_workflow_author`, `/root/clean_maintenance_author` |
| Integrated audit entry | `2026-09-15T18:14:52Z` |
| Latest explicit audit observation | `2026-09-15T18:22:59Z` |
| Later evidence-only entry | `2026-09-15T18:27:00Z` |

The reviewer is distinct from the candidate authors and integrator. The assigned
profile is T1 `gpt-6-astra/max`, exact `gpt-6-astra-max`,
`codex-desktop-collaboration`, subscription. Audit bounds are 50,000 tokens /
3,000 seconds. This later evidence-only follow-up has separate bounds of 20,000
tokens / 1,200 seconds. API allowance and spending are USD 0; no fallback,
downshift or child agent was used. Provider model introspection and measured
token accounting remain unavailable.

The exact live profile was rechecked during the audit and before evidence
authoring. It records client `26.901.41600 (build 7982)`, read/edit/test,
verification `2026-09-13T21:44:31Z`, expiry `2026-10-12T21:44:31Z`, and check
`desktop-profile-gpt-6-astra-max`. `Harness.qualified` confirms availability from
the owner-attested `docs/qualification/model-roster-v2.1.evidence.json`, SHA-256
`8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0`.
This is a dated observation, not a second roster or new qualification.

Routing-policy digest:
`61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0`.
Work-package digest:
`9ad162070c27e4c765ba145fc8a35d31dc288482453daaa39ec0bb6add8bd8d8`.

`git rev-parse --show-toplevel HEAD HEAD^{tree}`, `git branch --show-current`,
`git remote -v`, status and `git reflog show main` confirm the exact subject.
The main reflog records these fast-forwards:

- `338cd13505d6faffdb645c450b44ea9230aadd75` to
  `700565cd829871b04bde87e485c25d802505192c` through
  `merge cleanup/clean-workflow-20260915: Fast-forward`;
- `700565cd829871b04bde87e485c25d802505192c` to
  `2ff536f5435ea32ec03c687adecae0a6f74da81b` through
  `merge cleanup/clean-maintenance-20260915: Fast-forward`.

Main is exactly the previously independently approved evidence-bearing head;
there is no additional integration delta or semantic merge resolution.

## Ordinary entry and verification

The root router, `.agent/START_HERE.md`, validation/coordination guidance,
generated handoff, and non-authoritative `WORKSPACE.md` agree on the canonical
repository and explicit external state root. No wrapper silently chooses state,
initializes it, or falls back to a legacy store.

From the canonical repository, the exact ordinary command passed in 18.396 seconds:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
```

From the non-Git project home, the equivalent direct entry passed in 18.294 seconds:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B repo/.agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
```

`WORKSPACE.md` documents changing into the exact repository first and then using
the ordinary command. Both tested entry directories resolve the same code,
registry, state and main revision. `GIT_OPTIONAL_LOCKS=0` and bytecode suppression
were applied to audit commands.

Both full checks returned PASS with all ten dispatched registry commands exiting
0 and both refresh writers skipped. They ran the workspace contract, offline
adoption interpreter, facade/workspace/coordinator/sealed suites, both package
checksum validators, live state check and Git whitespace check. Each result
reported 136 JSON, one TOML and 21 Python files; 30 dossier paths, three instruction
files, 130 links and 538 hash-bound PASS/FAIL checks. Both package validators
passed 14/14 checks. All eleven generated outputs reconstructed exactly.

Generation:
`69d5520752b2779e30d2e9e9428812fa678dc3b932ea4d70e281ef1330874339`.
Source-scope SHA-256:
`b3adced634a9d427f3cb4b25cf350cf64a67fee52bbcf2aa04ae00e9471cdfe6`.

The bound coordinator `status`, `ready`, and `context WP-01` commands all exited
0. Status reports one completed WP and 43 planned WPs, all eleven exact profiles
available and zero declared API spending. Ready work is `WP-01`, `WP-18`.
WP-01 context is READY with twelve governing context files and T1/max author and
reviewer floors. The live query is not another readiness ledger or assignment.

The existing assignment, review and resumption templates retain exact scope,
qualification, evidence, independent review, remaining bounds and runtime-stop
requirements. Newcomers can prepare work from those routes; migration history is
not an ordinary prerequisite. Direct CLI execution is still unqualified by the
desktop roster, and the current runtime must be checked before each dispatch.

## Authority, history and compatibility

Current adoption PLAN-0001 through PLAN-0004 are completed with their scoped
evidence. Crosswalk v2 records `completed_current_contract` and current epoch
`external_state`. Its exact v1 predecessor remains at revision
`700565cd829871b04bde87e485c25d802505192c`, SHA-256
`689d5ffedb15938b25679c0cb9215bd7cac850b3b8f09e257a0f7a0c4fade00e`.
Dossier 1.3/supersession and the history classification remain coherent.

The retained transition procedure remains byte-exact at SHA-256
`1f5b0b1aa816f6bcd34f591a0b5f9f5b4e9d6e8bf35474ca77367418fb930919`.
Current navigation leads to current owners; prior procedure and ownership epochs
remain history. The earlier editor/Blueprint integration-before-final-audit timing
exception is explicitly preserved and was closed through a dated present audit,
not retroactive alteration of old evidence.

The reviewer revalidated all three new candidate-review envelopes against their
own exact subjects:

| Candidate | Review envelope SHA-256 | Required PASS checks |
|---|---|---|
| `48033f36b448167511bddd379fde04684918fdb1` | `40d520813d66f27c90d551e490080396067dc0363cb60791da3869ffcb5fc37a` | 23 |
| `0c0f202782720d9d7f34bc1d929d9df8a24868d1` | `08a0abf07c113220c80b197ba34e51b4bb55030c02a372be8a5f835b0f1a1803` | 17 |
| `59d16bc427840a3a35eaea07666eb473aacb3eda` | `d07cea3155bbbca31d410167bba9d1c3782f3ee3b6a909e9afb442eb73133b6c` | 23 |

The original access-time finding and missing-mapped-target finding remain
historical failures with verified corrective candidates. Their evidence was not
silently repurposed as approval of a later head.

All ten compatibility dispositions have exact owners, reasons, risks, triggers,
proof and recovery routes. Intentional retained differences include:

- non-Git project home with canonical `repo/` and external state/private inputs;
- sealed specifications plus scoped local ADRs and both source variants;
- hash-pinned sealed-v1 primitives and pre-binding-only defaults;
- four exact ignored receipt inputs, relocation recovery and absolute binding;
- preserved origin-v2 history and a checked active-config/example mirror;
- a small local origin interpreter and live `ready` query;
- omitted generic capability packages until a recurring need justifies them;
- retained branches, bundles, checkpoints and immutable review evidence.

No task, receipt, routing, decision, evidence, permission or product owner was
duplicated. No large harness rewrite was introduced for appearance alone.

Installed Blueprint 1.0.0 remains the selected structural reference. Clean
committed 4.2.0 retains PASS/PASS/FAIL qualification and is not adopted. Dirty
uncommitted 4.3.0 remains separate. RAIDQ-0005 names the external source maintainer,
expired-fixture and authentic-reviewed-seed blockers, exact retry trigger,
qualification commands, required proof and recovery. No new upstream source
qualification, repair, installation, upgrade or seed was performed.

## State, packages, private boundary and no-write proof

A 483-path snapshot covered canonical repository files including the four ignored
receipt inputs, external state, preserved source package and `WORKSPACE.md`
across both entry-directory checks. Content, path membership, mode, device/inode,
size, mtime and ctime were unchanged. No access-time changes were observed in that
interval; portable OS-managed atime stability nevertheless remains outside the
guarantee. Git internals, private inputs, other worktrees and disposable fixtures
outside measured roots were excluded. No timestamp restoration was attempted.

| Protected item | Value |
|---|---|
| `WORKSPACE.md` SHA-256 | `6d6a9f487698207480958c91fe129cc643423ac7dd5d1e5c78d3479faf7d15cf` |
| `.texenda-location.json` SHA-256 | `a92b6137856b7f9c2b3f13f69f4e6dc92ed4da1be82eec1ddf21188ebdde0365` |
| External state SHA-256 | `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235` |
| State version / receipts | `2.0` / 13 |
| Receipt tip | `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e` |
| Profiles / leases | 11 / 0 |
| Budget / cleared gates | USD 0 / empty gate map |
| Sealed manifest SHA-256 | `37fffb1a165cfa6b907e7433d617c06e1c64ff09cd282173f7d791cace2ac07e` |
| Source manifest SHA-256 | `8576bf08ec4f2a4718476eca70e6d1d5cb2b6be1af550bf5c20c692bcbaff715` |

The retained WP-00 evidence was replayed read-only through `Harness.recheck`:
eight submission, eleven review and five integration required PASS checks, 24
total. References/hashes and the historical integration candidate match. A
supplemental helper first used the wrong nested reference shape and raised
`KeyError: path`; inspection of the actual schema supplied the bounded correction.
The corrected replay passed without mutation. This is not new WP execution or
new runtime-stop proof for current actors.

`git diff --check 338cd13505d6faffdb645c450b44ea9230aadd75..HEAD` and protected
comparisons preserve sealed files, harness/routing/relocation, origin schemas/
record, `.codex`, and permission/context. Both package variants retain their
eleven differences. Editor version and WP-10/VAL-03 evidence remain gated.

Private checks used exact final-file existence and Git ignore/tracking only.
`local/private-inputs/kit/ohw/2026-09-14/subscribers.csv` exists outside Git;
the legacy repository-relative path remains ignored and untracked. No private
content, size, hash, copy, parse or directory listing was accessed, and no content
equality claim follows from these checks.

## Archive forward baseline

The exact external baseline is
`archive/integrity/2026-09-15-preimplementation/CURRENT-SHA256SUMS`, SHA-256
`b682602668d10e96e9c50fbf317d5e3eee4124f1db613e5c49bd86b281656fde`.
Its provenance SHA-256 is
`32e5ee34be5482ee8da28630690cca64720371ef63ebdd84a4cfc91b29de766f`.

After verifying these hashes and the manifest's 5,626 unique archive-only,
regular, symlink-free, traversal-free, non-private/non-CSV paths, the reviewer ran
from the project home:

```text
shasum -a 256 -c archive/integrity/2026-09-15-preimplementation/CURRENT-SHA256SUMS
```

All 5,626 files passed, with zero non-success lines, empty stderr and exit 0 in
0.654 seconds. Raw payload contents were not displayed. All 6,081 measured
archive file/directory metadata entries were unchanged, excluding OS access time.
No archive file or baseline was written. This establishes forward stability only;
missing pre-migration hashes cannot be reconstructed and future additions need
a new baseline. Raw artifacts retain their non-authoritative historical role.

## GitHub observations and external boundary

Fresh read-only observations on 2026-09-15 used:

```text
gh api --method GET repos/cooperonlineenterprises/texenda --jq '{name,private,visibility,default_branch}'
gh api --method GET repos/cooperonlineenterprises/texenda/branches --jq '{branch_count:length}'
gh api --method GET repos/cooperonlineenterprises/texenda/actions/workflows --jq '{total_count}'
gh api --method GET repos/cooperonlineenterprises/texenda/actions/permissions --jq '{enabled,allowed_actions}'
git --no-optional-locks ls-files -- .github/workflows
git --no-optional-locks ls-remote --heads origin
```

All commands completed successfully. Repository visibility is private;
`branch_count` is 0; workflow `total_count` is 0. The existing Actions setting
remains `enabled: true`, `allowed_actions: all`. The configured default branch
name is `main`, which does not mean a hosted branch exists. Tracked workflow and
hosted-head queries returned no entries. These observations match the expected
baseline and do not imply that a workflow was enabled or executed.

The reviewer issued no GitHub mutation, push, workflow dispatch, deployment,
publication, spending or external activation. Public documentation and GitHub
metadata were read only; no secret value or production data was inspected.
No product or external gate was passed by this structural audit.

## Codex registration: one manual action remains

The supported `list_projects` call returned:

- project ID `8445df3c-0057-4a15-a026-9ee972cc1293`;
- local label `texenda`, host `local`;
- path `/Users/jamesryancooper/Projects/texenda`;
- `isGitRepository: false`.

The saved project still points to the parent. `WORKSPACE.md` gives the bounded
manual step: in Codex, open/add the folder
`/Users/jamesryancooper/Projects/texenda/repo` and use that project for future
development. Registration was not updated by this audit.

Official OpenAI documentation was searched and fetched directly on 2026-09-15.
`developers.openai.com/codex/app/` redirected to the
[desktop app documentation](https://learn.chatgpt.com/docs/app), whose setup
guidance supports opening a folder as the work location. This is advisory product
context, not authority or proof that a particular local menu was activated.

The integrator reported the control refusal
`Computer Use is not allowed to use app com.openai.codex for safety reasons`.
The reviewer did not reproduce it because this audit explicitly excluded UI
actions. No application database, symlink or alternative control workaround was
used. The manual step remains an explicit completion limitation, not an inferred
successful registration or a request to override the safety boundary.

## Runtime and worktree handoff

The project home has no `.git` marker and Git root discovery there fails as
expected. All intended directory roles exist. Canonical `repo/` is the sole
integration checkout; three temporary worktrees are clean including ignored files:

| Worktree under project home | Head at audit |
|---|---|
| `worktrees/clean-workflow-20260915` | `700565cd829871b04bde87e485c25d802505192c` |
| `worktrees/clean-maintenance-20260915` | `2ff536f5435ea32ec03c687adecae0a6f74da81b` |
| `worktrees/clean-workflow-review-20260915` | `2ff536f5435ea32ec03c687adecae0a6f74da81b` |

The live-agent listing reports the maintenance author and inventory agent
completed; no author runtime is listed as live. Only the implementation lead
and this auditor are running. Exact state/lock `lsof` checks return empty output
with expected exit 1. All audit subprocesses and command sessions completed.
Clean temporary worktrees may be removed only after the parent observes this
later evidence-authoring reviewer runtime stopped; preserve branches and recovery
artifacts. No worktree removal is performed by this audit.

## Evidence-only successor boundary

Only this Markdown and its paired closed v2 envelope may be added in the later
evidence-only child commit with exact parent
`2ff536f5435ea32ec03c687adecae0a6f74da81b`. Every PASS envelope row binds this
Markdown's exact SHA-256. `TRN-WSM-0001` is the existing transition reference,
not a new task ledger or receipt. Containing commit/tree and file hashes are
reported separately to avoid self-reference.

Adding evidence makes the generated evidence index stale. The integrator must
refresh only declared views and obtain the required final exact-head audit.
This record does not approve its containing commit or a future head automatically.
The repository outcome is approved; manual Codex registration, future Blueprint/
CLI qualification, product implementation and external activation remain separate.
