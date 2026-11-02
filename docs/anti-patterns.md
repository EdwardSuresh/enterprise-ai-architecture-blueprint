# Anti-Patterns

Thirteen ways enterprise AI goes wrong, and the blueprint control that prevents each one. The first two come from the author's FS-AI anti-pattern series.

| 5W1H | Answer |
|---|---|
| **Who** | Architects, ARB members, delivery leads, risk |
| **What** | Named failure patterns with what they look like, an illustrative example and the blueprint control |
| **When** | At design reviews, ARB reviews and post-incident reviews |
| **Where** | Any AI system, built or bought |
| **Why** | Naming a problem makes it easier to spot and challenge |
| **How** | Use the list as a review prompt: "Are we doing any of these?" |

All examples are *illustrative examples (composites)*, not client case studies.

## 1. Silent vendor update

*From the FS-AI anti-pattern series.*

- **What it looks like:** A provider or SaaS vendor changes the model behind a product. Outputs shift. Nobody is told; nobody re-tests.
- **Illustrative example:** An insurer's embedded summarization feature began omitting exclusion clauses after a vendor update. Handlers noticed weeks later.
- **Blueprint control:** Model aliases and the [model version change runbook](../ops/runbooks/model-version-change.md); vendor notice clauses in the [third-party AI policy](../01-governance/policies/third-party-ai.md); scheduled evals for vendor-managed models.

## 2. Helpful hallucination

*From the FS-AI anti-pattern series.*

- **What it looks like:** When the system lacks an answer, it produces a plausible one instead of saying "I don't know".
- **Illustrative example:** A bank's internal assistant invented a fee waiver rule that sounded right. Staff applied it to customers.
- **Blueprint control:** Grounding checks and refusal when retrieval finds nothing ([RAG pattern](../02-architecture/patterns/rag-assistant.md)); groundedness SLO; refusal-when-unknown eval cases.

## 3. Pilot purgatory

- **What it looks like:** Many pilots, few in production. Pilots run for months with no decision.
- **Illustrative example:** A retailer ran nine pilots in a year; none had a baseline, so none could prove value.
- **Blueprint control:** [Value scorecard](../00-strategy/value-scorecard.md) with baselines; rule to scale, change or stop after two review cycles; shared platform that makes production the easy path.

## 4. Shadow AI sprawl

- **What it looks like:** Staff and teams use unapproved AI tools and features; nobody knows what data goes where.
- **Illustrative example:** A public agency found staff pasting case notes into a free online tool.
- **Blueprint control:** [Acceptable use policy](../01-governance/policies/acceptable-use.md); approved tools that are actually good; [champions](../enablement/champions-network.md); discovery in the [plug-in rollout](rollout-plugin.md).

## 5. Business logic in prompts

- **What it looks like:** Eligibility rules, limits and pricing logic live in prompt text, where they cannot be tested or audited like code.
- **Illustrative example:** A logistics firm encoded surcharge rules in a prompt. A prompt edit for tone changed a surcharge.
- **Blueprint control:** [Integration standard](../02-architecture/standards/integration-standards.md) 3.5 and 6.3: rules belong in code or tools; prompts in a registry with evals.

## 6. Over-privileged agent

- **What it looks like:** An agent runs with a broad service account that can read and write far more than its task needs.
- **Illustrative example:** A hospital scheduling agent's account could also edit patient demographics.
- **Blueprint control:** One identity per agent with least-privilege scopes ([agent-scopes.yaml](../security/identity/agent-scopes.yaml)); tool allow-lists; approval queue for writes.

## 7. Permission-blind RAG

- **What it looks like:** Documents are indexed with a single service account; every user can retrieve everything.
- **Illustrative example:** A manufacturer's engineering assistant returned board-level acquisition papers to a contractor.
- **Blueprint control:** `acl_source` in every [data contract](../data/contracts/README.md); retrieval must pass user groups; permission tests in evals.

## 8. Eval-free release

- **What it looks like:** Changes to prompts, models or data ship after a few manual tries.
- **Illustrative example:** An energy company changed chunk sizes; answer quality dropped and nobody measured it.
- **Blueprint control:** Golden sets and the evals gate in CI; [ARB checklist](../01-governance/arb/review-checklist.md) item 1.7.

## 9. Single-model lock-in

- **What it looks like:** Code, prompts and tooling are tied to one provider's model; changing costs months.
- **Illustrative example:** A bank could not respond to a price rise because model ids were hard-coded in forty services.
- **Blueprint control:** [ADR-AI-001](../02-architecture/adr/ADR-AI-001-llm-gateway.md) gateway and [ADR-AI-002](../02-architecture/adr/ADR-AI-002-model-aliases.md) aliases with fallbacks; adapters isolate cloud code.

## 10. Governance theater

- **What it looks like:** Policies and committees exist, but nothing is enforced and the inventory does not match reality.
- **Illustrative example:** An insurer's AI register listed twelve systems; the gateway logs showed thirty.
- **Blueprint control:** Policy gate in CI on the inventory; "not in the inventory, not in production"; gateway telemetry compared with inventory each quarter.

## 11. Rubber-stamp human in the loop

- **What it looks like:** A human "approves" every AI output, but has no time, evidence or authority to disagree.
- **Illustrative example:** A public agency's reviewers approved hundreds of AI-drafted letters a day, averaging seconds each.
- **Blueprint control:** [Human oversight policy](../01-governance/policies/human-oversight.md) section 3–4; override-rate monitoring; workload check in the [workforce impact assessment](../enablement/workforce-impact-assessment.md).

## 12. Token blind spend

- **What it looks like:** AI spend appears as one cloud line item; no one knows which use case costs what.
- **Illustrative example:** A retailer's monthly model bill tripled; it took weeks to trace the cause to one looping agent.
- **Blueprint control:** `use_case_id` tags on every call; [budgets](../finops/budgets.yaml) and gateway limits; agent step limits.

## 13. Orphaned bot

- **What it looks like:** An AI system keeps running after its owner leaves or its purpose ends.
- **Illustrative example:** A logistics firm found a chatbot still answering with a two-year-old rate card.
- **Blueprint control:** Named owner in the inventory; review dates checked by the policy gate; quarterly orphan check in the [retirement runbook](../ops/runbooks/model-retirement.md).
