# Independent review: external-state cutover evidence and projections

Verdict: **APPROVE**. Zero unresolved findings for the exact candidate below. This independent review verifies the entire 21-file result, all four commits, physical current-state evidence, and read-only mapped lifecycle access. It does not authorize new effects.

## Identity, separation and approval scope

| Field | Exact value |
|---|---|
| Base/main | `01247b6ecc2368610d03d8a82b7ac911d4ad1622`; tree `394741c97268edc81ad2587ba47156ac6a55a8f3` |
| Approved candidate/tree | `208ba24c3806a5423e53bd399431ba21acc1fd69` / `22fb2a3c8d813f4c8c184781dbe1215705d0dd31` |
| Canonical base-to-candidate binary diff SHA-256 | `8eed893d37b3510f21d1370a53441311589e40b9bc1f82894ee1ca9303f69e91` |
| Author/executor | `/root/execute_external_state_relocation` |
| Independent reviewer | `/root/review_mapped_facade` |
| Integrator | `/root` |
| Reviewer worktree | `/Users/jamesryancooper/Projects/texenda/worktrees/external-state-cutover-review` |
| Evidence issued / qualification rechecked | `2026-09-15T00:29:45+00:00` |

The three actors are distinct. The executor's physical journal names its exact actor; the tracked author report uses the descriptive alias `agent:external-state-cutover-evidence-astra`. Neither label independently authenticates a provider or person. The assigning coordinator supplies the role separation; this reviewer did not author or execute the cutover candidate.

Approval covers only `208ba24c3806a5423e53bd399431ba21acc1fd69` and its physical-evidence/projection claims. The containing review-evidence commit, integration, final integrated-head audit, new post-cutover work-package execution, product acceptance and external gates remain NOT_RUN. The plan/status text correctly leaves this candidate's independent review/integration and subsequent final audit pending as of its observation. These immutable statements are not retroactively rewritten by this review.

Canonical serialization:

```sh
git --no-optional-locks -c core.abbrev=40 -c color.ui=false diff --no-ext-diff --no-textconv --full-index --binary 01247b6ecc2368610d03d8a82b7ac911d4ad1622 208ba24c3806a5423e53bd399431ba21acc1fd69 | shasum -a 256
```

## Exact current reviewer qualification

Requested qualified route: `gpt-6-astra-max` / `gpt-6-astra` / max / T1. No downshift or fallback. Runtime `codex-desktop-collaboration`; client `26.901.41600 (build 7982)`; sign-in/billing subscription; read/edit/test capabilities. Verified `2026-09-13T21:44:31Z`, expires `2026-10-12T21:44:31Z`. The live bound coordinator's `Harness.qualified(..., 'gpt-6-astra-max')` passed at `2026-09-15T00:22:34+00:00` and was rechecked at the issue time above.

Roster: `docs/qualification/model-roster-v2.1.evidence.json`; SHA-256 `8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0`. Required qualification check: `desktop-profile-gpt-6-astra-max`. Canonical routing-policy digest: `61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0`. Work-package catalog digest: `9ad162070c27e4c765ba145fc8a35d31dc288482453daaa39ec0bb6add8bd8d8`. The evidence envelope carries the immutable exact qualification snapshot, not a second live roster. API allocation/spend zero; provider token accounting and independent executing-model/effort introspection unavailable.

## Four-commit sequence and exact 21-file classification

| Direct child commit | Tree | Paths | Bounded content |
|---|---|---|---|
| `a30b43c8680acccf0d815a6efc7a2a8a4743c5a4` | `b648c6b6d81b54e04be64f58adf640ce471089e5` | 8 | Five status/catalog updates, one TRN-0006 receipt, physical observation record/log. |
| `04174ae28396ec1b58498fa8013fd3f521fa8166` | `8a84f6cdc45e2ffbc1f1e2999538d7a1095d1ea6` | 11 | First generated-only external-root refresh. |
| `b18d5c0b60e09cdf233610cda9c19c4cd9535b9b` | `710ce03929d3fb90f384cc85981360a4566971b8` | 2 | Immutable author-validation record/log. |
| `208ba24c3806a5423e53bd399431ba21acc1fd69` | `22fb2a3c8d813f4c8c184781dbe1215705d0dd31` | 11 | Final generated-only evidence-index refresh. |

