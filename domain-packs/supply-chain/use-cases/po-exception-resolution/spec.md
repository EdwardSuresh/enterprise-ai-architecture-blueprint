# Use case spec: Purchase order exception resolution

Pack: `supply-chain`. Illustrative example; adapt to your organization.

| Field | Value |
|---|---|
| Pattern | Tool agent. Read tools look up PO, receipt and invoice; write tools (update PO, email supplier) go to the human approval queue. |
| Risk tier | Tier 2 |
| Autonomy | L2 |

## Business problem

Thousands of PO exceptions (price, quantity, date mismatches) sit in queues. Buyers spend most of their day on low-value checks.

## Users

Buyers, accounts payable analysts, category managers.

## Pattern

Tool agent. Read tools look up PO, receipt and invoice; write tools (update PO, email supplier) go to the human approval queue.

## Data

- ERP POs, receipts, invoices (confidential)
- Supplier contracts (confidential)
- P2P procedures (internal)

## Risk tier and autonomy

- Tier 2, autonomy L2. Confirm through governance intake.
- Raise the tier if the output feeds a regulated decision about a person.

## Guardrails

- Agent uses a scoped identity with read-only ERP access; writes run under the approver's authority.
- SC-G01 forces approval for PO changes and payments.
- Tool allow-list in kit.tools; no free-form API calls.
- Sector rules in [guardrails.yaml](../../guardrails.yaml) apply.

## Success metrics

- Exceptions resolved per buyer per day
- Approval rejection rate
- Payment errors (target zero)
- Set a baseline before launch. Agree targets with the business owner.

## Golden eval notes

Use resolved exceptions with the buyer's final action as the label. Include cases where the correct action is 'escalate'.

Each golden line follows the blueprint schema: `id`, `input`, `context`, `expected_keywords` (must appear in the context), `forbidden`.
