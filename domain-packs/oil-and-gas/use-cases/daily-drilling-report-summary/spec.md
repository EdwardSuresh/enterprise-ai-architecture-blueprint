# Use case spec: Daily drilling report summary

Pack: `oil-and-gas`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Summarization of the structured daily report into a fixed template: depth, operations, NPT, HSE, risks, plan. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

Managers and engineers read many long daily drilling reports each morning. Key events such as pit gains, NPT and HSE cases can be missed.

## Users

Drilling superintendents, drilling engineers, asset managers.

## Pattern

Summarization of the structured daily report into a fixed template: depth, operations, NPT, HSE, risks, plan.

## Data

- Daily drilling reports (confidential)
- Well plan (confidential)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Every number must appear in the source report (grounding check).
- Safety-critical events must always be included; never summarized away.
- OG-G02 routes live emergencies to people.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Golden set pass rate
- Missed safety events in sampled summaries (target zero)
- Reading time saved per manager
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Drilling engineers pick reports with known key events. Expected keywords are the depth, NPT cause and any HSE or well control event. See evals/golden.jsonl.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
