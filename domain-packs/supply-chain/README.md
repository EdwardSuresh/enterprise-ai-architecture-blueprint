# Supply Chain Domain Pack

Sector overlay for supply chain. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Procurement, logistics, planning and trade compliance teams in any industry. Owners: CPO, supply chain VP, trade compliance, EA. |
| **What** | A sector overlay for purchase order, supplier, logistics and trade compliance use cases. |
| **When** | When AI starts to read or act on ERP, supplier or shipment data. |
| **Where** | On top of platform/core and 01-governance; tool agents use kit.tools against ERP and logistics systems. |
| **Why** | Supply chain AI often takes actions (changes POs, contacts suppliers). Export controls, sanctions and contract terms add legal exposure. |
| **How** | Start with read-only use cases, put every write tool behind the approval queue, load guardrails.yaml, and test with golden evals built from real exceptions. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to kit controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/po-exception-resolution/spec.md](use-cases/po-exception-resolution/spec.md) | Starter spec: Purchase order exception resolution |
| [use-cases/supplier-contract-qa/spec.md](use-cases/supplier-contract-qa/spec.md) | Starter spec: Supplier contract Q&A |
| [use-cases/shipment-delay-briefing/spec.md](use-cases/shipment-delay-briefing/spec.md) | Starter spec: Shipment delay briefing |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Purchase order exception resolution | Tool agent | Tier 2 | L2 | Buyer approves every PO change or supplier message |
| Supplier contract Q&A | RAG Q&A | Tier 1 | L0 | Category manager reviews a sample |
| Shipment delay briefing | Summarization | Tier 1 | L1 | Logistics planner approves before sending to customers |
| Export classification support | RAG + classification | Tier 3 | L0 | Trade compliance decides the classification |
| Demand forecast narrative | Summarization | Tier 1 | L0 | Planner owns the forecast |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the kit's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Purchase orders, receipts and invoices | confidential | ERP data; supplier pricing is sensitive |
| Supplier contracts and pricing | confidential | May include confidentiality clauses that limit AI use |
| Export-controlled technical data | restricted | ITAR or EAR controlled; region and access limits apply |
| Shipment tracking and carrier data | internal | Shared with customers only in approved form |
| Public tariff schedules and denied party lists | public | Use the current official version |

Classes are the kit's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Change, cancel or release a PO, or approve a payment, without buyer approval.
- Classify an item for export or decide a license is not needed on its own.
- Send export-controlled technical data to a model, region or person not cleared for it.
- Share one supplier's pricing with another supplier or a competitor.
- Suggest ways to avoid customs duties, sanctions or export controls.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
