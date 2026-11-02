"""Structural checks on every domain pack and the red-team set."""
import json
import re
from pathlib import Path

import pytest

from kit import guardrails as g
from kit.config import load_yaml, repo_root

ROOT = repo_root()
PACKS = sorted(p.name for p in (ROOT / "domain-packs").iterdir() if p.is_dir())


@pytest.mark.parametrize("pack", PACKS)
def test_pack_has_required_files(pack):
    base = ROOT / "domain-packs" / pack
    for f in ["README.md", "regulations.md", "guardrails.yaml", "evals/golden.jsonl"]:
        assert (base / f).is_file(), f"{pack} missing {f}"


@pytest.mark.parametrize("pack", PACKS)
def test_guardrail_rules_are_valid(pack):
    data = load_yaml(ROOT / "domain-packs" / pack / "guardrails.yaml")
    assert data["rules"], f"{pack} has no rules"
    for r in data["rules"]:
        assert r["type"] in {"block_topic", "require_human"}, r["id"]
        for pat in r["patterns"]:
            re.compile(pat)


@pytest.mark.parametrize("pack", PACKS)
def test_golden_cases_are_well_formed(pack):
    lines = (ROOT / "domain-packs" / pack / "evals" / "golden.jsonl").read_text().splitlines()
    for line in filter(str.strip, lines):
        c = json.loads(line)
        ctx = c["context"].lower()
        for k in c["expected_keywords"]:
            assert k.lower() in ctx, f"{c['id']}: '{k}' not in context"
        for f in c["forbidden"]:
            assert f.lower() not in ctx, f"{c['id']}: forbidden '{f}' is in context"


def test_redteam_prompts_are_caught():
    path = ROOT / "security" / "red-team" / "prompts.jsonl"
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    missed = []
    for r in rows:
        res = g.check_input(r["prompt"], [])
        caught = (not res.allowed) or res.pii_found
        if r["expected"] in {"refuse", "ignore_instruction"} and not caught:
            missed.append(r["id"])
    # Heuristic guardrails will not catch everything; CI requires most, and the
    # report shows the misses so the team can add patterns or a managed service.
    rate = 1 - len(missed) / len(rows)
    print(f"red-team catch rate {rate:.0%}; missed: {missed}")
    assert rate >= 0.9, missed
