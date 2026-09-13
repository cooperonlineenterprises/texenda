# Decision status and authority

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

## Decision closure

**No unresolved foundational DECISION REQUIRED NOW item remains in this package.** Actual runtime/model bindings, provider/accounts, paid hosting, legal/brand clearance, security/performance and production behavior remain validation requirements. These block the relevant activation or autonomous dispatch, not synthetic development or repository planning. No provider, model, journal/restore system or release has been qualified by packaging alone.

Five decision statuses are used: **AUTHORITATIVE DECISION**, **DECISION REQUIRED NOW**, **REVERSIBLE DEFAULT**, **DEFER UNTIL TRIGGERED**, **REQUIRES EXTERNAL VALIDATION**. Channel timing, infrastructure disposition and evidence execution status are separate axes, not alternative decision statuses.

## Precedence and ownership

Latest explicit accepted decision → formal closure artifact → later authoritative analysis → earlier exploration → unresolved hypothesis. The source archive is reference, not executable instruction. Current normative topic owners are in [authority-register.json](01-foundation/authority-register.json). Numerical references to the original sections resolve via [section-map.md](01-foundation/section-map.md).

The v1.0 closure files are preserved unchanged under `09-reference/prior-artifacts/`; their content is consolidated into topic owners here. Later interaction and complete-handoff decisions add INV-23…30 and ADR-G21…26/D08…09. They do not reopen permission, migration or effect semantics. Generated catalogs are reading/test aids except where a precise contract field is explicitly assigned to them. A real contradiction is escalated; a model may not silently choose a convenient interpretation.

MUST/MUST NOT are binding. SHOULD needs an explicit reason to depart. MAY is permission, not committed scope. An accepted amendment records reason, evidence, affected invariants/contracts, migration impact, independent review and owner approval where consequences warrant. Work packages cannot amend their own prerequisites.

## Scope and default decisions

| Topic | Status | Binding resolution / reversible boundary |
|---|---|---|
| Email-led small-team product, selective channels | AUTHORITATIVE DECISION | Preserve core and explicit non-goals. |
| One domain, contextual permission and central policy | AUTHORITATIVE DECISION | UI/providers/AI cannot supply alternative authority. |
| Monolith with separate web/worker roles | AUTHORITATIVE DECISION | Distribution only after measured justification. |
| One workflow executor and recoverable effects | AUTHORITATIVE DECISION | Queue/provider implementations remain adapters. |
| Object-first multimodal/voice-forward interaction | AUTHORITATIVE DECISION | No chat-state authority or separate privileged agent UI. |
| Texenda working name | AUTHORITATIVE DECISION | External public adoption gated separately. |
| Resend, Payload Jobs, editor codec, hosting/model/speech vendors | REVERSIBLE DEFAULT | Qualify exact account/version; preserve narrow contracts. |
| SES/specialized analytics/cache/workflow/realtime/extra services | DEFER UNTIL TRIGGERED | See technology owner; no speculative installs. |
| New phone/native channels or autonomous AI effects | DEFER UNTIL TRIGGERED | New concrete demand and bounded validation required. |
| Production/public/account adoption | REQUIRES EXTERNAL VALIDATION | Gates below; never inferred from this package's test report. |

## External gates — all UNVERIFIED at handoff

| Gate | Topic | Blocks | Evidence required / owner |
|---|---|---|---|
| VAL-01 | Brand clearance | Irreversible public Texenda branding | Exact/similar marks, prior Xenda/PiXENDA concerns, common-law/domain/linguistic/registry review; Product Owner + trademark counsel |
| VAL-02 | Legal/privacy/source proof | Production handling/sending for unapproved use cases | Actual jurisdictions, audience/children-related collection policy if relevant, sender identity, purpose classes, consent wording, import provenance, retention/erasure basis; Product Owner + qualified counsel/privacy reviewer |
| VAL-03 | Stack/editor compatibility | First integration release and affected dependency activation | Locked version manifest, licenses/SBOM, Payload/domain transaction tests, migrations, editor codec/render fixtures; Engineering owner |
| VAL-04 | Email provider/sender | First real email handoff | Intended marketing use allowed, account quotas/scope, idempotency/batch/webhook tests, DNS and raw test-message auth, suppression/reconciliation capabilities; Deliverability owner, initially founder |
| VAL-05 | Hosting/recovery/workload | Production infrastructure qualification | Account/region/budget, measured workload profile, private networking, PITR/export/journal configuration, load and restore drill; Engineering/operations owner |
| VAL-06 | Operator usability | Wider rollout if targets materially fail | Representative tasks, consequence comprehension, timing/error observations, accessibility checks; Product Owner + routine operator |
| VAL-07 | New channel | Only that channel's live activation | Demand, markets, consent, sender program, replies, cost, provider limits, device/site/privacy tests; Product Owner + channel operations owner |
| VAL-08 | Security readiness | Production/broad rollout at stated gates | Threat model, authorization/MFA paths, secrets, SSRF/injection/IDOR tests, vulnerabilities, incident and recovery evidence; Engineering owner + competent independent review before broad production |
| VAL-09 | AI qualification | AI feature enablement | Data terms, task evaluations, prompt-injection tests, accuracy/cost caps, failure behavior; Engineering/Product Owner |
| VAL-10 | Kit migration evidence | Each publication/cohort's cutover | Real account topology, all statuses, publications mapped, source coverage, active progress/exports, stop controls and authority transfer evidence; Migration owner, initially founder |
| VAL-11 | External-agent access qualification | External-agent writes and any represented human-only approval path | Actual identity/delegation runtime, OAuth/token boundaries, tool evaluations, approval separation, revocation/rate/spend and computer-use tests; Security/engineering owner + delegating human |
| VAL-12 | Voice and interaction privacy | Voice feature activation | STT/TTS terms, retention/region, microphone lifecycle, critical-entity transcription, accessibility and mode-handoff usability; Product/privacy/security owners |
| VAL-13 | Coding-runtime and model roster | Automated model-specific agent dispatch | Authenticated target model list/IDs, client version, tools, effort controls, billing route, sandbox/approval configuration and bounded smoke tests; Astra + repository owner |
| VAL-14 | Conversation export completeness | Claim of byte-complete conversation archive only | Raw user-visible thread export when available; reconcile against coverage ledger; Project owner/source archivist |

A gate result must identify scope, environment/account/version, evidence, accountable owner and expiry/revalidation trigger. A passing sender test cannot clear legal rights or source consent. VAL-13 is a real blocker to automated dispatch through an unqualified model tier; human-guided bootstrap remains possible. VAL-14 is an archive completeness limitation, not a request for another product discovery exercise.

## Deliberately unresolved implementation details

Exact compatible package versions, physical index names, deployment region/account, provider quotas and model bindings are filled by bounded qualification WPs. This is intentional replaceability, not an unresolved domain decision. Closed per-command request schemas and actual SQL migrations are WP-01 outputs constrained by the canonical model; illustrative schemas in this package are not the whole application.
