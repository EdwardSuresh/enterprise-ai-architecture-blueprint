# Lab 05: Golden-Set Evals

**Business case (Illustrative example):** An oil and gas operator summarizes daily drilling reports for managers. A summary that drops a pit gain or an HSE event is a serious failure. Every change to the prompt, model or retrieval must pass a golden set before release.

| 5W1H | Answer |
|---|---|
| **Who** | Drilling engineers (write golden examples), product owner, platform engineers, model risk or AI risk reviewers |
| **What** | A golden-set evaluation runner with a pass threshold that gates releases |
| **When** | Before go-live and on every change to prompts, models, retrieval or guardrails |
| **Where** | `kit.evals` (`platform/core/kit/evals.py`), golden set in `domain-packs/oil-and-gas/evals/golden.jsonl`, suites in `evals/suites/` |
| **Why** | Without a fixed test set, quality drifts and nobody can show the system still works after a change |
| **How** | Concept with a mock answerer, Build with a managed evaluation service, Production with a CI gate and stored reports |

## Concept (plain Python, no cloud)

From the repo root:

```bash
pip install -e .
python labs/05-evals/concept.py
```

What it shows:

1. **Golden-set runner.** Loads `domain-packs/oil-and-gas/evals/golden.jsonl`. Each line has `input`, `context`, `expected_keywords` and `forbidden`.
2. **Pass rule.** A case passes when every expected keyword is in the answer and no forbidden phrase is.
3. **Pass threshold.** The baseline system passes. A simulated bad change (answering from the first sentence only) fails, and the runner lists what is missing.

You can also run the CLI:

```bash
kit-evals domain-packs/oil-and-gas/evals/golden.jsonl --threshold 0.9
kit-evals --suite evals/suites/quality.yaml
```

Try this: add a case for a new event type (for example a lost circulation event) and rerun.

## Build on Azure (reference implementation)

1. Create `rg-aikit-lab05` and a budget alert.
2. Upload the golden set as a dataset in your **Microsoft Foundry** project.
3. Run a **Foundry evaluation** against your model deployment. Use built-in quality evaluators (for example groundedness, relevance) and a custom evaluator that checks expected keywords and forbidden phrases.
4. Compare two runs: the current prompt and a changed prompt. Look at per-case results, not just the average.
5. Use a small model as the judge where possible and keep the dataset small. Judge-based evaluators cost tokens on every case.
6. Export results to `evals/reports/` (redacted) for review.

## Build on AWS (short)

- Use **Amazon Bedrock evaluations** (model evaluation or RAG evaluation jobs) with your dataset in S3.
- Add the blueprint's keyword check as a custom metric or run `kit-evals` against Bedrock outputs.

## Build on Google Cloud (short)

- Use the **Vertex AI evaluation** service (Gen AI evaluation) with pointwise metrics and custom metrics.
- Store the dataset in Cloud Storage and save results to BigQuery or a report file.

Service names and features change. Check the current docs for each provider.

## Production

1. Grow the golden set to 100-300 cases written or checked by drilling engineers. Over-sample safety-critical events.
2. Agree the threshold with the business owner and the AI risk team. Record it in `evals/suites/quality.yaml`.
3. Add the golden set path to the system's entry in `01-governance/ai-inventory.yaml` (`golden_set`). The policy gate checks it is present for the tier.
4. Add red-team prompts to `security/red-team/prompts.jsonl` and run `kit-evals --suite evals/suites/safety.yaml`.
5. **CI gates:** `.github/workflows/evals.yml` runs `kit-evals --suite evals/suites/quality.yaml` and fails the pull request below threshold. `.github/workflows/policy-gate.yml` fails if a Tier 2 or 3 system has no golden set.
6. Evidence to keep: dated eval reports, threshold decisions, who wrote and reviewed the golden cases.

## Exit criteria

- [ ] I can explain the pass rule and the threshold.
- [ ] The Concept lab shows a passing baseline and a failing regression.
- [ ] One cloud evaluation run compares two versions case by case.
- [ ] The quality suite gates pull requests in `evals.yml`.
- [ ] The inventory entry points to the golden set.

## Cleanup

```bash
az group delete -n rg-aikit-lab05 --yes --no-wait
```

On AWS, delete evaluation jobs' S3 outputs if not needed. On Google Cloud, delete datasets and result tables you created.

**Maps to:** `platform/core/kit/evals.py`, `evals/suites/quality.yaml`, `evals/suites/safety.yaml`, `evals/reports/`, `domain-packs/oil-and-gas/evals/golden.jsonl`, `domain-packs/oil-and-gas/use-cases/daily-drilling-report-summary/spec.md`, `01-governance/ai-inventory.yaml`.
