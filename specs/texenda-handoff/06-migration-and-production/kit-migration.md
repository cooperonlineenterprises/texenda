# Kit migration: fenced authority transfer

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal closure §16.3, retained without semantic change. Apply [package authority](../DECISION-STATUS.md).

### 16.3 Kit migration: evidence-led authority transfer

**Decision status: AUTHORITATIVE DECISION.** Migration is publication-by-publication **when the source can be independently fenced**. If shared Kit forms, account-wide states or automations make that unsafe, use the smallest connected migration wave that can be stopped and reconciled as a unit. This is a safety constraint, not permission to pool audiences.

Current Kit documentation defaults subscriber listing to `active`; the migration adapter must explicitly retrieve `status=all`, follow every returned cursor, and separately account for states or exclusions exposed only elsewhere. [S09](../09-reference/source-register.md#s09) Kit sequence membership includes entry time and subscriber state, but membership is not an exact per-email execution cursor. Definitions/content and aggregated sequence-email stats are available in current API documentation; they still do not establish what a particular person should receive next. [S10, S11](../09-reference/source-register.md#s10)

Kit's August 27, 2026 changelog introduces signed, batched Webhooks 2.0 with an incrementally available event catalogue. Validate actual event delivery for the account; do not assume every consent/progress transition is covered. Webhooks supplement final export/API reconciliation rather than replacing it. [S11](../09-reference/source-register.md#s11)

#### Migration records

Create a `MigrationUnit` with mapped source account(s), publications, forms, tags, segments, sender domains, current sequences/automations, subscriber cohorts, global/source-account restrictions, last extraction watermark, unsupported semantics and a complete authority matrix.

A `SendingAuthorityLease` identifies organization/brand/publication/channel/purpose/function and any explicit disjoint cohort, active system (`kit` or `texenda`), epoch, allowed interval and operator evidence. Normal migration uses one active system for the whole unit's marketing. Texenda checks the lease before every permit. A lease in Texenda cannot technically fence Kit; the migration gate requires observed source-side pause/disable controls and evidence that no scheduled/in-flight work remains unaccounted for.

#### Authority matrix

| Stage | Audience/consent authority | Acquisition write path | Broadcast/sequence/automation sending | Restrictive inputs | Historical analytics |
|---|---|---|---|---|---|
| Inventory/shadow | Kit for source state; Texenda is a non-sending replica with explicit provenance | Existing Kit forms/integrations | Kit only | Kit primary; mirrored restrictions retained, no Texenda grants | Kit original reports; imported observations labeled historical |
| Freeze/drain | Kit state frozen for permission-expanding writes; existing withdrawals still accepted | Controlled gateway/maintenance capture stages new requests without activating marketing | Kit new schedules/triggers paused; Texenda disabled; reconcile in-flight source work | Ingest from both surfaces into durable negative-evidence union | Snapshot/export retained |
| Final reconciliation | Final source snapshot plus restrictive delta log, reviewed in Texenda | New requests remain staged | Neither system issues new marketing | Both old Kit links and Texenda endpoints feed required restrictions | No fabricated metric parity |
| Commit/canary | Texenda effective audience/consent authority at new epoch | Texenda public endpoints; staged requests processed under current disclosure/proof rules | Texenda only, capped canary; Kit sending remains disabled | Texenda authoritative application of legacy and new restrictions | Texenda reports start; Kit history remains separately labeled |
| Observation | Texenda | Texenda | Texenda approved scope only | Legacy Kit opt-outs remain monitored/ingested | Side-by-side source labels, not summed duplicate events |
| Fully migrated | Texenda | Texenda | Texenda; all required source programs recreated/resolved | Texenda plus supported legacy-link intake for the required retention period | Required history migrated or intentionally archived |

#### Transfer protocol

1. **Discover and map.** Inventory actual source semantics and all ways a contact can enter, leave or be sent a message. A tag/form association is not automatically sufficient consent for an invented new publication.
2. **Extract every state.** Preserve source IDs, cancellation/suppression state, available evidence and extraction watermark. Include shared-account restrictions at their real scope. A source `active` record becomes active in Texenda only for a mapped, evidence-supported publication/channel; uncertain rows stay held.
3. **Dry run.** Show created/updated/held/invalid/ambiguous counts, field normalization and stronger restrictions. Repeat the import to prove idempotency. Snapshot load emits no live automation triggers.
4. **Install restrictive-event capture.** Verify legacy/current Kit event coverage and polling/export fallbacks. Keep original unsubscribe behavior functioning. Broader source-account opt-outs apply across the publications they actually covered, not just the currently migrating brand.
5. **Freeze and drain.** Pause source new enrollments, scheduled sends and integrations capable of starting work; capture new acquisition requests without pretending they already have a grant. If intake cannot be reliably captured, present a brief explicit unavailable/retry state rather than lose requests silently.
6. **Reconcile in-flight effects.** Record what Kit accepted/sent, what is definitely cancelled and what remains unknown. Do not activate Texenda duplicates for unknown source work. Establish exact per-enrollment progress from available recipient-level evidence or a reviewed manual export; never guess from elapsed days.
7. **Resolve every old execution.** Supported outcomes: verified resume at a mapped node with consumed effect keys; explicitly complete/retire with reviewed user impact; or hold/quarantine awaiting evidence. Default policy does not run the same program concurrently in both systems. An unresolved required program means the publication is not fully migrated.
8. **Final restrictive reconciliation.** Apply late opt-outs/complaints/erasure to the import, retain safety evidence independently and reconcile source totals. Fresh positive requests go through the new proof flow; last-write-wins imports cannot overrule a withdrawal.
9. **Commit authority.** Owner signs the unit's epoch transfer, records source pause evidence, points forms/integrations to Texenda and enables only the approved canary. The transfer record binds the exact source snapshot and mapping version.
10. **Observe.** Review sends, receipt explanations, acquisition, opt-outs, outcomes, source late events and accounting. Increase volume only with an approved next ceiling.
11. **Close.** Disable/retire old sending paths, preserve required records and legacy opt-out intake, then declare fully migrated only after section 17's observation and completeness tests.

Kit's unsubscribe endpoint is an account-level removal from future emails, not a publication-scoped Texenda operation. Preserve that asymmetry in both migration and rollback; do not call it to emulate a narrow target-publication withdrawal while other source publications remain active without understanding the impact. [S24](../09-reference/source-register.md#s24)

#### Rollback is another authority transfer, not a database rewind

Default incident response is **pause and repair forward in Texenda**. Returning sends to Kit requires a new reviewed epoch, current negative-evidence synchronization, verification that all Texenda-accepted/unknown communications are excluded, updated sequence positions, and proven source controls. If Kit cannot represent the required exclusions/cursors safely, do not roll back sending; keep the unit paused until repaired.

Never restore an old Kit export over current permission, re-enable old sequences from their original starting point, or let both systems send “temporarily.” Preserve all new withdrawals and delivered/uncertain occurrence claims across any rollback.

Legacy unsubscribe links may continue to point at Kit after cutover. Keep the account/endpoint capability needed to receive those requests until its actual persistence/retention behavior is verified. Do not cancel the Kit subscription or assume redirects preserve old links without VAL-10 evidence. Maintain a recipient-friendly reply/privacy route as an additional path, not a claimed replacement for broken one-click links.


## Execution packet required for each MigrationUnit

Astra MUST not infer account data or request write credentials merely to complete the plan. The owner supplies a read-only discovery grant first. Record account IDs, publications, shared rules, coupled cohorts, legacy unsubscribe routes, status exports, complete pagination, source timestamps and checksums. Separate activation authority from read access. Imports initially use historical mode and cannot emit enrollment triggers.

The designated owner signs the freeze/drain evidence and scope of authority transfer. Transition entries record source snapshot, negative reconciliation watermark, target revision, active send epoch, approving principal, canary ceiling and outstanding holds. If old Kit one-click URLs remain in delivered mail, preserve a working intake path for those restrictions; a new preference URL does not rewrite old messages. Do not close source access/account until that behavior has been validated.

**No cursor proof:** hold the enrollment or explicitly retire it with recipient/operator impact recorded. Do not restart the series, skip guessed steps, or calculate position from enrollment time. If proof cannot be obtained, remove that cohort from the claim of full migration until an owner-approved non-deceptive resolution is completed.

**Failed canary:** pause Texenda, continue restrictive intake, reconcile possible acceptances, and repair forward. Returning traffic to Kit requires a new negative-state reconciliation and explicit epoch transfer. No tool retry or incident request authorizes dual sending.

Use [migration-unit.template.json](migration-unit.template.json). Template fields are unfilled evidence requirements, not invented account facts. Acceptance checks AC-M01…AC-M09 and applicable delivery/recovery checks are binding.
