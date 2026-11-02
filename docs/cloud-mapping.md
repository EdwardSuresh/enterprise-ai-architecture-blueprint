# Cloud Mapping

How blueprint capabilities map to services on AWS, Microsoft Azure and Google Cloud.

> **Names change often.** Cloud providers rename, merge and retire services frequently. Verify every row against current provider documentation before design decisions. Being listed here is not an endorsement or a statement of feature parity.

| 5W1H | Answer |
|---|---|
| **Who** | Platform architects and engineers |
| **What** | A capability-to-service table across the three major clouds |
| **When** | Landing zone design; adapter development; cloud comparison |
| **Where** | Applies to the [reference architecture](../02-architecture/reference-architecture.md) layers |
| **Why** | The blueprint is cloud-neutral; this table shows how to realize it on each cloud |
| **How** | Pick the cloud column; check the service still exists and fits; record choices in an ADR |

## Mapping

| Capability (blueprint layer) | AWS | Azure | Google Cloud |
|---|---|---|---|
| **Foundation models** (5) | Amazon Bedrock | Microsoft Foundry (formerly Azure AI Foundry) and Azure OpenAI | Vertex AI Model Garden |
| **Agent runtime** (3) | Amazon Bedrock AgentCore | Foundry Agent Service | Vertex AI Agent Engine |
| **LLM gateway** (5) | Amazon API Gateway plus custom gateway service | Azure API Management (AI gateway capabilities) | Apigee |
| **Guardrails** (3, 5) | Amazon Bedrock Guardrails | Azure AI Content Safety and Prompt Shields | Model Armor |
| **Vector search and RAG** (4) | Amazon Bedrock Knowledge Bases; Amazon OpenSearch Serverless | Azure AI Search | Vertex AI Search; Vertex AI RAG Engine; Vertex AI Vector Search |
| **Classic ML** | Amazon SageMaker AI | Azure Machine Learning | Vertex AI |
| **Observability** (7) | Amazon CloudWatch; AWS X-Ray | Azure Monitor; Application Insights | Cloud Trace; Cloud Monitoring |
| **Identity, secrets and keys** | AWS IAM; AWS Secrets Manager; AWS KMS | Microsoft Entra ID; Azure Key Vault | Cloud IAM; Secret Manager; Cloud KMS |
| **Data governance** (4, 7) | AWS Lake Formation; Amazon SageMaker Unified Studio (formerly Amazon DataZone) | Microsoft Purview | Dataplex Universal Catalog |
| **Containers** | Amazon EKS | Azure Kubernetes Service (AKS) | Google Kubernetes Engine (GKE) |

## Notes

- **Gateway.** Managed API gateways provide auth, quotas and logging. Blueprint features such as alias resolution, data-class routing and the kill switch may need a thin custom service on any cloud. The blueprint's own gateway (`platform/core/kit/gateway.py`) shows the contract.
- **Third-party models.** Models from several providers are available through each cloud's model catalog, and some directly from the model provider. Route all of them through your gateway.
- **Tracing.** Prefer OpenTelemetry instrumentation exported to the cloud's observability service, so traces stay portable.
- **Multi-cloud.** Only `platform/adapters/` and `deploy/terraform/<cloud>/` should contain cloud-specific code.

## On-premises and other options

The same layers can run on-premises with open-weight models, a self-hosted gateway, an open-source vector store and OpenTelemetry collectors. Apply the same data-class hosting rules.
