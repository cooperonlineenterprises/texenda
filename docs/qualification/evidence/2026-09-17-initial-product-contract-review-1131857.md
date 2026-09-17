# Independent contract review — correction required

Dated 2026-09-17. Immutable record of a bounded semantic review, not candidate
approval or product acceptance. Later correction/re-review is separate evidence.

- Base: `d3556d0718e558fa3a12cf628add58dd71a0008c`
- Reviewed candidate: `113185776c124116ce0d3b51e9da7234ebd452d3`
- Candidate tree: `023335c7e047027b2c1c9ba7b69598133453370f`
- Full-index binary base-to-candidate diff SHA-256: `5e6838d027a7917b2a5a92bad41859975d2192647634ab1829b8fdcd31af8fa4`
- Author/integrator: `/root`
- Independent reviewer: `/root/integrated_release_reviewer`
- Requested and live-qualified profile: `gpt-6-astra/max`, desktop collaboration,
  subscription, no fallback, API USD 0; expiry `2026-10-12T21:44:31Z`.
- Qualification rechecked before dispatch at `2026-09-17T15:41:29Z`.
- Review bounds: 1800 seconds / 16000 tokens; measured provider tokens unavailable.
- Method: exact Git blobs and read-only in-memory graph/reference/hash checks;
  not the author's uncommitted working tree. No product or engine tests claimed.
- Stop: reviewer reported all subprocesses exited; collaboration returned final
  completion. No author/reviewer scope is released on lease expiry alone.

## Findings at this exact candidate

1. **P1 — readiness/activation cycle.** `initial-production` included actual
   transfer/canary/observation criteria, notably AC-M07 and AC-M09. WP-20 required
   that profile before activation and depended on WP-17. Removing AC-IP18 alone
   had not removed the cycle. Do not infer or falsely pass post-activation proof.
2. **P2 — native acquisition approval dependency missing.** WP-12/AC-IP02 promised
   complete page approval/publication but its dependency closure omitted WP-15,
   owner of shared Proposal/Approval services and review UI. WP-13's later
   dependency did not protect WP-12.

Neither finding is approved away by this record.

## Other observations and limits

The reviewed WP/profile graphs were acyclic as graphs; the P1 defect was a
semantic evidence-stage cycle. Synthetic closure contained no forbidden
real-discovery/cutover/voice/channel WPs or external gates. WP-29 retained WP-27;
WP-26 moved earlier; local versus real WP-39/41 evidence remained distinguished.
Integrated contextual AI, manual fallback, preferred structured tools, deliberate
computer use, native pages/resources, fresh cloning, recipes, canonical Publication
and brand isolation were present. All 18 extension rows were NOT_RUN and the three
sealed source hashes matched. These observations do not approve the engine or
unperformed application.

## Submitted corrections, still requiring combined candidate re-review

`78c6d4a1bdfc5592eb8adb33ffe4a7e935a4cbe7` adds WP-15 to WP-12; moves
actual-transfer AC-M04/05/06/07/09 applicability to rollout/email-pilot completion;
adds WP-20 to email-pilot; retains preactivation inventory/dry-run/recovery and
transfer-readiness proof; and scopes WP-18 to source inventory rather than actual
transfer. `34133e7c1e8715e902d11882131ecf7ec931f808` removes a duplicate WP-18
replace/append acceptance delta caught by the strict loader.

Final source+engine+facade review must recheck both fixes and all negative tests.
These references preserve failed candidates and do not transfer approval to any
new revision. No files/state/accounts were changed by the reviewer.
