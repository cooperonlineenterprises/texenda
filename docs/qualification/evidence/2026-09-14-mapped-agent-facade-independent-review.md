# Independent review: mapped Texenda facade and state-root candidate

Verdict: **APPROVE**. Zero unresolved findings in the exact code/facade candidate below. All 27 findings recorded across six rejected predecessors are resolved. This is immutable, bounded reviewer evidence; documentation and passing checks do not grant new authority.

## Scope and exact identity

| Field | Value |
|---|---|
| Base revision / tree | `680457854984020d0c8616a7f640a63079be9b3c` / `af3236e7639c163ba1766a5599286c3775ac53c1` |
| Approved candidate / tree | `7a1c37619e342370be0b0b05782727871a74b94f` / `ef31ca76c1b8dbee7bd8734246f91d93ef5f1205` |
| Canonical base-to-candidate binary diff SHA-256 | `469987ee1c5239f0d4026b1aef50454708a905090bd4c05d65291f5f0ffa26ba` |
| Latest rejected predecessor | `1bc710394a47931a2320f7b6cee0733a2dd991b6` |
| Latest correction diff SHA-256 | `f210e2c0818046901fb9c48772655322122fe4b99b432b770ac3314eb09e5b2a` |
| Author | `/root/mapped_facade_author` |
| Independent reviewer | `/root/review_mapped_facade` |
| Integrator | `/root` |
| Reviewer worktree | `/Users/jamesryancooper/Projects/texenda/worktrees/mapped-agent-facade-final-candidate-review` |
| Evidence issued / qualification rechecked | `2026-09-14T23:04:05+00:00` |
| Runtime / Python | Codex desktop collaboration / Python 3.13.9 on macOS |

Author, reviewer and integrator are distinct actors. The complete base-to-candidate result was reviewed through the initial full review and each complete corrective diff, preserving unchanged verified context. Root/nested instructions, accepted ADRs, operating/review contracts, changed sources and generated outputs were inspected or deterministically reconstructed. No source edit was made to make a candidate pass.

Approval covers this exact code/facade candidate only. It does **not** approve the containing evidence-only commit, an evidence head, integration, live state/private-input relocation, a real mapped task lifecycle, product acceptance, deployment, publication, or external gates. Any semantic candidate change requires new review. The integrator must separately refresh generated views and validate the resulting evidence/integration head.

Canonical serialization used for both bindings:

```sh
git --no-optional-locks -c core.abbrev=40 -c color.ui=false diff --no-ext-diff --no-textconv --full-index --binary 680457854984020d0c8616a7f640a63079be9b3c 7a1c37619e342370be0b0b05782727871a74b94f | shasum -a 256
git --no-optional-locks -c core.abbrev=40 -c color.ui=false diff --no-ext-diff --no-textconv --full-index --binary 1bc710394a47931a2320f7b6cee0733a2dd991b6 7a1c37619e342370be0b0b05782727871a74b94f | shasum -a 256
```

Early abbreviated diff output was configuration-sensitive: the first rejected candidate's ambient hash was `e5231abc5c43fbeb045e0da99b56064a9c8441cf5a020a342b05d7e7e3a9f3af`, while its canonical full-index hash was `2e2e8f4334afd93211135f50a37630507d713c2ae56f9d8afa66a604c02b4ae1`. Canonical serialization governs; this was not a tree mismatch.

## Exact reviewer qualification

Requested and qualified route: **gpt-6-astra / max / T1**, profile `gpt-6-astra-max`; no downshift or fallback. Runtime `codex-desktop-collaboration`; roster client version `26.901.41600 (build 7982)`; sign-in and billing `subscription`; capabilities read/edit/test. API allocation and API spend: zero. Provider token accounting and independent provider-level executing-model/effort introspection were unavailable. No new runtime qualification or entitlement is claimed.

Qualification was verified at `2026-09-13T21:44:31Z`, expires at `2026-10-12T21:44:31Z`, and was rechecked through the live ledger using `Harness.qualified(..., 'gpt-6-astra-max')` at the issue time above.

