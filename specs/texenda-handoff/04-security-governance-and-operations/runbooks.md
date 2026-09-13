# Operational runbooks and accountable ownership

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Accepted interaction architecture and complete-handoff directive. Apply [package authority](../DECISION-STATUS.md).


These runbooks define required production procedures. Their referenced Texenda commands are implementation contracts, not executable commands shipped in this handoff. Do not paste speculative SQL or provider write calls into production. Implement and rehearse the operator controls in WP-39/41 before activation.

## Ownership and severity

One accountable owner MUST be named for sender operations, incident response, privacy/withdrawal processing, security, backups/restores and provider billing. One person may own several areas, but absence/holiday cover and alert delivery must be explicit. AI can explain evidence; it cannot own incidents or approve resumption. Providers own transport and account restrictions, not Texenda consent truth.

**Critical:** possible unauthorized/cross-brand send, lost withdrawal, leaked credentials/PII, duplicate uncertain effects, restore with untrusted send state. Pause affected scope immediately (organization if scope uncertain), preserve evidence, notify owner, investigate and obtain independent review before resumption.

**High:** authentication failure, broken restriction ingestion, journal outage, material complaint/bounce anomaly, provider block, poisoned AI context. Hold affected sends; prioritize restriction traffic and evidence preservation.

**Routine:** non-safety queue lag, content validation, import rows held, abandoned proposals. Route to attention queue without interrupting operators repeatedly. Aggregate repeated alerts, record an owner and safe action.

## RB-01 — Wrong audience or accidental mass send

1. Use a pre-authorized `PauseSending` restriction at the smallest known scope; choose organization if unknown. Do not wait for an AI diagnosis.
2. Capture campaign revision, authority chain, recipient snapshot ID, final permits, journal range, provider request IDs and current send epoch.
3. Distinguish unclaimed, reserved, handed-off, accepted, rejected and unknown deliveries. Cancel only future work; delivered email cannot be recalled.
4. Do not delete recipient rows or reset campaign state to hide counts. Preserve protected evidence and suppress further equivalent occurrences.
5. Determine exact exposed recipients from records, not dashboard guesses. Engage privacy/legal review where required.
6. Correct policy/selection through a new revision and independent review. Any explanatory recipient communication requires its own reviewed purpose/permission; do not auto-send an apology to everyone.
7. Resume only with current restriction state, reconciled unknowns and owner-authorized scope. Record remediation and regression tests.

## RB-02 — Provider outage, rate limit or unknown acceptance

Pause or open the affected circuit breaker; retain quotas and safety records. Retry only proven safe failures within the same delivery payload/key and qualified window. A timeout after possible acceptance becomes `acceptance_unknown`; query qualified provider evidence and reconcile webhook/journal facts. Do not fail over to SES/another sender/channel merely to bypass the outage or suppression. Confirmed non-acceptance may permit the approved retry/fallback before expiry. Expired messages are skipped, not caught up in a burst. Persistent unknowns remain held or explicitly closed with uncertainty and durable tombstones.

## RB-03 — Opt-out/provider safety ingress or journal outage

Apply the database restriction immediately, journal it independently, then acknowledge success. If the journal fails, keep the denial, return a retryable response and hold outbound while durability is uncertain. Do not delay restrictions behind bulk import/analytics/model work. Invalid signatures are rejected; valid duplicate events are idempotent. Replay restrictive records before granting recovery permits. Provider blocks may be wider than internal publication scope and cannot be evaded by changing sender/account.

## RB-04 — Restore after database loss

1. Keep all outbound disabled in deployment/secret/runtime control outside the restored database. Revoke old worker epochs and credentials where appropriate.
2. Restore selected PITR or independent backup into an isolated environment; validate integrity and migration version. Record actual loss window.
3. Replay the independent encrypted restrictive-input, erasure and effect-intent journal newer than the snapshot. Apply denials/erasure before considering positive state. Journal records do not grant consent.
4. Reconcile all possible handoffs, including intents without responses. Unknowns stay blocked; stale database state is not permission to resend.
5. Rebuild derived counters, reservations, outbox/inbox status and workflow projections from authoritative records. Expired work stays expired.
6. Verify post-backup withdrawals, accepted-before-crash deliveries, source migration epoch and content/policy changes. Run AC-R and applicable security checks.
7. An authorized human issues a new send epoch through `ReleaseRecoveryHold` after independent review. Resume canary only, observe, then widen. Report measured RPO/RTO, not vendor promises.

