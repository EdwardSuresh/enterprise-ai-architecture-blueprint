# API layer

| | |
|---|---|
| **What** | The service layer that exposes agents through authenticated REST endpoints |
| **Why** | Channels (web, mobile, Teams, back-office) share one governed backend |
| **Who** | Platform team |
| **How** | `pip install -e .[api]` then `uvicorn api.app:app --reload` (reference only; runs the offline mock model) |

In production, put your API gateway in front (Azure API Management, Amazon API Gateway or Apigee) for identity, rate limits and versioning. The caller's groups come from the identity token, never from the request body.
