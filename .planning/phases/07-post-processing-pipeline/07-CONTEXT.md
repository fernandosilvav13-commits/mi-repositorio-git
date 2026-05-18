# Phase 7: Post-Processing Pipeline - Context

**Gathered:** 2026-05-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Add post-processing to `CVProcessor.process()` that applies gender inference, phone normalization, and RUT formatting after LLM extraction. Only overrides fields the LLM left as "NO ENCONTRADO" or empty. Also adds heuristic name capitalization for all-caps names.

Covers requirements POST-01, POST-02, POST-03, POST-04.

</domain>

<decisions>
## Implementation Decisions

### Post-Processing Location
- **D-01:** Wire post-processing directly inside `CVProcessor.process()` — after `extract_cv_data()` returns and after experience enrichment. The imports (`infer_gender`, `normalize_phone`, `RUTFormatter`) already exist in `cv_processor.py`, they just need to be called.

### Override Behavior
- **D-02:** Per-field check. Each field evaluated independently:
  - If `data.get("GENERO")` is "NO ENCONTRADO" or empty → call `infer_gender(data.get("NOMBRES"))`
  - If `data.get("RUT")` is "NO ENCONTRADO" or empty → call `RUTFormatter.format()` on available RUT data
  - If `data.get("TELEFONO_FIJO")` / `TELEFONO_CELULAR` is "NO ENCONTRADO" or empty → call `normalize_phone()` on the raw text
- Do NOT overwrite valid LLM output. If the LLM successfully extracted a field, leave it untouched.

### RUT Output Format
- **D-03:** Use `RUTFormatter.format(value, "con_puntos_y_guion")` — Chilean standard format (12.345.678-9). This is already the default format.

### Name Capitalization (from Phase 06 D-05)
- **D-04:** Include heuristic name capitalization in this phase. Title-case NOMBRES and APELLIDOS after LLM extraction:
  - `"MARÍA GARCÍA"` → `"María García"`
  - `"juan pérez"` → `"Juan Pérez"`
  - Preserve existing diacritics (accented characters stay as-is)
  - Must handle multi-word names correctly
- Name of the function is left to the implementer's discretion (e.g., `titlecase_name()`, `capitalize_name()`).

### Phone Extraction Scope
- **D-05:** (Agent discretion) Normalize phone numbers the LLM already extracted using `normalize_phone()`. Searching raw text for phones the LLM missed is optional — defer to implementer judgment.

### the Agent's Discretion
- Phone extraction scope: `normalize_phone()` on LLM-extracted phones is mandatory; `extract_phone_from_text()` on raw text is optional
- Name capitalization function name and exact implementation approach
- Experience enrichment via `get_top_3_experiences()` — keep existing behavior, no changes needed

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — POST-01 (gender), POST-02 (phone), POST-03 (RUT), POST-04 (override only when missing)

### Codebase
- `backend/app/services/cv_processor.py` — Target file where post-processing is wired into `process()` method
- `backend/app/services/gender_service.py` — Contains `infer_gender(nombres)` and GENDER_MAP lookup
- `backend/app/services/phone_service.py` — Contains `normalize_phone(raw)` and `extract_phone_from_text(text)`
- `backend/app/utils/rut_formatter.py` — Contains `RUTFormatter.format(value, fmt)` class
- `backend/app/services/cv_extractor.py` — `extract_cv_data()` is called before post-processing; EXTRACTION_SCHEMA has the field names
- `backend/app/services/preprocessor.py` — Phase 06 fix ensures proper noun casing preserved before LLM

### Phase Context
- `.planning/phases/06-preprocessor-proper-noun-fix/06-CONTEXT.md` — D-05 defers name capitalization to Phase 07

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `gender_service.py:infer_gender(nombres)` — Name-based gender lookup using GENDER_MAP (already imported in cv_processor.py)
- `gender_service.py:infer_gender_from_text(text)` — Text-based gender detection from keywords (optional secondary check)
- `phone_service.py:normalize_phone(raw)` — Normalizes Chilean phone numbers to +569/+56 format (already imported in cv_processor.py)
- `phone_service.py:extract_phone_from_text(text)` — Regex-based phone extraction from raw text (optional)
- `rut_formatter.py:RUTFormatter.format(value, fmt)` — RUT formatting with 3 format options (already imported in cv_processor.py)

### Established Patterns
- Service-oriented architecture in `backend/app/services/`
- Post-processing runs inside `CVProcessor.process()` after LLM extraction and experience enrichment
- Functions return "NO ENCONTRADO" for missing values (consistent sentinel across services)
- Existing imports in cv_processor.py are already correct but unused — just need to wire the calls

### Integration Points
- `cv_processor.py:CVProcessor.process()` — Entry point; adds post-processing after `extract_cv_data()` and `get_top_3_experiences()`
- The `EXTRACTION_SCHEMA` in `cv_extractor.py` includes all target fields (GENERO, TELEFONO_FIJO, TELEFONO_CELULAR, RUT, NOMBRES)
- No frontend changes needed — purely backend pipeline work

</code_context>

<specifics>
## Specific Ideas

- The wiring is minimal: ~10 lines of code in `cv_processor.py:process()` after the experience enrichment block
- Name capitalization should handle: all-caps, mixed-case, accented chars, and multi-word surnames
- Test pattern: follow the pattern from Phase 06 tests (pure function unit tests + integration tests for the full pipeline)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 7-Post-Processing Pipeline*
*Context gathered: 2026-05-18*
