---
phase: 10-advanced-preprocessing
plan: 03
subsystem: preprocessing
tags: [pipeline-orchestrator, section-boundary-adjustment, pitfall-2, pydantic, singleton-pattern]

requires:
  - phase: 10-advanced-preprocessing
    plan: 01
    provides: DetectionResponse, SectionBoundary, PreprocessingResult Pydantic models
  - phase: 10-advanced-preprocessing
    plan: 02
    provides: SectionDetector, NoiseFilter, LayoutNormalizer stage classes

provides:
  - PreprocessingPipeline class with process(document_text) → PreprocessingResult
  - Module-level singleton `preprocessing_pipeline` for production use
  - Pitfall 2 mitigation via _adjust_section_boundaries() for line-number re-alignment after noise removal
  - Per-stage error recovery (SectionDetector failure, LayoutNormalizer failure) with graceful fallback
  - 8 integration tests with mocked SectionDetector and real NoiseFilter/LayoutNormalizer

affects:
  - Plan 04+ — downstream extraction flow (cv_processor/cv_extractor) will import preprocessing_pipeline

tech-stack:
  added: []
  patterns:
    - "Pipeline orchestrator with constructor injection for testability, module-level singleton for production"
    - "Per-stage try/except error recovery — stage failure returns graceful PreprocessingResult without crashing"
    - "Section boundary adjustment via noisy-line-count offset correction (Pitfall 2 mitigation)"
    - "Legacy preprocess_cv_text() preserved alongside new pipeline for backward compatibility"

key-files:
  created:
    - backend/tests/test_preprocessor_pipeline.py
  modified:
    - backend/app/services/preprocessor.py

key-decisions:
  - "Backward compatibility: preprocess_cv_text() preserved in preprocessor.py alongside new PreprocessingPipeline class — cv_extractor.py imports it"
  - "Section boundary adjustment done in PreprocessingPipeline._adjust_section_boundaries() rather than in LayoutNormalizer — keeps normalizer stateless and pure"
  - "Constructor injection for tests, module-level singleton for production — matches PromptResolver pattern"

patterns-established:
  - "Pipeline orchestrator pattern: constructor injection → stage instances → process(text) entry point"
  - "Per-stage error isolation: each stage call wrapped in try/except with appropriate fallback behavior"

requirements-completed: [PREP-01, PREP-02]

duration: 25min
completed: 2026-05-22
---

# Phase 10 Plan 03: PreprocessingPipeline Orchestrator Summary

**PreprocessingPipeline orchestrator chaining SectionDetector → NoiseFilter → LayoutNormalizer with per-stage error recovery, Pitfall 2 section boundary adjustment, and 8 integration tests**

## Performance

- **Duration:** 25 min
- **Started:** 2026-05-22T15:10:00Z
- **Completed:** 2026-05-22T15:35:00Z
- **Tasks:** 2
- **Files modified:** 2 (1 created, 1 modified)

## Accomplishments

- Created `PreprocessingPipeline` class with `process(document_text)` entry point:
  - Chains SectionDetector → NoiseFilter → LayoutNormalizer in sequence per D-10
  - Constructor accepts stage instances for mock injection in tests
  - Empty/None text returns `PreprocessingResult(was_preprocessed=False, error="Empty document text")` immediately
  - D-03 fallback: returns original text with `was_preprocessed=False` when `can_identify=False` or `sections` empty
  - Per-stage error recovery: `SectionDetector.detect()` exception returns graceful fallback; `LayoutNormalizer.normalize()` exception returns text after noise removal
  - Returns `PreprocessingResult` with `was_preprocessed=True` on success

- Implemented Pitfall 2 mitigation via `_adjust_section_boundaries()`:
  - After NoiseFilter removes lines, original section line numbers are no longer accurate
  - Computes adjusted boundaries by subtracting count of noisy lines before each section
  - Uses integer arithmetic on validated `SectionBoundary` types (T-10-13 mitigation)

- Created module-level singleton `preprocessing_pipeline` with real stage classes for production use

- Preserved legacy `preprocess_cv_text()` function and helpers for backward compatibility with `cv_extractor.py`

