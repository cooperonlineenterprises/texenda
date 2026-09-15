# Texenda transition status

The mapped-existing workspace transition is complete through the
`external_state` epoch. This page is current navigation only; documentation is
not permission, live state, product readiness, or external-gate evidence.

Ordinary work starts at the [repository entry point](../../.agent/START_HERE.md),
uses the [single validation registry](../../.agent/validators.json), and reads
live work through the [coordinator](../../tooling/coordination/README.md). The
[adoption crosswalk](blueprint-adoption-crosswalk.json) records the active
single-owner map.

The completed transition is bound by these retained records:

- [ADR-0004](../../docs/decisions/ADR-0004-mapped-project-workspace.md) defines
  the mapped workspace and preservation boundaries.
- [ADR-0006](../../docs/decisions/ADR-0006-clean-ordinary-operating-contract.md)
  defines the clean ordinary entry contract without changing historical ADR bytes.
- [Relocation receipt](workspace-relocation-receipt.md) and
  [external-state receipt](external-state-relocation-receipt.md) record the
  physical moves.
- [Integrated-main audit](../../docs/qualification/evidence/2026-09-15-workspace-adoption-integrated-main-audit.evidence.json)
  approved the exact external-state baseline at
  `14682d798faed7cd398d21be3cf8076b84d5b0fe`, tree
  `09d8475a6fc746640edef52efa7c10b340a9299e`.
- [Closeout review](../../docs/qualification/evidence/2026-09-15-workspace-adoption-closeout-review.evidence.json)
  approved the bounded status correction at
  `1a088a40119859e3b97d275f7d367cb14d77bace`.

The original detailed procedure is retained byte-for-byte in
[history](../history/2026-09-15-workspace-transition-completed.md), SHA-256
`1f5b0b1aa816f6bcd34f591a0b5f9f5b4e9d6e8bf35474ca77367418fb930919`.
Read it only for migration provenance or recovery maintenance. Current ledger
recovery commands remain in the coordinator guide.

Blueprint 4.2.0 remains unqualified because its complete validator failed, and
no reviewed upgrade seed exists. ADR-0005 resolves only the package editor
wording as a reversible local default; WP-10 and VAL-03 remain gated. Neither
condition reopens the completed workspace epoch.
