# Data Use for AI Policy (Template)

| 5W1H | Answer |
|---|---|
| **Who** | Data owners, AI builders, platform team, privacy and security |
| **What** | Rules for which data may be used with AI, where it may be processed and how long it is kept |
| **When** | Applies at design, build, run and retirement of every AI system |
| **Where** | All model endpoints, vector stores, prompt logs, evaluation sets and training data |
| **Why** | AI systems copy data into new places (indexes, logs, prompts). Each copy needs the same protection as the source |
| **How** | Data class drives hosting; data contracts record ownership and quality; the gateway enforces endpoint rules |

**Policy owner:** <Chief data officer>  **Version:** 1.0

## 1. Classification

1.1 All data used by an AI system must have a class from [classification.yaml](../../data/classification.yaml): public, internal, confidential or restricted.
1.2 Derived data (embeddings, chunks, summaries, logs) inherits the highest class of its sources.

## 2. Hosting

2.1 Data may be sent only to model endpoints allowed for its class (`allowed_model_hosting` in the classification file).
2.2 Restricted data requires a private endpoint in an approved region, with no provider retention and no use for provider training.
2.3 The LLM gateway enforces endpoint rules. Direct calls to model providers are not allowed.

## 3. Purpose limitation

3.1 Personal data may be used only for the purpose recorded in the AI inventory entry.
3.2 Using existing data to train or fine-tune a model is a new purpose and needs privacy review.

## 4. Access control

4.1 Retrieval systems must enforce the source system's permissions for the requesting user (no permission-blind RAG).
4.2 The ACL source is recorded in the [data contract](../../data/contracts/README.md).

## 5. Minimization

5.1 Send the minimum data needed. Redact or mask identifiers where the task does not need them.
5.2 Do not index whole repositories "just in case".

## 6. Quality and lineage

6.1 Data feeding AI in production must have a data contract with an owner, freshness target and quality rules.
6.2 Lineage from source to index to answer must be traceable (see [lineage](../../data/lineage/README.md)).

## 7. Logs and retention

7.1 Prompt and response logs follow the [logging standard](../../02-architecture/standards/logging-standard.md).
7.2 Logs containing confidential or restricted data are retained no longer than the class retention period.
7.3 Vector indexes and caches are deleted when the source data is deleted or the system retires.

## 8. Provider terms

8.1 Provider contracts must state that prompts and outputs are not used to train provider models, unless approved by the ARB.
8.2 Provider data retention must be recorded in the vendor questionnaire.

## 9. Individual rights

9.1 AI systems must support data subject requests (access, deletion, correction) where law requires, including in indexes and logs.

## 10. Exceptions

10.1 Exceptions require written approval from the data owner and privacy lead, recorded in the ARB decision log with an expiry date.
