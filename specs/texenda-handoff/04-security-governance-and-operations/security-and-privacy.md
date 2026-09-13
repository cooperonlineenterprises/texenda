# Security, permissions, and governance

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f14"></a>
## 14. Security, permissions, and governance

**Decision status: AUTHORITATIVE DECISION.** Security enforcement belongs in principal resolution, domain authorization, scoped repositories, final handoff and runtime credentials—not merely navigation or a hidden button.

### 14.1 Authentication and authorization

Payload remains the operator authentication foundation. Require MFA before production administration; the initial implementation is a verified WebAuthn second factor/passkey ceremony integrated with Payload sessions through a role-independent assurance check. Recovery codes are single-use and hashed; registering/replacing factors requires step-up or a controlled recovery procedure. User-verification, RP ID/origin and challenge checks are mandatory. SimpleWebAuthn supplies the ceremony primitives, not Texenda's authorization policy. [S19](../09-reference/source-register.md#s19)

Enforce the resulting authenticated assurance on **all** protected generated/custom reads and mutations, server actions and job administration. A valid first-factor Payload session without MFA cannot access protected data. Revalidate domain membership at command time. Cookie/CSRF/origin protections, session expiry/revocation, login throttles, generic recovery responses and audit are required. Machine principals use separately scoped server credentials, not copied operator sessions.

