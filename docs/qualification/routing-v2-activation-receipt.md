# Routing v2 activation receipt

Installed at `2026-09-13T20:04:57Z` from committed roster evidence SHA-256 `dbfd99b98edc134c1e202c0b48145141f967718194b67012f75a3868bf4ef6a1`.

- Ledger version: `2.0`.
- Canonical routing-policy digest: `61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0`.
- Post-installation state SHA-256: `43cf040755cc587373fcddd9c7ff7727d41ccecbc260e9043869c3797a1a82fb`.
- Receipt count/tip: `12` / `a60e550b634c28cdfdab677e44481bc5fb5803d2056c10f6787df35fefe05092`.
- Exact qualified profiles: `11`; every profile in the policy is available.
- Available max defaults: T1 `gpt-6-astra-max`, T2 `gpt-5.6-sol-max`, T3 `gpt-5.6-terra-max`, T4 `gpt-5.6-luna-max`.
- Explicit T1 fallback: `gpt-5.6-sol-max`; no automatic fallback.
- WP-00 remains completed at fence 1 with no lease.
- API development budget / declared spend / remaining API budget: `$0` / `$0` / `$0`.
- Qualification expiry: `2026-10-12T19:51:23Z`, with earlier requalification after a relevant runtime, model, client, account, sandbox, or policy change.

The v1 checkpoint SHA-256 remains `a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a`. Its 10 receipts and all task/history records are the unchanged prefix/source of the v2 ledger.

`python3 tooling/coordination/harness.py --root . check` passed after roster installation. This receipt records local coordination state only; it does not authorize API spending, production data or credentials, external services, deployment, sending, or any Texenda product/external gate.