## RB-05 — Compromised credentials, malicious agent or prompt injection

Revoke the exact delegation/session/API credential; rotate compromised secrets through the secret store. Pause affected external effects. Capture attributable commands/proposals and redacted model-context lineage. Imported text never authorizes action. Inspect token audience/scope, grant expiry, changed policies and PII access. Prefer disable/restrict over model attempts to “fix” access. Requalify repaired boundaries with negative tests before re-enabling. Do not grant incident agents unrestricted owner credentials.

## RB-06 — Stalled or invalid workflow

Use execution ID, pinned definition, cursor, lease/fence, source coverage and decision receipts. Determine whether it is intentionally waiting, deferred, denied, expired, uncertain or quarantined. Do not move cursors manually in SQL or create a new enrollment to bypass uncertainty. Repair through explicit reviewed commands/replay with uniqueness guards. A definition edit creates a new revision; active instances remain pinned unless a previewed migration is approved. Events and timeouts get one winner.

## RB-07 — Source integration stale or purchase feed interrupted

Mark SourceCoverage stale/incomplete; negative conditions become UNKNOWN and hold. Continue safely processing incoming evidence and restrictions. Restore source checkpoints with overlap/deduplication, then prove coverage before release. Backdated event times cannot claim a branch would have known a fact earlier than recorded. Do not use an apparent absence of purchase while the feed is unavailable.

## RB-08 — Kit cutover incident

Pause target and verify Kit source fence before any response. Restrictive intake must continue. Reconcile current grant/withdrawal/suppression union, unknown deliveries and workflow cursor proofs. Repair forward is default. Rollback is a new authorized transfer, never a restored database or re-enabled old Kit automation. Do not narrow account-wide Kit withdrawal semantics to a target publication. Retain old opt-out links until actually decommissionable.

## RB-09 — Privacy erasure and evidence retention

Verify requester identity only to the degree needed for the requested disclosure/change; do not burden an ordinary scoped unsubscribe with authentication. Separate erased PII from minimal approved safety/blocking evidence. Apply erasure to active stores, analytics/model copies where governed and eventual backup expiry; journal erasure so restored data is not resurrected. A hash/pseudonym may still be personal data and needs a justified retention basis. Do not promise immutable logs retain personal content forever.

## RB-10 — Routine release and rollback

Build from a reviewed commit and locked dependencies; record artifact digest and ordered schema migration manifest. Run contract/rollback checks in staging with fake transports. Deploy additive compatible changes before destructive schema cleanup. Drain/version-fence workers; active workflows keep compatible handlers. Verify journal/safety ingestion before enabling outbound. Rollback binaries only when compatible with schema and pinned workflow revisions; otherwise pause and forward-fix. Production deploy/migration requires explicit owner authority, independent of Astra's task completion.

## Weekly operational checklist

Review only exceptions first: restrictions/complaints, unknown effects, journal lag, source coverage, paused senders, failed jobs and expiring domains/templates/grants. Verify upcoming communications for conflicts and expiry, review cost usage, backup coverage and provider notices. Inspect unusual growth/opt-out trends with sample sizes and denominators. Successful routine operation should be quiet; do not ask AI to manufacture weekly optimization tasks.

## Drill schedule — REVERSIBLE DEFAULT

Before the first live publication: full restore + crash/unknown/withdrawal drill. After major recovery/schema/provider change: repeat affected drill. During operation: weekly automated backup verification and quarterly isolated restore rehearsal, subject to actual purchased hosting and data-retention policy. New channels/agent access repeat their own incident/opt-out tests before activation. VAL-05 and VAL-08 approve evidence; these intervals are operating defaults, not claims of current execution.
