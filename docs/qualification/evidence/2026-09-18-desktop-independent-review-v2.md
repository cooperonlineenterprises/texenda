# Independent desktop qualification review — corrected evidence v2

Approved source remains `975d207f469834622810cc623d01a409c80c273e`,
tree`31f516ee383bedab60fd7e28bf9b0adb74e182a1`, base
`09b77007fc3049b2f391aa0b8f800356990e718e`, binary full-index diff
`3ffb896d0320cd834bf723867fd01d56e42deb9deea4bc4ca05771c9655a79b5`.
This record preserves that independent approval; it does not approve its own
containing head or perform roster installation.

## Successors and retained failed evidence

This supersedes the evidentiary command transcription and redundant qualification
metadata in [the v1 log](2026-09-18-desktop-independent-review.md) and
[the v1 envelope](2026-09-18-desktop-review.evidence.json). Their exact hashes,
including the retained [bootstrap correction](2026-09-18-desktop-reviewer-bootstrap-v2.json), are:

```text
9594c009f03160d546119f1d7f203ecb1a88cb294a36169049c993248764fe30  docs/qualification/evidence/2026-09-18-desktop-independent-review.md
dc9ff2303051314ab3b090e8bca552d8cb675133081747efb99a963f9d000182  docs/qualification/evidence/2026-09-18-desktop-review.evidence.json
e4e89359c4103e7c99c7d9c498f33821072c6d88e3e5333dd128310caacfb7cc  docs/qualification/evidence/2026-09-18-desktop-reviewer-bootstrap-v2.json
```

Candidate82c51a3 was not approved because bundle-observation time was mislabeled
as verifier start. The bootstrap-v2 successor records first tool observation
16:06:12Z and bundle observed by16:07:06Z; actual dispatch start is unavailable.
Original evidence is untouched. Corrected source975d207 was approved.

Evidence-bearing candidate9063919 was not approved for installation: its copied
qualification row referenced a check absent from that review envelope, and the
log retrofitted optional-lock flags into older commands. V2 uses the ordinary
review-template fields, references the existing qualified probe/bootstrap checks,
and does not copy a redundant qualification row. The exact historical command
spellings are below; current equivalent hardened commands are separately attributed.
These are evidence corrections only; roster/probes, product plan, policy, code,
permissions and live state remain unchanged. Reassessment retained the required
T1/max route and strengthened envelope/transcript verification, not a lower route.

## Actors and qualification limits

Source/evidence author and integrator: `/root` (AI). Initial probe actors:
`/root/desktop_astra_probe_20260918` and `/root/desktop_terra_probe_20260918`.
Distinct independent reviewer:
`/root/desktop_qualification_reviewer_20260918`, explicitly dispatched
`gpt-6-astra/max`, desktop collaboration26.908.70816(build9275), subscription,
APIUSD0. No fallback/downshift or model-self-identification proof.

Under the [current owner's conditional bootstrap authority](2026-09-18-desktop-owner-authorization.md),
the reviewer independently reproduced both five-test fixtures and completed its
own isolated read/edit/test by16:07:51Z. All fixture bytes/hashes matched.
Provider model/effort introspection and actual token use are unavailable.
The user supplies conditional attestation; `human:owner` identifies that actual
user, while the shell operator remains AI `/root`. The unchanged CLI does not
authenticate identity or require an additional personal interactive ceremony.
No product-facing AI, direct CLI, account connection or external gate is qualified.

The selected new [roster](../model-roster-v2.2.evidence.json), SHA
`287301864a074adbf920ea83756e40adcb1368cee1a9bf8a18cbe6c221b627a6`,
has only Astra/max and Terra/max, with native tiers1/3 and exact seven-day
windows. Other nine historical rows are omitted, not overwritten. Sol/max and
Luna/max were unnecessary, not tested and not declared account-unavailable.
Every lower effort remains out of scope. Earlier invalid-build inventory was
interrupted and supplies no qualification or accepted preparation work.

## Actual independent commands and results

On source975d207, completed by16:17:18Z, the reviewer ran exactly:

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda && git diff --check 09b77007fc3049b2f391aa0b8f800356990e718e 975d207f469834622810cc623d01a409c80c273e
env PYTHONDONTWRITEBYTECODE=1 python3 -B /Users/jamesryancooper/Projects/texenda/repo/tooling/coordination/harness.py --root /Users/jamesryancooper/Projects/texenda/repo --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda --read-only check
env PYTHONDONTWRITEBYTECODE=1 python3 -B /Users/jamesryancooper/Projects/texenda/repo/tooling/coordination/harness.py --root /Users/jamesryancooper/Projects/texenda/repo --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda --read-only status
```

All passed:156JSON,1TOML,28Python,223links,599bound checks, generated freshness.
In the separate9063919 review, hardened equivalents with optional locks disabled
passed by16:21:29Z:157JSON,223links,603bound checks. The v1 embedded qualification
validation failed as recorded above. No installation approval was issued for906.

The reviewer also ran `env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_probe.py`
in each isolated fixture; both originals5/5PASS and its own expected stubFAIL
then5/5PASS. Read-only `Harness.evidence(...,'roster',require_pass=True)` and
`_validate_qualification` verified both proposed roster rows. Only the unnecessary
copied row in the v1 review envelope failed its own check-ID binding.

Separately, the integrator's code-scope full registry and canonical full registry
on4a01e742 passed all applicable commands, including coordinator212,workspace117,
facade83(with two aggregate recursion guards),sealed39 and each package14checks.
The registry was not executed by the reviewer as a duplicate full-suite run.
Evidence-only corrections received fresh parsing/hash/control checks. Integrated
main will receive the complete registry after the approved forward update.

## Preservation, bounds and next boundary

Through the906 audit, state SHA remained
`fe218fc97325d3c255825d89cc0046e6ea27d38454c2a7dd06e09c0926d19bb0`;
14receipts, tip`e089594d853bc93a876aef100b779ef416bfaa82e5dacff84d027c6cb3eb8266`,
no leases, WP-01 planned/fence0/unassigned, budget0,gatesempty. Mainstill09b.
Binding/roster hashes and all accepted historical evidence were unchanged.
No private input contents,size,hash or external account was accessed. OS-managed
atime stability is not claimed. All probe/reviewer subprocesses exited.

Initial probes600seconds/6000tokens each; verifier600/8000; source review1200/16000;
corrected-source600/8000; evidence-head600/8000. All share the hard qualification
phase deadline16:58:25Z. Measurement/enforcement of provider tokens is unavailable.
No retries of substantive profile failures, reset, API allocation or paid credit.

A final independent audit of the v2 evidence-bearing head is still required.
Only afterward, with stopped affected runtimes, no leases/lock holders and exact
baseline continuity, may the AI operator invoke normal owner-attested set-roster.
Verify one appended receipt and roster/events-only field changes, then record,
refresh, review and fast-forward local main. No product work or gate changes.
