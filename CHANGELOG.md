# Changelog

All notable changes to the kit. Versions follow semantic versioning: a major
version changes the governance schemas (`ai-inventory.yaml`, `risk-tiers.yaml`).

## [1.0.0] - 2026-11-01
### Added
- Governance spine: charter, RACI, risk tiers, AI inventory, AI ARB, policies, templates.
- Control maps: NIST AI RMF 1.0 (category level), ISO/IEC 42001 Annex A areas, EU AI Act, OWASP Top 10 for LLM Applications 2025.
- Reference architecture, 10 patterns, which-pattern-when, standards, ADRs.
- Runnable `kit` package: LLM gateway (aliases, fallback, cost tags, budgets, kill switch), guardrails, permission-aware retrieval, tool registry with approval queue, orchestrator, tracing, evals runner, policy gate.
- Cloud adapters for Microsoft Foundry / Azure OpenAI, Amazon Bedrock, Google Vertex AI and the Claude API (reference, not run in CI).
- 10 domain packs plus a template; six-step industry overlay method.
- 18 labs (6 building blocks × Concept / Build / Production).
- CI: tests, evals gate, policy gate, website publishing.
- Website with maturity check, pattern ranking, anti-patterns and templates.

### Next review
- 2027-02-01: refresh cloud service names, OWASP list and regulatory references.