Every direct parent is exact; there are no merge parents or extra commits in this range. The two refresh commits touch precisely the same eleven registered outputs. No code, policy, coordinator, sealed specification, source-package, routing, origin-schema or accepted-ADR byte changed.

| Count / class | Repository-relative paths |
|---|---|
| 5 / existing dossier status and catalog | `project-dossier/ARTIFACT_CATALOG.json`<br>`project-dossier/conformance/findings.json`<br>`project-dossier/machine-readable/plan.json`<br>`project-dossier/machine-readable/raidq.json`<br>`project-dossier/transition/README.md` |
| 1 / immutable evidence receipt | `project-dossier/transition/external-state-relocation-receipt.md`; unique catalog ID `TRN-0006`; classification `evidence`; concern `adoption_transition`. |
| 4 / existing qualification evidence owner | `docs/qualification/evidence/2026-09-14-external-state-relocation-validation.log`<br>`docs/qualification/evidence/2026-09-14-external-state-relocation.evidence.json`<br>`docs/qualification/evidence/2026-09-14-external-state-cutover-author-validation.log`<br>`docs/qualification/evidence/2026-09-14-external-state-cutover-author.evidence.json` |
| 11 / generated, non-authoritative | `.agent/generated/manifest.json`<br>`.agent/generated/validation-report.json`<br>`.agent/state/current.json`<br>`.agent/state/RESUME.md`<br>`project-dossier/CANONICAL_SOURCE_MAP.md`<br>`project-dossier/current-state/current.json`<br>`project-dossier/current-state/README.md`<br>`project-dossier/handoff/START_HERE.md`<br>`project-dossier/machine-readable/evidence-index.json`<br>`project-dossier/machine-readable/findings.json`<br>`project-dossier/machine-readable/path-authority.json` |

The catalog and path-authority mirror classify the receipt once. Self-ownership of this immutable observation does not create a second live receipt chain or authoritative transition owner. Existing concern/epoch owners remain unique. The seven-file facade, existing task/decision/evidence/routing owners and deliberately deferred `.agents` capability packages retain their established boundaries.

## Durable evidence and generated integrity

| Committed record | SHA-256 |
|---|---|
| `project-dossier/transition/external-state-relocation-receipt.md` | `5ac1094c401d282011e3d57177f01c9defd809af54a387c9543a523930ac4999` |
| `docs/qualification/evidence/2026-09-14-external-state-relocation-validation.log` | `758bd7a9569bc6587f422cbdf1d8ac04c0a9229a56804c1b110b3c46f2eaeac6` |
| `docs/qualification/evidence/2026-09-14-external-state-relocation.evidence.json` | `22d5dfa06002c57aaf8caa20d77bbaa1344dd185b711be78c2633899400993c3` |
| `docs/qualification/evidence/2026-09-14-external-state-cutover-author-validation.log` | `7144cbff1209c2512332952515b3715d1b10bfd37354401e0a6b0707d9bd7e08` |
| `docs/qualification/evidence/2026-09-14-external-state-cutover-author.evidence.json` | `721f0ebcf35c4ee3fd468ada55ecd2ce0d8a018b9a40429ca0267b1c47b845ff` |

Every PASS/FAIL row in both new author observation records has a confined repository-relative log path, exact hash and command/procedure. All 309 candidate-wide PASS/FAIL bindings passed. These project-specific observation records are not new WP lifecycle receipts; the existing coordinator continues to validate the retained lifecycle envelopes. Independent current verification does not rely solely on the author's assertions.

All eleven generated outputs were independently reconstructed in memory with `refresh.build(..., generated_at=recorded_time, source_identity=(recorded_revision, recorded_tree), prevalidate=False)`; every byte matched disk and committed candidate bytes. No refresh writer ran in the review.

