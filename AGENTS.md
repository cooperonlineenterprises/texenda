# Texenda implementation instructions

This repository implements Texenda, an email-led audience and communication platform for very small teams. Read `specs/texenda-handoff/README.md`, `specs/texenda-handoff/DECISION-STATUS.md`, and `specs/texenda-handoff/07-agent-orchestration/project-kernel.md` before implementation. Read only the relevant normative domain/ADR context for the assigned WP; do not load the entire archive.

All surfaces share authoritative commands. Shared identity never grants permission. Withdrawal is distinct from safety Suppression. One workflow executor serves sequences and automations. Queues/providers/AI are not authority. Current denials outrank historical approval. Never blindly resend or fail over unknown provider acceptance. Journal/restore and Kit migration fences are mandatory before live sends.

Astra admits work from the WP graph, supplies bounded contexts, selects the least costly qualified model tier, reserves disjoint write scopes, and integrates independently reviewed candidates. Do not edit outside the assignment or change a governing decision without explicit amendment. Report exact tests/evidence and NOT RUN honestly. No production keys/data, billing, DNS/cloud mutation, deployment or sending without separate owner authorization. No destructive reset or overwriting another actor's edits.

Use `specs/texenda-handoff/08-project-harness/harness.py` for local coordination. The scaffold does not authenticate actors, enforce a sandbox, invoke models or grant production authority. Inspect current runtime capabilities; never invent model availability. Resume from verified state and repository evidence, not chat memory. Provider/model/framework defaults remain replaceable.
