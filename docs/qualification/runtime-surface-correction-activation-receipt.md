# Desktop runtime correction activation receipt

Activated locally: 2026-09-13T22:37:16.195654+00:00.

## Reviewed input

The instruction-system audit was already integrated at
0a72aba450c76e318b02f22c49133b406da7d4ef. The runtime-attribution correction
candidate d08f3da49a043ee9f62555b6098276ac05ed87f5 (tree
9172cd72b2c15cabd0b147c24fa5e8a2939d8b71) received independent
gpt-6-astra-max approval with no findings. Its review artifacts were added
without changing that candidate, producing integrated head
4c60df8e0e32e3616365205a3d4c2760d44b6f1d (tree
4fe68fbc946142910ee1010b2e464ef822541d28). A final read-only review approved
that exact integrated head with no findings.

The activated evidence is
[model-roster-v2.1.evidence.json](model-roster-v2.1.evidence.json), SHA-256
8e44034e6247ea47b3f0002100e6a343cfa6685d56138a24f55e8a13054173c0.
It retains routing-policy digest
61f0db448cf5ac5adad4d9340d568a7558c0369174e30aab92dd0ccf0d24bdf0.
The [independent review](evidence/runtime-surface-correction-independent-review.md)
and its [evidence envelope](evidence/runtime-surface-correction-review.evidence.json)
record the exact diff, tests, profile inventory, hashes, identity limitations
and safe activation boundary.

## Receipt transition

Immediately before activation, the harness passed check; main was clean at the
reviewed integrated head; the state was version 2.0 with receipt 12, zero active
leases and zero API budget. Independent pre-activation state SHA-256 was
43cf040755cc587373fcddd9c7ff7727d41ccecbc260e9043869c3797a1a82fb.

The owner-authorized local command was:

    python3 tooling/coordination/harness.py --root . set-roster --actor human:owner --record docs/qualification/model-roster-v2.1.evidence.json

It returned {"ok": true} and appended exactly one receipt:

| Field | Value |
|---|---|
| Sequence | 13 |
| Operation | set-roster |
| Actor | human:owner |
| Previous hash | a60e550b634c28cdfdab677e44481bc5fb5803d2056c10f6787df35fefe05092 |
| State digest | 98edcd7b3bb2f6bdc79a7e7958f47632c7146898667c3e189c3b18167e94f916 |
| Receipt hash | f39249184757101b108ea7ec5ea0ffebdd8237315b8ac3cad3ad0cc6ab3e827e |
| Post-state file SHA-256 | b993eebdba5d2d8e5597c7205ee58846bf83ecb9d553bc55a687dcf1f7880235 |

The first twelve receipt objects and receipt-12 head remain unchanged. The
v1-to-v2 migration checkpoint and source prefix remain preserved.

## Post-activation verification

The harness check command returned integrity PASS. Status reported:

- version 2.0 and receipt count 13;
- eleven available exact profiles and no unavailable profile;
- T1 gpt-6-astra-max, T2 gpt-5.6-sol-max, T3 gpt-5.6-terra-max and T4
  gpt-5.6-luna-max as available defaults;
- gpt-5.6-sol-max as the sole listed T1 fallback;
- one runtime, codex-desktop-collaboration, and one client,
  26.901.41600 (build 7982), across all roster rows;
- zero active or expired leases, zero API budget, zero declared spend and no
  paid-work authorization;
- WP-00 still completed and every other work package still planned.

The separately installed codex-cli 0.149.0 remains unqualified, including for
Astra. The activation does not silently substitute it or any model/effort. It
does not extend profile expiry or an assignment fence.

## Boundary

This receipt documents one local, reversible roster-evidence replacement in the
ignored coordination ledger. It is not a product deployment, provider
activation, API call, purchase, reset, send, production-data access or external
effect. It does not qualify direct CLI, API, cloud, IDE, another client/account
or another workspace. It does not mark any of the 125 product acceptance
criteria or any external gate passed.
