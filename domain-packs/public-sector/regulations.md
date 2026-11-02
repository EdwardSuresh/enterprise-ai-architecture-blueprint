# Public Sector: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Kit control that helps |
|---|---|---|
| US OMB memoranda on federal agency use and acquisition of AI (e.g. M-25-21, M-25-22) | Require AI governance, use case inventories, and minimum risk practices for high-impact AI, plus acquisition rules. Check for the current memoranda. | AI inventory, risk tiering (high-impact = Tier 3), ARB evidence |
| Section 508 of the Rehabilitation Act | Federal electronic content and services, including chat interfaces, must be accessible. | Accessibility testing in CI, UX checklist |
| Federal Records Act and state public records laws | Prompts, outputs and transcripts may be records. They must be kept per records schedules and may be released on request. | kit.tracing retention, records schedule mapping |
| Privacy Act of 1974 and E-Government Act (privacy impact assessments) | Limits on systems of records about individuals and PIAs for new IT that handles PII. | Data contracts, PIA link in AI inventory |
| FedRAMP / GovRAMP (formerly StateRAMP) | Cloud services used by agencies need the right authorization level. | Approved provider list in kit.gateway config |
| CJIS Security Policy | Controls for criminal justice information, including access, encryption and personnel screening. | Restricted class, separate environment, kit.retrieval ACLs |
| IRS Publication 1075 | Safeguards for federal tax information shared with agencies. | Restricted class, no-AI flag by default, data contracts |
| NIST AI Risk Management Framework | Voluntary framework widely referenced by agencies for AI risk management. | control-maps, 01-governance risk process |
| State AI laws and executive orders | Many states require inventories, impact assessments or disclosure for government AI. | control-maps, AI inventory fields |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the kit's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
