# Phase 10: Advanced Preprocessing - Context

**Gathered:** 2026-05-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Structural cleanup and noise removal applied before classification and extraction, so downstream stages receive clean, organized text. Implements PREP-01 (section detection + layout normalization) and PREP-02 (noise filtering). Builds on top of the existing preprocessor.py regex-based approach with LLM-guided enhancements.

</domain>

<decisions>
## Implementation Decisions

### Section Detection Strategy
- **D-01:** LLM-guided section detection — a dedicated Gemini call identifies document sections (Education, Experience, Skills, etc.) before extraction
- **D-02:** Detection returns boundary-only JSON — e.g., `{"Education": {"start_line": 0, "end_line": 50}}` — without modifying the original text
- **D-03:** If the LLM cannot identify clear section boundaries, preprocessing is skipped entirely for that document (raw text passes through)
- **D-04:** Section detection is a separate LLM call BEFORE extraction (not part of the extraction prompt)

### Noise Filtering Criteria
- **D-05:** Noise detection is combined with section detection into a single batched LLM call — one JSON response returns both sections and noise regions
- **D-06:** Total LLM calls per document: 2 (batched section+noise detection, then extraction)
- **D-07:** Noise types to detect and strip: page headers/running heads, page numbers, footers/disclaimers, document metadata artifacts

### Layout Normalization Strategy
- **D-08:** Intelligent structure: collapse inline whitespace within paragraphs, preserve paragraph breaks, and add section boundary markers based on LLM detection results
- **D-09:** Bullet points normalized to a consistent format (standard marker across all variants: -, *, •, →)

### Pipeline Architecture
- **D-10:** Multi-stage pipeline with separate classes per stage: SectionDetector, NoiseFilter, LayoutNormalizer
- **D-11:** Pipeline is a separate service injected into the extraction flow (not replacing preprocess_cv_text() inline)
- **D-12:** New test file per stage: test_section_detector.py, test_noise_filter.py, test_layout_normalizer.py, test_pipeline.py

### The agent's Discretion
- Specific LLM prompt templates for the batched section+noise detection call
- Bullet point normalization implementation details (which marker to use as standard)
- Paragraph break threshold (how many consecutive newlines constitute a paragraph break)
- Error handling strategy for LLM failures in the preprocessing pipeline

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Code
- `backend/app/services/preprocessor.py` — Current preprocessor with regex SECTIONS dict, clean_text(), preprocess_cv_text()
- `backend/tests/test_preprocessor.py` — 10 existing tests for current preprocessor behavior
- `backend/app/services/cv_extractor.py` — Calls preprocess_cv_text() before LLM extraction
- `backend/app/services/cv_processor.py` — Orchestrates the extraction pipeline, integration target
- `backend/app/services/llm_service.py` — LLM call patterns to follow for the batched detection call

### Requirements
- `.planning/REQUIREMENTS.md` — PREP-01 and PREP-02 defined with detailed scope

### Architecture
- `.planning/codebase/ARCHITECTURE.md` — Service layer and integration patterns
- `.planning/codebase/CONVENTIONS.md` — Coding conventions for new services and tests

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/app/services/preprocessor.py` — Existing clean_text(), extract_sections(), compress_experience(), preprocess_cv_text() can serve as regex fallback
- `backend/app/utils/logger.py` — Logger utility for pipeline tracing
- PromptResolver from Phase 9 — Can version LLM prompts used for section/noise detection

### Established Patterns
- Service class pattern (CVProcessor, PromptResolver) — module-level singletons with __init__ for configuration
- pytest fixture pattern — tmp_path for test isolation
- LLM service call pattern — async extract_fields() with model, schema, and TPM tracking

### Integration Points
- `backend/app/services/cv_processor.py` — The pipeline service should be injectable into CVProcessor.process()
- `backend/app/services/cv_extractor.py` — Current preprocess_cv_text() call site; the pipeline replaces or enriches this

</code_context>

<specifics>
## Specific Ideas

- The batched section+noise LLM call should return a JSON like: `{"sections": [{"name": "Education", "start": 0, "end": 50}, ...], "noise_regions": [{"start": 51, "end": 55, "type": "page_header"}, ...]}`
- Section boundary markers should align with prompt templates planned in Phase 13 (Two-Pass Pipeline)
- LLM prompt for detection should be versioned via PromptResolver (Phase 9 output)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 10-Advanced Preprocessing*
*Context gathered: 2026-05-21*
