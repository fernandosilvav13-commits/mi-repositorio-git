# Phase 02: Crossref Page Redesign - Context

**Gathered:** 2026-05-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Redesign the cross-reference file upload and management page using Apple Design System components from Phase 01. Users upload cross-reference data files (PDF/CSV/PPT/DOCX), see them in an artifact-based enriched table, and view match status per file. This is the standalone Crossref page — Wizard integration and export happen in Phases 03 and 04.

Two requirements, both in scope:
- **CRSS-01**: Upload and manage cross-reference files in an Apple-designed page with Tile, FrostedContainer, and PillChip components
- **CRSS-02**: View uploaded files in a clean artifact-based list with match status indicators (matched/unmatched/processing)

</domain>

<decisions>
## Implementation Decisions

### Upload UX Design
- **U-01**: Upload triggered via a dedicated **Upload section Tile** with a visual upload target as the focal point (hero-style, not a floating button or inline drop zone)
- **U-02**: Supports **both drag-and-drop and file picker** interaction
- **U-03**: **Multi-file upload** supported — users can select and upload several files at once
- **U-04**: **Progress per file** shown during upload and parsing (individual status updates)
- **U-05**: Accepted file types displayed as a **compact badge line** below the drop zone (PDF, CSV, PPT, DOCX)
- **U-06**: After upload completes, the new file **animates from the upload zone into the file list** below it

### File List as Artifacts
- **F-01**: Files displayed in an **enriched table** with artifact styling (combines table scanability with Apple aesthetics)
- **F-02**: **Minimal columns** — file name, match status, and actions only
- **F-03**: Table styled as a **frosted glass table** — semi-transparent rows with backdrop-blur, hairline borders, subtle hover effects
- **F-04**: Per-file actions: **delete only** (other actions — view contents, download matched output — belong in Phase 03/04)
- **F-05**: Files sorted **newest first** by default
- **F-06**: Match status shown via **PillChip badges**: green "Matched", amber "Unmatched", blue "Processing"

### the agent's Discretion
- Exact layout of hero Tile (content, heading, subtext)
- Animation implementation for upload-to-list transition
- Empty state copy and illustration approach
- Frosted table exact styling (column widths, row height, responsive breakpoints)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Design System
- `apple/DESIGN.md` — Full Apple design specification (colors, type, components, tokens)
- `frontend/src/components/apple/Tile.tsx` — Tile component with 5 variants (white/parchment/dark/dark-2/dark-3)
- `frontend/src/components/apple/FrostedContainer.tsx` — Frosted glass container (backdrop-blur-md)
- `frontend/src/components/apple/PillChip.tsx` — Pill-shaped chip for status/selection
- `frontend/src/components/apple/ProductCard.tsx` — Artifact product card for gallery views

### Existing Crossref Page
- `frontend/src/app/crossref/page.tsx` — Current crossref page (to be redesigned)
- `backend/app/api/crossref.py` — Existing Crossref API endpoints (POST /upload, GET /files, GET /files/{id}, DELETE /files/{id})
- `backend/app/services/crossref_service.py` — Backend service with file parsing and merge_data
- `backend/app/schemas/crossref.py` — ColumnMapping Pydantic schema

### UX Reference (Phase 01 Pattern)
- `frontend/src/app/extraction/page.tsx` — Museum gallery pattern with hero Tile + gallery + action sections
- `planning/phases/01-frontend-apple-design/01-CONTEXT.md` — Phase 01 design decisions (colors, typography, radii, layout)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Tile** (5 variants) — For upload section hero and file list sections
- **FrostedContainer** — For frosted glass table styling
- **PillChip** — For match status badges (matched/unmatched/processing)
- **ProductCard** — Available if the enriched table needs card-style row elements
- **button, badge, table** — Existing shadcn ui primitives can be restyled with Apple tokens

### Established Patterns
- **Museum gallery page pattern** (extraction page): hero Tile → controls → gallery/grid → action Tile — crossref page can follow this but with a dedicated upload hero + frosted table instead of a gallery grid
- **Dual-navigation shell** (GlobalNav + SubNav) — crossref page already works within this
- **Dual-navigation shell** — crossref page already works within this (layout.tsx renders both)

### Integration Points
- New page replaces `frontend/src/app/crossref/page.tsx` in-place
- Uses existing backend API: `api.crossref.list()`, `api.crossref.upload()`, `api.crossref.delete()`
- File structure: uploads to `uploads/crossref/` directory via backend
- Match status currently not stored in Supabase `crossref_files` table — may need a migration or computed status

</code_context>

<specifics>
## Specific Ideas

- Upload-to-list animation: new file animates from the upload Tile section into the frosted table below, like a card being placed into a collection
- Frosted table should feel like looking through glass at a museum display case — hairline separators, subtle reflections
- PillChip status: green (#34c759) for matched, amber (#ff9500) for unmatched, blue (#007aff) for processing

</specifics>

<deferred>
## Deferred Ideas

- View file contents / columns in a detail pane or modal (Phase 03 Wizard or separate)
- Download matched output per file (Phase 04 Export)
- Trigger manual re-matching from the file list (Phase 03)
- Column mapping configuration on the page (Phase 03 Wizard)
- None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-crossref-page-redesign*
*Context gathered: 2026-05-14*
