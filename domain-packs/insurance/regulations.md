# Insurance: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Blueprint control that helps |
|---|---|---|
| NAIC Model Bulletin on the Use of Artificial Intelligence Systems by Insurers | Adopted by many states. Expects a written AI systems program, governance, risk management, third-party oversight and documentation, scaled to consumer impact. | 01-governance AI program, AI inventory, risk tiering, ARB evidence |
| State unfair trade practices acts | Ban unfair discrimination and misleading statements. AI outputs that mislead or discriminate fall under the same rules as human ones. | INS guardrails, grounding check, fairness tests in kit.evals |
| State unfair claims settlement practices acts | Set standards for prompt, fair claim handling. AI cannot replace the required investigation or reasonable explanation of denials. | require_human for denials, kit.tracing audit trail |
| Colorado SB21-169 and Colorado Division of Insurance regulations | Requires insurers to show that external consumer data and algorithms do not unfairly discriminate, starting with life insurance, with governance and testing. | Tier 3 classification, bias testing evidence, data contracts |
| NYDFS Insurance Circular Letter No. 7 (2024) | Guidance on AI and external consumer data in underwriting and pricing, including fairness testing and governance. | Risk tiering, model documentation, kit.evals fairness checks |
| State rate and form filing laws | Rating factors and rules must match what is filed. An AI that changes how rates are derived may need a filing. | Change control through ARB, AI inventory |
| NAIC Insurance Data Security Model Law and state privacy laws | Information security program and breach notice for nonpublic information. | Data classification, kit.guardrails PII redaction |
| Fair Credit Reporting Act (FCRA) | Applies when consumer reports are used in underwriting. Adverse action notices are required. | Data contracts, human decision step |
| EU AI Act | AI for risk assessment and pricing in life and health insurance of natural persons is listed as high-risk. | Tier 3, control-maps, conformity evidence |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the blueprint's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
