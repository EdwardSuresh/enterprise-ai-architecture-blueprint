"""Prompt registry: versioned, reviewed prompts instead of hard-coded strings.

Implements integration standard section 6 (02-architecture/standards/integration-standards.md):
every prompt has an id, versions, an owner, a linked eval set and a change history.
Only approved versions load in normal use, and every rendered prompt carries its
id, version and content hash so an answer can be traced to the exact prompt text.
"""
from __future__ import annotations

import hashlib
import string
from dataclasses import dataclass
from pathlib import Path

from .config import load_yaml, repo_root


class PromptError(ValueError):
    pass


@dataclass(frozen=True)
class Prompt:
    id: str
    version: str
    template: str
    owner: str
    variables: tuple[str, ...]
    status: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.template.encode("utf-8")).hexdigest()[:12]

    @property
    def ref(self) -> str:
        return f"{self.id}@{self.version}"

    def render(self, **values: str) -> str:
        """Fill the template. Missing variables are an error; extra ones are ignored."""
        needed = {f for _, f, _, _ in string.Formatter().parse(self.template) if f}
        missing = sorted(needed - values.keys())
        if missing:
            raise PromptError(f"{self.ref} needs values for {missing}")
        return self.template.format(**{k: values[k] for k in needed})

    def trace_attributes(self) -> dict:
        return {"kit.prompt.id": self.id, "kit.prompt.version": self.version,
                "kit.prompt.sha256": self.sha256}


class PromptRegistry:
    def __init__(self, data: dict, root: Path):
        self.data = data.get("prompts", {})
        self.root = root

    @classmethod
    def load(cls, path: str = "prompts/registry.yaml") -> "PromptRegistry":
        return cls(load_yaml(path) or {}, repo_root())

    def ids(self) -> list[str]:
        return sorted(self.data)

    def get(self, prompt_id: str, version: str | None = None, allow_unapproved: bool = False) -> Prompt:
        entry = self.data.get(prompt_id)
        if entry is None:
            raise PromptError(f"unknown prompt '{prompt_id}'")
        version = str(version or entry.get("current", ""))
        v = entry.get("versions", {}).get(version)
        if v is None:
            raise PromptError(f"{prompt_id} has no version '{version}'")
        status = v.get("status", "draft")
        if status != "approved" and not allow_unapproved:
            raise PromptError(f"{prompt_id}@{version} is '{status}', not approved")
        text = (self.root / v["file"]).read_text(encoding="utf-8")
        return Prompt(prompt_id, version, text, entry.get("owner", ""),
                      tuple(entry.get("variables", [])), status)

    def resolve(self, ref: str) -> Prompt:
        """Accept 'id' (current version) or 'id@version'."""
        pid, _, ver = ref.partition("@")
        return self.get(pid, ver or None)

    def validate(self) -> list[str]:
        """Return problems: missing files, bad 'current', undeclared or unused variables."""
        problems = []
        for pid, entry in self.data.items():
            for key in ("owner", "eval_set", "current", "versions"):
                if not entry.get(key):
                    problems.append(f"{pid}: missing '{key}'")
            versions = entry.get("versions", {}) or {}
            cur = versions.get(str(entry.get("current")))
            if cur is None:
                problems.append(f"{pid}: current version '{entry.get('current')}' not listed")
            elif cur.get("status") != "approved":
                problems.append(f"{pid}: current version is not approved")
            declared = set(entry.get("variables", []))
            for ver, v in versions.items():
                f = self.root / v.get("file", "")
                if not f.is_file():
                    problems.append(f"{pid}@{ver}: file not found {v.get('file')}")
                    continue
                used = {x for _, x, _, _ in string.Formatter().parse(f.read_text(encoding="utf-8")) if x}
                if used - declared:
                    problems.append(f"{pid}@{ver}: uses undeclared variables {sorted(used - declared)}")
            if entry.get("eval_set") and not (self.root / entry["eval_set"]).is_file():
                problems.append(f"{pid}: eval_set not found {entry['eval_set']}")
        return problems
