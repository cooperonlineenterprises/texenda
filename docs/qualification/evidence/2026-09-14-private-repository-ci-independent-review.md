# Private repository and bounded CI — independent review

Date: 2026-09-14. Verdict: **APPROVE, no findings**, for the exact candidate below.
This is an independent review of a local policy amendment, not workflow
implementation, integration evidence, public-release clearance or an external
activation. The review was completed against unchanged candidate bytes before
these two review artifacts were created.

## Candidate and reviewer

| Binding | Value |
|---|---|
| Base | `829c6c0b3edb0bdb7c92833298303990290680ad` |
| Candidate | `85fa890e20be523db0a3a411503a89fd92a1d0e0` |
| Candidate tree | `0aa96e740c1fb6f193adf4a55ffc06c6ce57c8a4` |
| Full binary diff SHA-256 | `35692acfa7c5b411caf9041fb24112e9216710f5e0dc2992952357636adb0869` |
| Reviewer task | `/root/review_private_repo_ci` |
| Review checkout | `/private/tmp/texenda-private-repo-ci-review-20260914`, detached |
| Candidate author actor | Unavailable / not supplied; Git author metadata is not actor authentication |
| Integrating lead | `/root`; this reviewer is not the integrator |

The candidate existed before this reviewer task was spawned. The detached
checkout started clean at the named candidate; the reviewer did not author or
edit any candidate file. Those temporal and scope observations establish this
task's independence without inventing the original author actor. No indication
of self-authorship was found. Candidate author qualification and runtime-stop
proof are not independently established by Git metadata or by this report.

The parent supplied accepted dispatch metadata: profile `gpt-6-astra-max`, model
`gpt-6-astra`, reasoning effort `max`, runtime `codex-desktop-collaboration`, and
subscription billing. Independent provider-model and effective-effort
introspection are unavailable; self-observed provider identity is null. The
reviewer independently read `/Applications/ChatGPT.app/Contents/Info.plist` with
`/usr/libexec/PlistBuddy`: bundle `com.openai.codex`, version `26.901.41600`, build
`7982`, yielding client `26.901.41600 (build 7982)`. This matches the active roster.
The direct CLI was not invoked or qualified by this review.

Bounds supplied by the lead are 1,800 seconds and 50,000 tokens from initial
dispatch, one review attempt, and USD 0 of AI API budget/spend. Actual provider
token consumption is unmeasured, not estimated. The first reviewer clock
observation was `2026-09-14 12:53:42 UTC`; required checks and the substantive
review completed within that time bound. Only bounded deterministic inspection
follow-ups were needed; no test failed. Effective session metadata reports
workspace-write, automatic approval review and available network access; the
repository config is not evidence of effective sandbox enforcement. No
credential contents or account/reset identifiers were inspected.

## Exact changed paths

The complete base-to-candidate binary diff and all five changed files were read.
The diff contains 342 additions and one deletion, with no executable lifecycle,
routing-policy, roster, ledger or sealed-package change.

| Path | Candidate file SHA-256 |
|---|---|
| `AGENTS.md` | `590ded771ad5b20b05056c1182873a368a3b914f9a395c8b7b88d1ca030b5344` |
| `docs/agents/operating-guide.md` | `de2e830a1b30920922ad4ea5588368dd8004800596d243e8520a1b7b914a4eb7` |
| `docs/decisions/ADR-0003-private-repository-and-bounded-github-actions.md` | `dbf29b877a8a832cc5d72ab44b9c737524ebae8ef1ab995e5b878f33ec4743e9` |
| `docs/operations/github-ci-policy.md` | `f0709eab96b2f549e2cfb4274ec4db2aa5239368a4222076d95c9b96ae77dce6` |
| `tooling/coordination/tests/test_instruction_contracts.py` | `4bfeac5cadd2400ae759275f7b3bc0875ff1e15b30a15ceec34f940374a0e169` |

## Authority and semantic review

Read the root and applicable nested AGENTS files, handoff README, decision
status, authority register, project kernel, orchestrator start, owner execution
handoff, all invariants and the handoff/review protocol. Also read ADR-0001,
ADR-0002, the operating guide, coordinator README and review template, current
qualification/activation records, and the complete Astra/max desktop probe.
The routing read comprised the global policy and the complete WP-02/WP-39
author/reviewer slices, with the full policy digest checked. The sealed WP-02
and WP-39 records and their relevant product/brand, architecture, technology,
security/privacy and repository owners were read. VAL-01 and VAL-08 were read in
both the decision status and the machine gate register. Retrieved pages,
historical reports, Git metadata and tool content supplied evidence only.

