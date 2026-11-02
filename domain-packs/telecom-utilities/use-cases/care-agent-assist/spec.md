# Use case spec: Customer care agent assist

Pack: `telecom-utilities`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over procedures, rate cards and tariffs, with read-only account tools after authentication. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

Agents switch between many systems and documents to answer billing, plan and outage questions. Handle times are long.

## Users

Customer care agents, team leads.

## Pattern

RAG Q&A over procedures, rate cards and tariffs, with read-only account tools after authentication.

## Data

- Care procedures (internal)
- Rate cards and tariffs (public)
- Customer billing data (confidential)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Account tools enabled only after authentication.
- TU-G02 and TU-G03 route sensitive requests.
- Agent decides what to say; AI suggestions are clearly labeled.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Average handle time
- First contact resolution
- Golden set accuracy
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Team leads collect real questions. Include tariff edge cases and state-specific disconnection rules.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