- Created 8 integration tests, all passing:
  - `test_full_pipeline_happy_path` — verifies noise removal + section markers
  - `test_skip_on_cannot_identify` — D-03 fallback
  - `test_skip_on_empty_sections` — D-03 fallback (empty sections)
  - `test_skip_on_empty_text` — empty string handling
  - `test_skip_on_none_text` — None input handling
  - `test_error_during_detection` — graceful degradation on API failure
  - `test_error_during_normalization` — edge case handling
  - `test_section_boundary_adjustment` — Pitfall 2 mitigation verification

## Task Commits

Each task committed atomically:

1. **Task 1: Create PreprocessingPipeline orchestrator with module-level singleton** - `271cdaf` (feat)
   - `backend/app/services/preprocessor.py`
   - Amended to include legacy `preprocess_cv_text()` backward compatibility

2. **Task 2: Create pipeline integration tests** - `8d87c9c` (test)
   - `backend/tests/test_preprocessor_pipeline.py`

## Files Created/Modified

- `backend/app/services/preprocessor.py` — Modified: added `PreprocessingPipeline` class with `process()`, `_adjust_section_boundaries()`, and module-level singleton `preprocessing_pipeline`; preserved legacy `preprocess_cv_text()` function
- `backend/tests/test_preprocessor_pipeline.py` — Created: 8 integration tests with mocked SectionDetector

## Decisions Made

- **Backward compatibility preserved**: The legacy `preprocess_cv_text()` function and helpers (`clean_text`, `extract_sections`, `compress_experience`, constants) are kept in `preprocessor.py` alongside the new `PreprocessingPipeline` class. This prevents breaking `cv_extractor.py` which imports `preprocess_cv_text`.
- **Section adjustment in pipeline, not normalizer**: The `_adjust_section_boundaries()` method lives in `PreprocessingPipeline` rather than `LayoutNormalizer`, keeping the normalizer stateless and pure.
- **Constructor injection pattern**: The pipeline class accepts stage instances explicitly, matching the plan's testability requirement while the module-level singleton provides production convenience.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Legacy preprocess_cv_text() missing from preprocessor.py**
- **Found during:** Task 2 test execution
- **Issue:** The initial commit replaced the entire `preprocessor.py` content with the new `PreprocessingPipeline` class, but `cv_extractor.py` imports `preprocess_cv_text` from `app.services.preprocessor`. This caused `ImportError` when running tests that load the FastAPI app via conftest.py.
- **Fix:** Restored the legacy `preprocess_cv_text()` function and its helper functions (`clean_text`, `extract_sections`, `compress_experience`) along with `SECTIONS` and `REDUNDANT_PHRASES` constants. The old and new code coexist in the same module.
- **Files modified:** `backend/app/services/preprocessor.py`
- **Verification:** Import test passes: `from app.services.preprocessor import preprocess_cv_text, PreprocessingPipeline, preprocessing_pipeline`
- **Committed in:** `271cdaf` (amended Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Essential backward compatibility fix. No scope creep.

## Issues Encountered

- **Filesystem mismatch between Windows and WSL**: Files written via the Write tool go to the Windows filesystem (`C:\home\fernandosilvav\...`), but git operates on the WSL filesystem (`/home/fernandosilvav/...`). Required copying files between filesystems before each commit. Same issue as Plan 02.

## User Setup Required

None — no external service configuration required. The pipeline tests use a mocked SectionDetector and do not make real Gemini API calls.

## Next Phase Readiness

- `PreprocessingPipeline` with `process()` method ready for integration into extraction flow
- `preprocessing_pipeline` singleton importable by `cv_processor.py` and `cv_extractor.py`
- Legacy `preprocess_cv_text()` preserved — existing extraction flow continues to work unchanged
- Full test suite (43 tests) passes: `pytest tests/test_preprocessing_schemas.py tests/test_section_detector.py tests/test_noise_filter.py tests/test_layout_normalizer.py tests/test_preprocessor_pipeline.py -x`
- Plan 04 can wire `preprocessing_pipeline.process()` into the CV extraction flow

---

*Phase: 10-advanced-preprocessing*
*Completed: 2026-05-22*
