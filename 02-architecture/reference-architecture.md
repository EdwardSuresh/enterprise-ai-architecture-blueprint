# Reference Architecture

Seven layers. Every AI use case uses the same control plane, gateway and governance plane, whatever cloud or model it runs on.

| 5W1H | Answer |
|---|---|
| **Who** | Enterprise architects, platform engineers, solution architects |
| **What** | The logical layers of an enterprise AI platform and how a request flows through them |
| **When** | Platform design (Day-0), or gap analysis against an existing AI estate (plug-in) |
| **Where** | Cloud-neutral; map layers to services with [cloud-mapping.md](../docs/cloud-mapping.md) |
| **Why** | Shared layers mean controls are built once and applied everywhere |
| **How** | Build or map each layer; route every model call through the gateway; record decisions as ADRs |

## The seven layers

| # | Layer | Purpose | Main components |
|---|---|---|---|
| 1 | **Channels** | Where users and systems meet AI | Web, mobile, chat tools, contact centre, email, batch jobs, other systems |
| 2 | **Experience and API** | Product logic, authentication, session, output handling | Application back ends, API management, identity, UI disclosure |
| 3 | **AI control plane** | Orchestration and policy for AI work | Orchestrator or agent runtime, prompt registry, guardrails, evaluation hooks, human review queue |
| 4 | **Knowledge and tools** | What AI can read and do | Retrieval (search, vector index) with ACL filtering, MCP tool servers on allow-lists, data contracts |
| 5 | **Model access (LLM gateway)** | Single door to every model | Alias routing, auth, quotas, caching, content safety, logging, cost tags, kill switch |
| 6 | **Systems of record** | Where business truth lives | Core systems, ERP, CRM, case management, data platform |
| 7 | **Governance and operations plane** | Cross-cutting control and visibility | AI inventory, policy-as-code, observability, FinOps, incident management, evaluation store |

## Architecture view

```mermaid
flowchart TB
  subgraph L1["1. Channels"]
    C1["Web and mobile"]
    C2["Chat and collaboration tools"]
    C3["Contact centre"]
    C4["Batch and system events"]
  end
  subgraph L2["2. Experience and API"]
    E1["Application back ends"]
    E2["API management and identity"]
  end
  subgraph L3["3. AI control plane"]
    O1["Orchestrator and agent runtime"]
    O2["Prompt registry"]
    O3["Guardrails"]
    O4["Human review queue"]
  end
  subgraph L4["4. Knowledge and tools"]
    K1["ACL-aware retrieval"]
    K2["MCP tool servers on allow-list"]
  end
  subgraph L5["5. Model access"]
    G1["LLM gateway"]
    M1["Provider A models"]
    M2["Provider B models"]
    M3["Private or open-weight models"]
  end
  subgraph L6["6. Systems of record"]
    S1["Core business systems"]
    S2["Data platform"]
  end
  subgraph L7["7. Governance and operations plane"]
    V1["AI inventory"]
    V2["Policy-as-code"]
    V3["Observability and evals"]
    V4["FinOps"]
  end
  L1 --> L2 --> L3
  O1 --> K1
  O1 --> K2
  O1 --> G1
  G1 --> M1
  G1 --> M2
  G1 --> M3
  K1 --> S2
  K2 --> S1
  L3 -.-> L7
  G1 -.-> L7
  L4 -.-> L7
```

## Rules that hold across layers

1. **No direct model calls.** Every model call goes through the LLM gateway ([ADR-AI-001](adr/ADR-AI-001-llm-gateway.md)).
2. **Aliases, not model names.** Applications call aliases such as `reasoning-small`; the gateway maps them to approved models ([ADR-AI-002](adr/ADR-AI-002-model-aliases.md)).
3. **Retrieval honours source permissions.** The user's identity travels with the request.
4. **Tools through MCP on an allow-list**, with a non-human identity per agent and least-privilege scopes.
5. **Business rules stay in code or rules engines**, not in prompts.
6. **Everything is traced** with OpenTelemetry GenAI semantic conventions ([integration standards](standards/integration-standards.md)).
7. **There is always a human fallback** and a kill switch at the gateway.

## One guarded request, with human fallback

```mermaid
sequenceDiagram
  autonumber
  actor U as User
  participant APP as App and API
  participant CP as AI control plane
  participant GR as Guardrails
  participant KR as ACL-aware retrieval
  participant GW as LLM gateway
  participant M as Model (via alias)
  participant HQ as Human review queue
  U->>APP: Question (authenticated)
  APP->>CP: Request with user identity and use_case_id
  CP->>GR: Input check (injection, sensitive data)
  alt Input blocked
    GR-->>CP: Block with reason
    CP-->>APP: Safe refusal message
  else Input allowed
    CP->>KR: Retrieve with user permissions
    KR-->>CP: Permitted passages with sources
    CP->>GW: Prompt from registry plus passages, alias reasoning-small
    GW->>GW: Check kill switch, quota, data class route
    GW->>M: Model call
    M-->>GW: Draft answer
    GW-->>CP: Answer, tokens, trace id
    CP->>GR: Output check (grounding, redaction, policy)
    alt Output passes and confidence high
      CP-->>APP: Answer with citations and AI disclosure
    else Output fails or confidence low
      CP->>HQ: Route to human with context
      HQ-->>APP: Human answer
    end
  end
  APP-->>U: Response
```

## Layer responsibilities by team

| Layer | Owner | Typical consumers |
|---|---|---|
| 1–2 | Delivery teams | Business users |
| 3 | Platform (runtime, registry, guardrails) and delivery (flows) | Delivery teams |
| 4 | Data owners (retrieval content) and platform (tool hosting) | Agents, assistants |
| 5 | Platform | All AI systems |
| 6 | System owners | Tools and retrieval |
| 7 | Platform, EA, risk, FinOps | Everyone |

## Day-0 vs plug-in

- **Day-0:** build layers 3, 5 and 7 first, then onboard the first use case.
- **Plug-in:** put the gateway (layer 5) in front of existing AI use, register systems in the inventory (layer 7), then retrofit guardrails and retrieval controls. See [rollout-plugin.md](../docs/rollout-plugin.md).
