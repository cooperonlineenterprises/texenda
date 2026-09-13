# Product definition and boundary

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f01"></a>
## 1. Product definition and boundary

**Decision status: AUTHORITATIVE DECISION.** Preserve the email-led, small-team product. Selective channels extend its communication model; they do not redefine it as an omnichannel suite.

### 1.1 Users and jobs

The primary users are publishers, creators, owner-operated brands, solopreneurs, and approximately five or fewer routine operators. Technical administrators are secondary users. One person may perform several operational roles; safe operation MUST NOT require a permanent two-person approval staff.

Primary jobs are to acquire subscribers; understand and organize a permissioned audience; compose and publish email; run welcome and follow-up sequences; configure bounded event-driven communication; manage preferences and suppression; understand observed results; and coordinate work across owned brands without pooling their permissions.

The operator should decide **intent, audience, content, and timing**. Texenda absorbs repetitive administration, policy evaluation, duplicate prevention, scheduling, execution, and explanations. It does not remove human responsibility for claims, brand judgment, consent provenance, incidents, or channel suitability.

### 1.2 Scope

| Product classification | Included capability | Boundary |
|---|---|---|
| **CORE PRODUCT** | Audience identities/profiles; subscriptions; consent; preferences; suppressions; tags/attributes; segments; forms; imports/exports; email; broadcasts; sequences; bounded automations; performance reporting | These together replace the useful core of Kit. The first production pilot may precede sequences and automations, but complete Kit retirement may not. |
| **CORE PRODUCT** | Multi-workspace administration, communication equivalence/expiry, basic pressure enforcement, decision receipts, audit, recovery | Correctness foundations exist before the first real send. Rich portfolio views can follow. |
| **NATURAL EXPANSION** | Reusable recipes/templates; AI preparation; communication calendar; contextual onsite placements; qualified web push; cross-channel choose-one policies | Add in dependency order and only behind the same permission and execution model. |
| **OPTIONAL ADJACENCY** | SMS, WhatsApp, native/in-app messaging, narrowly authorized service notifications, joint-brand planning, experimentation | A use-case, legal/provider, cost, and operations gate is required. |
| **OUT OF SCOPE** | Sales pipelines, prospect scraping, cold outreach, CDP-scale behavioral collection, support ticketing, ad buying, ecommerce authority, social publishing, site building, arbitrary workflow code, autonomous marketing agents | Integrate a narrow fact or effect when needed; do not become the adjacent category. |

### 1.3 Portfolio and category

Seed one Organization: **Cooper Online Enterprises**. Initial Workspaces are One Happy Housewife, Homeschool Pickle, Endless Popcorn, Brewologist, Stavium, and Cooper Online Enterprises. Their initially associated properties are respectively `onehappyhousewife.com`, `homeschoolpickle.com`, `endlesspopcorn.com`, `brewologist.com`, `stavium.ai`, and `cooperonlineenterprises.com`. A brand can own multiple properties and publications. These domain names are context, not evidence that DNS ownership has been verified.

Initial operation is a private, single-organization installation. Preserve `organization_id` in data boundaries, but do not ship external-customer tenancy, customer billing, or self-service organization provisioning. Commercial multi-organization operation requires a separate isolation and operations qualification.

Present category: **Email Audience & Automation Platform**. Future category, only when multiple channels are actually useful: **Audience & Communication Platform**.

### 1.4 Durable product truth

Changing a database driver, provider, UI, queue, or AI model must not change who may be contacted, which brand is speaking, what a subscription means, how duplicate effects are prevented, or why an automation continued. Identity recognition is not permission. A successful product increases communication usefulness, not merely send volume.

**Alternatives rejected:** a channel-neutral UI from day one; a wrapper around several independent marketing systems; a generic engagement suite. All increase conceptual or authority ambiguity without serving current routine work.

**Downstream consequences:** section 5 is the sole conceptual vocabulary; email gets the richest first implementation; all future channels qualify against sections 6–8. **Revisit:** only an explicit product-boundary ADR supported by recurring user demand, not a provider's feature release.

---

<a id="f02"></a>
## 2. Naming and brand architecture

| Topic | Decision status | Resolution |
|---|---|---|
| Working master identity | **AUTHORITATIVE DECISION** | Use **Texenda** in design and internal product work. Naming uncertainty does not reopen audience or architecture decisions. |
| Initial descriptor | **AUTHORITATIVE DECISION** | **Email Audience & Automation Platform**. |
| Later descriptor | **DEFER UNTIL TRIGGERED** | Use **Audience & Communication Platform** when non-email surfaces are production-qualified and materially used. |
| Parent endorsement | **AUTHORITATIVE DECISION** | `Texenda by Cooper Online Enterprises` on ownership/about/legal surfaces; ordinary product conversation uses Texenda. |
| Public adoption/registration | **REQUIRES EXTERNAL VALIDATION** | VAL-01: trademark/common-law, similar-mark, domain, registry, linguistic, and market review before irreversible public branding. |
| Technical names | **REVERSIBLE DEFAULT** | Repository `coe-audience-platform`; descriptive internal package/runtime names. Branding is configuration, not a database-key namespace. |

Previously identified **Xenda / PiXENDA** concerns remain part of the clearance brief; this specification neither establishes their legal rights nor declares Texenda clear. Formal review must consider similarity and related goods/services, not exact spelling alone. USPTO guidance explicitly recognizes confusing similarity in sound, appearance, meaning, and related commercial fields. [S22](../09-reference/source-register.md#s22)

Use ordinary product surfaces: Audience, Forms, Messages, Broadcasts, Sequences, Automations, Calendar, Insights, Deliverability, Integrations, Settings. Do not create branded subproducts merely to label navigation.

**Consequence:** internal development may proceed under Texenda while the public brand gate remains closed. URLs, sender identities, RP IDs for authentication, and legal disclosures must be configured independently of the master name. **Revisit:** a clearance result changes presentation and identifiers where necessary, not product semantics.

---
