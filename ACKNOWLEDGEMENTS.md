# Acknowledgements and references

## Inspiration

- The starting point for this kit was a public infographic, **"Enterprise AI Project Structure File Tree" by Poornachandra Kongara**, which lays out a well-organized agent application repository. This kit asks what an *enterprise* needs on top of that (governance, multi-cloud, industry overlays, evidence) and answers it independently. No text or graphics from the infographic are reproduced here.
- **[The Architect's ML Playbook](https://edwardsuresh.github.io/architects-ml-playbook/)** by the same author, for the classic and deep-learning algorithms referenced in `platform/ml/`.

## Frameworks and standards referenced

The kit maps its artifacts to these works. Descriptions in this repository are the author's own short paraphrases, not reproductions. Consult the originals for authoritative text.

| Work | Publisher | Link |
|---|---|---|
| AI Risk Management Framework (AI RMF 1.0, NIST AI 100-1) | U.S. National Institute of Standards and Technology | https://www.nist.gov/itl/ai-risk-management-framework |
| ISO/IEC 42001:2023 Artificial intelligence management system | ISO / IEC (licensed standard) | https://www.iso.org/standard/81230.html |
| Regulation (EU) 2024/1689 (Artificial Intelligence Act) | European Union | https://eur-lex.europa.eu/eli/reg/2024/1689/oj |
| OWASP Top 10 for LLM Applications 2025 | OWASP GenAI Security Project | https://genai.owasp.org/llm-top-10/ |
| OpenTelemetry semantic conventions for generative AI | OpenTelemetry / CNCF | https://opentelemetry.io/docs/specs/semconv/gen-ai/ |
| Model Context Protocol | Model Context Protocol project | https://modelcontextprotocol.io |
| TOGAF® Standard | The Open Group | https://www.opengroup.org/togaf |

Sector regulations named in `domain-packs/*/regulations.md` belong to their respective regulators; see each file for names and the note to confirm current guidance with counsel.

## Third-party software

The kit's own code is MIT-licensed. It uses, but does not copy into this repository, the following:

| Component | Use | Licence |
|---|---|---|
| PyYAML | Runtime dependency | MIT |
| pytest | Tests (optional extra) | MIT |
| Mermaid | Diagrams on the website, loaded from the jsDelivr CDN | MIT |
| Archivo, Source Sans 3, JetBrains Mono | Website fonts, loaded from Google Fonts | SIL Open Font License 1.1 |
| openai (Python SDK) | Optional Azure adapter | Apache-2.0 |
| boto3 | Optional AWS adapter | Apache-2.0 |
| google-genai | Optional Google Cloud adapter | Apache-2.0 |
| anthropic (Python SDK) | Optional Claude API adapter | MIT |
| FastAPI, Uvicorn | Optional reference API | MIT, BSD-3-Clause |

Product and standard names are trademarks of their owners; see [DISCLAIMER.md](DISCLAIMER.md).
