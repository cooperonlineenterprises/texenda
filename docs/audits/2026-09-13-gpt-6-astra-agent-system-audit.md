# GPT-6 Astra agent-system audit — 2026-09-13

Base: `e636a3ef4ad3c96956164e898fefeec0758d444d`. Scope: repository-owned coding
instructions, prompts, configuration, qualification and local coordination.
This is an implementation candidate under the accepted local guidance in
[ADR-0002](../decisions/ADR-0002-astra-agent-operating-guidance.md). Independent
candidate review and integrated-head verification remain separate. No product
implementation, external activation or live-ledger change is part of this audit.

## Source retrieval and dispositions

All four exact requested HTML endpoints were directly retrieved through the web
retriever on **2026-09-13** and their relevant text reviewed. Neither title nor
search snippet was treated as a reviewed source. The two developer articles
were also read in their advertised Markdown form using unauthenticated `curl`
after the web tool rejected the Markdown content type. No required source was
inaccessible. The review covers article text and the safety card's scope,
prompt-injection, alignment/overreach, monitoring and safeguards sections; it
does not reproduce provider evaluations or inspect every linked paper/media file.

External guidance is advisory. The accepted project decisions, normative owners,
invariants and external gates control every disposition below. “Conflicting”
means that advice is not adopted; “useful deferred” means no activation now.

