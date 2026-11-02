# Supply Chain: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Kit control that helps |
|---|---|---|
| Export Administration Regulations (EAR, US BIS) | Control dual-use items and technology. Sending controlled technology to a cloud model or foreign-person support team can be an export. | Data classification (restricted), region pinning in kit.gateway, SC guardrails |
| International Traffic in Arms Regulations (ITAR, US DDTC) | Control defense articles and technical data. Hosting, model access and support staff must be cleared for ITAR data. | Separate restricted environment, kit.retrieval ACLs, require_human |
| Sanctions programs (e.g. US OFAC, EU, UK) | Prohibit dealings with listed parties and regions. AI cannot clear a screening hit. | require_human on screening matches, kit.tracing |
| Customs laws (e.g. US CBP reasonable care, EU Union Customs Code) | Importers must use reasonable care in classification and valuation. AI suggestions need broker or compliance review. | Tier 3 for classification, human decision |
| Forced labor import rules (e.g. US UFLPA) | Goods linked to forced labor can be detained. Supplier mapping evidence must be accurate. | Grounding check, cited sources |
| Supplier contract terms (confidentiality, data use, liability) | Contracts may forbid sharing supplier data with third parties, including AI providers. | Data contracts, vendor terms review in 01-governance |
| Competition law (information sharing) | Sharing competitor or supplier pricing can create antitrust risk. | SC-G04 guardrail, ACLs by category |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the kit's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
