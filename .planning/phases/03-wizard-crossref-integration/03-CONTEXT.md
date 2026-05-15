# Phase 03: Wizard Cross-Reference Integration - Context

**Gathered:** 2026-05-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Integrate cross-reference data matching into the Wizard flow. Users upload a cross-reference file (CSV/PDF/PPT/DOCX) at step 2 of the Wizard, configure column mapping between extraction result fields and cross-reference fields, and see matched/unmatched results previewed in the review step before export. The Wizard connects to the existing backend CrossrefService (semantic_match, merge_data, parse_file) and the existing export endpoint (which already accepts crossref_file_id and column_mapping).

Three requirements, all in scope:
- **WIZ-01**: User can upload a cross-reference file as a step in the Wizard flow
- **WIZ-02**: User can configure column mapping between extraction results and cross-reference fields in the Wizard
- **WIZ-03**: User can preview matched vs unmatched results within the Wizard before finalizing export

</domain>

<decisions>
## Implementation Decisions

### Preview UX for Match Results
- **P-01**: Preview displayed as a **summary with drill-down** — show counts ("X matched, Y unmatched") with ability to expand into detailed sections
- **P-02**: On drill-down, rows shown in **two separate sections**: "Matched" (merged data) and "Unmatched" (extraction rows with no match, shown with blank crossref columns)
- **P-03**: Match determination based on **any extraction column** of the user's choice (not limited to a primary key like RUT)

### Column Mapping UX
- **M-01**: Output column selection uses **smart suggestion with override** — system suggests crossref columns likely wanted based on name overlap with extraction template columns, user can adjust
- **M-02**: Match key selection uses **single shared field with auto-map** — if both extraction and crossref have a column with the same name (e.g., "RUT"), auto-suggest the match
- **M-03**: **Multiple match keys** supported for compound matching (e.g., RUT + Name)

### Wizard Flow Position
- **F-01**: Cross-reference step stays at **step 2** (current position — right after upload, before template)
- **F-02**: All column mapping configuration happens **at step 2 with file selection** — user uploads file, sets match keys and output columns at once

### Matching Strategy
- **S-01**: **Always semantic matching** — use Gemini AI via CrossrefService.semantic_match() for all matching, not exact matching first
- **S-02**: Semantic matching runs **during extraction** (not on-demand or during preview)

### Match Preview Timing
- **T-01**: Match results shown as **part of the review step** (final Wizard step) alongside extraction quality review
- **T-02**: If user changes column mapping and re-enters review, **re-run matching automatically** (no manual "Re-match" button needed)

### the agent's Discretion
- Exact layout of the summary counts display (pill-style counters, bar, etc.)
- Animation for expand/collapse drill-down sections
- Auto-map heuristic specifics (which name similarity threshold triggers auto-suggest)
- "Smart suggestion" column selection algorithm details
- Empty state when no crossref file uploaded but crossref is "enabled"
- Edge case: user has crossref enabled but no crossref files available

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Wizard
- `frontend/src/app/wizard/page.tsx` — Current Wizard page with existing crossref step (upload, column selection, export hooks). The new crossref integration builds on this.
- `frontend/src/components/apple/ConfiguratorCard.tsx` — ConfiguratorCard component used for Wizard step content

### Backend Crossref Service
- `backend/app/services/crossref_service.py` — CrossrefService with semantic_match(), parse_file(), merge_data(), load_file_data()
- `backend/app/api/crossref.py` — Crossref API endpoints (POST /upload, GET /files, GET /files/{id}, DELETE /files/{id})
- `backend/app/schemas/crossref.py` — ColumnMapping Pydantic schema
- `backend/app/services/export.py` — Export endpoint that already accepts crossref_file_id and column_mapping

### Design System
- `frontend/src/components/apple/PillChip.tsx` — PillChip with variant="status" for matched/unmatched/processing badges
- `frontend/src/components/apple/FrostedContainer.tsx` — Frosted glass container for preview sections
- `frontend/src/components/apple/Tile.tsx` — Tile component (for potential preview section containers)
- `apple/DESIGN.md` — Apple design specification (colors, type, components, tokens)

### Phase Context
- `.planning/phases/02-crossref-page-redesign/02-CONTEXT.md` — Phase 02 design decisions (upload UX, file list, match status)
- `.planning/phases/02-crossref-page-redesign/02-SUMMARY.md` — Phase 02 implementation results

### Integration Points (from export)
- `frontend/src/app/export/page.tsx` — Existing export page that can accept crossref parameters

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **ConfiguratorCard** — Already used for all Wizard steps. New crossref sub-steps should use the same pattern.
- **PillChip (status variant)** — Ready for matched/unmatched/processing status indicators in preview
- **FrostedContainer** — For frosted glass preview sections in the review step
- **CrossrefService.semantic_match()** — Already implemented, takes query_data, candidates, output_columns
- **CrossrefService.merge_data()** — Already implemented, merges crossref data with extraction results
- **export endpoint** — Already accepts crossref_file_id + column_mapping in payload

### Established Patterns
- **Wizard sub-step pattern**: Steps with multiple sub-steps use `subStep` state counter + conditional rendering (`currentStep === "crossref" && subStep === N`)
- **Product Configurator flow**: Each Wizard step is a ConfiguratorCard inside a stepped navigation
- **Export with crossref**: Current Wizard handleExport already constructs crossref_file_id + column_mapping payload
- **Data fetching pattern**: useEffect on mount fetches api.crossref.list(), api.templates.list(), api.rules.list()

### Integration Points
- New crossref sub-steps added within existing `currentStep === "crossref"` render block in wizard/page.tsx
- Preview UI added within the review step (`currentStep === "review"` block)
- Matching triggered during extraction (`handleExtract`) by passing crossref config to the extraction call, or via a separate merge call after extraction completes
- Column mapping stored in Wizard state for passing to export payload

</code_context>

<specifics>
## Specific Ideas

- Summary display in review step: pill-style counters showing "245 matched" (green) and "12 unmatched" (amber), expandable into sections
- Matched section: table with extraction columns + crossref columns side by side, green tinted header
- Unmatched section: table with extraction columns only, amber tinted header, blank crossref columns
- Auto-map heuristic: if extraction column name normalized matches crossref column name (case-insensitive, trimmed), auto-suggest as match key
- Smart suggestion: suggest crossref columns that DON'T appear in the extraction template as output columns (avoids duplication)

</specifics>

<deferred>
## Deferred Ideas

- Manual re-match button after mapping changes (decided: auto re-match on change instead)
- Separate dedicated preview step between Extract and Export (decided: part of review step instead)
- User choice between exact and semantic matching (decided: always semantic)
- Download matched output per file (Phase 04 — Cross-Reference Export)

</deferred>

---

*Phase: 03-wizard-crossref-integration*
*Context gathered: 2026-05-15*
