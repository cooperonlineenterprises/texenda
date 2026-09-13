# Provider and integration architecture

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f13"></a>
## 13. Provider and integration architecture

**Decision status: AUTHORITATIVE DECISION.** External systems impose additional constraints and return evidence; they cannot supply audience, consent, campaign, or workflow truth.

### 13.1 Transport contracts

The following is an interface sketch, not a promise that providers implement every capability:

```typescript
interface MailProvider {
  capabilities(route: QualifiedRoute): ProviderCapabilities;
  validatePrepared(request: PreparedEmail): ValidationResult;
  estimateCost(request: PreparedEmail): CostEstimate;
  send(request: PreparedEmail, permit: DispatchPermit): Promise<AcceptanceResult>;
  reconcile(reference: ProviderReference): Promise<ReconciliationResult>;
}
// A separate verified ingress adapter authenticates the original request bytes,
// retains evidence and returns normalized observations. It never calls send().
```

`AcceptanceResult` distinguishes accepted, definitely-not-accepted and unknown. Unsupported status retrieval is explicit; it does not default to not-sent. A provider-capability record includes API/account/region, idempotency scope/window, batch atomicity, item response correlation, status/event coverage, authentication, suppression scope, allowable headers, quotas, costs and qualification freshness.

The broader channel interface shares validation/readiness/cost/outcome vocabulary. It does not force onsite rendering into `MailProvider.send`, or map push/browser state into email bounce semantics. Channel adapters cannot construct unapproved recipients or grant fallback authority.

### 13.2 Resend baseline and sender isolation

**REVERSIBLE DEFAULT:** one qualified Resend account/team for the initial pilot brand. For additional substantial brands, prefer independently qualified teams/accounts or another proven isolation mechanism; a shared pool requires explicit acceptance of coupled limits and suppression. Record sender → provider account → team/region/program → legal sender mappings.

Do not assume domain-specific keys provide independent quotas or suppression. Resend's directly retrieved documentation describes team-wide suppression and team-level rate limits. Retrieved search summaries showed differing snapshots of some operational values; therefore **do not hard-code a remembered rate, domain count, price, or suppression geography**. Capture the live account's approved limits and verify behavior in VAL-04 before activation. [S07, S08](../09-reference/source-register.md#s07)

Texenda uses ordinary email sending APIs, not provider audience/automation features. A provider endpoint or plan labeled “transactional” is not a legal classification or permission to send marketing; confirm the selected plan permits the intended newsletter traffic. Provider scheduled-send features are not used initially—Texenda owns timing and cancellation.

Sender activation requires demonstrated domain control, allowed From/reply-to addresses, SPF/DKIM/DMARC configuration and alignment, test-message authentication results, functioning visible/one-click opt-out, provider feedback, and a named incident owner. Brand display identity remains clear. Shared IP pools and vendor reputation may still couple brands; domain separation is not a guarantee of complete deliverability isolation.

### 13.3 Webhook ingress and reconciliation

Authenticate the raw bytes according to the specific provider scheme, including its real timestamp/replay rules. Do not invent one universal signing method. Use separate endpoint secrets/account binding, size/content-type limits and constant-time verification where appropriate. Persist raw signed input and dedup ID before successful response; restrictive inputs additionally meet the safety-journal boundary. Do not execute a workflow in the HTTP callback.

Deduplicate `(provider_account, provider_event_id)` where supplied; use a qualified fallback identity only when necessary, preserving legitimately repeated distinct observations. A webhook may arrive before the API response: correlate by known provider/custom metadata or quarantine until the delivery is identifiable. It must not be attached to a guessed person by email alone.

Normalize into facts with source time, received time, confidence/coverage and source reference. Process safety events ahead of ordinary analytics. Unknown/contradictory events are visible and replayable. Poll/retrieve provider status or suppression exports when supported; APIs that cannot answer are marked inconclusive. Provider suppression removal never clears an independent Texenda withdrawal or safety hold.

### 13.4 Property API, event ingestion and SDK

Public API namespace is `/api/v1`, with explicit OpenAPI/JSON schemas, bounded pagination, stable opaque IDs, consistent errors and deprecation windows. Generated Payload REST/GraphQL is **not** the public audience API. Disable GraphQL unless a concrete internal requirement is qualified.

A publishable form identifier only submits to one preconfigured form. It is not a secret and cannot assign arbitrary tags, publications or purchases. Browser origin checks reduce accidental misuse but are not authentication. Rate limits, bot controls, verification and non-enumerating responses protect public acquisition.

Server API credentials are hashed/rotatable and scoped to organization, brand, property, allowed command/event types, rate and budget. Trusted purchase events require an authorized server integration and stable business event ID. Preserve original source IDs, schema version and source health. An integration may request a subscription only with required consent proof; no “add contact = active subscriber” shortcut exists.

Mutation idempotency is scoped by principal/route and a stable client key plus request digest. Same key/different request returns conflict. Keep transport-request deduplication and permanent business-occurrence constraints separate; a short API-idempotency TTL must not allow a duplicate purchase/welcome after it expires. Bulk APIs return per-item results and never conceal partial failure.

### 13.5 Outbound integrations and failure boundaries

Initially provide outbound webhooks only for a real integration need, using the existing outbox, signed minimized payloads, stable event IDs, bounded retry, endpoint pause and manual replay. Recipient identity is shared only by explicit scope. Protect outbound fetches from SSRF: approved HTTPS endpoints, controlled redirects, private-address denial and DNS/rebinding protections in the HTTP client/network policy.

Never let a failed webhook roll back consent or a completed campaign. Replays are tagged and idempotent; consumers must deduplicate. A later Svix adapter replaces delivery operations, not event semantics.

No automatic live failover to SES or another channel. Planned provider migration pauses, drains/reconciles outstanding work, preserves semantic keys, qualifies the new route, and explicitly activates it. Unknown effects remain on the old route's reconciliation path.

**Consequences:** one stable property API and permission model survive provider changes. **Revisit:** new integration types add schemas and capabilities under least privilege; no connector marketplace or general automation system is implied.

---