| Generation fact | Value |
|---|---|
| Generation ID | `b3688c5847b3419f4a401a76a3991e336c6b705d53b06685f301e272392cdc23` |
| Generated timestamp | `2026-09-15T00:10:46+00:00` |
| Source revision/tree | `b18d5c0b60e09cdf233610cda9c19c4cd9535b9b` / `710ce03929d3fb90f384cc85981360a4566971b8` |
| Source-scope SHA-256 | `1e8fefd861e8d4e28051189b104d89bf5282c0b04c431053a9e6b8de56fb7ed9` |
| Evidence-scope SHA-256 | `2b638a26ae5e3ffb916647291b5b583086b97e98f70f39541fd25827a9942a25` |
| Evidence index | 52 records; all four new evidence/log files included. |

The source scope is identical at the source commit, author-evidence commit and final candidate. The full HEAD/tree is separately reported to avoid a self-hash cycle. The historical pre-refresh canonical facade check exited 2 with `generated state-root observation is stale`; that expected failure remains preserved, not relabeled PASS. This candidate's explicit external-root checks resolve the projection mismatch. Canonical main is intentionally unchanged until integration.

The supplemental temporary report `/private/tmp/texenda-cutover-author.AhSiBy/final-tip-validation.json` was inspected (SHA-256 `528cfdfd4c8266f1a301154105ed5c5989352009c91d8c272bb8ea6e5b554be2`). Its final-tip facts match independent observations. The temporary snapshot driver SHA `831620847b5ee1c1d69cde93dc89e06c0a6a1d7944bf43080b3971b244340094` equals the full driver source embedded in the durable author-validation log. Temporary files are supplemental locators, not portable PASS evidence or sole support.

## Physical current-state audit

Canonical repository: `/Users/jamesryancooper/Projects/texenda/repo`. Selected external state root: `/Users/jamesryancooper/Projects/texenda/local/agent-state/texenda`. Physical artifact paths in this table are relative to `/Users/jamesryancooper/Projects/texenda`; they are exact local diagnostic locators, not portable evidence paths.

| Artifact | SHA-256 |
|---|---|
| `repo/.texenda-location.json` | `a92b6137856b7f9c2b3f13f69f4e6dc92ed4da1be82eec1ddf21188ebdde0365` |
| `local/logs/workspace-relocation/phase-4-state-relocation-journal.json` | `08c1254c9642a66de202b4909047887e83345a96ccb49ad65a2941204b5be8bf` |
| `local/logs/workspace-relocation/state-root-20260914.activated-moving.json` | `11438325ffa2203718b10dd3cc879ed16b95704d3921a9ef83c4cc7a20854950` |
| `local/logs/workspace-relocation/state-root-20260914.activation-complete.207c592fdadc82c9.json` | `74e25a1bff59f9cde722157e14826a90c280704bdd76e5f77ddb4cfe75e760ea` |
| `local/agent-state/texenda/state.json` | `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235` |
| `local/agent-state/texenda/state.lock` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Each non-private record was read through stable no-symlink regular-file checks and matched its supplied hash. The closed active binding has migration ID `state-root-20260914` and exact repository/root/baseline fields. It is ignored and untracked. The existing external lock was held during independent completed-activation validation; active descriptor, moving archive and completion transaction match exactly. No prepare, apply, recover, rollback, initialization or lifecycle mutator was invoked.

Exactly `state.json` and `state.lock` occupy the external state directory. Old repository state, lock and private-directory locations are absent. No pending state-write control, activation transaction or activation temporary remains. Final `lsof` returned 1 with empty output after all test sessions ended: no process held either exact state/lock path at that observation.

| Preserved state fact | Observation |
|---|---|
| Version / receipt count | 2.0 / 13; all thirteen receipt hashes equal the pre-move journal. |
| Receipt tip | `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e` |
| Roster / leases / budget / gates | 11 / 0 / 0 USD / empty; no receipt append. |
| State inode / device / mode | `670498844` / `16777232` / `100600` |
| Lock inode / device / mode | `670332379` / `16777232` / `100644` |
| Physical-rename timestamps | Recorded second-resolution mtime and modes match pre-move evidence. ctime changed during the physical rename as expected; no contrary preservation claim. |
| Review-period metadata | Exact nanosecond mtime/ctime and all scoped identities/bytes remain unchanged during this independent review. |

