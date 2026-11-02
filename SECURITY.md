# Security policy

This repository is a reference kit. It ships with an offline mock model and no
credentials.

- **Never commit secrets.** Use `.env` (ignored) based on `.env.example`, and a secrets manager in real deployments.
- **Reporting a vulnerability:** please use GitHub's private vulnerability reporting on this repository (Security tab → Report a vulnerability) rather than a public issue.
- The heuristic guardrails in `platform/core/kit/guardrails.py` are teaching references. Pair them with a managed service (Azure AI Content Safety and Prompt Shields, Amazon Bedrock Guardrails, Google Model Armor) in production.
