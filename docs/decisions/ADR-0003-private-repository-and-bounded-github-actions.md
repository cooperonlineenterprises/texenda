# ADR-0003: Private repository and bounded GitHub Actions

Status: AUTHORITATIVE DECISION — owner accepted the repository-visibility and CI
direction on 2026-09-14. Implementation status: candidate; independent review
and integration remain pending. This project-local decision does not amend
Texenda product semantics, the sealed handoff, external gates, or ADR-0001.

## Decision

Keep the GitHub repository private during implementation. Do not make it public
merely to obtain unmetered standard-runner minutes or public-repository
features. Public visibility is a separate, intentionally reviewed release
decision because public Git history cannot reliably be recalled after cloning,
indexing, caching, or forking.

A public transition requires all of the following:

1. explicit owner authorization for the exact repository and revision;
2. VAL-01 brand clearance for public use of Texenda, or a separately accepted
   neutral public identity that does not imply brand clearance;
3. a public-release audit of the complete reachable Git history and current
   tree for secrets, credentials, production or personal data, account
   identifiers, sensitive operational material, local paths, licenses and
   third-party redistribution obligations; and
4. review of repository settings, Actions artifacts/caches, issues, releases,
   packages and other already-hosted surfaces that a Git-only scan does not
   cover.

GitHub Actions uses the current private-repository allowance for the repository
owner's plan. Treat plan quantities, prices and billing-cycle dates as transient
observations, not permanent policy. The steady-state planning target is at most
75% of the then-current included allowance, retaining at least 25% for release,
security, migration and incident reruns. Additional Actions spend is zero unless
the owner separately authorizes a bounded amount and expiry. Usage pressure
causes cancellation, checkpointing, queueing or resumption; it never permits a
weaker verification oracle or a merge with required tests omitted.

WP-02 owns the first workflow implementation. Use standard GitHub-hosted Linux
runners by default, one pull-request verification path, a main-branch
post-integration path, bounded manual release qualification, cancellation of
superseded runs, explicit timeouts, safe dependency caching and short artifact
retention. Workflow permissions are read-only by default and third-party
actions are pinned to immutable commits. Production credentials, production
data and ignored local inputs never enter CI.

Do not introduce a self-hosted runner merely to avoid minute charges. It is
deferred until measured hosted-runner use justifies its operational burden and
WP-39 plus VAL-08 cover isolation, patching, ephemeral execution, credentials,
network policy, monitoring and incident response. Larger hosted runners,
scheduled jobs, paid minutes and deployment environments likewise require
explicit need, current cost evidence and owner authority.

Detailed operational rules are in the
[GitHub and CI policy](../operations/github-ci-policy.md).

## Evidence and advisory sources

The current GitHub repository was observed private with no remote branch on
2026-09-14. GitHub's current documentation was reviewed directly that day:

- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
  states that standard hosted-runner use is free for public repositories while
  private repositories consume the plan allowance, which resets by billing
  cycle; larger runners remain billable.
- [GitHub pricing](https://github.com/pricing) lists current plan allowances and
  public-repository benefits.

Those pages support the cost analysis but do not override project authority or
freeze today's quantities and prices.

## Consequences and alternatives

Private visibility preserves control over unfinished security, migration and
operational material and avoids crossing VAL-01 accidentally. CI must be
designed and measured rather than triggered redundantly. If required,
well-designed verification exceeds the included allowance, prefer a small
owner-capped hosted-runner budget or a plan change over weakening tests or
publishing the repository for cost avoidance.

Public open-source release remains available after deliberate clearance and
audit. Self-hosted runners remain available after measured need and security
qualification. Neither alternative is activated by this decision.

Changing visibility, pushing the initial branch, enabling Actions, setting a
spending limit, adding secrets or provisioning a runner changes external state
and remains separately authorized. This ADR itself performs none of those
actions.
