# Policy as code

Governance rules that a machine checks on every pull request.

| | |
|---|---|
| **What** | `kit-policy-gate` validates `01-governance/ai-inventory.yaml` against `risk-tiers.yaml` and `02-architecture/standards/approved-models.yaml` |
| **Why** | Stops "governance theater": approvals on paper that nothing enforces |
| **Who** | EA owns the rules; Risk approves changes; every delivery team is checked |
| **When** | Every pull request (`.github/workflows/policy-gate.yml`) |
| **Where** | Code: `platform/core/kit/policy_gate.py` |
| **How** | `pip install -e . && kit-policy-gate` |

## Rules checked today
- Required fields present (owner, tier, pattern, autonomy, models, data class, status, system card).
- Autonomy level within the tier's maximum; L4 needs an ARB ID.
- System card file exists.
- Tier 2+: ARB ID (once past "proposed"), golden set file, human-oversight statement.
- Tier 3: AI impact assessment file.
- Every model alias is on the approved list and allowed for the system's data class.
- Production systems: warning when the review date is older than the tier's review cycle.

## Adding a rule
Add the check in `check_system()`, add a failing case to `tests/test_policy_gate.py`, and record the change in `CHANGELOG.md`. You can also express rules in OPA/Rego if your organization already uses it; keep the same inputs.
