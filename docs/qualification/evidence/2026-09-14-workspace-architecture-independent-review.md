# Independent review: mapped Texenda workspace architecture

Reviewed on 2026-09-14. Verdict: APPROVE the exact corrected architecture
candidate below. No open candidate findings remain. This approves the transition
contracts and their bounded implementation plan; it does not attest a completed
relocation, operational facade, external-state cutover, product test or external
gate.

| Binding | Exact value |
|---|---|
| Base | `36b74e9e1ca6353b3d642136fa70b7d2ac950e08` |
| Base tree | `f55477c5be32c6c866c1822f1e464dbba7e42198` |
| Approved candidate | `d3482777c675cc009884b87b3031abe73ee752ac` |
| Approved tree | `8ea58ca9fe1e26463463c582868ea01fff476656` |
| Full binary diff SHA-256 | `04782d33049b7de58439dda8e414adcbc1fac7cc871da8e9e9a64660066e4787` |
| Rejected predecessor | `609ddda6da96ddf2460925cc759db724acd70d59` |
| Predecessor tree | `fe3f4c3268a2fc7a33898fb306a4eed9170a28ca` |
| Predecessor full binary diff SHA-256 | `d0a387a2133c7be0f9df4d71b800a46ec4953674041cd0141b4cbe8de96e1cc4` |

The diff procedure is `git diff --no-ext-diff --no-textconv --full-index --binary
<base> <candidate>`, hashing its exact stdout with SHA-256. The author's two chat
digests (`d29afd...` and `14ea...`) disagree with the actual bytes. They are not
stored in either candidate and were not used as authority. This review records
the independently reproduced digests above.

The reviewer is `/root/review_workspace_architecture`, distinct from author
`/root/workspace_architecture_author` and integrator `/root`. The requested exact
profile is `gpt-6-astra-max`, T1/max, on `codex-desktop-collaboration`, desktop
`26.901.41600 (build 7982)`, subscription billing and API USD0. At
`2026-09-14T15:30:10.294663+00:00`, the live qualification and its hash-bound
checks were independently revalidated; this profile expires
`2026-10-12T21:44:31Z`. The assignment bounds are 3,600 seconds and 90,000 tokens;
provider token metering and independent executing-model introspection are
unavailable. Recorded qualification does not remove those limits.

The review used `project-bootstrap` with the high-assurance profile, including
its dossier, harness, profile and migration references. Repository instructions,
accepted decisions, sealed authority and relevant harness implementations were
read. The complete original candidate, correction diff and added correction
records were inspected; unchanged context was verified by Git and content
hashes. Every file in the resulting eleven-file candidate was fingerprinted.
The machine [review record](2026-09-14-workspace-architecture-review.evidence.json)
contains the exact commands, captured outputs and file hashes.

P2 in the rejected candidate: `operations_recovery` and OPS-0001 pointed to
`06-migration-and-production/`, while the sealed authority register assigns
operations procedures to `04-security-governance-and-operations/runbooks.md`.
The [corrected crosswalk](../../../project-dossier/transition/blueprint-adoption-crosswalk.json)
now points to that owner in all three epochs and in the OPS-0001 mapping.
The validator derives and pins the unique sealed owner. Three new regression
tests verify the owner and reject the prior directory in each epoch and the
artifact mapping. Independent in-memory reproductions rejected all four wrong
mappings. The predecessor remains the direct Git parent; its author report,
validation log and historical output hashes remain unchanged. The
[correction record](2026-09-14-workspace-architecture-correction.json) supplies
new evidence without rewriting its predecessor.

The architecture has these verified boundaries:

- All 85 installed high-assurance planner paths, 35 catalog types and five
  additional triggered families are mapped. Forty-two concerns have one
  declared owner per epoch. The dossier owns new adoption, conformance,
  metadata and RAIDQ concerns; existing product owners remain sealed.
- Routing, WP lifecycle, live tasks, qualification, receipts, decisions and
  evidence retain their existing owners. The facade's task, decision, evidence
  and review directories are indexes. Policy/context cutover removes old
  duplicated prose in the same reviewed candidate; the command registry
  delegates to existing validators.
- The mapped extension is restrictions-only. No second active ledger, roster,
  routing policy, decision store or evidence store is created. No `.agent/`
  facade, origin record or copied product canonical directory exists yet.
- The [move manifest](../../../project-dossier/transition/workspace-move-manifest.json)
  covers all 16 exact source-package entries, reserves absent rename targets,
  preserves the active parent root, and requires serial non-overwriting moves,
  fresh runtime/worktree proof and an all-ref checkpoint. No deletion,
  symlink bridge or external mutation is authorized by the contract.
- Phase 1 retains the whole ignored `.texenda/` with the checkout. Later
  cutover moves active state/locks and private inputs. Receipt-bound historical
  `.texenda/evidence/`, `.texenda/context/` and the named v1 checkpoint stay
  byte-exact at their repository-relative paths.
- The planned explicit state-root binding separates repository evidence lookup
  from live-state location, blocks competing roots and interrupted moves,
  preserves receipt validation and has no implicit initialization. These are
  implementation acceptance requirements, not tested implementation claims.
- Generated views bind an exact source revision/tree, a declared source-scope
  digest and live ledger/evidence hashes. Their containing-commit hash cycle
  is handled explicitly; governance, code, schemas, tests and authoritative
  dossier inputs cannot be excluded from freshness. Only refresh writes
  generated integrity; check remains read-only.
- A complete real mapped maintenance lifecycle, independent reviews of later
  consequential candidates, final review after evidence addition, stopped
  runtimes and exact integrated-main validation remain required.

