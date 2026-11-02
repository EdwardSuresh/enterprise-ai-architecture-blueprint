"""Agent contracts: one executable definition of what an agent may do.

A contract covers the whole stack, not one checkpoint:

  planning    which intents a plan may contain, and for each intent exactly
              which tools, models, memory stores or delegates it may use
  models      which model aliases it may call, for which data classes
  memory      which short-term and long-term memory it may read or write
  tools       which tools, read or write, with approval rules and amount limits
  delegation  which agents it may hand work to, and how deep
  execution   per-task limits on cost and tool calls, shared across delegation

Contracts are data (YAML in contracts/), approved through the ARB, versioned,
expiring and revocable. Delegation only ever NARROWS authority: the effective
contract of a delegate is the intersection of its own contract and its
parent's, with the tighter of every limit (see narrow()).
"""
from __future__ import annotations

import copy
import datetime as dt
import math
from dataclasses import dataclass, field
from pathlib import Path

from .config import load_yaml, repo_root

AUTONOMY = ["L0", "L1", "L2", "L3", "L4"]
INTENT_KEYS = ("tools", "models", "memory", "delegates")


class ContractError(ValueError):
    pass


@dataclass
class ToolRule:
    name: str
    mode: str                      # read | write
    approval: str = "none"         # none | human
    max_amount: float | None = None
    amount_arg: str = "amount"     # which argument the limit applies to


@dataclass
class AgentContract:
    contract_id: str
    version: str
    agent: str
    inventory_id: str
    owner: str
    status: str                    # active | revoked
    valid_until: dt.date | None
    autonomy_level: str
    intents: dict[str, dict[str, set[str]]]   # intent -> {tools|models|memory|delegates: set}
    max_plan_steps: int
    models: set[str]
    data_classes: set[str]
    memory_short_term: dict
    memory_long_term_read: set[str]
    memory_long_term_write: set[str]
    tools: dict[str, ToolRule]
    delegates: set[str]
    max_delegation_depth: int
    max_cost_usd: float
    max_tool_calls: int
    approved_by: str = ""
    parent: str | None = None      # set when this is a narrowed (delegated) contract
    source: dict = field(default_factory=dict, repr=False)

    @property
    def ref(self) -> str:
        return f"{self.contract_id}@{self.version}"

    @property
    def allowed_intents(self) -> set[str]:
        return set(self.intents)

    def is_usable(self, today: dt.date | None = None) -> tuple[bool, str]:
        today = today or dt.date.today()
        if self.status != "active":
            return False, f"contract {self.ref} is {self.status}"
        if self.valid_until and today > self.valid_until:
            return False, f"contract {self.ref} expired on {self.valid_until}"
        return True, "ok"

    @classmethod
    def from_dict(cls, d: dict) -> "AgentContract":
        try:
            plan, mem, dele, exe = d["planning"], d.get("memory", {}), d.get("delegation", {}), d["execution"]
            lt = mem.get("long_term", {}) or {}
            tools = {}
            for name, r in (d.get("tools") or {}).items():
                tools[name] = ToolRule(name, r["mode"], r.get("approval", "none"),
                                       None if r.get("max_amount") is None else float(r["max_amount"]),
                                       r.get("amount_arg", "amount"))
            intents = {}
            for name, rule in (plan["intents"] or {}).items():
                rule = rule or {}
                unknown = set(rule) - set(INTENT_KEYS)
                if unknown:
                    raise ContractError(f"intent '{name}' has unknown keys {sorted(unknown)}")
                intents[name] = {k: set(rule.get(k, [])) for k in INTENT_KEYS}
            until = d.get("valid_until")
            c = cls(
                contract_id=d["contract_id"], version=str(d["version"]), agent=d["agent"],
                inventory_id=d["inventory_id"], owner=d["owner"], status=d.get("status", "active"),
                valid_until=dt.date.fromisoformat(str(until)) if until else None,
                autonomy_level=d["autonomy_level"], intents=intents,
                max_plan_steps=int(plan["max_steps"]),
                models=set(d["models"]), data_classes=set(d["data_classes"]),
                memory_short_term=dict(mem.get("short_term", {"read": False, "write": False})),
                memory_long_term_read=set(lt.get("read_keys", [])),
                memory_long_term_write=set(lt.get("write_keys", [])),
                tools=tools, delegates=set(dele.get("allowed_delegates", [])),
                max_delegation_depth=int(dele.get("max_depth", 0)),
                max_cost_usd=float(exe["max_cost_usd_per_task"]),
                max_tool_calls=int(exe["max_tool_calls_per_task"]),
                approved_by=d.get("approved_by", ""), source=d,
            )
        except (KeyError, TypeError) as exc:
            raise ContractError(f"contract missing or malformed field: {exc}") from exc
        c.validate()
        return c

    def validate(self) -> None:
        r = self.ref
        if self.autonomy_level not in AUTONOMY:
            raise ContractError(f"{r}: autonomy_level must be one of {AUTONOMY}")
        if self.max_plan_steps < 1 or self.max_delegation_depth < 0 or self.max_tool_calls < 0:
            raise ContractError(f"{r}: step, depth and tool-call limits must be non-negative (steps >= 1)")
        if not (math.isfinite(self.max_cost_usd) and self.max_cost_usd >= 0):
            raise ContractError(f"{r}: max_cost_usd_per_task must be a non-negative number")
        for t in self.tools.values():
            if t.mode not in {"read", "write"} or t.approval not in {"none", "human"}:
                raise ContractError(f"{r}: bad rule for tool {t.name}")
            if t.mode == "read" and t.approval == "human":
                raise ContractError(f"{r}: read tool {t.name} cannot require approval; make it a write or remove it")
            if t.max_amount is not None and not (math.isfinite(t.max_amount) and t.max_amount > 0):
                raise ContractError(f"{r}: max_amount for {t.name} must be a positive number")
            if t.mode == "write" and AUTONOMY.index(self.autonomy_level) <= 2 and t.approval != "human":
                raise ContractError(f"{r}: write tool {t.name} needs human approval at {self.autonomy_level}")
        for name, rule in self.intents.items():
            if not any(rule[k] for k in INTENT_KEYS):
                raise ContractError(f"{r}: intent '{name}' allows nothing; list its tools, models, memory or delegates")
            if not rule["tools"] <= set(self.tools):
                raise ContractError(f"{r}: intent '{name}' names tools not in the contract")
            if not rule["models"] <= self.models:
                raise ContractError(f"{r}: intent '{name}' names models not in the contract")
            if not rule["memory"] <= {"short", "long"}:
                raise ContractError(f"{r}: intent '{name}' memory must be short and/or long")
            if not rule["delegates"] <= self.delegates:
                raise ContractError(f"{r}: intent '{name}' names delegates not in the contract")

    @classmethod
    def load(cls, path: str | Path) -> "AgentContract":
        return cls.from_dict(load_yaml(path))


