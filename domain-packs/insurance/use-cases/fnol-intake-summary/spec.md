# Use case spec: First notice of loss intake summary

Pack: `insurance`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Extraction and summarization into a structured FNOL record that a handler confirms. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

FNOL notes, photos and calls are unstructured. Handlers re-key facts and miss details that affect coverage and reserves.

## Users

Claims intake staff, adjusters, claims supervisors.

## Pattern

Extraction and summarization into a structured FNOL record that a handler confirms.

## Data

- Claims notes and attachments (restricted)
- Policy summary (restricted)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Redact PII not needed for the claim.
- No coverage statement in the summary.
- INS-G01 and INS-G04 apply to any customer-facing text.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Field extraction accuracy
- Handler time per FNOL
- Rework rate after first contact
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Use closed claims with the final confirmed loss facts as labels. Cover each major peril and line.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
