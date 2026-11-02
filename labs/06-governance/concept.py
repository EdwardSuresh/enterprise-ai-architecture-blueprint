"""Lab 06 Concept: governance as code (business case: AI inventory and ARB).

Shows: the policy gate passing on the inventory, then catching three
common violations in a modified copy.
Run:  python labs/06-governance/concept.py
"""
import copy
import datetime as dt

from kit.config import load_yaml
from kit.policy_gate import check_system, run

res = run("01-governance/ai-inventory.yaml", "01-governance/risk-tiers.yaml",
          "02-architecture/standards/approved-models.yaml")
print(f"Inventory as committed: {'PASS' if res.ok else 'FAIL'} ({len(res.errors)} errors, {len(res.warnings)} warnings)")

tiers = {int(k): v for k, v in load_yaml("01-governance/risk-tiers.yaml")["tiers"].items()}
models = load_yaml("02-architecture/standards/approved-models.yaml")["models"]
system = load_yaml("01-governance/ai-inventory.yaml")["systems"][0]

bad = copy.deepcopy(system)
bad["autonomy_level"] = "L4"           # too much autonomy for Tier 2
bad["models"] = ["public-assistant"]   # public-only model with confidential data
bad.pop("golden_set")                  # no evals
print("\nModified system:")
for e in check_system(bad, tiers, models, dt.date.today()).errors:
    print("  FAIL", e)
