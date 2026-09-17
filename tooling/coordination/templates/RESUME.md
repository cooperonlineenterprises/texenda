# Checkpoint and resumption — <task ID>

Status: TEMPLATE. A checkpoint is not completion, approval or runtime-stop proof.
Use the [operating guide](../../../docs/agents/operating-guide.md) and existing
checkpoint/recovery evidence envelopes; do not invent a new lifecycle state.

| Contract field | Required value |
|---|---|
| Code and control roots | <exact candidate code root/revision; canonical control/evidence root; explicit bound state root; code versus control checks; no copied binding/ledger/receipt inputs> |
| Cause and observation | <usage window/reset or other interruption; date/time/timezone; source; unknown fields> |
| Intervention and resumption | <quota/tool/safety/approval/unknown cause; provider pause/end and resumable/nonresumable/unknown disposition; available action evidence; required owner/security/runtime review; unresolved effects> |
| Goal and authority | <original scoped objective; accepted decisions; pending material decision and owner> |
| Repository state | <worktree/branch; full candidate and accepted integration revisions; uncommitted paths/hashes> |
| Coordination state | <receipt tip/integrity; parent lease/fence/owner/expiry; checkpoint reference/hash> |
| Effective plan | <state version and active digest; unchanged source refs and assignment context; old sealed/unbound context cannot resume amended work> |
| Runtime state | <agent/process identity; running/stopped/unknown; actual stop/isolation evidence; previous fence> |
| Exact route | <profile/model/effort/runtime/client/billing mode; qualification ref/hash/expiry; policy digest> |
| Completed and outstanding | <outputs; actual commands/logs/exits; required NOT RUN checks; review and integration status> |
| Remaining bounds | <authorized time/tokens/API allowance remaining; observed subscription windows and reset times or unknown> |
| Next safe action | <specific continuation; dependencies/gates to recheck; recovery/new fence if required> |

Before resuming, inspect actual state and current qualification, not chat memory.
Preserve other actors' edits and all history. A blocked task or expired lease
still blocks conflicting work until prior execution is proved stopped or
isolated and recovery records a new fence. A fresh fence does not refresh the
owner's time/token/spend allowance. If qualification, candidate, authority or
scope changed, obtain the required fresh binding/review before dependent work.

Keep the selected qualified model, effort, review requirements and required
checks intact. No silent downshift, fallback, API switch, automatic reset
redemption or credit purchase is authorized by a usage interruption. If unable
to continue, preserve this handoff without marking the task complete or promising
background work. Product criteria and external gates remain separately governed.

A quota reset is not safety clearance. Never automatically resume, reset,
fallback or switch surfaces around a provider safety/misalignment intervention.
Preserve available evidence and obtain the applicable review and qualification;
a nonresumable provider stop stays nonresumable. Record these observations in
existing evidence `notes`/checks, without adding unrecognized schema fields.
