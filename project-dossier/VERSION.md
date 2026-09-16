# Dossier contract version

Current operational contract version: `1.4.2-mapped-existing`.

This patch closes the stale current-status metadata for the reviewed
[ADR-0007](../docs/decisions/ADR-0007-standalone-workspace-operating-contract.md)
workspace remediation. The [immutable review](../docs/qualification/evidence/2026-09-15-standalone-reference-review.evidence.json)
approves exactly `82da3f644ea82d6bc7531c1711c63b54eb3b9f5b`.
The [completion record](machine-readable/plan.json) separately binds direct Git
and historical generated observations at integrated revision
`087c0d65cf97c8f553b8915dd3cc93dddc46d4c4`: only the review evidence and eleven
declared projections follow the approved candidate. The prior integrated audit
was not separately committed; that conversation is not a source of validation
or inherited approval. Every consequential successor requires exact independent review.

[SUP-0005](SUPERSESSION.json) retains the exact `1.4.1-mapped-existing`
predecessor at `087c0d65cf97c8f553b8915dd3cc93dddc46d4c4`. Prior supersessions,
rejected candidates, the `external_state` epoch, 85 mappings, ten compatibility
dispositions and sole RAIDQ deferral ownership remain unchanged.

Operational conformance covers the governed development workspace. It grants
no task, permission, product readiness, external gate, live-state freshness,
Blueprint/runtime qualification or approval of a future revision. Neither
sealed/source package is versioned by this dossier patch.