The selected blueprint is the installed 1.0.0 bundle at
`/Users/jamesryancooper/.codex/skills/project-bootstrap/assets/blueprint-source`,
used as inspected structural reference only, with `adoption_mode: mapped-existing`.
Its planner works. Its source validator and acceptance runner calculate an
original-checkout root from the installed layout; the recorded failures are
preserved and were not rerun through unrelated account files. The closed
origin.v1 schema lacks `adoption_mode`, so no origin file is created before a
reviewed schema successor. The identified newer Octon Mini 4.3.0 source is still
at `5e2d3025aea6b1574ab984e5ebb89b5602a38535`, tree
`3c732979e580c80b020d09c22ce86f5202110518`, with 218 dirty entries and incomplete
qualification. No facts, permissions, decisions or status are imported from it.
Seventeen installed reference hashes and the exact 35-type catalog were
independently checked.

Required checks were rerun from
`/private/tmp/texenda-workspace-architecture-rereview-20260914`, Python 3.13.9.
Python suite commands used `PYTHONDONTWRITEBYTECODE=1` as well as `-B`, including
child interpreters.

| Check | Result |
|---|---|
| `tooling/workspace/validate_contract.py --check --audit` | PASS: 42 concerns, 85 paths, 35 types, 16 moves |
| Workspace unit/mutation suite | 30 PASS |
| Local coordination suite | 132 PASS |
| Sealed harness suite | 39 PASS |
| Sealed package validator with checksums | 14 PASS |
| Source package validator with checksums | 14 PASS |
| Candidate parsing before review records | 83 JSON, 1 TOML, 10 Python PASS |
| New candidate Markdown links | 7 PASS |
| Original Git-bound input hashes | 11 PASS |
| Historical author hashes | 8 PASS at predecessor revision |
| Correction output/source/history hashes | 4 / 2 / 2 PASS |
| Package bytes | 86 sealed files unchanged; 88 source files preserved |
| `git diff --check`; sealed diff against base | PASS |
| Baseline checkpoints | Three SHA-256 values match; bundle verifies complete history and 29 refs |
| Static read-only audit snapshot | All 220 review-tree and 106 source-tree paths unchanged, including atime/mtime/ctime |

Both handoff packages still identify as 1.1.0, share the recorded manifest hash
`bcb7488ecf2ac42b4b33e478918e7ce6c35d0bdc04b208ddd9ed66622b468b7f`, and have
exactly the eleven recorded differing paths. Sealed checksum-set SHA-256 is
`37fffb1a165cfa6b907e7433d617c06e1c64ff09cd282173f7d791cace2ac07e`; source
checksum-set SHA-256 is
`8576bf08ec4f2a4718476eca70e6d1d5cb2b6be1af550bf5c20c692bcbaff715`.
The sealed package remains implementation authority; the source variant remains
unpromoted provenance. The two preexisting source caches are preserved. Editor
wording reconciliation is the separately recorded deferred amendment task.

No move occurred. Canonical main remains `36b74e9e1ca6353b3d642136fa70b7d2ac950e08`
at `/Users/jamesryancooper/Projects/texenda-app`, clean, with the expected remote
`https://github.com/cooperonlineenterprises/texenda.git`. The project home is not
Git, its 16 original entries remain in place, and `texenda/repo` is absent.
All inspected locations are on the same filesystem with approximately 321 GiB
available. Four linked worktrees are retained: main, author, rejected review
and this corrected review. They must be reconciled after runtime stop.

Live state was read without calling a lock or writer. Its SHA-256 remains
`b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`, version 2.0,
with 13 receipts and tip
`f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e`.
Roster digest is
`a23705178b39e8d0dd194abd4cf6e42fc20be404739d0e28e0ca9b221c80ddcf`;
all eleven profiles revalidated. There are zero leases, budget, declared API
allocations and cleared gates. Historical evidence, v1 checkpoint and receipt
prefix verified; state bytes and state/lock metadata were unchanged. A read-only
`lsof` query returned no holders at its observation time, which does not replace
fresh runtime-stop proof before relocation.

Private handling used only exact CSV existence, `git check-ignore`, `git
ls-files` and Git status. The input remains at the owner-specified ignored,
untracked path under the old checkout. Its contents were never opened, parsed,
hashed, copied or logged, and it was excluded from snapshot/content-hash scopes.
The coordination archive's member names were checked for private-input/CSV
exclusion before verifying its already scoped archive hash.

This reviewer made no network requests, GitHub/app changes, moves, live-state
writes, pushes, deployments, publications, production changes or API spending.
GitHub visibility/settings and saved project paths remain attributed to the
coordinator's baseline observation; fresh read-only confirmations are required
at relocation and final completion. Product gates, later facade/state-root
negative tests, real mapped lifecycle and final integrated-head checks are
NOT RUN in this architecture review because their implementation has not occurred.

The author was independently observed completed through the collaboration
runtime. This reviewer has no child runtimes or background commands and ends
after writing and checking the two review artifacts. The parent must observe
reviewer completion before releasing its scope. These two uncommitted records
are the only review additions; the candidate's tracked bytes remain unchanged.
The earlier rejected review worktree and its one ignored test bytecode cache
remain retained, outside this clean corrected review worktree.

Next: preserve these records and the exact candidate, obtain the required final
read-only review after review evidence is added, then let the distinct T1
integrator proceed only with accepted integration and freshly verified move
preconditions. This record neither self-attests its containing commit nor
approves an unreviewed semantic integration change.
