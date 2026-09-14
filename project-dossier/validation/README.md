# Validation

The single command registry is [`.agent/validators.json`](../../.agent/validators.json).
Run the read-only facade check after explicit refresh. Run the registered local,
sealed, package, schema/link/owner/evidence, and negative/recovery suites for an
exact candidate. PASS is bounded evidence only; it clears no product or external
gate.

`validate.py --check` must not write tracked, untracked, ignored, cache, lock,
timestamp, or generated state. Only `refresh.py --refresh` may update generated
views.

`validate.py --check --all` resolves shell-free registry argv from a validated
repository/project-home/state-root context. It categorically skips every
`refresh_writer`; state-root options precede coordinator subcommands. Both check
modes reject an interrupted-refresh marker before delegation and deterministically
reconstruct all eleven generated outputs byte-for-byte.

Only those exact eleven paths are excluded from the source fingerprint.
`.agent/generated/README.md` and any additional implementation file under that
directory remain source; adding one makes an unrefreshed or uncommitted
projection stale. Complete synthetic check-all proofs cover both the default
pre-binding layout and an active external binding.
