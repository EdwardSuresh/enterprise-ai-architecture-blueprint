# AI Impact Assessment (Tier 3)

Required for every Tier 3 system. Recommended for Tier 2 systems that touch personal data. Can be combined with a data protection impact assessment where your privacy process allows.

| 5W1H | Answer |
|---|---|
| **Who** | Prepared by the delivery team and system owner; reviewed by risk, privacy, legal; signed off by the accountable executive |
| **What** | An assessment of how the AI system could affect people, and how harms are prevented or reduced |
| **When** | Before build starts; updated before release and after any material change |
| **Where** | Stored with the ARB pack; linked from the AI inventory entry |
| **Why** | Finds harms early, while design can still change |
| **How** | Answer each section. Where a section does not apply, say why |

**Use case id:** UC-___  **System name:** ______  **Version:** ___  **Date:** ______

## 1. Purpose and context

| Question | Answer |
|---|---|
| What does the system do, in plain words? | |
| What decision does it support, and who makes the final decision? | |
| Why is AI needed here? What is the non-AI alternative? | |
| Autonomy level (L0–L2 for Tier 3) | |
| Regulatory classification (confirmed by legal) | |

## 2. Affected people

| Group | How they are affected | Direct or indirect | Vulnerable? (e.g. minors, patients, people in financial difficulty) |
|---|---|---|---|
| | | | |

## 3. Fairness

| Question | Answer |
|---|---|
| Which groups could be treated differently? | |
| Which attributes or proxies (postcode, language, age) could drive unfair outcomes? | |
| Fairness measures and thresholds chosen, and why | |
| Test results by group (attach eval report) | |
| What happens if thresholds are breached in production? | |

## 4. Explainability and transparency

| Question | Answer |
|---|---|
| What does the reviewer see to understand the output (sources, reasons, confidence)? | |
| What are affected people told, and when? | |
| Can a decision be explained afterwards from logs? | |

## 5. Privacy

| Question | Answer |
|---|---|
| Personal data used, and lawful basis | |
| Special category data? | |
| Minimization and masking applied | |
| Retention in prompts, logs, indexes | |
| How data subject rights are met | |
| Link to privacy assessment | |

## 6. Safety and reliability

| Question | Answer |
|---|---|
| Worst credible failure and its effect on a person | |
| How the system fails safe (fallback to human queue, kill switch) | |
| Known limits and out-of-scope inputs | |
| Accuracy and groundedness thresholds | |
| Security threats (link to threat model) | |

## 7. Human oversight

| Question | Answer |
|---|---|
| Who reviews, with what training and authority | |
| Expected review time per item and workload | |
| Override and sampling plan | |
| Contest and redress route for affected people | |

## 8. Workforce

Link to the [workforce impact assessment](../../enablement/workforce-impact-assessment.md) if roles change.

## 9. Risks and mitigations

| # | Risk | Likelihood (L/M/H) | Impact (L/M/H) | Mitigation | Residual | Owner |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

## 10. Monitoring after release

| Measure | Threshold | Frequency | Owner |
|---|---|---|---|
| Override rate | | | |
| Fairness gap | | | |
| Complaints and contests | | | |
| Groundedness or accuracy | | | |

## 11. Sign-off

| Role | Name | Decision | Date |
|---|---|---|---|
| System owner | | | |
| Risk lead | | | |
| Data protection lead | | | |
| Legal | | | |
| Accountable executive | | | |
