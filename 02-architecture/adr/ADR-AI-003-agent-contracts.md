# ADR-AI-003: Executable agent contracts enforced outside the agent

**Status:** Accepted · **Date:** 2026-11-02 · **Applies to:** autonomy L2+, tool-using, conversational and multi-agent systems

## Context
Tool allow-lists and approval queues protected individual tool calls, but planning, memory and delegation were not governed by one binding definition, and the evidence for a step mixed together where it came from, what was checked, who allowed it and what happened. A public review of the blueprint asked whether its contracts are documented or executable across the whole stack.

## Options considered
1. Keep per-tool controls; document the rest in policies.
2. Ask the model to follow a contract placed in its system prompt.
3. One machine-readable contract per agent, enforced by a separate execution layer that approves plans and authorizes each step, with narrowing on delegation and four kinds of evidence.

## Decision
Option 3. The model may only propose plans. The contract enforcer approves the plan, then authorizes each step against the live contract. Delegation uses the intersection of parent and child contracts. Every step writes provenance, verification, authorization and execution records to a hash-chained ledger. Option 2 is rejected because a model cannot be the enforcer of its own boundaries.

## Consequences
- Plus: unauthorized actions are prevented and audited even when the model fails or is manipulated.
- Plus: one artifact for the ARB to approve, revoke and expire.
- Minus: agents must express actions as structured plan steps; free-text tool use is not allowed.
- Minus: the enforcer must be deployed as a service with no bypass path in production.

## Controls
`kit-policy-gate` requires contracts for in-scope systems and checks ARB id, autonomy, models, data classes, expiry and delegate coverage. Failure-mode tests in `tests/test_contracts.py`.
