# Terraform: AWS Landing Zone Contract

| 5W1H | Answer |
|---|---|
| **Who** | Platform and cloud engineers on AWS |
| **What** | Resources an AWS landing zone needs for the blueprint, and the module inputs and outputs |
| **When** | Day-0 platform build, or adding AWS as a secondary or exit cloud |
| **Where** | One AWS account per environment, inside your AWS Organization |
| **Why** | Same contract as Azure and Google Cloud, so platform code is unchanged |
| **How** | Implement each module to this contract; wire outputs into `config/models.yaml` (`cloud_bindings.aws`) and the AWS adapter |

> Service names and features change. Verify against current AWS documentation. See [cloud mapping](../../../docs/cloud-mapping.md).

## Resources by module

| Module | Resources (typical) |
|---|---|
| `network` | VPC, private subnets across availability zones, VPC endpoints (PrivateLink) for Amazon Bedrock and other services, security groups, NAT or egress controls |
| `identity` | IAM roles for gateway, API and each agent (IRSA or EKS Pod Identity on EKS), permission boundaries |
| `secrets_keys` | AWS Secrets Manager, AWS KMS customer-managed keys per data class |
| `model_access` | Amazon Bedrock model access, inference profiles where used, Amazon Bedrock Guardrails configurations |
| `search` | Amazon OpenSearch Serverless collections, or Amazon Bedrock Knowledge Bases |
| `gateway` | Amazon API Gateway (private) plus the blueprint gateway service on the runtime |
| `runtime` | Amazon EKS cluster or Amazon ECS; Amazon ECR for images |
| `observability` | Amazon CloudWatch log groups and metrics, AWS X-Ray or an OpenTelemetry collector (for example AWS Distro for OpenTelemetry) |
| `data_governance` | AWS Lake Formation permissions, Amazon DataZone domain (optional) |
| `budgets` | AWS Budgets with alerts per cost allocation tag |

## Inputs

Common inputs from the [module interface](../../README.md#common-inputs), plus:

| Input | Type | Description |
|---|---|---|
| `aws_account_id` | string | Target account |
| `bedrock_model_ids` | map(string) | Alias → Bedrock model id or inference profile ARN |
| `guardrail_policies` | map(object) | Guardrail settings per alias or use case |
| `eks_version` | string | If using EKS |

## Outputs

Common outputs from the [module interface](../../README.md#common-outputs). AWS-specific values:

| Output | AWS value |
|---|---|
| `model_endpoints` | Bedrock model ids or inference profile ARNs via the VPC endpoint |
| `workload_identities` | IAM role ARNs |
| `key_ids` | KMS key ARNs |
| `otel_collector_endpoint` | Collector service address |

## Checks before go-live

- Bedrock is reached only through VPC endpoints from the gateway's role.
- No IAM role other than the gateway's can invoke models.
- KMS keys exist for confidential and restricted classes.
- Budgets alert on the `use_case_id` cost allocation tag.
