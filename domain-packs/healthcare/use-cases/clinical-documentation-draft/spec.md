# Use case spec: Clinical documentation draft

Pack: `healthcare`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Summarization of visit transcript and chart context into a draft note for clinician review. |
| Risk tier | Tier 3 |
| Autonomy | L1 |

## Business problem

Clinicians spend hours each day on documentation, which adds to burnout and reduces time with patients.

## Users

Physicians, advanced practice providers, nurses.

## Pattern

Summarization of visit transcript and chart context into a draft note for clinician review.

## Data

- Visit audio/transcript (restricted)
- EHR context (restricted)

## Risk tier and autonomy

- Tier 3, autonomy L1. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Clinician reviews and signs every note; drafts are clearly labeled.
- Patient consent for recording per policy.
- BAA in place with every vendor in the path.
- No new findings that are not in the transcript (grounding check).
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Documentation time per visit
- Clinician edit rate
- Note accuracy audits
- Clinician satisfaction
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Clinical informatics builds de-identified test visits with expected findings. Expected keywords are key findings, medications and plan items.

Each golden line follows the kit schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
