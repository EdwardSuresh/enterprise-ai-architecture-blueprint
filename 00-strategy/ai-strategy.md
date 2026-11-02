# AI Strategy Template

Copy this file, replace the guidance text in each section, and keep it short. A strategy that people do not read does not steer anything. Aim for five pages or fewer.

| 5W1H | Answer |
|---|---|
| **Who** | Written by the chief AI officer or head of EA with the CIO; approved by the executive committee |
| **What** | The organization's direction for AI: goals, priorities, guardrails, operating model, funding |
| **When** | Drafted in the first two weeks of the program; reviewed every quarter; rewritten yearly |
| **Where** | This repo (versioned) plus the executive committee pack |
| **Why** | Gives teams one answer to "what AI work do we fund, and under what rules?" |
| **How** | Fill each section below. Link to the capability map, portfolio and governance charter |

---

## 1. Vision (2–3 sentences)

> Guidance: State what AI should change for customers, staff and the business in three years. Avoid technology words. Example shape: "Our staff spend their time on judgment, not searching. Customers get accurate answers in minutes. Every AI system we run is known, owned and controlled."

## 2. Business drivers

> Guidance: List the three to five business pressures AI must answer. Link each to an existing corporate goal.

| Driver | Corporate goal it supports | How we will know it improved |
|---|---|---|
| | | |

## 3. Strategic priorities (pick three, no more than five)

> Guidance: A priority is a theme, not a project. For example: "Knowledge work productivity", "Faster claims or case handling", "Safer operations". Each priority maps to rows in the [capability map](capability-map.md).

| # | Priority | Capabilities affected | Executive owner |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## 4. Guardrails (what we will not do)

> Guidance: Write plain rules. These feed the [acceptable-use policy](../01-governance/policies/acceptable-use.md).

- We will not use AI for prohibited purposes under applicable law.
- We will not let AI make final decisions that materially affect a person without human review (Tier 3, autonomy L2 maximum).
- We will not send restricted data to model endpoints that do not meet the [data classification](../data/classification.yaml) hosting rule.
- We will not put an AI system into production unless it is in the AI inventory with a named owner.

## 5. Operating model

> Guidance: Choose one and explain why. Most organizations start centralized and move to hub-and-spoke.

| Model | Description | Fits when |
|---|---|---|
| Centralized | One AI team builds and runs everything | Early maturity, few use cases |
| Hub-and-spoke | Central platform, standards and ARB; business units build on it | Growing demand, several delivery teams |
| Federated | Business units own AI with central guardrails only | High maturity, strong local architecture |

Chosen model: ______  Reason: ______

## 6. Platform position

> Guidance: State the cloud and model posture in one paragraph. The kit's default is: one shared AI platform, all model calls through an LLM gateway, more than one model provider approved, model access by alias. See [reference architecture](../02-architecture/reference-architecture.md).

## 7. Governance

> Guidance: Point to the [charter](../01-governance/charter.md), the ARB and the risk tiers. Say who can stop an AI system.

## 8. People and change

> Guidance: Link to [learning paths](../enablement/learning-paths.md) and the [workforce impact assessment](../enablement/workforce-impact-assessment.md). Say how staff will be told about AI use that affects their roles.

## 9. Funding and value

> Guidance: State the funding model (central fund, business-unit funded, or mixed) and how value is tracked using the [value scorecard](value-scorecard.md) and [FinOps](../finops/README.md).

| Item | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| Platform run cost | | | |
| Use-case delivery | | | |
| Enablement | | | |
| Expected value (from scorecards) | | | |

## 10. Roadmap

> Guidance: Four quarters, three lines. Keep detail in the portfolio.

| Quarter | Platform and governance | Use cases | People |
|---|---|---|---|
| Q1 | | | |
| Q2 | | | |
| Q3 | | | |
| Q4 | | | |

## 11. Measures of success

> Guidance: Mix value, adoption, risk and maturity. Target maturity uses the [maturity model](../docs/maturity-model.md).

| Measure | Baseline | Target | Owner |
|---|---|---|---|
| Use cases in production with measured value | | | |
| AI systems in inventory with named owner | | | |
| Current maturity level (average across 8 dimensions) | | | |
| Staff who completed AI literacy | | | |

## 12. Approval

| Role | Name | Date |
|---|---|---|
| Chief executive or delegate | | |
| CIO | | |
| Chief AI officer | | |
| Chief risk officer | | |

---

## Illustrative example

*Illustrative example (composite, not a client case study).* A regional insurer wrote a three-page strategy. Its three priorities were claims handling speed, underwriter productivity and customer self-service. Its guardrails banned fully automated claim denials. It chose hub-and-spoke with one shared platform. The strategy fit on one slide for the board and linked to twelve rows in the portfolio.
