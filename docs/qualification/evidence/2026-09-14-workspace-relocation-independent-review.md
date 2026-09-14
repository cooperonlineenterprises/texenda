# Independent Phase-1 workspace relocation review

Verdict: APPROVE the exact candidate below. No open candidate findings remain.
Approval covers the relocation evidence, navigation and opt-in physical audit;
it does not attest facade adoption, external-state cutover, the future `.agent`
timestamp guarantee, product acceptance or any external gate.

| Binding | Exact value |
|---|---|
| Base | `b99f71fbaba0183fa2857016819fb410cabc1160` |
| Base/canonical-main tree | `24fdd3f5c7e9b8b1a03c854210d2cc6427620477` |
| Candidate | `2f611948ca0f191ba0efc3478bc463644fde09f8` |
| Candidate tree | `a3d40c7338d0470b7cd7ff7527722d89109cade2` |
| Full binary diff SHA-256 | `626e1a8324a58daa7d1fea7ef6e5bd6408d84f254f4e0cd8fa292cf9675fef4b` |
| Author | `/root/workspace_relocation_author` |
| Reviewer | `/root/review_workspace_relocation` |
| Move executor/integrator | `/root` |
| Review worktree | `/Users/jamesryancooper/Projects/texenda/worktrees/workspace-relocation-review` |

The reviewer is a different actor from both author and integrator. The assigned
route is `gpt-6-astra-max`, T1, max effort, desktop collaboration, subscription,
with a 3,000-second/80,000-token allocation and zero API allowance/spend. Live
qualification was independently rechecked at `2026-09-14T16:32:22.825284Z` and
during subsequent stable ledger checks. Its expiry is
`2026-10-12T21:44:31Z`; the roster evidence hash is
`8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0`.
Direct `/usr/libexec/PlistBuddy` reads of
`/Applications/ChatGPT.app/Contents/Info.plist` independently returned
`com.openai.codex`, `26.901.41600`, build `7982`. Provider-level executing-model
introspection and a provider token meter remain unavailable.

The full eight-file diff, both new validation logs, complete author evidence,
post-relocation plan, receipt, physical-audit implementation/tests, applicable
instructions and accepted ADRs were inspected. The reviewed crosswalk and
move manifest were read in full. The `project-bootstrap` skill's high-assurance
references informed the review of mapped adoption and information ownership.
No generic scaffold was installed, no origin record was fabricated and no
product authority was imported from another project.

The exact predecessor `7b758abd63d62260b4fa95c89eb537d0d9c856c4` was preserved
and its validator was executed from its Git bytes in memory. With this declared
detached reviewer worktree it fails at `symbolic-ref HEAD`, as expected. The
candidate correction accepts the declared detached worktree and reports new
post-checkpoint refs while preserving all original ordinary refs and archived
worktree-head commit objects. A retained branch need not be deleted when its
worktree stops. This is a justified compatibility correction and grants no
mutation authority. The earlier pseudo-ref/ancestry assertion errors remain
disclosed in the immutable author log.

## Independently observed result

The project home is non-Git and has no parent `AGENTS.md`. `repo/` is the ordinary
canonical checkout, on clean main at the base above. `worktrees/`, `local/`,
`sources/` and `archive/` have the reviewed roles. `WORKSPACE.md` is navigation
only, routes to `repo/AGENTS.md`, and hashes to
`21873739871a3e8469dd6d5134d5d0cac4ec9d02716cfc1775143a634a4b7bb5`.
The old `/Users/jamesryancooper/Projects/texenda-app` and old temporary checkpoint
path are absent. No invalid old linked-worktree path remains. The only linked
checkouts are canonical main, the stopped author's evidence worktree, and this
detached reviewer worktree.

All 16 source entries and 88 regular files, including both preexisting source
caches, match the approved baseline. Both packages retain 86 package files,
version 1.1.0, and exactly the same 11 differences. The source remains unpromoted
at `sources/handoff-1.1.0-20260914/`; `repo/specs/texenda-handoff/` remains sealed
implementation authority. Their common manifest SHA-256 is
`bcb7488ecf2ac42b4b33e478918e7ce6c35d0bdc04b208ddd9ed66622b468b7f`.
Source checksum-set SHA-256 is
`8576bf08ec4f2a4718476eca70e6d1d5cb2b6be1af550bf5c20c692bcbaff715`;
sealed checksum-set SHA-256 is
`37fffb1a165cfa6b907e7433d617c06e1c64ff09cd282173f7d791cace2ac07e`.
The complete source inventory hashes to
`9be3c385dccdcb6f735993dc0fe24a6dcab07f8af4fcf1bd2c5fac58786ee4c4`.

