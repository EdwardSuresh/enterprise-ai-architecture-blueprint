# Use case spec: Underwriting manual Q&A

Pack: `insurance`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over current underwriting manuals with section citations and effective dates. |
| Risk tier | Tier 2 |
| Autonomy | L0 |

## Business problem

Underwriting guidelines span many manuals and bulletins. Underwriters lose time searching and sometimes apply outdated rules.

## Users

Underwriters, underwriting assistants, agency service staff.

## Pattern

RAG Q&A over current underwriting manuals with section citations and effective dates.

## Data

- Underwriting manuals and bulletins (internal)
- Filed rules (public)

## Risk tier and autonomy

- Tier 2, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Answer only from the current effective version; show the effective date.
- INS-G03 blocks protected class use.
- Refer to a senior underwriter when the manual is silent.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Golden set accuracy
- Referral rate to senior underwriters
- Underwriting audit findings on guideline misuse
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Senior underwriters supply 100-300 real questions per line of business, with the governing section. Include edge cases near eligibility limits.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
