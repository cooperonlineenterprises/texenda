# Governing principles and non-bypassable invariants

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f03"></a>
## 3. Governing principles and non-bypassable invariants

**Decision status: AUTHORITATIVE DECISION.** The following requirements apply through every supported UI, API, import, administrative action, integration, worker, and AI tool.

| ID | Normative invariant | Implementation/test implication |
|---|---|---|
| **INV-01** | One Texenda domain model owns audience and communication truth. | Provider contacts, analytics, CMS documents, and model output cannot independently grant communication authority. |
| **INV-02** | Shared identity never creates shared permission. | A profile/endpoint match cannot activate another publication, brand, purpose, or channel. |
| **INV-03** | Reachability, identity proof, consent, and preference are distinct facts. | A phone number, browser permission, or successful prior delivery is not a marketing grant. |
| **INV-04** | Every proactive message and personalized placement passes the applicable central policy. | No direct provider-send endpoint; service/auth/test classes use narrow policy branches, not bypass flags. |
| **INV-05** | Applicable denials dominate preferences and historical approvals. | Current opt-outs, blocks, safety holds, authority leases, and expired content are checked at final handoff. |
| **INV-06** | Scope is enforced server-side and structurally in relationships. | Composite scope keys/FKs, authorized repositories, and adversarial endpoint tests; UI filtering is insufficient. |
| **INV-07** | Queues wake work; business state is durable in PostgreSQL. | Dropped/duplicated jobs cannot lose an execution or create another logical effect. |
| **INV-08** | Published campaigns/content/workflows are versioned and immutable. | Edits create revisions; active runs pin versions; approved changes require explicit activation/migration. |
| **INV-09** | Logical occurrences, channel deliveries, attempts, and observations are different objects. | Retries do not create new communications; follow-ups consume additional interruption allowance. |
| **INV-10** | Admission, deduplication, and pressure/spend reservations are atomic. | Two workers cannot independently consume the same remaining slot. |
| **INV-11** | External effects are effectively-once where qualified, otherwise explicitly uncertain and reconcilable. | Unique semantic keys, stable payloads, provider idempotency, and `acceptance_unknown`; never claim universal exactly-once email. |
| **INV-12** | A timeout or outage never authorizes blind provider/channel failover. | Reconcile before another effect; a block or opt-out cannot trigger escape to another channel. |
| **INV-13** | Every consequential effect has a decision receipt and approved authority chain. | Record actor/configuration, revisions, eligibility evidence references, policy version, route, and timing. |
| **INV-14** | AI translates intent; deterministic systems enforce truth. | Models return typed proposals; never direct SQL, provider credentials, consent grants, or policy override. |
| **INV-15** | Recipient trust outranks communication volume. | Expire stale work; suppress duplicates; enforce caps; never flush a deferred backlog in a burst. |
| **INV-16** | Imports/replays do not silently activate automations or weaken denials. | Default `trigger_mode=historical`; negative evidence wins until an explicit valid reconsent. |
| **INV-17** | Successful opt-out acknowledgment means the restriction is durably recorded and applied. | No success response before authoritative mutation and the recovery safety evidence are durable. |
| **INV-18** | Restore/recovery cannot silently revive prior permissions or repeat uncertain effects. | Independent safety journal, deployment send gate, reconciliation, and new execution epoch before resuming. |
| **INV-19** | Publication migration has one active sending authority for each scoped function/cohort. | A Texenda worker checks an authority lease; Kit-side controls must be verified, not assumed enforceable by Texenda. |
| **INV-20** | Test/development environments cannot reach real recipients through production transport. | No production credentials, egress controls, fake providers/Mailpit; `NODE_ENV` alone is not a safety boundary. |
| **INV-21** | Audit immutability is not indefinite retention of personal data. | Append corrections; separate erasable PII; lawful retention/erasure process preserves only justified evidence. |
| **INV-22** | No automatic cross-brand marketing action derives from another brand's behavior. | Shared coordination may delay a send, but cannot supply missing permission, targeting authority, or disclosure. |

“Non-bypassable” describes enforcement through supported application paths and runtime identities. An infrastructure root/DBA compromise is outside that guarantee; least privilege, independent evidence, monitoring, and break-glass controls address that threat. The product must not advertise immunity to a compromised administrator or vendor.

**Revisit:** changes require a governing ADR, failure-mode review, and migration/acceptance impact assessment. No reversible-default change may weaken an invariant.

---


## Interaction invariants added by accepted human/agent architecture

| ID | Normative invariant | Implementation/test implication |
|---|---|---|
| **INV-23** | Conversation is an interface, never sole authoritative product state. | Durable goals/proposals/configurations survive session loss and are directly editable. |
| **INV-24** | All interaction surfaces invoke the same command/query and policy contracts. | Visual, voice, AI, API and computer use have no parallel mutation path. |
| **INV-25** | Approval binds exact immutable intent and consequence envelope. | Ambiguous speech, stale revisions, larger audiences/costs and changed scope cannot reuse approval. |
| **INV-26** | Machine action is attributable and bounded by current delegation. | Record agent + delegator + scope + command + result; revocation stops new authority. |
| **INV-27** | Semantic/accessibility UI improves legibility, never authority. | Inspect mode/DOM visibility/tool hints do not expand access. |
| **INV-28** | AI, voice and realtime services are optional to core operation. | Manual configuration and deterministic approved work survive provider outages. |
| **INV-29** | Working memory and persistent instructions cannot silently become policy. | Explicit scoped preferences/constraints are versioned and cannot overrule safeguards. |
| **INV-30** | The development harness coordinates work but cannot grant production authority. | No recipient sends, deployments, spend or credential use from a planning receipt. |
