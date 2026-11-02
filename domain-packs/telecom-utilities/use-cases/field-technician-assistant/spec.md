# Use case spec: Field technician knowledge assistant

Pack: `telecom-utilities`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over field procedures and equipment manuals on a mobile device. |
| Risk tier | Tier 2 |
| Autonomy | L0 |

## Business problem

Technicians need procedure and equipment answers in the field. Manuals are long and connectivity varies.

## Users

Line workers, network technicians, field supervisors.

## Pattern

RAG Q&A over field procedures and equipment manuals on a mobile device.

## Data

- Field procedures and equipment manuals (internal)

## Risk tier and autonomy

- Tier 2, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Answer only from current procedures with citations.
- TU-G01 blocks equipment control; TU-G04 handles hazards.
- Safety steps are never summarized away.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Golden set accuracy
- Time to answer
- Safety observations linked to procedure errors
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Field supervisors provide real questions with the governing procedure step.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
