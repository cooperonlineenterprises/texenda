# Project-local harness — executable coordination scaffold

**Texenda implementation handoff 1.1.0 · 2026-09-05 · NORMATIVE**

MUST/MUST NOT are binding; SHOULD requires a recorded reason to depart; MAY permits but does not commit scope. Source: Accepted interaction architecture and complete-handoff directive. Apply [package authority](../DECISION-STATUS.md).


## Scope and trust boundary

This is a small Python standard-library coordinator for Texenda implementation work. It records task admission, dependency completion, bounded assignments, declared edit leases, context manifests, evidence hashes, independent review, integration and resumption.

It does **not** call model APIs, spawn subagents, sandbox a process, merge Git, provision cloud resources, deploy Texenda, authenticate actor strings or authorize production sending. An actor able to rewrite all local files can forge evidence. Hash chaining detects accidental changes relative to retained checkpoints, not a malicious owner rewriting the chain. Use actual coding-runtime sandbox/approval controls, protected integration branches and accountable human release review.

Supported execution environment: POSIX/macOS/Linux/WSL, Python ≥3.10; `fcntl` file locks protect single-host writes. No package installs required. Multi-host/shared-network-filesystem operation is not qualified. Work in separate Git worktrees; declared path leases prevent coordinator-assigned conflicts, but filesystem enforcement belongs to the runtime.

## Run the scaffold

From the unpacked handoff:

```sh
python3 -m unittest discover -s 08-project-harness/tests -v
python3 10-validation/validate_package.py
python3 08-project-harness/install.py --target /absolute/path/to/new-repo
# Review the dry-run, then use --apply only for a genuinely empty target (or .git-only).
python3 08-project-harness/install.py --target /absolute/path/to/new-repo --apply
```

The installer copies this package to `specs/texenda-handoff/`, writes a small root `AGENTS.md`, an example Codex configuration, and a `.gitignore`. It refuses to overwrite an existing application repository. It does not initialize Git or install dependencies. Repository construction is WP-00/WP-02 work.

In the target repository:

```sh
python3 specs/texenda-handoff/08-project-harness/harness.py --root . init
python3 specs/texenda-handoff/08-project-harness/harness.py --root . ready
python3 specs/texenda-handoff/08-project-harness/harness.py --root . context WP-00 --out .texenda/context/WP-00.json
python3 specs/texenda-handoff/08-project-harness/harness.py --root . admit WP-00 --actor astra
# Human-guided bootstrap is explicit, not a fabricated model binding.
python3 specs/texenda-handoff/08-project-harness/harness.py --root . assign WP-00 --actor astra --agent human:owner --tier 2 --human
# Use the fence returned above, not an assumed value after resumption.
python3 specs/texenda-handoff/08-project-harness/harness.py --root . status
```

Use `--help` for each command. After the actual runtime is qualified, an accountable human records a sanitized `roster` evidence envelope with model/effort/capability smoke-test logs. `set-roster` activates those mappings for local coordination. New API spending is denied until a `budget` record and explicit `set-budget` command authorize it. Subscription runs require separately bounded usage/time; they are not assumed costless.

## Task lifecycle

```text
planned → admitted → assigned → running → submitted → reviewed → integrated → completed
                          │          │          │
                          └──────────┴──────────┴→ blocked → proved recovery → admitted
                                                       └→ proved stop → cancelled
```

`ready` is derived from completed dependencies. Deferred WPs require observed `trigger` evidence. Assigning overlapping parent/child paths is denied even if the previous lease expired. `recover` requires current fence, observed revision and evidence the old runtime stopped. Cancellation similarly does not pretend to terminate a process.

A submission may truthfully include NOT_RUN; it cannot pass required review or complete until required checks have actual PASS evidence. Review must be independent from the author and at least the WP's review tier. Candidate revision, evidence hash and integrated head are checked. Semantic merge changes need a fresh reviewed candidate. Successful integration releases the declared edit lease only after author-runtime stop evidence.

## Evidence schema and template

Use `schemas/evidence.schema.json` and `templates/evidence.json`. Each PASS/FAIL check needs a log/procedure file and SHA-256. All paths are relative to the target repository, not arbitrary absolute paths; traversal and symlinks are refused. Required NOT_RUN/NOT_APPLICABLE checks do not pass. The reviewer verifies whether checks are sufficient for the WP; the CLI cannot infer that from a single passing log.

Record `kind` as submission, review, integration, checkpoint, recovery, roster, budget, gate or trigger. Integration needs `integrated_revision` and `runtime_stopped:true`; recovery needs `previous_fence`, `observed_revision`, and stop proof. Gate records identify actual scope and covered WPs with an expiry. An activation WP cannot complete against an unrelated gate scope. This is evidence bookkeeping, not legal certification.

## State, evidence and resumption

`.texenda/state.json` is atomically rewritten under a POSIX lock with fsync; receipts form a hash chain and bind a state digest. `check` detects unintended tampering and baseline mismatch. `state.lock` is an OS advisory lock, not a stale lease file to delete. Back up state after integration. Commit sanitized implementation evidence and handoffs under `evidence/implementation/`; keep live state/transcripts/credentials out of Git.

After restoring a state checkpoint, compare current Git integration head, actual processes/worktrees and externally recorded receipts. Reconcile discrepancies and stop old runtimes before recovering leases. Never treat restored completed-state records as proof that later effects or external qualification did not occur. Package WP baseline changes require an explicit reviewed state migration rather than automatic history rewrite.

## Review gates versus production gates

`complete` verifies local work evidence and, for activation WPs, gate evidence records. It never sends or deploys anything. Product acceptance remains the 125 NOT-RUN criteria until the implementation team executes them. This package's synthetic harness tests validate only the scaffold.
