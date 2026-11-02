# Use case spec: Staff policy and procedure Q&A

Pack: `healthcare`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over current policies with citations. |
| Risk tier | Tier 1 |
| Autonomy | L0 |

## Business problem

Staff need quick answers on nursing, infection control and privacy policies across many documents.

## Users

Nurses, unit clerks, support staff.

## Pattern

RAG Q&A over current policies with citations.

## Data

- Policy and procedure library (internal)

## Risk tier and autonomy

- Tier 1, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- No PHI in questions; redact if present.
- Answer only from current policy; show policy number.
- Clinical judgment questions route to charge nurse.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Golden set accuracy
- Policy owner review findings
- Usage by unit
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Policy owners collect real questions. See evals/golden.jsonl for examples.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
