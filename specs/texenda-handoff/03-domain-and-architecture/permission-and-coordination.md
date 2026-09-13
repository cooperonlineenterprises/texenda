# Consent, eligibility, suppression, preferences, and recipient experience

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f06"></a>
## 6. Consent, eligibility, suppression, preferences, and recipient experience

**Decision status: AUTHORITATIVE DECISION.** Communication authority is explicit, contextual, revocable, and evaluated independently of transport reachability.

### 6.1 Permission tuple and evidence

For marketing, an effective grant identifies:

```text
organization + workspace + publication/purpose + channel
+ subject/profile + authorized endpoint binding + disclosure version
+ proof/source + validity + consent revision
```

Email subscriptions imported from Kit remain **email-only**. A web-push permission prompt, an SMS number, a purchased product, a tag, and a successful previous delivery do not grant unrelated marketing authority. Service messages use a separate, allowlisted resource/purpose authorization, not an active marketing subscription.

Consent evidence records the actual displayed disclosure, form/variant, source property, request/confirmation times, source-system identifiers, principal, proof method and processing purpose. Store only justified network evidence. Never backfill missing historical proof with a current disclosure or manufacture an opt-in timestamp from an import date.

**REVERSIBLE DEFAULT:** new public email subscriptions use double opt-in. A qualified publication may use another expressly approved policy after VAL-02 review. Public subscription requests are non-enumerating and abuse-limited; confirmation messages themselves pass the system/fulfillment policy and do not contain unrelated marketing.

### 6.2 Subscription and reconsent transitions

| Input | Authoritative result | Prohibited side effect |
|---|---|---|
| Public signup with required confirmation | Pending request; bounded confirmation message | No marketing enrollment before confirmation |
| Valid confirmation | Scoped grant and active channel subscription | No grants for other publications/brands/channels |
| Duplicate confirmation | Return current result; no extra grant or trigger | No repeat welcome |
| Publication/channel opt-out | Withdrawal and withdrawn current membership; cancel affected pending marketing | No alternate-channel escalation |
| Brand/portfolio stop | Broader withdrawal across the covered known scope | Do not invent unknown identity bindings |
| Ordinary signup after broad stop | Pending fresh reconsent with the prior restriction explicitly acknowledged in the confirmation context | Do not remove broad restrictions for sibling subscriptions |
| Fresh confirmed reconsent | A narrowly scoped grant may explicitly supersede specified recipient withdrawals for that same endpoint/purpose | Never releases complaint, endpoint-invalidity, or provider safety holds |
| Old confirmation issued before a later withdrawal | Reject as stale | Never resurrect authority through an old token |
| Safety-hold release | Removes only that named operational block after review | Does not manufacture a fresh consent or reactivate unrelated subscriptions |

To permit a person to rejoin one publication after a brand-wide opt-out without reviving every old subscription, a fresh grant may record **explicitly acknowledged withdrawal IDs it supersedes only within its own narrow scope**. Later withdrawals still win. This exception mechanism applies to recipient choice only, never to safety/provider restrictions.

A removed/revoked grant is never silently reactivated by import, API upsert, a provider suppression removal, or an operator changing a tag. Existing cancelled workflows do not resume on reconsent; a new qualified trigger or explicit enrollment creates a new execution identity.

### 6.3 Message classes

| Class | Required authority | Pressure treatment |
|---|---|---|
| `marketing` | Active scoped subscription/grant and all applicable safety checks | Full brand/portfolio/channel caps |
| `requested_fulfillment` | A particular recent authenticated or verified request, approved resource and endpoint | Separate bounded abuse/dedup limits; cannot carry unrelated promotions |
| `service` | Allowlisted resource relationship and approved message purpose | Service policy and rate limits; no arbitrary “urgent” bypass |
| `operator_auth` | Account-specific login/recovery/verification request, approved template and sender | Strict account/endpoint abuse limits; no marketing |
| `test` | Authorized operator, approved test purpose and preverified internal allowlist | Test quota; conspicuous marker; no audience-wide addressing |

All classes use the same entry point. Payload's automatic email adapter must route auth/recovery through the corresponding domain command and worker; the web process has no email-provider credentials. Classification of mixed commercial/service content is a legal/policy matter under VAL-02; labeling a campaign `service` does not make it so. FTC guidance distinguishes messages by primary purpose and requires clear commercial opt-out behavior. [S14](../09-reference/source-register.md#s14)

### 6.4 Suppression and propagation

