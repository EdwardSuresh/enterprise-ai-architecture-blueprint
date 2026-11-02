# ADR-AI-002: Applications use model aliases, not provider model ids

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-15 |
| **Deciders** | Kit author (enterprise architecture), platform reviewers |
| **Use case id** | platform |
| **Risk tier** | Applies to all tiers |
| **Pattern** | All patterns |

## 5W1H

| | |
|---|---|
| **Who** | Application and agent developers; platform team that manages bindings |
| **What** | Code requests a capability alias such as `reasoning-large`, `reasoning-small` or `extraction`; the gateway maps it to an approved model |
| **When** | All new code; existing code migrates during plug-in rollout |
| **Where** | `config/models.yaml` holds bindings and fallbacks; `approved-models.yaml` holds allowed data classes per alias |
| **Why** | Provider model ids change often and differ per cloud; hard-coded ids spread change cost and hide which systems use which model |
| **How** | Platform owns the alias-to-model mapping; changing a binding follows the model version change runbook |

## Context

Model providers release and retire model versions frequently. Each cloud uses different identifiers for similar models. When application code names models directly, every upgrade or provider switch needs code changes in many places, and nobody can quickly answer "which systems use model X?". Vendors can also change behaviour behind a stable name, the "silent vendor update" anti-pattern.

## Options considered

| Option | Summary | Pros | Cons |
|---|---|---|---|
| A. Provider model ids in code | Each app names the exact model | Explicit | Change cost spread across apps; per-cloud code; no central view |
| B. Capability aliases resolved by the gateway | Apps name a capability; platform maps it | One place to change; fallbacks; per-alias data-class rules | Apps cannot pick a specific model without asking for a new alias |
| C. Per-application config files | Each app holds its own mapping | Flexible | Same drift problem as A, just in config |

## Decision

We will use **Option B**. Aliases describe a capability and a cost or quality band, not a vendor. A new alias needs platform and ARB approval. Bindings include a primary model and ordered fallbacks.

## AI-specific considerations

| Topic | Answer |
|---|---|
| Model aliases | Starter set: `reasoning-large`, `reasoning-small`, `extraction`. Add others (for example an embedding alias) through the approved list |
| Data class and hosting | Each alias lists allowed data classes; the policy gate checks inventory entries against it |
| Evaluation | Any change to a binding triggers the eval suites of every system using that alias |
| Cost | Price per alias is tagged for chargeback |
| Exit or portability | Moving cloud means changing bindings, not code |

## Consequences

- **Positive:** model upgrades become a controlled platform change; the inventory shows exactly which systems depend on which alias; multi-provider fallback is simple.
- **Negative:** teams wanting a specific new model must wait for alias approval.
- **Risks:** an alias rebinding could change behaviour for many systems at once. Mitigate with per-system eval runs, canary rollout, and the [model version change runbook](../../ops/runbooks/model-version-change.md).

## Compliance

Integration standard section 2; OWASP LLM03 (supply chain); ISO/IEC 42001 A.6 (life cycle); policy gate check on approved aliases.

## Review

Review when the alias set grows beyond about ten aliases, or yearly.
