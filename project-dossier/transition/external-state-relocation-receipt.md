# External-state relocation receipt

Immutable sanitized observation and navigation for `state-root-20260914`.
This is evidence, not permission, a live ledger, independent approval, or a
product/external readiness result. Current facts require fresh direct checks.
Observed at 2026-09-14 23:57:06 UTC against approved canonical main
`01247b6ecc2368610d03d8a82b7ac911d4ad1622`, tree
`394741c97268edc81ad2587ba47156ac6a55a8f3`.

## Physical cutover

The T1 serial executor ran the independently reviewed helper's `prepare`,
`apply`, and `verify` commands with exit 0. The helper performed non-overwriting
renames, held the existing lock, activated the descriptor, and retained its
moving archive and completion transaction. No recovery or rollback was needed.

- Repository: `/Users/jamesryancooper/Projects/texenda/repo`.
- External live state: `/Users/jamesryancooper/Projects/texenda/local/agent-state/texenda`.
- Binding: `/Users/jamesryancooper/Projects/texenda/repo/.texenda-location.json`;
  regular, ignored, untracked, and `active`.
- State SHA-256 before/after:
  `b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235`.
- Receipt count: 13, every prefix hash preserved; tip:
  `f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e`.
- Roster: 11; leases: 0; budget: 0; gates: empty. No receipt was appended.
- State inode `670498844` and lock inode `670332379` were preserved on
  device `16777232`, with unchanged modes and modification times.
- Old `.texenda/state.json`, `.texenda/state.lock`, and
  `.texenda/private-inputs` are absent. State and lock are regular,
  symlink-free files at the external root; no second active ledger remains.
- Historical `.texenda/evidence/`, `.texenda/context/`, and
  `.texenda/state.v1.a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a.json`
  retain their exact hashes at the canonical repository-relative paths.

The private directory moved as a whole from
`/Users/jamesryancooper/Projects/texenda/repo/.texenda/private-inputs` to
`/Users/jamesryancooper/Projects/texenda/local/private-inputs`.
The exact CSV `kit/ohw/2026-09-14/subscribers.csv` exists at the new location
outside Git and is absent at the old location. Its old ignore/tracking checks
and new outside-Git tracking check were confirmed. Content was never opened,
parsed, listed, hashed, copied, or logged; no size check or private-directory
inventory was performed. No private-content equality claim is made.

## Local artifact bindings

These absolute local paths are diagnostic locators, not portable evidence links.
The tracked [observation log](../../docs/qualification/evidence/2026-09-14-external-state-relocation-validation.log)
and [evidence record](../../docs/qualification/evidence/2026-09-14-external-state-relocation.evidence.json)
bind the sanitized observations and exact procedures.

| Local artifact | SHA-256 |
|---|---|
| `local/logs/workspace-relocation/phase-4-state-relocation-journal.json` | `08c1254c9642a66de202b4909047887e83345a96ccb49ad65a2941204b5be8bf` |
| `repo/.texenda-location.json` | `a92b6137856b7f9c2b3f13f69f4e6dc92ed4da1be82eec1ddf21188ebdde0365` |
| `local/logs/workspace-relocation/state-root-20260914.activated-moving.json` | `11438325ffa2203718b10dd3cc879ed16b95704d3921a9ef83c4cc7a20854950` |
| `local/logs/workspace-relocation/state-root-20260914.activation-complete.207c592fdadc82c9.json` | `74e25a1bff59f9cde722157e14826a90c280704bdd76e5f77ddb4cfe75e760ea` |

All local artifact names above are relative to
`/Users/jamesryancooper/Projects/texenda`. The journal is non-authoritative.
Bound Harness and both 14-check package validators passed after relocation.
The canonical facade check then exited 2 with
`generated state-root observation is stale`. A separate tracked candidate
refreshes the eleven views with explicit external `--state-root`; its author
validation is indexed under the existing qualification evidence owner.

## Read-only mapped lifecycle replay

The author used the existing coordinator's stable read, receipt checks,
`_validate_retained_evidence`, and `recheck(..., require_pass=True)` against
the canonical repository and bound external root. No lifecycle mutator ran.
The replay validates the actual September 13 `WP-00` completion and maps
its retained phases; it does not manufacture a new WP run or new ledger.

| Receipt sequence | Retained operation / phase | Exact receipt hash |
|---|---|---|
| 1 | planned via init | `a50f2e78119801bf484a55fa202b75fa61429948b1aea100437cae11d451e30f` |
| 2 | admit | `f20b9a18bfb06899eb33fd33316e666c635c50233c964416ccc8d522074c3479` |
| 4 | assign | `c5f8e6e0c69b3097b5f3eec7e08769b4bf9d8a0a6a28072db9adbdbd313b2803` |
| 5 | start | `dc0d2166f55822d4098603f32355b175a0d5a91caf1bc0bc4d6dd51d832d18e9` |
| 7 | submit | `c0b30bd9764aec6bdf924b28ddada7ea23de8425eb344211e2b1df3c9730206b` |
| 8 | approve-review | `7158517d0578da4129b466a79e9fb0d2745fde8b8f7031b69e307fdf183b629b` |
| 9 | record-integration | `a29aedfcc97546dfa4610d55744a6601e5e0184e25faee2c943127190afb3c59` |
| 10 | complete | `93dd403aeb020f44431c590201eb245ef78b395776c7514c6c807f4e4a778155` |

The sealed `Harness.init` defines tasks as `planned`, so receipt 1 supplies
the planned baseline; no distinct `planned` event is invented. Intervening
roster receipts and the later routing migration remain intact.

Candidate `c95d01162fb6fc7fe0a669cf213bdd73813eb7a8` was integrated as
`12e19b167d7fd59722dc2a3194ce591f499de0e7`; both are ancestors of the
approved cutover main. Author `agent:wp00-terra`, reviewer
`agent:wp00-review-terra`, and integrator `astra` remain distinct historical
actors. The retained task is completed at fence 1 with no lease.

| Retained evidence owner | SHA-256 | Required checks revalidated |
|---|---|---|
| `docs/qualification/evidence/wp00-submission.evidence.json` | `d6f611d2be064c822fe5c4c9c8c507ea01a0c83d117dfa554864a3aab642906f` | 8 |
| `docs/qualification/evidence/wp00-review.evidence.json` | `371d47a3b2b47df6b5f2cf49bd73f8c8b849ff09a8bcb47586da8a77fbed8caf` | 11 |
| `.texenda/evidence/wp00-integration.evidence.json` | `ba2c632509b41aae33f7efb02e2d07cff5d39882ec876b0bd9d860f02d42042e` | 5 |

Every linked check hash was revalidated through the existing coordinator.
The ignored integration evidence resolves only under canonical `repo/`;
it was not copied into this worktree. This replay preserves the historical
qualification limitations and does not requalify those old model profiles.
It establishes mapped access to pre-existing real lifecycle evidence, not
new post-cutover execution or independent acceptance of this candidate.

## Remaining boundaries

The facade code is integrated and the physical move is verified. This
evidence/projection candidate still needs independent Astra/max review and
separate integration. The final integrated-head audit remains `NOT_RUN`.
No live state, policy, code, sealed/source package, external gate, account,
GitHub setting, remote, or external system was changed by this evidence task.
Installed Project Blueprint 1.0.0 remains structural-reference-only under the
existing high-assurance `mapped-existing` adoption; no stock generation or
newer blueprint adoption occurred.
