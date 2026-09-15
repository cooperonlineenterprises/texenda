# Independent review: portable read-only validation correction

Verdict: **APPROVE** with zero unresolved candidate findings for
`0c0f202782720d9d7f34bc1d929d9df8a24868d1`, tree
`e243baffc8acd256047e48bb74b4826c90975424`.

The P2 finding is resolved by a truthful portability limitation. The candidate
retains the meaningful project-preservation guarantees and explicitly discloses
that an operating system may advance access time on reads. It does not claim
that the original literal guarantee covering every filesystem timestamp has
become portable. No timestamp restoration or filesystem-setting change is added.

This approves the exact corrected candidate only. The containing evidence-only
commit, a later generated refresh, local integration and the resulting main
still require their own exact verification. No product or external gate is
approved by this review.

## Subject, independence and bounds

| Field | Value |
|---|---|
| Correction base | `28188ea2bc28d1fd747d8b37e68b50a912b68d4b` |
| Correction base tree | `82f800c242bb6f35471c03afc3ec3209f4b4a50e` |
| Corrected candidate | `0c0f202782720d9d7f34bc1d929d9df8a24868d1` |
| Corrected candidate tree | `e243baffc8acd256047e48bb74b4826c90975424` |
| Canonical full-index binary diff SHA-256 | `74c94cf1c70eac726ceb084665ff1b5c52cc547ebbf3f3868056cb4a0e898738` |
| Candidate author | `/root/clean_workflow_author` |
| Independent reviewer | `/root/clean_setup_reviewer` |
| Integrator | `/root` |
| Detached reviewer worktree | `/Users/jamesryancooper/Projects/texenda/worktrees/clean-workflow-review-20260915` |
| Corrected-review entry | `2026-09-15T16:53:07Z` |
| Evidence-only follow-up entry | `2026-09-15T16:56:16Z` |

The assigned profile is T1 `gpt-6-astra/max`, exact ID `gpt-6-astra-max`,
`codex-desktop-collaboration`, subscription billing. The corrected read-only
review has a 20,000-token / 1,200-second bound; this later evidence-only follow-up
has a separate 15,000-token / 900-second bound. API allowance and spending are
USD 0. No fallback, effort downshift, child agent, or live-ledger assignment is
used. Measured provider token accounting and independent executing-model
introspection remain unavailable.

The exact live profile was rechecked for the corrected review and again before
evidence authoring. It records client `26.901.41600 (build 7982)`, read/edit/test
capabilities, verification `2026-09-13T21:44:31Z`, expiry
`2026-10-12T21:44:31Z`, and check `desktop-profile-gpt-6-astra-max`.
`Harness.qualified` confirms availability from the owner-attested roster evidence
`docs/qualification/model-roster-v2.1.evidence.json`, SHA-256
`8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0`.
This is a dated observation, not another roster or a fresh qualification.

Routing-policy digest:
`61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0`.
Work-package digest:
`9ad162070c27e4c765ba145fc8a35d31dc288482453daaa39ec0bb6add8bd8d8`.

The canonical diff was verified with:

```text
git --no-optional-locks -c core.abbrev=40 -c color.ui=false diff --no-ext-diff --no-textconv --full-index --binary 28188ea2bc28d1fd747d8b37e68b50a912b68d4b 0c0f202782720d9d7f34bc1d929d9df8a24868d1 | shasum -a 256
```

## P2 finding and resolution

Final approval of `28188ea2bc28d1fd747d8b37e68b50a912b68d4b` was withheld
after two complete validation runs passed but their surrounding strict metadata
snapshots detected an access-time change. The first run took 19.226 seconds;
the field-level repeat took 18.598 seconds. The repeated observation was:

| `.agent/generated/manifest.json` field | Before | After |
|---|---|---|
| `atime_ns` | `1789490486225265910` | `1789490575483816624` |
| `mtime_ns` | `1789490394144419224` | unchanged |
| `ctime_ns` | `1789490394144419224` | unchanged |
| Inode | `687575508` | unchanged |
| Size | `53139` | unchanged |
| SHA-256 | `b0e22d79ce7a75bce4dbab21f97395fe032303714197eac1e3c1c315ce24cbde` | unchanged |

