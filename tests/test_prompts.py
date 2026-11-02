import copy
import datetime as dt

import pytest

from kit.config import load_yaml, repo_root
from kit.policy_gate import check_system
from kit.prompts import PromptError, PromptRegistry

REG = PromptRegistry.load()


def test_registry_is_valid():
    assert REG.validate() == []


def test_get_current_and_render():
    p = REG.get("rag-answer")
    assert p.version == "1.1.0" and p.status == "approved"
    text = p.render(history="(none)", context="[A] fact", question="q?")
    assert "[A] fact" in text and "QUESTION: q?" in text
    assert p.trace_attributes()["kit.prompt.version"] == "1.1.0"
    assert len(p.sha256) == 12


def test_missing_variable_is_an_error():
    with pytest.raises(PromptError):
        REG.get("rag-answer").render(context="x")


def test_deprecated_and_unknown_versions_blocked():
    with pytest.raises(PromptError):
        REG.get("rag-answer", "1.0.0")            # deprecated
    assert REG.get("rag-answer", "1.0.0", allow_unapproved=True).version == "1.0.0"
    with pytest.raises(PromptError):
        REG.resolve("rag-answer@9.9.9")
    with pytest.raises(PromptError):
        REG.get("no-such-prompt")


def test_validate_catches_bad_current():
    bad = copy.deepcopy(REG.data)
    bad["rag-answer"]["current"] = "1.0.0"         # deprecated version
    problems = PromptRegistry({"prompts": bad}, repo_root()).validate()
    assert any("not approved" in p for p in problems)


def test_policy_gate_checks_prompts():
    tiers = {int(k): v for k, v in load_yaml("01-governance/risk-tiers.yaml")["tiers"].items()}
    models = load_yaml("02-architecture/standards/approved-models.yaml")["models"]
    s = copy.deepcopy(load_yaml("01-governance/ai-inventory.yaml")["systems"][0])
    today = dt.date(2026, 11, 1)
    assert check_system(s, tiers, models, today, REG).errors == []
    s["prompts"] = ["rag-answer@1.0.0"]
    assert any("not approved" in e for e in check_system(s, tiers, models, today, REG).errors)
