# Integrated initial-product implementation path

Navigation and execution guidance, not a second plan or permission source.
[ADR-0008](../decisions/ADR-0008-integrated-initial-product-and-effective-plan.md)
owns the exact deltas, acceptance extensions and release profiles. Unchanged
[sealed topic owners](../../specs/texenda-handoff/01-foundation/authority-register.json)
remain controlling. Product implementation and all acceptance results are still
unperformed; this planning update builds no application.

## Ordinary entry

Start at canonical `repo/` with [AGENTS.md](../../AGENTS.md). Read the active
ignored binding and deliberately set the verified absolute state root:

```sh
env GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
env GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/plan.py --check --root .
env GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda --read-only status
env GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 python3 -B tooling/coordination/harness.py --root . --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda --read-only ready
```

From the project home, first `cd repo`. On another machine, use the exact verified
local binding instead of copying this machine's paths. A candidate worktree uses
`env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --scope code --all`;
live inspection always invokes the canonical script and root as explained in
[START_HERE](../../.agent/START_HERE.md). Never copy a ledger or binding.

Select an ID from fresh ready output; obtain its context and follow the
[assignment](../../tooling/coordination/templates/ASSIGNMENT.md),
[review](../../tooling/coordination/templates/REVIEW.md) and
[resumption](../../tooling/coordination/templates/RESUME.md) contracts.
The historical sealed catalog digest and activated effective-plan digest have
different meanings. An old sealed-only or unactivated context is not an amended
assignment. Ready/context do not admit work or authorize external effects.

Initial amended-plan assignments use max effort on qualified subscription routes.
Historical downshift/API-budget records cannot authorize enlarged scope. Future
plan-bound support has a precise trigger in RAIDQ-0025; this restriction does not
mean qualified high/medium profiles vanished, and product-AI budgets stay separate.

After plan activation, WP-01 is the first ordinary implementation unit. WP-18
waits for explicit read-only source discovery evidence. This does not prevent
synthetic migration mechanics under WP-19. No new product WP is completed by
planning or plan activation.

## What the first complete synthetic application must do

One isolated application runs a user-facing web process and durable workers,
with persistent PostgreSQL data, representative human/agent authorization,
isolated storage, captured mail, simulated callbacks and deterministic AI/provider
adapters. It must support:

- A new operator finding the right brand, creating/editing/previewing work,
  understanding consequences and approving in a separate authorized context.
- Contextual built-in assistance creating, editing, explaining and helping
  recover the same persistent objects that the manual UI operates.
- Structured external-agent operation and deliberate semantic/keyboard/computer-use
  journeys with restricted identities and actual resulting-state checks.
- Native signup/thank-you authoring, versioned publishing, forms/disclosures,
  confirmation and requested-resource delivery, including failures and repeat requests.
- Audience selection, no-offer newsletters, schedules/cancellation, fresh-draft
  reuse, welcome/nurture, reviewable hygiene and approved bounded automations.
- Truthful results, unavailable-source explanations, current restrictions,
  duplicate prevention, bounded retry, uncertain acceptance, interruption,
  restore and safe resumption.

A fake AI adapter must drive the actual context/proposal/command/result pipeline;
a canned chat page is not completion. A scripted browser driver proves interface
conformance, not an actual agent's ability. Real-model quality, actual client
behavior and observed operator usability have separate qualification evidence.

WP-02 must implement these future product commands:
`pnpm dev:synthetic`, `pnpm synthetic:stop`, `pnpm synthetic:reset`,
and `pnpm test:synthetic`. They are **not available today**. Reset must refuse
non-synthetic environments; no command may discover live credentials or silently
switch transports. All approved deterministic workflows remain usable without AI.

## Dependency order

This table groups work for understanding. The coordinator's composed catalog,
not this table, owns exact dependencies and allowed paths.

| Milestone | Existing work packages | Required outcome |
|---|---|---|
| Contracts and isolated runtime | WP-01 → WP-02 | Shared commands/context, native page/resource ownership, early accessibility contracts, exact versions and no-effect development stack |
| Data and effects | WP-03–12 plus WP-15 in dependency order | Identity/permission, independent journal, ingress/provider fakes, rendering/assets, shared delivery, approvals and complete acquisition |
| Initial objects and interaction context | WP-13/14/26 | Manual UI, safe cloning and durable context before contextual assistance; no duplicate application for agents |
| Core behavior and independent safety | WP-16/19/21–24/40 | Honest metrics, synthetic transfer mechanics, sequences/automations, portfolio isolation and independent core security |
| Integrated experience and recovery | WP-25/27–29/31/39/41 | Built-in assistant, external delegation/tools, deliberate computer use, usability and local deployment/restore exercises |
| Complete synthetic acceptance | WP-32, `initial-synthetic` | Every required journey runs end-to-end; missing or stubbed core flows cannot pass |
| Real source/integration/staging qualification | Triggered WP-18 and WP-17 | Exact account/model/client/provider, migration evidence, realistic nonproduction configuration and actual operator/agent tests |
| Exact preactivation approval | WP-17, `initial-production` | Applicable real acceptance and current gates; signed release/configuration and ready operational responsibilities |
| Separate activation and sustained operation | WP-20 → applicable WP-33/42 | Authorized canary/cutover, observation, legacy opt-outs, ongoing incidents/support/restore and later scoped releases |