| Restriction | Default scope and behavior |
|---|---|
| Confirmed permanent email-address failure | Block that endpoint across the organization; retain subscriptions as historical facts. Do not mark phone/push endpoints invalid. |
| Temporary/ambiguous bounce | Retry or hold according to the qualified error class; never convert a transient code to permanent invalidity by convenience. |
| Spam complaint | Block marketing on the email endpoint organization-wide. Where the identity is reliable, add a conservative person-level marketing safety hold. Preserve the source and reason; this is not fabricated revocation of every other legal consent. |
| Provider suppression | Mirror its actual account/team/region/program scope as an additional denial. Never remove it merely because a local subscription is active. |
| Publication withdrawal | Blocks the specified publication/channel/endpoint authority; presentation may offer a broader stop. |
| Brand stop / portfolio stop | Blocks covered marketing across the chosen scope and reliably linked endpoints. New later identity bindings inherit relevant known broad restrictions conservatively, not new permissions. |
| Push invalidation or device logout | Retire/disable the binding; shared devices must not continue receiving prior-user personalized notifications. |
| SMS/WhatsApp opt-out | Enforce the qualified legal and provider-program scope, which may exceed a Texenda workspace; acknowledge only as permitted by that channel's rules. |
| Administrative investigation/unknown imported proof | Scoped safety hold until evidence is reviewed; no automatic alternate route. |

An endpoint block, recipient withdrawal, and complaint are materially different; retain separate reason types. No routine “send anyway” action exists. A correction requires elevated rights, step-up authentication, evidence, and audit, and cannot overrule a recipient's current refusal.

**REQUIRES EXTERNAL VALIDATION — VAL-02/VAL-04/VAL-07:** jurisdictions, legal-sender scope, retention, channel disclosures, and provider revocation rules. Store effective-dated policy and sender-program mappings. Twilio's current policy is an example of sender/purpose-specific consent and opt-out obligations that a phone adapter must implement; it is not a generic consent source. [S16](../09-reference/source-register.md#s16)

### 6.5 Eligibility decision contract

```text
EvaluateCommunication(input, current_primary_state) ->
  ALLOW   { short_lived_permit, evidence_refs, reservations }
  DENY    { reason_codes, terminal_for_this_occurrence }
  DEFER   { reason_codes, next_eligible_at, expires_at }
  HOLD    { reason_codes, required_resolution }
  SKIP    { reason_codes: duplicate | expired | completed_goal | ... }
```

Evaluate in this order: principal and migration authority; scope and publication/purpose; approved/current content; endpoint binding/reachability; current grants/withdrawals; safety/provider holds; goal/cancellation state; equivalence claim; recipient preferences/quiet hours; pressure/priority; sender/provider readiness; spend/rate constraints. Collect all safe-to-disclose reasons, but do not leak unrelated brand information. Previews have no sending authority.

Unknown required proof, unknown source coverage for a safety-sensitive exclusion, or uncertain provider acceptance returns HOLD, not ALLOW. Provider outages and temporary limits return HOLD/DEFER. Retrying a permanently ineligible occurrence cannot turn it eligible without a legitimate state transition and, when necessary, new approval.

A final permit is acquired under a short transaction using current primary state and a deployment execution epoch. **If a withdrawal commits before permit acquisition, handoff is denied. If withdrawal commits after a valid handoff permit, the in-flight request may complete.** Workers revalidate immediately before calling the provider and cancel anything not yet handed off, but Texenda cannot make a remote provider call atomic with a local opt-out or recall an accepted message. This is the explicit linearization boundary, not a promise of impossible zero-race delivery.

### 6.6 Preferences and unsubscribe experience

Preference precedence is the restrictive intersection of law/provider rules, organization safety policy, recipient broad limits, brand policy, publication promise, recipient specific preferences, and campaign/workflow configuration. Recipient channel ranking orders only already-eligible options. An invalid preferred channel does not authorize another channel unless the recipient and approved plan permit it.

Use a brand-branded page from each message. It must identify the publication/channel and offer an immediate scoped stop, plus a plainly labeled brand-wide marketing stop. Portfolio-wide stop is available with explicit scope wording. **Stopping marketing must not require login or extra identity verification.** Authentication may be required to reveal cross-brand subscriptions, add permission, expose PII, or change unrelated settings—not to obstruct an opt-out. An opaque recipient-bound capability can authorize a blind broader denial without revealing the recipient's other relationships.

