# Phase 04: Cross-Reference Export - Research

**Researched:** 2026-05-15
**Domain:** Data Integration & Excel Export
**Confidence:** HIGH

## Summary

This research establishes the technical path for integrating cross-reference data into the Excel export process. The primary challenge is transitioning from a single-column match to a **compound match key** system (supporting multiple column pairs) and providing visual cues in the resulting Excel file to distinguish matched vs. unmatched data.

The solution involves updating the `CrossrefService` to handle complex lookups, modifying `api/export.py` to support the new Wizard payload, and enhancing `ExcelService` with conditional styling and header prefixing.

**Primary recommendation:** Use composite key tuples for efficient O(1) matching in Python and leverage `openpyxl`'s `PatternFill` for row highlighting.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Payload construction | Browser (Frontend) | — | The Wizard step 2 collects mapping; must send `matchKeys` array to API. |
| Data Consolidation | API (Backend) | Consolidator | Rows must be merged by RUT *before* cross-referencing to ensure one row per person. |
| Compound Merging | API (Backend) | CrossrefService | Logic for matching extraction results with cross-reference rows using multiple keys. |
| Excel Generation | API (Backend) | ExcelService | Creating the .xlsx file with specific styling and prefixes. |
| Visual Flagging | API (Backend) | ExcelService | Applying background colors based on match status. |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| openpyxl | 3.1.5 | Excel generation | Python industry standard for .xlsx manipulation. |
| pandas | 2.2.x | File parsing | Used by CrossrefService for robust CSV/Excel parsing. |
| FastAPI | 0.104.1 | Backend API | Current project framework. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|--------------|
| rapidfuzz | 3.14.5 | Fuzzy matching | Already in project; can be used if exact matching fails. |

**Installation:**
```bash
pip install openpyxl pandas rapidfuzz
```

**Version verification:**
- `openpyxl`: 3.1.5 (Verified via `pip show`)
- `fastapi`: 0.104.1 (Verified via `pip show`)

## Architecture Patterns

### Recommended Project Structure
```
backend/app/
├── api/
│   └── export.py            # Entry point: coordinates consolidation -> merge -> generate
├── services/
│   ├── consolidator.py     # Group rows by RUT
│   ├── crossref_service.py  # Merge logic with compound keys
│   └── excel_service.py     # Excel styling (fills, headers, prefixes)
```

### Pattern 1: Composite Lookup Keys
**What:** Create a hashable composite key for O(1) lookups in cross-reference data.
**When to use:** When matching requires multiple columns (e.g., Name + Date of Birth).
**Example:**
```python
# Create lookup
lookup = {}
for row in crossref_rows:
    key = tuple(str(row.get(k, "")).strip().lower() for k in crossref_keys)
    lookup[key] = row

# Match
row_key = tuple(str(row.get(k, "")).strip().lower() for k in extraction_keys)
matched = lookup.get(row_key)
```

### Anti-Patterns to Avoid
- **Nested Loops for Matching:** Do NOT use O(N*M) loops. Always build a hash map (dictionary) first for O(N+M) performance.
- **Frontend-only Merging:** While useful for preview, the final merge MUST happen on the backend to ensure data integrity in the exported file.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Excel styling | Custom XML generation | `openpyxl.styles` | Handles complex cell formatting, colors, and borders correctly. |
| CSV parsing | String splitting | `pandas.read_csv` | Handles encodings, delimiters, and quoted fields automatically. |

## Common Pitfalls

### Pitfall 1: Type Mismatch in Keys
**What goes wrong:** A RUT in a CSV might be `12345` (int) while in extraction it's `"12345"` (str).
**How to avoid:** Always cast keys to `str`, `strip()`, and `lower()` before comparison.

### Pitfall 2: Memory Bloat with Large Reference Files
**What goes wrong:** Loading a 100MB cross-reference file into memory for every export.
**How to avoid:** `load_file_data` currently loads the full file. Since this is a single-user tool, it's acceptable for now, but in Phase 05+ it should use chunking or DB indexing.

### Pitfall 3: Header Collision
**What goes wrong:** Cross-reference column "Nombre" collides with extraction column "Nombre".
**How to avoid:** Use the `[REF]` prefix for cross-reference headers to ensure uniqueness.

## Code Examples

### Compound Key Merging (CrossrefService)
```python
def merge_data(self, rows, crossref_rows, match_keys, output_columns):
    # match_keys: [{"extractionKey": "k1", "crossrefKey": "c1"}, ...]
    ext_keys = [m["extractionKey"] for m in match_keys]
    ref_keys = [m["crossrefKey"] for m in match_keys]
    
    lookup = {}
    for cr_row in crossref_rows:
        key = tuple(str(cr_row.get(k, "")).strip().lower() for k in ref_keys)
        lookup[key] = cr_row
        
    for row in rows:
        row_key = tuple(str(row.get(k, "")).strip().lower() for k in ext_keys)
        matched = lookup.get(row_key)
        # Apply output_columns with fallback to "NO ENCONTRADO"
```

### Visual Flagging (ExcelService)
```python
# apply yellow fill to entire row if unmatched
if is_unmatched:
    for cell in ws[row_idx]:
        cell.fill = YELLOW_FILL
```

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Payload uses `matchKeys` array | Summary | Frontend might still be sending single columns if not updated in sync. |
| A2 | Consolidation by RUT is sufficient | Summary | Users might want to consolidate by other keys (e.g., Email). |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| openpyxl | Excel generation | ✓ | 3.1.5 | — |
| pandas | Crossref parsing | ✓ | 2.2.x | — |
| FastAPI | API endpoints | ✓ | 0.104.1 | — |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (to be installed) |
| Config file | backend/pytest.ini |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| EXP-01 | Data from cross-ref is in Excel | Integration | `pytest tests/test_export.py` | ❌ Wave 0 |
| EXP-02 | Unmatched rows are yellow | UI/Logic | `pytest tests/test_excel_styles.py` | ❌ Wave 0 |

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V5 Input Validation | yes | Validate that requested columns exist in template and cross-ref file. |
| V12 File Upload | yes | Filename sanitization and extension validation (already implemented). |

### Known Threat Patterns for Data Integration

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Injection via CSV | Tampering | Sanitize data before writing to Excel; avoid formula injection (`=`, `@`, `+`, `-`). |

## Sources

### Primary (HIGH confidence)
- `backend/app/services/crossref_service.py` - Analyzed current merge logic.
- `backend/app/services/excel_service.py` - Analyzed current styling logic.
- `04-CONTEXT.md` - Verified phase requirements and decisions.

### Secondary (MEDIUM confidence)
- `frontend/src/app/wizard/page.tsx` - Analyzed `handleExport` payload structure.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Libraries already in use.
- Architecture: HIGH - Clear mapping of responsibilities.
- Pitfalls: MEDIUM - Dependent on user file quality.

**Research date:** 2026-05-15
**Valid until:** 2026-06-14
