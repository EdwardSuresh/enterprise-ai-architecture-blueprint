# Human Oversight Policy (Template)

| 5W1H | Answer |
|---|---|
| **Who** | System owners, delivery teams, reviewers who act as the human in the loop |
| **What** | When a human must review, approve or be able to override AI, and how to make that review real |
| **When** | Designed before build; tested before release; monitored in production |
| **Where** | Every AI system with an autonomy level above L0 or a risk tier above Tier 1 |
| **Why** | Human review only works if reviewers have the time, information and authority to disagree |
| **How** | Autonomy level is capped by risk tier; oversight design is reviewed at the ARB; override rates are monitored |

**Policy owner:** <Chief risk officer>  **Version:** 1.0

## 1. Autonomy levels

1.1 Every AI system declares an autonomy level from [autonomy-levels.md](../../ops/autonomy-levels.md): L0 Suggest, L1 Draft, L2 Act with approval, L3 Act within limits, L4 Autonomous.
1.2 Maximum autonomy by tier: Tier 1 up to L4 with ARB approval; Tier 2 up to L3; Tier 3 up to L2.

## 2. Material decisions

2.1 AI must not make a final decision that materially affects an individual without a qualified human approving it.
2.2 The human must be able to see the inputs, the AI recommendation, the reasons or sources, and the confidence where available.

## 3. Meaningful review

3.1 Reviewers must have the authority to reject or change the AI output without penalty.
3.2 Review workload must allow real review. The system owner sets a target review time and monitors it.
3.3 Reviewers are trained on the system's known limits and failure modes.
3.4 Interfaces must not pre-select "approve" or hide the evidence.

## 4. Monitoring the human in the loop

4.1 The system logs approvals, overrides and time-to-decision.
4.2 An override rate near zero over a long period is a warning sign of rubber-stamping and triggers a sample review.
4.3 Sample a share of approved items for second review, as set in the ARB decision.

## 5. Fallback

5.1 Every AI system has a human fallback path that works when the AI is switched off.
5.2 The kill switch at the LLM gateway routes work to the human queue (see [AI incident runbook](../../ops/runbooks/ai-incident.md)).

## 6. Contest and redress

6.1 Individuals affected by an AI-supported decision can ask for human review through <channel>.
6.2 Contest requests and outcomes are logged and reported to the ARB quarterly for Tier 3 systems.

## 7. Agents

7.1 Agents act only through tools on an allow-list, with scopes defined in [agent-scopes.yaml](../../security/identity/agent-scopes.yaml).
7.2 Actions that move money, change records of entitlement, send external communications or delete data need approval at L2 unless the ARB has approved limits at L3.

## 8. Review

8.1 Oversight design is part of the ARB [review checklist](../arb/review-checklist.md).
