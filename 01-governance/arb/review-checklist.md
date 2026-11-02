# ARB Review Checklist

Tiers are cumulative: Tier 2 includes every Tier 1 item; Tier 3 includes every Tier 2 item.

| 5W1H | Answer |
|---|---|
| **Who** | ARB members and the EA delegate for fast-track |
| **What** | The questions the ARB must be able to answer "yes" to, by tier |
| **When** | Design review (before build) and release review (before production) |
| **Where** | Attach the completed checklist to the ARB pack |
| **Why** | Consistent reviews; teams know in advance what "ready" means |
| **How** | Mark each item Yes / No / N/A with a link to evidence. A "No" becomes a condition or a reason to defer |

## Tier 1 (all AI systems)

| # | Check | Stage | Evidence |
|---|---|---|---|
| 1.1 | Use case is in the portfolio with sponsor and success metric | Design | Portfolio row, intake form |
| 1.2 | Tier and autonomy level are recorded and autonomy is within the tier maximum | Design | Intake form |
| 1.3 | Uses an approved pattern from the pattern catalog, or explains why not | Design | ADR |
| 1.4 | All model calls go through the LLM gateway using model aliases | Design | ADR, gateway config |
| 1.5 | Data class is known and the model hosting matches the class rule | Design | Classification, gateway route |
| 1.6 | Acceptable-use rules apply; users are told they are using AI | Design | UI copy |
| 1.7 | A basic evaluation set exists and passes agreed thresholds | Release | Eval report |
| 1.8 | Logging meets the logging standard | Release | Trace sample |
| 1.9 | A budget and alert are set in FinOps | Release | `finops/budgets.yaml` |
| 1.10 | Inventory entry exists with a named owner and kill switch | Release | `ai-inventory.yaml` |

## Tier 2 (adds)

| # | Check | Stage | Evidence |
|---|---|---|---|
| 2.1 | Threat model completed with STRIDE and OWASP LLM risks | Design | Threat model |
| 2.2 | Retrieval enforces the source permissions of the requesting user | Design | Data contract `acl_source`, test result |
| 2.3 | Guardrails configured for input and output (injection, sensitive data, harmful content) | Design | Gateway policy |
| 2.4 | Agents use non-human identities with least-privilege scopes and tool allow-lists | Design | `agent-scopes.yaml` |
| 2.5 | Data contracts exist for production data sources | Design | `data/contracts/` |
| 2.6 | Human oversight design meets the human oversight policy | Design | Oversight section of ADR |
| 2.7 | Red-team tests run and failures fixed or accepted | Release | Red-team report |
| 2.8 | Evaluation covers accuracy, groundedness, safety and regression against the previous version | Release | Eval report |
| 2.9 | SLOs defined and monitored | Release | `ops/slo.yaml` |
| 2.10 | Incident runbook adapted, on-call named, fallback to human queue tested | Release | Runbook, test record |
| 2.11 | Third-party AI questionnaire complete (if bought) | Design | Vendor questionnaire |
| 2.12 | Model version change process agreed, including vendor notice | Release | Runbook link |

## Tier 3 (adds)

| # | Check | Stage | Evidence |
|---|---|---|---|
| 3.1 | AI impact assessment completed and signed off | Design | Impact assessment |
| 3.2 | Legal has confirmed regulatory classification (for example EU AI Act high-risk) and obligations | Design | Legal note |
| 3.3 | Fairness tests across relevant groups with agreed thresholds | Release | Eval report |
| 3.4 | Explanations given to reviewers and, where required, to affected people | Release | UI and notice samples |
| 3.5 | Autonomy no higher than L2; reviewer can override; override rate monitored | Release | Oversight metrics |
| 3.6 | Contest and redress route for affected people works | Release | Process document, test |
| 3.7 | Workforce impact assessment done where roles change | Design | Workforce assessment |
| 3.8 | Post-release review scheduled at 30 and 90 days | Release | Decision log |
| 3.9 | Technical documentation enough for regulator or auditor request | Release | System card, ADRs, eval reports |
