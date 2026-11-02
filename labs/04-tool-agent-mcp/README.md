# Lab 04: Tool-Using Agent and MCP

**Business case (Illustrative example):** A supply-chain team uses an agent to work purchase order (PO) exceptions. The agent may read POs freely. Any change to a PO waits for a buyer's approval. The agent cannot use tools it was not granted.

| 5W1H | Answer |
|---|---|
| **Who** | Buyers (approvers), procurement owners, security (identity), platform engineers |
| **What** | A tool registry with an allow-list, read vs write tools, a human approval queue for writes, and a scoped agent identity |
| **When** | When AI moves from answering to acting on systems of record |
| **Where** | `kit.tools` (`platform/core/kit/tools.py`), scopes in `security/identity/agent-scopes.yaml`, pattern in `02-architecture/patterns/tool-using-agent.md` |
| **Why** | Agents that can write to ERP or send messages can cause real loss. Least privilege and approval queues keep a human accountable |
| **How** | Concept with an in-memory registry, Build with a managed agent service or an MCP server, Production with scopes, audit and CI |

## Concept (plain Python, no cloud)

From the repo root:

```bash
pip install -e .
python labs/04-tool-agent-mcp/concept.py
```

What it shows:

1. **Tool registry with an allow-list.** Tools are registered with a kind (`read` or `write`) and a required scope.
2. **Scoped agent identity.** The `po-exception-agent` has only `po:read` and `po:write`, and only two allowed tools.
3. **Read tool runs at once.** `get_po` returns data.
4. **Write tool waits for approval.** `adjust_po_quantity` goes into the human approval queue (autonomy L2). It runs only after a buyer approves.
5. **Denied tool.** `delete_supplier` is not on the allow-list, so the call fails.
6. **Audit log.** Every call, approval and denial is recorded.

The same contract applies when tools are served by an MCP server: the agent sees only allowed tools, and writes still go through the queue.

## Build on Azure (reference implementation)

1. Create `rg-aikit-lab04` and a budget alert.
2. Build two tools against a fake PO store (a small Azure Function or container app with a JSON file or table): `get_po` (read) and `adjust_po_quantity` (write that only creates an approval request).
3. **Option A:** Create an agent in **Foundry Agent Service**. Add the tools as OpenAPI or function tools. Give the agent a managed identity with read-only access.
4. **Option B:** Expose the tools from an **MCP server** (for example on Azure Container Apps or Functions). Connect the agent to it. Expose only the allowed tools.
5. Route write requests to an approval step (for example a Logic App or a simple approval table). The write runs under the approver's authority, not the agent's.
6. Put **Azure API Management** in front of the tool APIs so each call is authenticated and logged.
7. Test: read a PO, propose a change, approve it, and try a tool that is not allowed.

## Build on AWS (short)

- Use **Amazon Bedrock AgentCore** (runtime, gateway, identity) or Bedrock Agents with action groups backed by Lambda.
- Use the AgentCore gateway to expose tools, including as MCP. Use IAM roles scoped to read-only for the agent.
- Use Step Functions or a queue for the human approval step.

## Build on Google Cloud (short)

- Use **Vertex AI Agent Engine** with the Agent Development Blueprint, with tools as functions or from an MCP server.
- Give the agent a service account with read-only roles. Use Workflows or a queue for approvals.

Service names and features change. Check the current docs for each provider.

## Production

1. Add the agent's identity and scopes to `security/identity/agent-scopes.yaml`.
2. Add the system to `01-governance/ai-inventory.yaml` with `autonomy_level: L2` and a system card. The policy gate checks that the autonomy level is allowed for the risk tier in `01-governance/risk-tiers.yaml`.
3. Write a threat model from `security/threat-models/template.md`. Cover tool misuse, injected instructions in supplier emails, and over-broad scopes.
4. Add golden cases for the agent's decisions, including "escalate" cases. See `domain-packs/supply-chain/use-cases/po-exception-resolution/spec.md`.
5. **CI gates:** `.github/workflows/policy-gate.yml` rejects autonomy above the tier limit. `.github/workflows/ci.yml` runs the tool registry tests and this lab's `concept.py`. `.github/workflows/evals.yml` runs the supply-chain golden set.
6. Evidence to keep: scope file history, approval queue records, audit log export, threat model.

## Exit criteria

- [ ] The agent cannot call a tool that is not on its allow-list.
- [ ] Every write waits for a named human approver.
- [ ] The agent identity has read-only access to the system of record.
- [ ] One cloud build uses a managed agent service or an MCP server.
- [ ] The audit log shows calls, approvals and denials.
- [ ] Policy gate passes with the agent's inventory entry.

## Cleanup

```bash
az group delete -n rg-aikit-lab04 --yes --no-wait
```

On AWS, delete the AgentCore resources, Lambda functions and Step Functions. On Google Cloud, delete the Agent Engine deployment and service accounts.

**Maps to:** `platform/core/kit/tools.py`, `platform/core/kit/tracing.py`, `security/identity/agent-scopes.yaml`, `security/threat-models/`, `02-architecture/patterns/tool-using-agent.md`, `01-governance/policies/human-oversight.md`, `01-governance/risk-tiers.yaml`, `domain-packs/supply-chain/`.
