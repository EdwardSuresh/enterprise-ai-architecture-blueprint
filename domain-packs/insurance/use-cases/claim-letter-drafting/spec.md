# Use case spec: Claim correspondence drafting

Pack: `insurance`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | RAG drafting from approved templates, policy language and the claim file. |
| Risk tier | Tier 2 |
| Autonomy | L1 |

## Business problem

Adjusters write many similar letters. Quality and required notices vary, which creates complaint and market conduct risk.

## Users

Adjusters, claims supervisors, compliance reviewers.

## Pattern

RAG drafting from approved templates, policy language and the claim file.

## Data

- Letter templates and state notices (internal)
- Policy forms (public)
- Claim file (restricted)

## Risk tier and autonomy

- Tier 2, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Adjuster approves every letter.
- Quote policy language exactly; never paraphrase exclusions.
- Required state notices checked by a rule, not the model.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Letters sent without edits
- Missing-notice defects (target zero)
- Complaint rate on correspondence
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Use approved past letters as references. Expected keywords include provision citations and required notice phrases.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
