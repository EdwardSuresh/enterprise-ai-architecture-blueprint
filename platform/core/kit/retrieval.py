"""Permission-aware retrieval with citations.

Pure-Python TF-IDF so the Concept labs run anywhere. The important part is the
*order*: filter by the user's access rights first, then rank. That prevents the
"permission-blind RAG" anti-pattern. In Build labs this interface is backed by
Azure AI Search, OpenSearch / Bedrock Knowledge Bases, or Vertex AI Search.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field

_TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if len(t) > 2]


@dataclass
class Document:
    id: str
    title: str
    text: str
    acl: set[str] = field(default_factory=lambda: {"all-staff"})
    source: str = ""


@dataclass
class Hit:
    doc: Document
    score: float

    @property
    def citation(self) -> str:
        return f"[{self.doc.id}] {self.doc.title}"


class Index:
    def __init__(self, docs: list[Document]):
        self.docs = docs
        self.tf = [Counter(tokenize(d.title + " " + d.text)) for d in docs]
        df = Counter(t for tf in self.tf for t in tf)
        n = len(docs)
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1 for t, c in df.items()}

    def _vec(self, tf: Counter) -> dict[str, float]:
        return {t: c * self.idf.get(t, 1.0) for t, c in tf.items()}

    @staticmethod
    def _cos(a: dict[str, float], b: dict[str, float]) -> float:
        dot = sum(v * b.get(t, 0.0) for t, v in a.items())
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        return dot / (na * nb) if na and nb else 0.0

    def search(self, query: str, user_groups: set[str], k: int = 3, min_score: float = 0.05) -> list[Hit]:
        q = self._vec(Counter(tokenize(query)))
        hits = []
        for doc, tf in zip(self.docs, self.tf):
            if not (doc.acl & user_groups):  # access check BEFORE ranking
                continue
            s = self._cos(q, self._vec(tf))
            if s >= min_score:
                hits.append(Hit(doc, round(s, 4)))
        return sorted(hits, key=lambda h: -h.score)[:k]
