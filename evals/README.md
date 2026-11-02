# Evals

| | |
|---|---|
| **What** | Golden-set quality evals and red-team safety checks |
| **Why** | Stops the "eval-free release" anti-pattern: no change ships on "looks good to me" |
| **Who** | Delivery team writes cases with front-line experts; QA owns thresholds |
| **When** | Every pull request (`.github/workflows/evals.yml`) and before each model or prompt version change |
| **Where** | Golden sets live with each domain pack: `domain-packs/<pack>/evals/golden.jsonl`. Suites: `evals/suites/` |
| **How** | `kit-evals --suite evals/suites/quality.yaml` |

Golden line format:
```json
{"id": "INS-001", "input": "question", "context": "source text", "expected_keywords": ["..."], "forbidden": ["..."]}
```
CI runs the offline extractive mock model so results are deterministic. In Build labs, swap `answer_fn` for your real orchestrator and add model-graded metrics (groundedness, relevance) from Foundry evaluations, Bedrock evaluations or Vertex AI evaluation.

`datasets/` holds shared datasets; `reports/` receives exported results.
