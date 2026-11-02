"""Contract enforcer: the independent execution layer for agents.

The model proposes; the contract defines obligations; this layer enforces.

  1. start_task      checks the contract is active and unexpired and binds the
                     task to its subject (the user and conversation it serves)
  2. approve_plan    validates the model's proposed plan ONCE per task: every
                     step's shape, its intent, and that the intent allows that
                     exact tool, model, memory store or delegate
  3. execute         runs each approved step AT MOST ONCE, only if the live
                     contract still allows it; tool-call and cost budgets are
                     shared by the whole delegation chain
  4. approve         a human approves a queued write THROUGH the enforcer,
                     which re-checks the live contract and records the approver
  5. delegation      a delegate runs under the narrowed intersection of the two
                     contracts and spends the parent's budget

The agent never holds the tool registry, gateway or memory: it only returns
plans. Every step writes four linked evidence records (provenance,
verification, authorization, execution) to a hash-chained ledger, including
denials. Authority is never read from natural language in prompts, documents
or tool output, so a conflicting instruction cannot widen it.

Reference implementation: in-process for teaching. In production run the same
checks as a separate service in front of tools, models and memory (for example
a sidecar or the API/MCP gateway) so agents have no network path around it,
and only that service may call ToolRegistry.approve().
"""
from __future__ import annotations

import datetime as dt
import hashlib
import itertools
import json
import math
from dataclasses import dataclass, field
from typing import Any, Callable

from .contracts import AgentContract, ContractError, ContractStore, narrow
from .evidence import EvidenceLedger
from .gateway import Gateway
from .memory import LongTermMemory, ShortTermMemory
from .tools import AgentIdentity, PendingApproval, ToolRegistry

REQUIRED_FIELDS = {"tool": {"tool": str, "args": dict}, "model": {"alias": str, "prompt": str},
                   "memory": {"op": str, "store": str}, "delegate": {"agent": str}}


def _hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


class Denied(PermissionError):
    def __init__(self, reason: str, rule: str):
        super().__init__(reason)
        self.reason, self.rule = reason, rule


@dataclass
class Budget:
    """Shared by a task and every task it delegates to."""
    tool_calls: int = 0
    cost_usd: float = 0.0


@dataclass
class Task:
    id: str
    agent: str
    contract: AgentContract          # effective (possibly narrowed) contract
    chain: list[str]                 # delegation chain, root first
    data_class: str
    source: dict
    budget: Budget
    subject: dict                    # user_id / conversation_id the task acts for
    approved: list[dict] = field(default_factory=list)   # [{"hash", "step", "used"}]
    plan_hash: str = ""
    pending: set[int] = field(default_factory=set)
    counter: Any = field(default_factory=lambda: itertools.count(1))


