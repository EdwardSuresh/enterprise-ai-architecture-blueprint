# Docker

Container guidance for the blueprint services: the reference API (`api/app.py`), the LLM gateway and any MCP tool servers.

| 5W1H | Answer |
|---|---|
| **Who** | Platform engineers |
| **What** | How to build and run blueprint service images |
| **When** | Local testing, CI, and before deploying to Kubernetes or managed containers |
| **Where** | Any OCI-compatible registry and runtime |
| **Why** | One image per service, built the same way on every cloud |
| **How** | Small base image, non-root user, no secrets in the image, configuration by environment and mounted files |

## Images

| Image | Contents | Entry point |
|---|---|---|
| `kit-api` | Reference API and `kit` package | `uvicorn api.app:app --host 0.0.0.0 --port 8080` |
| `kit-gateway` | Gateway service and cloud adapter for the target cloud | Gateway service entry point |
| `kit-tools-<name>` | One MCP tool server per system of record | Tool server entry point |

## Build rules

1. Use a slim, maintained Python base image with a pinned version.
2. Install only the extras needed (for example `.[api,azure]`).
3. Run as a non-root user.
4. No secrets, keys or `.env` files in images. Use the cloud secret store and workload identity.
5. Mount `config/models.yaml`, `kit.yaml` and policy files read-only, or bake them into versioned config images.
6. Scan images in CI; sign images; record the digest in the release.
7. Expose health (`/healthz`) and readiness endpoints.

## Configuration

| Setting | Source |
|---|---|
| Cloud and provider | `kit.yaml` `primary_cloud`, `config/models.yaml` `cloud_bindings` |
| Gateway endpoint | Terraform output `gateway_endpoint` |
| Trace export | `OTEL_EXPORTER_OTLP_ENDPOINT` from `otel_collector_endpoint` |
| Identity | Workload identity provided by the runtime |

## Local run

Local runs use the offline mock providers, so no cloud account is needed. See the repo README quick start.
