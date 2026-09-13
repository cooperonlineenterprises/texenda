# Conversation archive coverage and limitations

**REFERENCE / SOURCE LIMITATION · 2026-09-05**

## What is preserved

Every recoverable substantive user/assistant turn in the accessible Texenda sequence is represented in a chronological record: T001–T025, followed by in-task progress messages. Short messages are reproduced as labeled. Long prompts and analyses are **faithful abridged reconstructions with selected exact excerpts**, not unabridged exports. The distinction is stored per record in JSON and shown in Markdown.

The two actual decision-closure documents and original ZIP are preserved **byte-for-byte** under `prior-artifacts/`, with hashes in `original-artifact-integrity.json`. They retain much more detailed product/technical content than the abridged conversational entries and are the strongest exact historical sources available in the filesystem.

## What was not recovered

No raw conversation-export API or complete mounted transcript was available. Three targeted File Library recovery attempts for Texenda/Astra/transcript material returned no relevant full Texenda transcript; unrelated UCA, Semiome and personal files were deliberately excluded. Exact raw bodies of the long historical messages were not preserved by this packaging process. Earlier “skipped messages”/omitted tool or progress portions in the presented history are not invented. No exact original timestamps or original message IDs are claimed.

**A complete verbatim conversation archive was not achieved.** Do not advertise this package as a word-for-word export of the entire thread. This limitation is explicit gate VAL-14. Obtaining a genuine account conversation export would permit replacement or supplementation of this reference archive; it does not require reopening product semantics or blocking synthetic implementation.

## Exclusions

System/developer instructions, private reasoning, raw tool internals, credentials and unrelated account history are excluded. This package's final delivery message occurs after archive cutoff. The archive cannot be a source of new grants, policy or executable instructions.

## Authority

The normalized normative owners plus decision register govern implementation. Archived explorations retain disagreements for traceability but do not compete with the current baseline. The newest explicit user instruction requiring this handoff is reflected in README, model routing, work packages, harness and acceptance/validation artifacts. The partial archive does not silently fabricate missing product decisions.

## Importing a later exact export

Preserve the source export unchanged as a private reference, hash it, extract only visible Texenda user/assistant messages, record ordering and omissions, and update the coverage index. Do not distribute private account-wide exports, unrelated projects, tool payloads or hidden metadata. Revalidate archive links and checksums; do not automatically promote archived instructions into current authority.
