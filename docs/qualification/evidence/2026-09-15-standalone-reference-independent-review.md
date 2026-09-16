# Standalone reference remediation — independent candidate review

Status: APPROVE the exact source-and-generated candidate below, with zero unresolved candidate findings. Issued 2026-09-16T00:18:55Z (2026-09-15 in America/Chicago).

This is immutable, bounded review evidence. It approves neither its containing evidence commit nor any future refresh, integration or head. It is not an implemented family migration, product-readiness result, external-gate clearance or authorization for additional work. Corrections require a successor record.

## Subject, authority and independent actors

| Role | Exact subject |
|---|---|
| Accepted base | `7de052690bbf3e2879f375c2b2e17207c7ee5bfe` |
| Initial source commit/tree | `385ce8eddef06fdc0ab9d46222e4c347fa1c11bd` / `6b57fa35b5afb7c00c2eb119b53ee1d0a524b3e8` |
| First corrected source commit/tree | `9f3d4db74577b15d79424f7bc5c7bbc1fb24cee3` / `fc2f0824f126d3675d89facabb7acf35acf43c09` |
| Final scope-correction source commit/tree | `8a3920e6c4fdb7a738b7044e56b3d48b7f918e52` / `ce8bf52393f4b00be8f2d27a1d1efbf1eb2c982b` |
| Approved source-and-generated candidate | `82da3f644ea82d6bc7531c1711c63b54eb3b9f5b` |
| Approved candidate tree | `d8d1f195e686a7c6071f54eb1a40bb2afbfd61c1` |
| Canonical base-to-candidate binary diff SHA-256 | `792b297946e52871dbe8c235e636eb6f18806474d5155dc5cd077d722af9f707` |
| Source author | `/root/standalone_contract_author` |
| Independent reviewer | `/root/architecture_synthesis_reviewer` |
| Integrator | `/root` |

The author, reviewer and integrator are distinct actors. The reviewer inspected the initial delta, independently reproduced material failures, reviewed each correction and reproduced the final checks. No review subagents were used. The reviewer subsequently authors only this evidence pair under the separate bounded evidence-recording assignment; that does not extend approval to the evidence-bearing head.

The current owner remediation request superseded the earlier read-only architectural-audit scope for necessary repository-local edits, tests, designated refresh, local commits, review evidence and independent review. This evidence-recording assignment permits only two new files under docs/qualification/evidence and their local commit. Pushes, external mutations, private-input contents, other repositories/global skills, gate clearance and history rewriting remain outside scope. No designated refresh is performed by this evidence-recording assignment.

Applicable authority includes [AGENTS.md](../../../AGENTS.md), the [entry point](../../../.agent/START_HERE.md), [policy](../../../.agent/policy.json), [context](../../../.agent/context.json), the [single registry](../../../.agent/validators.json), scoped ADRs 0004/0006/0007, and the existing coordinator instructions. [ADR-0007](../../decisions/ADR-0007-standalone-workspace-operating-contract.md) owns OPS-WSM-0001 operating metadata. That ID in the envelope is a contract reference, not a newly admitted WP, lease, receipt or task ledger.

Reviewer qualification: exact `gpt-6-astra-max`, model `gpt-6-astra`, effort `max`, T1, `codex-desktop-collaboration`, client recorded as `26.901.41600 (build 7982)`, subscription sign-in/billing, no fallback or downshift. Qualification verified at `2026-09-13T21:44:31Z`, expires `2026-10-12T21:44:31Z`; required check `desktop-profile-gpt-6-astra-max`. [Roster evidence](../model-roster-v2.1.evidence.json) SHA-256: `8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0`. Canonical routing-policy digest: `61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0`.

Qualification records and actor labels do not authenticate the provider's actual executing model or principal. Provider token/usage metering was not available to this reviewer. No separate numeric reviewer allocation was supplied in the delegated assignments; no allocation or runtime-stop attestation is invented. No API call, API spend or paid-route substitution was performed.

## Rejected candidates and exact resolutions

| Rejected candidate/tree | Independent P2 finding | Resolution in approved candidate |
|---|---|---|
| `a0bdca755d1df6f7c1cf791d9d1f7641c2baa107` / `8ff7685331f4df8e820b58c6ed6d988d228597a5` | The facade registry claimed code eligibility but resolved to default control and exited 2 without state-root. | Separate facade-code-check and facade-check entries execute their declared scopes; mismatched resolution is rejected and aggregation skips both self-commands. |
| Same rejected candidate | Editable remediation deferral details could disagree with RAIDQ; an in-memory contradictory blocker passed validation. | Closed deferred_ref records resolve the sole RAIDQ owner. Inline overrides, unknown/missing sources and mismatched record IDs are rejected. |
| Same rejected candidate | Replacing a real Blueprint path in both current lists passed the 85-count check. | The complete inventory and every mapping field are compared with immutable accepted Git history at the base. Coordinated substitution and field changes are rejected. |
| `486e65dc9fe8331274d00c7fc06685ff1897fafb` / `7ac80ea08b1ca3670c7449b8e9874b7add1a6b12` | External Plectarium/Octon family work was incorrectly described as Texenda migration and assigned a Texenda migration owner/dependency. | RAIDQ-0007/-0008 name those external families' own repositories and owners. Texenda is advisory only; Blueprint qualification is conditional on actual source adoption/upgrade, separate from layout authority. |

