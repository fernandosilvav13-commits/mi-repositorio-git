---
phase: 10-advanced-preprocessing
plan: 02
subsystem: preprocessing
tags: [section-detector, noise-filter, layout-normalizer, google-genai, structured-output, pydantic]

requires:
  - phase: 10-advanced-preprocessing
    plan: 01
    provides: DetectionResponse, SectionBoundary, PreprocessingResult Pydantic models, section-detection prompt YAML
provides:
  - SectionDetector class with Gemini structured output LLM call
  - NoiseFilter class for index-based line removal
  - LayoutNormalizer class for whitespace collapse, section markers, bullet normalization
  - Unit test suite for all three pipeline stages
affects:
  - Plan 03 - PreprocessingPipeline orchestrator (imports all three services)

tech-stack:
  added: []
  patterns:
    - "Module-level singleton pattern matching PromptResolver"
    - "Lazy-initialized genai.Client to allow import without API key"
    - "Pure string manipulation for NoiseFilter and LayoutNormalizer (no I/O)"
    - "Bottom-to-top section marker insertion to preserve line indices"
    - "Anchored regex patterns for bullet detection (Pitfall 4 safeguard)"

key-files:
  created:
    - backend/app/services/section_detector.py
    - backend/app/services/noise_filter.py
    - backend/app/services/layout_normalizer.py
    - backend/tests/test_section_detector.py
    - backend/tests/test_noise_filter.py
    - backend/tests/test_layout_normalizer.py
  modified: []

key-decisions:
  - "Lazy initialization of genai.Client: client created only when detect() is called, not at import time — allows module to be imported and tested without API key"
  - "NoiseFilter uses set[int] for O(1) lookups when checking noisy_lines membership"
  - "LayoutNormalizer inserts section markers bottom-to-top (sorted by start_line descending) to preserve line indices for subsequent insertions"
  - "Bullet patterns anchored to line start (^) with re.MULTILINE flag to prevent false matches on mid-line dashes (Pitfall 4)"
  - "All three stages have no __init__ method (no instance state) — pure function objects"

patterns-established:
  - "Module-level singletons with lazy initialization for API clients"
  - "Test file per stage (D-12): test_section_detector, test_noise_filter, test_layout_normalizer"
  - "Separation of concerns: LLM call (SectionDetector), pure manipulation (NoiseFilter, LayoutNormalizer)"

requirements-completed: [PREP-01, PREP-02]

duration: 30min
completed: 2026-05-22
---

# Phase 10 Plan 02: Preprocessing Pipeline Stage Services Summary

**SectionDetector (LLM-guided section detection), NoiseFilter (index-based line removal), and LayoutNormalizer (whitespace/markers/bullets) — the three building blocks of the multi-stage preprocessing pipeline per D-10**

## Performance

- **Duration:** 30 min
- **Started:** 2026-05-22T15:06:46Z
- **Completed:** 2026-05-22T23:55:25Z
- **Tasks:** 3
- **Files created:** 6
- **Tests passed:** 25 (4 SectionDetector + 9 NoiseFilter + 12 LayoutNormalizer)

## Accomplishments

- Created `SectionDetector` class with `detect()` method:
  - Uses `google-genai` SDK with `response_schema=DetectionResponse` for structured output
  - Integrates with `PromptResolver` to load `section-detection` prompt YAML
  - Lazy-initialized `genai.Client` allows import without API key
  - Empty/whitespace/None text returns `can_identify=False` without API call (T-10-10 mitigation)
  - `response.parsed` returns `DetectionResponse` Pydantic instance directly
  - Raises `RuntimeError` when `response.parsed` is `None`

- Created `NoiseFilter` class with `filter(text, noisy_lines)` method:
  - Removes lines by 0-indexed `set[int]` (O(1) membership check)
  - Optimization: returns text unchanged if `noisy_lines` is empty
  - Handles empty/`None` text gracefully (returns `""`)
  - Docstring documents D-07 noise types: page headers, page numbers, footers, metadata artifacts

