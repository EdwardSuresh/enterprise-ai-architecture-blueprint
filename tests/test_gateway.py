import pytest

from kit.gateway import BudgetExceeded, Gateway, KillSwitchActive, MockProvider, ProviderError

P = "CONTEXT:\nThe fee is waived with a $1,500 balance.\nQUESTION: When is the fee waived?"


def gw(**kw):
    a, b = MockProvider("mock-primary"), MockProvider("mock-secondary")
    return Gateway.from_config({"mock-primary": a, "mock-secondary": b}, **kw), a, b


def test_alias_routes_to_primary_and_tags_cost():
    g, a, _ = gw()
    out = g.complete("reasoning-large", P, use_case="uc1")
    assert out.provider == "mock-primary" and out.cost_usd > 0
    assert "waived" in out.text
    assert g.spend_usd["uc1"] == pytest.approx(out.cost_usd)


def test_fallback_on_outage():
    g, a, _ = gw()
    a.fail = True
    out = g.complete("reasoning-large", P, use_case="uc1")
    assert out.provider == "mock-secondary"


def test_all_routes_fail():
    g, a, b = gw()
    a.fail = b.fail = True
    with pytest.raises(ProviderError):
        g.complete("reasoning-large", P, use_case="uc1")


def test_unknown_alias():
    g, *_ = gw()
    with pytest.raises(KeyError):
        g.complete("gpt-whatever", P, use_case="uc1")


def test_budget_and_kill_switch():
    g, *_ = gw(budgets_usd={"uc2": 0.0})
    with pytest.raises(BudgetExceeded):
        g.complete("reasoning-large", P, use_case="uc2")
    g.kill("reasoning-large")
    with pytest.raises(KillSwitchActive):
        g.complete("reasoning-large", P, use_case="uc1")
    g.revive("reasoning-large")
    assert g.complete("reasoning-large", P, use_case="uc1").text


def test_trace_has_genai_attributes():
    g, *_ = gw()
    g.complete("reasoning-large", P, use_case="uc1")
    attrs = g.tracer.spans[-1].attributes
    assert attrs["gen_ai.request.model"] == "large-v1"
    assert attrs["gen_ai.usage.input_tokens"] > 0
