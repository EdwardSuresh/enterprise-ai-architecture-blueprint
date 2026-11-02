# Use case spec: HSE procedure and permit Q&A

Pack: `oil-and-gas`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over current HSE procedures with citations. |
| Risk tier | Tier 2 |
| Autonomy | L0 |

## Business problem

Field crews need fast answers on procedures, permits and PPE. Searching the HSE system on site is slow.

## Users

Field supervisors, crew members, HSE advisors.

## Pattern

RAG Q&A over current HSE procedures with citations.

## Data

- HSE management system documents (internal)

## Risk tier and autonomy

- Tier 2, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Answer only from the current procedure version.
- OG-G04 blocks permit approvals; OG-G02 handles emergencies.
- Always tell the user to follow the site procedure and supervisor.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Golden set accuracy
- HSE advisor review findings
- Usage by site
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

HSE advisors supply real field questions. Include questions about limits (distances, gas levels, durations).

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