| Binding | Repository-relative source | SHA-256 |
|---|---|---|
| Owner-attested roster | `docs/qualification/model-roster-v2.1.evidence.json` | `8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0` |
| Required check `desktop-profile-gpt-6-astra-max` | `docs/qualification/probes/2026-09-13/gpt-6-astra-max-desktop.json` | `e62f78f3930ffd840c0d5d596a910a87187fe26bdad314b925711a0d39ab8df0` |
| Runtime observation | `docs/qualification/runtime-surface-observation-2026-09-13.json` | `35995674a989b1b77233eafdc80ed092d0a8f8622b88990e8f7b3f8336978091` |
| Routing policy raw bytes | `tooling/coordination/routing-policy.json` | `5ebc903a1bd2d3e1925a01fcb1e556f0ed0a4c50682a3b3d93ccc7d7cdd6e979` |
| Work-package catalog | `specs/texenda-handoff/05-implementation/work-packages.json` | `9ad162070c27e4c765ba145fc8a35d31dc288482453daaa39ec0bb6add8bd8d8` |
| Accepted mapped-workspace decision | `docs/decisions/ADR-0004-mapped-project-workspace.md` | `e1594f793c892adecfebbf86ce76c7fb180d79cc66497d936fd215ea773b8b08` |
| Independent-review template | `tooling/coordination/templates/REVIEW.md` | `a43dd83f6b9972d2a332e9ca3a570a10989e31d81694af96ee15a158ad52d8aa` |

Canonical routing-policy digest: `61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0`. This intentionally differs from the raw-file SHA-256. The qualification snapshot is evidence, not a duplicate live roster. Existing live qualification/receipt ownership is unchanged.

## Rejected predecessors and resolved findings

Each predecessor remained rejected and preserved in Git history. This is the complete numbered finding history from this independent reviewer; repeated/adjacent defects are retained rather than silently collapsed. Every resolution below is verified in the approved candidate, not a retroactive approval of a predecessor.

| Rejected revision | Finding IDs | Review scope |
|---|---|---|
| `c9d10ec96b648637efb17f5a3e362262aeaddae5` | R01-R11 | Initial facade/state-root candidate |
| `2fdbdced3ba09be6bcc0a835d334ac48a2786413` | R12-R16 | First safety correction |
| `19cbe5daa77cd10e1354a9018584d2907827f79f` | R17-R22 | Residual-race correction |
| `8efe3aed33499402b6104d75c108dc2424f859f6` | R23-R24 | Transaction-finalization correction |
| `4db68b1f2bdf6f2629983fc5ed3e9cc760fd9cbd` | R25-R26 | State-write transaction correction |
| `1bc710394a47931a2320f7b6cee0733a2dd991b6` | R27 | Candidate/checkpoint correction |

