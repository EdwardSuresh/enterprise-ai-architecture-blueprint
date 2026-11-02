# AI Cost Model

| 5W1H | Answer |
|---|---|
| **Who** | FinOps lead, platform team, use-case owners, architects estimating new use cases |
| **What** | How to calculate cost per transaction, tag spend, charge it back and reduce it |
| **When** | Estimate at intake; measure from pilot; review monthly in production |
| **Where** | Gateway logs and cloud billing |
| **Why** | Cost must be known per use case to judge value and stop waste |
| **How** | Formula below; tags on every call; chargeback by use case; optimization levers |

## 1. Cost per transaction

A *transaction* is the business unit of work: one answer, one document, one case, one conversation.

```
cost_per_transaction =
    Σ over model calls in the transaction:
        (input_tokens  / 1000 × price_in_per_1k)
      + (output_tokens / 1000 × price_out_per_1k)
  + retrieval_cost          (search queries, embedding of the query)
  + tool_cost               (API calls with a charge)
  + guardrail_cost          (content-safety calls if billed separately)
  + allocated_platform_cost (shared gateway, observability, vector store ÷ transactions)
  + human_review_cost       (minutes reviewed × loaded cost per minute, if you want total cost of the process)
```

Prices per alias come from `config/models.yaml`. Use your contract prices, not list prices.

### Estimating before build

| Input | How to estimate |
|---|---|
| Calls per transaction | Count steps in the pattern (RAG: 1–2; agent: 3–10) |
| Input tokens per call | System prompt + retrieved passages + user input + history |
| Output tokens per call | Expected answer length |
| Volume | Transactions per month from the business case |

Run the [labs](../labs/) or a pilot to replace estimates with measured numbers as soon as possible.

## 2. Tagging

Every gateway call **must** carry these tags. Cloud resources carry the same tags where possible.

| Tag | Example |
|---|---|
| `use_case_id` | UC-002 |
| `system_id` | AIS-114 |
| `cost_centre` | CC-CLM |
| `environment` | dev / test / prod |
| `model_alias` | extraction |
| `owner` | role or team |

Untagged spend is reported weekly and assigned to the platform cost centre until fixed.

## 3. Chargeback and showback

| Stage | Approach |
|---|---|
| Early (maturity 1–2) | Showback only: publish cost by use case; platform centrally funded |
| Growing (maturity 3) | Chargeback of direct model and tool costs; platform shared cost still central |
| Mature (4–5) | Full chargeback including allocated platform cost by token share or transaction share |

## 4. Reducing cost

| Lever | What it means | Typical fit |
|---|---|---|
| **Model right-sizing** | Use `reasoning-small` or `extraction` unless evals show `reasoning-large` is needed | Most classification, extraction, short answers |
| **Routing** | Small model first; escalate to a larger one only when confidence is low | Mixed-difficulty workloads |
| **Prompt trimming** | Shorter system prompts; fewer, better retrieved passages | RAG |
| **Caching** | Cache responses to identical or near-identical requests; use provider prompt caching for long fixed prefixes | FAQ-style traffic, long system prompts |
| **Batching** | Use batch or asynchronous APIs for non-urgent work, often at lower price | Overnight document processing |
| **Output limits** | Set `max_tokens`; ask for structured output | All |
| **Step limits** | Cap agent steps and retries | Agents |
| **Stop waste** | Retire unused use cases; remove idle provisioned capacity | Whole estate |

Every optimization must be followed by an eval run. Saving money by lowering quality is a business decision, not a FinOps default.

## 5. Caching rules

- Never cache answers that depend on user permissions across users. Cache keys must include the permission scope.
- Cache time-to-live must not exceed the source data freshness target.
- Do not cache responses containing confidential or restricted data unless the cache meets the same class controls.

## Illustrative example

*Illustrative example (composite).* A logistics firm found that its exception-handling agent sent the full shipment history on every step. Trimming to the last ten events and routing first-pass classification to a small model cut cost per case markedly with no drop in eval scores.
