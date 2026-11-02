# Use case spec: <Use case name>

Pack: `<pack-slug>`. Copy this folder to `use-cases/<use-case-slug>/`. Make three starter specs per pack.

| Field | Value |
|---|---|
| Pattern | <RAG Q&A / RAG drafting / summarization / classification / tool agent> |
| Risk tier | <Tier 1 / 2 / 3> |
| Autonomy | <L0 / L1 / L2 / L3> |

## Business problem

<Two or three sentences. What is slow, costly or risky today?>

## Users

<Roles who will use it. Front-line roles first.>

## Pattern

<Which blueprint pattern, and why it fits.>

## Data

- <Source (class)>
- <Source (class)>

## Risk tier and autonomy

- <Tier and autonomy, and the reason. Regulated decisions about people start at Tier 3.>
- <What would raise the tier.>

## Guardrails

- <Use-case-specific guardrail>
- <Which sector rules from guardrails.yaml apply>
- <Human approval point>

## Success metrics

- <Quality metric tied to the golden set>
- <Business metric with baseline>
- <Risk metric with a target, e.g. zero leaks>

## Golden eval notes

<Who writes the examples, how many (100-300 in real use), which edge cases to include. Each line: `id`, `input`, `context`, `expected_keywords` (must appear verbatim in the context), `forbidden` (must not appear in input or context).>
