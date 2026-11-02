# Use case spec: Product description generation

Pack: `retail`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Drafting from structured PIM attributes and brand style guide. |
| Risk tier | Tier 1 |
| Autonomy | L1 |

## Business problem

New products need descriptions fast. Copywriters cannot keep up, and supplier text is uneven.

## Users

Merchandisers, copywriters, e-commerce content team.

## Pattern

Drafting from structured PIM attributes and brand style guide.

## Data

- PIM attributes (internal)
- Brand style guide (internal)

## Risk tier and autonomy

- Tier 1, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Use only attributes present in PIM; no invented features.
- RET-G03 blocks health claims.
- Merchandiser approves before publishing.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Time to publish
- Edits per description
- Claims flagged by legal review
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Use approved descriptions with their PIM records. Expected keywords are material, size and care attributes.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