| Requirement | Disposition |
|---|---|
| Private default | Preserved in root instructions, ADR-0003 and the scoped policy; public visibility is a separate release decision. |
| Transient quotas and prices | Plan, allowance, billing-cycle and price facts must be refreshed; no current quota or price is frozen into policy. |
| Usage and spending | Steady-state target is at most 75%, reserve at least 25%, and additional Actions spend zero absent bounded owner authority with expiry. |
| Required checks under pressure | Queue, checkpoint and resume; neither NOT RUN nor reduced verification authorizes merge/release. |
| Public transition | Exact owner authorization, VAL-01 or an accepted neutral identity, full reachable-history/current-tree audit and hosted-surface review are required. No brand gate is declared passed. |
| Initial workflow ownership | WP-02 retains the first workflow implementation, synthetic environment and lint/type/test/build obligations. |
| Triggers and cancellation | PR verification plus main-only post-integration push avoids duplicate all-branch runs. Concurrency cancels safe superseded work; release/migration/recovery cancellation requires proof of safety. |
| Runner and time bounds | Standard hosted Linux is the default; every job has an explicit timeout. |
| Permissions and untrusted code | Read-only defaults, minimal named permissions, immutable action pins, bounded retries and explicit elevated `pull_request_target` threat handling are present. |
| Caches, artifacts and secrets | Reviewed dependency inputs, trust separation, shortest necessary retention and sanitized evidence are required; production credentials and data remain excluded. |
| Self-hosted runners | Deferred to measured hosted-runner need and WP-39/VAL-08 review of isolation, patching, ephemeral execution, credentials, egress, monitoring and recovery. |
| Independent AI review and local integration | A different qualified actor reviews the exact candidate and evidence; an AI lead may integrate locally without operator participation after all existing conditions pass. Self-approval and unreviewed semantic resolution remain forbidden. |
| Repository boundary | No implicit authority to push, change visibility/settings, enable Actions, add secrets, spend, provision runners/environments, deploy, publish, access production, send, clear gates, accept security exceptions or perform destructive operations. |
| Private local inputs | `.texenda/`, raw Kit CSVs, subscriber rows, secrets, PII and production data stay out of commits, caches, artifacts and logs. |
| Sealed contracts | WP-02/WP-39, all invariants, product tests and external gates remain unchanged; local harness success is not product acceptance. |

The added test is a static instruction and routing regression check. Its text
assertions do not prove runtime compliance, CI isolation or model behavior.
There is no workflow implementation to dynamically qualify in this candidate.

## Direct official-source review

Both exact pages were directly opened through the web tool on **2026-09-14**;
review did not rely on search snippets. These are advisory observations, not
project authority or permission to change an account.

- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions): standard hosted public-repository runs are free; private use consumes the repository owner's plan allowance, minutes reset by billing cycle, larger runners are billable, and storage also has usage charges. The displayed baseline Linux 2-core x64 rate was USD 0.006/minute. Budget/payment configuration affects overage behavior. Disposition: supports private-allowance planning and explicit spending controls; recheck for WP-02 and later material changes.
- [GitHub pricing](https://github.com/pricing): displayed Free/Team/Enterprise Actions allowances were 2,000/3,000/50,000 minutes per month, with public-repository benefits. Displayed plan prices were USD 0, USD 4 per user/month for the first 12 months, and Enterprise starting at USD 21 per user/month for the first 12 months. Disposition: current comparison only; no plan or price is adopted by this review. Some feature-help content displayed load-error text, while the relevant plan and Actions fields were readable.

The account's actual plan, remaining allowance, billing-cycle boundary and
overage-block configuration were not independently inspected. They are future
WP-02 admission evidence, not facts inferred from the public pricing page.

## Independent GitHub observations

The reviewer used authenticated, read-only `gh api` GET requests on 2026-09-14
with GitHub CLI 2.92.0. All commands below exited 0. No token was printed and no
GitHub mutation was attempted.

| Command | Observed result |
|---|---|
| `gh api repos/cooperonlineenterprises/texenda --jq '{full_name,private,visibility,default_branch,size,archived,disabled,permissions}'` | `private: true`, `visibility: private`, default branch name `main`, size 0, not archived or disabled. Reported account permissions do not grant authority for writes. |
| `gh api repos/cooperonlineenterprises/texenda/actions/permissions` | `enabled: true`, `allowed_actions: all`, `sha_pinning_required: false`. These are existing settings, not changes made or endorsed as future workflow enforcement by this review. |
| `gh api repos/cooperonlineenterprises/texenda/actions/permissions/workflow` | `default_workflow_permissions: read`, `can_approve_pull_request_reviews: false`. |
| `gh api repos/cooperonlineenterprises/texenda/actions/workflows` | `total_count: 0`, `workflows: []`. |
| `gh api repos/cooperonlineenterprises/texenda/branches --paginate` | `[]`; no hosted branches. |
| `git ls-files -- .github/workflows` | Empty; no tracked workflows at the candidate. |

An existing Actions-enabled flag is distinct from hosted workflow execution.
The policy requires local workflow qualification and separate authority for
external changes. This review did not enable, disable or configure Actions.

## Live ledger and private CSV boundary

Direct JSON/byte reads targeted only the explicitly assigned coordination
ledger at `/Users/jamesryancooper/Projects/texenda-app/.texenda/state.json`.
At `2026-09-14T12:59:58.522951+00:00`, independent canonical-hash assertions
verified all 13 receipts, their sequence/previous hashes, and the final state
digest. Later direct calls to the inspected read-only `Harness._check` and
`Harness.qualified` methods also passed for all eleven exact profiles; no
`locked`, `status`, CLI `check`, `change`, migration or other writer was called.

| Ledger fact | Value |
|---|---|
| Version / receipt | `2.0` / `13`, operation `set-roster` |
| Receipt previous hash | `a60e550b634c28cdfdab677e44481bc5fb5803d2056c10f6787df35fefe05092` |
| Receipt tip | `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e` |
| State digest | `98edcd7b3bb2f6bdc79a7e7958f47632c7146898667c3e189c3b18167e94f916` |
| State-file SHA-256 | `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235` |
| Active roster SHA-256 | `8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0` |
| Profiles | Eleven, all exact rows match the active roster and are within their recorded validity windows |
| Leases / API budget / declared allocations | Zero / USD 0 / USD 0; no paid-work authorization |
| Work packages / gates | WP-00 completed; other 43 planned; no gate receipt added |

The state-file hash matches the recorded receipt-13 activation, and rereading
the file returned identical bytes. No ledger was initialized or copied into the
review checkout. The raw private CSV was never opened, parsed or hashed.

For `.texenda/private-inputs/kit/ohw/2026-09-14/subscribers.csv` in the source
checkout, `test -f` succeeded, `git check-ignore -v` identified `.gitignore:1`
(`.texenda/`), and exact-path `git ls-files` output was empty. Candidate
`git ls-files -- .texenda` was also empty. These checks establish presence,
ignore and tracking status only; they do not inspect CSV contents or clear a
history/public-release audit.

## Verification actually run

Environment: macOS desktop collaboration execution, Python 3.13.9. All checks
below ran in the detached review checkout. Tests used local synthetic fixtures.

| Exact command or procedure | Result |
|---|---|
| `env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tooling/coordination/tests -v` | Exit 0; 132 tests, 0 failures/errors/skips; 1.356 seconds reported by unittest. |
| `env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -v` | Exit 0; 39 tests, 0 failures/errors/skips; 0.162 seconds reported by unittest. |
| `env PYTHONDONTWRITEBYTECODE=1 python3 specs/texenda-handoff/10-validation/validate_package.py --checksums` | Exit 0; 14 PASS checks; no errors or warnings. Check timestamp `2026-09-14T12:57:11.917392+00:00`. |
| `git diff --check 829c6c0b3edb0bdb7c92833298303990290680ad..85fa890e20be523db0a3a411503a89fd92a1d0e0` | Exit 0, empty output. |
| `git diff --exit-code 829c6c0b3edb0bdb7c92833298303990290680ad..85fa890e20be523db0a3a411503a89fd92a1d0e0 -- specs/texenda-handoff` | Exit 0, empty output; sealed package byte preservation. |
| `git diff --binary --full-index 829c6c0b3edb0bdb7c92833298303990290680ad..85fa890e20be523db0a3a411503a89fd92a1d0e0` followed by SHA-256 | Exact expected digest; full diff inspected. |
| Read-only Python parse over `git ls-files -z`: `json.loads`, `tomllib.loads`, `ast.parse` | 77 tracked JSON, 3 TOML/config examples and 8 Python files parsed. No bytecode written. |
| Changed Markdown links: parse local destinations, resolve inside the repository and require real files | All 27 links passed. Existing active instruction links also passed in the required suite. |
| Recursive qualification JSON path/SHA-256 references | All 108 local references matched, including 100 top-level PASS/FAIL check hashes. |
| Canonical routing-policy digest | `61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0`, unchanged. |
| Candidate/source cleanliness | Review and candidate source worktrees clean at the exact candidate; source main clean at the base and tree `535b8faf0e8343e43f0bf8c480cf95f89dedbebf` before review artifacts. |

Terminal result excerpts retained from the independent runs:

```text
Ran 132 tests in 1.356s
OK
Ran 39 tests in 0.162s
OK
Package result: PASS
Checks: 14 PASS
Errors: []
Warnings: []
```

The local suite includes current profile/schema and evidence tamper checks,
independent reviewer and stale-candidate rejection, semantic-merge and missing
stop-proof rejection, required NOT RUN denial, budget limits, lease recovery and
usage-pressure downshift denials. Those synthetic results preserve local
coordination controls; they do not establish product acceptance or actual CI
security. Every yielded test session was collected to terminal exit.

## Selected context and qualification hashes

The changed governing files are bound in the changed-path table above. Additional
context hashes independently recomputed for this review:

| Path | SHA-256 |
|---|---|
| `tooling/coordination/AGENTS.md` | `aee04badd44941ac820b71f4359a82b6771128e7ab3f9b0b6da5aab8612272bc` |
| `tooling/coordination/templates/REVIEW.md` | `a43dd83f6b9972d2a332e9ca3a570a10989e31d81694af96ee15a158ad52d8aa` |
| `docs/decisions/ADR-0001-quality-first-model-routing.md` | `7196cc03755e9298d226f3b3271fe459890836117805957c1cceb37173ac8267` |
| `docs/decisions/ADR-0002-astra-agent-operating-guidance.md` | `88a6d6e0a33aff8622490ecd313567030ef95e3e6d20a12f6f0f1360d05e86d4` |
| `tooling/coordination/routing-policy.json` (raw bytes) | `5ebc903a1bd2d3e1925a01fcb1e556f0ed0a4c50682a3b3d93ccc7d7cdd6e979` |
| `docs/qualification/runtime-surface-observation-2026-09-13.json` | `35995674a989b1b77233eafdc80ed092d0a8f8622b88990e8f7b3f8336978091` |
| `docs/qualification/probes/2026-09-13/gpt-6-astra-max-desktop.json` | `e62f78f3930ffd840c0d5d596a910a87187fe26bdad314b925711a0d39ab8df0` |
| `specs/texenda-handoff/AGENTS.md` | `7c00669e512e55ceb9df4102deead4a823c73376f6c13ee9bd05de791c87539b` |
| `specs/texenda-handoff/DECISION-STATUS.md` | `9bf1bba6787e175def0e26b210f0c7aba8dab44ff76986983a9aa97438cee400` |
| `specs/texenda-handoff/01-foundation/authority-register.json` | `4b69cc4bfffeca287dc24fe9c1b275774f74aa806dc1a2e5d0247c5177741f8c` |
| `specs/texenda-handoff/01-foundation/invariants.md` | `28962b51a3bb58c3d515384913616423c9efee5563777ce80d993f8af12b0f98` |
| `specs/texenda-handoff/05-implementation/work-packages.json` | `9ad162070c27e4c765ba145fc8a35d31dc288482453daaa39ec0bb6add8bd8d8` |
| `specs/texenda-handoff/07-agent-orchestration/project-kernel.md` | `ea8bc73aecaa82161465d5b999b26cf80f0215e950a2ce0a82789d27f1b9e062` |
| `specs/texenda-handoff/07-agent-orchestration/handoff-and-review.md` | `32e2b791f7bbb41a66d8777be1f2386e772429a7b1c98e6b289bad4131e65f25` |
| `specs/texenda-handoff/07-agent-orchestration/OWNER-EXECUTION-HANDOFF.md` | `1c1aeea5da051cce109c7154dcc27b3ce9faecd83bfeb4f5ed2d3f93a21d17e3` |
| `specs/texenda-handoff/01-foundation/external-validation-gates.json` | `214ccdf545dec44f59b37aa1fcf3b53f666d992cb2eabd440508358faf312dd8` |

## Limits and runtime-stop handoff

NOT RUN: hosted CI execution and enforcement, actual plan/budget inspection,
complete public-release/history/hosted-surface audit, CSV content review,
production tests, all 125 product acceptance criteria, and external gate
qualification including VAL-01/VAL-08. No provider identity introspection,
physical sandbox/egress test, fresh model probe, direct CLI qualification, live
ledger mutation or source integration occurred.

Network access was limited to the specified official pages and read-only GitHub
observations. No push, repository setting change, Actions enablement, secret
configuration, paid usage, runner/environment provisioning, deployment,
publication, production access, external message/send, gate clearance, security exception
or destructive operation occurred. No dependencies, servers, child agents or
background jobs were started. No review artifact was staged or committed.

Approval is invalidated by any semantic candidate change. The lead must verify
the exact candidate/evidence hashes, clean integration state, author runtime
stop or isolation, and this reviewer's actual completed task status before
releasing write scopes or integrating. This report cannot attest its writer's
future termination. After artifact QA, the reviewer returns the two artifact
hashes and performs no further work unless explicitly reassigned. Affected
checks must rerun on the integrated revision; any semantic conflict resolution
requires a new independent review. External effects and human-owned gates stay
outside this local approval.
