# Independent review — desktop qualification 2026-09-18

**APPROVE** exact source candidate `975d207f469834622810cc623d01a409c80c273e`, tree
`31f516ee383bedab60fd7e28bf9b0adb74e182a1`, against base
`09b77007fc3049b2f391aa0b8f800356990e718e`.
Full-index binary diff SHA-256:
`3ffb896d0320cd834bf723867fd01d56e42deb9deea4bc4ca05771c9655a79b5`.
This does not approve its containing evidence commit or install the roster.

## Actors, authority and limits

Actual source/evidence author and integrator: `/root` (AI).
Initial probe actors: `/root/desktop_astra_probe_20260918` and
`/root/desktop_terra_probe_20260918`.
Independent reviewer: `/root/desktop_qualification_reviewer_20260918`, explicitly
dispatched `gpt-6-astra/max` through desktop collaboration on subscription/APIUSD0.
The reviewer is distinct from all source/probe authors and the integrator.

The [owner instruction](2026-09-18-desktop-owner-authorization.md) conditionally
authorizes this bootstrap, review and forward roster update. It does not grant
product admission, account access or any external effect. The CLI owner label
attributes the actual user's attestation; the actual operator remains AI.
No further personal ceremony is required by the inspected unchanged guard.

The reviewer independently reproduced both five-test fixtures and demonstrated
its own isolated read/edit/test by 16:07:51Z. The corrected
[bootstrap observation](2026-09-18-desktop-reviewer-bootstrap-v2.json) preserves
its predecessor by exact hash. Provider model/effort introspection and measured
token consumption remain unavailable; requested selection is tool-observed,
not established through self-identification. Direct CLI is not qualified.

Initial probes: one per selected profile,600seconds/6000tokens each, no retries.
Independent verifier exercise:600seconds/8000tokens. First source review:
1200seconds/16000tokens; corrected review:600seconds/8000tokens. Entire qualification
phase deadline16:58:25Z; no fallback, downshift, API allocation or reset.
All initial probe and reviewer commands exited; every completed runtime reports
no continuing subprocess. Source authorship is frozen; only serial integration
and evidence/refresh remain. The prior preparation inventory was interrupted
before this bootstrap; it supplies no accepted qualification or preparation work.

## Findings and resolution

Candidate `82c51a338ceacff0c4b7f688c6c34e8a1494a899` was **not approved**.
Its reviewer-bootstrap JSON mislabeled16:07:06Z as verification start. That was
the bundle observation time; first tool observation was16:06:12Z. The v2 successor
records both correctly and retains exact dispatch-start uncertainty. Original
record/commit remain unchanged. Successor SHA-256:
`e4e89359c4103e7c99c7d9c498f33821072c6d88e3e5333dd128310caacfb7cc`.
No other finding was reported; corrected exact candidate approved.

## Reproduced evidence

The reviewer inspected the real diff, request/observation distinction, all
embedded fixture bytes/hashes, native tiers/model/max effort, current desktop
build, seven-day expiries, policy digest, two replacement rows and nine omissions.
All seven original source-candidate paths remained byte-exact after correction.
New roster SHA-256:
`287301864a074adbf920ea83756e40adcb1368cee1a9bf8a18cbe6c221b627a6`.
Sol/max and Luna/max were unnecessary and not tested; lower efforts out of scope.
Omission is not a claim that a model is unavailable to the account.

Independent checks:

- `env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_probe.py`
  in each original fixture:5/5PASS; reviewer fixture expected stubFAIL then5/5PASS.
- Read-only harness `evidence(..., 'roster', require_pass=True)` plus
  `_validate_qualification` for both proposed rows:PASS; no ledger read/write.
- Repository-only `validate.py --check --scope code`:PASS on initial candidate.
- Canonical `env GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 python3 -B
  .agent/scripts/validate.py --check --state-root
  /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda`:PASS by
  16:17:18Z on corrected candidate;156JSON,1TOML,28Python,223links,599bound
  evidence checks; generated freshness checked.
- Canonical harness `--read-only check` and `status`:PASS.
- `git --no-optional-locks diff --check
  09b77007fc3049b2f391aa0b8f800356990e718e..975d207f469834622810cc623d01a409c80c273e`:PASS.

Integrator ran the complete registry in candidate code scope, then canonical
`--check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda`
on`4a01e742b217026652411ee092197aeabba703f8`:all13delegated commands exited0;
refresh writers skipped. This includes coordinator212,workspace117,facade83
(with its two aggregate recursion guards),sealed39 and both14-check packages.
The correction adds only evidence; independent parsing/control verification was
repeated. Full unchanged suites were not repeated by the reviewer. Exact integrated
main receives the complete registry again after approved roster installation.

## Pre-install state and preservation

Independent state SHA remained
`fe218fc97325d3c255825d89cc0046e6ea27d38454c2a7dd06e09c0926d19bb0`;
14receipts, tip`e089594d853bc93a876aef100b779ef416bfaa82e5dacff84d027c6cb3eb8266`,
zero leases, budget0,gatesempty, WP-01 planned/fence0/unassigned.
Binding hash unchanged; mainstill09b7700. Relevant bundles remained
com.openai.codex26.908.70816/build9275. No sealed/product/plan/routing/schema or
permission change. The new observation binds prior protected package/research
baselines; private inputs were not read, sized or hashed. OS-managed atime
stability is not claimed. No product acceptance or external gate is cleared.

## Conditions for next local step

First review the exact evidence-bearing head. Then verify no affected runtime,
lease, lock holder or changed baseline and apply only documented`set-roster`
with this versioned envelope, canonical repository and explicit state root.
Attribute the owner attestation separately from the AI operator. Verify exactly
one appended receipt and only roster/events state-field changes, refresh,
independently audit the resulting exact head, fast-forward clean main, and rerun
required checks. No manual ledger edit, forced integration or history rewrite.
