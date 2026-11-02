# Use case spec: Proposal and RFP response drafting

Pack: `professional-services`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG drafting from approved boilerplate, credentials and past winning proposals. |
| Risk tier | Tier 1 |
| Autonomy | L1 |

## Business problem

Proposal teams rebuild similar responses for each RFP, under tight deadlines.

## Users

Business development, engagement leads.

## Pattern

RAG drafting from approved boilerplate, credentials and past winning proposals.

## Data

- Proposal library (internal)
- Credentials database (internal)

## Risk tier and autonomy

- Tier 1, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Only approved credentials and client references with consent.
- No other client confidential details.
- Engagement lead approves the final response.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Time to first draft
- Edits per section
- Win rate (tracked, not attributed only to AI)
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Business development leads pick past questions and the approved answers.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
