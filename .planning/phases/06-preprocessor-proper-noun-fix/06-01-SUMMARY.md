---
phase: "06-preprocessor-proper-noun-fix"
plan: "01"
subsystem: "preprocessing"
tags: ["clean_text", "re.IGNORECASE", "proper noun", "pytest", "ruff"]

requires:
  - phase: "05-wizard-reordering"
    provides: "stable wizard flow for testing integration"
provides:
  - "clean_text() without blanket .lower() — preserves proper noun casing"
  - "re.IGNORECASE on redundant phrase removal so CV headers match regardless of input casing"
  - "10 pure-function tests (7 unit + 3 integration) covering all-caps preservation, IGNORECASE matching, whitespace normalization, and full pipeline casing"
  - "Fixed regex alternation ordering in SECTIONS (nombres|nombre, apellidos|apellido) to prevent short-alternation-first bug"
  - "Clean ruff on both source and test files (removed pre-existing unused import)"
affects: ["post-processing", "extraction pipeline", "LLM service"]

tech-stack:
  added: []
  patterns:
    - "Prefer re.IGNORECASE over manual .lower() when redundant phrase removal must be case-insensitive but output must preserve original casing"
    - "Alternation in regex must list longer alternatives before shorter ones (nombres before nombre)"

key-files:
  created:
    - "backend/tests/test_preprocessor.py"
  modified:
    - "backend/app/services/preprocessor.py"

key-decisions:
  - "D-01: clean_text() removes blanket .lower() to preserve proper noun casing in CVs (e.g., MARÍA GARCÍA stays MARÍA GARCÍA)"
  - "D-02: Redundant phrase removal uses re.IGNORECASE so CURRICULUM VITAE and currículum vitae and Hoja de Vida are all removed"
  - "D-03: regex alternation must always place longer pattern first (nombres|nombre -> nombres|nombre) to prevent short-match greediness"

patterns-established:
  - "Case-insensitive text normalization: use re.IGNORECASE on pattern, not .lower() on text"
  - "Test pattern: pure function unit tests + integration tests, no external service calls"

requirements-completed:
  - PREP-01

duration: 8min
completed: 2026-05-17
---

# Phase 06 Plan 01: Fix clean_text() Proper Noun Casing + Add Tests

**Removed blanket `.lower()` from `clean_text()`, added `re.IGNORECASE` to redundant phrase substitution, added 10 pure-function tests verifying proper noun casing survival across the preprocessing pipeline**

## Performance

- **Duration:** 8 min
- **Started:** 2026-05-17T18:27:00Z
- **Completed:** 2026-05-17T18:35:00Z
- **Tasks:** 3
- **Files modified:** 1 (+1 created)

## Accomplishments

- Removed `text = text.lower()` from `clean_text()` — fixes all-caps proper noun destruction
- Added `flags=re.IGNORECASE` to redundant phrase `re.sub()` — CV headers like "CURRICULUM VITAE", "Hoja de Vida", "currículum vitae" all removed regardless of input casing
- Created 10 pure-function tests: 7 unit tests for `clean_text()` and 3 integration tests for `preprocess_cv_text()`
- Fixed pre-existing regex alternation ordering bug in `SECTIONS` (nombres|nombre -> nombres|nombre) so uppercase `NOMBRES:` and `APELLIDOS:` headers are correctly matched
- Removed pre-existing unused `typing.Optional` import (ruff F401)

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix clean_text() in preprocessor.py** - `7501832` (fix)
2. **Task 2: Create unit + integration tests for preprocessor** - `b73ab7a` (test)
3. **Task 3: Verify lint + test + static analysis** - `024bbb4` (chore)

**Plan metadata:** (orchestrator-owned commit)

## Files Created/Modified

- `backend/app/services/preprocessor.py` — Modified: removed `.lower()`, added `re.IGNORECASE` flag, fixed regex alternation order, removed unused import
- `backend/tests/test_preprocessor.py` — Created: 10 tests for clean_text() and preprocess_cv_text()

## Decisions Made

- Removed blanket `.lower()` — proper nouns (names, titles) must preserve original casing from CV documents
- Used `re.IGNORECASE` on the `re.sub()` call rather than `.lower()` on the text — this is the correct pattern for case-insensitive matching while preserving original text

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed regex alternation ordering in SECTIONS patterns**
- **Found during:** Task 2 (Integration tests for preprocess_cv_text)
- **Issue:** The regex alternation `(?:nombre|nombres)` and `(?:apellido|apellidos)` had shorter alternatives first. When matching uppercase input like `"NOMBRES: ..."`, the engine would match `NOMBRE` (via `nombre`), then skip `[:\s]*` (0-width match on `S`), leaving only `S` in the capture group — breaking section extraction entirely.
- **Fix:** Reordered alternations to `(?:nombres|nombre)` and `(?:apellidos|apellido)` — always list longer alternatives first
- **Files modified:** `backend/app/services/preprocessor.py`
- **Verification:** Integration tests test_preprocess_preserves_casing_sections_found and test_preprocess_typical_cv_header now pass
- **Committed in:** `b73ab7a` (Task 2 commit)

**2. [Rule 2 - Missing Critical] Removed unused typing.Optional import**
- **Found during:** Task 3 (ruff verification)
- **Issue:** Pre-existing `from typing import Optional` with no usage in the file — ruff F401 error blocking zero-error criteria
- **Fix:** Removed unused import line
- **Files modified:** `backend/app/services/preprocessor.py`
- **Verification:** `ruff check backend/app/services/preprocessor.py` exits 0
- **Committed in:** `024bbb4` (Task 3 commit)

---

**Total deviations:** 2 auto-fixed (1 bug, 1 missing critical)
**Impact on plan:** Both fixes necessary for acceptance criteria compliance. No scope creep.

## Issues Encountered

- The existing test suite had 3 pre-existing failures in `test_excel_styling.py` and `test_export_api.py` (all documented as "expected to fail" in their comments). These are unrelated to preprocessor changes — zero regressions introduced.
- The entire `backend/` has 54 pre-existing ruff violations across other files — these are out of scope per scope boundary rule.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `clean_text()` now preserves proper noun casing and removes redundant phrases case-insensitively
- 10 tests cover the critical paths through the preprocessing pipeline
- Ready for Phase 07: Post-processing (gender inference, phone normalization, RUT formatting)

## Self-Check: PASSED

| Check | Result |
|-------|--------|
| preprocessor.py exists | YES |
| test_preprocessor.py exists | YES |
| `.lower()` removed from preprocessor.py | YES |
| `re.IGNORECASE` present in preprocessor.py | YES |
| `Optional` import removed | YES |
| Commit 7501832 exists | YES |
| Commit b73ab7a exists | YES |
| Commit 024bbb4 exists | YES |
| `ruff check` passes on preprocessor.py | YES |
| `ruff check` passes on test_preprocessor.py | YES |
| pytest 10/10 passes | YES |

---

*Phase: 06-preprocessor-proper-noun-fix*
*Completed: 2026-05-17*
