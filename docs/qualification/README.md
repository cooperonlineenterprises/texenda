# Runtime and routing qualification

This directory contains sanitized local evidence for the Texenda coding runtime. It does not qualify the Texenda application, production services, providers, legal/privacy posture, security readiness, deployment, sending, migration accounts, or any product acceptance criterion.

## Active routing policy

The project-local [quality-first routing decision](../decisions/ADR-0001-quality-first-model-routing.md) and [machine policy](../../tooling/coordination/routing-policy.json) supersede only the sealed handoff's coding-model tier recommendations. Use `tooling/coordination/harness.py`; the package under `specs/texenda-handoff/` remains byte-for-byte unchanged.

The four capability tiers default to max reasoning:

| Tier | Policy default | Policy-listed downshifts (not current availability) |
|---|---|---|
| T1 | `gpt-6-astra-max` | `gpt-6-astra-high` |
| T2 | `gpt-5.6-sol-max` | `gpt-5.6-sol-high` |
| T3 | `gpt-5.6-terra-max` | `gpt-5.6-terra-high`, `gpt-5.6-terra-medium` |
| T4 | `gpt-5.6-luna-max` | `gpt-5.6-luna-high`, `gpt-5.6-luna-medium`, `gpt-5.6-luna-low` |

Sol/max is also the sole explicit T1 fallback. The fallback requires an explicit flag and reason and is never selected automatically. Lower effort requires a current task/role/profile/fence-bound routing record proving bounded, reversible, fully specified work with deterministic verification. No existing whole parent WP has a T4 floor; T4 is reserved for separately fenced mechanical subtasks and future reviewed routes.

The live ledger selects the active exact-profile record; a policy row or dated
file is not availability. The [2026-09-18 record](model-roster-v2.2.evidence.json)
contains only newly demonstrated Astra/max and Terra/max on desktop
26.908.70816 (build 9275), with seven-day validity and earlier invalidation on
relevant runtime changes. Independent review and owner-attested installation
remain separate; inspect live `check`/`status` before use. Sol/max, Luna/max and
all lower efforts were omitted, not silently carried from the older build.
The [v2.1 record](model-roster-v2.1.evidence.json) remains immutable historical
evidence for desktop 26.901.41600 (build 7982), not a current-build qualification.
The [new observation](runtime-surface-observation-2026-09-18.json) separates
requested dispatch from unavailable independent provider identity introspection.
For historical provenance, see the
[runtime observation](runtime-surface-observation-2026-09-13.json) and
[correction verification](runtime-surface-correction-verification-2026-09-13.md).
The [activation receipt](runtime-surface-correction-activation-receipt.md)
records the reviewed local ledger transition.
The live ledger's latest `set-roster` receipt is the operational activation
proof; always run `check` and inspect `status` before assignment.
`probes/` contains the model/effort runs; `analysis/` and `evidence/`
retain author and independent review records. Profiles expire individually on
the timestamps in the roster, or earlier after a relevant model, desktop
client, account, sandbox or policy change. Direct CLI use remains unqualified.

## Historical v1 and original v2 evidence

The original [v1 roster](model-roster.evidence.json), verification record and
WP-00 evidence remain unchanged because the v1 receipt chain references their
exact hashes. The v1 roster was invalidated during migration and cannot qualify
a v2 profile. The original
[v2 roster](model-roster-v2.evidence.json), activation evidence and receipt also
remain unchanged because receipt 12 binds that roster's hash. Its
`client_version: 0.149.0` values are historical attribution evidence, not
current desktop qualification. A byte-exact v1 state checkpoint remains under
the ignored `.texenda/` ledger.

Before routing work, run `python3 tooling/coordination/harness.py --root . check` and inspect `status`. Missing, expired, changed, or unqualified exact profiles fail closed. The API development budget remains zero; subscription usage remains bounded by assignments.
