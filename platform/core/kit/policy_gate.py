"""Policy gate: governance as code.

Validates the AI inventory against the risk tiers and the approved model list.
Runs in CI (.github/workflows/policy-gate.yml). A failing gate blocks the merge,
so "approved on paper" and "running in production" can't drift apart.

    kit-policy-gate                                   # default inventory
    kit-policy-gate --inventory path/to/inventory.yaml
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .config import load_yaml, repo_root
from .contracts import AUTONOMY, AgentContract, ContractError
from .prompts import PromptError, PromptRegistry

REQUIRED = ["id", "name", "owner", "risk_tier", "pattern", "autonomy_level", "models",
            "data_class", "status", "system_card"]
STATUSES = {"proposed", "pilot", "production", "retired"}
AGENTIC_PATTERNS = {"tool-using-agent", "multi-agent-orchestration", "conversational-customer-agent"}
DATA_ORDER = ["public", "internal", "confidential", "restricted"]


def check_contracts(s: dict, models: dict, today: dt.date) -> Findings:
    """Agents that act need an executable contract that stays inside the inventory entry."""
    f = Findings()
    sid = s["id"]
    refs = s.get("contracts") or []
    needs = AUTONOMY.index(s["autonomy_level"]) >= 2 or s["pattern"] in AGENTIC_PATTERNS
    if needs and not refs and s["status"] != "proposed":
        f.errors.append(f"{sid}: autonomy {s['autonomy_level']} / pattern {s['pattern']} needs an agent contract")
        return f
    loaded: dict[str, AgentContract] = {}
    for ref in refs:
        if not _exists(ref):
            f.errors.append(f"{sid}: contract file not found {ref}")
            continue
        try:
            c = AgentContract.load(ref)
        except ContractError as exc:
            f.errors.append(f"{sid}: {ref}: {exc}")
            continue
        loaded[c.agent] = c
        tag = f"{sid}: {c.ref}"
        if c.inventory_id != sid:
            f.errors.append(f"{tag} belongs to {c.inventory_id}, not {sid}")
        ok, why = c.is_usable(today)
        if not ok:
            f.errors.append(f"{tag}: {why}")
        elif c.valid_until and (c.valid_until - today).days <= 30:
            f.warnings.append(f"{tag}: expires {c.valid_until}; re-approve through the ARB")
        if AUTONOMY.index(c.autonomy_level) > AUTONOMY.index(s["autonomy_level"]):
            f.errors.append(f"{tag}: autonomy {c.autonomy_level} exceeds the system's {s['autonomy_level']}")
        if not c.models <= set(s["models"]):
            f.errors.append(f"{tag}: models {sorted(c.models - set(s['models']))} not listed for the system")
        for alias in c.models:
            m = models.get(alias)
            if m is None:
                f.errors.append(f"{tag}: model '{alias}' not approved")
            else:
                bad = c.data_classes - set(m.get("allowed_data_classes", []))
                if bad:
                    f.errors.append(f"{tag}: data classes {sorted(bad)} not allowed for '{alias}'")
        sys_level = DATA_ORDER.index(s["data_class"]) if s["data_class"] in DATA_ORDER else -1
        above = sorted(d for d in c.data_classes if d not in DATA_ORDER or DATA_ORDER.index(d) > sys_level)
        if above:
            f.errors.append(f"{tag}: data classes {above} exceed the system's '{s['data_class']}'")
        if s.get("arb_id") and c.approved_by != s["arb_id"]:
            f.errors.append(f"{tag}: approved_by {c.approved_by or '(none)'} does not match ARB {s['arb_id']}")
    for c in loaded.values():
        for d in c.delegates:
            if d not in loaded:
                f.errors.append(f"{sid}: {c.ref} delegates to '{d}' which has no contract in this system")
    return f


@dataclass
class Findings:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _exists(rel: str | None) -> bool:
    return bool(rel) and (repo_root() / rel).exists()


def check_system(s: dict, tiers: dict, models: dict, today: dt.date,
                 prompts: PromptRegistry | None = None) -> Findings:
    f = Findings()
    sid = s.get("id", "<no id>")
    for key in REQUIRED:
        if s.get(key) in (None, "", []):
            f.errors.append(f"{sid}: missing '{key}'")
    if f.errors:
        return f

    if s["status"] not in STATUSES:
        f.errors.append(f"{sid}: status must be one of {sorted(STATUSES)}")
    if s["status"] == "retired":
        return f

    tier = tiers.get(int(s["risk_tier"]))
    if tier is None:
        f.errors.append(f"{sid}: unknown risk_tier {s['risk_tier']}")
        return f

    level = s["autonomy_level"]
    if level not in AUTONOMY:
        f.errors.append(f"{sid}: autonomy_level must be one of {AUTONOMY}")
    elif AUTONOMY.index(level) > AUTONOMY.index(tier["max_autonomy"]):
        f.errors.append(f"{sid}: autonomy {level} exceeds Tier {s['risk_tier']} max {tier['max_autonomy']}")
    if level == "L4" and not s.get("arb_id"):
        f.errors.append(f"{sid}: L4 autonomy needs an ARB approval (arb_id)")

    if not _exists(s["system_card"]):
        f.errors.append(f"{sid}: system_card not found at {s['system_card']}")

    for need in tier.get("requires", []):
        if need == "arb_id" and not s.get("arb_id") and s["status"] != "proposed":
            f.errors.append(f"{sid}: Tier {s['risk_tier']} in {s['status']} needs arb_id")
        if need == "golden_set" and not _exists(s.get("golden_set")):
            f.errors.append(f"{sid}: Tier {s['risk_tier']} needs a golden_set file")
        if need == "impact_assessment" and not _exists(s.get("impact_assessment")):
            f.errors.append(f"{sid}: Tier {s['risk_tier']} needs an impact_assessment file")
        if need == "human_oversight" and not s.get("human_oversight"):
            f.errors.append(f"{sid}: Tier {s['risk_tier']} needs a human_oversight description")

    for alias in s["models"]:
        m = models.get(alias)
        if m is None:
            f.errors.append(f"{sid}: model alias '{alias}' is not on the approved list")
        elif s["data_class"] not in m.get("allowed_data_classes", []):
            f.errors.append(f"{sid}: data class '{s['data_class']}' not allowed for '{alias}'")

    for ref in s.get("prompts", []) or []:
        if prompts is None:
            f.errors.append(f"{sid}: lists prompts but no prompt registry was found")
            break
        try:
            prompts.resolve(str(ref))
        except PromptError as exc:
            f.errors.append(f"{sid}: prompt {ref}: {exc}")

    cf = check_contracts(s, models, today)
    f.errors += cf.errors
    f.warnings += cf.warnings

    if s["status"] == "production":
        last = s.get("last_review")
        if not last:
            f.warnings.append(f"{sid}: no last_review date")
        else:
            age = (today - dt.date.fromisoformat(str(last))).days
            if age > int(tier.get("review_days", 365)):
                f.warnings.append(f"{sid}: review overdue ({age} days since {last})")
    return f


def run(inventory: str, tiers_path: str, models_path: str, today: dt.date | None = None) -> Findings:
    today = today or dt.date.today()
    tiers = {int(k): v for k, v in load_yaml(tiers_path)["tiers"].items()}
    models = load_yaml(models_path)["models"]
    inv = load_yaml(inventory)
    prompts = PromptRegistry.load() if (repo_root() / "prompts" / "registry.yaml").is_file() else None
    total = Findings()
    # Contracts the runtime could load must be exactly the ones the inventory references.
    referenced = {str((repo_root() / r).resolve()) for s in inv.get("systems", []) for r in (s.get("contracts") or [])}
    agents_seen: dict[str, str] = {}
    cdir = repo_root() / "contracts"
    for fpath in sorted(cdir.glob("*.yaml")) if cdir.is_dir() else []:
        rel = fpath.relative_to(repo_root())
        if str(fpath.resolve()) not in referenced:
            total.errors.append(f"{rel}: not referenced by any inventory entry (orphan contract)")
        try:
            agent = AgentContract.load(fpath).agent
        except ContractError as exc:
            total.errors.append(f"{rel}: {exc}")
            continue
        if agent in agents_seen:
            total.errors.append(f"{rel}: second contract for agent '{agent}' (also {agents_seen[agent]})")
        agents_seen[agent] = str(rel)
    seen: set[str] = set()
    for s in inv.get("systems", []):
        if s.get("id") in seen:
            total.errors.append(f"{s['id']}: duplicate id")
        seen.add(s.get("id"))
        r = check_system(s, tiers, models, today, prompts)
        total.errors += r.errors
        total.warnings += r.warnings
    return total


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate the AI inventory")
    ap.add_argument("--inventory", default="01-governance/ai-inventory.yaml")
    ap.add_argument("--tiers", default="01-governance/risk-tiers.yaml")
    ap.add_argument("--models", default="02-architecture/standards/approved-models.yaml")
    args = ap.parse_args(argv)
    res = run(args.inventory, args.tiers, args.models)
    for w in res.warnings:
        print(f"WARN  {w}")
    for e in res.errors:
        print(f"FAIL  {e}")
    n = len(load_yaml(args.inventory).get("systems", []))
    print(f"\nPolicy gate {'PASSED' if res.ok else 'FAILED'}: {n} systems, "
          f"{len(res.errors)} errors, {len(res.warnings)} warnings")
    return 0 if res.ok else 1


if __name__ == "__main__":
    sys.exit(main())
