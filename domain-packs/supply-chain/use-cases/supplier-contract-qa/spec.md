# Use case spec: Supplier contract Q&A

Pack: `supply-chain`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over executed contracts with clause citations. |
| Risk tier | Tier 1 |
| Autonomy | L0 |

## Business problem

Buyers and planners do not know key terms (payment, penalties, termination) in hundreds of supplier contracts.

## Users

Buyers, planners, accounts payable, category managers.

## Pattern

RAG Q&A over executed contracts with clause citations.

## Data

- Contract lifecycle management documents (confidential)

## Risk tier and autonomy

- Tier 1, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- ACL filter by category and business unit.
- SC-G04 blocks cross-supplier pricing.
- Legal interpretation questions route to Legal.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Golden set accuracy
- Contract leakage findings in audits
- Time to answer
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Category managers write questions and point to the clause. Include amended contracts where the amendment overrides the base term.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
