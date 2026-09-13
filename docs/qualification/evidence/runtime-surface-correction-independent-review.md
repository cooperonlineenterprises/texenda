# Independent desktop runtime correction review

Verdict: **APPROVE**. Actionable findings: none.

This review approves only candidate `d08f3da49a043ee9f62555b6098276ac05ed87f5` against base
`0a72aba450c76e318b02f22c49133b406da7d4ef`. It does not install the replacement roster, grant
owner attestation, or clear a product or external gate. The reviewer did not
author the candidate and wrote only this report and its adjacent evidence JSON,
as uncommitted additions after completing the candidate review.

## Candidate and reviewer binding

| Field | Value |
|---|---|
| Candidate | `d08f3da49a043ee9f62555b6098276ac05ed87f5` |
| Base | `0a72aba450c76e318b02f22c49133b406da7d4ef` |
| Candidate tree | `9172cd72b2c15cabd0b147c24fa5e8a2939d8b71` |
| Full diff SHA-256 | `06018da8f7d249c89852d8d0eaf8bb86590903b6450994c908c15c88eb238fbc` |
| Full diff length | 128724 bytes |
| Canonical routing policy SHA-256 | `61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0` |
| Review task identity | `/root/review_runtime_correction` |
| Requested reviewer model / effort | `gpt-6-astra` / `max` |
| Requested reviewer exact profile | `gpt-6-astra-max` |
| Executing provider model / effort independently observed | unavailable / unavailable; no self-attestation |
| Runtime surface | `codex-desktop-collaboration` |
| Independently inspected bundle | `com.openai.codex`, version `26.901.41600`, build `7982` |
| Desktop client string | `26.901.41600 (build 7982)` |
| Separately inspected CLI | `codex-cli 0.149.0`; unqualified |
| Billing / API allowance | subscription by parent assignment; API USD 0 |
| Review bounds | exact candidate, stated required checks, and two output files; numeric time/token allocation not supplied to reviewer |
| Final clean candidate observation before artifact writing | `2026-09-13T22:27:14.014566+00:00` |

The parent supplied the requested model/effort and dispatcher-accepted task
identity. The reviewer independently read the bundle fields using
`/usr/libexec/PlistBuddy` and ran `codex --version`, both at
`2026-09-13T22:18:35Z`. No provider identity or effort introspection was
available. Subscription account mode came from the bounded assignment and
recorded observation; no credential, account identifier or provider billing
telemetry was inspected. This session uses workspace writes with automatic
approval review and available network capability; no network operation was used.
Repository defaults were not taken as proof of effective session permissions.

The diff digest is over the exact stdout bytes of:

```sh
git diff --no-ext-diff --no-textconv --full-index --binary 0a72aba450c76e318b02f22c49133b406da7d4ef d08f3da49a043ee9f62555b6098276ac05ed87f5
```

All 17 changed files were reviewed. The three modified-file diffs were inspected
directly. Every one of the fourteen added-file diff bodies was reconstructed
and verified byte-identical to its fully reviewed candidate file. Reverse
application was checked without applying it.

## Assessment

The review read root and coordinator AGENTS, the sealed README, decision status,
kernel, orchestrator start, owner handoff, invariants and handoff/recovery
protocol; ADR-0001 and ADR-0002; the complete routing policy; coordinator README,
complete local harness, both test files and evidence/profile schemas; the review
template; current and historical rosters; all eleven dated probe reports; the
correction plan, observation and verification; and relevant prior independent
instruction-system and routing reviews and activation evidence. Repository,
retrieved and model evidence was assessed as data under the authoritative
project sources.

The correction changes runtime attribution and adds one instruction-contract
regression test. All 86 sealed-package files and 39 pre-existing qualification
and audit evidence files, excluding the intentionally updated qualification
README, match the base bytes. ADR-0001, lifecycle code, schemas, policy bytes
and its canonical digest are unchanged. The four max defaults, eleven allowed
profiles, all 44 author/reviewer routes, downshift conditions, sole explicit
Sol/max T1 fallback, two-writer limit and zero new API-spend authority remain
unchanged. ADR-0002's acceptance wording accurately points to the already
approved instruction candidate and its retained review commit.

