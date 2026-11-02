# Standards

Standards are the few rules every AI system must follow, whatever pattern or cloud it uses. They are short on purpose. Where possible they are enforced by the gateway, CI or the policy gate rather than by review alone.

| 5W1H | Answer |
|---|---|
| **Who** | Owned by EA and the platform team; followed by every delivery team |
| **What** | Integration standard, logging standard, approved models list |
| **When** | Apply at design; checked at ARB and in CI |
| **Where** | All environments that call models |
| **Why** | Shared rules make shared controls possible |
| **How** | Read the standard, meet the "must" rules, record any exception in the ARB decision log |

| File | Scope |
|---|---|
| [integration-standards.md](integration-standards.md) | LLM gateway, model aliases, MCP tools, tracing, prompt registry, APIs |
| [logging-standard.md](logging-standard.md) | What to log, where, for how long, and what never to log |
| `approved-models.yaml` | Approved model aliases and the data classes each may receive (maintained separately; read by the policy gate) |

## Language

- **Must**: required. An exception needs ARB approval with an expiry date.
- **Should**: expected. Deviate only with a recorded reason in the ADR.
- **May**: optional.

## Changing a standard

Open a pull request with the change and an ADR in [../adr/](../adr/README.md). The ARB approves. Give delivery teams a migration period for breaking changes.
