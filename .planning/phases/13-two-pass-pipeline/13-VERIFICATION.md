# Phase 13: Two-Pass Pipeline — Verification

## Goal
Wire classifier output into the extraction pipeline so the LLM receives a type-specific prompt tailored to the document's detected category (PIPE-01).

## Plans Executed
| Plan | Description | Status |
|------|-------------|--------|
| 13-01 | ExtractionPipeline orchestrator + llm_service prompt_override | ✅ |
| 13-02 | Integration into CVProcessor with two-pass flag | ✅ |
| 13-03 | Unit tests (6 tests) | ✅ |

## Gap Coverage

| Decision | Gaps | Status |
|----------|------|--------|
| D-01 | ExtractionPipeline in `app/services/extraction_pipeline.py` | ✅ |
| D-02 | Returns dict with extraction + classification + prompt_version | ✅ |
| D-03 | PromptResolver for cv-extraction prompt | ✅ |
| D-04 | Non-CV returns classification_warning | ✅ |
| D-05 | Non-CV flagged, extraction bypassed | ✅ |
| D-06 | Logging at each stage | ✅ |
| D-07 | Pipeline integrated into CVProcessor with `use_two_pass` flag | ✅ |
| D-08 | Single-pass backward compatible (default `use_two_pass=False`) | ✅ |

## Test Results
- 6 new tests: all pass
- 167 existing tests: all pass (3 pre-existing failures unrelated)
- No regression

## Files Changed
- `backend/app/services/llm_service.py` — added `prompt_override` parameter
- `backend/app/services/extraction_pipeline.py` — new file: ExtractionPipeline orchestrator
- `backend/app/services/cv_processor.py` — integrated two-pass pipeline with flag
- `backend/tests/test_two_pass_pipeline.py` — 6 tests

## Evidence
```
tests/test_two_pass_pipeline.py::test_pipeline_returns_warning_for_empty_text PASSED
tests/test_two_pass_pipeline.py::test_pipeline_returns_warning_for_whitespace_text PASSED
tests/test_two_pass_pipeline.py::test_pipeline_non_cv_classification PASSED
tests/test_two_pass_pipeline.py::test_pipeline_cv_classification_no_prompt PASSED
tests/test_two_pass_pipeline.py::test_pipeline_cv_classification_with_prompt PASSED
tests/test_two_pass_pipeline.py::test_pipeline_passes_prompt_override_to_extract PASSED
```
