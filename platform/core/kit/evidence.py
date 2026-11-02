"""Evidence ledger: four distinct, linked, tamper-evident records per action.

Provenance, verification, authorization and execution are different facts
and need different evidence:

  provenance     where the input and context came from (source, prompt id/hash,
                 retrieved document ids, the plan that proposed the action)
  verification   which checks ran and what they found (guardrails, schema,
                 grounding, limit checks)
  authorization  who or what allowed or denied it, under which contract
                 version and rule, and any human approver
  execution      what actually happened (result hash, error, cost)

Each record carries the action id that links the four, and the hash of the
previous record, so any edit, deletion or reordering breaks the chain and is
detected by verify().

A chain alone cannot show that records were cut off the END. So publish an
anchor (record count + head hash, from anchor()) somewhere the agent runtime
cannot write - append-only (WORM) storage, a separate log, or a periodic
signed checkpoint - and pass it to verify(anchor=...).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

KINDS = ("provenance", "verification", "authorization", "execution")
GENESIS = "0" * 64


def _digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode("utf-8")).hexdigest()


@dataclass
class EvidenceRecord:
    seq: int
    action_id: str
    kind: str
    agent: str
    contract: str          # contract_id@version
    data: dict
    at: str
    prev_hash: str
    hash: str = ""

    def body(self) -> dict:
        d = asdict(self)
        d.pop("hash")
        return d


@dataclass
class EvidenceLedger:
    records: list[EvidenceRecord] = field(default_factory=list)

    def append(self, action_id: str, kind: str, agent: str, contract: str, data: dict) -> EvidenceRecord:
        if kind not in KINDS:
            raise ValueError(f"evidence kind must be one of {KINDS}")
        prev = self.records[-1].hash if self.records else GENESIS
        rec = EvidenceRecord(len(self.records), action_id, kind, agent, contract, dict(data),
                             dt.datetime.now(dt.timezone.utc).isoformat(), prev)
        rec.hash = _digest(rec.body())
        self.records.append(rec)
        return rec

    def for_action(self, action_id: str) -> dict[str, list[EvidenceRecord]]:
        out: dict[str, list[EvidenceRecord]] = {k: [] for k in KINDS}
        for r in self.records:
            if r.action_id == action_id:
                out[r.kind].append(r)
        return out

    def anchor(self) -> dict:
        """Count and head hash to store outside the ledger (detects truncation)."""
        return {"count": len(self.records), "head": self.records[-1].hash if self.records else GENESIS}

    def verify(self, anchor: dict | None = None) -> tuple[bool, str]:
        """Recompute the chain; with an anchor, also detect records removed from the end."""
        prev = GENESIS
        for i, r in enumerate(self.records):
            if r.seq != i:
                return False, f"record {i}: sequence broken"
            if r.prev_hash != prev:
                return False, f"record {i}: previous-hash mismatch (deleted or reordered record)"
            if _digest(r.body()) != r.hash:
                return False, f"record {i}: content changed after it was written"
            prev = r.hash
        if anchor is not None:
            if len(self.records) < anchor["count"]:
                return False, f"ledger has {len(self.records)} records; anchor says {anchor['count']} (truncated)"
            if anchor["count"] and self.records[anchor["count"] - 1].hash != anchor["head"]:
                return False, "record at the anchored position does not match the anchor"
        return True, f"{len(self.records)} records verified" + (" against anchor" if anchor else "")

    def export_jsonl(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as fh:
            for r in self.records:
                fh.write(json.dumps(asdict(r), default=str) + "\n")