The other 361 entries were unchanged. This was an operating-system-managed
access-time effect, not a source-content write or observed explicit timestamp
write. Nevertheless, the literal all-timestamps-stable assertion was not met,
and the reviewer did not approve that assertion or restore timestamps.

The new 20-file candidate corrects the active contract in ADR-0006,
`project-dossier/validation/README.md`, `.agent/generated/README.md`, tool and
registry metadata, validation JSON, and generated manifest/report limitations.
It defines read-only validation as no explicit project writes while preserving
content, path membership, mode, size, mtime, ctime, generated outputs, caches,
locks and live state. OS-managed atime may advance during reads and is explicitly
outside the portable guarantee.

No source code attempts to prevent or restore access time, mutate filesystem
settings, or weaken content/path/symlink/receipt/lock safeguards. Only the declared
generated refresh changes derived files. The correction retains the exact
ordinary command and explicit external state-root selection; no wrapper, fallback,
initialization, authority expansion or second state store is introduced.

Deterministic tests protect the disclosure and the preserved properties.
Independent in-memory mutations were rejected when they:

1. changed the facade tool's side-effect declaration back to `none`;
2. removed the access-time limitation from the registry purpose; or
3. removed it from the generated manifest.

The respective errors were `facade tool overclaims portable timestamp stability`,
`facade check purpose overclaims portable timestamp stability`, and
`generated validation limitations overclaim portable atime stability`.
No repository file was modified to perform these negative checks.

## Exact verification

