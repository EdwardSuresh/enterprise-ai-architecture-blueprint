# platform/core: the cloud-neutral runtime

The blueprint's reference code is the Python package `kit` (install with `pip install -e .` from the repo root). Only PyYAML is required.

| Module | Role | Lab |
|---|---|---|
| `kit.gateway` | Model aliases, fallback, cost tags, budgets, kill switch | 01 |
| `kit.retrieval` | Permission-aware retrieval with citations | 02 |
| `kit.guardrails` | PII redaction, prompt injection, sector rules, grounding | 03 |
| `kit.tools` | Agent identities, tool allow-lists, human approval queue | 04 |
| `kit.evals` | Golden-set runner and CI gate | 05 |
| `kit.policy_gate` | AI inventory validator and CI gate | 06 |
| `kit.prompts` | Versioned prompt registry: approved versions only, hash in every trace | 02 |
| `kit.memory` | Short-term conversation memory and long-term facts with retention, export and forget | 02 |
| `kit.orchestrator` | One guarded request end to end | all |
| `kit.tracing` | Spans with OpenTelemetry GenAI attribute names | all |

The `MockProvider` answers extractively from the supplied context, so every lab and test runs offline and deterministically. Real models plug in through `platform/adapters`.
