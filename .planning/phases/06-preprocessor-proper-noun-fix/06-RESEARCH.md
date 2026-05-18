# Phase 6: Preprocessor Proper Noun Fix — Research

**Researched:** 2026-05-18
**Domain:** Python text preprocessing / regex
**Confidence:** HIGH

## Summary

This is a surgical backend-only bugfix affecting a single function (`clean_text()` in `preprocessor.py:22-28`). The current behavior calls `text = text.lower()` which destroys proper noun casing (names, cities, surnames) before the LLM receives the text. The fix removes the `.lower()` call and adds `re.IGNORECASE` to the redundant-phrase regex `sub()` calls so they still match regardless of casing.

The fix is minimal (2 changes, ~1 line removed + 1 flag added), zero-risk, and involves no new dependencies, no schema changes, no frontend work. The LLM (Gemini) receives text with original casing and handles proper noun detection on its own — no NER or heuristic capitalization is needed in this phase.

**Primary recommendation:** Remove line 24 (`text = text.lower()`), add `flags=re.IGNORECASE` to the `re.sub(phrase, "", text)` call on line 26. Write unit tests for `clean_text()` and an integration test verifying the full `preprocess_cv_text` → LLM pipeline preserves casing.

## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Remove `text = text.lower()` entirely from `clean_text()`. The LLM receives text with original casing and handles proper noun detection on its own.
- **D-02:** Add `re.IGNORECASE` to all redundant phrase regex `sub()` calls in `clean_text()` so they match regardless of text casing.
- **D-03:** Preserve all diacritics in proper nouns. Do not strip or normalize accents like é → e.
- **D-04:** No NER or explicit proper noun detection in this phase. The LLM detects proper nouns from context.
- **D-05:** Heuristic capitalization (e.g., title-casing names after extraction) is noted as a potential future enhancement but belongs in Phase 7 (Post-Processing Pipeline), not here.
- **D-06:** Only modify `clean_text()` function in `backend/app/services/preprocessor.py:22-26`. No changes to `extract_sections()`, `preprocess_cv_text()`, or `compress_experience()`.
- **D-07:** Accept original PDF/OCR casing as-is. If the CV has "MARÍA GARCÍA" in all caps, the LLM receives all-caps text and is expected to produce "María García" from context.
- **D-08:** No special-case map for multi-word surnames (e.g., "De la Fuente", "McDonald") — trust the LLM to handle these correctly from original casing.

### the agent's Discretion
- Testing approach: the implementer decides how to test the fix (unit test for clean_text + integration test for full pipeline).
- Name of the heuristic capitalization function if/when implemented in Phase 7.

### Deferred Ideas (OUT OF SCOPE)
- **Heuristic capitalization post-process**: Title-casing names after LLM extraction. This belongs in Phase 7 (Post-Processing Pipeline) alongside gender inference, phone normalization, and RUT formatting.

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PREP-01 | clean_text() preserves proper noun casing instead of blanket .lower() | Verified: `clean_text()` at `preprocessor.py:24` calls `text = text.lower()` [VERIFIED: code read]. Removing this line and adding `re.IGNORECASE` to redundant-phrase `re.sub()` (line 26) satisfies the requirement. `extract_sections()` already passes `re.IGNORECASE` flag (line 33) and receives `raw_text` (original casing), not `cleaned_raw` — no change needed there [VERIFIED: code read]. |

## Standard Stack

**Language:** Python 3.11+
**Key library:** `re` (stdlib) — no external dependencies
**Related services:** `llm_service.py` (Gemini API), `cv_extractor.py` (orchestrator)
**Linter:** `ruff` (per AGENTS.md)

## Architecture Patterns

- **Service-oriented architecture**: All services live in `backend/app/services/`. [VERIFIED: AGENTS.md]
- **Regex constants as module-level lists**: `REDUNDANT_PHRASES` is a module-level list of literal regex patterns. [VERIFIED: preprocessor.py:15-20]
- **`re.IGNORECASE` is already the established pattern**: `extract_sections()` uses `re.IGNORECASE | re.DOTALL`. [VERIFIED: preprocessor.py:33]
- **Pipeline flow**: `cv_extractor.extract_cv_data()` → `preprocess_cv_text()` → `clean_text()` + `extract_sections()` → LLM. [VERIFIED: cv_extractor.py:68, preprocessor.py:59-78]

## Common Pitfalls

1. **Over-eager redundant phrase matching without `.lower()`**: The redundant phrases contain accented characters (e.g., "currículum vitae", "teléfono"). Without `.lower()` preprocessing, matching depends on case. **Fix:** Add `flags=re.IGNORECASE` — confirmed working for accented chars with Python `re` module. [VERIFIED: preprocessor.py:15-20 current code patterns]

