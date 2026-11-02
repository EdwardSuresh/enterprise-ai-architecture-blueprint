"""Agent contracts: one executable definition of what an agent may do.

A contract covers the whole stack, not one checkpoint:

  planning    which intents a plan may contain and how many steps
  models      which model aliases it may call, for which data classes
  memory      which short-term and long-term memory it may read or write
  tools       which tools, read or write, with approval rules and limits
  delegation  which agents it may hand work to, and how deep
  execution   per-task limits on cost, tool calls and rate

Contracts are data (YAML in contracts/), approved through the ARB, versioned,
and can be revoked. Delegation only ever NARROWS authority: the effective
contract of a delegate is the intersection of its own contract and its
parent's, with the tighter of every limit (see narrow()).
"""
from __future__ import annotations

import copy
import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

from .config import load_yaml, repo_root

AUTONOMY = ["L0", "L1", "L2", "L3", "L4"]


class ContractError(ValueError):
    pass


@dataclass
class ToolRule:
    name: str
    mode: str                      # read | write
    approval: str = "none"         # none | human
    max_amount: float | None = None


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
    allowed_intents: set[str]
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
            tools = {name: ToolRule(name, r["mode"], r.get("approval", "none"), r.get("max_amount"))
                     for name, r in (d.get("tools") or {}).items()}
            until = d.get("valid_until")
            c = cls(
                contract_id=d["contract_id"], version=str(d["version"]), agent=d["agent"],
                inventory_id=d["inventory_id"], owner=d["owner"], status=d.get("status", "active"),
                valid_until=dt.date.fromisoformat(str(until)) if until else None,
                autonomy_level=d["autonomy_level"],
                allowed_intents=set(plan["allowed_intents"]), max_plan_steps=int(plan["max_steps"]),
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
        except KeyError as exc:
            raise ContractError(f"contract missing field {exc}") from exc
        if c.autonomy_level not in AUTONOMY:
            raise ContractError(f"{c.ref}: autonomy_level must be one of {AUTONOMY}")
        for t in c.tools.values():
            if t.mode not in {"read", "write"} or t.approval not in {"none", "human"}:
                raise ContractError(f"{c.ref}: bad rule for tool {t.name}")
            if t.mode == "write" and AUTONOMY.index(c.autonomy_level) <= 2 and t.approval != "human":
                raise ContractError(f"{c.ref}: write tool {t.name} needs human approval at {c.autonomy_level}")
        return c

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
    eff.allowed_intents = child.allowed_intents & parent.allowed_intents
    eff.max_plan_steps = min(child.max_plan_steps, parent.max_plan_steps)
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
        approval = "human" if "human" in (rule.approval, p.approval) else "none"
        amounts = [a for a in (rule.max_amount, p.max_amount) if a is not None]
        tools[name] = ToolRule(name, mode, approval, min(amounts) if amounts else None)
    eff.tools = tools
    eff.delegates = child.delegates & parent.delegates
    eff.max_delegation_depth = min(child.max_delegation_depth, parent.max_delegation_depth - 1)
    eff.autonomy_level = AUTONOMY[min(AUTONOMY.index(child.autonomy_level), AUTONOMY.index(parent.autonomy_level))]
    eff.max_cost_usd = min(child.max_cost_usd, parent.max_cost_usd)
    eff.max_tool_calls = min(child.max_tool_calls, parent.max_tool_calls)
    eff.parent = parent.ref
    return eff


class ContractStore:
    """Loads and holds contracts; revocation takes effect immediately."""

    def __init__(self, contracts: dict[str, AgentContract]):
        self.by_agent = contracts

    @classmethod
    def load_dir(cls, folder: str = "contracts") -> "ContractStore":
        root = repo_root() / folder
        found = {}
        for f in sorted(root.glob("*.yaml")):
            c = AgentContract.load(f)
            found[c.agent] = c
        return cls(found)

    def get(self, agent: str) -> AgentContract:
        if agent not in self.by_agent:
            raise ContractError(f"no contract for agent '{agent}'")
        return self.by_agent[agent]

    def revoke(self, agent: str, reason: str = "") -> None:
        self.get(agent).status = "revoked"
