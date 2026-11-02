# Use case spec: Firm knowledge and precedent search

Pack: `professional-services`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG Q&A over sanitized precedents and firm methods, with matter-level ACL filtering. |
| Risk tier | Tier 2 |
| Autonomy | L0 |

## Business problem

Professionals redo work because they cannot find the firm's past precedents and methods.

## Users

Lawyers, consultants, accountants, knowledge managers.

## Pattern

RAG Q&A over sanitized precedents and firm methods, with matter-level ACL filtering.

## Data

- Precedent library (internal)
- Matter documents (restricted, own matters only)

## Risk tier and autonomy

- Tier 2, autonomy L0. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- ACL and ethical wall filtering before ranking (kit.retrieval).
- PS-G01 and PS-G03 active.
- Every answer links to source documents.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Search success rate
- Hours saved per matter
- Wall breaches (target zero)
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Knowledge managers write questions with known precedent answers. Include tests where a screened document must not appear.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
