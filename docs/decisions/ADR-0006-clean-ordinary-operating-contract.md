# ADR-0006: Clean ordinary operating contract

Status: AUTHORITATIVE LOCAL DECISION — owner-supplied on 2026-09-15. This
decision supplies no candidate approval; review evidence, not this document,
binds each approved implementation revision.

## Decision

Normal Texenda work begins in
`/Users/jamesryancooper/Projects/texenda/repo`. The non-Git project home is
navigation and local-storage structure; it is not a second repository or
instruction root. A newcomer should be able to read `AGENTS.md`, validate the
repository, inspect live status and ready work, prepare an assignment, and use
the existing review/resumption templates without reading migration history.

The ordinary repository-root validation command is:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
```

The explicit absolute state root remains visible. No wrapper may silently
discover, initialize, substitute, or fall back to another ledger. The active
binding continues to fail closed when the option is missing or wrong. Direct
CLI model execution remains unqualified; desktop qualification evidence does
not transfer to another runtime merely because a command is available.

“Read-only” validation means no explicit project writes and preservation of
content, path membership, mode, size, mtime, ctime, generated outputs, caches,
locks, and live state. An operating system may advance a file's access time
(`atime`) when validation reads it. Portable Python cannot prevent or restore
that filesystem-managed update without mutation, so atime stability is outside
the portable no-write guarantee and must not be claimed by review evidence.

Current navigation leads to ordinary work. The detailed completed workspace
procedure is retained byte-for-byte as history, with its hash and successor
recorded. Recovery instructions that still protect live receipts remain
available through the coordinator and transition maintenance routes.

## Scope and supersession

This ADR supersedes only stale present-tense operational interpretations in
ADR-0001, ADR-0004, and ADR-0005 that describe already integrated local routing,
workspace, facade, external-state, or editor-default records as one still-pending
candidate. Those statements remain accurate historical snapshots of their own
decision epochs. Their routing, workspace, recovery, preservation, editor,
qualification, and gate semantics are unchanged.

This decision does not amend sealed product semantics, rewrite either handoff
package, qualify a Blueprint or runtime, create a second authority, mark product
work ready, pass an external gate, or authorize any external effect. Every future
consequential candidate still requires exact independent review under its
governing contract.
