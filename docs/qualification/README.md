# WP-00 runtime qualification

This directory is the local, sanitized evidence index for the bounded Codex runtime qualification required by WP-00 / VAL-13. It establishes only read, edit, and test capability in the subscription runtime; it does not pass any product, production, provider, legal, privacy, security, deployment, sending, billing, or other external gate.

Active bindings are `gpt-6-astra` (Tier 1, high), `gpt-5.6-terra` (Tier 2, medium), and `gpt-5.6-luna` (Tier 3, low). `gpt-5.6-sol` is a qualified Tier 1 fallback, not an active binding. `gpt-5.3-codex-spark` is unqualified and must not be routed. All active bindings expire exactly `2026-10-12T16:45:48Z`, or earlier upon a relevant model, client, account, sandbox, or policy change.

Use [runtime-inventory.json](runtime-inventory.json) for sanitized runtime facts, [model-roster.evidence.json](model-roster.evidence.json) for active binding metadata and expected hashes, [model-qualification-verification.md](model-qualification-verification.md) for the verification record, and `probes/` for the per-model bounded task evidence. Before resuming automated routing, parse every JSON artifact and recompute its SHA-256 against the roster; if any mismatch, expiry, or material runtime change is found, treat the binding as unavailable pending requalification.

No harness submission evidence is created here; Astra binds the committed candidate separately.
