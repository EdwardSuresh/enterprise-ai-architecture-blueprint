# AI impact assessment: AIS-004 Small-business credit memo drafter

> **Illustrative example** for a fictitious bank. Use `template.md` in this folder for real assessments.

| Question | Answer |
|---|---|
| Who | Credit officers (users); small-business applicants (affected people) |
| What | AI drafts the credit memo and reason codes from the approved probability-of-default model |
| When | At application review, before the credit decision |
| Where | Business lending workbench; private model endpoint in an approved region |
| Why | Officers spend most review time writing memos instead of analysing risk |
| How | Extraction model reads financial statements; scoring model produces reasons; officer edits and decides |

## Affected people and possible harms
- Applicants could be harmed if the memo misstates figures or if reason codes differ by group.
- Risk of automation bias: officers accepting drafts without checking.

## Controls
1. Officer makes and records the decision; the system cannot approve or decline (autonomy L1).
2. Figures in the memo are linked to source pages; grounding threshold 0.7.
3. Bias testing by protected-class proxies before each release; results to Model Risk.
4. Weekly sample of memos reviewed against source documents.
5. Edit rate and override rate tracked; a near-zero edit rate triggers a rubber-stamp review.

## Sign-off
| Role | Name | Date |
|---|---|---|
| Business owner | | |
| Model risk | | |
| Compliance (fair lending) | | |
| Enterprise architecture | | |
