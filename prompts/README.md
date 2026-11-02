# Prompt registry

| | |
|---|---|
| **What** | Versioned production prompts with owner, linked eval set and change history |
| **Why** | A prompt change can break behaviour as badly as a code change. Versions make changes reviewable, testable and reversible |
| **Who** | Prompt owners propose; the eval gate and reviewers approve |
| **When** | Every prompt change is a release: new version file, eval run, then move `current` |
| **Where** | `registry.yaml` (index) and `library/<id>/<version>.md` (text) |
| **How** | `PromptRegistry.load().get("rag-answer").render(context=..., question=..., history=...)` |

Rules (from `02-architecture/standards/integration-standards.md` section 6):
- No secrets, credentials or business rules in prompt text.
- Only `approved` versions load in normal use; `current` must point at one.
- Each rendered prompt carries its id, version and content hash into the trace, so any answer can be traced to the exact prompt text.
- AI systems list the prompts they use in `01-governance/ai-inventory.yaml`; the policy gate checks they exist and are approved.

## Changing a prompt
1. Copy the current file to a new version, e.g. `library/rag-answer/1.2.0.md`, and edit it.
2. Add the version to `registry.yaml` with `status: draft`.
3. Run `kit-evals` on the linked eval set with the new version.
4. If it passes, set `status: approved`, move `current`, and mark the old version `deprecated`.