| ID / severity | Rejected behavior | Resolution in approved candidate |
|---|---|---|
| R01 / P1 | Check-all invoked refresh recovery and changed generated files. | Mode-based writer exclusion and interruption preflight prevent delegation; both writers are skipped and check snapshots remain unchanged. |
| R02 / P2 | Delegated coordinator checks omitted the external state root. | Closed argv/context resolution forwards the validated optional or bound root before the subcommand; complete bound check-all passes. |
| R03 / P1 | Generated state, Markdown and manifest/report claims could be altered without rejection. | All eleven outputs are reconstructed and compared byte-for-byte; generation ID, source/evidence scope and every claim are checked. |
| R04 / P1 | An internally valid replacement ledger could bypass the binding baseline. | Harness and facade enforce baseline count/prefix and exact same-count bytes; valid appended receipts remain readable. |
| R05 / P1 | Unbound initialization permitted multiple external/default stores. | Unbound explicit roots are read-only; initialization and all locked mutations deny without creating state or locks. |
| R06 / P1 | Linked evidence logs and ignored instruction discovery could cross private-input boundaries. | Direct/indirect private or CSV paths are rejected before content access; instruction discovery uses the tracked/nonignored inventory. |
| R07 / P1 | Resolution and relocation recovery could follow symlink aliases. | Roots/components are checked before use; descriptor-relative operations and identity checks preserve unrelated targets under substitution. |
| R08 / P1 | State moved before lock acquisition and resumed with a held destination lock. | The selected source/destination lock spans each transaction, movement, verification and activation; concurrent writers and held locks deny. |
| R09 / P1 | Existence-check plus ordinary rename could replace a raced destination. | Darwin EXCL/SWAP or Linux equivalents use anchored directory descriptors; raced destinations survive and unsupported platforms deny. |
| R10 / P2 | Migration IDs could escape the rollback archive path. | Schema/runtime filename bounds and complete path validation reject traversal, separators, empty and overlength identifiers. |
| R11 / P2 | Origin validation omitted nested/type/constant/hash constraints. | The complete origin instance is validated; revision/tree string types and structural-reference-only provenance remain explicit. |
| R12 / P1 | A stale harness could recreate default state or leave a competing lock after cutover. | Binding/root/lock continuity is rechecked after acquisition and at commit; exclusive speculative ownership controls cleanup. |
| R13 / P1 | Binding activation could discard a descriptor changed after its final comparison. | Atomic exchange validates the displaced descriptor and retains/restores conflict material with a durable recovery transaction. |
| R14 / P1 | A late ancestor substitution could redirect the rename syscall. | Descriptor-relative EXCL/SWAP anchors reviewed directories; state, lock, private-directory and binding probes preserve unrelated content. |
| R15 / P2 | Directory-wide generated exclusions hid additional implementation files. | Only eleven exact outputs are excluded; README and additional implementation enter source scope and invalidate stale views. |
| R16 / P2 | Check-all's unbound test used the real bound repository. | The unbound resolver test uses an independent fixture; actual default and active-bound complete checks pass without writes. |
| R17 / P1 | A changed binding was detected only after a receipt had been appended. | Identity validation follows the final comparison; durable preparation/ready/recovery transactions preserve or restore exact previous bytes. |
| R18 / P1 | Speculative cleanup could claim another actor's zero-byte lock. | O_EXCL establishes ownership; existing/replaced inodes are never removed as the invocation's speculative lock. |
| R19 / P1 | Relocation namespace changes lacked directory durability barriers. | Affected source/destination parents are fsynced in order before later stages; failed completion sync retains/restores pending recovery. |
| R20 / P1 | Pending activation accepted work that later broke recovery. | Any pending activation transaction blocks normal harness/facade access until lock-held helper recovery completes. |
| R21 / P2 | Active-committed recovery accepted a corrupt moving archive. | Regular-file type, exact hash, content and transaction/binding relationships are verified before completion. |
| R22 / P2 | Resume failed after activation had durably completed. | Exact completion/archive/layout/baseline evidence is verified under lock; repeated resume returns already_completed. |
| R23 / P1 | Failed state fsync or rollback removed the only previous-state copy. | Preparation precedes candidate material; failed/interrupted transactions retain controls and both byte sets with explicit owner/runtime-stop recovery. |
| R24 / P1 | State exchange discarded an unvalidated displaced ledger. | Complete displaced bytes and prepared inode must match; a competing valid ledger is restored/preserved and ordinary operations stay blocked. |
| R25 / P1 | Ready publication adopted a substituted candidate's hash/content. | Preparation binds intended raw SHA; candidate-bound control uses the exclusively created inode; exact raw/hash/inode checks precede ready and exchange. |
| R26 / P2 | Preparing recovery skipped a captured corrupt checkpoint. | Identity-bound capture control and exact intended/attempted checkpoint sets are verified on nested recovery; corrupt, missing, duplicate and wrong-type cases deny. |
| R27 / P2 | Normal file/lock type boundaries could hang on FIFO or accept invalid types. | No-follow/nonblocking reads require regular opened descriptors; lock metadata/descriptors are checked; all 39 independent type probes deny promptly. |

