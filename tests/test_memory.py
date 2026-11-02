import datetime as dt

import pytest

from kit.gateway import Gateway, MockProvider
from kit.memory import LongTermMemory, ShortTermMemory
from kit.orchestrator import Orchestrator
from kit.prompts import PromptRegistry
from kit.retrieval import Document, Index


class Clock:
    def __init__(self):
        self.now = dt.datetime(2026, 11, 1, 9, 0, tzinfo=dt.timezone.utc)

    def __call__(self):
        return self.now

    def advance(self, **kw):
        self.now += dt.timedelta(**kw)


def test_short_term_keeps_last_turns_and_redacts():
    m = ShortTermMemory(max_turns=3)
    for i in range(5):
        m.add("c1", "user", f"turn {i}")
    assert [t.text for t in m.history("c1")] == ["turn 2", "turn 3", "turn 4"]
    m.add("c2", "user", "email me at pat@example.com")
    assert "[EMAIL]" in m.as_text("c2") and "pat@" not in m.as_text("c2")


def test_short_term_expires_when_idle():
    clock = Clock()
    m = ShortTermMemory(idle_minutes=30, clock=clock)
    m.add("c1", "user", "hello")
    clock.advance(minutes=31)
    assert m.history("c1") == [] and m.as_text("c1") == "(none)"


def test_long_term_retention_export_and_forget():
    clock = Clock()
    m = LongTermMemory(retention_days=30, clock=clock, allowed_keys={"language", "branch"})
    m.remember("u1", "language", "Spanish")
    m.remember("u1", "branch", "call 405-555-0134")
    assert m.recall("u1")["branch"] == "call [PHONE]"
    assert len(m.export("u1")) == 2
    with pytest.raises(ValueError):
        m.remember("u1", "income", "x")              # not an allowed key
    clock.advance(days=31)
    assert m.recall("u1") == {}                      # expired
    m.remember("u2", "language", "Tamil")
    assert m.forget("u2") == 1 and m.recall("u2") == {}


def test_long_term_caps_facts_per_user():
    m = LongTermMemory(max_facts_per_user=2, clock=Clock())
    for k in ("a", "b", "c"):
        m.remember("u", k, k)
    assert set(m.recall("u")) == {"b", "c"}


def test_orchestrator_uses_registry_prompt_and_memory():
    docs = [Document("P1", "Fees", "The monthly fee is waived when the balance is at least 1500 dollars.", {"customers"})]
    gw = Gateway.from_config({"mock-primary": MockProvider("mock-primary")})
    mem = ShortTermMemory()
    bot = Orchestrator(gw, Index(docs), "fee-faq", prompts=PromptRegistry.load(), memory=mem)
    r = bot.answer("When is the monthly fee waived?", {"customers"}, conversation_id="c9")
    assert r.status == "answered" and r.prompt_ref == "rag-answer@1.1.0"
    root = [s for s in gw.tracer.spans if s.name == "kit.request"][-1]
    assert root.attributes["kit.prompt.version"] == "1.1.0"
    assert len(mem.history("c9")) == 2              # user turn + assistant turn
    r2 = bot.answer("And what balance again?", {"customers"}, conversation_id="c9")
    assert len(mem.history("c9")) == 4
