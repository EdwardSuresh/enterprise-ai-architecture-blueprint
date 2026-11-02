# Lab 07: Agent contracts

**Business case:** a bank's fee-dispute agent that reads fee history, requests refunds and delegates lookups to a sub-agent.

| | |
|---|---|
| **What** | One executable contract per agent, enforced by an independent layer, with four linked evidence records per step |
| **Why** | The agent must not enforce its own boundaries. Unauthorized actions must be prevented and audited when the model fails, instructions conflict or a delegate exceeds its scope |
| **Who** | System owner drafts the contract; the AI ARB approves it; the platform team runs the enforcer |
| **When** | Any agent at autonomy L2 or above, or any tool-using or multi-agent system |
| **Where** | `contracts/*.yaml`, `platform/core/kit/{contracts,enforcer,evidence}.py` |
| **How** | The model returns a plan; the enforcer approves the plan, then executes only approved steps the contract allows |

## Concept (no cloud)
```bash
pip install -e .
python labs/07-agent-contracts/concept.py
```
You will see six scenarios: a normal plan, a conflicting instruction, a model deviating from its plan, delegation that only narrows, revocation mid-task, and evidence with tamper detection.

## Build on Azure
1. Run the enforcer as its own service (for example Azure Container Apps) in front of tools. Agents running in Foundry Agent Service call tools only through it.
2. Put Azure API Management in front of the enforcer and the model endpoints; give agents no direct network route to tools or models.
3. Store contracts in a Git repo; deploy them through the CI policy gate; load them read-only into the enforcer.
4. Write evidence records to append-only storage (for example Azure Blob immutable storage) as well as the hash chain.
5. Use Entra ID workload identities per agent; the enforcer maps identity → contract.

**AWS:** Bedrock AgentCore with tools behind an API Gateway + Lambda enforcer; S3 Object Lock for evidence. **Google Cloud:** Vertex AI Agent Engine with tools behind Cloud Run + Apigee; Cloud Storage bucket lock for evidence. Service names change; check current documentation.

## Production
- Every agent in `01-governance/ai-inventory.yaml` at L2+ lists its contracts; `kit-policy-gate` checks them on every pull request.
- Contracts expire (`valid_until`) and are re-approved through the ARB; revocation is the incident kill switch for one agent.
- Add failure-mode tests to `tests/test_contracts.py` for each new agent: scope exceeded, conflicting instruction, plan deviation, revocation.
- Export the evidence ledger daily and run `verify()`; alert on any break.

## Exit criteria
- [ ] Every acting agent has an approved, unexpired contract
- [ ] No tool, model or memory call path bypasses the enforcer
- [ ] Failure-mode tests pass for each agent
- [ ] Evidence chain verifies end to end

**Maps to:** `contracts/`, `platform/core/kit/enforcer.py`, `02-architecture/agent-contracts.md`, `02-architecture/adr/ADR-AI-003-agent-contracts.md`, `ops/autonomy-levels.md`, OWASP LLM06 Excessive Agency.
