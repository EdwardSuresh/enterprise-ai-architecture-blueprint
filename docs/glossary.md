# Glossary

| 5W1H | Answer |
|---|---|
| **Who** | Anyone reading the blueprint |
| **What** | Plain definitions of terms used across the blueprint |
| **When** | Whenever a term is unclear |
| **Where** | Terms are used across all folders |
| **Why** | Shared words prevent misunderstanding between business, risk and technology |
| **How** | Alphabetical list; links point to where the term is used most |

| Term | Definition |
|---|---|
| **Acceptable use policy** | Rules for how staff may use AI tools. See [policy](../01-governance/policies/acceptable-use.md). |
| **ACL source** | The system whose access permissions control who may retrieve a piece of content. Recorded in each data contract. |
| **ADR (Architecture Decision Record)** | A short document recording one significant decision, its options and reasons. |
| **Agent** | An AI system that plans steps and calls tools to complete a task. |
| **AI impact assessment** | A structured assessment of how an AI system could affect people. Required for Tier 3. |
| **AI inventory** | The authoritative list of AI systems with owner, tier, models and status (`ai-inventory.yaml`). |
| **Alias (model alias)** | A capability name such as `reasoning-small` that the gateway maps to an approved model. |
| **Approval queue** | Where write actions wait for a human to approve them before they run. |
| **ARB (Architecture Review Board)** | The body that reviews and approves AI systems. See [ARB](../01-governance/arb/README.md). |
| **Autonomy level** | L0–L4 scale of how much an AI system does without a human. See [autonomy levels](../ops/autonomy-levels.md). |
| **Canary release** | Releasing a change to a small share of traffic first, to catch problems early. |
| **Champion** | A staff member who helps peers adopt AI well. |
| **Chargeback / showback** | Charging (or showing) AI costs to the business unit that incurs them. |
| **Chunk** | A piece of a document stored in a search index for retrieval. |
| **Classic ML** | Machine learning models trained on structured data for prediction, classification or detection. |
| **Control plane (AI)** | The layer that orchestrates AI work and applies policies, prompts and guardrails. |
| **Data class** | One of public, internal, confidential, restricted. Sets where data may be processed. |
| **Data contract** | An agreement describing a data source's owner, schema, quality, class and access rules. |
| **Drift** | A change over time in data or model behaviour that reduces quality. |
| **Embedding** | A numeric representation of text or images used for similarity search. |
| **Evaluation (eval)** | A repeatable test of AI quality or safety against a set of cases and thresholds. |
| **Fallback (human)** | The non-AI path used when the AI is switched off or unsure. |
| **Fine-tuning** | Further training a model on your own data to adapt its behaviour. |
| **FinOps** | The practice of managing cloud and AI cost with shared accountability. |
| **Foundation model** | A large, general model trained on broad data and adapted to many tasks. |
| **General-purpose AI (GPAI)** | EU AI Act term for models usable for many tasks, with specific provider obligations. |
| **Golden set** | A curated set of inputs with expected outputs used for evaluation. |
| **Groundedness** | The degree to which an answer is supported by the supplied sources. |
| **Guardrail** | An automated check on AI inputs or outputs (for example injection detection, redaction). |
| **Hallucination** | AI output that is fluent but false or unsupported. |
| **Human in the loop** | A human reviews or approves AI output before it takes effect. |
| **Kill switch** | A control at the gateway that stops AI calls for a use case or model immediately. |
| **Landing zone** | The base cloud environment (network, identity, logging) into which the platform is deployed. |
| **Lighthouse use case** | An early, visible use case chosen to prove the platform and process. |
| **LLM (large language model)** | A foundation model that processes and generates text. |
| **LLM gateway** | The single service through which all model calls pass. See [ADR-AI-001](../02-architecture/adr/ADR-AI-001-llm-gateway.md). |
| **MCP (Model Context Protocol)** | An open protocol for connecting AI applications to tools and data sources. |
| **Model card** | A document describing a trained model's purpose, data, performance and limits. |
| **Non-human identity** | An identity (workload identity, service principal, service account) used by software, not a person. |
| **OpenTelemetry** | An open standard for traces, metrics and logs; has GenAI semantic conventions. |
| **Pattern** | A reusable solution design, such as RAG assistant or tool-using agent. |
| **Policy gate** | A CI check that validates the AI inventory against tiers and approved models. |
| **Prompt injection** | Input crafted to make a model ignore its instructions. Can be direct or hidden in content. |
| **Prompt registry** | A versioned store of production prompts with owners and linked evals. |
| **RACI** | Responsible, Accountable, Consulted, Informed: a responsibility matrix. |
| **RAG (retrieval-augmented generation)** | Retrieving relevant content and giving it to the model to ground its answer. |
| **Red teaming** | Adversarial testing to find ways to make a system misbehave. |
| **Risk tier** | Tier 1 (low), Tier 2 (medium), Tier 3 (high): sets controls and review depth. |
| **SLO (service level objective)** | A target for a measured service level, such as availability or groundedness. |
| **System card** | A document describing a whole AI system: purpose, components, data, oversight, evals. |
| **System of record** | The authoritative business system for a type of data. |
| **Threat model** | A structured analysis of how a system could be attacked and how to prevent it. |
| **Token** | A unit of text processed by a model; the usual basis for model pricing. |
| **Tool** | A function an agent can call, such as a lookup or an update. |
| **Vector index / vector store** | A store that searches embeddings by similarity. |
