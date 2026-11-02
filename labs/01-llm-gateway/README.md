# Lab 01: LLM Gateway

**Business case (Illustrative example):** A bank sends every model call through one gateway. Teams use model aliases, not vendor model names. The gateway handles fallback, cost tags per use case, budgets and a kill switch.

| 5W1H | Answer |
|---|---|
| **Who** | Platform engineers, architects, FinOps, the AI risk team |
| **What** | One entry point for all model calls with aliases, fallback, cost tags, budgets and a kill switch |
| **When** | Before the second team starts using models. Retro-fit it if teams already call models directly |
| **Where** | `kit.gateway` (`platform/core/kit/gateway.py`), aliases in `config/models.yaml`, cloud adapters in `platform/adapters/` |
| **Why** | Without a gateway, every team picks its own model, keys and logging. Costs, outages and model changes hit each app separately |
| **How** | Concept with mock providers, Build with a managed AI gateway in front of a model deployment, Production with policy and CI checks |

## Concept (plain Python, no cloud)

From the repo root:

```bash
pip install -e .
python labs/01-llm-gateway/concept.py
```

What it shows:

1. **Model aliases.** The app asks for `reasoning-large`. `config/models.yaml` decides which provider and model serve it.
2. **Fallback.** The primary mock provider fails. The gateway moves to the next route without the app changing.
3. **Cost tags and budgets.** Every call is tagged with a `use_case`. Spend is tracked per use case. A use case stops when it hits its budget.
4. **Kill switch.** An alias or use case can be switched off during an incident.
5. **Tracing.** Each call records a span through `kit.tracing`.

Try this: add a new alias in `config/models.yaml` and call it. Then remove the fallback list and rerun step 2.

## Build on Azure (reference implementation)

1. Create a resource group `rg-aikit-lab01` and a budget alert on it.
2. In **Microsoft Foundry**, create a project and deploy one small model as a standard (pay-per-token) deployment. Note the deployment name.
3. Create **Azure API Management** (choose a low-cost tier; check pricing, as some tiers bill by the hour). Import the model endpoint as an API using the AI gateway feature.
4. Add the **token limit policy** (tokens per minute per subscription key) and the **token metric policy** so usage is reported by a dimension such as `use_case`.
5. Use **managed identity** from API Management to the model endpoint. Do not hand out model keys to apps.
6. Add a second backend (another region or a smaller model) and configure a backend pool or retry so APIM falls back on errors such as 429 or 5xx.
7. Put the deployment name in `cloud_bindings.azure` in `config/models.yaml`. Point the Azure adapter (`platform/adapters/kit_adapters/azure.py`) at the APIM endpoint.
8. Run the same calls as the Concept lab. Check token metrics in Application Insights or Azure Monitor.

## Build on AWS (short)

- Call models through **Amazon Bedrock**. Use cross-Region inference profiles for resilience.
- Put **Amazon API Gateway** with usage plans, or a small proxy, in front for per-team keys and throttling.
- Tag spend with application inference profiles or request metadata. Track cost with AWS Budgets and Cost Explorer.
- Bind aliases in `cloud_bindings.aws` and use `platform/adapters/kit_adapters/aws.py`.

## Build on Google Cloud (short)

- Call models through **Vertex AI**. Use the global endpoint or several regions for resilience.
- Put **Apigee** (or API Gateway) in front for quotas and keys. Apigee has policies for LLM token counting.
- Tag requests with labels for cost reporting. Set a Cloud Billing budget.
- Bind aliases in `cloud_bindings.gcp` and use `platform/adapters/kit_adapters/gcp.py`.

Service names and features change. Check the current docs for each provider.

## Production

1. Record the gateway decision as an ADR. See `02-architecture/adr/ADR-AI-001-llm-gateway.md` and `ADR-AI-002-model-aliases.md`.
2. Make sure every model alias used in `01-governance/ai-inventory.yaml` maps to an entry in `02-architecture/standards/approved-models.yaml`.
3. Set budgets per use case and record them with the owner.
4. Write a short runbook for the kill switch: who can use it, how, and how to restore.
5. **CI gates:** `.github/workflows/policy-gate.yml` fails a pull request that uses an unapproved model. `.github/workflows/ci.yml` runs the gateway tests and this lab's `concept.py`.
6. Evidence to keep: alias config history (git), gateway metrics export, budget alert settings, kill switch test record.

## Exit criteria

- [ ] I can explain why apps use aliases, not model names.
- [ ] The Concept lab shows fallback, budget stop and kill switch.
- [ ] On one cloud, a call goes through the gateway with managed identity and a token limit.
- [ ] Token usage shows up per use case in monitoring.
- [ ] Policy gate passes for the inventory in this repo.

## Cleanup

```bash
az group delete -n rg-aikit-lab01 --yes --no-wait
```

On AWS, delete the API Gateway stage and any inference profiles you made. On Google Cloud, delete the Apigee environment or the project. API gateways can bill by the hour, so do not leave them running.

**Maps to:** `platform/core/kit/gateway.py`, `platform/core/kit/tracing.py`, `config/models.yaml`, `platform/adapters/`, `02-architecture/adr/`, `02-architecture/standards/approved-models.yaml`, `01-governance/ai-inventory.yaml`, `domain-packs/financial-services/`.