Both rejected commits remain in Git. SUP-0004 labels the original schema-v1 predecessor rejected, not accepted or integrated. The second rejection remains part of this exact review history. Historical passing test results did not conceal those findings and do not approve either rejected candidate. No rejected history was rewritten.

Canonical diff reproduction:

```text
git --no-optional-locks -c core.abbrev=40 -c color.ui=false diff --no-ext-diff --no-textconv --full-index --binary 7de052690bbf3e2879f375c2b2e17207c7ee5bfe 82da3f644ea82d6bc7531c1711c63b54eb3b9f5b | shasum -a 256
```

An earlier abbreviated-index binary serialization of the first candidate produced a different digest from full-index serialization. Matching exact commits/trees and use of the declared full-index command resolved that representation difference; it was not candidate drift.

## Reviewed architecture, dispositions and boundaries

The [remediation register](../../../project-dossier/conformance/remediation-register.json) retains all 18 findings: seven source-candidate remediations, six deferred concerns, one reported already-resolved app-registration concern, three retained controls/history concerns and one deliberate capability omission. The counts describe the reviewed candidate only and are not a second mutable status ledger. Acceptance of source remediation is separate from the register's future integration/evidence follow-up.

The review covered refresh discovery; code/control worktree boundaries; ready-to-selected-context flow; portable guidance; app-registration disposition; private-control unknowns; composite owner navigation; workspace retention; Blueprint qualification; external Plectarium/Octon work; standard publication; compatibility; exact mapped coverage; optional capabilities; retained history; CLI qualification; and hosted repository/CI boundaries. App registration is an attributed integrator observation in REM-0005, not independently reverified by this reviewer; local navigation/evidence follow-up remains outside candidate approval.

The ADR embeds one strict JSON operating contract rather than creating an independently edited companion. Nineteen path roles, seven retention classes and 45 navigable owner-reference sets validate. Existing policy/context, decision, task, receipt, routing, evidence and product owners retain their scopes. Composite references route to existing owners and scoped amendments, not substitute mutable truth. The dossier owns only its declared interpretation, conformance and maintenance information.

RAIDQ owns current deferred details. Remediation dispositions and crosswalk navigation reference it. Private control, Blueprint qualification, Plectarium work, Octon work, standalone publication and direct CLI qualification are separately classified; standalone publication has no Plectarium dependency. Plectarium's established family contract does not authorize a new migration. Octon work concerns octon, octonos and octon-mini, preserves dirty/worktree/unborn state and does not inherit Texenda authority.

All 85 Blueprint inventory paths and complete mappings are unchanged from the accepted base, as are the six supplemental mappings, five supplemental high-assurance entries, 35 artifact/path pairs and all ten compatibility dispositions. Existing indexes/functionally equivalent owners remain; no generic duplicate stores or optional .agents packages are installed.

Code scope rejects state-root input and operates on repository sources with eligible synthetic tests. It leaves control/live/generated freshness unassessed. Canonical control requires the active binding and explicit absolute state root; it fails closed on wrong/missing/relative/symlinked/moving/competing roots and pending transactions. Worktree inspections use the canonical script/root with --read-only. That flag rejects mutations and context output before Harness construction; it does not authenticate callers or prevent deliberate omission. Candidate worktrees do not copy live bindings, ledgers or receipt inputs.

Ready output leads to explicit selection of an eligible work-package ID for the objective. Empty readiness has no fallback; resumption uses the recorded task/fence. Context is not assignment. Existing assignment, review and resume templates now distinguish code and control roots.

Refresh discovery is read-only --help. Checks skip refresh writers; actual refresh/recovery is canonical-only and explicit. Retention grants no deletion permission, protects both package variants, decisions, evidence, branches/bundles/archive history, four exact receipt inputs, active binding/ledger and recovery records. Private access/retention remains unqualified.

Selected Blueprint 1.0.0 remains an inspected structural reference, high-assurance mapped-existing. Clean 4.2.0 remains PASS/PASS/FAIL and unadopted; dirty uncommitted 4.3.0 is separate and unqualified. The authentic reviewed upgrade seed remains absent. RAIDQ-0005 bytes, origin record and retained predecessor are preserved. No upstream qualification, generator, adoption, installation or upgrade was performed by this review.

## Commands and results

