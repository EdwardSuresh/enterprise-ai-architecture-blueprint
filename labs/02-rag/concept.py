"""Lab 02 Concept: permission-aware RAG (business case: insurer underwriting manual Q&A).

Shows: retrieval filtered by access rights BEFORE ranking, answers with citations,
a versioned prompt from prompts/registry.yaml, short-term conversation memory,
and a hand-off when the user may not see any relevant source.
Run:  python labs/02-rag/concept.py
"""
from kit.gateway import Gateway, MockProvider
from kit.memory import ShortTermMemory
from kit.prompts import PromptRegistry
from kit.orchestrator import Orchestrator
from kit.retrieval import Document, Index

docs = [
    Document("UW-3.2", "Restaurant appetite",
             "Restaurants with deep fryers need an automatic fire suppression system. "
             "Hood cleaning must be done every six months.", {"underwriters"}),
    Document("UW-5.1", "Property limits",
             "Senior underwriters may approve property limits up to 10 million dollars. "
             "Larger limits need reinsurance review.", {"underwriters"}),
    Document("EX-1.0", "Executive authority matrix",
             "Only the chief underwriting officer may approve limits above 50 million dollars.",
             {"executives"}),
]
gw = Gateway.from_config({"mock-primary": MockProvider("mock-primary")})
memory = ShortTermMemory()
bot = Orchestrator(gw, Index(docs), use_case="underwriting-assistant",
                   prompts=PromptRegistry.load(), memory=memory)

print("Underwriters cannot see EX-1.0, so their answers come only from documents they may read.")
for who, groups, q in [
    ("Underwriter", {"underwriters"}, "What does a restaurant with a deep fryer need?"),
    ("Underwriter", {"underwriters"}, "Who may approve limits above 50 million dollars?"),
    ("Executive", {"executives"}, "Who may approve limits above 50 million dollars?"),
]:
    r = bot.answer(q, groups, conversation_id=who)
    print(f"\n{who}: {q}\n  status={r.status}  prompt={r.prompt_ref}\n  answer={r.text}\n  citations={r.citations} reasons={r.reasons}")

print("\nUnderwriter conversation memory (PII redacted, expires when idle):")
print(memory.as_text("Underwriter"))
