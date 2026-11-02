"""Lab 05 Concept: golden-set evals (business case: oil & gas daily drilling report summary).

Shows: running a golden set, pass threshold, and what a regression looks like.
Run:  python labs/05-evals/concept.py
"""
from kit.evals import evaluate, load_golden, mock_answer, pass_rate

cases = load_golden("domain-packs/oil-and-gas/evals/golden.jsonl")
res = evaluate(cases)
print(f"Baseline system: {pass_rate(res):.0%} of {len(res)} cases pass")

def broken(question: str, context: str) -> str:
    """Simulates a bad prompt change: answers only from the first sentence."""
    return mock_answer(question, context.split(". ")[0])

res2 = evaluate(cases, broken)
print(f"After a bad change: {pass_rate(res2):.0%} pass")
for r in res2:
    if not r.passed:
        print(f"  {r.id} missing {r.missing}")
print("\nIn CI, evals.yml fails the pull request when the rate drops below the threshold.")
