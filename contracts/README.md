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
- **Intents are bound to actions.** Each intent lists exactly the `tools`, `models`, `memory` (`short`, `long`) or `delegates` it may use; a step whose action does not match its intent is rejected.
- **Plans are approved once, before execution;** each approved step runs at most once, and a step that is not in the approved plan is refused.
- **Human approvals go through the enforcer** (`enforcer.approve(task, id, approver)`), which re-checks the contract and records the approver.
- **Delegation shares one budget.** Cost and tool calls are counted across the whole chain.
- **Memory is bound to the task subject** (user and conversation from the task source).
- **Contracts are live.** Revoking or expiring a contract stops running tasks at their next step.
- **Every step leaves four linked evidence records** (provenance, verification, authorization, execution) in a hash-chained ledger, including denials.
- Write tools at L0–L2 must require human approval; L3 may act within stated limits. Read tools cannot require approval; `max_amount` must be positive; `amount_arg` names the argument it applies to.
- The runtime loads only contracts referenced by a non-retired inventory entry (`ContractStore.from_inventory()`); the policy gate flags orphan and duplicate contracts.

See `02-architecture/agent-contracts.md` and `labs/07-agent-contracts/`.
