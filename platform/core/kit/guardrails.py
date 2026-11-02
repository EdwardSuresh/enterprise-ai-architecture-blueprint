"""Input and output guardrails.

These are simple, transparent reference checks. In production, pair them with
your cloud's managed service (Azure AI Content Safety / Prompt Shields,
Amazon Bedrock Guardrails, Google Model Armor) behind the same interface.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .config import load_yaml, repo_root
from .gateway import _content_words

PII_PATTERNS = {
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "PHONE": re.compile(r"(?<!\d)(?:\+1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)"),
    "CARD": re.compile(r"\b(?:\d[ -]?){13,16}\b"),
}

INJECTION_PATTERNS = [
    # direct instruction override
    r"ignore (all |any )?(previous|prior|above|earlier) (instructions|rules)",
    r"disregard (your|the|all) (instructions|rules|guidelines|policies)",
    r"(new|updated) (policy|instructions?) from the (admin|administrator|developer|system)",
    r"you (no longer|don't|do not) need to (cite|follow|check|ask)",
    # indirect injection hidden in documents or emails
    r"note to the ai|(ai|llm) (assistant|agent|model),? reading this",
    # system prompt leakage
    r"(reveal|show|print|repeat|output|translate|summari[sz]e) (me )?(your|the) (full |entire |initial |original |hidden )?"
    r"(system prompt|instructions|initial instructions|hidden instructions|prompt)",
    # role-play jailbreaks and impersonation
    r"you are now (in )?(developer|dan|unrestricted|jailbroken)",
    r"(act as|pretend (to be|you are)|you are) (an? )?('?\w+'?,? )?(assistant )?(with no|without) (rules|policies|restrictions|guardrails)",
    r"pretend (to be|you are) (the )?(system )?(administrator|admin|developer|root)",
    r"\b(assistant|ai|bot|mode) (with no|without( any)?) (rules|policies|restrictions|guardrails|filters)",
    r"pretend (that )?(the|your) (rules|policies) (do not|don't) apply",
    # approval bypass and bulk destructive actions (excessive agency)
    r"skip (the )?(approval|review|human)( step)?",
    r"\b(mark|set|close|delete|resolve) (all|every) (open )?\w+",
    # cross-user and unauthorized data access
    r"(previous|other|last) user'?s?( asked| question| said)?|what did (the )?(previous|other) user",
    r"not allowed to see|i('m| am) not (authori[sz]ed|permitted)",
    # unbounded consumption
    r"(repeat|say|write|print) .{0,40}\b(million|billion|thousand) times|do not stop until",
]


def _luhn_ok(digits: str) -> bool:
    nums = [int(d) for d in digits][::-1]
    total = sum(n if i % 2 == 0 else (n * 2 - 9 if n * 2 > 9 else n * 2) for i, n in enumerate(nums))
    return total % 10 == 0


def redact_pii(text: str) -> tuple[str, list[str]]:
    """Replace personal data with [TYPE] placeholders. Returns (text, types found)."""
    found: list[str] = []

    def card_sub(m: re.Match) -> str:
        digits = re.sub(r"\D", "", m.group())
        if 13 <= len(digits) <= 16 and _luhn_ok(digits):
            found.append("CARD")
            return "[CARD]"
        return m.group()

    text = PII_PATTERNS["CARD"].sub(card_sub, text)
    for kind in ("EMAIL", "SSN", "PHONE"):
        text, n = PII_PATTERNS[kind].subn(f"[{kind}]", text)
        found += [kind] * n
    return text, found


def detect_injection(text: str) -> list[str]:
    low = text.lower()
    return [p for p in INJECTION_PATTERNS if re.search(p, low)]


@dataclass
class Rule:
    id: str
    type: str  # block_topic | require_human
    patterns: list[str]
    message: str = ""
    description: str = ""

    def matches(self, text: str) -> bool:
        return any(re.search(p, text, re.IGNORECASE) for p in self.patterns)


def load_pack_rules(pack: str) -> list[Rule]:
    path = repo_root() / "domain-packs" / pack / "guardrails.yaml"
    if not path.is_file():
        return []
    data = load_yaml(path) or {}
    return [Rule(id=r["id"], type=r["type"], patterns=list(r.get("patterns", [])),
                 message=r.get("message", ""), description=r.get("description", ""))
            for r in data.get("rules", [])]


def check_rules(text: str, rules: list[Rule]) -> list[Rule]:
    return [r for r in rules if r.matches(text)]


def grounding_score(answer: str, context: str) -> float:
    """Share of the answer's content words that appear in the source context."""
    a = _content_words(answer)
    if not a:
        return 1.0
    return round(len(a & _content_words(context)) / len(a), 3)


@dataclass
class GuardResult:
    allowed: bool
    text: str
    reasons: list[str] = field(default_factory=list)
    handoff: bool = False
    pii_found: list[str] = field(default_factory=list)


def check_input(text: str, rules: list[Rule]) -> GuardResult:
    clean, pii = redact_pii(text)
    inj = detect_injection(clean)
    if inj:
        return GuardResult(False, clean, ["prompt_injection"], pii_found=pii)
    hits = check_rules(clean, rules)
    blocks = [r for r in hits if r.type == "block_topic"]
    if blocks:
        return GuardResult(False, clean, [r.id for r in blocks], pii_found=pii)
    humans = [r for r in hits if r.type == "require_human"]
    return GuardResult(True, clean, [r.id for r in humans], handoff=bool(humans), pii_found=pii)


def check_output(answer: str, context: str, rules: list[Rule], min_grounding: float = 0.6) -> GuardResult:
    clean, pii = redact_pii(answer)
    reasons = [r.id for r in check_rules(clean, rules) if r.type == "block_topic"]
    score = grounding_score(clean, context)
    if score < min_grounding:
        reasons.append(f"low_grounding:{score}")
    return GuardResult(not reasons, clean, reasons, pii_found=pii)
