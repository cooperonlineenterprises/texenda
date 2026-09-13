# Operational model-routing policy

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Accepted interaction architecture and complete-handoff directive. Apply [package authority](../DECISION-STATUS.md).


## Current model awareness, not invented availability

On **2026-09-05**, the public Codex model page listed `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, and the text-only research-preview `gpt-5.3-codex-spark`. The candidate tier association below is this handoff's recommendation; it is not an authenticated availability claim. Source **N01** in the [source register](../09-reference/source-register.md).

This packaging environment has **no `codex` executable and no authenticated target execution roster**. It did not launch/smoke-test those models. Active tier mappings therefore ship **unverified/null**. “Astra orchestration agent” denotes the lead role independently of any provider model name.

| Tier | Operational role | Public candidates to qualify, not active assignments |
|---|---|---|
| **TIER 1** | Highest consequence/uncertainty; architecture, security, migration semantics, conflict resolution, difficult debugging, final critical review | `gpt-6-astra`; separately qualify `gpt-5.6-sol` as fallback |
| **TIER 2** | Substantial but bounded implementation, normal debugging/refactoring/schema/test work from established contracts | `gpt-5.6-terra` |
| **TIER 3** | Mechanical, low consequence, fully specified and easily verified operations | `gpt-5.6-luna`; Spark only if preview/availability/text constraints fit |

Public names may change. Refresh the official roster and the actual target client before binding. An API model list does not establish ChatGPT/Codex subscription entitlement. A model picker screenshot does not establish tool, effort, network, context or budget compatibility. Never silently substitute an unavailable model.

## Qualification protocol — WP-00 / VAL-13

Record the exact client/version, runtime/account mode (never tokens), available model ID, reasoning settings actually supported, tool capabilities, context constraints, data handling, sandbox/approval controls, billing mode and date. Use a synthetic bounded read/edit/test task to prove each selected tier. Verify that runtime-selected model matches the requested one. Capture sanitized output and hashes. Check whether a stronger model is necessary for the same task; do not invent pricing or capacity.

Store one active binding per tier through the harness `set-roster` evidence record. Bindings expire within 30 days and immediately require review after model/client/account/policy changes. Missing tiers remain unavailable; use a stronger qualified tier or explicit human work, never a weaker unqualified substitute. Rate-limit/network failures do not prove inadequate reasoning.

## Routing rules

Astra MUST route by subtask characteristics: reasoning depth, consequence, uncertainty, reversibility and verification quality. Agent title is not a routing policy. Context-window fit, tools, reliability, data permissions, latency and cost are separate requirements.

Split mixed tasks. A Tier-1 author may resolve state/transaction boundaries, then hand an approved contract and tests to Tier 2. Tier 3 may generate fixtures/boilerplate under that contract. Tier 1 independently reviews changes whose hidden error could expand consent, duplicate effects, expose PII or break migration/recovery. It must not repeatedly re-derive settled product decisions.

Start at the least capable **qualified** tier likely to meet the contract. Prefer a bounded deterministic retry for a simple tooling failure. Escalate after two failed substantive attempts, unexplained confidence loss, contradictory evidence, scope expansion, unexpected security implications or missing architecture. Downshift when the uncertainty has been resolved into an explicit contract. Reconsider routing when observed difficulty differs from the initial classification.

| Representative work | Author route | Review |
|---|---|---|
| Reconsent, withdrawal/suppression semantics or final-permit race | T1 contract → T2 implementation | Independent T1 |
| New type-safe audience UI from approved design | T2 | T2 plus accessibility evidence |
| Compiling parameterized segment AST, including UNKNOWN | T1 algorithm contract → T2 | T1 for logic/security |
| Copying verified schema fields into generated fixtures | T3 | Deterministic schema/tests; T2 spot review |
| Provider outage with uncertain accepts | T1 diagnosis | T1 independent effect/recovery review |
| Formatting/lint/import sorting | T3 | Diff + deterministic checks |
| Importing Kit sequence positions | T1 evidence interpretation → T2 mapper | T1; actual cursor proof required |
| Host setup from qualified runbook | T2 | Human external-effect approval and evidence |
| Documentation index/extraction | T3 | Link/ID/hash validator |
| AI-generated targeting/agent delegation threat model | T1 | Independent T1 + negative tests |

## Context and handoff

Every downshift hands off exact decisions, rationale only where necessary, versioned interfaces, forbidden changes, known traps, test oracles and failure/escalation conditions. A lower-tier agent may ask for more context; it may not resolve an absent policy by intuition. Preserve useful rejected approaches to avoid repeat research, but do not copy entire transcripts.

## Cost and parallelism

Development spending is owner-authorized and **defaults to no new API spending**. Subscription usage is still bounded by tasks, tokens/time and the actual plan limits; do not label it free. The scaffold records budgets but does not meter a provider it does not invoke. The runtime must enforce model/tool/network/spending limits externally and report actual usage where available.

Begin with at most two independent writer assignments. Increase only when review throughput, integration quality and budget support it. Parallel work needs integrated dependency contracts and nonoverlapping write scopes; unrelated agent titles do not make two edits independent. Review/integration is serialized for shared roots, migration manifest and lockfile. Do not keep spending on obsolete branches.
