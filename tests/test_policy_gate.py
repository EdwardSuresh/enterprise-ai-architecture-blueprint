import copy
import datetime as dt

from kit.config import load_yaml
from kit.policy_gate import check_system, run
from kit.prompts import PromptRegistry

TIERS = {int(k): v for k, v in load_yaml("01-governance/risk-tiers.yaml")["tiers"].items()}
MODELS = load_yaml("02-architecture/standards/approved-models.yaml")["models"]
BASE = load_yaml("01-governance/ai-inventory.yaml")["systems"][0]
TODAY = dt.date(2026, 11, 1)
PROMPTS = PromptRegistry.load()


def errors(**changes):
    s = copy.deepcopy(BASE)
    for k, v in changes.items():
        if v is None:
            s.pop(k, None)
        else:
            s[k] = v
    return check_system(s, TIERS, MODELS, TODAY, PROMPTS).errors


def test_committed_inventory_passes():
    res = run("01-governance/ai-inventory.yaml", "01-governance/risk-tiers.yaml",
              "02-architecture/standards/approved-models.yaml", TODAY)
    assert res.ok, res.errors


def test_valid_example_passes():
    assert errors() == []


def test_autonomy_over_tier_limit():
    assert any("exceeds" in e for e in errors(autonomy_level="L4"))


def test_model_not_allowed_for_data_class():
    assert any("not allowed" in e for e in errors(models=["public-assistant"]))


def test_unapproved_model():
    assert any("approved list" in e for e in errors(models=["random-model"]))


def test_tier2_needs_golden_and_arb():
    assert any("golden_set" in e for e in errors(golden_set=None))
    assert any("arb_id" in e for e in errors(arb_id=None))


def test_tier3_needs_impact_assessment():
    assert any("impact_assessment" in e for e in errors(risk_tier=3, autonomy_level="L1", impact_assessment=None))


def test_missing_system_card_file():
    assert any("system_card not found" in e for e in errors(system_card="nope.yaml"))
