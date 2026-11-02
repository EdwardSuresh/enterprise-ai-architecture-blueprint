# Terraform: Azure Landing Zone Contract

| 5W1H | Answer |
|---|---|
| **Who** | Platform and cloud engineers on Azure |
| **What** | Resources an Azure landing zone needs for the kit, and the module inputs and outputs |
| **When** | Day-0 platform build, or adding Azure as a secondary or exit cloud |
| **Where** | One subscription per environment under your management group hierarchy |
| **Why** | Same contract as AWS and Google Cloud, so platform code is unchanged |
| **How** | Implement each module to this contract; wire outputs into `config/models.yaml` (`cloud_bindings.azure`) and the Azure adapter |

> Service names and features change. Verify against current Microsoft documentation. See [cloud mapping](../../../docs/cloud-mapping.md).

## Resources by module

| Module | Resources (typical) |
|---|---|
| `network` | Virtual network, subnets, private endpoints and private DNS zones for Foundry or Azure OpenAI, Azure AI Search, Key Vault and storage; network security groups |
| `identity` | Managed identities (or Entra workload identities on AKS) for gateway, API and each agent; role assignments with least privilege |
| `secrets_keys` | Azure Key Vault; customer-managed keys per data class |
| `model_access` | Microsoft Foundry resource and project (or Azure OpenAI resource) with model deployments per alias; public network access disabled; Azure AI Content Safety and Prompt Shields |
| `search` | Azure AI Search with private endpoint |
| `gateway` | Azure API Management with AI gateway policies (token limits, logging), plus the kit gateway service if needed |
| `runtime` | Azure Kubernetes Service (AKS) or Azure Container Apps; Azure Container Registry |
| `observability` | Log Analytics workspace, Application Insights, Azure Monitor alerts; OpenTelemetry export |
| `data_governance` | Microsoft Purview account and data map integration |
| `budgets` | Azure Cost Management budgets filtered by tag |

## Inputs

Common inputs from the [module interface](../../README.md#common-inputs), plus:

| Input | Type | Description |
|---|---|---|
| `subscription_id` | string | Target subscription |
| `resource_group_name` | string | Platform resource group |
| `model_deployments` | map(object) | Alias → model name, version, deployment type and capacity |
| `apim_sku` | string | API Management tier |

## Outputs

Common outputs from the [module interface](../../README.md#common-outputs). Azure-specific values:

| Output | Azure value |
|---|---|
| `model_endpoints` | Foundry or Azure OpenAI deployment names and private endpoint |
| `workload_identities` | Managed identity client ids |
| `key_ids` | Key Vault key ids |
| `otel_collector_endpoint` | Application Insights connection or collector address |

## Checks before go-live

- Public network access is disabled on model, search and Key Vault resources.
- Only the gateway identity has a role that can call model deployments.
- API Management logs token usage per `use_case_id`.
- Budgets alert on the `use_case_id` tag.
