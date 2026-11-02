# <Sector Name>: Data Contracts

_List each main data source the pack's use cases need. No source is used by AI until it has an owner, a class and an ACL source._

| Data source | Owner | Classification | ACL source |
|---|---|---|---|
| <Policy and procedure library> | <Role> | internal | <Directory groups> |
| <System of record with personal data> | <Role> | restricted | <Application roles> |
| <Operational system> | <Role> | confidential | <Application roles> |
| <Published content> | <Role> | public | Public |

## Contract rules

- **ACLs travel with the data.** Every indexed chunk keeps its ACL groups. `kit.retrieval` filters by the caller's groups before ranking.
- **Restricted data** needs an approved purpose in the AI inventory, region pinning, and masking where possible.
- **Freshness.** State sync frequency and how deletes are applied.
- **Lineage.** Answers cite document ID and version. `kit.tracing` records it.
- **Change.** Schema or access changes go through the data owner and the ARB.

## Fields to record per source

| Field | Example |
|---|---|
| Source system | <System name> |
| Owner (role) | <Role> |
| Classification | <public / internal / confidential / restricted> |
| ACL source | <Where permissions come from> |
| Sync frequency | <Daily> |
| Retention | <Per records schedule> |
| Allowed AI uses | <RAG Q&A; no fine-tuning> |
