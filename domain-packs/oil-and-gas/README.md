# Oil and Gas Domain Pack

Sector overlay for oil and gas. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Upstream operators, drilling contractors, midstream pipeline operators, refiners. Owners: operations, HSE, engineering, OT security, EA. |
| **What** | A sector overlay for drilling, production, pipeline and HSE use cases, with strict separation from control systems. |
| **When** | When AI reads operational reports or sensor data, and before any proposal to link AI to OT networks. |
| **Where** | On top of platform/core and 01-governance. AI runs in the IT zone; OT data comes through approved one-way paths. |
| **Why** | Errors can harm people, assets and the environment. Safety regulations and OT security rules set firm limits on what AI may touch. |
| **How** | Start with read-only report summaries and HSE document Q&A. Keep AI advisory (L0-L1). Load guardrails.yaml and test with golden evals from engineers. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to kit controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/daily-drilling-report-summary/spec.md](use-cases/daily-drilling-report-summary/spec.md) | Starter spec: Daily drilling report summary |
| [use-cases/hse-procedure-qa/spec.md](use-cases/hse-procedure-qa/spec.md) | Starter spec: HSE procedure and permit Q&A |
| [use-cases/work-order-triage/spec.md](use-cases/work-order-triage/spec.md) | Starter spec: Maintenance work order triage |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Daily drilling report summary | Summarization | Tier 2 | L1 | Drilling superintendent reviews before distribution |
| HSE procedure and permit Q&A | RAG Q&A | Tier 2 | L0 | HSE advisor owns procedures and reviews samples |
| Maintenance work order triage | Classification | Tier 2 | L1 | Maintenance planner confirms priority |
| Pipeline integrity report review support | RAG + extraction | Tier 3 | L0 | Integrity engineer decides on repairs |
| Incident and near-miss report analysis | Summarization + classification | Tier 2 | L1 | HSE team confirms root cause categories |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the kit's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Real-time SCADA and control system data | restricted | Read via approved historian copies only; never write back |
| Daily drilling and production reports | confidential | Well and reservoir data is commercially sensitive |
| Seismic and reservoir models | restricted | High commercial value; tight need-to-know |
| HSE procedures, permits and JSAs | internal | Good first RAG source |
| Incident reports | confidential | May include personal and injury data |
| Regulatory filings already published | public | Use the filed version |

Classes are the kit's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Send commands, setpoints or writes to any control system, safety instrumented system or SCADA.
- Approve a permit to work, bypass a safety system, or override a stop-work decision.
- Decide that a leak, release or incident is or is not reportable to a regulator.
- Give well control or emergency response instructions in place of the approved procedure.
- Downplay or omit safety-critical facts from a summary.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
