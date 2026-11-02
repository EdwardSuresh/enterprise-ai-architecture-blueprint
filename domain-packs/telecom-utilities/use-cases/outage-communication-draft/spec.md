# Use case spec: Outage communication draft

Pack: `telecom-utilities`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Summarization of outage management system data into approved message templates. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

During outages, communications teams write many updates under time pressure. Messages can be inconsistent or overpromise restoration times.

## Users

Corporate communications, operations duty managers.

## Pattern

Summarization of outage management system data into approved message templates.

## Data

- Outage management system (internal)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Use only restoration times from the OMS.
- Safety messages use fixed approved text.
- Communications lead approves every message.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Time from outage to first update
- Message corrections
- Customer complaints on accuracy
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Use past outages with the final approved messages as references.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