@dataclass
class StepResult:
    allowed: bool
    status: str                      # done | queued | denied | failed
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
                  allowed: bool, reason: str, rule: str, execution: dict, approver: str | None = None) -> None:
        c = task.contract.ref + (f" (narrowed from {task.contract.parent})" if task.contract.parent else "")
        L = self.ledger
        L.append(action_id, "provenance", task.agent, c,
                 {**provenance, "chain": task.chain, "task_source": task.source, "subject": task.subject})
        L.append(action_id, "verification", task.agent, c,
                 {"checks": [{"check": n, "passed": ok, "detail": d} for n, ok, d in checks]})
        auth = {"decision": "allow" if allowed else "deny", "reason": reason, "rule": rule,
                "authority": "contract", "contract_status": self.store.get(task.agent).status}
        if approver:
            auth["approver"] = approver
        L.append(action_id, "authorization", task.agent, c, auth)
        L.append(action_id, "execution", task.agent, c, execution)

    def _live_check(self, task: Task) -> None:
        """Contract state is re-read on every call, so revocation stops a running task and its delegates."""
        for agent in task.chain:
            ok, why = self.store.get(agent).is_usable(self.today())
            if not ok:
                raise Denied(why, "contract.status")

    # ---------- lifecycle ----------
    def start_task(self, agent: str, source: dict, data_class: str = "internal",
                   _contract: AgentContract | None = None, _chain: list[str] | None = None,
                   _budget: Budget | None = None) -> Task:
        contract = _contract or self.store.get(agent)
        subject = {"user_id": source.get("user_id"), "conversation_id": source.get("conversation_id")}
        task = Task(f"T{next(self._task_ids)}", agent, contract, (_chain or []) + [agent], data_class,
                    dict(source), _budget or Budget(), subject)
        aid = f"{task.id}-start"
        checks: list[tuple[str, bool, str]] = []
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

    def _validate_step(self, c: AgentContract, s: Any) -> None:
        if not isinstance(s, dict):
            raise Denied("step must be an object", "validation")
        t = s.get("type")
        if t not in REQUIRED_FIELDS:
            raise Denied(f"unknown step type {t!r}", "validation")
        for name, typ in REQUIRED_FIELDS[t].items():
            if not isinstance(s.get(name), typ):
                raise Denied(f"{t} step needs '{name}' as {typ.__name__}", "validation")
        intent = s.get("intent")
        rule = c.intents.get(intent)
        if rule is None:
            raise Denied(f"intent '{intent}' not in contract", "planning.allowed_intents")
        target = {"tool": ("tools", s.get("tool")), "model": ("models", s.get("alias")),
                  "memory": ("memory", s.get("store")), "delegate": ("delegates", s.get("agent"))}[t]
        if target[1] not in rule[target[0]]:
            raise Denied(f"intent '{intent}' does not allow {t} '{target[1]}'", "planning.intent_scope")
        if t == "memory" and (s["op"] not in {"read", "write"} or s["store"] not in {"short", "long"}):
            raise Denied("memory step needs op read|write and store short|long", "validation")
        if t == "memory" and s["store"] == "long" and not isinstance(s.get("key"), str):
            raise Denied("long-term memory step needs a 'key'", "validation")

    def approve_plan(self, task: Task, plan: list[dict], proposed_by: str = "model") -> StepResult:
        aid = f"{task.id}-plan"
        c = task.contract
        checks: list[tuple[str, bool, str]] = []
        prov = {"event": "plan_proposed", "proposed_by": proposed_by, "plan_hash": _hash(plan),
                "steps": len(plan) if isinstance(plan, list) else None}
        try:
            self._live_check(task)
            if task.plan_hash:
                raise Denied("this task already has an approved plan; start a new task", "planning.single_plan")
            if not isinstance(plan, list) or not plan:
                raise Denied("plan must be a non-empty list of steps", "validation")
            if len(plan) > c.max_plan_steps:
                raise Denied(f"plan has {len(plan)} steps; contract allows {c.max_plan_steps}", "planning.max_steps")
            checks.append(("plan_length", True, f"{len(plan)}/{c.max_plan_steps}"))
            for s in plan:
                self._validate_step(c, s)
            checks.append(("steps_match_intents", True, ",".join(sorted({s['intent'] for s in plan}))))
        except Denied as d:
            checks.append((d.rule, False, d.reason))
            self._evidence(task, aid, prov, checks, False, d.reason, d.rule, {"status": "plan_rejected"})
            return StepResult(False, "denied", d.reason, action_id=aid)
        task.approved = [{"hash": _hash(s), "step": s, "used": False} for s in plan]
        task.plan_hash = prov["plan_hash"]
        self._evidence(task, aid, prov, checks, True, "plan approved", "planning", {"status": "plan_approved"})
        return StepResult(True, "done", "plan approved", action_id=aid)

    # ---------- execution ----------
    def execute(self, task: Task, step: dict) -> StepResult:
        aid = f"{task.id}-{next(task.counter)}"
        prov = {"event": "step", "intent": step.get("intent") if isinstance(step, dict) else None,
                "type": step.get("type") if isinstance(step, dict) else None,
                "step_hash": _hash(step), "plan_hash": task.plan_hash}
        checks: list[tuple[str, bool, str]] = []
        try:
            self._live_check(task)
            checks.append(("contract_live", True, task.contract.ref))
            slot = next((a for a in task.approved if a["hash"] == prov["step_hash"] and not a["used"]), None)
            if slot is None:
                used = any(a["hash"] == prov["step_hash"] for a in task.approved)
                raise Denied("step already executed (replay)" if used else "step is not in the approved plan",
                             "planning.replay" if used else "planning.approved_plan")
            checks.append(("in_approved_plan_unused", True, prov["step_hash"]))
            run, more = getattr(self, f"_authorize_{step['type']}")(task, step)   # raises Denied
            checks += more
        except Denied as d:
            checks.append((d.rule, False, d.reason))
            self._evidence(task, aid, prov, checks, False, d.reason, d.rule, {"status": "denied"})
            return StepResult(False, "denied", d.reason, action_id=aid)
        except Exception as exc:    # malformed input found while authorizing: never "allowed"
            reason = f"invalid step: {type(exc).__name__}: {exc}"
            checks.append(("validation", False, reason))
            self._evidence(task, aid, prov, checks, False, reason, "validation", {"status": "denied"})
            return StepResult(False, "denied", reason, action_id=aid)
        slot["used"] = True
        try:
            status, output, after = run()
            checks += after
        except Exception as exc:    # authorized, then the tool/model/memory call itself failed
            self._evidence(task, aid, prov, checks, True, "allowed by contract", step["type"],
                           {"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
            return StepResult(True, "failed", str(exc), action_id=aid)
        exe = {"status": status, "output_hash": _hash(output.__dict__ if isinstance(output, PendingApproval) else
                                                      (output.id if isinstance(output, Task) else output)),
               "chain_tool_calls": task.budget.tool_calls, "chain_cost_usd": round(task.budget.cost_usd, 6)}
        if isinstance(output, PendingApproval):
            exe["approval_id"] = output.id
            task.pending.add(output.id)
        if isinstance(output, Task):
            exe["sub_task"] = output.id
        self._evidence(task, aid, prov, checks, True, "allowed by contract", step["type"], exe)
        return StepResult(True, status, "allowed", output, aid)

    def approve(self, task: Task, approval_id: int, approver: str) -> StepResult:
        """A human approves a queued write. Re-checks the live contract and records the approver."""
        aid = f"{task.id}-approve-{approval_id}"
        prov = {"event": "human_approval", "approval_id": approval_id}
        checks: list[tuple[str, bool, str]] = []
        try:
            if approval_id not in task.pending:
                raise Denied(f"approval {approval_id} does not belong to task {task.id}", "approval.task")
            self._live_check(task)
            if not approver:
                raise Denied("approver must be named", "approval.approver")
            checks.append(("contract_live", True, task.contract.ref))
        except Denied as d:
            checks.append((d.rule, False, d.reason))
            self._evidence(task, aid, prov, checks, False, d.reason, d.rule, {"status": "denied"}, approver)
            return StepResult(False, "denied", d.reason, action_id=aid)
        task.pending.discard(approval_id)
        try:
            out = self.registry.approve(approval_id, approver)
        except Exception as exc:
            self._evidence(task, aid, prov, checks, True, "approved by human", "approval",
                           {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}, approver)
            return StepResult(True, "failed", str(exc), action_id=aid)
        self._evidence(task, aid, prov, checks, True, "approved by human", "approval",
                       {"status": "done", "output_hash": _hash(out)}, approver)
        return StepResult(True, "done", "approved", out, aid)

    # ---------- per-type authorization (raise Denied; return a runner) ----------
    def _authorize_tool(self, task: Task, step: dict):
        c, name, args = task.contract, step["tool"], dict(step["args"])
        rule = c.tools.get(name)
        if rule is None:
            raise Denied(f"tool '{name}' not in contract", "tools")
        if task.budget.tool_calls >= c.max_tool_calls:
            raise Denied(f"tool-call limit {c.max_tool_calls} reached (shared across delegation)",
                         "execution.max_tool_calls")
        tool = self.registry.tools.get(name)
        if tool is None:
            raise Denied(f"tool '{name}' not registered", "tools.registry")
        if rule.mode == "read" and tool.kind == "write":
            raise Denied(f"contract allows '{name}' as read only", "tools.mode")
        amount_detail = "n/a"
        if rule.max_amount is not None:
            amount = args.get(rule.amount_arg)
            if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not math.isfinite(amount):
                raise Denied(f"'{rule.amount_arg}' must be a finite number for '{name}'", "tools.amount_type")
            if amount < 0:
                raise Denied(f"'{rule.amount_arg}' cannot be negative", "tools.amount_range")
            if amount > rule.max_amount:
                raise Denied(f"amount {amount} exceeds contract limit {rule.max_amount:g}", "tools.max_amount")
            amount_detail = f"{amount} <= {rule.max_amount:g}"
        identity = AgentIdentity(task.agent, {tool.scope}, set(c.tools))
        checks = [("tool_allowed", True, f"{name}:{rule.mode}"), ("amount_limit", True, amount_detail)]

        def run():
            task.budget.tool_calls += 1
            if tool.kind == "write" and rule.approval == "none":
                out = self.registry.execute_within_limits(identity, name, **args)   # L3, limits checked
            else:
                out = self.registry.call(identity, name, **args)                    # writes queue for a human
            return ("queued" if isinstance(out, PendingApproval) else "done"), out, []
        return run, checks

    def _authorize_model(self, task: Task, step: dict):
        c, alias = task.contract, step["alias"]
        if self.gateway is None:
            raise Denied("no gateway configured", "models")
        if alias not in c.models:
            raise Denied(f"model alias '{alias}' not in contract", "models")
        if task.data_class not in c.data_classes:
            raise Denied(f"data class '{task.data_class}' not allowed", "data_classes")
        if task.budget.cost_usd >= c.max_cost_usd:
            raise Denied(f"cost limit ${c.max_cost_usd} reached (shared across delegation)", "execution.max_cost")

        def run():
            out = self.gateway.complete(alias, step["prompt"], use_case=c.inventory_id)
            task.budget.cost_usd += out.cost_usd
            # The budget is checked before each call: the call that crosses the limit
            # completes and the next one is refused. Size limits with headroom.
            return "done", out.text, [("cost_after_call", True, f"${task.budget.cost_usd:.6f} of ${c.max_cost_usd}")]
        return run, [("model_allowed", True, f"{alias} for {task.data_class}")]

    def _authorize_memory(self, task: Task, step: dict):
        c, op, store = task.contract, step["op"], step["store"]
        for k in ("user_id", "conversation_id"):
            if k in step and step[k] != task.subject.get(k):
                raise Denied(f"memory {k} must be the task's own subject", "memory.subject")
        if store == "short":
            conv = task.subject.get("conversation_id")
            if not c.memory_short_term.get(op):
                raise Denied(f"short-term memory {op} not allowed", f"memory.short_term.{op}")
            if self.short_memory is None or not conv:
                raise Denied("no short-term memory or conversation for this task", "memory")
            if op == "write":
                if not isinstance(step.get("text"), str):
                    raise Denied("memory write needs 'text'", "validation")
                return (lambda: (self.short_memory.add(conv, step.get("role", "assistant"), step["text"])
                                 or ("done", "written", []))), [("memory_short_write", True, conv)]
            return (lambda: ("done", self.short_memory.as_text(conv), [])), [("memory_short_read", True, conv)]
        user, key = task.subject.get("user_id"), step["key"]
        allowed = c.memory_long_term_write if op == "write" else c.memory_long_term_read
        if key not in allowed:
            raise Denied(f"long-term memory {op} of '{key}' not allowed", f"memory.long_term.{op}")
        if self.long_memory is None or not user:
            raise Denied("no long-term memory or user for this task", "memory")
        if op == "write":
            if not isinstance(step.get("value"), str):
                raise Denied("memory write needs 'value'", "validation")
            return (lambda: (self.long_memory.remember(user, key, step["value"]) or ("done", "written", []))), \
                [("memory_long_write", True, key)]
        return (lambda: ("done", self.long_memory.recall(user).get(key), [])), [("memory_long_read", True, key)]

    def _authorize_delegate(self, task: Task, step: dict):
        child_agent = step["agent"]
        if child_agent in task.chain:
            raise Denied(f"delegation loop to '{child_agent}'", "delegation.loop")
        try:
            effective = narrow(task.contract, self.store.get(child_agent))
        except ContractError as exc:
            raise Denied(str(exc), "delegation") from exc
        if task.data_class not in effective.data_classes:
            raise Denied(f"delegate may not handle data class '{task.data_class}'", "delegation.data_class")

        def run():
            sub = self.start_task(child_agent,
                                  {"delegated_by": task.agent, "parent_task": task.id, **task.subject},
                                  task.data_class, _contract=effective, _chain=task.chain, _budget=task.budget)
            return "done", sub, []
        return run, [("delegate_allowed", True, child_agent),
                     ("narrowed", True, f"tools={sorted(effective.tools)} depth={effective.max_delegation_depth}")]

    # ---------- convenience ----------
    def run(self, agent: str, propose: Callable[[dict], list[dict]], task_input: dict,
            source: dict, data_class: str = "internal") -> tuple[Task, list[StepResult]]:
        """Ask the agent for a plan, approve it, then execute each approved step once."""
        task = self.start_task(agent, source, data_class)
        plan = propose(task_input)
        verdict = self.approve_plan(task, plan)
        if not verdict.allowed:
            return task, [verdict]
        return task, [self.execute(task, s) for s in plan]
