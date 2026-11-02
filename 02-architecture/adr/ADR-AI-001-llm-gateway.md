# ADR-AI-001: All model calls go through an enterprise LLM gateway

| Field | Value |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-15 |
| **Deciders** | Blueprint author (enterprise architecture), platform reviewers |
| **Use case id** | platform |
| **Risk tier** | Applies to all tiers |
| **Pattern** | All patterns |

## 5W1H

| | |
|---|---|
| **Who** | Every application, agent and batch job that calls a generative or embedding model |
| **What** | A single gateway in front of all model providers |
| **When** | Effective from the first production use case; existing direct calls migrate during plug-in rollout |
| **Where** | Layer 5 of the reference architecture, in every cloud and environment |
| **Why** | Without one control point, quotas, logging, data-class routing, cost attribution and the kill switch must be rebuilt in every app |
| **How** | Gateway exposes one API; provider adapters translate to each cloud; apps pass alias and `use_case_id` |

## Context

Teams adopting AI tend to call model providers directly, each with its own SDK, keys, logging and retry logic. This makes it hard to answer basic questions: how many AI systems call models, which data goes where, what each use case costs, and how to stop one quickly. Model providers and model versions also change often, and each change ripples into every application.

## Options considered

| Option | Summary | Pros | Cons |
|---|---|---|---|
| A. Direct provider calls with shared libraries | Each app uses a common client library | Low latency, simple | Controls depend on every team updating the library; no central kill switch; keys spread |
| B. Enterprise LLM gateway | One service fronts all providers | Single control point; central logging, quotas, routing, kill switch; easy provider change | Extra hop; gateway becomes critical infrastructure |
| C. Rely on each cloud's native controls only | Use provider-native policies per cloud | No build effort | Different controls per cloud; no cross-cloud view; harder for multi-provider |

## Decision

We will use **Option B**. All model calls go through an enterprise LLM gateway. The gateway may be built on a managed API gateway product with AI policies, or as a thin service, as long as it meets the integration standard.

## AI-specific considerations

| Topic | Answer |
|---|---|
| Model aliases | Gateway resolves aliases (see ADR-AI-002) |
| Data class and hosting | Gateway refuses to route data to an alias not approved for its class |
| Guardrails | Gateway hosts shared content-safety checks; use-case guardrails stay in the control plane |
| Human oversight and fallback | Kill switch per use case and per alias, routing work to the human queue |
| Evaluation | Gateway logs feed evaluation and monitoring |
| Cost | Gateway tags every call with `use_case_id` and enforces budgets |
| Exit or portability | Provider adapters isolate cloud-specific code |

## Consequences

- **Positive:** one place to enforce policy and observe usage; provider changes do not touch apps; kill switch works everywhere.
- **Negative:** added latency (normally small compared with model latency); the gateway must be highly available and properly scaled.
- **Risks and how we watch them:** gateway outage stops all AI. Mitigate with multi-zone deployment, provider fallbacks, SLOs in `ops/slo.yaml`, and the human fallback path.

## Compliance

Integration standard sections 1 and 5; OWASP LLM10 (unbounded consumption); logging standard; NIST AI RMF MANAGE 2 (ability to disengage).

## Review

Review when a cloud provider offers equivalent cross-provider controls natively, or yearly.
