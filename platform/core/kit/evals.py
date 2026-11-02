"""Golden-set evaluation runner.

Golden line format (JSONL):
{"id": "...", "input": "...", "context": "...", "expected_keywords": [...], "forbidden": [...]}

A case passes when every expected keyword appears in the answer and no
forbidden phrase does. Use it as a CI gate:

    kit-evals --suite evals/suites/quality.yaml
    kit-evals domain-packs/insurance/evals/golden.jsonl --threshold 0.9
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .config import load_yaml, repo_root
from .gateway import MockProvider

AnswerFn = Callable[[str, str], str]


@dataclass
class CaseResult:
    id: str
    passed: bool
    missing: list[str]
    forbidden_found: list[str]


def load_golden(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.is_absolute():
        p = repo_root() / p
    with p.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def mock_answer(question: str, context: str) -> str:
    """Offline answerer: the extractive MockProvider over the case's own context."""
    prompt = f"CONTEXT:\n{context}\nQUESTION: {question}"
    return MockProvider().complete(prompt, "mock").text


def evaluate(cases: list[dict], answer_fn: AnswerFn = mock_answer) -> list[CaseResult]:
    results = []
    for c in cases:
        ans = answer_fn(c["input"], c.get("context", "")).lower()
        missing = [k for k in c.get("expected_keywords", []) if k.lower() not in ans]
        bad = [f for f in c.get("forbidden", []) if f.lower() in ans]
        results.append(CaseResult(c["id"], not missing and not bad, missing, bad))
    return results


def pass_rate(results: list[CaseResult]) -> float:
    return round(sum(r.passed for r in results) / len(results), 3) if results else 0.0


def _report(name: str, results: list[CaseResult], threshold: float) -> bool:
    rate = pass_rate(results)
    ok = rate >= threshold
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {rate:.0%} of {len(results)} cases (threshold {threshold:.0%})")
    for r in results:
        if not r.passed:
            print(f"   - {r.id}: missing={r.missing} forbidden={r.forbidden_found}")
    return ok


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run golden-set evals")
    ap.add_argument("golden", nargs="?", help="path to a golden.jsonl file")
    ap.add_argument("--suite", help="YAML suite listing golden sets and thresholds")
    ap.add_argument("--threshold", type=float, default=0.8)
    args = ap.parse_args(argv)

    jobs: list[tuple[str, float]] = []
    redteam: list[tuple[str, float]] = []
    if args.suite:
        suite = load_yaml(args.suite)
        jobs = [(s["golden"], float(s.get("threshold", suite.get("default_threshold", 0.8))))
                for s in suite.get("sets", [])]
        redteam = [(r["prompts"], float(r.get("threshold", 0.9))) for r in suite.get("redteam", [])]
        if not jobs and not redteam:
            ap.error(f"{args.suite} has no 'sets' or 'redteam' entries")
    elif args.golden:
        jobs = [(args.golden, args.threshold)]
    else:
        ap.error("give a golden file or --suite")

    all_ok = True
    for path, thr in jobs:
        all_ok &= _report(path, evaluate(load_golden(path)), thr)
    for path, thr in redteam:
        all_ok &= _report_redteam(path, thr)
    return 0 if all_ok else 1


def redteam_results(path: str | Path) -> list[CaseResult]:
    """Check each red-team prompt against the input guardrail."""
    from .guardrails import check_input
    results = []
    for row in load_golden(path):
        if row.get("expected") == "redact":
            continue  # redaction requests are handled by output redaction, tested separately
        res = check_input(row["prompt"], [])
        caught = (not res.allowed) or bool(res.pii_found)
        results.append(CaseResult(row["id"], caught, [] if caught else [row.get("category", "")], []))
    return results


def _report_redteam(path: str, threshold: float) -> bool:
    return _report(f"{path} (red team)", redteam_results(path), threshold)


if __name__ == "__main__":
    sys.exit(main())
