# Lab 06: Governance as Code

**Business case (Illustrative example):** Any organization needs one list of its AI systems and an Architecture Review Board (ARB) that approves them. Here the inventory is a YAML file. A policy gate checks every change against risk tiers, approved models and autonomy limits before it can merge.

| 5W1H | Answer |
|---|---|
| **Who** | ARB members, AI risk and compliance, EA, system owners, platform engineers |
| **What** | A policy gate that validates `01-governance/ai-inventory.yaml` against risk tiers, approved models and autonomy limits |
| **When** | On every pull request that adds or changes an AI system, and at each ARB meeting |
| **Where** | `kit.policy_gate` (`platform/core/kit/policy_gate.py`), `01-governance/`, `02-architecture/standards/approved-models.yaml` |
| **Why** | Policies on paper are not enforced. Policy as code turns ARB rules into checks that run on every change and leave evidence |
| **How** | Concept with the local policy gate, Build with cloud policy and inventory tools, Production with a required CI check and ARB records |

## Concept (plain Python, no cloud)

From the repo root:

```bash
pip install -e .
python labs/06-governance/concept.py
```

What it shows:

1. **The committed inventory passes.** The gate reads `01-governance/ai-inventory.yaml`, `01-governance/risk-tiers.yaml` and `02-architecture/standards/approved-models.yaml`.
2. **Three common violations are caught** in a modified copy:
   - autonomy level above what the risk tier allows,
   - a model not approved for the system's data class,
   - a missing golden set.
3. **Errors are specific.** Each names the system ID and the rule.

You can also run the CLI:

```bash
kit-policy-gate
```

Try this: add a new system to the inventory with `risk_tier: 3` and `autonomy_level: L3`, and run the gate.

## Build on Azure (reference implementation)

1. Create `rg-aikit-lab06` and a budget alert.
2. Tag every AI resource from Labs 01-05 with `ai_system_id` (for example `AIS-001`), `risk_tier` and `owner`.
3. Use **Azure Policy** to require these tags on AI resources and to restrict which model deployments are allowed. Start in audit mode.
4. Use **Azure Resource Graph** to list AI resources and compare them with the inventory file. Anything missing from the inventory is shadow AI.
5. Review the AI security and governance views in **Microsoft Foundry** and **Microsoft Defender for Cloud** (check which features your subscription includes at no cost).
6. Add **GitHub Actions** branch protection so `policy-gate.yml` must pass before merge.

## Build on AWS (short)

- Use **AWS Config** rules and **Service Control Policies** to require tags and restrict which Bedrock models can be invoked.
- Use AWS Resource Explorer or Config inventory to find AI resources and compare with the inventory file.

## Build on Google Cloud (short)

- Use **Organization Policy** constraints to restrict Vertex AI models and locations, and require labels.
- Use **Cloud Asset Inventory** to list Vertex AI resources and compare with the inventory file.

Service names and features change. Check the current docs for each provider.

## Production

1. Every system in the inventory has a system card (`01-governance/system-cards/`) and, for Tier 3, an impact assessment (`01-governance/impact-assessments/`).
2. ARB decisions go in `01-governance/arb/decision-log.md`, with the `arb_id` in the inventory entry.
3. Map controls to frameworks in `01-governance/control-maps/` (NIST AI RMF, ISO/IEC 42001, EU AI Act, OWASP LLM Top 10).
4. Sector use cases cite their pack, for example `domain-packs/financial-services/regulations.md`.
5. **CI gates:** `.github/workflows/policy-gate.yml` runs `kit-policy-gate` and must pass before merge. `.github/workflows/evals.yml` and `.github/workflows/ci.yml` provide the quality and test evidence the ARB reviews.
6. Evidence to keep: inventory git history, policy gate run logs, ARB decision log, cloud policy compliance reports.

## Exit criteria

- [ ] The policy gate passes on the committed inventory.
- [ ] I can trigger and explain each of the three violations.
- [ ] Cloud AI resources are tagged with the inventory system ID.
- [ ] A cloud policy audits required tags or allowed models.
- [ ] `policy-gate.yml` is a required check on the main branch.
- [ ] Each inventory entry links to a system card and ARB decision.

## Cleanup

```bash
az group delete -n rg-aikit-lab06 --yes --no-wait
```

Remove or switch off any policy assignments you created in audit mode if you no longer need them. On AWS, remove test Config rules. On Google Cloud, remove test organization policies.

**Maps to:** `platform/core/kit/policy_gate.py`, `01-governance/ai-inventory.yaml`, `01-governance/risk-tiers.yaml`, `01-governance/arb/`, `01-governance/system-cards/`, `01-governance/control-maps/`, `02-architecture/standards/approved-models.yaml`, `domain-packs/`.
