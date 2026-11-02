# Use case spec: Caseworker case summary

Pack: `public-sector`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Summarization of case notes and documents into a structured brief. |
| Risk tier | Tier 3 |
| Autonomy | L1 |

## Business problem

Caseworkers read long case histories before each contact. Key facts are hard to find.

## Users

Caseworkers, supervisors.

## Pattern

Summarization of case notes and documents into a structured brief.

## Data

- Case management system (restricted)

## Risk tier and autonomy

- Tier 3, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Summary only; no eligibility recommendation.
- Every fact cites the source note.
- Impact assessment completed before launch.
- Bias review of summaries across groups.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Preparation time per case
- Factual error rate in audits
- Caseworker trust survey
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Supervisors select de-identified cases with expected key facts. Over-sample complex and appeal cases.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
