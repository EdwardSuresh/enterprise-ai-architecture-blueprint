# Retail Domain Pack

Sector overlay for retail. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Store and e-commerce retailers, marketplaces, consumer brands. Owners: digital, customer service, merchandising, privacy, EA. |
| **What** | A sector overlay for customer chat, product content, merchandising and store operations use cases. |
| **When** | Before a customer-facing assistant launches, and when AI starts to touch pricing, promotions or customer data. |
| **Where** | On top of platform/core and 01-governance. Customer chat runs through kit.guardrails on every turn. |
| **Why** | Customer-facing AI can make false claims, leak personal or payment data, or make promises the business must honor. |
| **How** | Load guardrails.yaml into kit.guardrails, keep payment data out of prompts, ground answers in current policy, and test with golden evals before launch. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to kit controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/customer-service-chat/spec.md](use-cases/customer-service-chat/spec.md) | Starter spec: Customer service chat |
| [use-cases/product-description-drafting/spec.md](use-cases/product-description-drafting/spec.md) | Starter spec: Product description generation |
| [use-cases/store-associate-qa/spec.md](use-cases/store-associate-qa/spec.md) | Starter spec: Store associate policy Q&A |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Customer service chat (orders, returns, policies) | RAG Q&A + tools | Tier 2 | L1 | Agent handoff for refunds above limits, complaints and disputes |
| Product description generation | Drafting | Tier 1 | L1 | Merchandiser approves before publishing |
| Store associate policy Q&A | RAG Q&A | Tier 1 | L0 | Store operations reviews samples |
| Review and feedback theme analysis | Classification + summarization | Tier 1 | L0 | Insights team validates themes |
| Promotion and pricing analysis support | Analytics assistant | Tier 2 | L0 | Pricing manager decides |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the kit's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Payment card data (PAN, CVV) | restricted | Never in prompts, logs or indexes; PCI scope |
| Customer profile, order and loyalty data | confidential | Personal data under state privacy laws |
| Product catalog and attributes | internal | Becomes public once published |
| Return, shipping and warranty policies | public | Use the current published version |
| Supplier cost and margin data | confidential | Never in customer-facing context |

Classes are the kit's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Collect, repeat or store full payment card numbers or security codes in chat.
- Invent prices, discounts, stock levels or delivery dates.
- Make health, safety or environmental claims about products that are not substantiated.
- Issue refunds or credits above the set limit without a human.
- Use customer data for purposes the customer was not told about.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
