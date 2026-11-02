# Use case spec: Shipment delay briefing

Pack: `supply-chain`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Summarization of TMS events and carrier notes into an approved template. |
| Risk tier | Tier 1 |
| Autonomy | L1 |

## Business problem

Planners write delay updates by hand from carrier messages and TMS data. Customers get late or inconsistent updates.

## Users

Logistics planners, customer service.

## Pattern

Summarization of TMS events and carrier notes into an approved template.

## Data

- TMS shipment events (internal)
- Carrier messages (internal)
- Customer order data (confidential)

## Risk tier and autonomy

- Tier 1, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Use only facts from TMS and carrier records.
- Planner approves before any customer message.
- No promised dates unless the carrier confirmed them.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Time from delay event to customer notice
- Edits per briefing
- Customer complaints about delay communications
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Use past delay cases with the final sent message. Expected keywords are shipment IDs, new ETA and cause.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
