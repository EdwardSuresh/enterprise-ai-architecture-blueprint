# Professional Services: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Kit control that helps |
|---|---|---|
| Client confidentiality duties (e.g. ABA Model Rule 1.6, AICPA confidentiality rule) | Professionals must protect client information, including from AI vendors, and use reasonable safeguards. | Restricted class, matter ACLs in kit.retrieval, vendor register |
| Professional competence and supervision rules (e.g. ABA Model Rules 1.1, 5.1, 5.3; ABA Formal Opinion 512) | Professionals must understand AI tools they use, supervise them and verify outputs. Some bars require client consent for certain AI uses. | require_human, golden evals, training records in 01-governance |
| Conflicts of interest and ethical walls (e.g. ABA Model Rules 1.7, 1.10) | Screened matters must stay screened. AI search across all firm documents can breach a wall. | kit.retrieval ACL filtering by matter and wall |
| Auditor independence and audit standards (e.g. PCAOB, AICPA) | Audit evidence and documentation standards apply to AI-assisted procedures. | kit.tracing, evidence retention |
| Court rules and standing orders on AI-generated filings | Some courts require disclosure or certification that AI-assisted filings were checked. | PS-G03, citation verification step |
| Intellectual property and client ownership of deliverables | Engagement terms often give clients ownership of deliverables. Model inputs and outputs must respect IP rights. | Data contracts, engagement term flags |
| Privacy laws (e.g. GDPR, state privacy laws) | Client data often includes personal data with transfer and purpose limits. | Data classification, region pinning in kit.gateway |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the kit's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
