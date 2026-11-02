# Agent contracts

| | |
|---|---|
| **What** | One machine-readable contract per agent covering planning, models, data classes, memory, tools, delegation and execution limits |
| **Why** | The agent must not enforce its own boundaries. The model proposes; the contract defines obligations; an independent execution layer enforces them |
| **Who** | System owner drafts; AI ARB approves (`approved_by` = ARB id); platform team runs the enforcer |
| **When** | Required for every AI system at autonomy L2 or above, or using the tool-agent or multi-agent pattern. Re-approved before `valid_until` |
| **Where** | `contracts/<agent>.yaml`, referenced from `01-governance/ai-inventory.yaml` |
| **How** | `kit.enforcer.ContractEnforcer` enforces at runtime; `kit-policy-gate` validates in CI |

## Rules
- **Delegation only narrows.** A delegate's effective contract is the intersection of its own and its parent's, with the tighter of every limit. See `kit/contracts.py: narrow()`.
- **Authority comes only from the contract.** Text in prompts, retrieved documents or tool output can never widen it.
- **Plans are approved before execution;** a step that is not in the approved plan is refused, even if the model asks for it later.
- **Contracts are live.** Revoking or expiring a contract stops running tasks at their next step.
- **Every step leaves four linked evidence records** (provenance, verification, authorization, execution) in a hash-chained ledger, including denials.
- Write tools at L0–L2 must require human approval; L3 may act within stated limits.

See `02-architecture/agent-contracts.md` and `labs/07-agent-contracts/`.
