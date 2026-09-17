# ADR-0008: Integrated initial product and effective implementation plan

Status: AUTHORITATIVE LOCAL AMENDMENT — explicit owner decisions on 2026-09-17.
Acceptance of these decisions is distinct from exact-candidate independent review,
plan activation, implementation, product acceptance and production authorization.

## Decision and supersession

The first usable Texenda application includes contextual built-in AI, complete
direct human workflows, preferred structured external tools/API, and deliberately
designed/tested accessible computer use. They share objects, commands, permissions,
revision-bound approvals and results. Drafts, active-object context, pending
approvals, failures and recovery survive handoffs. A chat box or static demo is
not completion. Manual completeness during AI outage is resilience, not grounds
to postpone integrated assistance. Foundational work defines these contracts
without needing a live model.

Texenda owns fixed-layout, accessible, brand-aware signup and thank-you pages,
including authoring, preview, versioned publication/unpublication and operation.
They integrate disclosures, forms, confirmation and requested-resource fulfillment.
Existing sites may link/embed; they do not replace native pages. No general site
builder, blog, newsletter archive, arbitrary scripting or replacement CMS is added.

Adopt safe draft-only cloning, representative welcome/nurture and reviewable
hygiene recipes, returning-user/human-agent handoff and review/correction-effort
evaluation, and evidence-led Kit parity/continuity. Research scores/complexity
budgets remain hypotheses. Preserve voice direction with explicit capture,
manual/text fallback and VAL-12; voice is not an initial non-voice prerequisite.

This supersedes the prior thread assessment's external-first/deferred-embedded
recommendation and existing-website-first/fallback-as-substitute recommendation.
The research refinement itself already proposed bounded native pages; neither
research package becomes authority, and its normative labels do not transfer.

## Exact scope and one owner

This ADR is the sole owner of its machine block below. It is an overlay, not a
second independently maintained catalog. The effective plan is deterministically
composed from the hash-pinned sealed catalog/profiles/acceptance plus these exact
deltas. Unchanged sealed fields retain their owners. The dossier indexes this
owner; it must not copy requirements or maintain product task status.
The existing consolidated RAIDQ owner also records the new product qualification
and deferred-dependency details. Those records reference, never redefine or clear,
the sealed external gates; existing workspace records remain byte-preserved.

Superseded interpretation is limited to:
- product-and-brand scope: integrated assistance and bounded native acquisition
  are initial usable scope; site-building exclusion continues outside that slice;
- operator-workflows/interaction implementation-order statements allowing a
  manual-only email pilot to count as the first usable product;
- only the listed work-package fields and email-pilot profile parent/scope;
- acceptance extension rows AC-IP01–AC-IP18 and stage-specific interpretation
  specified here. Existing criteria/invariants are not waived.

Publication remains a recurring communication promise. AcquisitionPage revisions
reference the relevant Property, Workspace/Brand, Publication/purpose and disclosure.
They do not replace Publication. Acquisition owns page lifecycle/forms/requests;
content owns resource manifests/versioning; the asset adapter owns storage
mechanics only; permission owns grants/withdrawals; delivery owns fulfillment
effects; the existing executor owns workflow progress. Audience remains a view.
Email still follows ADR-0005; no second renderer/content truth is implied.

Shared command services own every mutation. Built-in AI is a proposal/explanation
adapter. External API and computer-use sessions use attributable constrained
principals, never the delegating human session. Human-only approval cannot be
satisfied by agent clicking, tool annotations or conversational assent. No
autonomous sending, publishing, spending, permission expansion or approval
authority is added. Page publication, domains, accounts and all other external
effects retain their existing approvals.

## Stage and evidence separation

1. **Initial synthetic:** runnable web/worker, persistent synthetic data,
   representative authentication/authorization, complete integrated journeys,
   deterministic fake AI/mail/Kit/storage, callbacks, retries, cancellation,
   interruptions and recovery. No real account/data/paid resource required.
2. **Real AI/provider qualification:** exact model/client/provider, terms,
   scope, grant/revocation, injection/quality, quotas/cost and failure evidence.
   A deterministic model substitute cannot prove real model quality or agent ability.
3. **Production-connected staging:** separately authorized nonproduction accounts,
   isolated realistic infrastructure, actual callbacks, credentials, deployment,
   security, workload/backup/restore and operator/agent rehearsals. WP-17 owns the
   qualification packet; WP-39/41 supply mechanisms and local exercises.
4. **Production readiness:** all applicable acceptance and gates bound to exact
   revision/configuration/accounts/infrastructure, data/migration readiness,
   accountable incident/support/recovery ownership and signed release approval.
5. **Activation/operation:** separate owner-approved public-page/domain/sender/
   production-data/canary authority; WP-20 then WP-33/42 retain controlled rollout,
   legacy opt-outs, observation, alerts, support, backup/restore and repair-forward
   recovery. VAL-01 or an accepted neutral identity precedes public branding.

The initial-production profile carries real AI/agent gates; inherited email-pilot
cannot bypass it. Optional voice/channels keep their own qualifications. Synthetic
completion never clears a gate or marks a real-environment acceptance row passed.
AC-IP18 is post-approval activation/operation evidence owned by WP-20/33/42,
not a prerequisite for preactivation readiness; AC-IP17 and applicable sealed
operational criteria require the rehearsed plan and accountable owners first.
A scoped synthetic analogue may pass while its real qualification remains NOT RUN.
Actual operator and actual external-agent observations cannot be fabricated by a
scripted browser driver; record precisely which was exercised.

## Forward coordination boundary and recovery

Use the existing coordinator, ledger, routing policy and evidence store. Keep the
same 44 WP IDs and original sealed catalog digest for historical interpretation.
A new, explicit effective-plan digest identifies the amended contract. No roster,
model, effort, budget, gate, completed WP or old receipt is reinterpreted.

