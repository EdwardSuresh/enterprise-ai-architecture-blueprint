# Use case spec: Maintenance troubleshooting assistant

Pack: `manufacturing`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over equipment manuals and past CMMS work orders. |
| Risk tier | Tier 2 |
| Autonomy | L0 |

## Business problem

Technicians search manuals and old work orders to diagnose faults. Downtime grows while they look.

## Users

Maintenance technicians, reliability engineers.

## Pattern

RAG Q&A over equipment manuals and past CMMS work orders.

## Data

- Equipment manuals (internal)
- CMMS work order history (internal)

## Risk tier and autonomy

- Tier 2, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Always state lockout/tagout before any hands-on step.
- MFG-G01 blocks control actions.
- Cite manual section or work order number.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Mean time to repair
- Golden set accuracy
- Safety observations
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Reliability engineers build questions from real fault cases with the known fix.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