Historical repository-relative inputs remain intact: `.texenda/context/WP-00.json` SHA `e13a3eded54663caeb3c3d84ad1a968dde0a9b8eb247be8f6b73350ca8e5435e`; `.texenda/evidence/wp00-integration-verification.log` SHA `be034ce2eb69d9f943a2f78ded7915237c1abb4927335c8dd780f52da1f54e23`; retained integration envelope as below; and `.texenda/state.v1.a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a.json` whose bytes hash to its filename. These are compatibility/history inputs, not live stores.

## Independent read-only WP-00 replay

An inline standard-library `python3 -B -` procedure loaded the candidate coordinator with canonical repo and explicit external root. It captured stable state bytes; called `_read()`, `_validate_retained_evidence(state)`, and `recheck(reference, kind=..., task='WP-00', candidate=..., require_pass=True)` for submission/review/integration; checked phase order, exact hashes, completed state, fence/lease, distinct actors, retained stop booleans and ancestry; and compared exact state bytes afterward. It invoked no lifecycle mutator.

| Receipt sequence | Retained phase | Hash |
|---|---|---|
| 1 | init / planned baseline | `a50f2e78119801bf484a55fa202b75fa61429948b1aea100437cae11d451e30f` |
| 2 | admit | `f20b9a18bfb06899eb33fd33316e666c635c50233c964416ccc8d522074c3479` |
| 4 | assign | `c5f8e6e0c69b3097b5f3eec7e08769b4bf9d8a0a6a28072db9adbdbd313b2803` |
| 5 | start | `dc0d2166f55822d4098603f32355b175a0d5a91caf1bc0bc4d6dd51d832d18e9` |
| 7 | submit | `c0b30bd9764aec6bdf924b28ddada7ea23de8425eb344211e2b1df3c9730206b` |
| 8 | approve-review | `7158517d0578da4129b466a79e9fb0d2745fde8b8f7031b69e307fdf183b629b` |
| 9 | record-integration | `a29aedfcc97546dfa4610d55744a6601e5e0184e25faee2c943127190afb3c59` |
| 10 | complete | `93dd403aeb020f44431c590201eb245ef78b395776c7514c6c807f4e4a778155` |

Sealed `Harness.init` supplies the planned baseline through receipt 1; no separate planned event is invented. Intervening roster and later routing-migration receipts remain untouched.

| Kind | Canonical repo-relative envelope | SHA-256 | Required PASS |
|---|---|---|---|
| submission | `docs/qualification/evidence/wp00-submission.evidence.json` | `d6f611d2be064c822fe5c4c9c8c507ea01a0c83d117dfa554864a3aab642906f` | 8 |
| review | `docs/qualification/evidence/wp00-review.evidence.json` | `371d47a3b2b47df6b5f2cf49bd73f8c8b849ff09a8bcb47586da8a77fbed8caf` | 11 |
| integration | `.texenda/evidence/wp00-integration.evidence.json` | `ba2c632509b41aae33f7efb02e2d07cff5d39882ec876b0bd9d860f02d42042e` | 5 |

All 24 required checks revalidated, including their exact linked log bytes and retained runtime-stop attestations. WP-00 is completed at fence 1 with no lease. Candidate `c95d01162fb6fc7fe0a669cf213bdd73813eb7a8` is an ancestor of integration `12e19b167d7fd59722dc2a3194ce591f499de0e7`, itself an ancestor of the approved base. Author `agent:wp00-terra`, reviewer `agent:wp00-review-terra` and integrator `astra` are distinct historical actors. Ignored integration evidence was resolved only under canonical repo and was not copied into the review worktree.

This qualifies mapped access to an actual pre-existing September 13 lifecycle. It is not a new post-cutover execution, new lease/event/ledger, historical profile requalification, product acceptance or external-gate clearance.

## Commands and observed results

Commands ran in the reviewer worktree unless an explicit root/source path is shown. Environment: `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`. Registered command results below were observed through check-all's actual subprocess execution, not inferred from author logs. The standalone facade run additionally exercises the full-check test deliberately skipped to prevent recursive check-all.

