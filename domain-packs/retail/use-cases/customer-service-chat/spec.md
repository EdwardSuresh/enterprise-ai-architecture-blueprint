# Use case spec: Customer service chat

Pack: `retail`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over published policies plus read-only order lookup tools; handoff to agents. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

Contact volume spikes at peaks. Most questions are about orders, returns and shipping, and answers must match current policy.

## Users

Online customers; customer service agents for handoffs.

## Pattern

RAG Q&A over published policies plus read-only order lookup tools; handoff to agents.

## Data

- Customer service knowledge base (public)
- Order management system (confidential, signed-in customer only)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- All RET rules active on input and output.
- PII redaction and prompt-injection check on every turn (kit.guardrails).
- Disclose to the customer that they are chatting with an AI assistant.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Containment rate with satisfaction above target
- Policy accuracy on golden set
- Card data captured in logs (target zero)
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Use real chat transcripts. Customer service leads write expected answers from policy. Include adversarial prompts and card-number attempts.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
