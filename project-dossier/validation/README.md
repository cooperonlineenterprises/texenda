# Validation

The single command registry is [`.agent/validators.json`](../../.agent/validators.json).
Run the read-only facade check after explicit refresh. Run the registered local,
sealed, package, schema/link/owner/evidence, and negative/recovery suites for an
exact candidate. PASS is bounded evidence only; it clears no product or external
gate.

`validate.py --check` must not write tracked, untracked, ignored, cache, lock,
timestamp, or generated state. Only `refresh.py --refresh` may update generated
views.
