# Manufacturing Domain Pack

Sector overlay for manufacturing. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Discrete and process manufacturers, contract manufacturers, industrial equipment makers. Owners: plant operations, quality, engineering, EHS, OT security, EA. |
| **What** | A sector overlay for quality, maintenance, engineering knowledge and plant operations support use cases. |
| **When** | When AI reads quality, production or engineering data, and before any link to plant control systems. |
| **Where** | On top of platform/core and 01-governance. AI services sit in the enterprise zone with controlled conduits to OT data. |
| **Why** | Product safety, quality records and export-controlled designs carry legal exposure. Plant control systems must stay protected. |
| **How** | Start with read-only knowledge and summary use cases, keep AI advisory, load guardrails.yaml, and test with golden evals from engineers and quality staff. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to kit controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/ncr-summary-routing/spec.md](use-cases/ncr-summary-routing/spec.md) | Starter spec: Nonconformance report summary and routing |
| [use-cases/sop-operator-qa/spec.md](use-cases/sop-operator-qa/spec.md) | Starter spec: Standard work and SOP Q&A |
| [use-cases/maintenance-troubleshooting/spec.md](use-cases/maintenance-troubleshooting/spec.md) | Starter spec: Maintenance troubleshooting assistant |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Nonconformance report (NCR) summary and routing | Summarization + classification | Tier 2 | L1 | Quality engineer decides disposition |
| Standard work and SOP Q&A for operators | RAG Q&A | Tier 2 | L0 | Area supervisor owns the SOP |
| Maintenance troubleshooting assistant | RAG Q&A | Tier 2 | L0 | Maintenance technician follows lockout/tagout |
| Supplier quality issue draft (SCAR) | Drafting | Tier 2 | L1 | Supplier quality engineer approves |
| Engineering change impact search | RAG + search | Tier 2 | L0 | Engineering owns the change decision |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the kit's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Design files and technical data packages | restricted | May be export controlled (EAR/ITAR) |
| Quality records (NCRs, CAPAs, inspection results) | confidential | ISO 9001 controlled records |
| PLC, SCADA and MES operational data | restricted | Read via replicas only; never write back |
| SOPs, work instructions and maintenance manuals | internal | Controlled documents; use current revision |
| Published product manuals and safety data sheets | public | Use the current released version |

Classes are the kit's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Send commands or setpoints to PLCs, robots, MES or any machine control system.
- Release product, disposition a nonconformance or sign a certificate of conformance.
- Tell a worker to skip lockout/tagout, guarding or other safety steps.
- Share export-controlled design data with an unauthorized person, model or region.
- Decide that a product defect is not a safety issue or not reportable.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
