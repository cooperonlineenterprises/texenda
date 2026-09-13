# Model qualification verification

Verified at: `2026-09-13T16:45:44Z`
Baseline revision: `0cd7010242ee1ee35837aace4ea2a1f1a186777e`
Runtime: `codex-desktop-collaboration` via `codex-cli 0.149.0`

The owner authorized a bounded model-tier qualification in the interactive Codex task. Four isolated agents were dispatched through the runtime with exact model and reasoning-effort overrides. Each agent read the project kernel and invariants, wrote one scoped JSON artifact, parsed it with `jq`, ran the offline package validator, and ran all 39 synthetic harness tests. No agent used network access, installed dependencies, read credentials, contacted an external service, committed, pushed, deployed, or sent communications.

| Role | Requested model | Effort | Package validation | Harness tests | Artifact SHA-256 |
|---|---|---:|---:|---:|---|
| Tier 1 active | `gpt-6-astra` | high | PASS | 39/39 PASS | `6ab0d7b121630937de88441c1aedf1e46de1da1d0319ac01806bb7435fdf726f` |
| Tier 1 fallback | `gpt-5.6-sol` | high | PASS | 39/39 PASS | `b3517e156c382bc9fb45ed29994a8ff573854ddcd03436fee88ed053810ae300` |
| Tier 2 active | `gpt-5.6-terra` | medium | PASS | 39/39 PASS | `1c81e33c60d7da2e23b1d9f4fc1c8e8647bb26dfce3ff9fcce6dc3d1d19aeda3` |
| Tier 3 active | `gpt-5.6-luna` | low | PASS | 39/39 PASS | `469723e6801d3a2c91d29d52ca3ed69c4bcdc6206d7a85cceb12c472b08ab00f` |

Independent orchestration checks confirmed that every artifact parses as JSON, preserves INV-02, INV-12, and INV-30 accurately, declares no secret access, reports both required commands with exit code 0, and retains the same SHA-256 after copying into the repository.

The dispatch API's accepted model override is the runtime selection evidence. The agents had no separate introspection channel, so `self_reported_model_id` remains `null`; this limitation is retained rather than converted into stronger evidence. The probes do not qualify application behavior, production services, providers, legal/privacy status, deployment, sending, or external effects. The bindings expire after 29 days and must be requalified sooner after a model, client, account, sandbox, or policy change.
