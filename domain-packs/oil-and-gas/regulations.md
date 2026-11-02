# Oil and Gas: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Kit control that helps |
|---|---|---|
| PHMSA pipeline safety regulations (49 CFR Parts 192 and 195) | Set integrity management, control room, operator qualification and reporting rules for gas and hazardous liquid pipelines. AI may support analysis but qualified people make integrity decisions. | Tier 3 for integrity decisions, require_human, kit.tracing evidence |
| OSHA Process Safety Management (29 CFR 1910.119) | Covers process hazard analysis, operating procedures, management of change and incident investigation. An AI tool that changes how procedures are used may need management of change. | ARB review as management of change, OG guardrails |
| BSEE offshore safety rules (e.g. SEMS, 30 CFR Part 250) | Safety and environmental management systems for US offshore operations. | Risk tiering, procedure-grounded RAG |
| EPA reporting (e.g. Greenhouse Gas Reporting Program, release reporting) | Emissions and release data must be accurate and reported on time. AI cannot be the system of record for reportable values. | Grounding check, human sign-off, data contracts |
| API standards and recommended practices (e.g. API RP 1173, API 1160) | Industry standards for pipeline safety management and integrity. Many operators adopt them as company requirements. | Control-maps, golden evals from engineers |
| IEC 62443 (industrial automation and control systems security) | Zones, conduits and security levels for OT. AI services belong outside control zones with controlled conduits. | Network architecture in 02-architecture, kit.tools allow-list (no OT write tools) |
| TSA pipeline security directives | Cybersecurity requirements for designated US pipeline operators, including network segmentation. | OT segmentation, access reviews |
| NIST SP 800-82 (OT security guide) | Guidance for securing industrial control systems. | Architecture patterns, threat model |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the kit's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
