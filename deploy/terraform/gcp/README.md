# Terraform: Google Cloud Landing Zone Contract

| 5W1H | Answer |
|---|---|
| **Who** | Platform and cloud engineers on Google Cloud |
| **What** | Resources a Google Cloud landing zone needs for the blueprint, and the module inputs and outputs |
| **When** | Day-0 platform build, or adding Google Cloud as a secondary or exit cloud |
| **Where** | One project per environment under your organization and folder hierarchy |
| **Why** | Same contract as AWS and Azure, so platform code is unchanged |
| **How** | Implement each module to this contract; wire outputs into `config/models.yaml` (`cloud_bindings.gcp`) and the Google Cloud adapter |

> Service names and features change. Verify against current Google Cloud documentation. See [cloud mapping](../../../docs/cloud-mapping.md).

## Resources by module

| Module | Resources (typical) |
|---|---|
| `network` | VPC network, subnets, Private Service Connect or Private Google Access for Vertex AI, VPC Service Controls perimeter, firewall rules |
| `identity` | Service accounts for gateway, API and each agent; Workload Identity Federation for GKE; least-privilege IAM roles |
| `secrets_keys` | Secret Manager; Cloud KMS keys per data class (CMEK) |
| `model_access` | Vertex AI API enablement, Model Garden model access, regional endpoints; Model Armor templates |
| `search` | Vertex AI Search, Vertex AI RAG Engine or Vertex AI Vector Search index and endpoint |
| `gateway` | Apigee (or API Gateway) with policies, plus the blueprint gateway service |
| `runtime` | Google Kubernetes Engine (GKE) or Cloud Run; Artifact Registry |
| `observability` | Cloud Logging buckets and sinks, Cloud Monitoring, Cloud Trace; OpenTelemetry export |
| `data_governance` | Dataplex lakes and zones, data catalog integration |
| `budgets` | Cloud Billing budgets filtered by label |

## Inputs

Common inputs from the [module interface](../../README.md#common-inputs), plus:

| Input | Type | Description |
|---|---|---|
| `project_id` | string | Target project |
| `vertex_models` | map(string) | Alias → Vertex AI model name and region |
| `vpc_sc_perimeter` | string | Service perimeter name |

Note: Google Cloud uses **labels** for cost attribution; map the `tags` input to labels.

## Outputs

Common outputs from the [module interface](../../README.md#common-outputs). Google Cloud-specific values:

| Output | Google Cloud value |
|---|---|
| `model_endpoints` | Vertex AI model names and regional endpoints |
| `workload_identities` | Service account emails |
| `key_ids` | Cloud KMS key resource names |
| `otel_collector_endpoint` | Collector address or Cloud Trace exporter settings |

## Checks before go-live

- Vertex AI is inside the VPC Service Controls perimeter.
- Only the gateway service account holds the role that can call models.
- CMEK is set for confidential and restricted data stores.
- Budgets alert on the `use_case_id` label.
