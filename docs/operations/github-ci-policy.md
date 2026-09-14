# GitHub repository and CI operating policy

Status: project-local operating policy. Apply this guide when WP-02 creates
GitHub workflows and whenever repository visibility, CI triggers, runners,
permissions, secrets, artifacts or Actions spending changes. ADR-0003 owns the
private-repository decision. The sealed work-package contracts and applicable
external gates remain controlling.

## Visibility and data boundary

The repository remains private. Public visibility is not a CI optimization.
Before any public transition, complete ADR-0003's VAL-01 and public-release
audit requirements against the exact revision and GitHub-hosted surfaces.

Never commit, cache, upload as an artifact, print to logs, or expose through a
workflow:

- .texenda/ or its private inputs and coordination state;
- raw Kit exports, subscriber rows, production fixtures or other personal data;
- environment files, credentials, tokens, private keys or provider secrets;
- production database snapshots, journals, rendered recipient content or
  unsanitized incident evidence.

Tracked migration inventory contains sanitized schemas, counts, hashes and
redacted findings only. Synthetic fixtures must be demonstrably synthetic.
Git ignore is a guardrail, not proof that data is absent from history or Actions
artifacts.

## Admission and allowance

At WP-02 and after a plan, owner, billing or material workflow change, record
the current included Actions allowance, billing-cycle boundary, storage
allowance, runner prices and whether overage is blocked. Do not copy those
transient numbers into this policy.

Plan steady-state CI to consume no more than 75% of the currently included
private-repository allowance and reserve at least 25% for release, security,
migration, recovery and incident reruns. Additional Actions spend is zero by
default. Paid minutes, larger runners or a higher spending limit require an
owner record with scope, maximum amount and expiry.

Measure per-workflow duration, queue time, cancellation, retry, cache and
artifact-storage behavior. Revisit the design using actual runs. A quota warning
stops new nonessential dispatch and preserves required evidence. It cannot
change a required test to NOT RUN and still authorize merge or release.

## AI review and local integration

A qualified AI author may hand a local candidate to a different qualified AI
reviewer, and an AI implementation lead may integrate an approved candidate
into local main without operator involvement. Follow the current model-routing,
lease/fence, evidence, runtime-stop and serialized-integration contracts.

Review must identify the exact candidate and base, inspect the real diff and
changed paths, recompute referenced hashes, run contract-required checks and
record actionable findings or approval. Integration is denied if the candidate
changed, evidence is missing, a required check did not pass, either write scope
is still active, main is dirty, or conflict resolution would change semantics.
Rerun affected checks after integration.

Local integration authority ends at the repository boundary. It cannot push the
branch, enable a workflow, change visibility/settings, configure secrets or
spending, provision a runner/environment, deploy, publish or clear an external
gate. An operator is unnecessary for the deterministic local review/integration
path but remains required wherever project authority assigns an external or
human-owned decision.

## Trigger and concurrency contract

WP-02 should implement one coherent verification path:

- pull_request runs the checks required before integration;
- push runs post-integration verification only on main;
- workflow_dispatch permits bounded release, recovery or diagnostic runs;
- schedule is absent by default and requires a documented need, owner,
  frequency, timeout and usage estimate.

Do not also run an equivalent all-branches push workflow for commits already
covered by pull_request. Give each workflow a concurrency group derived from
workflow and ref, with cancel-in-progress enabled for superseded, non-release
runs. Release, migration and recovery runs are not cancelled unless their
contract explicitly proves cancellation safe.

Every job has timeout-minutes and least-privilege permissions. Use standard
GitHub-hosted Linux runners unless a contract requires another platform.
Parallelize for useful latency only; unnecessary matrices and sharding may
increase total usage.

## Verification layers

Select checks by affected contract and consequence:

1. Pull request baseline: formatting, lint, type checks, unit tests, contract
   and schema validation, dependency-boundary checks, migration/static safety
   checks and changed-document links.
2. Consequential pull requests: add the required PostgreSQL, security,
   concurrency, migration, rendering, browser or fault tests before merge.
3. Main: rerun affected integration/build checks against the serialized
   integrated revision.
4. Release qualification: run the complete profile-required suite and external
   gate evidence only when the release candidate and environment are explicit.

Path filtering may avoid unrelated expensive jobs, but authority, permission,
effect, recovery, migration, shared-contract and workflow changes run every
test required by their contract. Local success does not replace a required
independent CI or review boundary. Usage pressure never justifies skipping a
required test; checkpoint and resume instead.

Cache only dependency and tool inputs derived from reviewed lockfiles and
versioned keys. Do not cache build output across incompatible trust boundaries.
Keep artifact retention to the shortest period required by review/recovery and
upload only sanitized evidence needed after the job.

## Workflow security

- Set workflow and job permissions read-only by default; grant the smallest
  named write permission only where required.
- Pin third-party actions to full immutable commit SHAs and review updates.
- Do not expose secrets to untrusted pull requests.
- Do not use pull_request_target to check out or execute untrusted contributor
  code with elevated tokens or secrets.
- Keep build/test jobs unable to contact production transports, databases,
  object stores or provider accounts.
- Separate deployment workflows and environments from CI. Their creation,
  secrets and execution require the applicable owner authority and product
  gates.
- Bound retries. Preserve a real failure instead of repeatedly spending minutes
  until a flaky check happens to pass.

## Runner policy

Standard GitHub-hosted Linux is the default. A larger or non-Linux runner needs
a contract-specific reason and current cost evidence.

A self-hosted runner is deferred until hosted-runner measurements establish a
material need. Any proposal must be reviewed under WP-39 and VAL-08 and cover a
dedicated isolated host, patching, ephemeral clean execution, network egress,
secret scope, untrusted-code policy, monitoring, shutdown/revocation and
incident recovery. Do not attach an ordinary workstation or a machine with
production credentials simply to avoid Actions charges.

## Public-release audit

Public release is a separate bounded task. It must inspect all reachable refs
and history, not only the current checkout; scan for secrets and personal or
production data; review local paths, author metadata, licenses and vendored
assets; and inspect GitHub-hosted Actions logs/artifacts/caches, packages,
releases, issues and settings. Resolve every finding before visibility changes.
Record the exact revision, scan procedures, limitations, VAL-01 disposition,
independent review and owner approval.

Making the repository public does not clear a production release gate, and a
private repository does not authorize putting production data or secrets in
Git.
