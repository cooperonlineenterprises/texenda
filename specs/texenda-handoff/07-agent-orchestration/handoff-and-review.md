# Agent handoff, verification and recovery protocol

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Accepted interaction architecture and complete-handoff directive. Apply [package authority](../DECISION-STATUS.md).


## Assignment contract

Use the machine WP as the parent. Subtasks may narrow scope but cannot add authority. Record task ID/fence, repository/base commit, contract refs and hashes, permissible files, objective, output contract, exact tests, tier selection and rationale, budget/time, expected integration points and stop conditions. High-consequence mixed WPs SHOULD be split into reasoning-contract and bounded implementation subtasks before dispatch.

The supplied CLI coordinates the 44 parent work packages. Fine-grained subtasks are bounded assignment records linked to their parent; until a subtask is explicitly added through a reviewed plan update, it does not gain an independent harness lease. One parent writer can delegate read-only analysis or create disjoint child worktrees under its coordinated scope; Astra still owns the parent lease and integrates serially. Do not spawn conflicting writers merely because the CLI lacks child rows.

## Agent completion packet

A handoff MUST contain candidate revision (full Git commit or artifact-tree SHA-256), changed paths and hashes, accepted interface versions, test commands/procedures with environment/output/exit result, acceptance IDs, remaining NOT RUN checks, known limitations, current process/branch state, and resumption instructions. “Tests pass” without logs or “ready for production” without external evidence is insufficient.

The author stops before changing invariants, legal assumptions, provider semantics or review gates. A failed command is not automatically an architectural problem; inspect deterministic environment errors before requesting a stronger model. After repeated substantive failure, stop and hand off evidence rather than restarting without history.

## Independent verification

The reviewer is a different human/agent from the author. It independently checks the diff, scope, contract compliance, negative/concurrent paths and evidence. Stronger review is mandatory where prescribed by the WP. The local harness can verify identity labels, hashes and state transitions; it cannot prove actor identities or the truth of a test report. Runtime controls and accountable review supply those guarantees.

The reviewer binds approval to the exact candidate. A changed candidate invalidates review. An integration that changes semantics due to conflict resolution returns for review. CI and affected acceptance tests run against the integrated head. Retain original and integrated commits so the work can be audited.

## Leases and safe parallelism

A lease is an exclusive declared write surface; nested paths conflict. Expired leases stay blocking until the previous runtime is proved stopped. The CLI does not kill a process and does not restrict filesystem writes. Use separate Git worktrees and actual sandbox permissions. Do not share production credentials or a browser owner session with coding agents.

Contract files, generated code inputs, migrations/manifest, lockfile and common UI primitives have one integration owner. Readers may inspect accepted snapshots; readers must not depend on an unreviewed moving branch. Astra serializes merges and records the resulting head.

## Resumption and recovery

Run `status` and `check`; inspect checkpoint, current worktrees and repository head. If execution status is uncertain, treat it as running until the runtime is stopped or isolated. Record stop/recovery evidence at the current fence and observed revision, then `recover` to obtain a new fence. Never erase `.texenda/state.json` to clear a lock. A restored state checkpoint is not proof that external runtime work stopped; revalidate before resuming.

Failed/rejected work can return to running with the same lease only while its owner and fence remain valid. Expired or replaced executions require recovery. Partial outputs are retained in history. A completed WP records an integration receipt; it does not mean all future release-profile tests are passed.

## Definition of done

Scope implemented; contract unchanged or explicitly approved; required checks actually run and passed; security/negative paths covered; docs/contracts updated; no secrets/PII; independent review bound to candidate; affected tests rerun at integrated head; prior runtime stopped; handoff complete; applicable external activation gates satisfied; receipt recorded. Deferred or blocked activation remains visible and cannot be marked production-complete by omitting a test.
