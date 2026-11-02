# Financial Services: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Kit control that helps |
|---|---|---|
| SR 11-7 / OCC 2011-12 (model risk management guidance) | US supervisory guidance on model development, validation and governance. AI and LLM systems used for business decisions are usually treated as models and need inventory, validation and monitoring. | AI inventory (01-governance/ai-inventory.yaml), risk tiering, kit.evals evidence |
| ECOA and Regulation B | Prohibits credit discrimination and requires specific adverse action reasons. CFPB guidance says complex algorithms do not excuse vague reasons. | Tier 3 by default, fairness testing in kit.evals, human decision step |
| Fair Credit Reporting Act (FCRA) | Governs use of consumer report data and adverse action notices. Data fed to AI may make it a consumer report use. | Data contracts, purpose limits in kit.retrieval ACLs |
| Gramm-Leach-Bliley Act (GLBA) privacy and safeguards | Protects customer nonpublic personal information. Prompts, logs and vector indexes holding NPI must meet safeguards requirements. | Data classification, kit.guardrails PII redaction, kit.tracing log redaction |
| UDAAP (Dodd-Frank Act, CFPB) | Bans unfair, deceptive or abusive acts. A chatbot that gives wrong fee or rate information can create UDAAP risk. | Grounding check in kit.guardrails, golden evals on fees and disclosures |
| Bank Secrecy Act / AML rules | Require monitoring and reporting of suspicious activity and confidentiality of SARs. | FS guardrails (tipping-off block), human decision for filings |
| FINRA Rule 2210 and SEC Marketing Rule | Rules on fair, balanced communications with the public and principal approval. AI-drafted content is still the firm's communication. | require_human approval step, kit.tracing records |
| SEC Rule 17a-4 and FINRA Rule 4511 (books and records) | Business communications must be retained. AI chat transcripts with clients may be records. | kit.tracing retention, records schedule in 01-governance |
| EU Digital Operational Resilience Act (DORA) | ICT risk management and third-party oversight for EU financial entities, including cloud and AI providers. | kit.gateway fallback, vendor register, exit plan in 01-governance |
| EU AI Act | Creditworthiness scoring of natural persons is listed as high-risk, with obligations on providers and deployers. | Tier 3 classification, control-maps, conformity evidence |
| NYDFS 23 NYCRR Part 500 (cybersecurity) | Cybersecurity program, access control and third-party requirements for New York regulated entities. | Scoped identities in kit.tools, access reviews |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the kit's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