Additional author-side discoveries (candidate-before-control, validate-then-unlink cleanup, partial control publication, checkpoint-backed rollback restart and intended-checkpoint hardlink alias) remain in existing author successor evidence. They did not replace independent review; their corrections were inspected and exercised through the final suites and matrix.

## Validation commands and observed results

Commands ran against the approved candidate in the reviewer worktree unless an absolute canonical/source root is shown. Test data and adverse mutations were synthetic. Direct suites used `python3 -B`; registry delegation additionally supplied `PYTHONDONTWRITEBYTECODE=1`. The cache qualification below limits claims about descendants outside the check oracles.

| Check | Exact command | Exit / result |
|---|---|---|
| facade-tests | `python3 -B -m unittest discover -s .agent/tests -p 'test_*.py' -v` | 0; 26 tests PASS |
| workspace-tests | `python3 -B -m unittest discover -s tooling/workspace/tests -p 'test_*.py' -v` | 0; 77 tests PASS |
| coordination-tests | `python3 -B -m unittest discover -s tooling/coordination/tests -p 'test_*.py' -v` | 0; 184 tests PASS |
| sealed-harness-tests | `python3 -B -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -p 'test_*.py' -v` | 0; 39 tests PASS |
| workspace-contract | `python3 -B tooling/workspace/validate_contract.py --check --audit` | 0; 42 concerns, 85 mappings, 35 types, 16 source moves; 86 sealed/88 source files |
| facade-check | `python3 -B .agent/scripts/validate.py --check --state-root /Users/jamesryancooper/Projects/texenda/repo/.texenda` | 0; PASS |
| facade-check-all | `python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/repo/.texenda` | 0; nine nonwriters pass; both refresh writers SKIPPED_WRITER |
| sealed-package | `python3 -B specs/texenda-handoff/10-validation/validate_package.py --checksums` | 0; 14/14 PASS |
| source-package | `python3 -B /Users/jamesryancooper/Projects/texenda/sources/handoff-1.1.0-20260914/10-validation/validate_package.py --checksums` | 0; 14/14 PASS |
| diff-check | `git --no-optional-locks diff --check 680457854984020d0c8616a7f640a63079be9b3c 7a1c37619e342370be0b0b05782727871a74b94f` | 0; no whitespace errors |
| sealed-unchanged | `git --no-optional-locks diff --exit-code 680457854984020d0c8616a7f640a63079be9b3c 7a1c37619e342370be0b0b05782727871a74b94f -- specs/texenda-handoff` | 0; empty diff |
| candidate-clean | `git --no-optional-locks status --porcelain=v1 --untracked-files=all` | 0; empty tracked/untracked status |
| live-state-check | `python3 -B tooling/coordination/harness.py --root /Users/jamesryancooper/Projects/texenda/repo check` | 0; local integrity PASS; status and ready also preserved metadata |

The final facade/contract checks reported 122 JSON files, one TOML file, 19 Python files, 27 dossier paths, three instruction files, 101 facade local links, 254 bound PASS/FAIL evidence checks, 42 concerns, 85 blueprint mappings and 35 artifact types. These counts describe the candidate before these two review artifacts. The workspace audit compared all 86 sealed and 88 preserved-source files.

All eleven generated outputs matched deterministic reconstruction, including every Markdown byte, current-state mirror, manifest/report claim and generation-ID derivation. Source scope: `c4f8c047acfd8de4ead7c806f4130d02d6ef5b90158c88ced83acc109a21bd11`. Generation ID: `9bea818feb1b297b2b8fe02013664b6b3cca80ad97a8c2a9a5d5436ac74a2a7f`. README/additional generated-directory implementation remain source-scoped. Origin v2 truthfully records high-assurance `mapped-existing`, installed Blueprint 1.0.0 structural-reference-only; the dirty 4.3.0 source is not adopted.

