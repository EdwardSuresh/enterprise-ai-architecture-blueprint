# Healthcare Domain Pack

Sector overlay for healthcare. Use it with the core kit. It does not replace your own legal, compliance or risk review.

| 5W1H | Answer |
|---|---|
| **Who** | Hospitals, health systems, clinics, health plans, health IT vendors. Owners: CMIO, CNIO, compliance, privacy, clinical informatics, EA. |
| **What** | A sector overlay for clinical documentation, patient communication, revenue cycle and operations use cases. |
| **When** | Before AI touches protected health information or clinical workflows, and at every clinical governance review. |
| **Where** | On top of platform/core and 01-governance, with a business associate agreement for every AI provider that handles PHI. |
| **Why** | Clinical errors can harm patients. PHI is tightly regulated. Some AI software can be a regulated medical device. |
| **How** | Start with administrative and documentation support. Keep clinicians in the loop. Confirm BAAs, load guardrails.yaml, and run golden evals built with clinicians. |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators that shape AI use in this sector, mapped to kit controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Starter golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Main data sources, owners, classification and ACL source |
| [use-cases/clinical-documentation-draft/spec.md](use-cases/clinical-documentation-draft/spec.md) | Starter spec: Clinical documentation draft |
| [use-cases/patient-message-reply/spec.md](use-cases/patient-message-reply/spec.md) | Starter spec: Patient message reply draft |
| [use-cases/staff-policy-qa/spec.md](use-cases/staff-policy-qa/spec.md) | Starter spec: Staff policy and procedure Q&A |

## Starter use cases

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| Clinical documentation draft (visit note) | Summarization | Tier 3 | L1 | Clinician reviews, edits and signs every note |
| Patient message reply draft | RAG drafting | Tier 3 | L1 | Clinician or nurse approves before sending |
| Prior authorization packet preparation | Extraction + drafting | Tier 2 | L1 | Revenue cycle staff submit |
| Staff policy and procedure Q&A | RAG Q&A | Tier 1 | L0 | Policy owners review samples |
| Coding suggestion support | Classification | Tier 2 | L1 | Certified coder decides final codes |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review. Tier 3 = high risk, Tier 1 = low risk. Final tier comes from the kit's risk tiering in [01-governance](../../01-governance/)._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| Protected health information (PHI) in the EHR | restricted | HIPAA; minimum necessary; BAA required |
| Substance use disorder records (42 CFR Part 2) | restricted | Extra consent and redisclosure limits |
| Claims and billing data | confidential | Contains PHI and payer contract terms |
| Clinical guidelines and order sets | internal | Versioned; owned by clinical committees |
| Patient education materials | public | Approved versions only |

Classes are the kit's four: public, internal, confidential, restricted.

## What AI must never do in this sector

- Diagnose, prescribe or change a treatment plan without a licensed clinician.
- Send a message to a patient that a clinician has not approved.
- Send PHI to any model or service without a BAA and an approved purpose.
- Tell a patient that symptoms are not serious, or delay emergency care.
- Deny or delay care or coverage based only on a model output.

## How to adopt this pack

1. Confirm the use case list with the business owner. Keep regulated decisions at Tier 3.
2. Review [regulations.md](regulations.md) with Legal and Compliance. Add local rules.
3. Check the data classes against your data catalog.
4. Tune [guardrails.yaml](guardrails.yaml) and test it with `kit.guardrails`.
5. Replace the starter golden set with 100-300 real examples per use case from front-line experts.
6. Send each use case through governance intake and publish the approved list.

Organization names, policies and numbers in this pack are fictitious. Illustrative example only.