- Created `LayoutNormalizer` class with `normalize(text, sections)` method:
  - Implements D-08: collapse inline whitespace, preserve paragraph breaks, insert section markers
  - Implements D-09: standardize bullet points to `"* "`
  - `PARAGRAPH_BREAK = re.compile(r"\n\s*\n")` — detects 2+ newlines with optional whitespace
  - `INLINE_WHITESPACE = re.compile(r"[^\S\n]+")` — matches non-newline whitespace only
  - `BULLET_PATTERNS` anchored to line start (`^`) with `re.MULTILINE` — Pitfall 4 safeguard
  - Section markers inserted **bottom-to-top** (sorted by `start_line` descending) to preserve line indices
  - Handles arbitrary section names dynamically (no hardcoded names)

- Created 25 unit tests, all passing:
  - `test_section_detector.py`: 4 tests (instantiation, constants, singletons, empty text handling)
  - `test_noise_filter.py`: 9 tests (removal, preservation, edge cases, D-07 docstring)
  - `test_layout_normalizer.py`: 12 tests (whitespace, paragraphs, markers, bullets, edge cases)

## Task Commits

Each task committed atomically:

1. **Task 1: Create SectionDetector with Gemini structured output** - `e5e8e27`
   - `backend/app/services/section_detector.py`
   - Lazy initialization of `genai.Client` (Rule 1 fix: SDK validates API key at construction time)

2. **Task 2: Create NoiseFilter and LayoutNormalizer classes** - `a34f799`
   - `backend/app/services/noise_filter.py`
   - `backend/app/services/layout_normalizer.py`

3. **Task 3: Create unit tests for all three stages** - `1d01cbb`
   - `backend/tests/test_section_detector.py`
   - `backend/tests/test_noise_filter.py`
   - `backend/tests/test_layout_normalizer.py`

## Files Created/Modified

- `backend/app/services/section_detector.py` — LLM-guided section detection via google-genai SDK with Pydantic response_schema
- `backend/app/services/noise_filter.py` — Index-based line removal for noise filtering (D-07)
- `backend/app/services/layout_normalizer.py` — Whitespace collapse, section markers, bullet normalization (D-08, D-09)
- `backend/tests/test_section_detector.py` — 4 structural tests for SectionDetector
- `backend/tests/test_noise_filter.py` — 9 tests for NoiseFilter
- `backend/tests/test_layout_normalizer.py` — 12 tests for LayoutNormalizer

## Decisions Made

- **Lazy `genai.Client` initialization**: The google-genai SDK's `genai.Client()` validates the API key at construction time, not at call time. This prevented the module from being imported without an API key present. Fixed by using a global `_client = None` and `_get_client()` helper that creates the client only when `detect()` is called.

- **Bullet character includes `*`**: The test input `  * Item three` uses asterisk as a bullet character. Added `\*` to the bullet pattern character class to normalize existing `*` bullets (removing leading whitespace).

- **`set[int]` for `noisy_lines` parameter**: Using a set instead of list provides O(1) membership checking when filtering lines.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Lazy initialization of genai.Client**
- **Found during:** Task 1
- **Issue:** `genai.Client()` validates the API key at construction time (when the module is imported), not at call time. This caused `ImportError` when trying to import SectionDetector without `GEMINI_API_KEY` in the environment.
- **Fix:** Changed from eager `_client = genai.Client()` at module level to lazy pattern: `_client: genai.Client | None = None` at module level, with `_get_client()` helper that creates the client only when `detect()` is first called.
- **Files modified:** `backend/app/services/section_detector.py`
- **Commit:** `e5e8e27`

**2. [Rule 1 - Bug] Added `*` to bullet pattern character class**
- **Found during:** Task 2 testing
- **Issue:** The test input `  * Item three` uses asterisk as a bullet character, but the original bullet pattern only included `[•●▪➢➤\-–—]` (special bullet chars and dashes). Existing `*` bullets with leading whitespace were not being normalized.
- **Fix:** Added `\*` to the bullet pattern: `re.compile(r"^[\s]*[•●▪➢➤\-–—\*]\s+", re.MULTILINE)`
- **Files modified:** `backend/app/services/layout_normalizer.py`
- **Commit:** `a34f799`

