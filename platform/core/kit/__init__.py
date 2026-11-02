"""The Architect's Enterprise AI Kit - cloud-neutral core.

Modules
-------
config       find the repo root and load YAML config
tracing      lightweight spans using OpenTelemetry GenAI attribute names
gateway      LLM gateway: model aliases, fallback, cost tags, budgets, kill switch
guardrails   PII redaction, prompt-injection check, sector rules, grounding check
retrieval    permission-aware retrieval with citations (pure Python TF-IDF)
tools        tool registry, agent identities, allow-lists, human approval queue
prompts      versioned prompt registry (prompts/registry.yaml)
memory       short-term and long-term memory with retention rules
orchestrator one guarded request end to end
evals        golden-set evaluation runner (CLI: kit-evals)
policy_gate  AI inventory validator for CI (CLI: kit-policy-gate)

Everything here runs with only PyYAML installed. Cloud SDKs live in kit_adapters.
"""

__version__ = "1.0.1"
