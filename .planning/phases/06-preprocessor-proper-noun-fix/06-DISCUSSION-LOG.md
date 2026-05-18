# Phase 6: Preprocessor Proper Noun Fix - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-17
**Phase:** 6-Preprocessor Proper Noun Fix
**Areas discussed:** Casing Strategy, Detection Approach, Scope Boundary, Edge Cases

---

## Casing Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Remove .lower() entirely | Remove the line entirely. The LLM receives text with original casing and handles proper noun detection on its own. Simplest fix. | ✓ |
| Conditional lowercase | Only lowercase non-proper-noun sections but keep names/cities as-is | |
| Title Case after processing | Keep lowercasing then apply title-case heuristics at the end | |

**User's choice:** Remove .lower() entirely
**Notes:** Chose simplest approach — let LLM handle casing

| Option | Description | Selected |
|--------|-------------|----------|
| Make regex case-insensitive | Add re.IGNORECASE to redundant phrase regex patterns instead of depending on lowercased text | ✓ |
| Use casefold() on pattern search only | Normalize for matching only, keep text unchanged | |
| Drop redundant phrases entirely | Simplify code, LLM can handle them | |

**User's choice:** Make regex case-insensitive
**Notes:** Redundant phrase removal should still work, just with IGNORECASE flag

| Option | Description | Selected |
|--------|-------------|----------|
| Preserve all diacritics | Don't strip or normalize accents. The LLM handles accented characters fine | ✓ |
| NFD normalize | Decompose accents for matching but keep visual output | |
| Strip and let LLM restore | Strip diacritics, let LLM infer accented form | |

**User's choice:** Preserve all diacritics
**Notes:** Names like "María José" should keep their accents

---

## Detection Approach

| Option | Description | Selected |
|--------|-------------|----------|
| Just remove .lower() — simplest | The LLM receives text with original casing. No detection code needed | |
| Add heuristic capitalization | Capitalize first letter of each word in name sections after cleaning | |
| Add NER-based approach | Use spaCy to detect proper nouns | |

**User's choice:** Add heuristic capitalization
**Notes:** Wants heuristic capitalization but as a post-process after LLM extraction (Phase 7), not in the preprocessor

| Option | Description | Selected |
|--------|-------------|----------|
| Only on known name sections | Apply capitalization only to 'nombres' and 'apellidos' regex sections | |
| On the full preprocessed text | Run capitalization pass over entire output | |
| As a post-process after LLM extraction | Capitalize names after LLM extraction in result fields | ✓ |

**User's choice:** As a post-process after LLM extraction
**Notes:** Deferred to Phase 7 (Post-Processing Pipeline)

---

## Scope Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Only clean_text() | Remove .lower(), add IGNORECASE. Minimal change, minimal risk | ✓ |
| clean_text() + preprocess_cv_text() refactor | Also clean up preprocess_cv_text() composition | |
| Full preprocessor audit | Review and clean up entire preprocessor.py | |

**User's choice:** Only clean_text()
**Notes:** Minimal scope — fix the one bug, nothing else

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, include IGNORECASE in clean_text() | Add re.IGNORECASE to the sub() calls inside clean_text() | ✓ |
| No, only remove .lower() | Just delete the .lower() line, phrase patterns may miss uppercase matches | |

**User's choice:** Yes, include IGNORECASE in clean_text()
**Notes:** The IGNORECASE on redundant phrase patterns is part of the same fix scope

---

## Edge Cases

| Option | Description | Selected |
|--------|-------------|----------|
| Accept original PDF/OCR casing | Whatever casing the PDF/OCR produces is what the LLM receives | ✓ |
| Add special-case map | Maintain override dictionary for known special patterns | |
| Title-case the name sections | Apply .title() to name sections | |

**User's choice:** Accept original PDF/OCR casing
**Notes:** Trust the LLM to handle multi-word surnames, "McDonald", etc.

| Option | Description | Selected |
|--------|-------------|----------|
| Let LLM handle it | LLM receives "MARÍA GARCÍA" (all caps) and properly cases it | ✓ |
| Add smart downcasing | Detect all-caps text blocks and apply Spanish-aware title-case | |

**User's choice:** Let LLM handle it
**Notes:** The success criteria specifies that "MARÍA GARCÍA" should output "María García". The LLM can do this from context without extra code.

---

## the agent's Discretion

- Testing approach for the fix
- Name of heuristic capitalization function in Phase 7

## Deferred Ideas

- **Heuristic capitalization post-process**: Title-casing names after LLM extraction. This belongs in Phase 7 (Post-Processing Pipeline) alongside gender inference, phone normalization, and RUT formatting.
