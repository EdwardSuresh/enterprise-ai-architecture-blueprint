"""Lab 04 Concept: tool-using agent (business case: supply-chain PO exceptions).

Shows: agent identity with scopes, tool allow-list, read tool runs at once,
write tool waits in a human approval queue (autonomy L2), full audit log.
The same contract applies when the tools are served by an MCP server.
Run:  python labs/04-tool-agent-mcp/concept.py
"""
from kit.tools import AgentIdentity, Tool, ToolDenied, ToolRegistry

POS = {"PO-7781": {"supplier": "Acme Fasteners", "qty_ordered": 500, "qty_received": 430, "status": "open"}}

def get_po(po_id: str) -> dict:
    return POS[po_id]

def adjust_po_quantity(po_id: str, new_qty: int) -> str:
    POS[po_id]["qty_ordered"] = new_qty
    return f"{po_id} quantity set to {new_qty}"

def delete_supplier(name: str) -> str:
    return f"deleted {name}"

reg = ToolRegistry()
reg.register(Tool("get_po", get_po, "read", "po:read"))
reg.register(Tool("adjust_po_quantity", adjust_po_quantity, "write", "po:write"))
reg.register(Tool("delete_supplier", delete_supplier, "write", "supplier:admin"))

agent = AgentIdentity("po-exception-agent", scopes={"po:read", "po:write"},
                      allowed_tools={"get_po", "adjust_po_quantity"})

po = reg.call(agent, "get_po", po_id="PO-7781")
print("1) Read tool:", po)
short = po["qty_ordered"] - po["qty_received"]
print(f"   Agent finds a shortfall of {short} units and proposes closing the PO at the received quantity.")

pending = reg.call(agent, "adjust_po_quantity", po_id="PO-7781", new_qty=po["qty_received"])
print(f"2) Write tool queued for approval: #{pending.id} status={pending.status}")

print("3) Buyer approves:", reg.approve(pending.id, approver="buyer.jlee"))

try:
    reg.call(agent, "delete_supplier", name="Acme Fasteners")
except ToolDenied as e:
    print("4) Blocked:", e)

print("\nAudit log:")
for row in reg.audit:
    print("  ", row)