The replacement roster has eleven unique closed qualification rows and twelve
required PASS checks. Every row matches its policy model, effort, native tier,
desktop runtime/client, subscription mode and read/edit/test capabilities.
Every row's verification time matches its own fresh report; every validity
window is exactly 29 days and current at review. All qualification and
observation hashes match. The new regression contract checks desktop attribution
from the observation without making transient version numbers permanent policy.

The report shape differs among probes, but every report records the correct
requested model and effort, observed desktop build, bounded read/edit/test
exercise, ten passing then-current instruction tests and a passing sealed
checksum validator. Source commits are limited to their single report and match
the integrated report bytes. The installed CLI is independently distinct and
remains unqualified; the recorded 0.153.0 Astra minimum is dated evidence from
the previously reviewed source, not a new network revalidation by this review.

No probe or correction transfers qualification to CLI, API, cloud, IDE, another
account/workspace, client, model or effort. Model/effort names remain dispatch
metadata. No product behavior or external gate is treated as passed.

## Exact profile inventory

All rows below use `codex-desktop-collaboration`,
`26.901.41600 (build 7982)`, subscription billing, and read/edit/test scope.
Each report is under `docs/qualification/probes/2026-09-13/` with filename
`<profile_id>-desktop.json`.

| Exact profile | Verified UTC | Expires UTC | Report SHA-256 |
|---|---|---|---|
| `gpt-6-astra-max` | `2026-09-13T21:44:31Z` | `2026-10-12T21:44:31Z` | `e62f78f3930ffd840c0d5d596a910a87187fe26bdad314b925711a0d39ab8df0` |
| `gpt-6-astra-high` | `2026-09-13T21:37:21Z` | `2026-10-12T21:37:21Z` | `39667e91d35f6f538338047ecac039a9b282bc41b842cb7789fb8b863ac19e55` |
| `gpt-5.6-sol-max` | `2026-09-13T21:45:13Z` | `2026-10-12T21:45:13Z` | `bade3a896b777d08d134b596edef0c95ee80fa59df81e7c95a3ec3985346c429` |
| `gpt-5.6-sol-high` | `2026-09-13T21:37:53Z` | `2026-10-12T21:37:53Z` | `bfeb7d4639e2af5fd1d686a599e8c5ae4165b645bfd84bbcc90384c7ab62bc70` |
| `gpt-5.6-terra-max` | `2026-09-13T21:51:56Z` | `2026-10-12T21:51:56Z` | `0e8e8d8b5e1027b18fde140f7e207c7bab7cb0daea79fae714dd55a5cbb48f66` |
| `gpt-5.6-terra-high` | `2026-09-13T21:51:17Z` | `2026-10-12T21:51:17Z` | `763d6ca28031640217699b00157d45c636b4abe7829cfd7e980b7aee287dbf6a` |
| `gpt-5.6-terra-medium` | `2026-09-13T21:58:11Z` | `2026-10-12T21:58:11Z` | `5ce0c586e5506c78643b86850620804fe534c6017690f5b4ab4718c30ce3e61d` |
| `gpt-5.6-luna-max` | `2026-09-13T21:59:22Z` | `2026-10-12T21:59:22Z` | `73e6370836289af4babb18c0f0ffffb8b2b853a5e6ffabadec31bcca691dbd44` |
| `gpt-5.6-luna-high` | `2026-09-13T22:04:30Z` | `2026-10-12T22:04:30Z` | `a4b4b39af3e27ce36d8e7b368d6e5fa7508a9088d6409ce42717e7fede54a5db` |
| `gpt-5.6-luna-medium` | `2026-09-13T22:03:56Z` | `2026-10-12T22:03:56Z` | `f4bbaf3d7ef77cb946a44b9fdb69591eac01f9ef8c5ed0bac6d94352c47f78be` |
| `gpt-5.6-luna-low` | `2026-09-13T22:07:26Z` | `2026-10-12T22:07:26Z` | `d223cfcda3e8232fd0610fc8d0c11f89f7d7c91d9c3eeca92bd48a2cd4cf0975` |

The replacement roster SHA-256 is
`8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0`.
The historical v2 roster SHA-256 remains
`dbfd99b98edc134c1e202c0b48145141f967718194b67012f75a3868bf4ef6a1`.

## Probe completion and Luna/low correction

