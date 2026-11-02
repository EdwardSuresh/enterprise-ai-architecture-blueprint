# Use case spec: Patient message reply draft

Pack: `healthcare`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG drafting grounded in chart context and approved patient education. |
| Risk tier | Tier 3 |
| Autonomy | L1 |

## Business problem

Patient portal message volume has grown. Care teams struggle to reply quickly and consistently.

## Users

Nurses, physicians, medical assistants.

## Pattern

RAG drafting grounded in chart context and approved patient education.

## Data

- Portal messages (restricted)
- Patient education library (public)

## Risk tier and autonomy

- Tier 3, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- HC-G01 to HC-G03 on every message.
- Clinician approves every reply.
- Disclose AI-assisted drafting where required by state law or policy.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Reply time
- Draft acceptance rate
- Safety events linked to messages (target zero)
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Nursing leaders select real de-identified messages. Include emergency phrasing and medication requests.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