| Check | Exact command | Observed result |
|---|---|---|
| facade-check | `python3 -B .agent/scripts/validate.py --check --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda` | 0; PASS. |
| facade-check-all | `python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda` | 0; nine nonwriters pass; both refresh writers SKIPPED_WRITER. |
| facade-standalone | `python3 -B -m unittest discover -s .agent/tests -p 'test_*.py' -v` | 0; 26/26 in 42.131 s; no skips. |
| workspace-suite | `python3 -B -m unittest discover -s tooling/workspace/tests -p 'test_*.py' -v` | 0 through check-all; 77-test suite. |
| coordination-suite | `python3 -B -m unittest discover -s tooling/coordination/tests -p 'test_*.py' -v` | 0 through check-all; 184-test suite. |
| sealed-suite | `python3 -B -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -p 'test_*.py' -v` | 0 through check-all; 39-test suite. |
| workspace-contract | `python3 -B tooling/workspace/validate_contract.py --check --audit` | 0 through check/check-all; 42 concerns, 85 blueprint paths, 35 types, 16 moves; 86 sealed/88 source files. |
| sealed-package | `python3 -B specs/texenda-handoff/10-validation/validate_package.py --checksums` | 0 through check-all; 14/14. |
| source-package | `python3 -B /Users/jamesryancooper/Projects/texenda/sources/handoff-1.1.0-20260914/10-validation/validate_package.py --checksums` | 0 through check-all; 14/14. |
| canonical-helper | `python3 -B tooling/workspace/relocate_state.py --repo-root /Users/jamesryancooper/Projects/texenda/repo --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda verify` | 0; active state-root-20260914; exact state hash, 13 receipts and expected tip. |
| canonical-harness | `python3 -B tooling/coordination/harness.py --root /Users/jamesryancooper/Projects/texenda/repo --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda check` | 0; local state/receipt/policy integrity PASS, not production readiness. |
| registered-harness | `python3 -B tooling/coordination/harness.py --root /Users/jamesryancooper/Projects/texenda/worktrees/external-state-cutover-review --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda check` | 0 through check-all; detached read-only access with explicit root. |
| diff-check | `git --no-optional-locks diff --check 01247b6ecc2368610d03d8a82b7ac911d4ad1622 208ba24c3806a5423e53bd399431ba21acc1fd69` | 0; also each of four parent/child deltas. |
| sealed-and-code-unchanged | `git --no-optional-locks diff --exit-code 01247b6ecc2368610d03d8a82b7ac911d4ad1622 208ba24c3806a5423e53bd399431ba21acc1fd69 -- tooling .agent/scripts .agent/policy.json .agent/context.json .agent/validators.json specs/texenda-handoff` | 0; exact full changed-path comparison additionally rules out every other unlisted source change. |
| final-lock-holders | `lsof -nP -F pcf -- /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda/state.json /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda/state.lock` | 1 with empty stdout/stderr; no holders at observation. |
| candidate-clean | `git --no-optional-locks status --porcelain=v1 --untracked-files=all --ignored` | 0; empty before/after all review checks, prior to these artifacts. |

Facade parsing/link/schema/origin/owner/evidence validation reported 125 JSON, one TOML, 19 Python, 28 dossier paths, three instruction files, 104 local links and 309 bound PASS/FAIL checks. Both package variants retain 86 manifest files; preserved source has 88 regular files including two original caches. The eleven known source/sealed differences remain unreconciled and no semantic amendment is implied.

The project-bootstrap skill's already inspected Blueprint 1.0.0 references were used for this audit. Its read-only command `python3 -B /Users/jamesryancooper/.codex/skills/project-bootstrap/scripts/plan_adoption.py --target /Users/jamesryancooper/Projects/texenda/worktrees/external-state-cutover-review --profile high-assurance --format json` returned 0 with 44 literal collisions and 41 candidate paths. They remain reconciliation signals, not missing-function findings or authority to generate. No stock generator, profile upgrade or source overwrite ran.

## Lossless no-write proof and private-input boundary

A before/after inline `python3 -B -` snapshot covered the complete reviewer and canonical trees (excluding Git internals/private paths), exact external state and recovery directory, and complete preserved source. It compared SHA-256 for regular files, mode, device/inode, size, exact nanosecond mtime/ctime, directory inventory/metadata and main/reviewer Git HEAD/status including ignored entries. Nanosecond fields were serialized as decimal strings so the reporting layer could not round them.

