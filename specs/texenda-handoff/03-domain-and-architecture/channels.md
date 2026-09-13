# Channel strategy and abstraction

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f07"></a>
## 7. Channel strategy and abstraction

**Decision status: AUTHORITATIVE DECISION.** One audience/workflow system may use several qualified channels; channels retain their distinct permission, delivery, content and observation semantics.

| Channel/purpose | Channel disposition | Decision status | Required qualification |
|---|---|---|---|
| Email | **FIRST-CLASS NOW** | **AUTHORITATIVE DECISION** | Core end-to-end safety, rendering, sender and provider gates |
| Contextual onsite messaging | **DESIGN FOR NOW, BUILD LATER** | **DEFER UNTIL TRIGGERED** | One property with a defined placement/use case, privacy basis, accessibility/performance test and fail-soft behavior |
| Web push | **DESIGN FOR NOW, BUILD LATER** | **DEFER UNTIL TRIGGERED** | Recipients request a timely alert; browser/origin/device tests; endpoint lifecycle; purpose consent; interruption caps |
| SMS | **REVISIT WHEN DEMAND EXISTS** | **DEFER UNTIL TRIGGERED** | High-value repeated use case, actual geography, consent evidence, registered sender program, STOP/reply operations, explicit spend ceiling |
| WhatsApp | **REVISIT WHEN DEMAND EXISTS** | **DEFER UNTIL TRIGGERED** | Supported market/category, templates/service-window policies, permission, reply ownership and provider qualification |
| Native push/in-app | **REVISIT WHEN DEMAND EXISTS** | **DEFER UNTIL TRIGGERED** | An actual app/account lifecycle; authenticated subject/device bindings; logout/reassignment testing |
| Cold outreach, social DMs, voice campaigns, ad audiences | **DO NOT PURSUE** | **AUTHORITATIVE DECISION** | Outside the product boundary |
| Transactional/service | Not a channel | **AUTHORITATIVE DECISION** | Purpose/resource authorization applied to an eligible channel; only narrow approved uses |

Push must not require an email address. Technical browser permission and the chosen brand/topic are separate facts. Apple's documented iOS/iPadOS Web Push behavior involves Home Screen web apps and direct user interaction; pilot the actual audience/browser mix rather than assume universal support. [S17](../09-reference/source-register.md#s17)

Onsite has two modes: anonymous contextual selection from the current page, and known-recipient personalization under approved processing/identity rules. Email consent alone does not authorize browser tracking. Use defined inline/dismissible placements, not a site builder or aggressive overlay system. The website continues normally if Texenda fails.

Every new channel has a qualification record: approved use case; geography; purpose/consent wording; sender/program ownership; supported capabilities; content limits; cost/rate behavior; inbound opt-out and replies; monitoring owner; retention; incident plan; tested adapter version. Without qualification its configuration may be drafted but its dispatch is disabled.

### Supported coordination semantics

1. **Single outbound channel:** the default for each occurrence.
2. **Passive onsite companion:** optional and independently impression-limited; no automatic extra outbound contact.
3. **Choose one approved channel:** later, deterministic preference/policy selection among eligible representations. AI may recommend the policy but does not select a route at runtime.
4. **Confirmed-failure fallback:** later, only from definitive non-acceptance, with separate valid channel permission and explicit plan authority.
5. **Outcome-based follow-up:** a separately approved step/occurrence with its own count, spacing, expiry and cancellation. It is not a provider retry.

Never use non-opening as proof of non-receipt, and never escalate because of unsubscribe, complaint, invalid consent, or a provider policy block. Unknown acceptance pauses a plan. A business outcome such as verified purchase can cancel all equivalent pending promotions.

**Consequences:** email-only implementations populate shared identifiers now but do not build empty channel administration screens. **Revisit:** a channel moves to first-class only after VAL-07 and its Roadmap gate; lack of demand is a valid reason never to implement it.

---
