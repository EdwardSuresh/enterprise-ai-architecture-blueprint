# Use case spec: Standard work and SOP Q&A

Pack: `manufacturing`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over released SOPs and work instructions, current revision only. |
| Risk tier | Tier 2 |
| Autonomy | L0 |

## Business problem

Operators need quick answers on standard work. Paper binders and long documents slow them down and old revisions linger.

## Users

Machine operators, team leads, new hires.

## Pattern

RAG Q&A over released SOPs and work instructions, current revision only.

## Data

- Document control system (internal)

## Risk tier and autonomy

- Tier 2, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Retrieve only released, current revisions.
- MFG-G01 and MFG-G02 active.
- Show document number and revision with every answer.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Golden set accuracy
- Use of obsolete revisions (target zero)
- Supervisor escalations
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Area supervisors supply real operator questions with the governing step.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