All seven archived artifacts match their recorded hashes: the original and
fresh Git bundles, state JSON checkpoint, scoped coordination archive and three
reviewer caches. Both bundles verify. The fresh bundle SHA-256 is
`f94b0e81858197e5d0419cf7170650f889263602aa35b1d1e7e8710468064897`.
It retains 29 ordinary refs, `HEAD`, and four archived worktree-head pseudo-refs.
The archived detached review commits remain present without implied integration.
The only new ordinary ref is the authorized relocation-evidence branch pointing
to the candidate. The local journal hashes to
`807bc10b7d66dc60c807152db374b85fbe308e94fcc0a97ab8839f011f5c51c8`
and binds all 18 completed moves to the approved base/tree and state boundary.

The live state remains in `repo/.texenda/state.json`, with its complete ignored
compatibility inputs still present. Before/after SHA-256 is
`b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`.
Version is 2.0, receipt count 13, tip
`f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e`,
and roster canonical digest
`a23705178b39e8d0dd194abd4cf6e42fc20be404739d0e28e0ca9b221c80ddcf`.
All 11 exact profiles revalidate; leases, API budget, declared API allocations
and cleared gates are zero. Existing receipt and retained-evidence validators
were used without the legacy writable lock-opening `status`/`check` commands.
The planned external state directory, external private directory and location
descriptor remain absent. No receipt was appended or rewritten.

The CSV was checked only for exact-path existence, `.gitignore:1:.texenda/`,
untracked status and location. It remains at
`repo/.texenda/private-inputs/kit/ohw/2026-09-14/subscribers.csv`. Its contents
were never opened, hashed, parsed, copied or logged. The entire private subtree
was excluded from metadata snapshots. The coordination archive was checked by
member names only: nine members, no private-input or CSV members.

The installed read-only planner reproduces the committed plan byte-for-byte:
SHA-256 `fa3144f5a622d1fcaffaa768d74e2f9b50d520f8614401fe5af87a4503710c15`,
blueprint 1.0.0, high-assurance, with two literal collisions and 83 other paths.
The existing 42-concern/85-path/35-type crosswalk remains controlling.
`mapped-existing` and structural-reference-only qualification are truthful;
the newer-source qualification and origin-schema successor remain later work.

## Commands and results

Commands ran in the reviewer worktree unless an absolute path is shown. Every
Python interpreter inherited `PYTHONDONTWRITEBYTECODE=1` and used `-B`.

| Command or exact procedure | Result |
|---|---|
| `python3 -B -m unittest discover -s tooling/workspace/tests -v` | 43 PASS |
| `python3 -B -m unittest discover -s tooling/coordination/tests -v` | 132 PASS |
| `python3 -B -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -v` | 39 PASS |
| `python3 -B specs/texenda-handoff/10-validation/validate_package.py --checksums` | 14 PASS |
| `python3 -B /Users/jamesryancooper/Projects/texenda/sources/handoff-1.1.0-20260914/10-validation/validate_package.py --checksums` | 14 PASS |
| `python3 -B tooling/workspace/validate_contract.py --check --audit` | PASS: 42 concerns, 85 paths, 35 types, 16 moves, 143 qualification check bindings; 87 JSON, 1 TOML, 12 Python; 13 registry links, 86 sealed/88 source files |
| `python3 -B tooling/workspace/validate_relocation.py --project-home /Users/jamesryancooper/Projects/texenda --expected-revision b99f71fbaba0183fa2857016819fb410cabc1160 --allowed-worktree /Users/jamesryancooper/Projects/texenda/worktrees/workspace-relocation-evidence --allowed-worktree /Users/jamesryancooper/Projects/texenda/worktrees/workspace-relocation-review` | PASS, exit 0 |
| Same physical command with `--expected-revision 2f611948ca0f191ba0efc3478bc463644fde09f8` | Expected rejection, exit 1: `canonical revision changed` |
| Exact predecessor validator loaded using `git show 7b758abd63d62260b4fa95c89eb537d0d9c856c4:tooling/workspace/validate_relocation.py` and executed in memory against both declared worktrees | Expected rejection: `Git check failed: symbolic-ref HEAD` |
| `python3 -B /Users/jamesryancooper/.codex/skills/project-bootstrap/scripts/plan_adoption.py --target /Users/jamesryancooper/Projects/texenda/repo --profile high-assurance --format json` | Exact committed bytes match |
| `git --no-optional-locks diff --no-ext-diff --no-textconv --full-index --binary b99f71fbaba0183fa2857016819fb410cabc1160 2f611948ca0f191ba0efc3478bc463644fde09f8` piped to `shasum -a 256` | Exact assigned diff digest matches |
| `git --no-optional-locks diff --check b99f71fbaba0183fa2857016819fb410cabc1160..2f611948ca0f191ba0efc3478bc463644fde09f8`; `git --no-optional-locks diff --check` | PASS |
| `git --no-optional-locks diff --exit-code 36b74e9e1ca6353b3d642136fa70b7d2ac950e08 -- specs/texenda-handoff` | PASS, exit 0 |
| Nine input/output hashes plus correction-log hash recomputed; all changed Markdown links resolved | PASS; nine changed-file links |
| `git --no-optional-locks ls-files -z AGENTS.md tooling/coordination/ .codex/ docs/agents/ docs/operations/` and old absolute-path search in the returned files | 21 sources; zero active old-checkout dependencies |
| `lsof -F pcfn` on canonical `state.json` and `state.lock` | No holders, exit 1; supporting observation, not runtime-stop proof |

