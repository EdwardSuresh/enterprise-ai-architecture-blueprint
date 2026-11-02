"""Reference API (FastAPI). Offline mock model; replace providers via kit_adapters.

Run: pip install -e .[api] && uvicorn api.app:app --reload
"""
from fastapi import FastAPI, Header
from pydantic import BaseModel

from kit.gateway import Gateway, MockProvider
from kit.guardrails import load_pack_rules
from kit.orchestrator import Orchestrator
from kit.retrieval import Document, Index

app = FastAPI(title="Enterprise AI Blueprint reference API")
_docs = [Document("POL-1", "Returns", "Returns are accepted within 30 days with a receipt.", {"customers"})]
_bot = Orchestrator(Gateway.from_config({"mock-primary": MockProvider("mock-primary")}),
                    Index(_docs), use_case="retail-chat", rules=load_pack_rules("retail"))


class Ask(BaseModel):
    question: str


@app.post("/v1/ask")
def ask(body: Ask, x_user_groups: str = Header(default="customers")):
    # Demo only: real deployments derive groups from the verified identity token.
    r = _bot.answer(body.question, set(x_user_groups.split(",")))
    return {"status": r.status, "answer": r.text, "citations": r.citations, "trace_id": r.trace_id}
