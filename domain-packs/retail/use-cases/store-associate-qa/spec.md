# Use case spec: Store associate policy Q&A

Pack: `retail`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over store operations policies on a handheld device. |
| Risk tier | Tier 1 |
| Autonomy | L0 |

## Business problem

Associates ask managers or search binders for policy answers during customer conversations.

## Users

Store associates, store managers.

## Pattern

RAG Q&A over store operations policies on a handheld device.

## Data

- Store operations manual (internal)
- Published customer policies (public)

## Risk tier and autonomy

- Tier 1, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Answer only from the current manual.
- Refer HR and safety issues to the manager.
- No customer personal data in prompts.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Golden set accuracy
- Manager escalations
- Associate usage
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Store managers collect common associate questions. Include region-specific rules.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