A broader independent probe snapshotted 1,871 project paths, including Git,
ignored/cache files and directory metadata, excluding the whole private subtree.
The candidate's mode/size/mtime/ctime guarantee passed; names and inodes also
remained equal. A Python audit hook rejected write-capable opens and filesystem
mutations and prohibited private/CSV content opens. No such attempt occurred.
Live state bytes remained equal. The full timestamp probe FAIL is retained:
ordinary Git reads changed only `atime_ns` on these six paths, reproduced at
`2026-09-14T16:35:59.036952Z`:

- `repo/.git/index`
- `repo/.git/objects/24/fdd3f5c7e9b8b1a03c854210d2cc6427620477`
- `repo/.git/objects/60/9ddda6da96ddf2460925cc759db724acd70d59`
- `repo/.git/objects/66/6b6da286bacbd7e02d6d3ca27b3e6c2aa81b1a`
- `repo/.git/objects/b9/9f71fbaba0183fa2857016819fb410cabc1160`
- `repo/.git/objects/c6/220627cb84ea0862323d14dda2a1b72e466e01`

This is an explicit candidate limitation, not an unreported passing result:
the author expressly excludes access-time equality and the future `.agent`
check from Phase-1 claims. It is not an open defect in the approved Phase-1
candidate. The later `.agent` acceptance must resolve or precisely bound its
timestamp behavior; it must not inherit a full timestamp PASS from this review.
The hook covers the Python process; Git subprocess observations are bounded by
the filesystem snapshots, not a claim of system-wide syscall tracing.

Four independent `gh api --method GET` calls checked
`repos/cooperonlineenterprises/texenda`, its `branches?per_page=100`,
`actions/workflows` and `actions/permissions`. Results: private true/visibility
private, configured default branch `main` with zero hosted branches, zero
workflows, and unchanged `enabled: true`, `allowed_actions: all`,
`sha_pinning_required: false`. No tracked workflow exists. The remote remains
`https://github.com/cooperonlineenterprises/texenda.git`. No remote write or push
was performed by this reviewer.

The app's read-only project listing independently confirms saved Texenda project
`8445df3c-0057-4a15-a026-9ee972cc1293` still targets the non-Git project home.
Available app-tool metadata exposes no saved-project path update. The exact
remaining action is to open/add `/Users/jamesryancooper/Projects/texenda/repo`
through Codex's project control. No app storage or registration was edited.

## Limits and handback

The pre-move stop observation is explicitly attributed to the parent dispatcher;
this reviewer did not witness it retrospectively. Current collaboration state
independently shows the relocation author and final architecture reviewer
completed. The journal, approved manifest, checkpoints and actual byte-preserved
layout independently corroborate the physical result. A lease or `lsof` absence
alone is not treated as runtime-stop proof.

Facade/origin-schema implementation, generated projections, a real mapped task
lifecycle, external state/private-input movement, final integrated-main review,
product checks and external gates are NOT RUN here because they are subsequent
work. Both editor wordings stay preserved; semantic reconciliation remains the
separate future project-local amendment task. No second task, decision, evidence,
roster, routing or receipt authority was introduced by this candidate.

No candidate file was edited. The only reviewer additions are this Markdown
and its JSON review envelope, left uncommitted for the parent. All commands have
completed; no child agent or background command remains. The reviewer stops
after checking those two artifacts. The parent must observe completion before
scope release or worktree removal, preserve the candidate/review evidence, and
obtain the required final read-only review after adding evidence. Integration
and subsequent cutover remain distinct operations.