After exact independent approval and proved runtime stop, explicit plan activation
may append one forward receipt and move the state protocol to 2.1. Preserve the
byte-exact preactivation checkpoint and all original events/tasks/history. Refuse
leases (including expired), uncertain work, already-started changed scope, missing
or substituted sources/evidence, and corrupt checkpoints. Reads/check/context never
activate. Old 2.0 lifecycle writers must refuse 2.1; old unbound context manifests
are insufficient for dispatch. Future admissions/assignments and acceptance bind
the effective plan; stale plans fail closed. Changed plan bytes cannot silently
renew authority. Old lower-effort/paid attestations cannot authorize enlarged work.

Activation is local planning governance, not product admission, execution or gate
clearance. The current owner request authorizes this bounded forward cutover once
independently approved. Do not impersonate an owner; record the real integrating
actor and the owner-request basis. Recovery preserves checkpoint/receipts and uses
the existing atomic-write protocol; no destructive rollback/history rewrite.
Future semantic plan changes need another reviewed successor and explicit boundary.

## Machine-readable scoped contract

The code block is authoritative only for the named amended fields and additions.
Human summaries are navigation; research and test fixtures cannot change this owner.

<!-- texenda-initial-product-contract -->
```json
{
  "schema_version": "texenda.initial-product.v1",
  "id": "PLAN-IP-0001",
  "decision": "docs/decisions/ADR-0008-integrated-initial-product-and-effective-plan.md",
  "owner_decision_date": "2026-09-17",
  "sealed_catalog_sha256": "9ad162070c27e4c765ba145fc8a35d31dc288482453daaa39ec0bb6add8bd8d8",
  "sealed_profiles_sha256": "869813ada7d0ea1a829cdad9204b35c67fd2631707fbbfbab50a315a3a3b8b15",
  "sealed_acceptance_sha256": "e6bf0bb96152e4fbcd9b4da13817f0a06ca4e57cd5502c4b329a4cc216ee7e58",
  "authority": "Scoped successor fields and acceptance additions only; sealed unchanged fields retain authority. No permission, implementation, gate clearance or readiness is created.",
  "work_package_updates": [
    {
      "id": "WP-01",
      "reason": "Design integrated interaction and bounded acquisition into foundational contracts, not a retrofit.",
      "replace": {},
      "append": {
        "scope": [
          "Include page/resource lifecycle, shared UI/AI/tool command ownership, draft cloning, scope-aware interaction context and semantic/keyboard navigation contracts. No model is needed to define these contracts."
        ],
        "expected_outputs": [
          "Closed AcquisitionPage/ResourceRequest and shared interaction contracts; command/path owners; early accessibility and handoff fixtures."
        ],
        "acceptance_criteria": [
          "Publication remains a recurring communication promise; an AcquisitionPage revision references it rather than replacing it.",
          "One Organization and brand isolation remain mandatory; no customer billing, external tenant provisioning, general CMS or generic connector designer.",
          "Define new/returning operator and human-agent handoff test cases before UI implementation."
        ],
        "acceptance_ids": [
          "AC-IP02",
          "AC-IP04",
          "AC-IP05",
          "AC-IP15"
        ]
      }
    },
    {
      "id": "WP-02",
      "reason": "A complete isolated application requires reproducible local processes, data, storage and deterministic adapters.",
      "replace": {},
      "append": {
        "allowed_paths": [
          "tests/dev",
          "docs/development"
        ],
        "expected_outputs": [
          "Repeatable pnpm dev:synthetic, synthetic:stop, synthetic:reset and test:synthetic commands; web and worker, PostgreSQL, Mailpit, isolated resource/journal storage and deterministic AI/provider/Kit fixtures."
        ],
        "acceptance_criteria": [
          "Synthetic mode denies real egress/effects, accepts only synthetic identities/data and requires no external account, credential, paid infrastructure or model.",
          "Startup, graceful shutdown, restart and explicit synthetic-only reset are tested; reset refuses any non-synthetic environment."
        ],
        "acceptance_ids": [
          "AC-IP01",
          "AC-IP16"
        ]
      }
    },
    {
      "id": "WP-07",
      "reason": "Journal and resource storage share infrastructure ports only, never safety-record ownership.",
      "replace": {},
      "append": {
        "acceptance_criteria": [
          "Synthetic independent journal failure/replay is testable without purchased storage; resource assets cannot overwrite journal objects or supply restrictive-event authority."
        ]
      }
    },
    {
      "id": "WP-10",
      "reason": "Requested resources and native pages need versioned content and a bounded asset port.",
      "replace": {},
      "append": {
        "allowed_paths": [
          "packages/adapters/assets"
        ],
        "expected_outputs": [
          "Versioned resource/asset manifests, storage port and isolated local fake; deterministic safe page blocks reusable by acquisition; resource availability/type/size validation and approved access policy."
        ],
        "acceptance_criteria": [
          "ADR-0005 editor/EmailDocumentCodec remains controlling for email; page documents do not become canonical email or Publication objects.",
          "Changing or removing an approved resource invalidates affected unpublished/stale acquisition revisions; safe asset references cannot execute scripts or fetch arbitrary URLs."
        ],
        "acceptance_ids": [
          "AC-IP02",
          "AC-IP03",
          "AC-IP05"
        ]
      }
    },
    {
      "id": "WP-12",
      "reason": "Owner requires Texenda-owned signup/thank-you pages and end-to-end confirmation/resource fulfillment.",
      "replace": {
        "title": "Implement native acquisition pages, confirmation, fulfillment and staged imports",
        "dependencies": [
          "WP-03",
          "WP-04",
          "WP-05",
          "WP-07",
          "WP-10",
          "WP-11"
        ],
        "scope": "Texenda-owned fixed-layout signup and thank-you authoring/preview/publication/versioning; property-scoped forms, disclosures, confirmation, requested-resource delivery through shared effects; abuse protection; staged field-mapped imports/exports."
      },
      "append": {
        "allowed_paths": [
          "apps/web/acquisition",
          "packages/persistence/acquisition",
          "tests/acquisition/pages",
          "tests/acquisition/fulfillment"
        ],
        "expected_outputs": [
          "AcquisitionPage definition/revisions and public renderer with atomic publish/unpublish, last-good revision and visible success/held/failure state.",
          "Idempotent verified ResourceRequest/fulfillment through existing delivery commands; public endpoints cannot grant unrelated marketing.",
          "Explicit per-field absent/blank/value mapping and historical no-trigger import previews."
        ],
        "acceptance_criteria": [
          "Only fixed accessible brand-aware signup/thank-you layouts; no general site builder, blog, newsletter archive, arbitrary scripting or replacement CMS.",
          "Publication/purpose and disclosure revisions are pinned; page publication/domain changes remain separately approved external effects.",
          "Missing assets, failed/unknown delivery, repeated request, expired link, stale confirmation and abuse have visible bounded recovery without new consent.",
          "A supported standalone native page is required; existing-site linking/embedding is optional, not a substitute."
        ],
        "acceptance_ids": [
          "AC-IP02",
          "AC-IP03",
          "AC-IP11",
          "AC-IP15"
        ]
      }
    },
    {
      "id": "WP-13",
      "reason": "Human and agent discoverability and handoffs are part of the first UI, not a late parallel surface.",
      "replace": {
        "dependencies": [
          "WP-03",
          "WP-06",
          "WP-10",
          "WP-12",
          "WP-15"
        ]
      },
      "append": {
        "acceptance_criteria": [
          "Stable object URLs/revisions, semantic labels, keyboard focus, visible brand/context, pending approval and safe next actions exist in initial core views.",
          "Human editing and assistant/API proposals use the same objects and revision/conflict rules; normal manual operation is complete without a model."
        ],
        "acceptance_ids": [
          "AC-IP04",
          "AC-IP06",
          "AC-IP09"
        ]
      }
    },
    {
      "id": "WP-14",
      "reason": "Reuse must not inherit authority or delivery history.",
      "replace": {},
      "append": {
        "acceptance_criteria": [
          "Clone content/structure into fresh drafts only: no approval, frozen recipients, enrollment/cursor, delivery history, current schedule or activation is inherited.",
          "Newsletter/educational nurture needs no Offer/course/commerce object; approved external offer references do not fabricate buyer exclusions or revenue."
        ],
        "acceptance_ids": [
          "AC-IP05",
          "AC-IP06",
          "AC-IP14"
        ]
      }
    },
    {
      "id": "WP-15",
      "reason": "All interaction adapters share revision-bound previews and human-only approval.",
      "replace": {},
      "append": {
        "acceptance_criteria": [
          "Draft, pending, stale, approved, committed and uncertain states remain distinct across UI, built-in AI, external tools and computer use; approval is never inferred from conversational text.",
          "An external computer-use principal cannot use the delegating human session or challenge to approve its own effects."
        ],
        "acceptance_ids": [
          "AC-IP04",
          "AC-IP07",
          "AC-IP08",
          "AC-IP09"
        ]
      }
    },
    {
      "id": "WP-16",
      "reason": "Truthful metrics and reviewable hygiene must be visible in initial operation.",
      "replace": {},
      "append": {
        "acceptance_criteria": [
          "Unavailable commerce or event coverage displays unavailable/unknown, never zero revenue, inferred nonpurchase, causal lift or an automatic experiment winner.",
          "Provider/API/AI ceilings hold work without creating paid-tier entitlements or automatic upgrades."
        ],
        "acceptance_ids": [
          "AC-IP10",
          "AC-IP14"
        ]
      }
    },
    {
      "id": "WP-18",
      "reason": "Actual source discovery is separately authorized; documented API/MCP availability is not a grant.",
      "replace": {
        "activation": "DEFER UNTIL TRIGGERED",
        "triggers": "Exact owner-approved read-only Kit discovery scope, data-handling boundary and qualified extraction method; no write credentials or account connection inferred."
      },
      "append": {
        "acceptance_criteria": [
          "Inventory all status classes, complete pagination, source field absent/blank/value semantics, legacy opt-outs and every required live workflow.",
          "Exported definitions/content and entry timestamps are not per-recipient next-unsent-step evidence; unknown progress stays held.",
          "Kit MCP documentation does not establish read-only enforcement, account access, audit coverage or client/model privacy qualification."
        ],
        "acceptance_ids": [
          "AC-IP11",
          "AC-IP12"
        ]
      }
    },
    {
      "id": "WP-19",
      "reason": "Implement synthetic migration mechanics without requiring private source discovery; real cutover still requires WP-18.",
      "replace": {
        "dependencies": [
          "WP-12",
          "WP-14",
          "WP-07"
        ],
        "scope": "Implement and test MigrationUnit staging, fencing, restrictive reconciliation, source checkpoint and authority-transfer mechanics against synthetic Kit fixtures only. Real account topology and transfer qualification remain WP-18/WP-17/WP-20."
      },
      "append": {
        "acceptance_criteria": [
          "Completion proves synthetic mechanics only and cannot satisfy real AC-M/VAL-10 evidence.",
          "Absent field preserves; explicit blank follows reviewed field-specific preserve/clear/quarantine policy; positive permission is never inferred; historical imports emit no enrollment triggers."
        ],
        "acceptance_ids": [
          "AC-IP11",
          "AC-IP12",
          "AC-IP16"
        ]
      }
    },
    {
      "id": "WP-22",
      "reason": "A representative welcome/nurture set is core initial behavior.",
      "replace": {},
      "append": {
        "expected_outputs": [
          "Editable welcome and educational nurture recipes using one executor and prospective revisions."
        ],
        "acceptance_criteria": [
          "Recipe runs preserve progress across restart and edits; duplicate confirmation/import cannot restart welcome or imply purchaser exit without a qualified source."
        ],
        "acceptance_ids": [
          "AC-IP06",
          "AC-IP10",
          "AC-IP13"
        ]
      }
    },
    {
      "id": "WP-23",
      "reason": "Bounded automation and reviewable hygiene are included, not an optimization product.",
      "replace": {},
      "append": {
        "expected_outputs": [
          "Representative event-driven and reviewable re-engagement/sunset recipes with explicit eligibility, stopping rules and simulation."
        ],
        "acceptance_criteria": [
          "No automatic deletion/repermission or blanket resend based on nonopens; missing source coverage holds the affected condition."
        ],
        "acceptance_ids": [
          "AC-IP06",
          "AC-IP10",
          "AC-IP13"
        ]
      }
    },
    {
      "id": "WP-25",
      "reason": "Measure usability across operators, modalities and recovery; scores remain hypotheses.",
      "replace": {},
      "append": {
        "acceptance_criteria": [
          "Test new and returning users plus human-agent handoff, with prompting, review, correction and exceptional-handling effort counted.",
          "Preserve current navigation unless observed task evidence supports a separately reviewed change; safety/accessibility/consequence comprehension cannot be traded for fewer clicks."
        ],
        "acceptance_ids": [
          "AC-IP04",
          "AC-IP09",
          "AC-IP10"
        ]
      }
    },
    {
      "id": "WP-26",
      "reason": "Foundational interaction context should not wait for all portfolio dashboards and automation UX.",
      "replace": {
        "dependencies": [
          "WP-15",
          "WP-13"
        ]
      },
      "append": {
        "acceptance_criteria": [
          "Durable draft/object refs, scope and revision survive switching interaction method and session resumption; unsaved changes require explicit reconciliation."
        ],
        "acceptance_ids": [
          "AC-IP04",
          "AC-IP07"
        ]
      }
    },
    {
      "id": "WP-27",
      "reason": "Built-in contextual assistance is initial-product scope, with deterministic substitutes before real-model qualification.",
      "replace": {
        "dependencies": [
          "WP-26",
          "WP-15",
          "WP-40"
        ]
      },
      "append": {
        "expected_outputs": [
          "Integrated contextual assistant connected to the same command services and persistent objects as UI/tools, deterministic scripted AI adapter, error/outage/injection fixtures and later real-model evaluation packet."
        ],
        "acceptance_criteria": [
          "Creation/editing/explanation/recovery cross real application handlers, not static chat mockups; synthetic outputs are visibly labeled and cannot certify model quality.",
          "No model needed in the effect policy path; outage preserves complete manual workflows and approved deterministic execution.",
          "No autonomous sending/publication/spend, permission expansion or human-only approval."
        ],
        "acceptance_ids": [
          "AC-IP04",
          "AC-IP07",
          "AC-IP08",
          "AC-IP14"
        ]
      }
    },
    {
      "id": "WP-28",
      "reason": "Deliberate external-agent identity and approval separation are initial requirements.",
      "replace": {},
      "append": {
        "acceptance_criteria": [
          "Test separately attributable API and computer-use principals; no fallback to human cookies/tokens on failure.",
          "Coding roster qualification never qualifies product agents, credentials, model data processing or delegation."
        ],
        "acceptance_ids": [
          "AC-IP08",
          "AC-IP09"
        ]
      }
    },
    {
      "id": "WP-29",
      "reason": "Keep the integrated assistant dependency and use shared services, not a separate agent product.",
      "replace": {},
      "append": {
        "acceptance_criteria": [
          "Structured tools are preferred; all authorized reads, drafts, previews and approved execution return shared object revisions and receipts.",
          "No mandatory MCP implementation for the core API; each actually selected protocol/client needs exact qualification."
        ],
        "acceptance_ids": [
          "AC-IP04",
          "AC-IP08"
        ]
      }
    },
    {
      "id": "WP-30",
      "reason": "Preserve voice direction without making speech a prerequisite for the initial non-voice release.",
      "replace": {
        "activation": "DEFER UNTIL TRIGGERED",
        "triggers": "Owner explicitly selects the voice release profile; actual speech enablement additionally requires VAL-12 and all applicable current gates."
      },
      "append": {
        "acceptance_criteria": [
          "No always-on listening or conversational approval; voice is tested through its own selected profile and cannot block non-voice synthetic completeness."
        ]
      }
    },
    {
      "id": "WP-31",
      "reason": "Synthetic computer-use interface conformance precedes actual external-agent qualification.",
      "replace": {
        "scope": "Implement and exercise browser-isolated representative computer-use journeys against synthetic data and delegated identities; semantic/keyboard navigation, Inspect, stale state, stop and actual-result verification. Record scripted adapter tests separately from real-agent usability/qualification."
      },
      "append": {
        "acceptance_criteria": [
          "Verify resulting object/revision/receipt, not only successful clicks or an agent narrative.",
          "New/returning navigation and interrupted handoff recover; lost agents stop/reobserve; human-only approvals remain outside agent reach.",
          "A scripted driver proves UI contract only; real client/model behavior remains VAL-11 evidence before external access."
        ],
        "acceptance_ids": [
          "AC-IP04",
          "AC-IP08",
          "AC-IP09",
          "AC-IP10"
        ]
      }
    },
    {
      "id": "WP-32",
      "reason": "Make integrated synthetic acceptance explicit, independent of voice and external qualification.",
      "replace": {
        "title": "Qualify the integrated initial synthetic application",
        "dependencies": [
          "WP-24",
          "WP-25",
          "WP-27",
          "WP-29",
          "WP-31",
          "WP-39",
          "WP-40",
          "WP-41"
        ],
        "activation": "AUTHORITATIVE DECISION",
        "external_gates_for_activation": [],
        "scope": "Integrated synthetic acceptance of full human, built-in assistant, structured-agent, computer-use, native acquisition, newsletter/sequence/automation, interruption/recovery and operator-workflow contracts. Compile—not clear—the remaining real-provider/model/staging/production qualification packet.",
        "expected_outputs": [
          "Exact revision/configuration-bound initial-synthetic acceptance report covering AC-IP01 through AC-IP18; explicit actual vs simulated evidence and all remaining gate requirements."
        ],
        "acceptance_criteria": [
          "All initial-synthetic journeys execute end-to-end through persistent application and worker state; no major workflow remains a stub.",
          "Required safety and accessibility checks pass; target-operator usability and actual agent/model evaluation remain honestly NOT RUN until performed.",
          "Deterministic AI/fake-provider success cannot clear VAL-09/11 or claim production readiness; optional voice is excluded without waiving non-voice interaction safety."
        ]
      },
      "append": {
        "acceptance_ids": [
          "AC-IP01",
          "AC-IP02",
          "AC-IP03",
          "AC-IP04",
          "AC-IP05",
          "AC-IP06",
          "AC-IP07",
          "AC-IP08",
          "AC-IP09",
          "AC-IP10",
          "AC-IP11",
          "AC-IP12",
          "AC-IP13",
          "AC-IP14",
          "AC-IP15",
          "AC-IP16",
          "AC-IP17",
          "AC-IP18"
        ]
      }
    },
    {
      "id": "WP-39",
      "reason": "Build deployment/runbook mechanisms locally; purchased infrastructure is a later qualification responsibility.",
      "replace": {
        "scope": "Implement pinned deployment configuration, ordered migrations, runtime liveness, independent send fence, backup/key/restore procedures and incident ownership contracts using isolated local infrastructure. Prepare managed-host selection evidence; no purchasing/provisioning or actual-host qualification required for synthetic completion.",
        "expected_outputs": [
          "Locally exercised deployment/rollback/restore/incident procedures and configuration templates; explicit real-host qualification checklist for WP-17/VAL-05."
        ]
      },
      "append": {
        "acceptance_criteria": [
          "Synthetic operations never claim actual hosting/PITR/durability, availability, real alert delivery or purchased retention; those are required later evidence."
        ],
        "acceptance_ids": [
          "AC-IP01",
          "AC-IP13",
          "AC-IP16",
          "AC-IP17"
        ]
      }
    },
    {
      "id": "WP-41",
      "reason": "Separate synthetic failure/restore proof from purchased host and production workload qualification.",
      "replace": {
        "scope": "Run isolated restore, journal, accepted-before-crash and workload failure drills on synthetic fixtures; measure local recovery and preserve post-backup restrictions. Prepare exact nonproduction/production infrastructure repetitions for WP-17 and VAL-05.",
        "acceptance_criteria": [
          "No accepted effect blindly resent after restored synthetic DB loss; current denials/erasures survive recovery.",
          "Local RPO/RTO and workload measurements are labeled local; actual planned workload and purchased-host recovery evidence remain required before production.",
          "Synthetic journal/backup failure and cancellation retain safe holds and a repeatable resumption path."
        ]
      },
      "append": {
        "acceptance_ids": [
          "AC-IP13",
          "AC-IP16",
          "AC-IP17"
        ]
      }
    },
    {
      "id": "WP-17",
      "reason": "First production release is the complete integrated product; real integration/staging/production qualification is separate from synthetic acceptance.",
      "replace": {
        "title": "Qualify real integrations, staging and the initial production release",
        "dependencies": [
          "WP-14",
          "WP-16",
          "WP-18",
          "WP-19",
          "WP-32",
          "WP-39",
          "WP-40",
          "WP-41"
        ],
        "external_gates_for_activation": [
          "VAL-02",
          "VAL-03",
          "VAL-04",
          "VAL-05",
          "VAL-06",
          "VAL-08",
          "VAL-09",
          "VAL-10",
          "VAL-11"
        ],
        "scope": "After initial-synthetic completion, qualify exact AI/provider/client contracts, authorized nonproduction accounts and production-connected staging; repeat actual infrastructure, security, privacy, usability, recovery and migration qualification; assemble signed initial-production release evidence. Preparatory qualification and release approval do not activate production.",
        "expected_outputs": [
          "Revision/configuration/account/model/region-bound qualification packets for existing gates; independently reviewed production acceptance, bounded canary/activation plan and accountable owner sign-off."
        ]
      },
      "append": {
        "acceptance_criteria": [
          "Built-in contextual AI, structured external-agent and representative actual computer-use evaluations are qualified for initial production; no manual-only email pilot is called the first usable product.",
          "All applicable real AC-D/S/L/W/C/A/R/M/P/O and non-voice AC-I criteria need actual required evidence; synthetic analogues alone cannot pass them.",
          "Production activation, public page publication/DNS, paid resources and data access require separate current approvals; VAL-01 or accepted neutral identity applies before public branding."
        ],
      "acceptance_ids": [
          "AC-IP17"
        ]
      }
    },
    {
      "id": "WP-20",
      "reason": "Production activation/rollout cannot bypass the integrated initial release or real AI/agent gates.",
      "replace": {
        "external_gates_for_activation": [
          "VAL-02",
          "VAL-04",
          "VAL-05",
          "VAL-08",
          "VAL-10",
          "VAL-09",
          "VAL-11"
        ]
      },
      "append": {
        "acceptance_criteria": [
          "Require the initial-production profile for first activation; exact owner activation scope is separate from readiness and remains revocable.",
          "Retain live legacy opt-outs, no dual send authority, repair-forward recovery, ongoing incident/support ownership and applicable observation periods."
        ],
        "acceptance_ids": [
          "AC-IP17",
          "AC-IP18"
        ]
      }
    },
    {
      "id": "WP-33",
      "reason": "Production activation/rollout cannot bypass the integrated initial release or real AI/agent gates.",
      "replace": {
        "external_gates_for_activation": [
          "VAL-02",
          "VAL-04",
          "VAL-05",
          "VAL-08",
          "VAL-10",
          "VAL-09",
          "VAL-11"
        ]
      },
      "append": {
        "acceptance_criteria": [
          "Require the initial-production profile for first activation; exact owner activation scope is separate from readiness and remains revocable.",
          "Retain live legacy opt-outs, no dual send authority, repair-forward recovery, ongoing incident/support ownership and applicable observation periods."
        ],
        "acceptance_ids": [
          "AC-IP17",
          "AC-IP18"
        ]
      }
    },
    {
      "id": "WP-42",
      "reason": "Production activation/rollout cannot bypass the integrated initial release or real AI/agent gates.",
      "replace": {
        "external_gates_for_activation": [
          "VAL-02",
          "VAL-03",
          "VAL-04",
          "VAL-05",
          "VAL-06",
          "VAL-08",
          "VAL-10",
          "VAL-09",
          "VAL-11"
        ]
      },
      "append": {
        "acceptance_criteria": [
          "Require the initial-production profile for first activation; exact owner activation scope is separate from readiness and remains revocable.",
          "Retain live legacy opt-outs, no dual send authority, repair-forward recovery, ongoing incident/support ownership and applicable observation periods."
        ],
        "acceptance_ids": [
          "AC-IP17",
          "AC-IP18"
        ]
      }
    },
    {
      "id": "WP-34",
      "reason": "Do not confuse native acquisition surfaces with speculative additional marketing channels.",
      "replace": {
        "activation": "DEFER UNTIL TRIGGERED",
        "triggers": "Observed recurring onsite job not served by native acquisition pages; privacy/maintenance/value evidence and owner-selected onsite profile."
      },
      "append": {}
    },
    {
      "id": "WP-35",
      "reason": "Do not confuse native acquisition surfaces with speculative additional marketing channels.",
      "replace": {
        "activation": "DEFER UNTIL TRIGGERED",
        "triggers": "One explicitly requested opted-in push use case, audience/channel permission, provider/cost/operations evidence and owner-selected push profile."
      },
      "append": {}
    }
  ],
  "acceptance_extensions": [
    {
      "id": "AC-IP01",
      "title": "Runnable isolated system",
      "work_packages": [
        "WP-02",
        "WP-39"
      ],
      "sealed_criteria": [
        "AC-S05",
        "AC-R01"
      ],
      "scenario": "Start web and worker, authenticate representative roles, persist synthetic data; stop, restart and explicitly reset.",
      "pass_condition": "Documented synthetic commands work from a clean environment; reset refuses real environments; denied real egress/credentials and persistent worker state are proved.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP02",
      "title": "Native page lifecycle",
      "work_packages": [
        "WP-10",
        "WP-12"
      ],
      "sealed_criteria": [
        "AC-D03",
        "AC-S03",
        "AC-S04"
      ],
      "scenario": "Author, preview, approve, publish, revise, unpublish signup/thank-you layouts on synthetic local origins.",
      "pass_condition": "Texenda owns versioned pages; atomic last-good behavior, pinned brand/publication/disclosure, visible success/held/error, keyboard/accessibility and no arbitrary script/CMS/archive are proved.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP03",
      "title": "Requested-resource fulfillment",
      "work_packages": [
        "WP-10",
        "WP-11",
        "WP-12"
      ],
      "sealed_criteria": [
        "AC-D03",
        "AC-L06",
        "AC-L07"
      ],
      "scenario": "Request and confirm where appropriate, deliver a resource; repeat, expire, remove asset, fail storage/provider and retry.",
      "pass_condition": "Resource access never creates unrelated marketing permission; verified request/purpose gates, bounded dedup/abuse limits and current denial checks apply through shared effects; unknown outcome never blind-retries.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP04",
      "title": "Integrated multimodal handoff",
      "work_packages": [
        "WP-01",
        "WP-13",
        "WP-15",
        "WP-25",
        "WP-26",
        "WP-27",
        "WP-29",
        "WP-31"
      ],
      "sealed_criteria": [
        "AC-I01",
        "AC-I02",
        "AC-I03",
        "AC-I04",
        "AC-I19"
      ],
      "scenario": "Create/edit/explain/recover one newsletter and one automation using manual UI, contextual assistant, structured tools and computer use.",
      "pass_condition": "All use persistent shared objects/commands/approvals/results; draft/context/revision survive handoff and interruption; no chat-only state, unimplemented path or hidden authority.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP05",
      "title": "Fresh draft cloning",
      "work_packages": [
        "WP-10",
        "WP-14",
        "WP-22"
      ],
      "sealed_criteria": [
        "AC-W05",
        "AC-A03"
      ],
      "scenario": "Clone a previously approved/sent campaign or recipe and adapt brand, dates and content.",
      "pass_condition": "New draft/identities only; no inherited approval, recipient snapshot, schedule activation, enrollment/cursor or delivery/effect history; source history untouched; new effects require fresh review.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP06",
      "title": "Complete core manual journeys",
      "work_packages": [
        "WP-06",
        "WP-13",
        "WP-14",
        "WP-22",
        "WP-23"
      ],
      "sealed_criteria": [
        "AC-D07",
        "AC-W01",
        "AC-W02",
        "AC-I18"
      ],
      "scenario": "Acquire a synthetic subscriber, create a no-offer newsletter, select audience, schedule/approve/cancel, run welcome/nurture and bounded automation with AI disabled.",
      "pass_condition": "Complete user/worker state transitions and meaningful outputs exist; no commerce setup, unqualified purchase exit or model required; no workflow stub passes.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP07",
      "title": "Stale and ambiguous intent",
      "work_packages": [
        "WP-15",
        "WP-26",
        "WP-27"
      ],
      "sealed_criteria": [
        "AC-I02",
        "AC-I03",
        "AC-I08",
        "AC-I27"
      ],
      "scenario": "Race manual edits with old model/tool proposals; switch brands; interrupt streaming; supply ambiguous consequential intent.",
      "pass_condition": "No overwrite/silent rebase or commit of provisional text; explicit conflict/clarification and resumable draft; material change invalidates approval.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP08",
      "title": "Agent authority and hostile inputs",
      "work_packages": [
        "WP-15",
        "WP-27",
        "WP-28",
        "WP-29",
        "WP-31"
      ],
      "sealed_criteria": [
        "AC-A02",
        "AC-A05",
        "AC-I10",
        "AC-I11",
        "AC-I12",
        "AC-I13",
        "AC-I14"
      ],
      "scenario": "Inject hostile research/content/model output, invalid schemas, expired/revoked/wrong-scope grants; exhaust time/rate/cost; try human approval bypass.",
      "pass_condition": "Server scopes precede data access; no grants/secrets/raw provider access, autonomous send/publication/spend or human-only approval; bounded correction then manual fallback; attribution/receipts remain exact.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP09",
      "title": "Deliberate computer use and accessibility",
      "work_packages": [
        "WP-13",
        "WP-25",
        "WP-31"
      ],
      "sealed_criteria": [
        "AC-I15",
        "AC-I16",
        "AC-I17",
        "AC-I29"
      ],
      "scenario": "Navigate representative audience/newsletter/acquisition/sequence/recovery tasks with semantic/keyboard paths and constrained browser principal.",
      "pass_condition": "Stable references/focus/labels, no hidden privileges, verify actual objects/results; lost session stops; agent cannot inherit human cookie/session or satisfy independent approval; scripted evidence not mislabeled actual-agent qualification.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP10",
      "title": "Operator burden and hygiene",
      "work_packages": [
        "WP-16",
        "WP-22",
        "WP-23",
        "WP-25",
        "WP-31"
      ],
      "sealed_criteria": [
        "AC-O07",
        "AC-I25",
        "AC-I26",
        "AC-I30"
      ],
      "scenario": "Run new-user, returning-user, human-only and agent-assisted tasks including reviewable re-engagement and exceptional recovery.",
      "pass_condition": "Record prompting, review, correction, navigation, errors, consequence comprehension and recovery effort; research scores remain hypotheses; no open-only sunset, automatic erasure/repermission, or unsafe simplicity tradeoff.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP11",
      "title": "Import mapping and extraction coverage",
      "work_packages": [
        "WP-12",
        "WP-18",
        "WP-19"
      ],
      "sealed_criteria": [
        "AC-M02",
        "AC-M03"
      ],
      "scenario": "Use all source statuses, every cursor page and absent/blank/value fixtures; replay historical imports.",
      "pass_condition": "Reconciled counts, explicit per-field preserve/clear/quarantine policy; unknown consent held; restrictions cannot weaken; no duplicate or enrollment triggers. Actual source proof stays separate.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP12",
      "title": "Required source workflow continuity",
      "work_packages": [
        "WP-18",
        "WP-19",
        "WP-20"
      ],
      "sealed_criteria": [
        "AC-M04",
        "AC-M05",
        "AC-M06",
        "AC-M09"
      ],
      "scenario": "Inventory source programs, definitions/content, recipient progress, stop controls and legacy opt-outs; exercise synthetic hold/drain/transfer.",
      "pass_condition": "Content/entry time never substitutes for next-unsent-step proof. Every required source behavior has recreate/drain/verified-resume/approved-retire/hold disposition; no dual send or unsupported full-retirement claim.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP13",
      "title": "Durable failures and recovery",
      "work_packages": [
        "WP-07",
        "WP-11",
        "WP-21",
        "WP-23",
        "WP-39",
        "WP-41"
      ],
      "sealed_criteria": [
        "AC-L07",
        "AC-L09",
        "AC-W08",
        "AC-W09",
        "AC-R01",
        "AC-R03",
        "AC-R06"
      ],
      "scenario": "Crash at transaction/journal/acceptance/wait boundaries; race cancellation/withdrawal; restore old DB and lose callbacks.",
      "pass_condition": "One cursor/effect identity; atomic wait winner; current denials/erasures and consumed/uncertain effects survive; outbound stays fenced until explicit recovery; repeatable safe resume.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP14",
      "title": "Truthful outputs and sources",
      "work_packages": [
        "WP-14",
        "WP-16",
        "WP-27"
      ],
      "sealed_criteria": [
        "AC-D08",
        "AC-A06"
      ],
      "scenario": "Show stale or missing commerce/engagement data, noisy opens and simulated model/provider results.",
      "pass_condition": "Unavailable/unknown is visible, never fabricated purchase/revenue/causal lift or forced winner; counts/denominators/revisions/actors/coverage cited; proposed vs approved vs committed distinct.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP15",
      "title": "Bounded product and data ownership",
      "work_packages": [
        "WP-01",
        "WP-03",
        "WP-12",
        "WP-24"
      ],
      "sealed_criteria": [
        "AC-D01",
        "AC-S01",
        "AC-S02"
      ],
      "scenario": "Inspect schema/route/module ownership and attempt cross-brand/public operator access.",
      "pass_condition": "One Organization and workspace/publication/consent semantics retained; public recipient endpoints never provision operators; no billing/tenancy/CMS/general connector subsystem; assets/pages do not redefine Publication.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP16",
      "title": "Synthetic evidence boundary",
      "work_packages": [
        "WP-02",
        "WP-19",
        "WP-32",
        "WP-39",
        "WP-41"
      ],
      "sealed_criteria": [
        "AC-S05"
      ],
      "scenario": "Complete the initial-synthetic dependency closure with no Kit access, paid infrastructure, live provider/model, production data or activation.",
      "pass_condition": "Every required WP and journey has scoped evidence; deterministic fakes prove integration/failure handling only; no external gate/real AC is cleared by synthetic evidence; no major workflow remains stubbed.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP17",
      "title": "Real qualification and staging",
      "work_packages": [
        "WP-17",
        "WP-18",
        "WP-39",
        "WP-41"
      ],
      "sealed_criteria": [
        "AC-O01",
        "AC-O03",
        "AC-O04",
        "AC-O06",
        "AC-O08"
      ],
      "scenario": "Under separate authority qualify actual AI/agent/email/storage/host services in nonproduction and rehearse release, rollback, recovery and migration.",
      "pass_condition": "Bind revision/configuration/accounts/regions/provider/model/protocol versions, terms, quota/budget, credentials, callbacks, actual workload/restore, accessible operator and real-agent results; retain failures/NOT RUN; no synthetic substitution.",
      "evidence_status": "NOT_RUN"
    },
    {
      "id": "AC-IP18",
      "title": "Release, activation and operation",
      "work_packages": [
        "WP-17",
        "WP-20",
        "WP-33",
        "WP-42"
      ],
      "sealed_criteria": [
        "AC-M06",
        "AC-M09",
        "AC-O01",
        "AC-O02",
        "AC-O05",
        "AC-O08"
      ],
      "scenario": "Approve exact initial-production release, then separately authorize canary/cutover/public pages and observe/support ongoing operation.",
      "pass_condition": "Applicable gates and current owner approvals required; production readiness is not activation; independent alert/support/incident/restore owners tested; restrictions/legacy links survive; pause/repair forward; no unqualified rollout or optional-channel claim.",
      "evidence_status": "NOT_RUN"
    }
  ],
  "additional_profiles": [
    {
      "id": "initial-synthetic",
      "parents": [],
      "requires_work_packages": [
        "WP-01",
        "WP-02",
        "WP-03",
        "WP-04",
        "WP-05",
        "WP-06",
        "WP-07",
        "WP-08",
        "WP-09",
        "WP-10",
        "WP-11",
        "WP-12",
        "WP-13",
        "WP-14",
        "WP-15",
        "WP-16",
        "WP-19",
        "WP-21",
        "WP-22",
        "WP-23",
        "WP-24",
        "WP-25",
        "WP-26",
        "WP-27",
        "WP-28",
        "WP-29",
        "WP-31",
        "WP-32",
        "WP-39",
        "WP-40",
        "WP-41"
      ],
      "required_criteria": [
        "AC-IP01",
        "AC-IP02",
        "AC-IP03",
        "AC-IP04",
        "AC-IP05",
        "AC-IP06",
        "AC-IP07",
        "AC-IP08",
        "AC-IP09",
        "AC-IP10",
        "AC-IP11",
        "AC-IP12",
        "AC-IP13",
        "AC-IP14",
        "AC-IP15",
        "AC-IP16"
      ],
      "requires_gates": [],
      "scope": "Complete integrated application on synthetic data; real model/provider/agent quality and all external gates remain unverified.",
      "evidence_mode": "synthetic"
    },
    {
      "id": "initial-production",
      "parents": [
        "initial-synthetic"
      ],
      "requires_work_packages": [
        "WP-17",
        "WP-18"
      ],
      "required_criteria": [
        "AC-D01",
        "AC-D02",
        "AC-D03",
        "AC-D04",
        "AC-D05",
        "AC-D06",
        "AC-D07",
        "AC-D08",
        "AC-D09",
        "AC-D10",
        "AC-S01",
        "AC-S02",
        "AC-S03",
        "AC-S04",
        "AC-S05",
        "AC-L01",
        "AC-L02",
        "AC-L03",
        "AC-L04",
        "AC-L05",
        "AC-L06",
        "AC-L07",
        "AC-L08",
        "AC-L09",
        "AC-L10",
        "AC-C01",
        "AC-C02",
        "AC-C03",
        "AC-C04",
        "AC-C05",
        "AC-C06",
        "AC-R01",
        "AC-R02",
        "AC-R03",
        "AC-R04",
        "AC-R05",
        "AC-R06",
        "AC-M01",
        "AC-M02",
        "AC-M03",
        "AC-M04",
        "AC-M05",
        "AC-M06",
        "AC-M07",
        "AC-M08",
        "AC-M09",
        "AC-P01",
        "AC-P02",
        "AC-P03",
        "AC-P04",
        "AC-P05",
        "AC-P06",
        "AC-P07",
        "AC-P08",
        "AC-O01",
        "AC-O02",
        "AC-O03",
        "AC-O04",
        "AC-O05",
        "AC-O06",
        "AC-O07",
        "AC-O08",
        "AC-W01",
        "AC-W02",
        "AC-W03",
        "AC-W04",
        "AC-W05",
        "AC-W06",
        "AC-W07",
        "AC-W08",
        "AC-W09",
        "AC-W10",
        "AC-W11",
        "AC-W12",
        "AC-A01",
        "AC-A02",
        "AC-A03",
        "AC-A04",
        "AC-A05",
        "AC-A06",
        "AC-I01",
        "AC-I02",
        "AC-I03",
        "AC-I04",
        "AC-I05",
        "AC-I06",
        "AC-I07",
        "AC-I08",
        "AC-I09",
        "AC-I17",
        "AC-I18",
        "AC-I19",
        "AC-I24",
        "AC-I25",
        "AC-I26",
        "AC-I27",
        "AC-I28",
        "AC-I30",
        "AC-I10",
        "AC-I11",
        "AC-I12",
        "AC-I13",
        "AC-I14",
        "AC-I15",
        "AC-I16",
        "AC-I29",
        "AC-IP17"
      ],
      "requires_gates": [
        "VAL-02",
        "VAL-03",
        "VAL-04",
        "VAL-05",
        "VAL-06",
        "VAL-08",
        "VAL-09",
        "VAL-10",
        "VAL-11"
      ],
      "scope": "Exact integrated initial product qualified for its intended production use; separate public-brand clearance/neutral identity and activation authority still required.",
      "evidence_mode": "real-qualified"
    }
  ],
  "profile_updates": [
    {
      "id": "email-pilot",
      "replace": {
        "parents": [
          "initial-production"
        ],
        "scope": "Bounded transport/cutover canary within the integrated initial-production release; no longer an independently sufficient first usable product."
      },
      "append": {}
    }
  ],
  "synthetic_forbidden_dependencies": [
    "WP-17",
    "WP-18",
    "WP-20",
    "WP-30",
    "WP-33",
    "WP-34",
    "WP-35",
    "WP-36",
    "WP-37",
    "WP-38",
    "WP-42",
    "WP-43"
  ],
  "evidence_rule": "AC-IP synthetic exercises referencing sealed criteria are supplemental analogues, not passing real-environment proof. Each AC-IP case is scoped to its exercised stage; real portions of AC-IP11/12 await WP-18/20. Existing applicable acceptance/gates must pass independently for the exact production revision/environment.",
  "coordinator_boundary": {
    "base_state_version": "2.0",
    "active_state_version": "2.1",
    "activation": "explicit_reviewed_forward_receipt_only",
    "preserve_sealed_catalog_digest": true,
    "preserve_routing_policy_and_roster": true,
    "preserve_prior_events_tasks_and_evidence": true,
    "implicit_activation": false,
    "old_lifecycle_reader": "fails_closed",
    "old_context": "unbound_sealed_context_is_not_valid_dispatch",
    "future_tasks": "bind_effective_plan_digest",
    "fallback": "preserve_checkpoint_and_repair_forward_no_history_rewrite"
  }
}
```
