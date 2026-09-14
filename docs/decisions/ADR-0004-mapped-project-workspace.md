# ADR-0004: Mapped Texenda project workspace

Status: AUTHORITATIVE DECISION — the owner explicitly selected and authorized
this structural migration on 2026-09-14. Implementation remains a candidate
until independent review, serial integration, relocation evidence and final
verification establish completion. This record accepts no product amendment,
editor reconciliation, external effect or external gate.

Texenda's project home is `/Users/jamesryancooper/Projects/texenda`. It is not a
Git repository. Its canonical checkout and sole integration worktree is
`repo/`; temporary linked worktrees belong in `worktrees/`. `local/` holds
active coordination state, private inputs, raw logs, caches and temporary
artifacts. `sources/` holds unpromoted imported package variants. `archive/`
holds retained local checkpoints and superseded local artifacts. A parent
`WORKSPACE.md` is navigation only and routes to `repo/AGENTS.md`.

Keep instructions, stable `.agent/` governance, justified project-local
`.agents/` capability definitions, the dossier, sealed specifications,
accepted decisions, code/configuration and sanitized immutable evidence in
Git. Keep live ledger/locks/leases/process records, private inputs, secret
values, raw exports/logs, caches, large temporary artifacts and temporary
worktrees outside the Git root. This authorizes no private-input content
inspection. Existing ignore rules remain; a local state-location descriptor
is ignored configuration, not a second ledger.

Adopt the high-assurance profile through `mapped-existing` reconciliation.
Concurrent agents, sensitive inputs, external-effect boundaries, durable
recovery and audit require these controls. Literal absent blueprint paths are
not proof of missing functionality. The [crosswalk](../../project-dossier/transition/blueprint-adoption-crosswalk.json)
maps all 85 planner paths, all 35 catalog artifact types and five additional
triggered artifact families before the facade is built. Existing decisions,
qualification evidence, routing, task state and receipts keep one owner.

The inspected installed Project Blueprint is 1.0.0. Its read-only adoption
planner works, but its source validator and acceptance runner assume another
source layout. The dirty Octon Mini 4.3.0 candidate has only partial
qualification. Therefore 1.0.0 supplies inspected structure and validation
patterns only; neither source supplies project facts, permissions, accepted
decisions, evidence, status or readiness. The installed closed origin.v1
schema cannot express `adoption_mode: mapped-existing`. Do not create
`.project-blueprint-origin.json` until an exact reviewed schema successor
truthfully supports this mode and the structural-reference limitation. No
stock generator runs against this established repository.

The implementation's `specs/texenda-handoff/` remains its current sealed
authority. Move the existing non-Git package intact to
`sources/handoff-1.1.0-20260914/`. Both identify as 1.1.0 and pass 14 checks,
but eleven files differ. The later source variant's `@react-email/editor`
refinements are a provenance/transition finding, not an amendment. Preserve
both variants, their manifest/checksum sets and the source's two preexisting
cache files. A later project-local amendment may assess reconciliation;
structural migration neither selects nor merges their semantics.

Ownership transfers in three explicit epochs. Existing root instructions
initially own agent permission classes and precedence/trust. One reviewed
facade candidate activates `.agent/policy.json` and `.agent/context.json`
while replacing their duplicated root/guide prose with routing in that same
candidate. `.agent/validators.json` then becomes the single command registry;
older command instructions route there. The generic schema/lifecycle must
not replace product schemas, IDs, WP transitions or receipts. Register
`tooling/coordination/` as a restrictions-only extension by exact paths and
hashes; tools reference fresh qualification without copying the live roster.

`docs/decisions/` remains the durable decision owner and
`docs/qualification/evidence/` remains the evidence/review owner.
`.agent/tasks/`, `.agent/decisions/`, `.agent/evidence/` and `.agent/reviews/`
initially contain ownership indexes only. The existing external ledger owns
active tasks and receipts. New dossier authority is limited to dossier
interpretation/metadata, conformance findings, adoption transition/plan,
adoption provenance and consolidated RAIDQ. Canonical target material stays
with the sealed owners and accepted local amendments. Every dossier path has
one information role; documentation cannot grant permission.

Generated current-state, handoff, source maps and integrity are projections.
They bind exact source Git revisions/trees, a declared source-scope digest and
exact external-ledger/evidence hashes. `check` is read-only and only explicit
`refresh` writes derived integrity. A tracked projection cannot contain its
own containing Git commit without a hash cycle: the source revision is exact,
source-scope equality determines freshness, and the final read-only check
reports the current full HEAD/tree separately. Governance, implementation,
schemas, tests and authoritative dossier inputs cannot be freshness exclusions.
Any allowed generated/evidence-only exclusion is named and independently
validated. This is not permission to call a stale projection current.

Relocation and live-state cutover are separate reviewed operations. Phase 1
moves the checkout with its whole ignored `.texenda/` intact. Phase 4 first
adds independently reviewed, backward-compatible explicit `--state-root`
support. Then the T1 implementation lead moves active `state.json` and locks
to `local/agent-state/texenda/`, and moves the private-input directory to
`local/private-inputs/`, using verified non-overwriting renames. Existing
`.texenda/evidence/**`, `.texenda/context/**` and the named v1 checkpoint remain
byte-exact ignored historical compatibility inputs at their old relative
paths: current receipts still reference them. They contain no active
`state.json` after cutover. This preserves receipt/state bytes without
copying an active ledger or rewriting its history.

An ignored root `.texenda-location.json` descriptor binds the exact repository
and external state root. Its `moving` status survives interrupted moves and
fails closed; only verified serial recovery can mark it `active`. Once a
binding exists, the harness requires explicit `--state-root`, rejects a
competing default or external store, and refuses default initialization.
The descriptor contains location/migration metadata only. It cannot qualify
agents, authorize effects or supersede the receipt chain.

Use the [move manifest](../../project-dossier/transition/workspace-move-manifest.json)
and [operator procedure](../../project-dossier/transition/README.md). Require a
different Astra/max reviewer for every consequential exact candidate and
the final integrated result, including a final read-only review after review
evidence is added. The author, reviewer and integrator are distinct actors.
No more than two disjoint writers may run concurrently. All affected
runtimes must be observed stopped before release or relocation; a lease's
absence/expiry alone is insufficient. Preserve branches, review commits,
bundles and evidence. Rollback uses verified reverse moves, never deletion,
overwriting, history rewriting or a symlink bridge.

Completion requires the mapped facade and dossier, one demonstrated real
mapped task lifecycle, exact integrated-main checks, unchanged sealed/source
bytes, external state/private-input placement, stopped reviewers and clean
main. Local tests pass no product or external gate. GitHub stays private;
pushes, hosted workflows, settings/secrets/budget changes, spending,
deployment, publication and production activation remain outside this scope.