Commands ran from the detached reviewer worktree with
`PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`.

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s .agent/tests -p 'test_*.py' -v
env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tooling/coordination/tests -p 'test_instruction_contracts.py' -v
git --no-optional-locks diff --check 28188ea2bc28d1fd747d8b37e68b50a912b68d4b..0c0f202782720d9d7f34bc1d929d9df8a24868d1
```

| Check | Result |
|---|---|
| Exact ordinary complete check | PASS, exit 0, 19.221 seconds |
| All nine dispatched registry commands | Exit 0; both refresh writers skipped |
| Standalone facade suite | 35 tests, 49.850 seconds, PASS without skips |
| Targeted instruction suite | 16 tests, 0.056 seconds, PASS |
| Independent atime-disclosure negatives | Three mutations rejected |
| Registered workspace/coordinator/sealed suites | PASS |
| Both registered package checksum validators | PASS, 14/14 each |
| Strict parsing | 134 JSON, 1 TOML, 19 Python |
| Dossier/instruction/link validation | 30 dossier paths, 3 instruction files, 126 links |
| Hash-bound PASS/FAIL evidence checks | 496 |
| Generated reconstruction | All eleven outputs match |
| Diff and protected-path comparisons | PASS |

The registered commands exercised the workspace contract, facade/workspace/
coordination/sealed test suites, both package validators, external-ledger check,
and Git whitespace check. The standalone facade run includes the complete-check
fixture skipped during recursive aggregation. Targeted instruction tests confirm
the ordinary validation/status/ready/context and assignment/review/resumption
routes remain intact.

The exact generation is
`e393135a44b4c84896e47c90ae776f37e92866f770b3e06fcf8877c9a9fae633`;
source-scope SHA-256 is
`fb2a83c6ed2e6756e078ce74a3f302b1c6bd91f81b0f334950a74e749ed3361d`.
Validation JSON explicitly reports `explicit_project_writes: false`, all ten
preserved properties, `portable_atime_stability: false`, and the atime limitation.
Generated manifest and validation-report limitations agree and reconstruct from
the approved source.

## Preservation measurement

An in-memory before/after snapshot surrounded the corrected complete check.
The interval also included concurrent read-only facade testing; individual access
times are observations of that interval, not attribution to one particular read.
Across 362 review-worktree and external-state paths, there were **zero changes**
to content hashes, path membership, mode, device/inode, size, mtime or ctime.
Generated outputs, caches, locks and live-state bytes were preserved.

The measurement recorded, rather than restored, these OS-managed access times:

| Path within review worktree | Before `atime_ns` | After `atime_ns` |
|---|---|---|
| `.agent/scripts/validate.py` | `1789491187541640970` | `1789491259122540004` |
| `.agent/generated/manifest.json` | `1789491187541472719` | `1789491259122288086` |
| `.agent/tests/test_validate.py` | `1789491187541777304` | `1789491259122703755` |

Private subtrees and CSV content were rejected from the snapshot scope. Shared
Git internals beyond the worktree's `.git` pointer, other worktrees and disposable
fixtures outside the measured roots were outside this snapshot. No claim of
portable atime stability follows from this proof.

| Protected observation | Result |
|---|---|
| External state SHA-256 | `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235` |
| Receipt count | 13 |
| Receipt tip | `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e` |
| Live profiles / leases | 11 / 0 |
| Budget / cleared gates | USD 0 / empty gate map |
| Sealed manifest SHA-256 | `37fffb1a165cfa6b907e7433d617c06e1c64ff09cd282173f7d791cace2ac07e` |
| Source manifest SHA-256 | `8576bf08ec4f2a4718476eca70e6d1d5cb2b6be1af550bf5c20c692bcbaff715` |
| Exact transition-history SHA-256 | `1f5b0b1aa816f6bcd34f591a0b5f9f5b4e9d6e8bf35474ca77367418fb930919` |

Protected comparisons preserve `specs/texenda-handoff`, both package semantics,
existing review evidence, retained transition history, coordinator code, routing,
permission/trust owners and ADR-0001/4/5. Both package checksum validators and
the workspace byte audit pass; all eleven package differences remain classified.
No product or external gate changed.

Private checks used only exact final-file existence and Git ignore/tracking:
`local/private-inputs/kit/ohw/2026-09-14/subscribers.csv` exists outside Git,
the old repository-relative location remains ignored, and no private CSV is
tracked. No private contents, sizes, hashes, copies, parsing or directory
listing were accessed. Content equality is not inferred from those checks.

The worktree remained clean at the exact corrected head/tree. No source,
generated, package, private-input or live-state file was explicitly edited by
the reviewer. All completed review processes were reaped.

## Earlier review remains immutable and scoped

The original clean-workflow review still applies only to
`48033f36b448167511bddd379fde04684918fdb1`. Its exact hashes remain:

- `2026-09-15-clean-workflow-independent-review.md`:
  `ae2a4fb0ff2fdd40ca6167d01b17f91e8c8b17cc59fd8c6ec56968e846341f2b`;
- `2026-09-15-clean-workflow-review.evidence.json`:
  `40d520813d66f27c90d551e490080396067dc0363cb60791da3869ffcb5fc37a`.

`Harness.evidence(require_pass=True)` revalidated that envelope against its exact
old candidate and task. It is not silently repurposed as approval of this
correction. Its dated snapshot observations remain intact; they never establish
a universal guarantee for a later head or another filesystem.

The inherited `836e209..338cd135` editor/Blueprint present audit and its historical
integration-before-final-audit timing exception remain unchanged. No old evidence
is backdated or rewritten. Blueprint 4.2.0 remains unqualified, no reviewed seed
or upgrade is supplied, and WP-10/VAL-03 remain gated.

## Evidence-only handoff and limits

Only this Markdown and the paired closed v2 review envelope may be added by this
follow-up. The exact parent of their evidence-only commit must be the approved
corrected candidate. Every PASS envelope row binds this Markdown's exact hash.
`TRN-WSM-0001` is an existing transition reference, not a new task ledger or WP
receipt. The containing commit/tree and file hashes are reported separately to
avoid self-reference.

Adding evidence makes the generated evidence index stale. The integrator must
explicitly refresh only declared outputs and obtain an independent final audit
of that exact head before local integration. This writer does not refresh,
integrate, or approve its containing evidence commit.

All review command sessions completed; no child agent or background job remains.
The parent must observe this evidence-authoring runtime's final stop before scope
release. No GitHub, Codex UI, global skill, upstream source, private input,
filesystem setting or live ledger was changed. No push, deployment, publication,
spending, hosted workflow, activation or external-gate clearance occurred.
GitHub and Codex registration were not re-queried by this reviewer; those remain
the integrator's separately observed scope.