Final candidate commands ran from `/Users/jamesryancooper/Projects/texenda/repo` with bytecode disabled:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --scope code --all
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
git --no-optional-locks diff --check 7de052690bbf3e2879f375c2b2e17207c7ee5bfe..82da3f644ea82d6bc7531c1711c63b54eb3b9f5b
```

| Final check | Observed result |
|---|---|
| Full code aggregation | PASS, exit 0; 8 dispatched checks; live/control/generated freshness unassessed |
| Full control aggregation | PASS, exit 0; 11 dispatched checks; both refresh writers skipped |
| Registered facade/workspace/coordinator/sealed suites | Exit 0, including the new scope/deferral/mapping/family negatives |
| Both package checksum validators | Exit 0 through control aggregation; both independently returned 14/14 PASS during the first candidate review |
| Code parsing | 133 JSON, 1 TOML, 23 Python |
| Control parsing | 140 JSON, 1 TOML, 23 Python |
| Dossier/instruction coverage | 32 paths, 3 instruction files |
| Local links | 133 code / 200 control |
| Bound PASS/FAIL evidence checks | 562 before this evidence pair |
| Generated reconstruction | All 11 output byte sequences match |
| Protected source and whitespace checks | PASS |

The exact delegated suite commands are the registry's python3 -B -m unittest discover commands for .agent/tests, tooling/workspace/tests, tooling/coordination/tests and specs/texenda-handoff/08-project-harness/tests, with test_*.py and -v. Package commands are python3 -B specs/texenda-handoff/10-validation/validate_package.py --checksums and python3 -B /Users/jamesryancooper/Projects/texenda/sources/handoff-1.1.0-20260914/10-validation/validate_package.py --checksums.

During the first review, `env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s .agent/tests -p test_standalone.py -v` passed all 11 then-existing tests in 46.342 seconds, including the clean-clone/worktree aggregation that outer --all deliberately skips to avoid recursion. Later complete aggregations ran the new correction tests; the independent clone/worktree implementation was unchanged. No claim is made that recursively skipped tests reran on the final head.

Independent correction probes directly executed both resolved registry self-commands and observed code/control scope with exit 0. The previously accepted coordinated inventory substitution now raised the immutable-baseline denial; an inline deferred_ref blocker override now raised the closed-reference denial. These probes changed in-memory objects only.

Approved generated identity: generation `7bc4fe7f60f9ba5d35e39191e1d2cca058aac766553104c78755f4fa3a25f5a9`; source-scope SHA-256 `8426d44e52f8513128ae90fb65e61c2b7ac38d3d4680a50d440fb958012ce7be`; recorded source `8a3920e6c4fdb7a738b7044e56b3d48b7f918e52`, tree `ce8bf52393f4b00be8f2d27a1d1efbf1eb2c982b`; generated at `2026-09-16T00:13:23+00:00`. The final full HEAD/tree was separately verified, avoiding a containing-commit hash cycle.

Protected base-to-candidate comparisons were empty for the sealed package, origin, preexisting qualification evidence, policy/context, routing policy and relocation helper. Prior ADR preservation was checked during the first review. Both source variants retain their roles; no product semantics, external gate or receipt was amended by the candidate.

## Preservation and limitations

Before/after in-memory snapshots around each candidate review compared path membership, mode, size, mtime, ctime and symlink targets across repo (including Git metadata), sources, archive, local/agent-state and local/logs. These are metadata observations, not claims of independent whole-archive byte hashing. Directory metadata can appear in both parent and own traversal records. Tracked/source/package content was covered by Git and the declared checks; state and binding were separately hashed. Private-input trees were excluded entirely.

| Final review scope | Metadata entries | Equal before/after metadata SHA-256 |
|---|---:|---|
| repo | 3245 | `a11391c9dde94cacfe314d10f9909ce50aa30eb0918fb8ba22ce08868f40b340` |
| sources | 126 | `bd5de5a58f61b87d0fa2dcd60331b36b768e0e4f51723acf78c655a7da2a9798` |
| archive | 6548 | `e5b2880dbddceac73d70c1b3ad30089abad82e8216061adaf88b470308d52958` |
| local/agent-state | 6 | `fffe23cc7683c3e4399577e5627d25253be5ff483c19259bab3fb1018d1c5e02` |
| local/logs | 8 | `3971427831a9c21f266a5a411af80351854c63df04425cf04624f0205f5f7718` |

Ledger SHA-256 stayed `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`; binding SHA-256 stayed `a92b6137856b7f9c2b3f13f69f4e6dc92ed4da1be82eec1ddf21188ebdde0365`. The generated receipt observation remained 13 receipts with tip `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e`. The checkout remained clean at the approved candidate throughout final review. No source, state, binding, parent guidance or generated output was edited by the reviewer during review. Synthetic tests wrote only disposable fixtures outside measured project roots. OS-managed atime is outside the portable no-write guarantee; no timestamp restoration was attempted.

Integrator-reported limitation, not independently reproduced: During root integrator baseline inspection, one combined metadata command inadvertently queried the private CSV's file-size field once. The value was not used or persisted in project evidence; no contents were opened, parsed, copied or hashed. The independent reviewer did not inspect private contents or size. This record retains no size value and makes no whole-workflow no-size-access claim.

No external effect, publication, push, deployment, spend or production access occurred in the reviewer work. Private access controls remain unqualified. No product criterion, deployment/security gate or external approval was passed. No claim is made about future heads, the containing evidence commit, final integration, actual runtime termination, unperformed upstream qualification or the app registration beyond attributed evidence.

Adding this evidence pair is a separate authorized local write. It intentionally changes the evidence index inputs and requires the integrator's later designated refresh and independent review of the evidence-bearing/integrated head. This review does not perform that refresh or preapprove its result.
