# Use case spec: Employee policy and procedure Q&A

Pack: `financial-services`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over approved internal policies, with citations. |
| Risk tier | Tier 1 |
| Autonomy | L0 |

## Business problem

Front-line staff search long policy manuals to answer routine questions on limits, fees and procedures. Answers vary by person and branch.

## Users

Branch staff, contact center agents, operations analysts.

## Pattern

RAG Q&A over approved internal policies, with citations.

## Data

- Policy and procedure library (internal)
- Fee schedules and rate sheets (public)

## Risk tier and autonomy

- Tier 1, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Answer only from retrieved policy text; say 'I don't know' otherwise.
- Cite document ID and section for every answer.
- FS-G01 and FS-G03 apply if staff paste customer questions.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Answer accuracy on golden set at or above the agreed threshold
- Time to answer versus baseline
- Share of answers with a valid citation
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Collect 100-300 real staff questions from contact center logs. Policy owners write the expected answer and the source section. Include questions where the right answer is 'not covered'.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
