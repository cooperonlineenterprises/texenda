# Kit discovery: preparation for a future authorized inventory

Status: **PREPARATION ONLY; NO DISCOVERY, ACCOUNT CONNECTION OR PRODUCT TEST
EXECUTED.** No actual source accounts, exports, private inputs, status counts,
programs, source-control settings or recipient cursors were inspected. Empty
evidence below means missing evidence, not a zero count or successful check.

This checklist is subordinate to the sealed
[Kit migration owner](../../specs/texenda-handoff/06-migration-and-production/kit-migration.md),
the WP-18 amendment and AC-IP11/12 in
[ADR-0008](../decisions/ADR-0008-integrated-initial-product-and-effective-plan.md),
and existing [RAIDQ-0011](../../project-dossier/machine-readable/raidq.json).
Use the existing [MigrationUnit template](../../specs/texenda-handoff/06-migration-and-production/migration-unit.template.json)
and [acceptance catalog](../../specs/texenda-handoff/06-migration-and-production/acceptance-catalog.json),
not a second migration plan or readiness ledger. Source revision:
`79db6081dd929af3f46a1cc8e1eec5f8ac09e9cc`; preparation base:
`efaa8fa9772d332dd3bfb2b40bbae2110b06a5fa`. A governing-source change invalidates
the affected checklist until compared, regenerated and rechecked.

Accountable decision owner: Ryan, initially the founder/migration owner, with the
data owner as required by RAIDQ-0011. Before discovery, he must identify the
actual authorized extraction operator and any replacement migration owner.
This document appoints nobody and grants no account or data access.

## Trigger packet still needed

| Item | Required scope/evidence and next concrete action | Hold/fallback and risk |
|---|---|---|
| Current owner authorization | Identify exact account(s), publications/cohorts, read operations, purpose, operator, duration/expiry, output destination and prohibited effects. Obtain the explicit read-only WP-18 discovery grant. Account identifiers are not guessed here. | No connection/export until authorized. Continue synthetic foundations; account availability or a saved session is not permission. |
| Extraction method | Qualify the selected API/export/client/protocol and actual grant, endpoint/tool allowlist, enforced read-only scope, audit trail, pagination and completeness limitations. Document why it cannot mutate under that grant. | Kit MCP documentation or a visible connector is not proof of read-only enforcement, audit coverage, account access or client/model privacy. If adequate restriction cannot be established, hold and request an approved bounded alternative. |
| Data handling | Record the allowed metadata/PII fields, least-privilege readers, protected storage, retention/erasure, approved model exposure if any, redaction and evidence destination. Preserve raw authorized evidence separately from sanitized repository summaries. | Current preparation cannot inspect existing private inputs, even sizes/hashes. RAIDQ-0006 remains controlling for their handling; do not copy exports into Git, prompts or logs. |
| Inventory output contract | Use WP-18's allowed inventory/readers/fixture paths only after admission. Plan provenance, extraction timestamp/watermark, exact method/version, coverage gaps and authorized source checksums; bind each conclusion to its evidence. | A schema/template does not prove actual evidence. Report unknown/not observed and retain source programs. |
| Later control authority | Separately name who may freeze/drain, change intake, transfer epoch, run canary and restore service, with exact approved scope and current gates. | Discovery permission does not authorize operating pause/stop controls or proving cutover by changing settings. |

The immediate next action is to prepare the exact WP-18 trigger packet with Ryan:
named accounts/scopes, method and metadata/data-handling boundary. Nothing here
requires connecting an account now. WP-01 and isolated WP-12/19 fixtures can
proceed through their own authorized dependency order without Kit discovery.

## Read-only inventory checklist for that future grant

All rows are **NOT PERFORMED**. Source API descriptions in the sealed document
are dated context; actual account/version behavior must be established during
authorized discovery. No claim of current Kit API functionality is made here.