The concise root routes to seven scoped `.agent` contracts and existing sealed/ADR owners. There is one owner per concern/epoch; no second task, receipt, routing, roster, decision or evidence authority was introduced. `.agents` capability packages remain deliberately deferred. Dossier classifications/provenance are distinct from permission and current-state authority.

## Independent 75-case hard-exit matrix

A standard-library `python3 -B -` driver loaded the candidate harness, created parent-owned temporary repositories, forked one child per case, injected `os._exit(73)` at the specified boundary, and used `waitpid` to verify/reap that child. External layout used a synthetic active binding and byte-preserving state/lock renames. Initialization started without a ledger. Normal access had to deny while operational controls existed. Explicit `recover-state-write` used `human:owner` and `runtime_stopped=True` under the preserved lock.

Results: default 26/26, external-bound 26/26, initialization 23/23; **75/75 PASS**, zero failed children or remaining blockers. Three previous-ledger capture boundaries do not occur in successful first initialization. Earlier phases restored exact previous bytes/absence; a durably archived outcome or later phase retained the committed ledger. All 75 children were reaped. Nested rollback/checkpoint-backed interruption cases also passed in the coordinator suite.

| Boundary | Target / qualification |
|---|---|
| `state_write_after_control_staging_partial` | preparation target |
| `state_write_after_control_publish_before_fsync` | preparation target |
| `state_write_after_preparation_control` | normal transaction |
| `state_write_before_candidate_file_fsync` | normal transaction |
| `state_write_after_control_staging_partial` | intended-checkpoint target |
| `state_write_after_control_publish_before_fsync` | intended-checkpoint target |
| `state_write_after_control_staging_partial` | candidate-bound target |
| `state_write_after_control_publish_before_fsync` | candidate-bound target |
| `state_write_after_candidate_file_fsync` | normal transaction |
| `state_write_after_candidate_directory_fsync` | normal transaction |
| `state_write_after_transaction_prepared` | normal transaction |
| `before_state_commit` | normal transaction |
| `after_final_state_comparison_before_replacement` | normal transaction |
| `state_write_before_exchange` | normal transaction |
| `state_write_after_exchange_before_fsync` | normal transaction |
| `state_write_after_exchange_fsync` | normal transaction |
| `state_write_after_displaced_validation` | normal transaction |
| `after_state_replacement_before_validation` | normal transaction |
| `state_write_after_commit_cleanup_marker` | normal transaction |
| `state_write_before_candidate_capture` | previous-ledger capture |
| `state_write_after_candidate_capture_before_fsync` | previous-ledger capture |
| `state_write_after_candidate_capture` | previous-ledger capture |
| `state_write_after_commit_candidate_cleanup` | normal transaction |
| `state_write_after_outcome_archive` | durable outcome; forward completion expected |
| `state_write_after_preparation_archive` | completed; forward state expected |
| `state_write_after_commit_archive` | completed; forward state expected |

Independent injections and required suites additionally covered first candidate/control publication and fsync, first directory sync, failed rollback exchange and sync, competing internally valid state, original-candidate correlation, captured-inode substitution, missing/corrupt/ambiguous controls/checkpoints, intended/attempted independent inodes, owner/runtime-stop denial, unsupported primitives, and activation exchange/archive/completion interruptions. Both state byte sets and controls remain whenever rollback cannot be proved. No recovery path reserializes or splices receipts.

## Independent 39-case file-type matrix and lock checks

A bounded `python3 -B -` parent driver created canonical fixtures under `/private/tmp`, launched children with captured output, and imposed a two-second timeout with kill-and-reap fallback. Twelve surfaces were each tested against FIFO, directory and Unix socket: normal state, lock, binding, policy, evidence envelope, evidence log, harness shared reader, facade shared reader, relocation shared reader, and post-preflight substitutions in each of those three shared readers. The three shared readers were additionally tested against `/dev/null` read-only. Result: **39/39 promptly denied**, zero timeouts, all children reaped; no device content was used as evidence.

