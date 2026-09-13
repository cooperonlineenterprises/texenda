# Decision lineage and supersession

**REFERENCE / TRACEABILITY.** Implementation authority is assigned by `../DECISION-STATUS.md`; this index explains provenance without reopening settled choices.

| Current decision | Primary provenance | Earlier idea superseded or qualified |
|---|---|---|
| Email-led small-team product; qualified channels | T013/T015 correction; T017/T018 expansion; exact Foundation §1 | Cross-brand intelligence as the product's center; broad omnichannel suite |
| Working Texenda, public clearance unresolved | T019/T020; exact Foundation §2 | Earlier naming winner interpreted as legal clearance |
| Payload draft/admin infrastructure; explicit domain transactions | exact Foundation §4; ADR-G02 | Every entity a generic Payload collection; hooks as execution engine |
| Identity/endpoint/permission distinct | exact Foundation §5–6; ADR-G04/G05 | One email string automatically proves one human; lists imply consent |
| Withdrawal distinct from safety suppression; scoped reconsent | exact Foundation §6; ADR-G05 | One generic unsubscribed/suppressed flag |
| One workflow executor | exact Foundation §8; ADR-G10 | Separate sequence and automation engines/cursors |
| Atomic pressure/equivalence before live mail | exact Foundation §6/8; T018 | Deferring all recipient coordination until channels exist |
| Independent recovery journal, outbound-held restore | exact Foundation §4/8; ADR-G11 | Database PITR alone makes external sending recoverable |
| Fenced Kit authority transfer | exact Roadmap §16.3; ADR-G17 | Dual sending or guessed recipient sequence progress |
| Object-first voice-forward, shared commands, Inspect | T023/T024; handoff ADR-G21/G25 | Chat as truth, mandatory voice, separate privileged agent app |
| Proposals/approval before writable AI | T024; ADR-G23; current WP graph | Build assistant mutations first and add review later |
| Explicit goals/preferences; no inferred policy memory | T024; ADR-G22 | Durable goals exist only in chat or model memory |
| External delegated principals, structured tools first | T024; ADR-G24 | Agents inherit human browser authority or provider keys |
| File-native Astra implementation harness | T025; ADR-G26/D09 | General harness framework or product AgentRun used for coding tasks |
| Model candidates separate from actual availability | T025; N01; runtime probe; ADR-D09 | Static assumed model names or strongest model for all work |

## Exact reference anchors

`prior-artifacts/Texenda_Product_Technical_Foundation_v1.0.md` and `prior-artifacts/Texenda_Implementation_Roadmap_Acceptance_v1.0.md` are the unchanged formal source artifacts. Current topic ownership is mapped in `../01-foundation/section-map.md`. Conversation entries are in `conversation-record.md`; their preservation fidelity is explicitly limited. External observations are in `source-register.json`.

## Interpretation fixes made during packaging

The previous human-agent prose called the C0…C4 scale “four” levels while enumerating five: use **five classes**. ApprovalRecord is an alias for the established Approval concept, not a second approval database. “Conversation for intent” does not make source transcript authoritative. New tag/attribute mutations can trigger existing workflows, so consequence classification must evaluate transitive effects before an AI mutation is committed. A scoped one-click withdrawal stays account-free even though withdrawal is consequential; generic high-risk UI rules cannot obstruct recipient opt-out.

The work graph retains original PH-00…PH-10 identifiers and adds IX tracks. A goal marked achieved by an operator is not verified business activity. The local harness's receipts are engineering evidence, not Texenda's production DecisionReceipt/Approval authority. None of these clarifications authorizes wider product scope.