| Snapshot scope | Files | Directories |
|---|---|---|
| Reviewer worktree | 273 | 63 |
| Canonical repository including non-private ignored history/binding | 273 | 66 |
| External state | 2 | 1 |
| Local recovery/journal records | 4 | 1 |
| Preserved source variant | 88 | 18 |
| Total | 640 | 149 |

Before/after values were exactly equal. Exclusions: Git internals, all private-input directories and CSV contents/metadata, atime and disposable synthetic fixtures outside the declared roots. This does not claim physical power-loss durability or absence of transient fixture writes. Canonical main remained clean at the base; only its expected ignored binding and historical inputs remained. Reviewer tracked/untracked/ignored status was empty, no cache appeared, and no cache was removed or moved. The two preserved source caches remained unchanged.

The only real CSV checks were exact final-path existence, exact old-path absence and Git ignore/tracking scope. Exact final path: `/Users/jamesryancooper/Projects/texenda/local/private-inputs/kit/ohw/2026-09-14/subscribers.csv`. Exact old path: `/Users/jamesryancooper/Projects/texenda/repo/.texenda/private-inputs/kit/ohw/2026-09-14/subscribers.csv`. New existence true; old existence false. Old `git check-ignore -v -- <exact-old-path>` returned 0 and `git ls-files --error-unmatch -- <exact-old-path>` returned 1. The same exact new-path Git scope checks returned 128 because the destination is outside the Git repository; this is not an inside-Git ignore failure. No CSV open, parse, hash, copy, content/size logging, detailed stat or directory-content inventory occurred. No private-content equality is claimed.

## Read-only GitHub observation

At `2026-09-15T00:25:20+00:00`, four `gh api --hostname github.com --method GET` calls inspected `repos/cooperonlineenterprises/texenda`, `repos/cooperonlineenterprises/texenda/branches?per_page=100`, `repos/cooperonlineenterprises/texenda/actions/workflows?per_page=100` and `repos/cooperonlineenterprises/texenda/actions/permissions`. Results: private true; zero hosted branches; zero hosted workflows; Actions enabled, allowed_actions all, sha_pinning_required false. These equal the prior workspace-relocation observation. GET responses were filtered to relevant metadata; no credential value was inspected or logged. No push, hosted run, settings/workflow/branch mutation or external write occurred.

## Findings, limitations and evidence-only handoff

Zero unresolved findings. The historical stale-projection failure is bounded and resolved in the reviewed candidate, not silently erased. An optional nonexistent tooling/workspace README/AGENTS orientation probe returned 1; actual root/nested instruction discovery found and used the applicable sources. It was not a candidate-check failure.

Code-candidate safety conclusions were retained because those bytes are unchanged; the registered adverse/recovery suites reran. The separate prior 75-case transaction and 39-probe type matrices were not newly claimed as cutover executions. No review-only action performed prepare/apply/recover, changed live receipts or created an alternate store.

No atime, physical power-loss, provider executing-model/effort, private-content equality, production, legal/privacy/security or external-gate assurance is claimed. Runtime and Git metadata are bounded observations, not continuous authentication. Physical stop history is supported by the immutable executor journal and parent attestation; this review independently observed current lock availability and no holders.

All reviewer command sessions/children finished and were reaped; no child agents or background services remain. The parent must observe this reviewer task's final stop before releasing scope. This is not a blanket stop attestation for other actors.

The paired [review envelope](2026-09-15-external-state-cutover-review.evidence.json) uses the existing closed evidence v2 review contract. `TRN-WSM-0001` is the existing adoption-transition reference, not an admitted work-package lifecycle receipt. Every PASS/FAIL row binds this exact Markdown SHA-256 with a safe repository-relative path and command/procedure.

Only these two review artifacts are authorized for the evidence-only child commit. Its parent must be the exact candidate above. The subsequent handoff reports the containing commit/tree and both file hashes, avoiding a self-reference. No reviewed candidate or generated file is changed. Adding these artifacts makes the generated evidence index stale until the integrator separately refreshes and validates a new head. This candidate approval does not approve that later head.
