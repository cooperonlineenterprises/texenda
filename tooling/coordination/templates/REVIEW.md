# Independent review — <task ID and candidate>

Status: TEMPLATE. Fill before review; no approval is pre-recorded.
Use the [operating guide](../../../docs/agents/operating-guide.md) and the
[version-2 review envelope](review.json) when recording model review.

| Contract field | Required value |
|---|---|
| Candidate and base | <full exact candidate/base revisions; author identity; changed paths/hashes> |
| Reviewer route | <different actor; required reviewer floor; exact profile/model/effort/runtime/client; current qualification and billing route> |
| Authority and context | <assignment; accepted contracts/ADRs and hashes; policy digest; applicable instructions; this template hash> |
| Review scope and oracle | <required checks, negative/concurrent paths and evidence; forbidden writes; bounded independent reproductions> |
| Bounds and usage | <time/tokens and remaining allocation; API USD; subscription usage availability or unknown> |
| Decision and stop | <findings with evidence or approval of this exact candidate; NOT RUN checks; limits; actual process/stop state> |

Independently inspect the diff, contract compliance and sufficiency of evidence.
Reproduce material failure paths proportionately; do not substitute the author's
assertions for required verification. Preserve sealed specifications, historical
hashes, safety controls and product gates. Any semantic candidate change
invalidates this review. Do not edit the candidate merely to make it pass.

Usage pressure is not authority to reduce reviewer capability, effort, depth or
required checks. If interrupted, preserve the partial review with unverified
items explicit, use [RESUME.md](RESUME.md), and do not record approval. Keep
model identity, account access and runtime enforcement limits visible. Report
actionable findings plainly, bound to exact files/revisions and their consequence.
