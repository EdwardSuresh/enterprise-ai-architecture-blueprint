"""Contract enforcer: the independent execution layer for agents.

The model proposes; the contract defines obligations; this layer enforces.

  1. start_task      checks the agent's contract is active and unexpired
  2. approve_plan    the model's proposed plan is checked against the contract
                     (allowed intents, step count) BEFORE anything runs
  3. execute         runs one step only if it is in the approved plan and the
                     contract allows it right now: tool, model, memory or
                     delegation, with per-task limits on cost and tool calls
  4. delegate        starts a sub-task whose contract is the narrowed
                     intersection of parent and child (authority only shrinks)

The agent never holds the tool registry, gateway or memory: it only returns
plans. Every step writes four linked evidence records (provenance,
verification, authorization, execution) to a hash-chained ledger, including
denials. Authority is never read from natural language in prompts, documents
or tool output, so a conflicting instruction cannot widen it.

Reference implementation: in-process for teaching. In production run the same
checks as a separate service in front of tools, models and memory (for example
a sidecar or the API/MCP gateway) so agents have no network path around it.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import itertools
import json
from dataclasses import dataclass, field
from typing import Any, Callable

from .contracts import AgentContract, ContractError, ContractStore, narrow
from .evidence import EvidenceLedger
from .gateway import Gateway
from .memory import LongTermMemory, ShortTermMemory
from .tools import AgentIdentity, PendingApproval, ToolRegistry

STEP_TYPES = {"tool", "model", "memory", "delegate"}


def _hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


class Denied(PermissionError):
    def __init__(self, reason: str, rule: str):
        super().__init__(reason)
        self.reason, self.rule = reason, rule


@dataclass
class Task:
    id: str
    agent: str
    contract: AgentContract          # effective (possibly narrowed) contract
    chain: list[str]                 # delegation chain, root first
    data_class: str
    source: dict
    approved_steps: dict[str, dict] = field(default_factory=dict)
    plan_hash: str = ""
    tool_calls: int = 0
    cost_usd: float = 0.0
    counter: Any = field(default_factory=lambda: itertools.count(1))


@dataclass
class StepResult:
    allowed: bool
    status: str                      # done | queued | denied
    reason: str
    output: Any = None
    action_id: str = ""


class ContractEnforcer:
    def __init__(self, store: ContractStore, registry: ToolRegistry, gateway: Gateway | None = None,
                 short_memory: ShortTermMemory | None = None, long_memory: LongTermMemory | None = None,
                 ledger: EvidenceLedger | None = None, today: Callable[[], dt.date] = dt.date.today):
        self.store, self.registry, self.gateway = store, registry, gateway
        self.short_memory, self.long_memory = short_memory, long_memory
        self.ledger = ledger or EvidenceLedger()
        self.today = today
        self._task_ids = itertools.count(1)

    # ---------- evidence ----------
    def _evidence(self, task: Task, action_id: str, provenance: dict, checks: list[tuple[str, bool, str]],
                  allowed: bool, reason: str, rule: str, execution: dict) -> None:
        c = task.contract.ref + (f" (narrowed from {task.contract.parent})" if task.contract.parent else "")
        L = self.ledger
        L.append(action_id, "provenance", task.agent, c, {**provenance, "chain": task.chain, "task_source": task.source})
        L.append(action_id, "verification", task.agent, c,
                 {"checks": [{"check": n, "passed": ok, "detail": d} for n, ok, d in checks]})
        L.append(action_id, "authorization", task.agent, c,
                 {"decision": "allow" if allowed else "deny", "reason": reason, "rule": rule,
                  "authority": "contract", "contract_status": task.contract.status})
        L.append(action_id, "execution", task.agent, c, execution)

    def _live_check(self, task: Task) -> None:
        """Contract state is re-read on every call, so revocation stops a running task."""
        for agent in task.chain:
            ok, why = self.store.get(agent).is_usable(self.today())
            if not ok:
                raise Denied(why, "contract.status")

    # ---------- lifecycle ----------
    def start_task(self, agent: str, source: dict, data_class: str = "internal",
                   _contract: AgentContract | None = None, _chain: list[str] | None = None) -> Task:
        contract = _contract or self.store.get(agent)
        task = Task(f"T{next(self._task_ids)}", agent, contract, (_chain or []) + [agent], data_class, source)
        aid = f"{task.id}-start"
        checks = []
        try:
            self._live_check(task)
            checks.append(("contract_usable", True, contract.ref))
            if data_class not in contract.data_classes:
                raise Denied(f"data class '{data_class}' not allowed by {contract.ref}", "data_classes")
            checks.append(("data_class", True, data_class))
        except Denied as d:
            checks.append((d.rule, False, d.reason))
            self._evidence(task, aid, {"event": "start_task"}, checks, False, d.reason, d.rule, {"status": "denied"})
            raise
        self._evidence(task, aid, {"event": "start_task"}, checks, True, "task started", "contract", {"status": "started"})
        return task

    def approve_plan(self, task: Task, plan: list[dict], proposed_by: str = "model") -> StepResult:
        aid = f"{task.id}-plan"
        c = task.contract
        checks: list[tuple[str, bool, str]] = []
        prov = {"event": "plan_proposed", "proposed_by": proposed_by, "plan_hash": _hash(plan), "steps": len(plan)}
        try:
            self._live_check(task)
            if len(plan) > c.max_plan_steps:
                raise Denied(f"plan has {len(plan)} steps; contract allows {c.max_plan_steps}", "planning.max_steps")
            checks.append(("plan_length", True, f"{len(plan)}/{c.max_plan_steps}"))
            for s in plan:
                if s.get("type") not in STEP_TYPES:
                    raise Denied(f"unknown step type {s.get('type')}", "planning.step_type")
                if s.get("intent") not in c.allowed_intents:
                    raise Denied(f"intent '{s.get('intent')}' not in contract", "planning.allowed_intents")
            checks.append(("intents_allowed", True, ",".join(sorted({s['intent'] for s in plan}))))
        except Denied as d:
            checks.append((d.rule, False, d.reason))
            self._evidence(task, aid, prov, checks, False, d.reason, d.rule, {"status": "plan_rejected"})
            return StepResult(False, "denied", d.reason, action_id=aid)
        task.approved_steps = {_hash(s): s for s in plan}
        task.plan_hash = prov["plan_hash"]
        self._evidence(task, aid, prov, checks, True, "plan approved", "planning", {"status": "plan_approved"})
        return StepResult(True, "done", "plan approved", action_id=aid)

    # ---------- execution ----------
    def execute(self, task: Task, step: dict) -> StepResult:
        aid = f"{task.id}-{next(task.counter)}"
        prov = {"event": "step", "intent": step.get("intent"), "type": step.get("type"),
                "step_hash": _hash(step), "plan_hash": task.plan_hash}
        checks: list[tuple[str, bool, str]] = []
        try:
            self._live_check(task)
            checks.append(("contract_live", True, task.contract.ref))
            if _hash(step) not in task.approved_steps:
                raise Denied("step is not in the approved plan", "planning.approved_plan")
            checks.append(("in_approved_plan", True, prov["step_hash"]))
            handler = getattr(self, f"_do_{step['type']}")
            status, output, more = handler(task, step)
            checks += more
        except Denied as d:
            checks.append((d.rule, False, d.reason))
            self._evidence(task, aid, prov, checks, False, d.reason, d.rule, {"status": "denied"})
            return StepResult(False, "denied", d.reason, action_id=aid)
        except Exception as exc:  # execution failed after authorization
            self._evidence(task, aid, prov, checks, True, "authorized", step.get("type", ""),
                           {"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
            return StepResult(True, "failed", str(exc), action_id=aid)
        out_hash = _hash(output.__dict__ if isinstance(output, PendingApproval) else output)
        exe = {"status": status, "output_hash": out_hash, "task_cost_usd": round(task.cost_usd, 6),
               "task_tool_calls": task.tool_calls}
        if isinstance(output, PendingApproval):
            exe["approval_id"] = output.id
        self._evidence(task, aid, prov, checks, True, "allowed by contract", step["type"], exe)
        return StepResult(True, status, "allowed", output, aid)

    def _do_tool(self, task: Task, step: dict):
        c, name, args = task.contract, step["tool"], dict(step.get("args", {}))
        rule = c.tools.get(name)
        if rule is None:
            raise Denied(f"tool '{name}' not in contract", "tools")
        if task.tool_calls >= c.max_tool_calls:
            raise Denied(f"tool-call limit {c.max_tool_calls} reached", "execution.max_tool_calls")
        tool = self.registry.tools.get(name)
        if tool is None:
            raise Denied(f"tool '{name}' not registered", "tools.registry")
        if rule.mode == "read" and tool.kind == "write":
            raise Denied(f"contract allows '{name}' as read only", "tools.mode")
        amount = args.get("amount")
        if rule.max_amount is not None and amount is not None and float(amount) > rule.max_amount:
            raise Denied(f"amount {amount} exceeds contract limit {rule.max_amount}", "tools.max_amount")
        identity = AgentIdentity(task.agent, {tool.scope}, set(c.tools))
        task.tool_calls += 1
        if tool.kind == "write" and rule.approval == "none":
            out = self.registry.execute_within_limits(identity, name, **args)   # L3, limits checked above
        else:
            out = self.registry.call(identity, name, **args)                    # writes queue for a human
        checks = [("tool_allowed", True, f"{name}:{rule.mode}"),
                  ("amount_limit", True, f"{amount} <= {rule.max_amount}" if amount is not None else "n/a")]
        status = "queued" if isinstance(out, PendingApproval) else "done"
        if rule.approval == "human" and status != "queued":
            raise Denied(f"'{name}' requires human approval", "tools.approval")
        return status, out, checks

    def _do_model(self, task: Task, step: dict):
        c, alias = task.contract, step["alias"]
        if self.gateway is None:
            raise Denied("no gateway configured", "models")
        if alias not in c.models:
            raise Denied(f"model alias '{alias}' not in contract", "models")
        if task.cost_usd >= c.max_cost_usd:
            raise Denied(f"cost limit ${c.max_cost_usd} reached", "execution.max_cost")
        out = self.gateway.complete(alias, step["prompt"], use_case=c.inventory_id)
        task.cost_usd += out.cost_usd
        return "done", out.text, [("model_allowed", True, alias),
                                  ("cost", task.cost_usd <= c.max_cost_usd, f"${task.cost_usd:.6f}")]

    def _do_memory(self, task: Task, step: dict):
        c, op, store = task.contract, step["op"], step.get("store", "short")
        if store == "short":
            if not c.memory_short_term.get(op):
                raise Denied(f"short-term memory {op} not allowed", f"memory.short_term.{op}")
            if self.short_memory is None:
                raise Denied("no short-term memory configured", "memory")
            if op == "write":
                self.short_memory.add(step["conversation_id"], step.get("role", "assistant"), step["text"])
                return "done", "written", [("memory_short_write", True, "")]
            return "done", self.short_memory.as_text(step["conversation_id"]), [("memory_short_read", True, "")]
        key = step["key"]
        allowed = c.memory_long_term_write if op == "write" else c.memory_long_term_read
        if key not in allowed:
            raise Denied(f"long-term memory {op} of '{key}' not allowed", f"memory.long_term.{op}")
        if self.long_memory is None:
            raise Denied("no long-term memory configured", "memory")
        if op == "write":
            self.long_memory.remember(step["user_id"], key, step["value"])
            return "done", "written", [("memory_long_write", True, key)]
        return "done", self.long_memory.recall(step["user_id"]).get(key), [("memory_long_read", True, key)]

    def _do_delegate(self, task: Task, step: dict):
        child_agent = step["agent"]
        if child_agent in task.chain:
            raise Denied(f"delegation loop to '{child_agent}'", "delegation.loop")
        try:
            child = self.store.get(child_agent)
            effective = narrow(task.contract, child)
        except ContractError as exc:
            raise Denied(str(exc), "delegation") from exc
        sub = self.start_task(child_agent, {"delegated_by": task.agent, "parent_task": task.id},
                              task.data_class, _contract=effective, _chain=task.chain)
        return "done", sub, [("delegate_allowed", True, child_agent),
                             ("narrowed", True, f"tools={sorted(effective.tools)} depth={effective.max_delegation_depth}")]

    # ---------- convenience ----------
    def run(self, agent: str, propose: Callable[[dict], list[dict]], task_input: dict,
            source: dict, data_class: str = "internal") -> tuple[Task, list[StepResult]]:
        """Ask the agent for a plan, approve it, then execute each approved step."""
        task = self.start_task(agent, source, data_class)
        plan = propose(task_input)
        verdict = self.approve_plan(task, plan)
        if not verdict.allowed:
            return task, [verdict]
        return task, [self.execute(task, s) for s in plan]
