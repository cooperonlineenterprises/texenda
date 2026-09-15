# ADR-0005: React Email editor as a reversible default

Status: AUTHORITATIVE LOCAL AMENDMENT — owner-requested reversible implementation
default on 2026-09-15. This exact repository candidate still requires independent
review/integration. No package compatibility, VAL-03 or product readiness is
established by the decision.

## Decision and authority boundary

This ADR is the sole project-local owner of the editor wording amendment.
React Email remains the renderer. Use `@react-email/editor` as the initial
composer in a custom Payload/Next view behind versioned `EmailDocumentCodec`.
Persist versioned TipTap JSON plus immutable compiled HTML/plain text and hashes;
retain subject/preview, renderer, asset/link and protected-fact revision bindings.
Payload owns authentication and draft administration; Payload Lexical is not
the canonical email representation and is not converted to email by default.

The later source variant supplies the refinement being selected locally.
Neither preserved 1.1.0 package is edited, promoted, merged or replaced. Their
eleven byte differences, original manifests/checksums and historical evidence
remain intact. Other sealed semantics and accepted local decisions retain scope.
This is a reversible implementation default, not a dependency installation or
authority to publish/send/activate anything.

## Exact amendment scope

Only the following editor wording/scope fields are superseded locally.
The files themselves remain byte-exact; this ADR governs interpretation of
these fields for future implementation.

| Preserved sealed path (under `specs/texenda-handoff/`) | Limited scope |
|---|---|
| `01-foundation/adr-set.md` | ADR-D01 editor portions of chosen approach, alternatives, rationale, consequences and revisit trigger; framework/persistence ownership unchanged. |
| `03-domain-and-architecture/technology-baseline.md` | React Email/editor reversible-default row. |
| `03-domain-and-architecture/content.md` | Section 9 initial composer, versioned email representation and qualification/fallback wording; other content/approval semantics unchanged. |
| `05-implementation/compatibility-manifest.template.json` | Meaning of `packages.email_editor`: named package/codec, version null and qualification UNVERIFIED until WP-10 evidence. |
| `05-implementation/work-breakdown.md` | WP-10 editor portions of Scope/output and Expected outputs. |
| `05-implementation/work-packages.json` | WP-10 `scope` and editor-related `expected_outputs`; dependencies, allowed paths, invariants, lifecycle and routing unchanged. |

ADR indexes, source-register observations, decision-status text and checksum
differences remain historical package records; they are not rewritten or adopted
wholesale. The existing VAL-03 gate and renderer/content acceptance boundaries
are retained, not superseded.

## Safety, fallback and qualification

Replace the editor's default extension set with the approved blocks: text,
heading, image, button, divider, callout, article/recipe card and immutable
compliance-footer structure. An installed extension is not approval to add a
template node. Arbitrary React, JavaScript and raw executable content are forbidden.
Imported HTML remains sanitized/quarantined for review; it does not become
executable UI.

If qualification fails, retain React Email with a small fixed-block composer.
Once documents exist, preserve old codec versions and compiled immutable outputs;
never discard unsupported JSON to force an editor upgrade. This amendment changes
no approval invalidation, protected-fact, permission, delivery or domain authority.

The exact editor package version is UNVERIFIED and unpinned. WP-10 and VAL-03
still require a compatible locked manifest, license/SBOM assessment,
peer/dependency closure, Next/React/Payload integration, JSON round trips,
build-performance measurements and deterministic email rendering fixtures.
No dependency is installed and no VAL-03 result is marked passed here.

## First-party observations

Retrieved 2026-09-15 UTC:

- [Editor overview](https://react.email/docs/editor/overview): the editor uses
  TipTap/ProseMirror and supports email-oriented exports. Its documented Prism
  dependency can slow Next.js development compilation; build performance remains
  a qualification concern, not a locally applied workaround.
- [EmailEditor API](https://react.email/docs/editor/api-reference/email-editor):
  structured TipTap JSON and HTML/plain-text export helpers are exposed, and the
  extension array can be replaced to enforce the approved schema.
- [Upstream releases](https://github.com/resend/react-email/releases):
  `@react-email/editor@1.7.7` was observed. That observation is not a selected,
  compatible or pinned version.

These are dated upstream observations, not a substitute for project fixtures or
a perpetual latest-version claim. Exact retrieval procedures and bounded local
checks are recorded under the existing qualification-evidence owner.

## Machine-readable local contract

This JSON block belongs to this ADR; validators consume it directly. It is not
a second editor authority.

<!-- texenda-editor-default-contract -->
```json
{
  "schema_version": "texenda.editor-default.v1",
  "amendment_owner": "docs/decisions/ADR-0005-react-email-editor-reversible-default.md",
  "status": "reversible_implementation_default",
  "renderer": "React Email",
  "composer": "@react-email/editor",
  "composer_version": null,
  "composer_qualification": "UNVERIFIED",
  "observed_release": {
    "version": "1.7.7",
    "retrieved_on": "2026-09-15",
    "selected": false
  },
  "host": "custom Payload/Next view",
  "document_codec": "EmailDocumentCodec",
  "codec_versioned": true,
  "canonical_email_document": "versioned TipTap JSON",
  "compiled_outputs": [
    "HTML",
    "plain text"
  ],
  "retain_hashes": true,
  "payload_lexical_is_canonical_email": false,
  "block_allowlist": [
    "text",
    "heading",
    "image",
    "button",
    "divider",
    "callout",
    "article/recipe card",
    "immutable compliance-footer structure"
  ],
  "default_extensions_automatically_approved": false,
  "arbitrary_react_allowed": false,
  "javascript_allowed": false,
  "raw_executable_content_allowed": false,
  "fallback": "React Email with a small fixed-block composer",
  "preserve_old_codecs": true,
  "preserve_compiled_outputs": true,
  "required_qualification": [
    "compatibility_manifest",
    "license_and_SBOM",
    "peer_dependency_closure",
    "Next_React_Payload_integration",
    "JSON_round_trip",
    "build_performance",
    "rendering_fixtures"
  ],
  "qualification_gate": "VAL-03",
  "qualification_gate_passed": false,
  "work_package": "WP-10",
  "dependencies_installed": false,
  "package_variants_modified": false,
  "source_package_promoted": false
}
```
