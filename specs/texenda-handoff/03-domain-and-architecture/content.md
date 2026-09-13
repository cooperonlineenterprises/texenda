# Content and message model

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Formal foundation v1.0 plus accepted interaction architecture. Apply [package authority](../DECISION-STATUS.md).

<a id="f09"></a>
## 9. Content and message model

**Decision status: AUTHORITATIVE DECISION.** Use a lightweight communication brief plus independently approved, typed channel representations. Keep ordinary email authoring direct.

```text
Communication intent / purpose
     + approved facts, offer, CTA, validity and disclosures
     + brand-context revision
                 |
        channel-specific representation revisions
        email | onsite | push | qualified future channels
```

An operator may start in the email editor. Texenda derives the minimum brief from the draft: purpose, publication, approved links/offers, required variables, expiry and brand. Do not force a second abstract authoring exercise for a newsletter.

**REVERSIBLE DEFAULT:** React Email renders email; its editor is the initial visual-authoring dependency behind `EmailDocumentCodec`. The official editor exposes structured JSON and email-oriented rendering/export facilities, but its exact package version, license/dependencies, Payload integration and rendering fidelity require VAL-03 qualification. [S05](../09-reference/source-register.md#s05) If qualification fails, retain React Email with a small fixed-block composer; do not replace the content/approval model or stall identity work for a visual editor.

Store editor JSON with its schema/codec version, plus compiled HTML/plain-text template, subject/preview templates, renderer version, asset/link manifest and hashes. Do not execute arbitrary uploaded React/JavaScript or template code. Templates contain approved blocks: text, heading, image, button, divider, callout, article/recipe card, and immutable compliance-footer structure. Raw imported HTML is sanitized and quarantined for review; it never becomes executable UI.

A published representation pins template/theme, brand-context and protected-fact revisions. Protected facts include prices, dates, offer terms, claims, disclosures and canonical CTA destination/meaning. External systems remain authoritative for their facts; Texenda stores approved snapshots/references. A fact change/withdrawal marks affected unsent representations stale. A send must not continue using a known-withdrawn offer just because it was previously approved.

Personalization uses an allowlisted variable schema with type, source, escaping, required/optional status and explicit default. Missing required values hold the affected recipient; optional values use approved fallback text. URLs are validated separately from text. Compile and retain the resolved recipient payload/digest before an uncertain attempt; retries use exactly the same bytes and provider key. A new privacy withdrawal prevents retry even if the payload was prepared earlier.

Shared brand components may be reused across brands only through explicit target-brand adoption. Updating a shared source does not mutate published messages. AI channel/brand adaptation creates a draft with a difference view; required facts/claims/disclosures/CTA meaning cannot be silently changed. Each channel representation requires approval before it becomes sendable. SMS encoding, WhatsApp template variables, push lengths/deep links, and onsite placement/accessibility rules remain channel-specific.

**Downstream consequences:** editor replacement preserves old document codecs or compiled immutable versions; adding a channel does not turn email HTML into a universal content model. **Revisit:** add blocks or codecs for demonstrated content needs, with backward-compatibility tests and no expansion into general site building.

---
