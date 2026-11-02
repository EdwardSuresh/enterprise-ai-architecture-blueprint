# Manufacturing: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Blueprint control that helps |
|---|---|---|
| Product safety laws (e.g. US Consumer Product Safety Act, EU General Product Safety Regulation) | Manufacturers must report certain defects and hazards. AI cannot decide reportability. | MFG-G03 require_human, kit.tracing evidence |
| ISO 9001 (quality management) and sector standards (e.g. IATF 16949, AS9100, ISO 13485) | Require controlled documents and records. AI outputs that become quality records must be controlled and traceable. | kit.tracing, document revision checks in kit.retrieval |
| Export controls (EAR and ITAR) | Controlled technical data cannot go to unauthorized foreign persons, including through cloud services or support staff. | Restricted class, region pinning in kit.gateway, ACLs |
| IEC 62443 (industrial automation and control systems security) | Zones and conduits for OT. AI belongs outside control zones. | 02-architecture patterns, kit.tools (no OT write tools) |
| OSHA standards (e.g. lockout/tagout 29 CFR 1910.147, machine guarding) | Worker safety rules. AI answers must never contradict them. | MFG-G02 guardrail, procedure-grounded RAG |
| EU Machinery Regulation and EU AI Act | AI used as a safety component in machinery can be high-risk and need conformity assessment. | Tier 3, control-maps |
| Customer contract quality clauses and flow-downs | Customers often require notice of process changes and control of records. | Data contracts, ARB change review |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the blueprint's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
