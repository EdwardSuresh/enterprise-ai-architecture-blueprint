"""LLM gateway.

Agents ask for a model *alias* ("reasoning-large"), never a vendor model ID.
The gateway maps the alias to a provider via config/models.yaml, tries
fallbacks on failure, tags cost to a use case, enforces budgets and honours
a kill switch. Swapping clouds means changing config and an adapter, not agents.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Protocol

from .config import load_yaml
from .tracing import Tracer


@dataclass
class Completion:
    text: str
    input_tokens: int
    output_tokens: int
    provider: str = ""
    model: str = ""
    alias: str = ""
    cost_usd: float = 0.0


class Provider(Protocol):
    name: str

    def complete(self, prompt: str, model: str, max_tokens: int = 512) -> Completion: ...


class ProviderError(RuntimeError):
    pass


class BudgetExceeded(RuntimeError):
    pass


class KillSwitchActive(RuntimeError):
    pass


def estimate_tokens(text: str) -> int:
    """Rough estimate: about 1.3 tokens per word. Real adapters return true counts."""
    return max(1, int(len(text.split()) * 1.3))


_WORD = re.compile(r"[a-z0-9]+")
_STOP = set("a an the of to and or is are was were be for on in at by with this that it as do does did "
            "what which who whom how when where why can could should would my our your their i we you".split())


def _stem(w: str) -> str:
    """Very light stemming so 'fryers' matches 'fryer'."""
    for suf in ("ing", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def _content_words(text: str) -> set[str]:
    return {_stem(w) for w in _WORD.findall(text.lower()) if w not in _STOP and len(w) > 2}


class MockProvider:
    """Deterministic offline model used by labs and CI.

    It answers *extractively*: it returns the context sentences that share
    words with the question. That makes grounding and evals testable without
    any cloud account.
    """

    def __init__(self, name: str = "mock", fail: bool = False):
        self.name = name
        self.fail = fail
        self.calls = 0

    def complete(self, prompt: str, model: str, max_tokens: int = 512) -> Completion:
        self.calls += 1
        if self.fail:
            raise ProviderError(f"{self.name} unavailable")
        context, question = "", prompt
        if "CONTEXT:" in prompt and "QUESTION:" in prompt:
            context = prompt.split("CONTEXT:", 1)[1].split("QUESTION:", 1)[0]
            question = prompt.split("QUESTION:", 1)[1]
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", context) if s.strip()]
        q = _content_words(question)
        scored = sorted(((len(q & _content_words(s)), i, s) for i, s in enumerate(sentences)),
                        key=lambda t: (-t[0], t[1]))
        best = scored[0][0] if scored else 0
        picked = [t for t in scored if t[0] > 0 and t[0] >= best * 0.5][:4] or scored[:1]
        picked.sort(key=lambda t: t[1])  # keep source order
        text = " ".join(t[2] for t in picked) if picked else \
            "I don't know based on the approved sources. I will pass this to a colleague."
        return Completion(text=text, input_tokens=estimate_tokens(prompt),
                          output_tokens=estimate_tokens(text), provider=self.name, model=model)


@dataclass
class Gateway:
    models: dict
    providers: dict[str, Provider]
    tracer: Tracer = field(default_factory=Tracer)
    budgets_usd: dict[str, float] = field(default_factory=dict)
    disabled: set[str] = field(default_factory=set)  # aliases or use cases switched off
    spend_usd: dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_config(cls, providers: dict[str, Provider], path: str = "config/models.yaml",
                    tracer: Tracer | None = None, budgets_usd: dict[str, float] | None = None) -> "Gateway":
        cfg = load_yaml(path)
        return cls(models=cfg["aliases"], providers=providers, tracer=tracer or Tracer(),
                   budgets_usd=budgets_usd or {})

    def kill(self, name: str) -> None:
        """Kill switch: block an alias or a use case immediately."""
        self.disabled.add(name)

    def revive(self, name: str) -> None:
        self.disabled.discard(name)

    def complete(self, alias: str, prompt: str, use_case: str, max_tokens: int = 512) -> Completion:
        if alias in self.disabled or use_case in self.disabled:
            raise KillSwitchActive(f"'{alias}' / '{use_case}' is switched off")
        if alias not in self.models:
            raise KeyError(f"Unknown model alias '{alias}'. Add it to config/models.yaml.")
        # The budget is checked before each call, so the call that crosses the
        # limit completes and later calls are refused. Set budgets with headroom.
        budget = self.budgets_usd.get(use_case)
        if budget is not None and self.spend_usd.get(use_case, 0.0) >= budget:
            raise BudgetExceeded(f"{use_case} reached its budget of ${budget:.2f}")

        entry = self.models[alias]
        route = [entry["primary"], *entry.get("fallbacks", [])]
        errors = []
        for hop, target in enumerate(route):
            provider = self.providers.get(target["provider"])
            if provider is None:
                errors.append(f"{target['provider']}: not configured")
                continue
            with self.tracer.span("gen_ai.chat", **{
                "gen_ai.system": target["provider"], "gen_ai.request.model": target["model"],
                "kit.alias": alias, "kit.use_case": use_case, "kit.fallback_hop": hop,
            }) as sp:
                try:
                    out = provider.complete(prompt, target["model"], max_tokens)
                except ProviderError as exc:
                    sp.status = "error"
                    errors.append(str(exc))
                    continue
                cost = (out.input_tokens / 1000) * target.get("price_in_per_1k", 0) + \
                       (out.output_tokens / 1000) * target.get("price_out_per_1k", 0)
                out.cost_usd, out.alias = round(cost, 6), alias
                out.provider, out.model = target["provider"], target["model"]
                self.spend_usd[use_case] = self.spend_usd.get(use_case, 0.0) + cost
                sp.attributes.update({
                    "gen_ai.usage.input_tokens": out.input_tokens,
                    "gen_ai.usage.output_tokens": out.output_tokens,
                    "kit.cost_usd": out.cost_usd,
                })
                return out
        raise ProviderError(f"All routes failed for '{alias}': {errors}")
