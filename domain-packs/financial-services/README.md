# Financial Services Domain Pack

Sector overlay for financial services. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Banks, credit unions, broker-dealers, asset managers, payments firms. Owners: business line leaders, model risk management, compliance, information security, EA. |
| **What** | A sector overlay with starter use cases, regulation mapping, data classification, guardrails and golden evals for banking and capital markets. |
| **When** | When a financial services team proposes its first AI use case, and at every model risk validation or annual review. |
| **Where** | Applied on top of the blueprint's core platform (platform/core) and governance (01-governance). Lives in this folder. |
| **Why** | Credit, trading, AML and customer communications are heavily regulated. Models that touch them need model risk controls, fair lending checks and records. |
| **How** | Copy this pack, confirm the regulation list with Legal and Compliance, load guardrails.yaml into kit.guardrails, and run evals/golden.jsonl through kit.evals before go-live. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to blueprint controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/policy-qa/spec.md](use-cases/policy-qa/spec.md) | Starter spec: Employee policy and procedure Q&A |
| [use-cases/complaint-triage/spec.md](use-cases/complaint-triage/spec.md) | Starter spec: Customer complaint triage and summary |
| [use-cases/credit-memo-drafting/spec.md](use-cases/credit-memo-drafting/spec.md) | Starter spec: Commercial credit memo first draft |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Employee policy and procedure Q&A | RAG Q&A | Tier 1 | L0 | Content owners review a monthly sample of answers |
| Customer complaint triage and summary | Classification + summarization | Tier 2 | L1 | Complaint analyst confirms category, priority and routing |
| Commercial credit memo first draft | RAG drafting | Tier 3 | L1 | Credit officer edits and signs; model risk validates before use |
| Marketing and client communication pre-review | Classification + drafting | Tier 2 | L1 | Registered principal approves every piece |
| Suspicious activity alert narrative draft | Summarization | Tier 3 | L1 | BSA/AML investigator decides and files |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the blueprint's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Customer identity and contact data (NPI) | restricted | GLBA nonpublic personal information |
| Account balances and transactions | restricted | Never sent to a model without masking and an approved purpose |
| Credit files and financial statements | restricted | Used only in Tier 3 credit workflows |
| Complaint records | confidential | May contain PII; redact before prompting |
| Internal policies and procedures | internal | Good first RAG source |
| Published product disclosures and rate sheets | public | Use the current approved version only |

Classes are the blueprint's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Make or send a final credit, pricing or account decision without a qualified human.
- Give personalized investment, tax or legal advice to a customer.
- Use protected characteristics, or close proxies for them, in credit or pricing logic.
- Tell anyone that a suspicious activity report was or may be filed (tipping off).
- Move money, change limits, or open or close accounts on its own.
- Expose one customer's information to another customer or to unauthorized staff.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
