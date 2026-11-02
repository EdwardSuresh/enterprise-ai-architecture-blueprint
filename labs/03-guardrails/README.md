# Lab 03: Guardrails

**Business case (Illustrative example):** A retailer runs a customer chat assistant. It must not capture card numbers, must resist prompt injection, must follow retail rules (refunds go to a human, no health claims), and must only say what the policy says.

| 5W1H | Answer |
|---|---|
| **Who** | Digital product owners, security, privacy, customer service leads, platform engineers |
| **What** | Input and output checks: PII redaction, prompt-injection check, sector rules, grounding check |
| **When** | On every turn of every customer-facing assistant. Add before any public launch |
| **Where** | `kit.guardrails` (`platform/core/kit/guardrails.py`), sector rules in `domain-packs/retail/guardrails.yaml` |
| **Why** | Customer-facing AI can leak data, be manipulated, or make promises the business must honor |
| **How** | Concept with regex and heuristics, Build with managed safety services, Production with red-team tests and CI |

## Concept (plain Python, no cloud)

From the repo root:

```bash
pip install -e .
python labs/03-guardrails/concept.py
```

What it shows:

1. **PII redaction.** Card numbers and emails are replaced with tokens before the text reaches a model or a log.
2. **Prompt-injection check.** "Ignore all previous instructions..." is blocked.
3. **Sector guardrails.** Rules load from `domain-packs/retail/guardrails.yaml`. `block_topic` rules stop the turn. `require_human` rules hand off to an agent.
4. **Grounding check.** A draft answer is scored against the source context. Answers with words not found in the source are blocked.

Try this: add a rule to `domain-packs/retail/guardrails.yaml`, rerun, and check that `pytest -q` still passes.

## Build on Azure (reference implementation)

1. Create `rg-aikit-lab03` and a budget alert.
2. Create **Azure AI Content Safety** on the **F0 (free) tier**.
3. Call **Prompt Shields** on the user input and on retrieved documents (to catch indirect injection).
4. Call text moderation on input and output. Set category thresholds for your use case.
5. Use groundedness detection (if available in your region) or keep the blueprint's grounding check on outputs.
6. Configure content filters on your **Microsoft Foundry** model deployment. Note what they block by default.
7. Keep `kit.guardrails` in the flow for PII redaction and sector rules. Managed services and blueprint rules work together; neither covers everything.
8. Run the Concept test inputs plus the prompts in `security/red-team/prompts.jsonl` through the full chain.

## Build on AWS (short)

- Use **Amazon Bedrock Guardrails**: denied topics, content filters, prompt attack filter, sensitive information filters (PII masking) and contextual grounding checks.
- Apply the guardrail on model calls, or call it on its own for text from other sources.

## Build on Google Cloud (short)

- Use **Model Armor** to screen prompts and responses for prompt injection, jailbreaks, sensitive data and harmful content.
- Use Sensitive Data Protection for PII detection, and Vertex AI safety settings on the model.

Service names and features change. Check the current docs for each provider.

## Production

1. Document which risks each layer covers. Map them in `01-governance/control-maps/owasp-llm-top10.md`.
2. Grow the red-team set in `security/red-team/prompts.jsonl`. Record the catch rate per release.
3. Make sure logs and traces store only redacted text. See `02-architecture/standards/logging-standard.md`.
4. Add a customer-facing AI disclosure and a clear path to a human.
5. **CI gates:** `.github/workflows/ci.yml` runs the guardrail tests, the pack structure tests and the red-team catch rate test. `.github/workflows/evals.yml` checks that guardrails do not break normal answers on the retail golden set.
6. Evidence to keep: guardrail config history, red-team reports, content filter settings, sample of blocked turns (redacted).

## Exit criteria

- [ ] Card numbers never appear in prompts, logs or traces.
- [ ] Known injection prompts are blocked.
- [ ] Refund and complaint requests hand off to a human.
- [ ] Ungrounded answers are blocked.
- [ ] A managed safety service is in the flow on one cloud.
- [ ] Red-team catch rate is recorded and meets the CI threshold.

## Cleanup

```bash
az group delete -n rg-aikit-lab03 --yes --no-wait
```

On AWS, delete the guardrail. On Google Cloud, delete the Model Armor templates you created.

**Maps to:** `platform/core/kit/guardrails.py`, `domain-packs/retail/guardrails.yaml`, `security/red-team/`, `01-governance/control-maps/owasp-llm-top10.md`, `01-governance/policies/acceptable-use.md`, `02-architecture/patterns/conversational-customer-agent.md`.
