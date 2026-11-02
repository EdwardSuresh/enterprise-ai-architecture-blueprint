# Architecture Decision Records

Decisions that shape the blueprint itself. Use-case teams write their own ADRs with the [ADR template](../../01-governance/templates/adr-ai.md).

| 5W1H | Answer |
|---|---|
| **Who** | Proposed by architects or platform engineers; accepted by the ARB |
| **What** | One record per significant, hard-to-reverse decision |
| **When** | When the decision is made; superseded, not edited, when it changes |
| **Where** | This folder, numbered `ADR-AI-NNN-short-title.md` |
| **Why** | Future teams can see what was decided, why, and what was rejected |
| **How** | Copy the template, fill it, open a pull request, ARB accepts |

## Index

| ADR | Title | Status |
|---|---|---|
| [ADR-AI-001](ADR-AI-001-llm-gateway.md) | All model calls go through an enterprise LLM gateway | Accepted |
| [ADR-AI-002](ADR-AI-002-model-aliases.md) | Applications use model aliases, not provider model ids | Accepted |
| [ADR-AI-003](ADR-AI-003-agent-contracts.md) | Executable agent contracts enforced outside the agent | Accepted |

## Status values

Proposed → Accepted → (Superseded by ADR-AI-NNN | Deprecated)