Email headers implement RFC 8058: HTTPS endpoint, prescribed POST value, DKIM coverage of both unsubscribe headers, no login/cookies requirement, no redirect. GET displays a safe confirmation/preferences page and does not change state merely because a scanner followed the link. POST applies the named denial idempotently while already withdrawn. A later valid request after fresh reconsent can withdraw again. Unsubscribe tokens remain usable for the justified life of the message/retained subscription; they do not expire after a short login-token window. [S12](../09-reference/source-register.md#s12) Do not use the token itself as a permanent request-idempotency key that would prevent a later valid withdrawal after reconsent. Deduplicate an already-applied request/current denial while preserving the ability to record a new withdrawal.

Tokens disclose no plaintext personal data, are purpose-bound, and survive key rotation through retained verification keys or opaque server-side lookup. Forwarded messages can permit an opt-out; they must not permit reading profile data or granting consent. Export/portfolio-edit capabilities are separate.

### 6.7 Frequency, priorities and expiry

**Decision status: AUTHORITATIVE DECISION** for layered coordination, atomicity and precedence. **The numeric defaults below each have decision status REVERSIBLE DEFAULT.** They are initial safety settings, not empirically optimal frequencies or legal safe harbors.

| Default ID | Initial setting | Revision boundary |
|---|---|---|
| **POL-01** | Maximum one discretionary marketing interruption per brand per rolling 24 hours | Organization-approved policy; no per-campaign bypass |
| **POL-02** | Maximum two marketing interruptions per known person across the portfolio per rolling 24 hours; minimum four-hour spacing | Explicit organization/recipient policy; first run in shadow against actual publication promises |
| **POL-03** | Additional interruptive-channel bucket: maximum one combined push/SMS/WhatsApp interruption per rolling 24 hours | Qualify before those channels go live; may be tightened by recipient |
| **POL-04** | Every publication records its promised cadence; missing cadence blocks activation | Daily/weekly promise can have an explicit approved civil-calendar schedule; cannot silently bypass portfolio policy |
| **POL-05** | Discretionary email defaults to a 24-hour dispatch window; it expires rather than backlogs after that | Operator may approve a different finite window; offer validity is always an upper bound |
| **POL-06** | Default preferred marketing hours: 08:00–20:00 in a recipient-supplied timezone, otherwise the configured workspace timezone for email | Labeled fallback, not an inferred location; regulated channels require a separately qualified rule |

Before enforcing inherited caps, replay real intended publication schedules in shadow mode. A recipient's deliberately chosen daily publications must not be quietly broken by a new default. Resolve conflicts through an explicit organization/recipient cadence policy; do not secretly raise limits or silently drop promised editions. Until resolved, hold the affected schedule at approval and explain the conflict.

Priority classes: requested/service fulfillment under its own authority; promised scheduled publications; explicitly requested time-sensitive alerts; ordinary lifecycle marketing; discretionary promotion. Campaign versus automation is **not** a priority distinction. Within a class, use a deterministic ordering of expiry, ready time, least recently served eligible brand, and stable ID. Fairness prevents a busy brand from indefinitely starving another. Operators cannot relabel promotion as service to win arbitration.

Reservations count provisionally until acceptance or definitive non-acceptance. Accepted sends consume interruption allowance; unknown acceptance consumes it conservatively. Provider retries reuse a delivery and reservation; a genuine follow-up adds an interruption. A confirmed failure can release the transport interruption reservation where qualified, but the logical occurrence and dedup trail remain. Passive onsite impressions use separate impression/dismissal caps; they do not reset outbound allowance.

Global coordination is limited to reliably known identities. It does not justify fingerprinting anonymous devices. A brand operator receives “deferred under portfolio policy,” not another brand's interests, purchase history, or campaign details.

### 6.8 Equivalence and cross-brand safeguards

An equivalence family means several approved representations express the same underlying communication. Its occurrence key distinguishes a particular issue, purchase event, guide request or reminder opportunity. Editorially similar copy does not by itself imply equivalence; an AI similarity score cannot create or remove a claim.

Default occurrence uniqueness is organization + brand + equivalence family + occurrence key + coordination subject. A protected endpoint fingerprint additionally prevents duplicate contact to a shared/aliased destination. A planned email and push share a logical occurrence but still have distinct effect keys and interruption accounting. Multi-device push defaults to one verified preferred device, not all devices.

Portfolio planning may link separate brand campaigns with an explicitly approved cross-brand equivalence group. Each child retains its own permission, sender, audience, content and approval. No pooled audience or automatic source-brand-event-to-target-brand-send exists in V1. An invitation to another brand is not enrollment in it.

**Consequences:** the basic coordinator precedes pilot delivery, not merely multichannel rollout. **Revisit:** numeric policy changes are reversible, versioned and previewed; consent/authority semantics require a governing ADR. Legal uncertainty blocks the affected channel/use case rather than broadening permission.

---
