# AI Program RACI

R = Responsible (does the work). A = Accountable (one owner, signs off). C = Consulted. I = Informed.

| 5W1H | Answer |
|---|---|
| **Who** | All parties to the AI program |
| **What** | Who does what across the AI life cycle |
| **When** | Agreed at program start; revisited yearly or when the operating model changes |
| **Where** | Referenced from the [charter](charter.md) and ARB packs |
| **Why** | Removes "I thought you were doing that" gaps, especially between delivery, risk and platform |
| **How** | Adjust roles to your organization. Keep exactly one A per row |

## Columns

- **EA**: Enterprise architecture (ARB chair)
- **Platform**: AI platform team (gateway, models, tools, observability)
- **Delivery**: Use-case delivery team
- **Risk/Sec**: Risk, compliance, security and privacy
- **Business**: Use-case sponsor and system owner
- **Legal**: Legal counsel
- **Procurement**: Sourcing and vendor management
- **HR**: Human resources and workforce planning

## RACI table

| Activity | EA | Platform | Delivery | Risk/Sec | Business | Legal | Procurement | HR |
|---|---|---|---|---|---|---|---|---|
| AI strategy and priorities | R | C | I | C | A | C | I | C |
| Use-case intake and scoring | C | I | R | C | A | I | I | I |
| Risk tier assignment | A | I | C | R | C | C | I | I |
| AI impact assessment (Tier 3) | C | I | R | A | R | C | I | C |
| ARB review and decision | A | C | R | C | C | C | I | I |
| Reference architecture and patterns | A | R | C | C | I | I | I | I |
| Approved model list | A | R | I | C | I | C | C | I |
| LLM gateway and guardrails | C | A | I | C | I | I | I | I |
| Data classification and contracts | C | C | R | C | A | C | I | I |
| Threat model and red teaming | C | C | R | A | I | I | I | I |
| Evaluations before release | C | C | R | C | A | I | I | I |
| Human oversight design | C | I | R | C | A | C | I | C |
| Production release approval | C | C | R | C | A | I | I | I |
| AI inventory maintenance | A | R | R | I | C | I | I | I |
| Monitoring, SLOs and on-call | I | A | R | I | I | I | I | I |
| AI incident response | C | R | R | C | A | C | I | I |
| Regulator or customer notification | I | I | C | R | C | A | I | I |
| Third-party AI due diligence | C | C | I | R | C | C | A | I |
| Vendor contract terms for AI | I | I | I | C | C | R | A | I |
| FinOps budgets and chargeback | C | R | C | I | A | I | C | I |
| Workforce impact assessment | I | I | C | C | R | C | I | A |
| AI literacy and learning paths | C | C | C | C | C | I | I | A |
| Model version change | C | R | R | C | A | I | I | I |
| Model or system retirement | C | R | R | I | A | I | C | I |

## Notes

- The **Business** system owner is accountable for each AI system in production. Platform is accountable for the shared platform, not for each use case.
- **Risk/Sec** is shown as one column for brevity. Split it into risk, security and privacy if those are separate functions.
- For bought AI, Procurement is accountable for due diligence completion; Risk/Sec does the assessment.
