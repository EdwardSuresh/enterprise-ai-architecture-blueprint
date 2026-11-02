# Use case spec: Nonconformance report summary and routing

Pack: `manufacturing`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Summarization and classification of NCRs, plus search for similar past NCRs. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

NCRs are written in free text with uneven detail. Routing to the right engineer and spotting repeat issues is slow.

## Users

Quality engineers, inspectors, plant quality managers.

## Pattern

Summarization and classification of NCRs, plus search for similar past NCRs.

## Data

- QMS NCR and CAPA records (confidential)
- Part master data (internal)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Suggest only; quality engineer decides disposition.
- MFG-G03 routes release and safety questions.
- Every similar-NCR suggestion links to its record.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Routing accuracy
- Time to disposition
- Repeat issues caught
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Quality engineers label past NCRs with the correct category and owner. Include safety-related NCRs.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
