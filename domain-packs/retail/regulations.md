# Retail: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Blueprint control that helps |
|---|---|---|
| PCI DSS | Payment card data must be protected. Chat, prompts, logs and vector stores must not capture card numbers, or they come into PCI scope. | kit.guardrails PII redaction (card patterns), RET-G01, kit.tracing log redaction |
| FTC Act Section 5 (unfair or deceptive practices) | Claims made by AI on behalf of the retailer must be truthful and substantiated. The FTC has said AI claims and AI-generated content are covered. | Grounding check, RET-G03, golden evals |
| FTC rules on reviews and endorsements | Bans fake or AI-generated reviews presented as real customer reviews. | RET-G04 guardrail, content review |
| CCPA / CPRA and other US state privacy laws | Notice, purpose limits and consumer rights over personal data, plus rules on automated decision-making technology in some states. | Data classification, data contracts, purpose fields in AI inventory |
| ADA and WCAG 2.x (accessibility) | Digital customer experiences, including chat widgets, are expected to be accessible. | Accessibility testing in CI, 02-architecture UX checklist |
| TCPA and CAN-SPAM | Rules on automated calls, texts and marketing email consent. | Consent check before outbound messages, require_human for campaigns |
| Children's Online Privacy Protection Act (COPPA) | Rules on collecting data from children under 13. | Age-gating, block collection of child data |
| EU GDPR and EU AI Act transparency duties | For EU customers: lawful basis for data and telling people when they interact with an AI system. | AI disclosure in UX, control-maps |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the blueprint's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
