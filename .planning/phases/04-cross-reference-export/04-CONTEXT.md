# Phase 04: Cross-Reference Export - Context

**Gathered:** 2026-05-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Consolidate the cross-reference feature by ensuring the exported Excel file reflects the matched data accurately. This involves updating the backend `merge_data` logic to support the compound match keys introduced in the Wizard (Phase 03) and enhancing the `ExcelService` to visually highlight rows that failed to match any cross-reference data.

Requirements:
- **EXP-01**: Exported Excel includes cross-referenced data columns from matched rows.
- **EXP-02**: Unmatched rows are visually flagged in the exported output (e.g., cell background color).

</domain>

<decisions>
## Implementation Decisions

### Backend Logic Update
- **B-01**: Support **compound match keys** in `CrossrefService.merge_data()`. Instead of single `match_column`, it should accept a list of mapping pairs (Extraction Field ↔ Crossref Field).
- **B-02**: Update `api/export.py` to handle the new `matchKeys` structure from the Wizard payload (which replaced `match_column` in Phase 03).

### Visual Flagging in Excel
- **V-01**: Use a **specific fill color** (e.g., light yellow or amber) for rows that have no cross-reference match.
- **V-02**: A row is considered "unmatched" if a cross-reference file was provided but no match was found (i.e., columns were filled with `NO ENCONTRADO`).
- **V-03**: Add a **secondary header** or prefix to cross-reference columns in Excel to clearly distinguish them from extraction results (e.g., "[REF] Column Name").

### the agent's Discretion
- The exact RGB value for the "unmatched" fill color (recommend amber/light yellow to distinguish from "critical failure" red).
- Whether to flag the entire row or only the cross-reference cells (decided: flag the entire row for better visibility).
- Formatting of the "[REF]" prefix in headers.

</decisions>

<canonical_refs>
## Canonical References

### Backend
- `backend/app/services/crossref_service.py` — `merge_data()` needs update for compound keys.
- `backend/app/services/excel_service.py` — `generate()` needs update for visual flagging of unmatched rows.
- `backend/app/api/export.py` — Main entry point for export, needs to adapt to Phase 03 payload.

### Frontend (Context only)
- `frontend/src/app/wizard/page.tsx` — Check `handleExport` to see the structure of `matchKeys` being sent.
- `frontend/src/components/apple/MatchKeySelector.tsx` — Structure of the match key pairs.

</canonical_refs>

<code_context>
## Existing Code Insights

### Crossref Matching
- `CrossrefService.merge_data()` currently takes `match_column` and `crossref_match_column` as strings.
- The Wizard (Phase 03) now stores `matchKeys` as an array of objects: `{ extractionKey: string, crossrefKey: string }`.

### Excel Styling
- `ExcelService` already has constants for `RED_FILL`, `GREEN_FILL`, `YELLOW_FILL`.
- `YELLOW_FILL` (line 9) is already defined as `FFFF44`. This is perfect for "unmatched" flagging.
- `NO_ENCONTRADO_TEXT` is "NO ENCONTRADO".

### Export Payload
- The Wizard `handleExport` (Phase 03) sends:
  ```json
  {
    "template_id": "...",
    "rows": [...],
    "crossref_file_id": "...",
    "column_mapping": {
       "matchKeys": [{ "extractionKey": "...", "crossrefKey": "..." }],
       "output_columns": ["...", "..."]
    }
  }
  ```

</code_context>

<specifics>
## Specific Ideas

- **Consolidation**: Since rows are already consolidated by RUT (in `consolidator.py`), the merge logic must ensure it works with consolidated data.
- **Header Styling**: Apply a different header color (e.g., a lighter blue or green) to cross-reference columns to make them stand out.

</specifics>

---

*Phase: 04-cross-reference-export*
*Context gathered: 2026-05-15*
