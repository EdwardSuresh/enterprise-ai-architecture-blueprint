"""Tool registry, agent identities and the human approval queue.

- Every agent has its own non-human identity with scopes (least privilege).
- Every tool is on an allow-list per agent.
- Read tools run immediately. Write tools go to an approval queue and run only
  when a named human approves. This implements autonomy level L2.
The same contract applies when tools are served by MCP servers.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Any, Callable


class ToolDenied(PermissionError):
    pass


@dataclass
class AgentIdentity:
    name: str
    scopes: set[str]
    allowed_tools: set[str]


@dataclass
class Tool:
    name: str
    func: Callable[..., Any]
    kind: str  # "read" or "write"
    scope: str
    description: str = ""


@dataclass
class PendingApproval:
    id: int
    agent: str
    tool: str
    args: dict
    status: str = "pending"
    approver: str | None = None
    result: Any = None


@dataclass
class ToolRegistry:
    tools: dict[str, Tool] = field(default_factory=dict)
    queue: dict[int, PendingApproval] = field(default_factory=dict)
    audit: list[dict] = field(default_factory=list)
    _ids: Any = field(default_factory=lambda: itertools.count(1))

    def register(self, tool: Tool) -> None:
        if tool.kind not in {"read", "write"}:
            raise ValueError("kind must be 'read' or 'write'")
        self.tools[tool.name] = tool

    def call(self, agent: AgentIdentity, tool_name: str, /, **args: Any) -> Any:
        name = tool_name
        tool = self.tools.get(name)
        if tool is None or name not in agent.allowed_tools:
            self._log(agent.name, name, args, "denied:not_allowed")
            raise ToolDenied(f"{agent.name} may not call {name}")
        if tool.scope not in agent.scopes:
            self._log(agent.name, name, args, "denied:missing_scope")
            raise ToolDenied(f"{agent.name} lacks scope {tool.scope}")
        if tool.kind == "write":
            item = PendingApproval(next(self._ids), agent.name, name, args)
            self.queue[item.id] = item
            self._log(agent.name, name, args, f"queued:{item.id}")
            return item
        result = tool.func(**args)
        self._log(agent.name, name, args, "ok")
        return result

    def execute_within_limits(self, agent: AgentIdentity, tool_name: str, /, **args: Any) -> Any:
        """Run a write tool without the approval queue.

        Only for autonomy L3 ("act within limits"): the caller (the contract
        enforcer) has already checked the contract's limits for this call.
        Allow-list and scope checks still apply here.
        """
        tool = self.tools.get(tool_name)
        if tool is None or tool_name not in agent.allowed_tools or tool.scope not in agent.scopes:
            self._log(agent.name, tool_name, args, "denied:not_allowed")
            raise ToolDenied(f"{agent.name} may not call {tool_name}")
        result = tool.func(**args)
        self._log(agent.name, tool_name, args, "executed_within_limits")
        return result

    def approve(self, approval_id: int, approver: str) -> Any:
        item = self.queue[approval_id]
        if item.status != "pending":
            raise ValueError(f"approval {approval_id} is {item.status}")
        item.result = self.tools[item.tool].func(**item.args)
        item.status, item.approver = "approved", approver
        self._log(item.agent, item.tool, item.args, f"approved_by:{approver}")
        return item.result

    def reject(self, approval_id: int, approver: str) -> None:
        item = self.queue[approval_id]
        item.status, item.approver = "rejected", approver
        self._log(item.agent, item.tool, item.args, f"rejected_by:{approver}")

    def _log(self, agent: str, tool: str, args: dict, outcome: str) -> None:
        self.audit.append({"agent": agent, "tool": tool, "args": args, "outcome": outcome})
