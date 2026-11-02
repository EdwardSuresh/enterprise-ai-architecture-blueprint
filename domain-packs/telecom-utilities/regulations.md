# Telecom and Utilities: Regulations and Frameworks

> Not legal advice; confirm with counsel and current regulator guidance.

This list covers common rules that affect AI in the sector. It is a starting point, not a complete register. Jurisdictions differ. Add local, state and national rules that apply to you.

| Regulation / framework / regulator | What it means for AI | Blueprint control that helps |
|---|---|---|
| FCC CPNI rules (47 U.S.C. 222 and 47 CFR 64.2001 et seq.) | Carriers must protect customer proprietary network information, authenticate customers before disclosure and report breaches. | Restricted class, authentication before tool access in kit.tools, TU-G03 |
| NERC CIP Reliability Standards | Cybersecurity standards for the bulk electric system, including information protection and electronic security perimeters. | Keep AI outside ESPs, restricted class, network patterns in 02-architecture |
| State public utility commission rules | Set customer service rules on billing, disconnection notices, medical certificates and winter moratoriums. | TU-G02 require_human, golden evals on disconnection rules |
| FCC rules on robocalls and TCPA | Consent and identification rules for automated calls and texts, including AI-generated voices. | Consent check before outbound messages |
| TSA and CISA guidance for critical infrastructure | Security directives and guidance for designated operators. | Threat model, access reviews |
| IEC 62443 and NIST Cybersecurity Framework | OT security and general cyber risk frameworks used across utilities and carriers. | control-maps, kit.tools allow-list |
| State privacy laws and utility data access rules | Some states limit sharing of energy usage data without customer consent. | Data contracts, purpose fields in AI inventory |

## How to use this list

1. Legal confirms which items apply and adds missing ones.
2. Map each item to controls in the blueprint's control-maps (see [01-governance](../../01-governance/)).
3. Record the mapping on each use case in the AI inventory.
4. Review the list at least once a year and when a regulator issues new guidance.

_Not legal advice; confirm with counsel and current regulator guidance._
