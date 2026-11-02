"""Conversation memory with retention rules.

Short-term memory keeps the last few turns of one conversation so follow-up
questions make sense. Long-term memory keeps a small number of facts per user
(for example a preferred language) with an expiry date.

Both redact personal data before storing, both expire, and long-term memory
supports export and forget-me requests. Memory is never used as a source of
truth for answers: the orchestrator passes it to the prompt only as context
for understanding the question, and the prompt says so.
"""
from __future__ import annotations

import datetime as dt
from collections import deque
from dataclasses import dataclass, field
from typing import Callable

from .guardrails import redact_pii

Clock = Callable[[], dt.datetime]


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


@dataclass
class Turn:
    role: str  # "user" or "assistant"
    text: str
    at: dt.datetime


@dataclass
class ShortTermMemory:
    """Last N turns per conversation; idle conversations expire."""
    max_turns: int = 6
    idle_minutes: int = 30
    clock: Clock = _utcnow
    _store: dict[str, deque] = field(default_factory=dict)

    def add(self, conversation_id: str, role: str, text: str) -> None:
        clean, _ = redact_pii(text)
        q = self._store.setdefault(conversation_id, deque(maxlen=self.max_turns))
        q.append(Turn(role, clean, self.clock()))

    def history(self, conversation_id: str) -> list[Turn]:
        q = self._store.get(conversation_id)
        if not q:
            return []
        if self.clock() - q[-1].at > dt.timedelta(minutes=self.idle_minutes):
            del self._store[conversation_id]  # expired
            return []
        return list(q)

    def as_text(self, conversation_id: str) -> str:
        return "\n".join(f"{t.role}: {t.text}" for t in self.history(conversation_id)) or "(none)"

    def clear(self, conversation_id: str) -> None:
        self._store.pop(conversation_id, None)


@dataclass
class Fact:
    key: str
    value: str
    created: dt.datetime
    expires: dt.datetime


@dataclass
class LongTermMemory:
    """A few remembered facts per user, each with an expiry. Supports export and forget."""
    retention_days: int = 90
    max_facts_per_user: int = 20
    allowed_keys: set[str] | None = None  # None = any key; set it to restrict what may be kept
    clock: Clock = _utcnow
    _store: dict[str, dict[str, Fact]] = field(default_factory=dict)

    def remember(self, user_id: str, key: str, value: str) -> None:
        if self.allowed_keys is not None and key not in self.allowed_keys:
            raise ValueError(f"'{key}' is not an allowed memory key")
        clean, _ = redact_pii(value)
        now = self.clock()
        facts = self._store.setdefault(user_id, {})
        if key not in facts and len(facts) >= self.max_facts_per_user:
            oldest = min(facts.values(), key=lambda f: f.created)
            del facts[oldest.key]
        facts[key] = Fact(key, clean, now, now + dt.timedelta(days=self.retention_days))

    def recall(self, user_id: str) -> dict[str, str]:
        self.purge_expired()
        return {k: f.value for k, f in self._store.get(user_id, {}).items()}

    def purge_expired(self) -> int:
        now, removed = self.clock(), 0
        for user_id in list(self._store):
            facts = self._store[user_id]
            for k in [k for k, f in facts.items() if f.expires <= now]:
                del facts[k]
                removed += 1
            if not facts:
                del self._store[user_id]
        return removed

    def export(self, user_id: str) -> list[dict]:
        """Everything kept about a user, for access requests."""
        return [{"key": f.key, "value": f.value, "created": f.created.isoformat(),
                 "expires": f.expires.isoformat()} for f in self._store.get(user_id, {}).values()]

    def forget(self, user_id: str) -> int:
        """Erase everything about a user. Returns the number of facts removed."""
        return len(self._store.pop(user_id, {}) or {})
