# Adoption provenance

[`sources.json`](sources.json) identifies the selected structural reference,
the separate clean committed and dirty uncommitted blueprint observations,
both preserved handoff variants, dated editor sources, and the two archive
forward baselines. Provenance does not transfer permissions, project facts,
accepted decisions, evidence authority, status or readiness.

Installed Project Blueprint 1.0.0 remains selected as structural reference only.
Clean revision `5e2d3025aea6b1574ab984e5ebb89b5602a38535` has committed
VERSION `4.2.0`; source contracts/acceptance pass, but its full validator fails
the expired source-activation fixture. The dirty checkout's working `4.3.0`
and 218 entries are uncommitted and are not attributed to that clean commit.
The upgrade plan is blocked for an authentic reviewed seed; no upgrade occurred.
The exact source owner, blocker, retry trigger and requalification commands are
recorded once in [RAIDQ-0005](../machine-readable/raidq.json). The local
[planner interpreter](../../tooling/workspace/README.md) validates the v3 view
without fixing or qualifying the upstream source.

The two 1.1.0 handoff packages retain all eleven byte differences.
[ADR-0005](../../docs/decisions/ADR-0005-react-email-editor-reversible-default.md)
resolves only the named editor wording locally. Exact version and VAL-03
qualification remain unverified; the source variant is not promoted or merged.

The five debug files have a verified current forward baseline. No pre-move
manifest exists, so historical equality cannot be reconstructed. The archive's
debug/bytecode payloads do not become project source, approval or readiness.

SRC-0008 records the wider archive's dated forward baseline: 5,626 files verified
on 2026-09-15, manifest SHA-256
`b682602668d10e96e9c50fbf317d5e3eee4124f1db613e5c49bd86b281656fde`.
Its exact verification route is in the source record. The baseline does not
reconstruct missing historical hashes or promote raw logs, bytecode or Git
objects into project authority. Future archive additions need a new baseline.
