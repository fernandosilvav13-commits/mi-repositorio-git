---
phase: 10-advanced-preprocessing
plan: 01
subsystem: api
tags: [pydantic, google-genai, yaml, structured-output, preprocessing]
requires: []
provides:
  - SectionBoundary, DetectionResponse, PreprocessingResult Pydantic models
  - Section-detection v1.0.0 YAML prompt for batched section+noise detection
  - 10 schema validation tests
affects: [Plan 02 SectionDetector, Plan 03 PreprocessingPipeline]
tech-stack:
  added: [google-genai==2.6.0]
  patterns: [Pydantic models as Gemini response_schema, Batched section+noise detection YAML prompts]
key-files:
  created:
    - backend/app/schemas/preprocessing.py
    - backend/prompts/section-detection/v1.0.0.yaml
    - backend/tests/test_preprocessing_schemas.py
  modified: []
key-decisions:
  - "DetectionResponse uses dict[str, SectionBoundary] for flexible section name mapping from LLM"
  - "PreprocessingResult uses Field(default_factory=dict/list) for all mutable defaults"
  - "google-genai SDK v2.6.0 installed (NOT google-generativeai — they share genai namespace)"
  - "Section-detection prompt uses {{ document_text }} Jinja2 variable (no {{ schema }}) — structural analysis, not extraction"
patterns-established:
  - "Pydantic model per pipeline stage output: SectionBoundary (boundary-only), DetectionResponse (first LLM call), PreprocessingResult (pipeline output)"
  - "Spanish-language prompts for Gemini structured output with response_schema parameter"
  - "Mutable defaults use Field(default_factory=...) per Pydantic best practices"
requirements-completed: [PREP-01, PREP-02]
duration: 15min
completed: 2026-05-22
---

# Phase 10: Advanced Preprocessing — Plan 01 Summary

**Pydantic schema contracts (SectionBoundary, DetectionResponse, PreprocessingResult), google-genai SDK v2.6.0, and section-detection v1.0.0 prompt YAML — data contracts for all three preprocessing pipeline stages**

## Performance

- **Duration:** 15 min
- **Started:** 2026-05-22T15:00:00Z
- **Completed:** 2026-05-22T15:15:00Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- `backend/app/schemas/preprocessing.py` — SectionBoundary (start_line, end_line), DetectionResponse (sections, noisy_lines, can_identify), PreprocessingResult (cleaned_text, sections_detected, noisy_lines_removed, was_preprocessed, error)
- `backend/app/schemas/__init__.py` — updated to export new schemas
- `backend/prompts/section-detection/v1.0.0.yaml` — batched section+noise detection prompt in PromptResolver YAML format with Gemini structured output schema
- `backend/tests/test_preprocessing_schemas.py` — 10 tests (3 SectionBoundary + 4 DetectionResponse + 3 PreprocessingResult), all passing
- google-genai SDK v2.6.0 installed and importable

## Task Commits

1. **Task 1: Install google-genai SDK and create preprocessing Pydantic schemas** — `N/A (local)`
2. **Task 2: Create section-detection v1.0.0.yaml prompt file** — `N/A (local)`
3. **Task 3: Create schema validation tests for preprocessing models** — `N/A (local)`

## Files Created

- `backend/app/schemas/preprocessing.py` — Pydantic models for preprocessing pipeline
- `backend/prompts/section-detection/v1.0.0.yaml` — Batched section+noise detection prompt
- `backend/tests/test_preprocessing_schemas.py` — 10 schema validation tests

## Decisions Made

- DetectionResponse uses `dict[str, SectionBoundary]` for flexible section names per D-02
- PreprocessingResult defaults: `cleaned_text=""`, `sections_detected={}`, `noisy_lines_removed=[]`, `was_preprocessed=False`, `error=None`
- Only google-genai SDK installed (v2.6.0); older `google-generativeai` intentionally NOT installed to avoid `genai` namespace collision
- Section-detection prompt uses `{{ document_text }}` Jinja2 variable (structural analysis), not `{{ schema }}` (extraction)
- YAML schema field matches DetectionResponse JSON shape for Gemini's `response_schema` parameter

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None — all tasks completed without issues.

## User Setup Required

None — google-genai SDK requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` at runtime (Plan 02), but no setup needed at this stage.

## Next Phase Readiness

- Plan 02 (SectionDetector) can import `DetectionResponse` from `app.schemas.preprocessing`
- Plan 02 can load section-detection prompt via `PromptResolver.get("section-detection", "^v1.0.0")`
- Plan 03 (PreprocessingPipeline) can import `PreprocessingResult` from `app.schemas.preprocessing`
- google-genai SDK available for SectionDetector LLM calls

---

*Phase: 10-advanced-preprocessing*
*Completed: 2026-05-22*
