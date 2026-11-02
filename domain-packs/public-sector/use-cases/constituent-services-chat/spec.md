# Use case spec: Constituent services chat

Pack: `public-sector`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over published agency content with handoff to staff. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

Call centers get many repeat questions on hours, forms and processes. Wait times are long.

## Users

Members of the public; contact center staff for handoffs.

## Pattern

RAG Q&A over published agency content with handoff to staff.

## Data

- Agency website content (public)
- Published forms and notices (public)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- PUB-G01 and PUB-G02 on every turn.
- Clear notice that the user is talking to an AI system, with a path to a person.
- Accessible interface (Section 508 / WCAG).
- Transcripts retained per records schedule.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Call deflection with satisfaction
- Golden set accuracy
- Accessibility test pass rate
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Contact center leads collect top questions. Include multilingual and plain-language variations.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
