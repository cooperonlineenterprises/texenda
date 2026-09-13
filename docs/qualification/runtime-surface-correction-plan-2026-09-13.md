# Runtime surface correction plan — version 1

Recorded: 2026-09-13. Status: REQUIRES EXTERNAL VALIDATION — replacement
qualification/owner attestation and live installation are pending. This plan is
a repository-local candidate, not a new roster or permission to dispatch through
an unqualified route. Base: `e636a3ef4ad3c96956164e898fefeec0758d444d`.

## Observations and limits

The installed bundle `/Applications/ChatGPT.app/Contents/Info.plist` reports
`CFBundleIdentifier=com.openai.codex`, `CFBundleShortVersionString=26.901.41600`
and `CFBundleVersion=7982`. These public bundle fields were read directly with
`/usr/libexec/PlistBuddy` on the recorded date. Separately, `codex --version`
returned `codex-cli 0.149.0` (exit 0, with a nonfatal PATH-alias permission warning).
Neither command accessed credentials or invoked a model.

The [current official availability guidance](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)
was retrieved on 2026-09-13 and requires Codex CLI 0.153.0 or newer for Astra.
Direct Astra CLI use is unqualified: the installed CLI is below that minimum and
no direct CLI read/edit/test qualification is present. Updating a client alone
would still not establish the target account's access or exact effort/tool support.

The existing [v2 roster](model-roster-v2.evidence.json) binds 11 exact profiles
to `codex-desktop-collaboration` but records `client_version: 0.149.0`. Its SHA-256
is `dbfd99b98edc134c1e202c0b48145141f967718194b67012f75a3868bf4ef6a1`.
The [activation receipt](routing-v2-activation-receipt.md) binds that exact record.
The [original inventory](runtime-inventory.json), probes and verification files
also retain this association. The probes exercised the desktop collaboration
dispatch, not a direct CLI model invocation. The CLI version therefore cannot
establish the desktop client version or CLI Astra support.

This correction preserves the recorded desktop read/edit/test outcomes and their
limitations. Exact requested model/effort selection was accepted by that runtime;
independent provider model introspection was unavailable. Today's bundle version
does not establish which app build executed an earlier probe. Do not replace
historical timestamps, retrofit today's build into old probes, or silently
extend qualification expiry.

## Replacement procedure

1. Preserve every existing qualification file and receipt byte-for-byte. Create
   a new dated runtime observation record with desktop bundle identity/version/
   build separate from installed CLI identity/version. Identify the actual
   dispatch surface, account/sign-in/billing mode, effective sandbox/approval
   settings and observation time without tokens or account identifiers.
2. For each profile to retain, gather fresh bounded read/edit/test evidence on
   that exact desktop model/effort/route, or obtain independently reviewed
   contemporaneous route/build evidence sufficient to correct attribution
   without inventing a new test result. The latter must retain original probe
   dates/expiry and explicit limits. No evidence is transferred to direct CLI.
3. Prepare a new schema-2 roster record under a new filename. For desktop rows,
   use `runtime_id: codex-desktop-collaboration` and a `client_version` describing
   the observed desktop version/build, not the separately installed CLI. Link
   every qualification to its exact PASS checks and the new runtime observation.
   Preserve the current routing-policy digest, native tier, model/effort and
   subscription billing. Use true validity windows of at most 30 days; keep
   unverified profiles out of the new roster.
4. Independently review the replacement, all evidence hashes and route/version
   distinctions. Before owner-attested `set-roster`, inspect live `check` and
   `status`, current worktrees and leases. Stop/recover affected assignments
   before replacing their pinned qualification. Replacement invalidates prior
   assignment bindings; never edit the ledger or old record to avoid recovery.
5. With accountable owner attestation, install the new record through the local
   coordinator, recheck integrity/status, and append a new activation receipt
   identifying old/new roster hashes, profile set, qualification limits and
   observed live state. Retain the earlier receipt as history. This audit does
   not execute these live steps.

A future direct CLI route needs an allowed updated CLI (at least the currently
documented 0.153.0 minimum), freshly checked official requirements, actual
account access, exact model/effort/tool tests and a distinct route qualification.
The current schema holds one active qualification per exact profile, so it cannot
activate desktop and CLI versions of the same profile simultaneously. Deliberate
route replacement or a separately reviewed schema/policy migration is required;
do not create duplicate rows or pretend the routes are interchangeable.

The new repository config applies to new trusted-project sessions and must be
checked on the actual runtime; parsing it is not a launch or entitlement test.
API budget and declared spend remain zero. No reset, upgrade, paid credit, live
roster change, production access or external gate is authorized by this plan.
