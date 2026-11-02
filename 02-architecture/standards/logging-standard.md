# AI Logging Standard

| 5W1H | Answer |
|---|---|
| **Who** | Platform team (gateway logs), delivery teams (app and agent logs), security (monitoring), risk and audit (consumers) |
| **What** | What AI systems log, where, how long, and what must never be logged |
| **When** | From the first environment that handles real data |
| **Where** | Central observability platform and the gateway log store |
| **Why** | Logs explain decisions, detect misuse, attribute cost and support audits and regulator requests |
| **How** | OpenTelemetry traces plus structured gateway logs; content capture depends on tier and data class |

## 1. Always log (metadata)

| Field | Example | Source |
|---|---|---|
| `timestamp` | ISO 8601 UTC | All |
| `trace_id`, `span_id` | | All |
| `kit.use_case_id` | UC-002 | Gateway |
| `kit.system_id` | AIS-114 | Gateway |
| `kit.risk_tier` | 2 | Gateway |
| `user.pseudonymous_id` | Hash of user id | App |
| `kit.model_alias` and `gen_ai.request.model` | reasoning-small / provider model id | Gateway |
| `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens` | | Gateway |
| `kit.cost_usd` | | Gateway |
| `latency_ms` | | Gateway |
| `kit.guardrail.decision` | allow / block / redact, with rule id | Control plane |
| `kit.retrieval.sources` | Document ids returned (not content) | Retrieval |
| `kit.tool.name`, `kit.tool.outcome` | | Agent runtime |
| `kit.approval.id`, `kit.approval.approver`, `kit.approval.outcome` | | Approval queue |
| `kit.human.override` | true/false | App |
| `prompt.id`, `prompt.version` | | Control plane |

## 2. Content capture (prompts and responses)

| Tier | Data class internal or lower | Confidential | Restricted |
|---|---|---|---|
| Tier 1 | Sampled, redacted | Off by default | Off |
| Tier 2 | Full, redacted | Full, redacted, restricted access | Off unless ARB approves |
| Tier 3 | Full, redacted | Full, redacted, restricted access | Full in a restricted store if ARB and privacy approve |

- Redaction removes personal identifiers and payment data before storage.
- Access to content logs is role-based and itself logged.

## 3. Never log

- Secrets, credentials, API keys, tokens.
- Full payment card numbers or national identifiers.
- Content of restricted data outside an approved restricted store.

## 4. Retention

| Log type | Default retention |
|---|---|
| Metadata and traces | 13 months (to cover a full year plus review) |
| Content logs | Shortest of: data class retention ([classification.yaml](../../data/classification.yaml)), legal requirement, 90 days default |
| Approval and override records | Same as the business record they relate to |
| Incident evidence | Kept with the incident record |

Adjust to your legal and regulatory requirements.

## 5. Integrity

- Logs for Tier 2 and Tier 3 systems **must** be write-once or tamper-evident.
- Time sources **must** be synchronized.

## 6. Use of logs

- Monitoring: SLOs, guardrail block rates, cost, override rates.
- Investigation: AI incidents, complaints, contested decisions.
- Improvement: logs feed new golden cases (after redaction and review).
- Logs **must not** be used to train models without privacy review.
