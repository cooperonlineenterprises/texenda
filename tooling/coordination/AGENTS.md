# Local coordinator instructions

Read the [operator README](README.md), [operating guide](../../docs/agents/operating-guide.md),
and [ADR-0001](../../docs/decisions/ADR-0001-quality-first-model-routing.md) for
coordination changes. Keep the sealed lifecycle code and package byte-for-byte
unchanged. This adapter coordinates local evidence; runtime permissions and
accountable owner authority remain separate.

Use the [assignment](templates/ASSIGNMENT.md), [review](templates/REVIEW.md), and
[resumption](templates/RESUME.md) prompts for new work. Read only the applicable
template, and include its hash with the local instructions in the dispatch
context manifest. The generated `context` command is a starting manifest, not
a complete prompt.

Preserve exact-profile qualification, max defaults, independent review,
closed evidence schemas, budget bounds, leases/fences, history and runtime-stop
proof. Prefer instructions and regression tests when those can close a workflow
gap; change executable behavior only for a demonstrated enforcement gap. Update
affected schemas, templates, docs and negative tests together when it changes.

Run the local coordinator suite, sealed suite and checksum-aware package
validation for material coordinator or instruction-contract changes, using the
README commands. Add no model, network, credential or production dependency to
these tests. Recheck existing evidence hashes, parse changed JSON/TOML, validate
local links, and run `git diff --check`. Once required checks pass, broaden only
for a new change, failure or unresolved concern. Passing checks do not attest
runtime entitlement, actual model identity, product acceptance or an external gate.
