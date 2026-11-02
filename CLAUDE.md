# Conventions for AI coding assistants

- Agents call models only through `kit.gateway.Gateway` using aliases from `config/models.yaml`. Never import a cloud SDK outside `platform/adapters/`.
- Business rules belong in the orchestrator or tools, not in prompt text.
- Write tools must go through the approval queue (`kit.tools.ToolRegistry`); never call system-of-record writes directly.
- Retrieval must pass the caller's groups; never search without an access filter.
- Any new AI system needs an entry in `01-governance/ai-inventory.yaml` and a system card; run `kit-policy-gate`.
- Add or update golden cases when behaviour changes; run `kit-evals --suite evals/suites/quality.yaml`.
- Run `pytest -q` before finishing.
- Label any organization example "Illustrative example".
