# Telecom and Utilities Domain Pack

Sector overlay for telecom and utilities. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Telecom carriers, internet providers, electric, gas and water utilities. Owners: customer operations, network/grid operations, regulatory affairs, security, EA. |
| **What** | A sector overlay for customer care, field service, outage communication and network or grid operations support. |
| **When** | Before AI touches customer account data or operational technology, and at each regulatory compliance review. |
| **Where** | On top of platform/core and 01-governance. AI runs outside critical cyber asset and network control zones. |
| **Why** | Customer proprietary data has special protection. Grid and network systems are critical infrastructure with strict security standards. Service disconnections affect safety. |
| **How** | Start with customer care and field knowledge use cases, keep AI out of control systems, load guardrails.yaml, and test with golden evals from front-line staff. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to kit controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/care-agent-assist/spec.md](use-cases/care-agent-assist/spec.md) | Starter spec: Customer care agent assist |
| [use-cases/outage-communication-draft/spec.md](use-cases/outage-communication-draft/spec.md) | Starter spec: Outage communication draft |
| [use-cases/field-technician-assistant/spec.md](use-cases/field-technician-assistant/spec.md) | Starter spec: Field technician knowledge assistant |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Customer care agent assist (billing, plans, outages) | RAG Q&A | Tier 2 | L1 | Agent decides what to tell the customer |
| Outage communication draft | Summarization + drafting | Tier 2 | L1 | Communications lead approves before publishing |
| Field technician knowledge assistant | RAG Q&A | Tier 2 | L0 | Technician follows approved procedures |
| Network or grid incident ticket summary | Summarization | Tier 2 | L1 | Operations engineer confirms |
| Regulatory filing research support | RAG Q&A | Tier 1 | L0 | Regulatory affairs owns filings |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the kit's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Customer proprietary network information (CPNI) | restricted | Call details, services used; FCC rules apply |
| Grid and network operational data (BES Cyber System information) | restricted | NERC CIP information protection |
| Customer billing and payment history | confidential | Includes payment arrangements and hardship flags |
| Field procedures and equipment manuals | internal | Good first RAG source |
| Published tariffs and rate schedules | public | Use the approved tariff version |

Classes are the kit's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Send commands to network elements, SCADA, energy management or distribution control systems.
- Disconnect service, or tell a customer service will be disconnected, without a human and the required notices.
- Disclose CPNI to anyone before the customer is authenticated as required.
- Give safety instructions for downed lines, gas leaks or hazards in place of emergency procedures.
- Quote rates or fees that are not in the approved tariff.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
