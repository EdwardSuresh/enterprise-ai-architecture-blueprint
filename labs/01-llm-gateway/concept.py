"""Lab 01 Concept: LLM gateway (business case: a bank routes every model call).

Shows: model aliases, automatic fallback, cost tags per use case, budgets, kill switch.
Run from the repo root:  python labs/01-llm-gateway/concept.py
"""
from kit.gateway import BudgetExceeded, Gateway, KillSwitchActive, MockProvider

primary, secondary = MockProvider("mock-primary"), MockProvider("mock-secondary")
gw = Gateway.from_config({"mock-primary": primary, "mock-secondary": secondary},
                         budgets_usd={"fee-dispute": 0.0005})

prompt = "CONTEXT:\nMonthly maintenance fee is $12. It is waived with a $1,500 balance.\nQUESTION: When is the fee waived?"

print("1) Normal call through alias 'reasoning-large'")
out = gw.complete("reasoning-large", prompt, use_case="branch-faq")
print(f"   {out.provider}/{out.model} -> {out.text!r}  cost=${out.cost_usd}")

print("\n2) Primary provider has an outage -> gateway falls back")
primary.fail = True
out = gw.complete("reasoning-large", prompt, use_case="branch-faq")
print(f"   served by {out.provider}/{out.model}")
primary.fail = False

print("\n3) Budget per use case")
try:
    for i in range(10):
        gw.complete("reasoning-large", prompt, use_case="fee-dispute")
except BudgetExceeded as e:
    print(f"   stopped after {i} calls: {e}")

print("\n4) Kill switch during an incident")
gw.kill("branch-faq")
try:
    gw.complete("reasoning-large", prompt, use_case="branch-faq")
except KillSwitchActive as e:
    print(f"   blocked: {e}")

print("\nSpend by use case:", {k: round(v, 6) for k, v in gw.spend_usd.items()})
print("Trace spans recorded:", len(gw.tracer.spans))
