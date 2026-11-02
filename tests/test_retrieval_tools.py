import pytest

from kit.retrieval import Document, Index
from kit.tools import AgentIdentity, Tool, ToolDenied, ToolRegistry


def test_acl_filter_before_ranking():
    idx = Index([Document("A", "Pay", "executive bonus pool rules", {"execs"}),
                 Document("B", "Leave", "annual leave policy rules", {"all-staff"})])
    assert [h.doc.id for h in idx.search("executive bonus", {"all-staff"})] == [] or \
           all(h.doc.id != "A" for h in idx.search("executive bonus", {"all-staff"}))
    assert idx.search("executive bonus", {"execs"})[0].doc.id == "A"


def test_tool_allow_list_scope_and_approval():
    reg = ToolRegistry()
    reg.register(Tool("read_x", lambda: "x", "read", "x:read"))
    reg.register(Tool("write_x", lambda v: f"set {v}", "write", "x:write"))
    reg.register(Tool("admin_x", lambda: "boom", "write", "x:admin"))
    agent = AgentIdentity("a", {"x:read", "x:write"}, {"read_x", "write_x", "admin_x"})
    assert reg.call(agent, "read_x") == "x"
    p = reg.call(agent, "write_x", v=3)
    assert p.status == "pending"
    assert reg.approve(p.id, "human") == "set 3"
    with pytest.raises(ToolDenied):
        reg.call(agent, "admin_x")            # missing scope
    with pytest.raises(ToolDenied):
        reg.call(AgentIdentity("b", {"x:read"}, set()), "read_x")   # not allow-listed
    assert any(r["outcome"].startswith("approved_by") for r in reg.audit)