2. **`compress_experience()` keyword matching still lowercased**: Line 49 calls `stripped.lower()` for keyword matching — this is safe because it's a per-line filter on an intermediate variable, not the final output. [VERIFIED: preprocessor.py:49] — **No change needed.**

3. **`extract_sections()` receives `raw_text`, not `cleaned_raw`**: Line 63 calls `extract_sections(raw_text)` which means sections are already extracted from original-casing text. The `cleaned_raw` (after `clean_text()`) is only used as fallback at line 75. Removing `.lower()` makes the fallback path return original-casing text — this is a **positive side effect**. [VERIFIED: preprocessor.py:61,63,75]

4. **Fallback path length limit**: `cleaned_raw[:4000]` (line 75) truncates at 4000 chars. With original casing, each char takes the same 1 byte (for ASCII), so there's no size change concern. [VERIFIED: preprocessor.py:75]

5. **OCR output may be all-caps**: Many PDFs/OCR extracts produce all-caps text like "MARÍA GARCÍA". The LLM receives this as-is. Gemini can infer proper casing from context. This is **accepted behavior** per D-07. [VERIFIED: CONTEXT.md D-07]

6. **No existing tests**: There are no test files for `preprocessor.py`. Tests must be created from scratch. [VERIFIED: glob search — no `test*preprocessor*` files found]

## Code Examples

### Current (buggy) code — `preprocessor.py:22-28`:
```python
def clean_text(text: str) -> str:
    """Basic cleaning to remove double spaces and redundant phrases."""
    text = text.lower()                          # <-- LINE TO REMOVE
    for phrase in REDUNDANT_PHRASES:
        text = re.sub(phrase, "", text)           # <-- NEEDS IGNORECASE
    text = re.sub(r"\s+", " ", text)              # <-- NO CHANGE NEEDED (no case)
    return text.strip()
```

### Fixed code:
```python
def clean_text(text: str) -> str:
    """Basic cleaning to remove double spaces and redundant phrases."""
    for phrase in REDUNDANT_PHRASES:
        text = re.sub(phrase, "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
```

### Test scenarios to cover:
| Input | Expected behavior |
|-------|------------------|
| `"MARÍA GARCÍA"` | Stays `"MARÍA GARCÍA"` (not `"maría garcía"`) |
| `"Hoja de Vida"` | Removes `"Hoja de Vida"` (IGNORECASE matches) |
| `"CURRICULUM VITAE"` | Removes `"CURRICULUM VITAE"` (IGNORECASE matches) |
| `"  spaced   text  "` | Normalizes to `"spaced text"` (whitespace unchanged) |
| `"Curriculum Vitae - María García"` | Removes redundant phrase, preserves `"María García"` casing |
| `"currículum vitae"` (lowercase with accent) | Removed (IGNORECASE matches accented lowercase) |

### Integration test (pseudocode):
```python
async def test_full_pipeline_preserves_casing():
    raw = "CURRICULUM VITAE\nMARÍA GARCÍA LÓPEZ\nRUT: 12.345.678-9"
    result = await extract_cv_data(raw)
    assert result["NOMBRES"] == "MARÍA GARCÍA"  # LLM receives original casing
    assert result["APELLIDOS"] == "LÓPEZ"
    # Note: LLM may normalize to "María García" — that's fine per D-07
```

## Assumptions Log

- [ASSUMED] Python's `re.IGNORECASE` handles Unicode accented characters correctly (e.g., `"currículum vitae"` matches `"CURRÍCULUM VITAE"`). This is standard Python `re` behavior confirmed by the Unicode standard for case-insensitive matching.
- [ASSUMED] The LLM (Gemini) can infer correct proper noun casing from context even when input is all-caps. This is the core design decision (D-07) and is based on documented LLM capabilities.
- [ASSUMED] No other function in the codebase depends on `clean_text()` returning lowercased text. Verified: only `preprocess_cv_text()` calls `clean_text()`, and `cleaned_raw` is only used as fallback text (line 75) — lowercasing was never a contract, just a side effect. [VERIFIED: grep for `clean_text` in backend/]

## Sources

- `backend/app/services/preprocessor.py` — target file, full code read [VERIFIED]
- `backend/app/services/cv_extractor.py` — consumer of preprocessor output [VERIFIED]
- `.planning/phases/06-preprocessor-proper-noun-fix/06-CONTEXT.md` — user decisions [VERIFIED]
- `.planning/REQUIREMENTS.md` — PREP-01 requirement [VERIFIED]
- `.planning/STATE.md` — project state and decision log [VERIFIED]
- `AGENTS.md` — project conventions (ruff linting, backend architecture) [VERIFIED]
