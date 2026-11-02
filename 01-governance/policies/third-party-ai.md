# Third-Party AI Policy (Template)

| 5W1H | Answer |
|---|---|
| **Who** | Procurement, vendor management, risk, security, legal, system owners |
| **What** | Rules for buying AI products, using model providers and accepting AI features in existing software |
| **When** | Before contract, before enabling a new AI feature, at renewal and on vendor change notice |
| **Where** | All suppliers whose products include AI, including SaaS features turned on by default |
| **Why** | Much AI arrives through vendors. Vendors change models without warning; the risk stays with you |
| **How** | Vendor questionnaire, contract clauses, inventory entry, change-notification monitoring |

**Policy owner:** <Head of procurement>  **Version:** 1.0

## 1. Scope

1.1 This policy covers model providers, AI products, and AI features within any purchased software.
1.2 New AI features in existing software count as a change and need review before use.

## 2. Due diligence

2.1 Complete the [vendor questionnaire](../templates/vendor-questionnaire.md) before contract or enablement.
2.2 Depth of review follows the risk tier of the intended use.

## 3. Inventory

3.1 Every third-party AI system in use is recorded in the AI inventory with an internal owner.

## 4. Contract terms

4.1 Contracts must cover: no training on our data without consent; data location; retention; security incident notice; sub-processor disclosure; audit or assurance reports; exit and data return.
4.2 Contracts must require advance notice of material model or behaviour changes.
4.3 For Tier 2 and Tier 3 uses, the contract must allow us to evaluate outputs or provide equivalent evidence.

## 5. Change management

5.1 Vendor model changes are treated as model version changes (see [runbook](../../ops/runbooks/model-version-change.md)).
5.2 Where the vendor cannot give notice, the system owner runs scheduled evaluations to detect behaviour change.

## 6. Integration

6.1 Where technically possible, vendor model calls are routed through the LLM gateway.
6.2 Where not possible, the vendor must provide logs or reports enough to meet the [logging standard](../../02-architecture/standards/logging-standard.md) for the tier.

## 7. Ongoing monitoring

7.1 Review vendor AI at least yearly, and at each renewal.
7.2 Track vendor incidents and notices in the AI inventory entry.

## 8. Exit

8.1 Keep an exit plan for Tier 2 and Tier 3 vendor AI, including data return and deletion confirmation.

## 9. Exceptions

9.1 Exceptions require ARB approval with an expiry date and are logged in the decision log.
