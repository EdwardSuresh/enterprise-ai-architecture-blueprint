# Professional Services Domain Pack

Sector overlay for professional services. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Law firms, accounting and audit firms, consulting firms, engineering and architecture firms. Owners: managing partners, risk and general counsel, knowledge management, IT, EA. |
| **What** | A sector overlay for knowledge search, proposal drafting, document review and engagement operations. |
| **When** | Before client data enters any AI system, and when engagement letters or client terms change. |
| **Where** | On top of platform/core and 01-governance, with ethical walls enforced in retrieval. |
| **Why** | Client confidentiality, professional conduct rules and ownership of work product set firm limits. Wrong outputs can become professional liability. |
| **How** | Enforce matter-level access control in kit.retrieval, check client terms before use, load guardrails.yaml, and keep a qualified professional responsible for every deliverable. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to blueprint controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/knowledge-precedent-search/spec.md](use-cases/knowledge-precedent-search/spec.md) | Starter spec: Firm knowledge and precedent search |
| [use-cases/proposal-drafting/spec.md](use-cases/proposal-drafting/spec.md) | Starter spec: Proposal and RFP response drafting |
| [use-cases/document-review-first-pass/spec.md](use-cases/document-review-first-pass/spec.md) | Starter spec: Document review first pass |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Firm knowledge and precedent search | RAG Q&A | Tier 2 | L0 | Professional verifies sources before use |
| Proposal and RFP response drafting | RAG drafting | Tier 1 | L1 | Engagement lead approves |
| Document review first pass (contracts, discovery) | Classification + extraction | Tier 3 | L1 | Qualified reviewer decides |
| Timesheet narrative cleanup | Drafting | Tier 1 | L1 | Timekeeper approves |
| Engagement acceptance and conflict check support | Search + summarization | Tier 3 | L0 | Risk / conflicts team decides |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the blueprint's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Client confidential data and work product | restricted | Matter-level access; client terms may forbid AI use |
| Privileged communications | restricted | Attorney-client privilege; disclosure can waive it |
| Engagement letters and fee data | confidential | Commercially sensitive |
| Firm methodologies, templates and precedents | internal | Firm IP; remove client identifiers |
| Published thought leadership | public | Approved versions only |

Classes are the blueprint's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Use one client's confidential information for another client, or cross an ethical wall.
- Send client data to an AI service that the engagement terms or client instructions do not allow.
- Present unverified citations, case law or figures as fact in a deliverable.
- Sign, file or deliver advice or an opinion without a qualified professional's review.
- Give legal, tax or audit conclusions directly to a client without professional sign-off.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