Metadata-only `status`, `ready`, and CLI `check` with a missing lock passed without creating a lock or changing state. A FIFO inserted at `before_lock_create` was denied as a nonregular opened lock before any `flock` call (observed call count zero), with state unchanged. Symlinks, traversal, device/directory/socket inputs, bound/unbound roots and private direct/indirect evidence references retained their deny behavior.

## No-write scope, cache qualification and active-bound checks

Before/after the final ordinary check and check-all, a parent driver compared 268 scoped review-worktree regular files by SHA-256, size, inode, mtime and ctime; compared Git status including untracked/ignored entries; and compared exact live-state hash and live state/lock metadata. All comparisons were identical. `.git` directory internals and private-input contents were excluded; no atime claim is made. This proves these check invocations did not change the observed scope, not that every earlier direct test invocation created no temporary artifact.

A complete synthetic active-bound layout was created using the reviewed relocation helper and refreshed only in that fixture. Both `python3 -B .agent/scripts/validate.py --check --state-root <synthetic-external-root>` and the same command with `--all` returned zero. The 360-file synthetic project/source/local-state snapshot, excluding `.git` internals and private-input contents, retained hashes, sizes, mtimes, ctimes and inodes. No real generated view or live state was refreshed or relocated.

At evidence-authoring entry, `git status --porcelain=v1 --untracked-files=all --ignored` reported one ignored cache: `specs/texenda-handoff/08-project-harness/__pycache__/harness.cpython-313.pyc`. It is preserved under the authorized two-file write scope. SHA-256 `004fcede6d1ef2e178a3b82ddbf99bd57779e4edb691c7214a976f4f7fdb8071`; size 51154; inode 680767598; mtime_ns 1789425813884155708; ctime_ns 1789425813884252875. Its timestamp falls within the review-test period; direct `-B` does not itself propagate to a descendant Python CLI, so no whole-session cache-absence claim is made. Its origin is not independently attributed. The check/check-all oracle included any existing ignored files and proved no change during those calls. This cache is outside the 86-file sealed manifest scope and is not a tracked package-byte change; later cleanup is separate.

## Package and historical-input preservation

Both variants remain version 1.1.0, with 86 manifest files each, 44 WPs, 125 product criteria, 30 invariants, 35 ADRs and 14 external gates. Exactly eleven baseline differences remain, including later editor wording; semantic reconciliation is deferred. The preserved source has 88 regular files including two original caches. Fingerprints below were checked against the accepted Phase-0 baseline and actual files.

| Fingerprint | Sealed implementation package | Preserved source package |
|---|---|---|
| `manifest.json` SHA-256 | `bcb7488ecf2ac42b4b33e478918e7ce6c35d0bdc04b208ddd9ed66622b468b7f` | `bcb7488ecf2ac42b4b33e478918e7ce6c35d0bdc04b208ddd9ed66622b468b7f` |
| `MANIFEST.md` SHA-256 | `cfc5a88ab37fa86bd35f0dcb946e14d62d5c87860a22a3487fb9031102df8179` | `cfc5a88ab37fa86bd35f0dcb946e14d62d5c87860a22a3487fb9031102df8179` |
| `SHA256SUMS` SHA-256 | `37fffb1a165cfa6b907e7433d617c06e1c64ff09cd282173f7d791cace2ac07e` | `8576bf08ec4f2a4718476eca70e6d1d5cb2b6be1af550bf5c20c692bcbaff715` |
| Sorted path/NUL/hash/newline inventory SHA-256 | `0b672e476b38a99bfbdcd3b9dbfca1baa2f1fcdc7329410986caefa9e5421336` | `c3b25ae42e74324fedd3f4d545fe4105e9a2607c2f777afe049af10e75d9fe98` |
| Canonical sorted `{path,sha256}` array SHA-256 | `83cceb48e29bd3d070856976abe5aa2f5559d5479c5a0d1485d2d12c326de1c8` | `26fa6487334c2782bdff8e98c49963e6720228824f6b91a9a7126e0d6cec2131` |