| Exact profile | Dispatcher task | Source commit | Completion evidence |
|---|---|---|---|
| `gpt-6-astra-max` | `/root/requal_astra_max` | `e86099271cdf0810185ae563f73128c90c68c4de` | Parent dispatcher observation: completed |
| `gpt-6-astra-high` | `/root/requal_astra_high` | `baa5e350d3b27326ec4f405858ecb56ff9d53a57` | Parent dispatcher observation: completed |
| `gpt-5.6-sol-max` | `/root/requal_sol_max` | `f6427f98b3bd3899215b77413b56c651f19c3280` | Parent dispatcher observation: completed |
| `gpt-5.6-sol-high` | `/root/requal_sol_high` | `304f63cf7bee4b3980b00a370a91cca1c3442ca3` | Parent dispatcher observation: completed |
| `gpt-5.6-terra-max` | `/root/requal_terra_max` | `702314d59500d3b5dcd1bf5cb0e8dc7a055338bf` | Parent dispatcher observation: completed |
| `gpt-5.6-terra-high` | `/root/requal_terra_high` | `358bc0a6a057d969f3ac313cbe9832f9520274f2` | Parent dispatcher observation: completed |
| `gpt-5.6-terra-medium` | `/root/requal_terra_medium` | `e83cfc7fd64cd3c4997bb8fff1e831d335ded92b` | Parent dispatcher observation: completed |
| `gpt-5.6-luna-max` | `/root/requal_luna_max` | `a3449b3a4ee60dba3476df50d1cb9999189075d4` | Parent dispatcher observation: completed |
| `gpt-5.6-luna-high` | `/root/requal_luna_high` | `05ca53bc88a998a2e020c53081d89b3bd65e3156` | Parent dispatcher observation: completed |
| `gpt-5.6-luna-medium` | `/root/requal_luna_medium` | `7f7176d76465c9b66057af5ec53a817e07afedf6` | Directly observed completed; parent also observed |
| `gpt-5.6-luna-low` | `/root/requal_luna_low` | `0f0f4a97151a2f17c9831069f1f86fcbb2345550` | Directly observed completed; parent also observed |

The parent supplied its prior `collaboration.list_agents` / final-answer
observations that all eleven probe tasks completed before integration, with no
live probe left. The reviewer independently called `collaboration.list_agents`
and observed the two still-listed Luna/medium and Luna/low tasks as completed.
The other nine historical completion observations are parent-supplied
dispatcher evidence, not independently rediscovered provider telemetry.
Subprocess exit evidence and no-background-work statements are recorded by the
probes; they are distinct from the parent-observed end of the enclosing agent.

Luna/low could not create its source commit because the linked Git metadata was
outside its writable sandbox. After that agent completed, the parent corrected
only `profile_id` from `gpt-5.6-luna-low-desktop` to the exact policy ID and
`expires_at` from `2026-10-12T19:51:23Z` to
`2026-10-12T22:07:26Z`, matching verified time plus 29 days.
The reviewer reconstructed the original bytes in memory by reversing those
two replacements. Their SHA-256 is
`1d40c826248911c1c98c70c9d9ddccfac436b5583f1b706b26bfd6ae0cbecacf`,
exactly the original dispatcher-returned report hash. This proves all other
bytes, including requested model/effort, observation and test results, were
preserved. The corrected source commit
`0f0f4a97151a2f17c9831069f1f86fcbb2345550` contains only that report.
This was a disclosed candidate correction before independent acceptance, not
a rewrite of previously accepted historical evidence.

## Independent verification

| Command or check | Result |
|---|---|
| `env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tooling/coordination/tests -v` | Exit 0; 131 tests passed in 1.426s |
| `env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -v` | Exit 0; 39 tests passed in 0.164s |
| `env PYTHONDONTWRITEBYTECODE=1 python3 specs/texenda-handoff/10-validation/validate_package.py --checksums` | Exit 0; 14 checks passed, zero errors/warnings |
| Targeted eight contract/negative tests listed below | Exit 0; 8 passed in 0.064s |
| Read-only candidate/provenance/hash program | Exit 0; all 163 tracked files match candidate objects; 76 JSON, 3 TOML/config examples and 8 Python files parsed; 86 sealed and 39 historical files unchanged; 14 added diff bodies match; 8 envelopes and 80 evidence hash references verified |
| Read-only schema/link program | Exit 0; 12 evidence/template records satisfy the actual schema keywords; 69 local links in 13 active Markdown files resolve; sealed links/anchors separately covered by package validator |
| In-memory actual-profile negative checks | Exit 0; all 66 runtime/client/model/effort/billing/expiry cases denied, inputs preserved |
| `git diff --check` on candidate range and worktree | Exit 0; no whitespace errors |
| Explicit base/candidate diff of sealed package, harness, policy, schemas and old rosters | Exit 0; no differences |
| Full binary diff piped to `git apply --reverse --check` | Exit 0; verification only, no application |
| Final `git rev-parse HEAD` and `git status --porcelain=v1 --untracked-files=all` before artifact writing | Exact candidate; clean |