**3. [Rule 1 - Bug] Fixed test splitlines() assumption**
- **Found during:** Task 3 test execution
- **Issue:** `test_preserve_leading_trailing_newlines` assumed `"\nheader\ncontent\nfooter\n".splitlines()` would return 5 elements (including trailing empty string), but `splitlines()` without `keepends=True` does not create an empty element for trailing newlines.
- **Fix:** Rewrote the test to focus on actual behavior: removing specific indices while preserving other content (including leading empty lines).
- **Files modified:** `backend/tests/test_noise_filter.py`
- **Commit:** `1d01cbb`

## Issues Encountered

- **Filesystem mismatch between Windows and WSL**: Files created via Write tool went to Windows filesystem (`C:\home\fernandosilvav\...`), but git runs in WSL (`/home/fernandosilvav/...`). Required copying files between filesystems before commits.
- **Plan 01 files not committed**: Plan 01 was executed in Windows environment without git available. Had to commit Plan 01 files (`preprocessing.py`, `section-detection/v1.0.0.yaml`, `test_preprocessing_schemas.py`) before committing Plan 02 work.

## User Setup Required

To use `SectionDetector.detect()` for actual LLM calls:
- Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable
- The SDK reads these automatically via `genai.Client()` with no arguments

For unit tests (no API calls):
- No setup required — tests verify structure, constants, and non-API logic only

## Next Phase Readiness

- Plan 03 (PreprocessingPipeline) can import:
  - `from app.services.section_detector import SectionDetector, DetectionResponse`
  - `from app.services.noise_filter import NoiseFilter`
  - `from app.services.layout_normalizer import LayoutNormalizer`
- All 25 unit tests pass: `pytest backend/tests/test_section_detector.py backend/tests/test_noise_filter.py backend/tests/test_layout_normalizer.py -x`
- Module imports succeed without API key (lazy client initialization)

## Self-Check: PASSED

| Check | Result |
|-------|--------|
| `backend/app/services/section_detector.py` exists | FOUND |
| `backend/app/services/noise_filter.py` exists | FOUND |
| `backend/app/services/layout_normalizer.py` exists | FOUND |
| `backend/tests/test_section_detector.py` exists | FOUND |
| `backend/tests/test_noise_filter.py` exists | FOUND |
| `backend/tests/test_layout_normalizer.py` exists | FOUND |
| `from app.services.section_detector import SectionDetector` | PASS |
| `from app.services.noise_filter import NoiseFilter` | PASS |
| `from app.services.layout_normalizer import LayoutNormalizer` | PASS |
| `pytest backend/tests/test_noise_filter.py backend/tests/test_layout_normalizer.py -x` | 21/21 PASS |
| `pytest backend/tests/test_section_detector.py -x` | 4/4 PASS |

## Threat Flags

No new threat flags beyond those documented in the plan's threat model:

| Threat | Mitigation Status |
|--------|-------------------|
| T-10-05: LLM response tampering | `response_schema=DetectionResponse` in `GenerateContentConfig` validates structure at SDK boundary |
| T-10-06: API key disclosure | `genai.Client()` reads from environment only; key never hardcoded or logged |
| T-10-07: Jinja2 injection | Document text passed as render context data, not template code |
| T-10-08: ReDoS in bullet patterns | Fixed anchored patterns with no nested quantifiers; bounded repetition only |
| T-10-10: Empty text edge case | `SectionDetector.detect()` returns `can_identify=False` without API call for empty/None/whitespace text |

## Known Stubs

None — all three stages are complete implementations:
- `SectionDetector.detect()` makes actual Gemini API calls via google-genai SDK when text is non-empty
- `NoiseFilter.filter()` has complete index-based removal logic
- `LayoutNormalizer.normalize()` has complete whitespace, marker, and bullet logic

No placeholder content, no hardcoded empty values flowing to downstream consumers.

---

*Phase: 10-advanced-preprocessing*
*Completed: 2026-05-22*