Inventory fingerprints exclude `__pycache__` components and `.pyc`; canonical JSON uses sorted keys, compact separators and UTF-8. Source caches were separately verified: `08-project-harness/__pycache__/harness.cpython-314.pyc` SHA `df56919db3116d0deade32a26f1c1bba70337c67e9e688878434f494b41e4d5a`, and `08-project-harness/tests/__pycache__/test_harness.cpython-314.pyc` SHA `39d2ea9c358cbbecafbe458d1b8a50e643442e22447a9c0796206259d45064b3`. These differ from the reviewer-worktree cache above.

Historical repository-relative `.texenda/evidence`, `.texenda/context`, and `.texenda/state.v1.a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a.json` remain compatible and present. The v1 checkpoint hash matches its filename. They are historical inputs, not another active state store.

## Live baseline and private-input handling

| Observation | Value |
|---|---|
| Canonical main | `680457854984020d0c8616a7f640a63079be9b3c`; tracked/untracked status empty |
| Canonical repository | `/Users/jamesryancooper/Projects/texenda/repo` |
| Current state root | `/Users/jamesryancooper/Projects/texenda/repo/.texenda`; no live cutover performed |
| State version / SHA-256 | `2.0` / `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235` |
| Receipt count / tip | `13` / `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e` |
| Roster count / canonical SHA-256 | `11` / `a23705178b39e8d0dd194abd4cf6e42fc20be404739d0e28e0ca9b221c80ddcf` |
| Leases / declared budget | `0` / `0.0 USD` |
| Status / ready / check | Passed; state/lock inode/size/mtime/ctime unchanged; ready count 2 |

The real private input was checked only at the exact supplied path `/Users/jamesryancooper/Projects/texenda/repo/.texenda/private-inputs/kit/ohw/2026-09-14/subscribers.csv`: existence true, `git check-ignore -v` exit 0 (the `.texenda/` ignore rule), and `git ls-files --error-unmatch` expected exit 1 (untracked). No directory-content inventory, open, parse, hash, copy or logging of its contents occurred. Private-file content was excluded from every real snapshot; no unobserved content equality is claimed. All private-content adversarial instrumentation used synthetic fixtures.

GitHub, remote branches/settings/workflows, accounts, credentials, external systems, production state and API spending were not touched. No push, publish, send, deploy or network qualification occurred. No current remote-visibility/API observation is invented.

## Limits, stop state and evidence-only handoff

Darwin descriptor-relative EXCL/SWAP primitives were exercised on the actual host. Unsupported rename platforms fail closed. Process hard exits and ordered file/directory fsync were tested; physical power-loss behavior was not. This review does not authenticate the provider's executing model beyond the requested qualified route and source evidence, prove a runtime sandbox, or clear a product/external gate.

At review completion, every child process and command session was stopped/reaped; no child agents or background jobs remained. The parent must observe this reviewer task's final stop before releasing scope or moving live files. Writing these artifacts is a separately authorized evidence step, not a blanket runtime-stop attestation for other actors.

The paired [review envelope](2026-09-14-mapped-agent-facade-review.evidence.json) uses the existing closed local evidence v2 contract, kind `review`, and transition identifier `TRN-WSM-0001`. This is not an admitted WP lifecycle receipt. Every PASS/FAIL row points to this Markdown and its exact SHA-256. Additional metadata and complete historical findings live in this hash-bound document, avoiding unsupported envelope keys.

Only these two review artifacts are to be committed atop the candidate. Their containing commit/tree and file hashes are reported in the subsequent handoff, avoiding a self-referential hash cycle. Generated views are intentionally not refreshed here. Their evidence index becomes stale after this evidence-only addition until the integrator explicitly refreshes and validates a new head. Approval of the original code candidate must not be confused with approval of that new head.