The targeted command was:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tooling/coordination/tests python3 -m unittest -v test_instruction_contracts.InstructionContracts.test_current_roster_binds_exact_profiles_to_observed_desktop_not_cli test_routing_v2.RoutingTests.test_roster_rejects_duplicate_and_mismatched_exact_profiles test_routing_v2.RoutingTests.test_roster_bytes_and_logs_rechecked test_routing_v2.RoutingTests.test_explicit_fallback_only_sol_max_with_flag_and_reason test_routing_v2.RoutingTests.test_usage_pressure_text_cannot_supply_downshift_conditions test_routing_v2.RoutingTests.test_budget_amount_scope_and_hash_tampering_cannot_authorize_new_work test_routing_v2.MigrationTests.test_migration_refuses_live_and_expired_leases test_routing_v2.RoutingTests.test_untrusted_review_text_cannot_make_required_not_run_pass
```

The independent 66-case program exercised all eleven actual qualification
snapshots. For each, it altered the runtime to direct CLI, client to 0.149.0,
model, effort and billing route, and separately evaluated expiry at equality.
All attempts failed closed. Existing tests additionally cover duplicate rows,
roster/log tamper, explicit fallback, usage-driven downshift denial, budget
tamper, live/expired lease migration and untrusted NOT_RUN evidence.

`jsonschema` was not installed in the local Python runtime
(`ModuleNotFoundError`, exit 1). No dependency was installed. Schema validation
used a standard-library checker covering the actual evidence/profile schema
keywords plus the committed harness validators; this is not a claim of general
Draft 2020-12 engine conformance. An initial orientation read used the original
package-root paths and was corrected to the installed `specs/texenda-handoff`
paths. One compact policy display requested a nonexistent array after printing
the full policy; inspection and the successful policy validator used
`work_package_routes`. An initial optional ledger lookup used the source
specification workspace; the parent identified the installed ledger root below.
These inspection errors caused no candidate or live-state mutation.

Exact inline verification programs and tool output are retained in this review
task's transcript. All reported counts describe the committed candidate before
the two review artifacts were added.

## Live state and safe activation boundary

At `2026-09-13T22:26:37.487605+00:00`, the reviewer read
`/Users/jamesryancooper/Projects/texenda-app/.texenda/state.json`
and its referenced v1 checkpoint directly, without calling lock-creating
commands. The state and checkpoint bytes were checked again after inspection.

| Live fact | Independently verified value |
|---|---|
| State version / SHA-256 | `2.0` / `43cf040755cc587373fcddd9c7ff7727d41ccecbc260e9043869c3797a1a82fb` |
| Receipt count / head | `12` / `a60e550b634c28cdfdab677e44481bc5fb5803d2056c10f6787df35fefe05092` |
| Last operation / active roster | `set-roster` / historical v2 roster |
| Active profiles / leases | 11 / 0 |
| API budget / declared spend | USD 0 / USD 0 |
| WP-00 | completed |
| V1 checkpoint SHA-256 | `a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a` |
| Preserved source | all ten v1 receipt objects and every task/history record |
| Live mutations by this review | none; no lock or write operation called |

The correction plan provides a safe forward replacement: independently approve
the exact candidate; integrate serially; refresh live checks, worktree/runtime
status and leases; stop and recover any affected assignment before replacing
its pinned qualification; then perform the distinct owner-attested
`set-roster` against the reviewed integrated files. Retain the old roster,
checkpoint and receipt chain. Verify the unchanged receipt prefix, new roster
hash, eleven profiles, corrected client, zero leases and zero API authority,
then append a new activation receipt. A changed live state needs reconciliation
before installation. Do not edit the ledger, delete state, reuse an invalidated
assignment binding, or use rollback to discard later history. This review
neither executes nor pre-attests that activation.

## Source hashes and runtime stop

The eleven profile file hashes are above. The remaining relevant candidate,
authority and evidence hashes are retained here.

| File | SHA-256 |
|---|---|
| `AGENTS.md` | `08e03c382b155f7bc2429a2ea13b5424f670e683be7d8d1d66dce3d349cb2dc7` |
| `docs/agents/operating-guide.md` | `d448b14dad65155c2b9d794b6f21eb49fd577260ee8a49fd36682176fcb7dadc` |
| `docs/decisions/ADR-0001-quality-first-model-routing.md` | `7196cc03755e9298d226f3b3271fe459890836117805957c1cceb37173ac8267` |
| `docs/decisions/ADR-0002-astra-agent-operating-guidance.md` | `88a6d6e0a33aff8622490ecd313567030ef95e3e6d20a12f6f0f1360d05e86d4` |
| `tooling/coordination/AGENTS.md` | `aee04badd44941ac820b71f4359a82b6771128e7ab3f9b0b6da5aab8612272bc` |
| `tooling/coordination/README.md` | `a219084c6d4974da8adf1308b8c4c392ba8819eb5a59fa95c684975adefc366e` |
| `tooling/coordination/templates/REVIEW.md` | `a43dd83f6b9972d2a332e9ca3a570a10989e31d81694af96ee15a158ad52d8aa` |
| `tooling/coordination/harness.py` | `4d6b15408c6b77483c93dace1b693651e6b50c81607f4e2b22084313d2d205e4` |
| `tooling/coordination/routing-policy.json` | `5ebc903a1bd2d3e1925a01fcb1e556f0ed0a4c50682a3b3d93ccc7d7cdd6e979` |
| `tooling/coordination/schemas/evidence.schema.json` | `2f41bb0879ad832c1f8db951924055331506f14ea24208372e8a119e5aba7e3a` |
| `tooling/coordination/schemas/profile-qualification.schema.json` | `9a5ea83d161557e2439d5155662c04ab8f17b47ee295d87fcebea02b5133866c` |
| `docs/qualification/runtime-surface-correction-plan-2026-09-13.md` | `d54cefc5eb9fc87198ddcf7763c17b905b6d92a2b315e5cbdde2d89dae53daf2` |
| `docs/qualification/runtime-surface-correction-verification-2026-09-13.md` | `ff68101fc42e258f8d0563665779ad4e018e3ce015a28b21406ce30a0f8d8545` |
| `docs/qualification/runtime-surface-observation-2026-09-13.json` | `35995674a989b1b77233eafdc80ed092d0a8f8622b88990e8f7b3f8336978091` |
| `docs/audits/2026-09-13-gpt-6-astra-independent-review.md` | `9bddaa709fbbc11568eccd01cf4f2c85f35ba794a315a64c119805c4ba5cd69d` |
| `docs/audits/2026-09-13-gpt-6-astra-review.evidence.json` | `1d453169c1e8e39e3ed25d23cfce095f3bdbde5446ab74b4efb36f8f629a107a` |
| `docs/qualification/README.md` | `20122d35d4f824c761b8be0c7fc3a9cbb94e8a3c16109f26a3f8bf4de9838371` |
| `docs/qualification/model-roster-v2.1.evidence.json` | `8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0` |
| `tooling/coordination/tests/test_instruction_contracts.py` | `1c417d343f1ef89d3489962ba54f3eaf7b6d3df606166ef452eca2af5743dc4d` |

Every review command and test subprocess returned, and the sole yielded unit
test process was collected to exit 0. No persistent session, background job,
server, subagent or harness lease was started by this reviewer. The review
checkout has no `.texenda/` state. All candidate files stayed byte-identical;
only the two assigned review artifacts are added without staging or committing.

The reviewer still has to deliver the final handoff after verifying these two
artifacts. The parent must observe that final task completion before recording
the reviewer as stopped. This file cannot attest its author's future runtime
termination.

No network, credential, account, reset, API-spend, push, deployment, provisioning,
sending or production-data action occurred. NOT RUN: fresh model dispatch
repetition, independent provider model/effort and entitlement introspection,
provider billing telemetry, sandbox/egress enforcement, new-session config
loading, direct CLI model qualification, live roster activation, all 125 product
acceptance criteria and external production/security/legal/provider gates.
