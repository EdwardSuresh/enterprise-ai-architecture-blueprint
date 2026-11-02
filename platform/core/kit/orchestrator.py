"""One guarded request, end to end.

input guardrails -> sector rules -> permission-aware retrieval -> LLM gateway
-> output guardrails -> answer with citations, refusal, or human hand-off.
Every step is traced. This is the sequence diagram in
02-architecture/reference-architecture.md, as code.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import guardrails as g
from .gateway import Gateway, KillSwitchActive, ProviderError
from .retrieval import Index
from .tracing import Tracer

PROMPT = """You answer only from the CONTEXT. If the answer is not there, say you don't know.
Cite sources by their [id].
CONTEXT:
{context}
QUESTION: {question}"""

HANDOFF = "I've passed this to a colleague who will follow up with you."
REFUSAL = "I can't help with that request here."


@dataclass
class Response:
    status: str  # answered | refused | handoff
    text: str
    citations: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    trace_id: str = ""
    cost_usd: float = 0.0


@dataclass
class Orchestrator:
    gateway: Gateway
    index: Index
    use_case: str
    rules: list[g.Rule] = field(default_factory=list)
    alias: str = "reasoning-large"
    min_grounding: float = 0.6
    tracer: Tracer | None = None

    def __post_init__(self) -> None:
        self.tracer = self.tracer or self.gateway.tracer

    def answer(self, question: str, user_groups: set[str]) -> Response:
        tid = self.tracer.new_trace()
        with self.tracer.span("kit.request", **{"kit.use_case": self.use_case}) as root:
            with self.tracer.span("kit.guardrail.input") as sp:
                gin = g.check_input(question, self.rules)
                sp.attributes.update({"kit.pii_found": gin.pii_found, "kit.reasons": gin.reasons})
            if not gin.allowed:
                root.attributes["kit.outcome"] = "refused"
                return Response("refused", REFUSAL, reasons=gin.reasons, trace_id=tid)
            if gin.handoff:
                root.attributes["kit.outcome"] = "handoff"
                return Response("handoff", HANDOFF, reasons=gin.reasons, trace_id=tid)

            with self.tracer.span("kit.retrieve") as sp:
                hits = self.index.search(gin.text, user_groups)
                sp.attributes["kit.hits"] = [h.doc.id for h in hits]
            if not hits:
                root.attributes["kit.outcome"] = "handoff"
                return Response("handoff", HANDOFF, reasons=["no_authorized_sources"], trace_id=tid)

            context = "\n".join(f"[{h.doc.id}] {h.doc.text}" for h in hits)
            try:
                out = self.gateway.complete(self.alias, PROMPT.format(context=context, question=gin.text),
                                            use_case=self.use_case)
            except (KillSwitchActive, ProviderError) as exc:
                root.attributes["kit.outcome"] = "handoff"
                return Response("handoff", HANDOFF, reasons=[type(exc).__name__], trace_id=tid)

            with self.tracer.span("kit.guardrail.output") as sp:
                gout = g.check_output(out.text, context, self.rules, self.min_grounding)
                sp.attributes["kit.reasons"] = gout.reasons
            if not gout.allowed:
                root.attributes["kit.outcome"] = "handoff"
                return Response("handoff", HANDOFF, reasons=gout.reasons, trace_id=tid, cost_usd=out.cost_usd)

            root.attributes["kit.outcome"] = "answered"
            used = [h.citation for h in hits if f"[{h.doc.id}]" in out.text] or [h.citation for h in hits]
            return Response("answered", gout.text, used, trace_id=tid,
                            cost_usd=out.cost_usd)
