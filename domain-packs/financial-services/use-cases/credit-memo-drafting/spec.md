# Use case spec: Commercial credit memo first draft

Pack: `financial-services`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG drafting over the borrower file, producing a structured draft with citations to source documents. |
| Risk tier | Tier 3 |
| Autonomy | L1 |

## Business problem

Relationship managers spend many hours assembling credit memos from financial statements, covenants and prior reviews.

## Users

Relationship managers, credit analysts, credit officers.

## Pattern

RAG drafting over the borrower file, producing a structured draft with citations to source documents.

## Data

- Loan origination and credit files (restricted)
- Credit policy (internal)

## Risk tier and autonomy

- Tier 3, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Draft only; the credit decision stays with the credit officer.
- Every figure must cite a source page; ungrounded numbers are flagged.
- No protected characteristics in prompts or outputs.
- Model risk validation before production use.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Analyst hours per memo
- Number of factual corrections per draft
- Validation findings closed before launch
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Credit officers pick past approved memos and the source files. Expected keywords are key ratios, covenants and risk ratings found in the sources.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
