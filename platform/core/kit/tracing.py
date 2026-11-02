"""Minimal tracer.

Attribute names follow the OpenTelemetry GenAI semantic conventions
(gen_ai.request.model, gen_ai.usage.input_tokens, ...) so the same fields
carry over when you swap this for the real OpenTelemetry SDK.
"""
from __future__ import annotations

import json
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator


@dataclass
class Span:
    name: str
    trace_id: str
    span_id: str
    start: float
    end: float = 0.0
    attributes: dict[str, Any] = field(default_factory=dict)
    status: str = "ok"

    @property
    def duration_ms(self) -> float:
        return round((self.end - self.start) * 1000, 2)

    def to_dict(self) -> dict:
        return {
            "name": self.name, "trace_id": self.trace_id, "span_id": self.span_id,
            "duration_ms": self.duration_ms, "status": self.status, "attributes": self.attributes,
        }


class Tracer:
    def __init__(self, export_path: str | Path | None = None):
        self.spans: list[Span] = []
        self.export_path = Path(export_path) if export_path else None
        self.trace_id = uuid.uuid4().hex[:16]

    def new_trace(self) -> str:
        self.trace_id = uuid.uuid4().hex[:16]
        return self.trace_id

    @contextmanager
    def span(self, name: str, **attributes: Any) -> Iterator[Span]:
        sp = Span(name=name, trace_id=self.trace_id, span_id=uuid.uuid4().hex[:8],
                  start=time.perf_counter(), attributes=dict(attributes))
        try:
            yield sp
        except Exception as exc:  # record, then re-raise
            sp.status = f"error: {type(exc).__name__}"
            raise
        finally:
            sp.end = time.perf_counter()
            self.spans.append(sp)
            if self.export_path:
                self.export_path.parent.mkdir(parents=True, exist_ok=True)
                with self.export_path.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(sp.to_dict()) + "\n")

    def for_trace(self, trace_id: str) -> list[Span]:
        return [s for s in self.spans if s.trace_id == trace_id]