| Inventory area | Evidence to collect/reconcile | Decision or failure to expose |
|---|---|---|
| Topology and required programs | Account-to-brand/publication/purpose map; Property/forms/embeds/native landing paths; sender domains; tags/segments/custom fields; broadcasts/schedules; welcome/nurture sequences; event automations; integrations and every way a person enters, leaves or receives a message. Include required resource fulfillment and any actually used course/commerce/event behavior. | Mark which source behaviors are required for OHW replacement and later full retirement. Do not invent hypothetical integrations or treat a tag/form association as permission for a new Publication. |
| Coupling and parity | Shared forms, source-account restrictions, cross-publication automation effects, common cohorts and dependent integrations; definition/content version and intended trigger, eligibility, waits, exits, reentry, cadence, approved sender and maximum contacts for each required program. | Determine the smallest independently fenceable MigrationUnit or connected wave. Preserve separate audience/permission scopes within a wave. Map each required behavior to recreate, drain, verified resume, approved retire or hold, with owner/evidence. |
| Every status class | Explicit all-state extraction (including the sealed owner's `status=all` requirement where supported), actual names/definitions of active, pending/unconfirmed, unsubscribed/cancelled, bounced, complained, suppressed/blocked and every other source state exposed. Check additional endpoints/exports for exclusions absent from the list. | These are coverage categories to discover, not an assertion that Kit uses these exact labels. Reconcile account-wide versus publication-specific restrictions; active-only output cannot establish completeness. |
| Complete extraction | Start/end snapshot or watermark, filters, page size, every returned cursor, termination proof, repeated/missing pages, retry history, unique source IDs, totals per actual state and source/export totals. Record concurrent-change/delta coverage and inaccessible data. | Missing pages or unreconciled totals block a completeness claim. Duplicate pagination results are deduplicated by source identity without silently discarding conflicts. Webhooks supplement final reconciliation; they do not prove all changes were observed. |
| Field meaning | For each field, distinguish absent key, explicit blank, explicit value, invalid type and source-specific null. Retain submitted/source values and chosen normalization separately. Show created/updated/held/invalid/ambiguous preview counts and reason reports. | Absent preserves an existing value (or leaves a new value unset); explicit blank follows a reviewed field-specific preserve/clear/quarantine policy. Never treat blank as automatic clearing, affirmative permission or a substitute opt-in timestamp. |
| Permission and negative evidence | Actual disclosure/provenance/source identifiers/times and endpoint/publication/channel support; source account opt-outs, complaints, invalid endpoints, suppression and erasure facts; unresolved identity matches. | Unknown consent remains held; source active status alone cannot invent a grant. Restrictions retain their real scope and dominate positive upserts. Withdrawal and safety Suppression remain distinct. |
| Historical imports | Preview mappings and repeatable dry-run inputs; preserve source history/provenance and mark imported analytics as historical. Plan an idempotent replay demonstration under `trigger_mode=historical`. | No enrollment/event automation triggers from snapshot/replay; no duplicate membership/effect or weakened denial. Synthetic tests are early mechanics; actual dry-run evidence belongs to later qualification. |
| Legacy opt-outs | Actual old one-click URLs/capabilities, account-level unsubscribe scope, lifetime/key/account dependencies, signed-event coverage, polling/export fallback and negative-delta reconciliation. | Do not call an account-wide source unsubscribe operation to emulate a narrow publication stop. Keep source/legacy intake until actual continuity is verified; a new preference URL cannot rewrite delivered messages. |
| Source stop controls | Read-only inventory of actual controls for broadcasts, scheduled/in-flight sends, sequences, new enrollments, automations, forms and integrations; who can operate each, scope, known delay, evidence obtainable and coupled consequences. | A Texenda SendingAuthorityLease cannot fence Kit. Reading a “paused” setting is not a fresh freeze/drain test or proof all in-flight work is accounted for. Operating controls needs later authorization. |
| History and retirement | Required analytics/content/consent/history retention and intentional archive dispositions, support/privacy path, unresolved programs and long-lived link dependencies. | Definitions/content available is not execution continuity. Unresolved required programs or broken legacy restrictions prevent a claim of full migration or safe source-account retirement. |

## Per-subscriber continuity proof

For every required active enrollment, the later evidence packet must identify
the exact source program/version and recipient/enrollment, its ordered/stable
steps, and which relevant effects were accepted/sent, definitely not accepted,
cancelled, skipped or still uncertain. Retain evidence provenance and coverage,
the actual wait/due/exit context, and the target node/content/effect mapping.
The reviewed next-unsent step must follow that recipient-level evidence.

| Observed evidence situation | Permitted disposition to prepare | What it cannot establish |
|---|---|---|
| Definitions, email content, aggregate statistics and entry time only | Recreate the definition for future entrants; hold existing enrollments, or prepare an explicit retirement decision with recipient/operator impact. | No elapsed-days calculation, guessed next email, restart-from-first or arbitrary skip. Membership/`added_at` is not a cursor. |
| Verifiable recipient-level progress and complete compatible mapping | Prepare verified resume at a mapped node, retaining consumed/uncertain effects and current permission checks for later reviewed transfer. | Proof of progress does not itself stop the source or authorize target sending. |
| Source can safely finish a required program before transfer | Prepare a bounded drain disposition, source-only authority and final reconciliation evidence requirements. | No concurrent target copy of that program for the same function/cohort. |
| Source effects or next step remain uncertain | Hold/quarantine; preserve claims and source evidence. Escalate only the missing source fact or reviewed retirement decision. | No assertion of complete parity/full retirement. A timeout never authorizes a duplicate effect. |
| Owner approves retirement after impact review | Record exact program/cohort, reason, omitted future behavior, owner decision and retained restrictions/history. | Retirement cannot be backfilled from an agent recommendation or silently labeled successful completion. |

Use [PREP-CASE-0012](../implementation/preparation/synthetic-cases.md#prep-case-0012)
and sealed FX-11 for the no-cursor failure. Synthetic fixtures show how an
unproved cursor is held; only actual evidence can establish real continuity.

## Evidence and authorization boundaries after discovery

WP-18 records inventory and evidence availability. WP-19 implements synthetic
mechanics. WP-17 later requires real inventory/dry-run/recovery qualification,
verified continuity or explicit holds, and a reviewed transfer-readiness packet
under AC-M01/02/03/08 and the scoped VAL-10 readiness boundary.

Actual source freeze/drain and final negative reconciliation, signed authority
transfer, canary, legacy-link operation and observation remain separately
authorized WP-20/33 work. AC-M04/05/06/07/09 keep their actual-transfer meanings;
inventory does not pass them. Before target handoff, evidence must prove the
actual source controls stopped the relevant schedules/triggers and account for
in-flight accepted/cancelled/unknown effects. Never infer this from a target
lease, source definition export or read-only inventory.

The fallback is to retain required source programs and hold affected migration
units while continuing safe synthetic work. Failed canary means pause, preserve
restrictive intake, reconcile and repair forward. Returning sending to Kit is
another reviewed authority transfer with current negative-state/cursor/effect
reconciliation; an old export or a restored database is not rollback authority.
If the source cannot safely express exclusions/progress, keep sending paused.

Principal risks remain those in RAIDQ-0011: lost permission, repeated/missed
messages and broken legacy opt-outs. Track new evidence and unresolved facts in
that existing owner and the authorized WP-18 packet. This checklist creates no
new prerequisite for synthetic foundations and clears no gate.
