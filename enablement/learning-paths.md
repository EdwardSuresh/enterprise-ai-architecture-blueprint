# Learning Paths

| 5W1H | Answer |
|---|---|
| **Who** | All staff; builders (engineers, data scientists, architects); reviewers (people who approve AI outputs or AI systems); leaders |
| **What** | Role-based modules with outcomes and evidence of completion |
| **When** | All-staff literacy before AI tool access; other paths before taking on the role |
| **Where** | Your learning platform; kit labs for builders |
| **Why** | Safe and effective use needs shared basics and role-specific skills |
| **How** | Assign by role in HR or identity data; track completion as governance evidence |

## 1. All-staff AI literacy (about 2 hours)

| Module | Outcome |
|---|---|
| What AI is and is not | Explain in plain words what generative AI and ML do, and where they fail |
| Using approved tools | Know which tools are approved and where to find them |
| Data and AI | Apply data classes; know what never to paste into AI |
| Checking outputs | Verify facts and sources before relying on AI output |
| Responsible use | Know prohibited uses, disclosure rules and how to report issues |

Evidence: completion record, short knowledge check, policy acknowledgement.

## 2. Builders (about 3–5 days, plus labs)

| Module | Outcome | Kit material |
|---|---|---|
| Reference architecture and patterns | Pick and apply the right pattern | `02-architecture/` |
| LLM gateway and aliases | Call models only through the gateway | `labs/01-llm-gateway` |
| Permission-aware RAG | Build retrieval that honours source ACLs | `labs/02-rag` |
| Guardrails | Apply input and output checks | `labs/03-guardrails` |
| Agents and tools | Build tool-using agents with scopes and approvals | `labs/04-tool-agent-mcp` |
| Evaluation | Build golden sets and run eval suites | `labs/05-evals` |
| Governance as code | Inventory entries, system cards, policy gate | `labs/06-governance` |
| Security for LLM apps | Threat-model with STRIDE and OWASP LLM | `security/` |
| Classic ML foundations | Choose and explain classic algorithms | The Architect's ML Playbook |

Evidence: lab completion, a reviewed pull request on a real or practice use case.

## 3. Reviewers (about 1 day)

Two groups: **output reviewers** (the human in the loop) and **system reviewers** (ARB members, risk, audit).

| Module | Outcome |
|---|---|
| Known failure modes | Spot hallucination, bias, outdated sources, injected content |
| Meaningful review | Use evidence on screen; reject or edit with confidence; avoid rubber-stamping |
| Autonomy levels and tiers | Know what the system may and may not do alone |
| Escalation and incidents | Know when and how to stop or escalate |
| ARB review (system reviewers) | Apply the review checklist and read eval reports |
| Control maps (system reviewers) | Use NIST, ISO, EU AI Act and OWASP maps for evidence |

Evidence: completion record; for output reviewers, a supervised review sample.

## 4. Leaders (about half a day)

| Module | Outcome |
|---|---|
| AI strategy and value | Set priorities and judge use cases with the value scorecard |
| Governance and accountability | Understand tiers, ARB decisions and personal accountability as system owner |
| Risk and regulation | Know the main regulatory duties at a high level |
| Workforce and change | Lead role changes with the workforce impact assessment |
| Maturity | Read the maturity model and set targets |

Evidence: completion record; leaders sign the AI strategy or charter.

## Refresh

- All-staff literacy: yearly refresher.
- Builders and reviewers: on major changes to standards or tooling.
- Leaders: yearly.
