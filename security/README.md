# Security

AI adds new attack surfaces: prompts, retrieved content, tools, agents and model supply chains. This folder holds the threat model template, a starter red-team set and non-human identity scopes for agents.

| 5W1H | Answer |
|---|---|
| **Who** | CISO team, security architects, red team, platform team, delivery teams |
| **What** | Threat modelling, red teaming, agent identity and least privilege |
| **When** | Threat model at design (Tier 2+); red team before release and after major changes; scope review at every ARB |
| **Where** | Gateway, control plane, retrieval, agent runtime, tools |
| **Why** | Traditional security controls do not cover prompt injection, excessive agency or embedding leaks |
| **How** | STRIDE plus OWASP LLM Top 10 per use case; automated red-team prompts in CI; per-agent scopes |

## Contents

| Path | Purpose |
|---|---|
| [threat-models/template.md](threat-models/template.md) | STRIDE plus OWASP LLM threat model per use case |
| [red-team/](red-team/README.md) | Red-team approach and starter prompt set |
| [identity/agent-scopes.yaml](identity/agent-scopes.yaml) | Non-human identity and least-privilege scopes per agent |

## Core controls

| Control | Where | Reference |
|---|---|---|
| All model calls through the gateway | Layer 5 | [ADR-AI-001](../02-architecture/adr/ADR-AI-001-llm-gateway.md) |
| Input and output guardrails | Control plane, gateway | [OWASP map](../01-governance/control-maps/owasp-llm-top10.md) |
| Permission-aware retrieval | Retrieval layer | [Integration standard](../02-architecture/standards/integration-standards.md) §4 |
| One identity per agent, least privilege | Identity provider, tool registry | [agent-scopes.yaml](identity/agent-scopes.yaml) |
| Write actions through an approval queue | Tool registry | [Autonomy levels](../ops/autonomy-levels.md) |
| No secrets in prompts | Prompt registry | Integration standard §6.3 |
| Kill switch | Gateway | [AI incident runbook](../ops/runbooks/ai-incident.md) |

Report vulnerabilities in the blueprint itself as described in the repo's `SECURITY.md`.
