# Use case spec: Customer complaint triage and summary

Pack: `financial-services`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Classification and summarization with a human confirming each result. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

Complaints arrive by email, chat and phone notes. Manual triage is slow and categories are inconsistent, which weakens regulatory reporting.

## Users

Complaint analysts, customer experience managers, compliance reviewers.

## Pattern

Classification and summarization with a human confirming each result.

## Data

- CRM and complaint records (confidential)
- Complaint category taxonomy (internal)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Redact PII before the model call (kit.guardrails).
- FS-G02 and FS-G04 route disputes and fraud to a person.
- Model never closes or responds to a complaint on its own.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Category agreement with analysts
- Triage time per complaint
- Missed regulatory-reportable complaints (target zero)
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Use past complaints with the final analyst category as the label. Over-sample rare categories such as fair lending and elder abuse.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
