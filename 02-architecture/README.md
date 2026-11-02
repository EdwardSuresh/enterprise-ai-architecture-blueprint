# 02 Architecture

One reference architecture, a catalog of reusable patterns, a small set of standards, and the decisions behind them. Teams pick a pattern, follow the standards, and record their choices as ADRs.

| 5W1H | Answer |
|---|---|
| **Who** | Enterprise and solution architects, platform team, delivery teams |
| **What** | Reference architecture (7 layers), 10 solution patterns, integration and logging standards, ADRs |
| **When** | Design stage of every use case; platform decisions as they arise |
| **Where** | Applies on AWS, Azure, Google Cloud or on-premises (see [cloud mapping](../docs/cloud-mapping.md)) |
| **Why** | Reuse beats reinvention. Shared layers give shared controls |
| **How** | Start at [which-pattern-when](patterns/which-pattern-when.md), apply the pattern, meet the standards, write an ADR |

## Contents

| Path | Purpose |
|---|---|
| [reference-architecture.md](reference-architecture.md) | The 7-layer architecture and a guarded request flow |
| [patterns/which-pattern-when.md](patterns/which-pattern-when.md) | Decision flow to choose a pattern |
| [patterns/](patterns/) | Ten solution patterns |
| [standards/](standards/README.md) | Integration and logging standards; approved models list (`approved-models.yaml`, maintained separately) |
| [adr/](adr/README.md) | Architecture decision records for the kit itself |

## Pattern catalog

| Pattern | One-line summary |
|---|---|
| [RAG assistant](patterns/rag-assistant.md) | Answers questions from your own documents with citations |
| [Document extraction](patterns/document-extraction.md) | Turns documents into structured, validated data |
| [Tool-using agent](patterns/tool-using-agent.md) | Plans and calls approved tools to complete a task |
| [Copilot in app](patterns/copilot-in-app.md) | AI help inside an existing business application |
| [Multi-agent orchestration](patterns/multi-agent-orchestration.md) | Several specialist agents coordinated by an orchestrator |
| [Classic ML with GenAI explanation](patterns/classic-ml-with-genai-explanation.md) | Trained model decides; LLM explains in plain words |
| [Anomaly detection with agent triage](patterns/anomaly-detection-agent-triage.md) | Detector flags; agent gathers context and proposes action |
| [Conversational customer agent](patterns/conversational-customer-agent.md) | Customer-facing chat or voice with handoff to humans |
| [Content generation](patterns/content-generation.md) | Drafts text for human review and approval |
| [Vision-LLM report](patterns/vision-llm-report.md) | Images in, structured findings and a report out |
