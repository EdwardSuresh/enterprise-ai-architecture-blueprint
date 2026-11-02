# Use case spec: Maintenance work order triage

Pack: `oil-and-gas`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Classification of work requests into equipment class, failure mode and suggested priority. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

Work requests arrive with free text and uneven priority. Planners spend time re-reading and re-coding them.

## Users

Maintenance planners, reliability engineers.

## Pattern

Classification of work requests into equipment class, failure mode and suggested priority.

## Data

- CMMS work orders (internal)
- Equipment criticality list (internal)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Planner confirms every priority.
- Safety-critical equipment always flagged for planner review.
- No write to CMMS without approval (kit.tools).
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Priority agreement with planners
- Time to schedule
- Safety-critical misses (target zero)
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Use closed work orders with the planner's final codes. Over-sample safety-critical equipment.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
