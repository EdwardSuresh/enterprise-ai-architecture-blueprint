# Documentation Index

The map of the whole kit. Start with the [executive summary](executive-summary.md) if you are new.

| 5W1H | Answer |
|---|---|
| **Who** | Everyone using the kit |
| **What** | An index of every folder and key document |
| **When** | First visit, and whenever you need to find something |
| **Where** | This file |
| **Why** | The kit is broad; this page saves searching |
| **How** | Find your role below, then follow the links |

## Start here by role

| Role | Read first |
|---|---|
| CIO, chief AI officer | [Executive summary](executive-summary.md), [maturity model](maturity-model.md), [AI strategy template](../00-strategy/ai-strategy.md) |
| Head of EA | [Governance](../01-governance/README.md), [ARB](../01-governance/arb/README.md), [reference architecture](../02-architecture/reference-architecture.md) |
| Platform team | [Reference architecture](../02-architecture/reference-architecture.md), [integration standards](../02-architecture/standards/integration-standards.md), [deploy](../deploy/README.md), [ops](../ops/README.md) |
| Delivery team | [Which pattern when](../02-architecture/patterns/which-pattern-when.md), [intake form](../01-governance/arb/intake-form.yaml), [labs](../labs/) |
| Risk and compliance | [Control maps](../01-governance/control-maps/README.md), [policies](../01-governance/policies/), [impact assessment](../01-governance/impact-assessments/template.md) |
| Security | [Security](../security/README.md), [OWASP LLM map](../01-governance/control-maps/owasp-llm-top10.md) |
| Procurement | [Build, buy, partner](../00-strategy/build-buy-partner.md), [third-party AI policy](../01-governance/policies/third-party-ai.md), [vendor questionnaire](../01-governance/templates/vendor-questionnaire.md) |
| HR and learning | [Enablement](../enablement/README.md) |

## Repository map

| Folder | Contents |
|---|---|
| [00-strategy](../00-strategy/README.md) | Strategy, capability map, use-case portfolio, value scorecard, build-buy-partner |
| [01-governance](../01-governance/README.md) | Charter, RACI, policies, ARB, impact assessments, templates, control maps, risk tiers, AI inventory, policy-as-code |
| [02-architecture](../02-architecture/README.md) | Reference architecture, 10 patterns, standards, ADRs |
| `platform/` | Runnable kit package: gateway, guardrails, retrieval, tools, orchestrator, tracing, evals, policy gate, cloud adapters |
| `config/` | Model alias bindings |
| [data](../data/README.md) | Classification, data contracts, lineage |
| [security](../security/README.md) | Threat models, red team, agent identities |
| [finops](../finops/README.md) | Budgets, cost model |
| [ops](../ops/README.md) | SLOs, autonomy levels, runbooks |
| [enablement](../enablement/README.md) | Learning paths, champions, workforce impact |
| `domain-packs/` | Sector overlays |
| `labs/` | Hands-on labs |
| `evals/` | Evaluation suites and datasets |
| [deploy](../deploy/README.md) | Terraform module contracts, Docker, Kubernetes |
| [case-studies](../case-studies/README.md) | Client-approved case studies (none published yet) |
| docs | This folder |

## Docs in this folder

| Document | Purpose |
|---|---|
| [executive-summary.md](executive-summary.md) | Two-to-three-page overview for executives and procurement |
| [maturity-model.md](maturity-model.md) | 8 dimensions × 5 levels, with self-assessment |
| [rollout-day0.md](rollout-day0.md) | Week-by-week plan when no AI is in production |
| [rollout-plugin.md](rollout-plugin.md) | Week-by-week plan when AI is already running |
| [anti-patterns.md](anti-patterns.md) | 13 anti-patterns with kit controls |
| [cloud-mapping.md](cloud-mapping.md) | Kit capabilities mapped to AWS, Azure and Google Cloud services |
| [glossary.md](glossary.md) | Terms used in the kit |
| [faq.md](faq.md) | Common questions |

## A note on examples

Organization examples across the kit are **illustrative composites**, not client case studies.
