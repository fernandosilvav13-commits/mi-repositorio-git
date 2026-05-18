# Phase 6: Preprocessor Proper Noun Fix - Context

**Gathered:** 2026-05-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix `clean_text()` in the preprocessor to preserve proper noun casing instead of blanket lowercasing. The function currently does `text = text.lower()`, which damages names (NOMBRES, APELLIDOS) before LLM extraction. The fix is minimal — remove the `.lower()` call and make the redundant-phrase removal case-insensitive.

</domain>

<decisions>
## Implementation Decisions

### Casing Strategy
- **D-01:** Remove `text = text.lower()` entirely from `clean_text()`. The LLM receives text with original casing and handles proper noun detection on its own.
- **D-02:** Add `re.IGNORECASE` to all redundant phrase regex `sub()` calls in `clean_text()` so they match regardless of text casing.

### Diacritics
- **D-03:** Preserve all diacritics in proper nouns. Do not strip or normalize accents like é → e.

### Detection Approach
- **D-04:** No NER or explicit proper noun detection in this phase. The LLM detects proper nouns from context.
- **D-05:** Heuristic capitalization (e.g., title-casing names after extraction) is noted as a potential future enhancement but belongs in Phase 7 (Post-Processing Pipeline), not here.

### Scope Boundary
- **D-06:** Only modify `clean_text()` function in `backend/app/services/preprocessor.py:22-26`. No changes to `extract_sections()`, `preprocess_cv_text()`, or `compress_experience()`.

### Edge Cases
- **D-07:** Accept original PDF/OCR casing as-is. If the CV has "MARÍA GARCÍA" in all caps, the LLM receives all-caps text and is expected to produce "María García" from context.
- **D-08:** No special-case map for multi-word surnames (e.g., "De la Fuente", "McDonald") — trust the LLM to handle these correctly from original casing.

### the agent's Discretion
- Testing approach: the implementer decides how to test the fix (unit test for clean_text + integration test for full pipeline).
- Name of the heuristic capitalization function if/when implemented in Phase 7.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — PREP-01: clean_text() preserves proper noun casing

### Codebase
- `backend/app/services/preprocessor.py` — The target file containing `clean_text()` (line 22) and `preprocess_cv_text()` (line 59)
- `backend/app/services/cv_extractor.py` — Consumer of preprocessor output, calls `preprocess_cv_text()` at line 68 and feeds result to LLM
- `.planning/ROADMAP.md` — Phase 6 goal and success criteria

</canonical_refs>

<code_context>
## Existing Code Insights

### Current Bug
- `backend/app/services/preprocessor.py:24`: `text = text.lower()` — the line to remove
- `REDUNDANT_PHRASES` list (line 8-12): patterns currently rely on lowercased text to match; need `re.IGNORECASE` flag
- `extract_sections()` (line 30): already uses `re.IGNORECASE` and returns original-casing values from `raw_text` — no change needed
- Fallback path: `if not parts: return cleaned_raw[:4000]` — this was returning lowercased text; after fix, returns original-casing text

### Established Patterns
- Service-oriented architecture: `backend/app/services/`
- Regex-based extraction with `re.IGNORECASE` flag
- Module-level constants for patterns (REDUNDANT_PHRASES, SECTIONS)

### Integration Points
- `cv_extractor.py:extract_cv_data()` receives preprocessed text and sends to LLM
- `llm_service.py:extract_fields()` receives the processed text
- No UI/frontend changes needed — purely backend

</code_context>

<specifics>
## Specific Ideas

- The fix should be a surgical removal of `.lower()` + adding `re.IGNORECASE` to the three `re.sub` calls in `clean_text()`
- The whitespace normalization (`re.sub(r"\s+", " ", text)`) and strip should stay unchanged

</specifics>

<deferred>
## Deferred Ideas

- **Heuristic capitalization post-process**: Title-casing names after LLM extraction. This belongs in Phase 7 (Post-Processing Pipeline) alongside gender inference, phone normalization, and RUT formatting.

</deferred>

---

*Phase: 6-Preprocessor Proper Noun Fix*
*Context gathered: 2026-05-17*
