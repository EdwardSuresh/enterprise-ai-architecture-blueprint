# Insurance Domain Pack

Sector overlay for insurance. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Property and casualty, life, and health insurers, brokers and third-party administrators. Owners: underwriting, claims, actuarial, compliance, EA. |
| **What** | A sector overlay for underwriting, claims and policy servicing use cases, mapped to insurance AI rules. |
| **When** | Before any AI touches underwriting, rating, claims or fraud decisions, and at each annual AI program review. |
| **Where** | On top of platform/core and 01-governance. Pair it with the insurer's written AI program. |
| **Why** | Regulators expect insurers to govern AI systems, test for unfair discrimination and keep humans accountable for adverse consumer outcomes. |
| **How** | Confirm the state list with Legal, map rules to control-maps, load guardrails.yaml, and run golden evals built from real underwriting and claims questions. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to blueprint controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/underwriting-manual-qa/spec.md](use-cases/underwriting-manual-qa/spec.md) | Starter spec: Underwriting manual Q&A |
| [use-cases/fnol-intake-summary/spec.md](use-cases/fnol-intake-summary/spec.md) | Starter spec: First notice of loss intake summary |
| [use-cases/claim-letter-drafting/spec.md](use-cases/claim-letter-drafting/spec.md) | Starter spec: Claim correspondence drafting |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Underwriting manual Q&A | RAG Q&A | Tier 2 | L0 | Underwriter applies the answer; manual owner reviews samples |
| First notice of loss (FNOL) intake summary | Extraction + summarization | Tier 2 | L1 | Claims handler confirms facts and coverage |
| Claim correspondence drafting | RAG drafting | Tier 2 | L1 | Adjuster approves every letter before it is sent |
| Rating factor analysis support | Analytics assistant | Tier 3 | L0 | Actuary owns the rating plan and filing |
| Fraud referral explanation | Summarization | Tier 3 | L1 | Special investigations unit (SIU) decides on referral |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the blueprint's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Policyholder PII and policy records | restricted | Includes driver, property and payment data |
| Claims files, photos and medical records | restricted | Health data may fall under HIPAA or state law |
| External consumer data and scores | confidential | Subject to unfair discrimination testing |
| Underwriting manuals and guidelines | internal | Versioned; filed rules may be public in some states |
| Filed rates, rules and forms | public | Use only the filed and approved version |

Classes are the blueprint's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Deny, rescind or cancel coverage, or decide a claim, without a licensed human.
- Use race, religion, national origin or other protected classes, or proxies, in rating or underwriting.
- Tell a customer a claim will be paid or a loss is covered before a coverage decision.
- Use external consumer data that has not passed unfair discrimination testing.
- Discourage a claimant from filing a claim or from seeking legal advice.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
