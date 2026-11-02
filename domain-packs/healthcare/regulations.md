# Healthcare: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Blueprint control that helps |
|---|---|---|
| HIPAA Privacy, Security and Breach Notification Rules | PHI in prompts, outputs, logs and indexes is covered. AI vendors that handle PHI are business associates and need a BAA. | Data classification, kit.guardrails PII/PHI redaction, kit.tracing log controls, vendor register |
| 42 CFR Part 2 | Extra protection for substance use disorder treatment records. | Separate ACL tags in kit.retrieval, data contracts |
| FDA guidance on AI-enabled device software functions and clinical decision support | Software that diagnoses or drives treatment may be a medical device. Non-device CDS must let clinicians review the basis for recommendations. | Tier 3, intended-use statement in AI inventory, ARB review |
| ONC HTI-1 Final Rule (decision support interventions transparency) | Certified health IT must give users source attributes for predictive decision support, such as intended use and known limits. | Model cards in 01-governance, citations in outputs |
| ACA Section 1557 nondiscrimination rule | Covered entities must make reasonable efforts to identify and reduce discrimination risk from patient care decision support tools. | Fairness testing in kit.evals, Tier 3 controls |
| CMS rules on coverage decisions in Medicare Advantage | Coverage decisions must be based on the individual patient's circumstances, not an algorithm alone. | require_human for denials, HC-G04 |
| State AI and health privacy laws | Some states require disclosure when AI is used in patient communications or limit AI in utilization review. | AI disclosure text, control-maps |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the blueprint's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
