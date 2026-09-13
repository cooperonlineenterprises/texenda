# AI operating model

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f10"></a>
## 10. AI operating model

**Decision status: AUTHORITATIVE DECISION.** AI prepares and explains. Deterministic commands, current permission, and approved revisions remain the only execution authority.

| Capability | Role | Maximum authority | Required validation and review |
|---|---|---|---|
| Natural-language segment | INTERPRET, CONFIGURE | **MAY CONFIGURE WITH PREVIEW** | Schema/compiler, workspace scope, source coverage, plain-language criteria, count/sample; operator accepts before use |
| Automation or sequence creation | GENERATE, CONFIGURE | **MAY PREPARE DRAFT** | Supported graph, bounded sends, no consent mutation, exits/expiry, simulation; publish approval |
| Campaign/sequence copy | GENERATE | **MAY PREPARE DRAFT** | Human verifies facts, offer, tone, CTA and disclosures |
| Channel adaptation | GENERATE | **MAY PREPARE DRAFT** | Typed representation, protected-fact equivalence, channel limits; per-variant approval |
| Brand adaptation | GENERATE | **MAY PREPARE DRAFT** | Access to source/target context and target-brand review; no audience transfer |
| Import mapping | INTERPRET, CONFIGURE | **MAY CONFIGURE WITH PREVIEW** | Dry run and provenance; uncertain consent held, never guessed |
| Performance summary | INTERPRET, EXPLAIN | **ADVISORY ONLY** | Computed metric references, windows/denominators/coverage; no fabricated causal claims |
| Anomaly explanation | MONITOR, EXPLAIN | **ADVISORY ONLY** | Deterministic threshold and evidence; AI cannot release a pause |
| Audience/timing/channel recommendation | RECOMMEND | **ADVISORY ONLY** | Show eligible options, evidence, uncertainty, cost and policy consequences |
| Product/settings assistance | EXPLAIN | **ADVISORY ONLY** | Version-correct documentation and role-scoped evidence |
| Schedule an already approved campaign through natural language | EXECUTE | **MAY EXECUTE WITH CONFIRMATION** | Confirmation binds exact approved revision, audience contract, schedule, ceiling and principal; normal command executes |
| Bounded internal draft/summary jobs | GENERATE, MONITOR | **MAY EXECUTE AUTONOMOUSLY WITHIN EXPLICIT POLICY** | Internal-only output, allowlisted sources, task/model/token budget; no outgoing recipient messages |
| Create consent, clear suppression, expand authorization/budget, override policy, invent live campaigns | CONFIGURE, EXECUTE | **NOT PERMITTED** | No tool/capability exists for these operations |

Structured output is a required interface, not proof of correctness. Models return proposed DTOs, never raw SQL, arbitrary URLs to invoke, or an imperative script. Run normal validation and authorization after model output exactly as for a human-created draft. A confirmation token is short-lived, single-use, digest-bound and invalidated by changes; the UI shows what the token authorizes.

Data minimization occurs before model access: schema, approved brand context, aggregates and necessary redacted examples. Raw contact export, other brands' data, credentials and unrestricted event history are not model context. Retrieved documents, emails, imports, website text and tool results are untrusted data, not instructions. Tool allowlists, typed boundaries, isolation and approvals reduce risk; they do not prove prompt-injection immunity. [S18](../09-reference/source-register.md#s18)

Record task ID, initiating principal, allowed scope, input-document revisions, model/provider/version, prompt-template version, structured proposal, validator results, operator changes/approval, token/cost usage and resulting command IDs. Do not collect hidden model reasoning. Retain only task-relevant data under the telemetry/PII schedule.

**REVERSIBLE DEFAULT:** use an `AIProvider` adapter with OpenAI API as the first integration candidate; do not freeze a specific model name. Bind an exact evaluated model snapshot where available, not an unreviewed “latest” alias. Select a lower-cost qualified model per task and escalate only within the same budget and authority. An initial internal ceiling of **USD 25/month and USD 1/task** is a proposed reversible cap, disabled until the owner activates billing. Hard ceilings include reservations and estimated output cost. No automatic credit reload or budget expansion.

**REQUIRES EXTERNAL VALIDATION — VAL-09:** provider data terms, retention, model evaluations, injection tests, cost behavior and operator acceptance. An unavailable or invalid AI response leaves a visible draft/task error. Deterministic builders and all approved live automations continue without AI. No AI call is required in the send-policy path.

**Consequences:** ordinary UI and source-of-truth calculations must be complete without AI. **Revisit:** additional internal autonomy may be added only with a bounded capability and evaluation; autonomous marketing send invention remains out of scope.

---


## External-agent and interaction authority extension

The product's `AIProvider` and Astra's coding-model routing are separate systems, budgets and credentials. Texenda's USD 25/month and USD 1/task reversible AI defaults do not authorize any development API spending. The build harness starts with no live model budget and no active runtime mapping.

Agents receive tools, not database/provider credentials. Built-in assistant authority is the initiating human's current scoped authority narrowed by the tool allowlist. External agents additionally require AgentPrincipal + current DelegationGrant. Effective permission is the intersection of organization policy, user membership, grant/resource/command scope, approval and current domain policy. Neither inferred intent nor provider model confidence increases it.

Initial external-agent deployment supports authorized reads and proposals. C3 execution requires an already approved, digest-bound command envelope, an explicitly allowed grant, current policy and spending reservation. C4 operations remain unavailable to agent tools. Agents cannot approve their own proposals or manufacture human authentication assurance. Subsequent autonomous internal draft/summary work remains explicitly bounded and non-external.

Use API `/api/v1` and stable JSON schemas; an MCP layer later maps to the same commands. Qualify the protocol revision, resource/audience-bound OAuth tokens, PKCE where applicable, issuer validation, exact redirects and revocation. Do not pass third-party provider tokens through Texenda tools. Tool descriptions, resource text and annotations are data; server authorization is decisive.

Browser computer use SHOULD use a distinct constrained agent session. A general agent controlling an ordinary human browser cannot be reliably distinguished by inference; disclose this attribution limit and offer no additional authority. A button cannot authenticate human judgment. Human-only high-risk approvals require an independent interaction/assurance context unavailable to the agent. UI accommodations do not solve identity impersonation.

Persist only explicit assistant preferences, scoped goals, proposal refs and bounded session summaries. No general inferred memory store initially. Models see minimized authorized context; secrets and bulk contact records are not prompt inputs. Logging records model/task/configuration refs and outputs, not hidden chain-of-thought. Provider/model changes require task requalification.
