# Desktop runtime qualification correction verification

Date: 2026-09-13. Base:
`0a72aba450c76e318b02f22c49133b406da7d4ef`. Candidate branch:
`audit/runtime-surface-correction`.

## Outcome and authority

The replacement [v2.1 roster](model-roster-v2.1.evidence.json) binds all eleven
allowed model/effort profiles to fresh, bounded probes through
`codex-desktop-collaboration` and records the observed Codex desktop client as
`26.901.41600 (build 7982)`. The separately installed `codex-cli 0.149.0`
remains unqualified, including for Astra; desktop evidence does not transfer to
that execution route.

This corrects attribution evidence only. It does not change ADR-0001, the
machine routing policy, profile/tier membership, defaults, downshift
conditions, the explicit Sol/max fallback, product semantics, any work-package
route or any external gate. Historical roster, probe, review, receipt and
migration files remain unchanged. The sealed handoff remains byte-identical.

Before this candidate, the live harness was version 2.0 at receipt 12
(`set-roster`, head
`a60e550b634c28cdfdab677e44481bc5fb5803d2056c10f6787df35fefe05092`),
with eleven profiles, zero active leases, zero API budget and declared spend,
WP-00 completed and all other work packages planned. The v1-to-v2 migration
boundary and checkpoint were intact; no outstanding migration was found.

## Evidence

The [runtime observation](runtime-surface-observation-2026-09-13.json), SHA-256
`35995674a989b1b77233eafdc80ed092d0a8f8622b88990e8f7b3f8336978091`,
was made before the probes. It separates desktop bundle metadata from the
direct CLI and records a transient usage snapshot only as admission evidence,
not policy or a future allowance.

Only two probe writers ran concurrently. Every probe read the governing
invariants, created one scoped report, exercised local read/edit/test behavior,
ran exactly the ten then-current instruction-contract tests and all fourteen
sealed package checksum checks, and stopped before its result was integrated.
No probe used network access, API billing, paid credits, credentials,
production data, deployment, sending, provisioning or another external effect.

| Exact profile | Observed UTC | Report SHA-256 |
|---|---|---|
| `gpt-6-astra-max` | 2026-09-13T21:44:31Z | `e62f78f3930ffd840c0d5d596a910a87187fe26bdad314b925711a0d39ab8df0` |
| `gpt-6-astra-high` | 2026-09-13T21:37:21Z | `39667e91d35f6f538338047ecac039a9b282bc41b842cb7789fb8b863ac19e55` |
| `gpt-5.6-sol-max` | 2026-09-13T21:45:13Z | `bade3a896b777d08d134b596edef0c95ee80fa59df81e7c95a3ec3985346c429` |
| `gpt-5.6-sol-high` | 2026-09-13T21:37:53Z | `bfeb7d4639e2af5fd1d686a599e8c5ae4165b645bfd84bbcc90384c7ab62bc70` |
| `gpt-5.6-terra-max` | 2026-09-13T21:51:56Z | `0e8e8d8b5e1027b18fde140f7e207c7bab7cb0daea79fae714dd55a5cbb48f66` |
| `gpt-5.6-terra-high` | 2026-09-13T21:51:17Z | `763d6ca28031640217699b00157d45c636b4abe7829cfd7e980b7aee287dbf6a` |
| `gpt-5.6-terra-medium` | 2026-09-13T21:58:11Z | `5ce0c586e5506c78643b86850620804fe534c6017690f5b4ab4718c30ce3e61d` |
| `gpt-5.6-luna-max` | 2026-09-13T21:59:22Z | `73e6370836289af4babb18c0f0ffffb8b2b853a5e6ffabadec31bcca691dbd44` |
| `gpt-5.6-luna-high` | 2026-09-13T22:04:30Z | `a4b4b39af3e27ce36d8e7b368d6e5fa7508a9088d6409ce42717e7fede54a5db` |
| `gpt-5.6-luna-medium` | 2026-09-13T22:03:56Z | `f4bbaf3d7ef77cb946a44b9fdb69591eac01f9ef8c5ed0bac6d94352c47f78be` |
| `gpt-5.6-luna-low` | 2026-09-13T22:07:26Z | `d223cfcda3e8232fd0610fc8d0c11f89f7d7c91d9c3eeca92bd48a2cd4cf0975` |

The Luna/low agent initially labeled its report profile
`gpt-5.6-luna-low-desktop`. After the agent stopped, the parent corrected that
field to the policy's exact `gpt-5.6-luna-low` identifier and aligned the
report expiry before committing it. The model, effort, runtime observation and
test results were not changed. This correction is part of the candidate and
must be independently reviewed.

The v2.1 roster SHA-256 at author verification was
`8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0`.
The historical v2 roster remains
`dbfd99b98edc134c1e202c0b48145141f967718194b67012f75a3868bf4ef6a1`.

## Verification

The following checks passed on the correction candidate:

- `env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tooling/coordination/tests -v`: 131 tests.
- `env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s specs/texenda-handoff/08-project-harness/tests -v`: 39 unchanged sealed tests.
- `env PYTHONDONTWRITEBYTECODE=1 python3 specs/texenda-handoff/10-validation/validate_package.py --checksums`: 14 checks, zero errors or warnings.
- Direct read-only harness validation of the v2.1 envelope: 11 exact profiles and 12 required PASS checks.
- Eight targeted negative/contract tests for desktop-versus-CLI attribution, roster mismatch and tamper, fallback, usage-driven downshift, budget tamper, live/expired lease migration and untrusted NOT RUN evidence: PASS.
- All 76 JSON files, all 3 TOML/config examples and all 8 Python files parsed.
- `git diff --check` for the full candidate and working changes: PASS.
- `git diff --exit-code 0a72aba450c76e318b02f22c49133b406da7d4ef -- specs/texenda-handoff`: PASS.

The new regression contract derives the expected desktop client string from the
runtime observation and checks every exact roster row and evidence-path mapping.
It also asserts that the direct CLI is not Astra-qualified and is not the
desktop client version. The harness still relies on accountable owner
attestation for actual runtime identity; the test does not turn transient
version numbers into permanent policy.

## Review, activation and limits

An independent T1 reviewer must approve the exact committed correction
candidate before the v2.1 roster is installed. Installation is a distinct
owner-attested `set-roster` event on the integrated main revision. After that
event, rerun `check` and `status`, verify the new receipt prefix/head,
eleven available profiles, corrected client version, zero leases and zero API
budget, and record a new activation receipt without editing receipt-bound
history.

Requested model and effort are dispatcher metadata; the runtime exposes no
independent provider-model/effort introspection. The probes qualify only
bounded local repository read/edit/test behavior on the named desktop build.
They do not qualify direct CLI, API, cloud, IDE, another account/workspace,
product behavior, production, providers, security, privacy, legal compliance,
sending, deployment or spending. All 125 product acceptance criteria and all
external gates remain unpassed by this audit.
