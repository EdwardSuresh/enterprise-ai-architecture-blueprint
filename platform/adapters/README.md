# Cloud adapters

| | |
|---|---|
| **What** | Thin classes that let the LLM gateway call Microsoft Foundry / Azure OpenAI, Amazon Bedrock, Google Vertex AI or the Claude API |
| **Why** | Keeps cloud SDKs out of agents, so changing cloud means changing config and one adapter |
| **Who** | Cloud platform team |
| **When** | When you move a lab from Concept to Build, or add a second cloud |
| **Where** | `platform/adapters/kit_adapters/` (installed as the `kit_adapters` package) |
| **How** | `pip install -e .[azure]` then `get_provider("azure")`, and map aliases in `config/models.yaml` → `cloud_bindings` |

```python
from kit.gateway import Gateway
from kit_adapters import get_provider

gw = Gateway.from_config(providers={"azure": get_provider("azure")})
```
Then point the alias routes in `config/models.yaml` at `provider: azure` with your deployment names.

Adapters are reference code and are not run in CI (no cloud credentials there). Verify them in your sandbox. Map every SDK error to `ProviderError` so the gateway can fall back.
