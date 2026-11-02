# Use case spec: Public records request triage

Pack: `public-sector`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Classification of requests and search for candidate records; human decides release. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

Records requests are growing. Staff spend time finding responsive records and routing requests.

## Users

Records officers, legal staff.

## Pattern

Classification of requests and search for candidate records; human decides release.

## Data

- Records management system (confidential)
- Email archive (confidential)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- AI never releases records.
- Exemption and redaction decisions by records officer.
- Search access limited to the records team.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Time to first response
- Statutory deadline misses (target zero)
- Search recall on test requests
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Records officers build test requests with the known responsive records.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
