# Financial Services: Data Contracts

Main data sources for this pack's use cases. Each source needs a named owner, a class and an ACL source before AI can use it. Illustrative example; replace with your systems.

| Data source | Owner | Classification | ACL source |
|---|---|---|---|
| Policy and procedure library | Compliance / Operations | internal | Document management groups |
| Core banking accounts and transactions | Retail banking operations | restricted | Core banking entitlements |
| CRM and complaint system | Customer experience | confidential | CRM role model |
| Loan origination and credit files | Credit risk | restricted | Loan system entitlements per portfolio |
| Product disclosures and rate sheets | Product / Legal | public | Public; publish only approved versions |

## Contract rules

- **ACLs travel with the data.** Indexes store the ACL source groups on every chunk. `kit.retrieval` filters by the caller's groups before ranking.
- **Restricted data** needs an approved purpose in the AI inventory, region pinning, and masking where possible.
- **Freshness.** Each source states how often it is synced and how deletes are applied.
- **Lineage.** Every answer cites the source document ID and version. `kit.tracing` records it.
- **Change.** Schema or access model changes go through the data owner and are reviewed at the ARB.

## Fields to record per source

| Field | Example |
|---|---|
| Source system | Document management system |
| Owner (role) | Head of knowledge management |
| Classification | internal |
| ACL source | Directory groups synced nightly |
| Sync frequency | Daily |
| Retention | Per records schedule |
| Allowed AI uses | RAG Q&A; no fine-tuning |
