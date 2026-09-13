# Runtime and routing qualification

This directory contains sanitized local evidence for the Texenda coding runtime. It does not qualify the Texenda application, production services, providers, legal/privacy posture, security readiness, deployment, sending, migration accounts, or any product acceptance criterion.

## Active routing policy

The project-local [quality-first routing decision](../decisions/ADR-0001-quality-first-model-routing.md) and [machine policy](../../tooling/coordination/routing-policy.json) supersede only the sealed handoff's coding-model tier recommendations. Use `tooling/coordination/harness.py`; the package under `specs/texenda-handoff/` remains byte-for-byte unchanged.

The four capability tiers default to max reasoning:

| Tier | Default | Qualified downshifts |
|---|---|---|
| T1 | `gpt-6-astra-max` | `gpt-6-astra-high` |
| T2 | `gpt-5.6-sol-max` | `gpt-5.6-sol-high` |
| T3 | `gpt-5.6-terra-max` | `gpt-5.6-terra-high`, `gpt-5.6-terra-medium` |
| T4 | `gpt-5.6-luna-max` | `gpt-5.6-luna-high`, `gpt-5.6-luna-medium`, `gpt-5.6-luna-low` |

Sol/max is also the sole explicit T1 fallback. The fallback requires an explicit flag and reason and is never selected automatically. Lower effort requires a current task/role/profile/fence-bound routing record proving bounded, reversible, fully specified work with deterministic verification. No existing whole parent WP has a T4 floor; T4 is reserved for separately fenced mechanical subtasks and future reviewed routes.

Use [model-roster-v2.evidence.json](model-roster-v2.evidence.json) for the current exact-profile roster, [routing-v2-activation-verification.md](routing-v2-activation-verification.md) for the independently reviewed pre-installation snapshot, and [routing-v2-activation-receipt.md](routing-v2-activation-receipt.md) for the installed live-ledger state. `probes/` contains the model/effort runs; `analysis/` and `evidence/` retain author and independent review records. Profiles expire on `2026-10-12T19:51:23Z`, or earlier after a relevant model, client, account, sandbox, or policy change.

## Historical v1 evidence

The original [v1 roster](model-roster.evidence.json), verification record, and WP-00 evidence are retained unchanged because the v1 receipt chain references their exact hashes. The v1 roster was invalidated during migration and cannot qualify a v2 profile. A byte-exact v1 state checkpoint is retained under the ignored `.texenda/` ledger.

Before routing work, run `python3 tooling/coordination/harness.py --root . check` and inspect `status`. Missing, expired, changed, or unqualified exact profiles fail closed. The API development budget remains zero; subscription usage remains bounded by assignments.