Payload Local API and job operations can bypass access controls by default. Safe wrappers must explicitly apply the authenticated user and `overrideAccess: false` on request-driven operations; privileged internal calls are allowlisted and still enter authorized domain commands. `overrideLock: false` is used for editorial writes when applicable. Do not treat a request-supplied user/context object as trusted. [S01, S04](../09-reference/source-register.md#s01)

**Initial owner bootstrap:** disable public first-user registration and self-service organization creation. Use a one-time deployment-console command with a short-lived bootstrap capability to create the initial auth identity and activate its domain owner membership; a partially created auth record has no owner authority until the domain activation commits. Record the bootstrap actor/evidence, require MFA enrollment before general administration, then revoke the capability. Subsequent operator provisioning is owner-invited and scoped. Bootstrap/recovery can establish operator access but cannot create audience consent or bypass sending policy. Test reuse, concurrent bootstrap attempts and access before factor enrollment.

### 14.2 Role and capability model

| Role | Allowed core responsibilities | Sensitive capabilities not implied |
|---|---|---|
| Portfolio owner/admin | Organization settings, authorized brands, policy activation, migration authority | Cannot bypass recipient refusal or invent consent |
| Brand admin | One or more explicitly granted brands, publications, content and routine operations | No other-brand identity/history or organization limit override |
| Editor/marketer | Audience reads within scope, draft content/segments/workflows | No high-risk live approval or PII export unless separately granted |
| Approver | Approve/schedule within explicit recipient/spend limits | No automatic policy/sender/consent administration |
| Analyst | Scoped aggregates and approved read models | No unmasked exports or mutations |
| Support/privacy operator | Locate a scoped profile and apply recipient-requested restrictions | No unrestricted reconsent, broader identity view or safety-hold release |
| Deliverability/security operator | Sender health, incident holds, evidence-based corrections | No arbitrary marketing content or targeting authority |
| Integration principal | Enumerated commands/events/property scopes | No raw database/API wildcard, provider keys or live-send bypass |
| Worker principal | Execute approved domain work within current policies/leases | Cannot approve new campaigns or expand scope |

Capabilities separately control PII export, portfolio identity inspection, sender changes, permission correction, safety-hold release, policy activation and large-send approval. Audit both allowed sensitive operations and denied attempts. UI roles are presentations of these capabilities, not a second authority system.

### 14.3 Initial mass-send and approval safeguards

The following numeric settings are **REVERSIBLE DEFAULTS**; their enforcement is authoritative:

| Default ID | Pilot/initial rule |
|---|---|
| **APR-01** | Every new representation/sender combination requires a successful internal test and preflight before live use. |
| **APR-02** | The first live canary per publication is explicitly approved and capped at **250 eligible, genuinely subscribed recipients or the smaller actual audience**. It is not a synthetic permission grant. |
| **APR-03** | After pilot qualification, campaigns above **5,000 candidates** require elevated review. A campaign above an operator's recipient/spend authority must be approved by a principal with sufficient authority; step-up alone does not increase permissions or organization budget. The 5,000 figure is a safety default, not an assumed audience size. |
| **APR-04** | A solopreneur may perform elevated review using fresh MFA, a separate review step, retyped brand/count confirmation and a **10-minute cooling-off interval**. Organizations may require a second human instead. |
| **APR-05** | Approved candidate and cost ceilings are hard ceilings. Any change to bound content/audience/channel/sender/schedule requires reapproval. |
| **APR-06** | New provider accounts/senders and organization-wide policy relaxations require owner-level activation, even below recipient thresholds. |

Kill switches exist for deployment, organization, provider account, sender, brand, campaign and execution. A safety pause is immediate for future permits and does not wait behind bulk queue work. Workers use rate profiles and spend reservations. No positive metered sending budget means no live paid-channel activation; the owner records explicit ceilings before a canary.

### 14.4 Data, secrets and environment boundaries

Provider credentials exist only in authorized worker/runtime secret scopes. Web roles hold only ingress verification keys and the secrets necessary for their approved work. AI receives no provider or database credentials. Separate production, staging and development databases/buckets/keys; do not copy production contact data into tests except a documented minimized, protected dataset approved for that purpose.

Use TLS, managed encryption at rest, private database networking, least-privilege DB roles, per-runtime credentials, tested key rotation and redacted logs. Public media assets are separate from private imports/exports and safety evidence. Imported/rendered HTML is sanitized and isolated in preview; arbitrary URL fetching, header injection, template execution, malicious CSVs and oversized inputs are tested.

Exports require explicit capability and current MFA, create an audit record, use encrypted storage and short-lived access. **REVERSIBLE DEFAULT:** signed download links expire in 15 minutes; export files in 24 hours. Spreadsheet-friendly CSV neutralizes formula-leading cells; a separate typed JSON export preserves exact values. Exporting data is not permission to market through another system.

Consent/audit evidence is append-only under ordinary application credentials, with corrections as new records. Strong tamper resistance comes from restricted roles and independent versioned journal copies, not the word “immutable.” PII is separable/encrypted so authorized erasure/retention can remove personal content without rewriting every operational fact. HMAC lookup/dedup values remain potentially personal/pseudonymous data, not automatically anonymous. A minimal do-not-contact tombstone is retained only under an approved legal basis; reimport must not erase it.

### 14.5 Overrides, incidents and external review

There is no administrative command that simply ignores recipient permission. Break-glass access is time-bound, reasoned, logged and scoped to pause, inspect, recover or make evidence-based corrections. Infrastructure administrators are recognized as a separate threat boundary. An emergency incident does not authorize a promotional campaign.

**REQUIRES EXTERNAL VALIDATION — VAL-02/VAL-08:** privacy/retention, sender obligations, MFA/session access coverage, dependency vulnerabilities, hostile-input tests, transport qualification, and backup/restore safety. Unresolved findings block the affected activation gate. No claim of legal compliance or production security is made by issuing this specification.

---


## Interaction-specific threat boundaries

| Boundary | Threat | Enforcement |
|---|---|---|
| Microphone → speech provider | Ambient capture, private utterance leakage | Explicit capture, visible state, immediate mute, no raw-audio retention; provider terms/region qualification |
| Transcript/model → command | Wrong entity, negation loss, injected instruction | Finalized turns, typed schema, scope resolution, preview, approval and domain validation |
| Imported content → AI context | Prompt injection and exfiltration | Data/instruction separation, tool allowlist, minimized context, SSRF/egress limits, no model-supplied authority |
| Agent → delegation | Confused deputy, token theft, scope escalation | Resource-bound short-lived credentials, current membership/grant checks, revocation and budget limits |
| Browser session → approval | Agent impersonating human; confirmation spoof | Dedicated principal; out-of-agent human approval channel for human-only actions; no chat “yes” approval |
| Human/agent parallel edits | Stale update and TOCTOU | Expected revisions, immutable proposal digest, current checks at command and final handoff |
| SSE/status stream | Cross-brand leak or authority inferred from event | Auth-scoped cursors, reconnect/refetch, stream as derived observation only |
| Persistent preference → policy | Hidden widening of future behavior | Typed scoped promotion with authorization and audit; restrictive policy always wins |

All protected UI, API, generated Payload endpoints, job controls, Inspect views and real-time subscriptions must enforce the same authentication assurance and domain scope. Test token reuse after membership/grant revocation. Rotate provider/model/STT keys without placing them in the browser; ephemeral media-session credentials may be issued only for their bounded purpose.

Proposed reversible interaction retention: raw audio 0 days; transcript and bounded session summary 30 days unless the user selects session-only; agent operational records 30 days for debugging with separate justified audit retention; draft proposals follow configured product retention. Durable approval/command evidence is not erased merely by clearing a chat. Record source PII separately so privacy deletion is enforceable. These values require VAL-02/VAL-12 review; no claim about provider-side logging or deletion is made without evidence.

A grant contains expiry, permitted commands/resources, workspace scope, max consequence, rate and spend ceilings, and no onward delegation by default. Renewal is explicit. A cancelled run cannot be restarted under an expired grant. Long-running approved Texenda automations are not dependent on agent session survival and retain their own published authority.
