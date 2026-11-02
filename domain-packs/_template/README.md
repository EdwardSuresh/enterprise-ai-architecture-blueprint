# <Sector Name> Domain Pack (template)

Copy this folder to `domain-packs/<sector-slug>/`. Replace every `<placeholder>`. Delete guidance lines in italics when done.

| 5W1H | Answer |
|---|---|
| **Who** | <Sector organizations and the roles that own AI here: business owner, risk, compliance, security, EA> |
| **What** | <One sentence: the sector overlay and the kinds of use cases it covers> |
| **When** | <Trigger: e.g. first AI use case in this sector; annual review; new regulator guidance> |
| **Where** | On top of platform/core and 01-governance. <Any hosting or network limits for this sector> |
| **Why** | <The sector risks: regulated decisions, sensitive data, safety, records> |
| **How** | <Steps: confirm regulations, load guardrails.yaml, run golden evals, go through intake> |

## Files

| File | Purpose |
|---|---|
| [regulations.md](regulations.md) | Rules and regulators mapped to blueprint controls |
| [guardrails.yaml](guardrails.yaml) | Sector guardrail rules loaded by `kit.guardrails` |
| [evals/golden.jsonl](evals/golden.jsonl) | Golden examples run by `kit.evals` |
| [data-contracts/README.md](data-contracts/README.md) | Data sources, owners, classification, ACL source |
| [use-cases/example-use-case/spec.md](use-cases/example-use-case/spec.md) | Use case spec template (make three) |

## Starter use cases

_List 3-5. Pick one low-risk internal Q&A use case first. Regulated decisions about people, money, safety or legal rights start at Tier 3._

| Use case | Pattern | Typical risk tier | Autonomy | Human oversight |
|---|---|---|---|---|
| <Internal policy Q&A> | RAG Q&A | Tier 1 | L0 | <Who reviews samples> |
| <Drafting use case> | RAG drafting | Tier 2 | L1 | <Who approves each draft> |
| <Regulated decision support> | <Pattern> | Tier 3 | L1 | <Who decides> |

_L0 = suggest only, L1 = draft for human approval, L2 = act with approval per action, L3 = act within limits with after-the-fact review._

## Key data types and classification

| Data type | Class | Note |
|---|---|---|
| <Personal or regulated data> | restricted | <Law or rule that applies> |
| <Business-sensitive data> | confidential | <Why> |
| <Policies and procedures> | internal | <Good first RAG source> |
| <Published content> | public | <Use current approved version> |

## What AI must never do in this sector

- <Make the regulated decision without a qualified human>
- <Act on physical or financial systems on its own>
- <Expose restricted data to unauthorized people or services>
- <Give professional advice the sector reserves for licensed people>

Organization names, policies and numbers in a pack must be fictitious. Label them "Illustrative example".