WP-29 retains WP-27 as a dependency: external-first/deferred-built-in advice is
superseded. The assisted-workspace component profile explicitly inherits
initial-production, not mature-email; external-agent still inherits
assisted-workspace. Their own checks/gates/WPs are unchanged, so enabled-profile
selection cannot reintroduce rollout as a prerequisite for initial AI operation.
Mature-email retains its later rollout; voice remains separately triggered.
WP-26 no longer waits for all later UX work; foundational interaction
and accessibility enter WP-01/13. WP-12 now waits for rendering/assets and shared
delivery. WP-19 no longer requires actual Kit discovery to implement/test synthetic
mechanics. WP-39/41 implement/exercise local mechanisms; actual infrastructure
qualification is explicitly repeated in WP-17. WP-32 excludes optional voice but
not integrated AI/agents/computer use.

No synthetic-release dependency requires real Kit access, a paid host, a real
model/provider, production data or cutover. This is a graph invariant, not a claim
that those future qualifications are unnecessary.

## External qualification and operating responsibilities

The [existing gate register](../../specs/texenda-handoff/01-foundation/external-validation-gates.json)
defines gates. The [RAIDQ owner](../../project-dossier/machine-readable/raidq.json)
contains exact blockers, evidence, triggers, next actions and recovery; references
below do not copy or clear them.

| Capability / transition | Local substitute or preparation | Real evidence and accountable route |
|---|---|---|
| Model assistance | Scripted AI success/error/ambiguity/injection fixtures | Exact model/provider data terms, quality/cost/outage and task evaluations; VAL-09; RAIDQ-0012 |
| External tools/computer use | Constrained synthetic principals, protocol fixtures, browser/keyboard result checks | Actual client identity/grants/revocation and human approval isolation; VAL-11/08; RAIDQ-0013 |
| Email / DNS / sender | MailProvider fake and Mailpit, simulated signed callbacks | Qualified Resend candidate account/region/use/limits, authenticated domains, headers, actual feedback and seed results; VAL-04; RAIDQ-0014 |
| Hosting / database / object storage / secrets / telemetry | Local containers, separate journal/assets, templates and failure drills | Qualified Render/managed PostgreSQL and S3-compatible candidates or reviewed alternatives; secret isolation, actual retention/keys/restore, alerts, workload and costs; VAL-05/08; RAIDQ-0015 |
| Kit/source migration | Synthetic all-status/page/field/cursor/fencing fixtures | Authorized read-only discovery, complete source coverage, required parity, exact continuity/holds, negative reconciliation and legacy opt-outs; VAL-10; RAIDQ-0011 |
| Public pages, data and legal sender | Local origins, synthetic disclosures/resource requests | Actual intended-use/privacy/retention/processor review and public identity; VAL-02 and VAL-01 or accepted neutral identity; RAIDQ-0016 |
| Usability/accessibility | Automated scenarios and synthetic test scripts | Actual routine operators, new/returning/handoff/correction burden, keyboard and screen-reader observations; VAL-06; RAIDQ-0017 |
| Dependencies and rendering | Locked versions, approved blocks, codec/render fixtures | Exact compatibility/licenses/SBOM and actual email-client fidelity; VAL-03/ADR-0005; RAIDQ-0018 |
| Activation and operation | Tested release/canary/incident/rollback procedures | Separate owner activation scope; reachable sending, migration, incident/support, privacy, billing and restore owners; WP-20/33/42; RAIDQ-0024 |

Production-connected staging uses separately approved nonproduction accounts and
realistic infrastructure, not live users/data. It tests actual callbacks, tokens,
quotas, service outages, deployment and operational controls that fakes cannot
prove. A provider name, SDK, installed coding model or passing local suite is not
qualification. No service is connected by this plan.

Initial-production approval is a preactivation decision. AC-IP18's actual
activation/observation evidence belongs afterward to WP-20/33/42; it does not make
readiness circular. Actual-transfer/observation AC-M04/05/06/07/09 likewise apply
at their rollout boundaries, not preactivation readiness. Email-pilot completion
requires WP-20 and retains all sealed migration criteria. Before approval, WP-17
requires actual inventory, dry-run and recovery rehearsal, continuity/holds and
transfer-readiness evidence; a scoped VAL-10 readiness attestation is not completed
cutover. WP-20 must prove actual source fencing before target handoff and retain
the remaining canary, legacy-link and observation checks. No approval permits self-authorized sending, domain publication,
account access or provisioning. Recheck expiry and actual configuration before
each effect boundary.

During operation, follow the existing [runbook owner](../../specs/texenda-handoff/04-security-governance-and-operations/runbooks.md):
retain restrictive intake and legacy opt-outs, pause uncertain work, reconcile
possible acceptances, and repair forward. Restoring a database cannot restore
old permission or erase already-consumed effects. Post-release response, billing,
maintenance, backup verification, restore drills and absence cover need named
accountable people, even if one person holds several roles.

## Intentional deferrals and authority

RAIDQ-0019 retains voice direction without always-on capture. RAIDQ-0020 covers
triggered channels; native acquisition pages are not an optional onsite channel.
RAIDQ-0021 covers named commerce/course/event/content sources, with required Kit
parity overriding hypothetical deferral. RAIDQ-0022 covers evidence-dependent
experiments/referrals/adaptive recommendations. RAIDQ-0023 retains measured
infrastructure triggers. Blueprint/direct-CLI/family/private-control issues remain
their existing separate RAIDQ records, not new prerequisites for synthetic work.

The [research disposition map](../qualification/analysis/research-impact-dispositions.json)
accounts for all sixteen findings from the preceding assessment. It is traceability,
not another requirements or task store. Both research packages and handoff variants
remain unchanged. AC-IP rows supplement existing acceptance under the same local
amendment route; they do not grant permissions or mark implementation tests passed.
