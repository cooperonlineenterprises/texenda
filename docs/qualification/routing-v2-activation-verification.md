# Routing v2 activation verification

Verified at `2026-09-13T19:51:23Z` for local integrated head `75a7dc180f759570ec8d245b8d606528925a2bc0` and canonical routing-policy digest `61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0`.

The owner explicitly selected a quality-first two-dimensional routing model: T1–T4 capability is separate from reasoning effort, every capability defaults to `max`, listed lower efforts require a fresh bounded routing attestation, and Sol/max is the sole explicit T1 fallback. Official OpenAI model guidance was used as candidate guidance only; actual availability comes from the local subscription probes: <https://developers.openai.com/api/docs/guides/latest-model>.

## Integrated implementation

- Candidate `4ce1be33ea3d9e86e6806d992b4bdb7224ab3014` received independent Astra/max approval with no remaining findings.
- Rejected candidates `61d921aeeb7b386e442dbdf8d1db91f1d6be0a81` and `7ffeb4779bd8560237f4a0682197fd214e699fb6` remain in history with their findings and corrections.
- Local integrated head `75a7dc180f759570ec8d245b8d606528925a2bc0` includes the exact candidate plus its author/reviewer audit envelopes.
- The sealed `specs/texenda-handoff/` tree is unchanged and its 14 checksum-aware package checks pass.
- The project-local coordinator passes 115 tests; the unchanged sealed coordinator passes 39 tests.
- All routing/tooling JSON and TOML artifacts parse, all 11 profiles and 88 WP role routes were checked, and the base-to-integrated diff is clean.
- Adversarial review also passed 40 process races, 104 retained-evidence tamper cases, exact rollback and atomic-replacement faults, cumulative author/reviewer budget accounting, and exact/post-expiry budget denial.

## Live ledger migration

- V1 source SHA-256: `a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a`.
- V1 receipt count/tip: `10` / `93dd403aeb020f44431c590201eb245ef78b395776c7514c6c807f4e4a778155`.
- Byte-exact checkpoint: `.texenda/state.v1.a2a58e20004c86c0081b1427087626e36f931c3804532e8a1caf1c94a49a609a.json`, verified with the same SHA-256.
- V2 receipt count immediately after migration: `11`; all 10 prior receipt objects are an unchanged prefix.
- Every task/history record is unchanged; WP-00 remains completed with fence 1 and no lease.
- The v1 roster was cleared and not promoted. No profile is active yet; installation of the reviewed v2 roster record remains pending.
- API development budget and declared spend remain `$0`.

## Exact-profile evidence

| Profile | Probe SHA-256 |
|---|---|
| `gpt-6-astra-max` | `d5ca2d2136c8ea958069a6cc4af3604b839b6b78dc58250f171b0be03691c021` |
| `gpt-6-astra-high` | `6ab0d7b121630937de88441c1aedf1e46de1da1d0319ac01806bb7435fdf726f` |
| `gpt-5.6-sol-max` | `d53046c0c75c549ab6ce41c9385f6f13cf8d69b9a6dfd3addfff68fa934605ad` |
| `gpt-5.6-sol-high` | `b3517e156c382bc9fb45ed29994a8ff573854ddcd03436fee88ed053810ae300` |
| `gpt-5.6-terra-max` | `2cd4aa563083a29b00b3a0fa9481ef9a19101cc5e126f6268fbb23990139431c` |
| `gpt-5.6-terra-high` | `4bf17a79ae8bcc32bcbb38e49d9ed295e4743808126bd4716d70c65cfd5db267` |
| `gpt-5.6-terra-medium` | `1c81e33c60d7da2e23b1d9f4fc1c8e8647bb26dfce3ff9fcce6dc3d1d19aeda3` |
| `gpt-5.6-luna-max` | `5b8beec0eefc42830da3097f10f817f765034b4e72594f6c2b23bc817cd2a09e` |
| `gpt-5.6-luna-high` | `f47fcc9a55cb7702ec8896919eaacc289bbe0b69e783dc132eaa9657cc1a0322` |
| `gpt-5.6-luna-medium` | `9ca408754af445cfdd40f4753a239b89e026a2ab9d109f013d63692346758160` |
| `gpt-5.6-luna-low` | `469723e6801d3a2c91d29d52ca3ed69c4bcdc6206d7a85cceb12c472b08ab00f` |

Each probe exercised local read/edit/test behavior and preserved INV-02, INV-12, and INV-30. The runtime dispatch accepted the exact requested model/effort overrides, but agents had no independent self-identification channel; their `self_reported_model_id` remains `null`. No probe cleared a product or external gate.

The resulting roster is subscription-only and expires after 29 days. It does not authorize API spend, production data, external services, deployment, or sending.
