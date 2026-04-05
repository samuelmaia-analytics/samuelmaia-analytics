# Analytics GenAI Layer

## Purpose

The platform includes an optional GenAI layer designed for analytics use cases instead of generic chat output.
It remains useful without an external LLM provider and stays easy to test, review, and replace.

## Supported Use Cases

- narrative KPI insights
- executive summary generation
- anomaly explanation draft
- metric definition assistant
- business glossary explanation
- pipeline and dataset description generation

## Architecture

```text
config/prompts/genai/*.md                 prompt pack per analytics use case
core/ai/models.py                         typed context and artifact contracts
core/ai/providers.py                      provider abstraction with local and OpenAI-compatible implementations
core/ai/service.py                        orchestration and per-use-case generation logic
core/operational_context.py               freshness, lineage, and recent runtime signal extraction
core/pipeline.py                          injects governed context and persists artifacts in the canonical snapshot
services/api/main.py                      protected GenAI endpoint for downstream consumption
app/pages/05_GenAI_Analytics_Assistant.py review surface for generated drafts
```

## Runtime Context Used By GenAI

The GenAI layer no longer relies only on semantic metrics and quality status.
It also consumes:

- artifact and source freshness metadata
- recent structured events from observability logs
- comparative run history and metric deltas between recent snapshots
- historical snapshot comparison for quality, repository surface, semantic catalog, and GenAI capability count
- lightweight dataset lineage for generated outputs
- repository registry metadata

This keeps anomaly drafts and dataset descriptions anchored in actual runtime evidence from the scaffold.
The same historical snapshot base also powers a structured trend series for APIs, warehouse exports, and executive UI.

## Provider Strategy

Two provider modes are supported:

- `local-template`
  deterministic, mockable, and CI-safe
- `openai-compatible`
  sends structured prompts to a `/chat/completions` compatible endpoint and expects JSON output

The local provider remains the default for tests, offline review, and controlled demos.

## How to Plug an LLM API Later

1. Configure the provider variables.

```powershell
$env:PORTFOLIO_GENAI_PROVIDER="openai-compatible"
$env:PORTFOLIO_GENAI_MODEL="gpt-4.1-mini"
$env:PORTFOLIO_GENAI_BASE_URL="https://api.openai.com/v1"
$env:PORTFOLIO_GENAI_API_KEY="your-api-key"
```

2. Keep prompts versioned under `config/prompts/genai/`.

3. Ensure the provider supports `POST /chat/completions` with bearer authentication.

4. Return JSON content using this shape:

```json
{
  "narrative": "string",
  "bullets": ["string", "string", "string"]
}
```

5. Validate generated output through tests and the `/genai` endpoint before broader adoption.

## Operating Guidance

- treat generated output as draft content, not approval-ready truth
- keep metric and glossary definitions sourced from the semantic catalog
- use low temperature and predictable prompt structures
- validate anomalies against contracts, freshness, and lineage before escalation
- do not couple UI rendering to provider-specific response formats
