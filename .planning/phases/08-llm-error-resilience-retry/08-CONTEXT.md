# Phase 8: LLM Error Resilience & Retry - Context

**Gathered:** 2026-05-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Add robust JSON error handling, schema fallback, and bounded retry logic to `llm_service.py` so that transient Gemini formatting issues and extraction failures don't crash the pipeline. Parse repairs, structured logging, and TPM-aware retry backoff.

Covers requirements LLM-01, LLM-02, RETR-01, RETR-02.

</domain>

<decisions>
## Implementation Decisions

### JSON Repair Strategy
- **D-01:** Use regex fixes only — no `json-repair` or `json5` dependency. Handle trailing commas before `]` and `}` (strip them), and replace single quotes with double quotes before `json.loads()`.
- **D-02:** If regex repair + `json.loads()` still fails, retry the API call instead of escalating repair complexity.
- **D-03:** Strip markdown code fences (already implemented in `extract_fields()` via `removeprefix`/`removesuffix`).

### Retry Configuration
- **D-04:** Retry only on JSON parse failures. Network errors, API timeouts, and HTTP errors propagate up immediately — don't mask infrastructure issues.
- **D-05:** Keep the existing exponential backoff formula: `2^attempt * 2 + random(0,1)` seconds. Max 3 attempts before schema fallback.
- **D-06:** Add a simple TPM token counter: track estimated tokens consumed per window and inject a delay when approaching configured limits. No external TPM library.
- **D-07:** The existing `asyncio.Semaphore(5)` in `cv_extractor.py` stays as a concurrency gate.

### Schema Fallback Mechanics
- **D-08:** 3 retries with the dynamic schema (built from template columns via `_build_dynamic_schema()`). On total failure, retry 2 more times with the generic `EXTRACTION_SCHEMA`.
- **D-09:** Return whatever `EXTRACTION_SCHEMA` successfully extracts — partial data is better than `None`. The fallback may miss fields the dynamic schema would have captured, but any data is better than total failure.

### Error UX
- **D-10:** No visual change during retries — retries complete server-side in under 2 seconds. The user sees the same loading state.
- **D-11:** On complete failure (all retries + schema fallback exhausted): show an error banner with helpful message and retry suggestion.
- **D-12:** On partial extraction (fallback succeeded but with fewer fields): display data normally with a subtle info note that some fields could not be extracted.

### Logging & Monitoring
- **D-13:** Structured logging at WARNING level for: each retry attempt (number, error type, model used), schema fallback event, and total extraction failure. No logging on success.
- **D-14:** Use the existing Python logging setup (`backend/app/utils/logger.py`) — do not introduce a new logging mechanism.

### the agent's Discretion
- Exact regex patterns for JSON repair (implementer chooses the specific trailing-comma and single-quote regex)
- TPM counter implementation details (window size, delay formula)
- Error banner component (frontend team builds per the design system)
- Function naming for new helper functions in `llm_service.py`

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — LLM-01 (malformed JSON handling), LLM-02 (strip fences before parse), RETR-01 (fallback to EXTRACTION_SCHEMA), RETR-02 (bounded backoff within TPM limits)

### Codebase
- `backend/app/services/llm_service.py` — Target file. Currently has `extract_fields()` with basic fence-stripping. Needs JSON repair, retry logic, and structured logging.
- `backend/app/services/cv_extractor.py` — Contains `EXTRACTION_SCHEMA` (fallback schema), `_build_dynamic_schema()` (template-based schema), and existing 3-attempt retry loop with exponential backoff.
- `backend/app/services/cv_processor.py` — Entry point for the full extraction pipeline; will call the updated `extract_fields()`.
- `backend/app/core/config.py` — Configuration with `gemini_model_extract`, `gemini_model_retry` model names.
- `backend/app/utils/logger.py` — Existing logging setup to use for structured logging.

### Prior Phase Context
- `.planning/phases/07-post-processing-pipeline/07-CONTEXT.md` — Phase 7 post-processing pipeline context
- `.planning/phases/06-preprocessor-proper-noun-fix/06-CONTEXT.md` — Phase 6 preprocessor fix context

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `llm_service.py:extract_fields()` — Current function to extend with JSON repair and retry logic
- `cv_extractor.py:EXTRACTION_SCHEMA` — Fallback schema with standard fields (NOMBRES, APELLIDOS, RUT, GENERO, TELEFONO_FIJO, TELEFONO_CELULAR, NACIONALIDAD, TITULO_PROFESIONAL, experiencia_laboral)
- `cv_extractor.py:_build_dynamic_schema()` — Builds extraction schema from template columns for richer extraction
- `cv_extractor.py:extract_cv_data()` — Already has 3-attempt retry loop with `2^attempt * 2 + random(0,1)` backoff and `asyncio.Semaphore(5)` concurrency gate

### Established Patterns
- Service-oriented architecture in `backend/app/services/`
- LLM calls use `google-genai` SDK with `response_mime_type: "application/json"`
- Retry with exponential backoff + jitter already established in `extract_cv_data()`
- Sentinel value `"NO ENCONTRADO"` for missing fields (consistent across all extraction code)
- Structured logging via `backend/app/utils/logger.py`

### Integration Points
- `llm_service.py:extract_fields()` — Called by `cv_extractor.py:extract_cv_data()` (line 85)
- The retry loop currently lives at `cv_extractor.py` level (lines 82-97) — phase moves it into `llm_service.py`
- Schema fallback requires access to both the dynamic schema and `EXTRACTION_SCHEMA` — both in `cv_extractor.py`

</code_context>

<specifics>
## Specific Ideas

- Move retry logic from `cv_extractor.py:extract_cv_data()` into `llm_service.py:extract_fields()` so all LLM resilience lives in one place
- The existing `extract_cv_data()` retry loop (lines 82-97) uses a different model for retries (`gemini_model_retry`) — preserve this model-switching behavior
- Schema fallback: `extract_fields()` should accept an optional `fallback_schema` parameter; when all dynamic-schema retries fail, retry with `fallback_schema`
- Error banner should follow the existing Apple design system in `globals.css`

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 8-LLM Error Resilience & Retry*
*Context gathered: 2026-05-17*
