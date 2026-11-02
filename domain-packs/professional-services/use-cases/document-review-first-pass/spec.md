# Use case spec: Document review first pass

Pack: `professional-services`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Classification and clause extraction with reviewer confirmation and sampling. |
| Risk tier | Tier 3 |
| Autonomy | L1 |

## Business problem

Contract and discovery reviews involve large volumes. First-pass review is slow and costly.

## Users

Associates, reviewers, engagement managers.

## Pattern

Classification and clause extraction with reviewer confirmation and sampling.

## Data

- Matter documents (restricted)
- Review protocol (internal)

## Risk tier and autonomy

- Tier 3, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Reviewer confirms every privilege and responsiveness call.
- Client consent where engagement terms require it.
- Statistical sampling of AI-coded documents.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Recall and precision against reviewer coding
- Review hours per thousand documents
- Privilege errors (target zero)
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Senior reviewers code a seed set. Expected keywords are clause names and key terms found in the documents.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
