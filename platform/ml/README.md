# platform/ml: classic and deep machine learning

| | |
|---|---|
| **What** | Feature pipelines, training, model registry, serving and explainability for predictive models |
| **Why** | Fraud scores, reserves, demand forecasts and failure risk are tabular problems. GenAI explains the result; a classic model produces it |
| **Who** | Data science and ML engineering, governed by the same ARB and inventory as GenAI |
| **Where** | `features/`, `training/`, `registry/`, `serving/`, `explainability/` |
| **How** | Pick the algorithm with [The Architect's ML Playbook](https://edwardsuresh.github.io/architects-ml-playbook/) (30 algorithms, Concept/Build/Production labs), then register it here with a model card (`01-governance/templates/model-card.yaml`) |

Pattern: `02-architecture/patterns/classic-ml-with-genai-explanation.md`.
Every model gets an inventory entry, a risk tier, drift monitoring and a retirement trigger, exactly like an agent.