def narrow(parent: AgentContract, child: AgentContract) -> AgentContract:
    """Effective contract for `child` when delegated by `parent`.

    Every permission is the intersection and every limit is the tighter value,
    so a delegate can never gain authority its parent does not have.
    """
    if child.agent not in parent.delegates:
        raise ContractError(f"{parent.agent} may not delegate to {child.agent}")
    if parent.max_delegation_depth < 1:
        raise ContractError(f"{parent.agent} has no delegation depth left")
    eff = copy.copy(child)
    eff.models = child.models & parent.models
    eff.data_classes = child.data_classes & parent.data_classes
    eff.memory_short_term = {k: bool(child.memory_short_term.get(k)) and bool(parent.memory_short_term.get(k))
                             for k in ("read", "write")}
    eff.memory_long_term_read = child.memory_long_term_read & parent.memory_long_term_read
    eff.memory_long_term_write = child.memory_long_term_write & parent.memory_long_term_write
    tools = {}
    for name, rule in child.tools.items():
        p = parent.tools.get(name)
        if p is None:
            continue
        mode = "write" if (rule.mode == "write" and p.mode == "write") else "read"
        approval = "human" if mode == "write" and "human" in (rule.approval, p.approval) else "none"
        amounts = [a for a in (rule.max_amount, p.max_amount) if a is not None]
        tools[name] = ToolRule(name, mode, approval, min(amounts) if amounts else None, rule.amount_arg)
    eff.tools = tools
    eff.delegates = child.delegates & parent.delegates
    intents = {}
    for name in set(child.intents) & set(parent.intents):
        rule = {k: child.intents[name][k] & parent.intents[name][k] for k in INTENT_KEYS}
        rule["tools"] &= set(tools)
        rule["models"] &= eff.models
        rule["delegates"] &= eff.delegates
        if any(rule[k] for k in INTENT_KEYS):
            intents[name] = rule
    eff.intents = intents
    eff.max_plan_steps = min(child.max_plan_steps, parent.max_plan_steps)
    eff.max_delegation_depth = min(child.max_delegation_depth, parent.max_delegation_depth - 1)
    eff.autonomy_level = AUTONOMY[min(AUTONOMY.index(child.autonomy_level), AUTONOMY.index(parent.autonomy_level))]
    eff.max_cost_usd = min(child.max_cost_usd, parent.max_cost_usd)
    eff.max_tool_calls = min(child.max_tool_calls, parent.max_tool_calls)
    eff.parent = parent.ref
    return eff


class ContractStore:
    """Holds the contracts the runtime may use; revocation takes effect immediately."""

    def __init__(self, contracts: dict[str, AgentContract]):
        self.by_agent = contracts

    @classmethod
    def _load(cls, files: list[Path]) -> "ContractStore":
        found: dict[str, AgentContract] = {}
        for f in files:
            c = AgentContract.load(f)
            if c.agent in found:
                raise ContractError(f"two contracts for agent '{c.agent}': {found[c.agent].ref} and {c.ref}")
            found[c.agent] = c
        return cls(found)

    @classmethod
    def load_dir(cls, folder: str = "contracts") -> "ContractStore":
        return cls._load(sorted((repo_root() / folder).glob("*.yaml")))

    @classmethod
    def from_inventory(cls, inventory: str = "01-governance/ai-inventory.yaml") -> "ContractStore":
        """Load only contracts that a non-retired inventory entry references, so the
        runtime uses exactly the contracts the policy gate has checked."""
        refs = [repo_root() / ref for s in load_yaml(inventory).get("systems", [])
                if s.get("status") != "retired" for ref in (s.get("contracts") or [])]
        return cls._load(refs)

    def get(self, agent: str) -> AgentContract:
        if agent not in self.by_agent:
            raise ContractError(f"no contract for agent '{agent}'")
        return self.by_agent[agent]

    def revoke(self, agent: str, reason: str = "") -> None:
        self.get(agent).status = "revoked"
