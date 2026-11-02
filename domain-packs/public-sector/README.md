# Public Sector Domain Pack

Sector overlay for public sector. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Federal, state and local agencies, and public universities in their administrative role. Owners: agency CIO, chief AI officer, privacy officer, records officer, EA. |
| **What** | A sector overlay for constituent services, caseworker support, records and internal operations use cases. |
| **When** | Before any AI use that affects the public's rights or access to services, and at each annual AI use case inventory update. |
| **Where** | On top of platform/core and 01-governance, in authorized cloud environments (for example FedRAMP for US federal). |
| **Why** | Government AI affects rights, benefits and safety. Rules require inventories, impact assessments, accessibility and records retention. |
| **How** | Classify each use case for rights and safety impact, apply minimum practices, load guardrails.yaml, and keep AI outputs as records where required. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to kit controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/constituent-services-chat/spec.md](use-cases/constituent-services-chat/spec.md) | Starter spec: Constituent services chat |
| [use-cases/caseworker-case-summary/spec.md](use-cases/caseworker-case-summary/spec.md) | Starter spec: Caseworker case summary |
| [use-cases/records-request-triage/spec.md](use-cases/records-request-triage/spec.md) | Starter spec: Public records request triage |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Constituent services chat (hours, forms, eligibility info) | RAG Q&A | Tier 2 | L1 | Handoff to staff for case-specific questions |
| Caseworker case summary | Summarization | Tier 3 | L1 | Caseworker makes every eligibility decision |
| Public records request triage | Classification + search | Tier 2 | L1 | Records officer decides on release and redaction |
| Internal policy and procurement Q&A | RAG Q&A | Tier 1 | L0 | Policy owners review samples |
| Meeting minutes draft | Summarization | Tier 1 | L1 | Clerk approves before publication |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the kit's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Case files with PII (benefits, licensing, tax) | restricted | Privacy Act or state equivalents; federal tax data has extra rules |
| Criminal justice information | restricted | CJIS Security Policy applies |
| Internal memos and drafts | confidential | May be exempt from disclosure; still records |
| Agency policies and procedures | internal | Often public on request |
| Published forms, notices and web content | public | Must meet accessibility standards |

Classes are the kit's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Make or communicate an eligibility, benefit, enforcement or licensing decision without a human official.
- Give legal advice to members of the public.
- Delete, alter or fail to retain records created by AI-assisted work.
- Use AI for surveillance or profiling of protected activity such as speech or assembly.
- Deploy a rights- or safety-impacting use without the required impact assessment and notice.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
