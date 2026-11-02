# Lab 02: Permission-Aware RAG

**Business case (Illustrative example):** An insurer gives underwriters a Q&A assistant over the underwriting manual. Answers must cite manual sections. Underwriters must never see documents meant only for executives.

| 5W1H | Answer |
|---|---|
| **Who** | Underwriters (users), knowledge owners, data owners, platform engineers |
| **What** | Retrieval-augmented generation that filters by the caller's access rights before ranking and cites every source |
| **When** | The first production use case in most organizations. Start here after the gateway |
| **Where** | `kit.retrieval` (`platform/core/kit/retrieval.py`) and `kit.orchestrator`; pattern in `02-architecture/patterns/rag-assistant.md` |
| **Why** | RAG without access filtering leaks documents. RAG without citations cannot be checked |
| **How** | Concept with keyword/TF-IDF style retrieval over sample docs, Build with a managed search index, Production with data contracts and evals |

## Concept (plain Python, no cloud)

From the repo root:

```bash
pip install -e .
python labs/02-rag/concept.py
```

What it shows:

1. **Keyword / TF-IDF style retrieval** over a few sample underwriting documents.
2. **Access-control filtering before ranking.** Each document carries ACL groups. The search only scores documents the caller's groups allow.
3. **Citations.** Each answer lists the document IDs used.
4. **Safe hand-off.** When an underwriter asks about a document only executives can see, the assistant says it cannot answer from approved sources, instead of guessing.

Try this: add a document with a new group, then ask a question as a user with and without that group.

## Build on Azure (reference implementation)

1. Create `rg-aikit-lab02` and a budget alert.
2. Create **Azure AI Search** on the **Free tier**. Note its limits on index count and size.
3. Create a storage account and upload a few sample manual pages (fictitious content only).
4. Create an index with fields: `id`, `title`, `content`, `section`, `version`, and `acl_groups` (a filterable collection of strings).
5. Load the documents. Use the push API or an indexer. Set `acl_groups` from the source system's groups.
6. Query with a filter such as `acl_groups/any(g: search.in(g, 'underwriters'))`. Use keyword search first, then try semantic ranking or vector search if your tier allows it.
7. Send the top results to your **Microsoft Foundry** model deployment through the Lab 01 gateway. Prompt the model to answer only from the context and cite `id` and `section`.
8. Test the same three questions as the Concept lab.

## Build on AWS (short)

- Use **Amazon Bedrock Knowledge Bases** with **OpenSearch Serverless** or another supported vector store.
- Add metadata (for example `acl_groups`) to each document and use metadata filters on retrieval.
- OpenSearch Serverless has a minimum capacity charge. Delete the collection at the end of each session.

## Build on Google Cloud (short)

- Use **Vertex AI Search** or the **Vertex AI RAG Engine** with a corpus in Cloud Storage.
- Add metadata to documents and filter by the caller's groups at query time.
- Ground answers with citations returned by the service.

Service names and features change. Check the current docs for each provider.

## Production

1. Write a data contract for the manual source. Use `data/contracts/` and `domain-packs/insurance/data-contracts/README.md` as the model: owner, class, ACL source, sync frequency, retention.
2. Add the system to `01-governance/ai-inventory.yaml` with a system card (see `01-governance/system-cards/AIS-001-underwriting-assistant.yaml`).
3. Grow the golden set in `domain-packs/insurance/evals/golden.jsonl` with real underwriter questions. Include "not covered" questions and ACL tests.
4. **CI gates:** `.github/workflows/evals.yml` fails when the golden pass rate drops below threshold. `.github/workflows/policy-gate.yml` checks the inventory entry. `.github/workflows/ci.yml` runs the retrieval tests.
5. Evidence to keep: index schema, ACL sync logs, eval reports in `evals/reports/`, trace samples showing citations.

## Exit criteria

- [ ] Retrieval never returns a document the caller's groups do not allow.
- [ ] Every answer cites at least one source, or hands off.
- [ ] The cloud index has an ACL field that is filtered on every query.
- [ ] The data contract names an owner and an ACL source.
- [ ] The insurance golden set passes in `evals.yml`.

## Cleanup

```bash
az group delete -n rg-aikit-lab02 --yes --no-wait
```

On AWS, delete the knowledge base and the OpenSearch Serverless collection. On Google Cloud, delete the search app, data store or RAG corpus.

**Maps to:** `platform/core/kit/retrieval.py`, `platform/core/kit/orchestrator.py`, `02-architecture/patterns/rag-assistant.md`, `data/contracts/`, `data/classification.yaml`, `01-governance/system-cards/`, `domain-packs/insurance/`.
