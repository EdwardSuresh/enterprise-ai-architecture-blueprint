# Changelog

All notable changes to the kit. Versions follow semantic versioning: a major
version changes the governance schemas (`ai-inventory.yaml`, `risk-tiers.yaml`).

## [1.0.1] - 2026-11-01
### Changed (name)
- Renamed from "The Architect's Enterprise AI Kit" to **Enterprise AI Architecture Blueprint** (part of The Architect's Series), to reflect enterprise-wide, industry-neutral use. Repository: `enterprise-ai-architecture-blueprint`. The reference code package keeps the name `kit`.

### Added
- Prompt registry: `prompts/registry.yaml`, versioned prompt library, `kit.prompts` (approved-only loading, required variables, content hash in traces, registry validation).
- Conversation memory: `kit.memory` with short-term memory per conversation (turn limit, idle expiry) and long-term facts per user (allowed keys, retention, export, forget); PII redacted before storing.
- Orchestrator uses the registry prompt and conversation memory; responses carry the prompt reference.
- Policy gate checks that prompts listed in the AI inventory exist and are approved.
- Acknowledgements file; disclaimer note on how the blueprint was built.
### Changed
- Lab 02 demonstrates the prompt registry and memory. Test suite: 74 tests.

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