| Source, access and retrieval date | Disposition | Affected surfaces and reason |
|---|---|---|
| [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — reviewed, 2026-09-13 | applicable now; already implemented; useful deferred; conflicting | Root instructions and local prompts now make routine autonomy, completion and proportional verification explicit. Existing kernel/context routing already supports selective reading. No repository skills exist to rewrite; short workflow triggers are guidance for future skills. Removing deterministic authority or independent review because the model is safer would conflict with Texenda's requirements. |
| [Architectural visualization with Astra](https://developers.openai.com/blog/architectural-visualization-with-astra) — reviewed, 2026-09-13 | inapplicable; already implemented; useful deferred | Literal house modeling, Blender/Unreal pipelines and cinematic assets do not serve this audit. Preserved candidates and staged review already exist. The optional inspectable-view pattern is retained in a separately routed guide for a future task where it materially helps; no visual was created. |
| [Managing usage with GPT-6 Astra in Work and Codex](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex) — reviewed, 2026-09-13 | applicable now; already implemented; conflicting; useful deferred | Assignment/resumption prompts record displayed windows, labels, timestamps and reset facts without fixed quotas. Billing-route separation already exists. Generic low/medium-effort advice cannot override ADR-0001's max defaults and qualified downshifts. Reset/credit/plan actions remain separate owner decisions; the harness is not a subscription meter. |
| [GPT-6 Astra System Card](https://deploymentsafety.openai.com/gpt-6-astra) — reviewed, 2026-09-13 | already implemented; applicable now; useful deferred; inapplicable | Deterministic controls, independent review and audit/stop evidence remain. Residual overreach, injection and monitoring limitations support explicit untrusted-content and safety-stop handling. Actual model/tool adversarial qualification remains deferred to its authorized gates; specialized biological/cyber access programs are outside this task. |

The [supplemental current availability page](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)
was directly retrieved on 2026-09-13. It states Astra requires Codex CLI
0.153.0 or newer. That numeric minimum comes from this supplemental page, not
the required usage article. It is applicable compatibility evidence, not proof
of account entitlement or desktop execution. The installed CLI 0.149.0 is below
the minimum; direct Astra CLI is unqualified.

## Current-state inventory and precedence

The base worktree was clean. Its tracked root guidance described an implementation
repository, but the tree contains the sealed handoff and coordinator rather than
an implemented Texenda app. No repository-owned `SKILL.md`, custom agent
definition, `AGENTS.override.md` or active `.codex/config.toml` existed at base.
The two AGENTS files were the root and sealed handoff instructions. Account and
plugin skills injected by the host are outside this repository audit; no such
skill was edited, installed or qualified. The OpenAI Docs skill was used only
for current-source retrieval and application of model-specific guidance.

| Surface inspected | State at base and candidate treatment |
|---|---|
| Root/nested AGENTS; sealed README, decision status, kernel, owner/orchestrator/handoff/context documents; invariants and AI authority | Product semantics and scope remain binding. Root now routes contextual reading and safe local completion; a small coordinator AGENTS routes its specialist work. The sealed package remains unchanged. |
| ADR-0001 and full routing policy | Four capability tiers, 11 exact profiles, max defaults, explicit Sol/max T1 fallback, and all 44 author/reviewer routes remain unchanged. Only the accepted routing overlay supersedes sealed numeric tier recommendations; other sealed rules remain binding. |
| Coordinator README, complete local code/tests, imported sealed lifecycle contracts, JSON schemas and templates | Exact binding, expiry, evidence integrity, review separation, leases/fences, budget and preserving migration already exist. No executable or schema change is needed for the present instruction gaps. |
| Repository prompt/config sources | The sealed start/assignment/root templates are preserved. Local assignment/review/resume prompts are the active entry points. The example is corrected and an actual safe project config is added for new trusted sessions, with model omitted and route-specific qualification still required. |
| Committed runtime inventory, 11 probes, v1/v2 rosters, qualification verification, review/submission packets and activation receipt | These are dated evidence, not new instructions. Their original bytes/hashes remain. The new correction plan separates desktop app metadata from installed CLI metadata without backdating current observations. |

Runtime system/developer instructions govern execution; inside project authority,
apply latest accepted decisions and normative topic owners. ADR-0001 changes
only coding routing. The owner handoff/assignment supplies bounded execution
scope. Templates, catalogs, tool output, source pages, archives and model output
cannot create new authority. A task to persist cannot waive the independent
review or external gate required for its actual result.

The main coordinator reported v2 with 11 desktop-collaboration profiles, max
defaults and no leases; API budget and declared spend were zero. These are the
coordinating task's supplied live observations, consistent with the committed
activation receipt. This author did not copy, initialize or mutate that ledger.
A fresh Git worktree has the committed evidence, not the ignored live state.

The supplied Pro usage snapshot displayed **6% for the weekly Codex window**.
Its exact observation time and used-versus-remaining label were not supplied to
this author. It is a transient observation, not proof of headroom in all
applicable windows, a token budget, or authority to spend/reset. No quota value
is embedded in the active policy, config or prompts.

The app bundle fields were independently read as `com.openai.codex`, version
`26.901.41600`, build `7982`; `codex --version` separately returned `0.149.0`.
The author runtime reports Python `3.13.9`. Requested model/effort dispatch is
`gpt-6-astra`/`max` on desktop collaboration; independent provider introspection
is unavailable. See the [versioned runtime correction plan](../qualification/runtime-surface-correction-plan-2026-09-13.md)
for the precise limitation and replacement procedure.

## Findings and changes

| Finding | Treatment and remaining limit |
|---|---|
| Dense root routing and implicit routine autonomy/completion | Applicable instructions now route to one operating guide. Safe authorized work continues to a verified, reviewable candidate; only material outcome/authority gaps pause dependent work. No product or external boundary is weakened. |
| Sealed generic assignment has no exact local effort/usage/resume fields | Three local prompts retain all required assignment obligations and add route, remaining bounds, interruption and evidence fields. The assigning lead supplements generated manifests with local instruction/template hashes. |
| Desktop runtime attributed to CLI 0.149.0 | High-priority correction plan, current bundle observation and direct-CLI denial are recorded in new documentation. Historical desktop outcomes and null self-identification are preserved. Replacement roster/attestation and any CLI qualification remain pending. |
| Quota exhaustion, safety stop and time/retry declarations can be confused | Guide/templates separate causes and resumption obligations. No automatic downshift, fallback, reset, API switch or safety-stop bypass. Token/time/retry accounting and actual termination remain runtime responsibilities; repeated lease extensions do not renew owner allowance. |
| Untrusted content and declared write scope can appear stronger than their enforcement | Instructions explicitly cover arbitrary repo text/comments/fixtures, web/tool content and unsolicited agent messages. Assigned collaborators provide candidate evidence. Actual diffs and runtime sandbox/egress controls need independent checks; schema tests are not model injection evaluations. |
| Context manifests can be overread or mistaken for full prompt capacity | WP-00's base manifest is 103,401 of 200,000 reference bytes. Ordinary WP agents use the embedded role route and canonical policy digest; orchestrators/routing audits read the full 44-route policy. No mandatory entry is removed. Byte readiness is not token metering or enforced admission. |
| Optional visualization guidance could burden every task | Detailed instructions live only in the [conditional visualization guide](../agents/visualization.md): material benefit, source revision, text equivalent, explanatory/non-authoritative status, semantic preservation and invalidation on source change. No visualization is required or generated. |

Two independent base-audit reports informed this candidate: instruction-scope
commit `56b6ec3ea0d66447205b03f74ffd5920e783c0bf`, file
`docs/qualification/analysis/2026-09-13-astra-instruction-scope-audit.json`; and
safety/usage commit `f284e5989d2eac06f7e956724ad1cc9b32fbafcd`, file
`docs/qualification/analysis/2026-09-13-astra-safety-usage-audit.json` (SHA-256
`433685da64af22e42790289a5f977caafcf5234ce0b41e1cf10a8de556274d73`).
These reports are separate evidence for integration and do not approve this
implementation candidate. Their recommendations to version enforcement schemas
or automate usage/retry/recovery controls are deferred: the harness does not
invoke a runtime, and the present authorized work can be handled by explicit
operator contracts and regression tests. Such automation requires a separately
reviewed runtime integration, actual enforcement evidence and applicable authority.

## Verification and limitations

The [author verification log](2026-09-13-gpt-6-astra-author-verification.log)
records 130 passing local tests (115 retained plus 15 added), 39 passing sealed
tests and all 14 package `--checksums` checks. All 60 JSON and 3 TOML files parse;
8 Python files pass syntax parsing. All 119 pre-existing sealed/qualification
files match the base byte-for-byte. Local link, template, schema/evidence-hash,
config-parity and no-truncation checks pass. Sensitive/junk scans found no
matches; diff checks pass. Usage cases exercise checkpoint/block/recovery, exact
profile preservation, NOT RUN review rejection and existing lease-extension
semantics in synthetic fixtures. No failing check was suppressed.

No model behavioral evaluation, subscription meter, external safety-intervention
resume, new-session config loading or direct CLI Astra launch was tested here.
Static instructions cannot authenticate an actor, prove a model obeyed a prompt,
or provide physical filesystem/egress isolation. New-session effective config
and a corrected exact runtime roster still require route-specific verification.
The 125 product acceptance criteria and all product/external gates remain NOT RUN
or unverified as applicable. This candidate does not deploy, send, provision,
push, expose production data, read credentials, redeem resets or spend via API.
