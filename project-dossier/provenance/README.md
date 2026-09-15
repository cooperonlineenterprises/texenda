# Adoption provenance

[`sources.json`](sources.json) identifies the selected structural reference,
the separate clean committed and dirty uncommitted blueprint observations,
both preserved handoff variants, dated editor sources, and the debug archive's
forward baseline. Provenance does not transfer permissions, project facts,
accepted decisions, evidence authority, status or readiness.

Installed Project Blueprint 1.0.0 remains selected as structural reference only.
Clean revision `5e2d3025aea6b1574ab984e5ebb89b5602a38535` has committed
VERSION `4.2.0`; source contracts/acceptance pass, but its full validator fails
the expired source-activation fixture. The dirty checkout's working `4.3.0`
and 218 entries are uncommitted and are not attributed to that clean commit.
The upgrade plan is blocked for a reviewed seed; no upgrade occurred.

The two 1.1.0 handoff packages retain all eleven byte differences.
[ADR-0005](../../docs/decisions/ADR-0005-react-email-editor-reversible-default.md)
resolves only the named editor wording locally. Exact version and VAL-03
qualification remain unverified; the source variant is not promoted or merged.

The five debug files have a verified current forward baseline. No pre-move
manifest exists, so historical equality cannot be reconstructed. The archive's
debug/bytecode payloads do not become project source, approval or readiness.
