# Integration Standards

| 5W1H | Answer |
|---|---|
| **Who** | Platform engineers, delivery teams, integration architects |
| **What** | Rules for how AI systems call models, tools, data and each other |
| **When** | Design and build of every AI system; vendor integration |
| **Where** | Layers 2–5 of the [reference architecture](../reference-architecture.md) |
| **Why** | One way to integrate means one place to control, log and change |
| **How** | Follow the "must" rules below; CI and the policy gate check several of them |

## 1. LLM gateway (mandatory)

1.1 All model calls **must** go through the enterprise LLM gateway. No application or agent may call a model provider directly. See [ADR-AI-001](../adr/ADR-AI-001-llm-gateway.md).
1.2 Cloud SDKs for model providers **must** only be used inside the gateway's provider adapters (`platform/adapters/`).
1.3 Each call **must** carry a `use_case_id` so cost, quotas and logs are attributed.
1.4 The gateway **must** enforce: authentication, per-use-case quotas and budgets, data-class routing, content-safety checks, logging, and the kill switch.
1.5 Vendor products that cannot route through the gateway **must** be recorded as an exception with compensating controls (see [third-party AI policy](../../01-governance/policies/third-party-ai.md)).

## 2. Model aliases

2.1 Applications **must** request models by alias (for example `reasoning-large`, `reasoning-small`, `extraction`), never by provider model id. See [ADR-AI-002](../adr/ADR-AI-002-model-aliases.md).
2.2 Aliases and their bindings live in `config/models.yaml`. Allowed data classes per alias live in `approved-models.yaml`.
2.3 Changing what an alias points to is a model version change and follows the [runbook](../../ops/runbooks/model-version-change.md).

## 3. Tools through MCP with allow-lists

3.1 Agents **should** reach tools through Model Context Protocol (MCP) servers, or through the blueprint tool registry with the same contract.
3.2 Each agent **must** have its own non-human identity and an explicit tool allow-list in [agent-scopes.yaml](../../security/identity/agent-scopes.yaml).
3.3 Dynamic tool discovery **must not** be used in production. Only allow-listed servers and tools are reachable.
3.4 Write tools **must** go through the approval queue unless the ARB has approved L3 limits for that tool.
3.5 Tools **must** validate their own inputs and enforce business rules. Do not rely on the model to respect limits.
3.6 MCP servers **must** authenticate callers and pass end-user identity where the tool acts on the user's behalf.

## 4. Retrieval

4.1 Every retrieval call **must** pass the caller's identity or groups. Searching without an access filter is not allowed.
4.2 Each index **must** have a [data contract](../../data/contracts/README.md) naming its `acl_source`.
4.3 Indexes **should** be separated by data class.

## 5. Tracing (OpenTelemetry GenAI semantic conventions)

5.1 AI systems **must** emit traces using OpenTelemetry, following the GenAI semantic conventions for attribute names (for example `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`). The conventions are still evolving; pin the version you use.
5.2 One trace **must** cover the whole request: app, control plane, retrieval, each model call, each tool call, guardrail decisions and human review.
5.3 Kit-specific attributes use the `kit.` prefix: `kit.use_case_id`, `kit.risk_tier`, `kit.model_alias`, `kit.guardrail.decision`, `kit.cost_usd`.
5.4 Content capture (prompts and responses) follows the [logging standard](logging-standard.md).

## 6. Prompt registry

6.1 Production prompts **must** be stored in the prompt registry (versioned, reviewed), not hard-coded.
6.2 Each prompt has an id, version, owner, linked eval set and change history.
6.3 Prompts **must not** contain secrets, credentials or business rules that belong in code.
6.4 A prompt change is a release: run the eval suite before promotion.

## 7. API standards

7.1 AI capabilities exposed to other systems **must** use the organization's API standards (versioning, authentication, error model).
7.2 Responses **should** include: `trace_id`, `model_alias`, `sources` (when grounded), `ai_generated: true`, and a `review_required` flag when human review applies.
7.3 Structured outputs **must** be validated against a published JSON schema before being returned.
7.4 Long-running agent tasks **should** use asynchronous patterns (job id, status endpoint, callback or event).
7.5 Rate limits **must** be published per consumer.

## 8. Events

8.1 AI systems **should** publish key events (decision made, human override, guardrail block, kill switch) to the enterprise event backbone for monitoring and audit.

## 9. Compliance check

| Rule | Checked by |
|---|---|
| 1.1, 1.2 | CI dependency scan; code review |
| 2.1 | Policy gate (inventory `models` must be approved aliases) |
| 3.2, 3.4 | Agent scopes review at ARB; tool registry |
| 4.1 | Retrieval API rejects calls without groups |
| 5.1–5.3 | Trace sample at release review |
| 6.4 | Evals gate in CI |
