# Frequently Asked Questions

| 5W1H | Answer |
|---|---|
| **Who** | Executives, architects, risk, procurement and delivery teams evaluating the kit |
| **What** | Short answers to common questions |
| **When** | Before and during adoption |
| **Where** | This file |
| **Why** | Saves repeat explanations |
| **How** | Scan the headings; follow links for detail |

## About the kit

**What is the kit?**
An open-source repo template, governance pack and architecture playbook for running AI as an enterprise capability. See the [executive summary](executive-summary.md).

**Is it free?**
Yes. Code is MIT-licensed and content is CC BY 4.0. Your costs are people's time and your normal cloud spend.

**Is it tied to one cloud or one model provider?**
No. Cloud-specific code is limited to `platform/adapters/` and `deploy/terraform/<cloud>/`. Models are reached by alias through the gateway. See [cloud mapping](cloud-mapping.md).

**Is it only for financial services?**
No. The author's background is financial services, but the kit is industry-neutral. Sector specifics go in `domain-packs/`.

**Do I have to adopt all of it?**
No. Common starting points are the governance pack alone, the gateway standard alone, or one pattern. The [maturity model](maturity-model.md) helps choose.

## Governance

**Will this slow teams down?**
It should speed up low-risk work. Tier 1 uses an asynchronous fast-track review (default target: 2 business days, set in `risk-tiers.yaml`). Effort is concentrated on Tier 3.

**Does the AI ARB replace our existing architecture board or risk committees?**
No. It is a specialty board that plugs into existing governance.

**Does using the kit make us compliant with the EU AI Act or certified to ISO/IEC 42001?**
No. The [control maps](../01-governance/control-maps/README.md) help you organize evidence. Compliance and certification depend on your own implementation, legal advice and, for ISO, an accredited audit.

**How do we handle AI features that vendors switch on inside our SaaS tools?**
Treat them as third-party AI: intake, tier, vendor questionnaire, inventory entry. See the [third-party AI policy](../01-governance/policies/third-party-ai.md).

## Architecture

**Why must every call go through a gateway?**
It is the one place to enforce data rules, quotas, logging, cost tagging and the kill switch. See [ADR-AI-001](../02-architecture/adr/ADR-AI-001-llm-gateway.md).

**Why aliases instead of model names?**
Models change often. Aliases let the platform change a model in one place, with evals, instead of in every app. See [ADR-AI-002](../02-architecture/adr/ADR-AI-002-model-aliases.md).

**Can we use agents?**
Yes, within the autonomy cap for the tier, with one identity per agent, least-privilege scopes and an approval queue for writes. See the [tool-using agent pattern](../02-architecture/patterns/tool-using-agent.md).

**Where does classic machine learning fit?**
Classic ML remains the right tool for many prediction and detection tasks. See the [classic ML with GenAI explanation pattern](../02-architecture/patterns/classic-ml-with-genai-explanation.md) and The Architect's ML Playbook.

## Operations and cost

**What happens if a model starts behaving badly in production?**
On-call uses the kill switch at the gateway; work goes to the human fallback; the [incident runbook](../ops/runbooks/ai-incident.md) covers the rest.

**How do we control cost?**
Tag every call by use case, set budgets with alerts and hard limits, right-size models and cache where safe. See the [cost model](../finops/cost-model.md).

## Examples and case studies

**Are the organization examples real clients?**
No. They are illustrative composites. Real case studies will only be published with written client approval. See [case studies](../case-studies/README.md).

**Can I contribute?**
Yes. Open an issue or pull request. Changes to standards need an ADR.
