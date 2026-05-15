# Phase 02: Crossref Page Redesign - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-14
**Phase:** 02-crossref-page-redesign
**Areas discussed:** Upload UX Design, File List as Artifacts

---

## Upload UX Design

| Option | Description | Selected |
|--------|-------------|----------|
| Floating bar button | Like extraction's "Add Artifacts" — frosted pill bar at the top | |
| Always-visible drop zone | Dedicated frosted drop zone on a Tile, always visible | |
| Upload section Tile | Dedicated full-width section with visual upload target as focal point | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Drag-and-drop + picker | Visual drop zone accepts drag-and-drop, also clickable | ✓ |
| File picker only | Simple button that opens native file dialog | |

| Option | Description | Selected |
|--------|-------------|----------|
| Single file | One file per upload action | |
| Multiple files | Select and upload several files at once | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Silent + toast | Background upload, toast notification on completion | |
| Progress per file | Show each file's upload/parse progress inline | ✓ |
| Upload queue | Dedicated queue area with individual progress bars | |

| Option | Description | Selected |
|--------|-------------|----------|
| More questions | Continue discussing Upload UX | ✓ |
| Next area | Move to File List as Artifacts | |

| Option | Description | Selected |
|--------|-------------|----------|
| Compact badge line | Small badges below drop zone: "PDF, CSV, PPT, DOCX" | ✓ |
| Expanded helper | List each format with description | |
| Minimal | Just the drop zone, user discovers formats via file picker | |

| Option | Description | Selected |
|--------|-------------|----------|
| Stay + notification | Stay on upload section, toast confirms success | |
| Auto-scroll to list | Auto-scroll to file list after upload completes | |
| Animate into list | New file animates from upload zone into list below | ✓ |

**User's choice:** Upload section Tile, drag-and-drop + picker, multi-file, progress per file, compact badge line, animate into list
**Notes:** User wanted the strongest visual hierarchy for upload. "Animate into list" selected for delight.

---

## File List as Artifacts

| Option | Description | Selected |
|--------|-------------|----------|
| ProductCard grid | Files as ProductCards in responsive grid (museum gallery style) | |
| Frosted row list | Single-column list of frosted rows with artifact labels | |
| Enriched table | Table with artifact styling — frosted header, pill badges, metadata | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal columns | File name + match status + actions | ✓ |
| Detailed columns | File name, type, columns, rows, date, status, actions | |
| Full metadata | All available metadata | |

| Option | Description | Selected |
|--------|-------------|----------|
| Frosted glass table | Semi-transparent rows, backdrop-blur, hairline borders | ✓ |
| Minimal white table | White rows, minimal borders | |
| Card-group layout | Each row styled as mini card | |

| Option | Description | Selected |
|--------|-------------|----------|
| Delete only | Keep it simple — delete action only | ✓ |
| Delete + View | Allow viewing file contents/columns | |
| Delete + View + Download | Also allow downloading matched output | |

| Option | Description | Selected |
|--------|-------------|----------|
| Newest first | Most recently uploaded at top | ✓ |
| Alphabetical | Sorted A-Z by filename | |
| Status first | Grouped by match status | |

| Option | Description | Selected |
|--------|-------------|----------|
| PillChip badges | Green/amber/blue colored chips | ✓ |
| Icon + text | Status icon + label text | |
| Color bar + label | Thin colored bar on row edge + text | |

**User's choice:** Enriched table, minimal columns, frosted glass table, delete only, newest first, PillChip badges
**Notes:** User prefers table scanability with Apple aesthetics. Match status colors: green (#34c759), amber (#ff9500), blue (#007aff).

---

## the agent's Discretion

- Exact layout of hero Tile (content, heading, subtext)
- Animation implementation for upload-to-list transition
- Empty state copy and illustration approach
- Frosted table exact styling (column widths, row height, responsive breakpoints)

## Deferred Ideas

- View file contents / columns in a detail pane or modal (Phase 03 Wizard or separate)
- Download matched output per file (Phase 04 Export)
- Trigger manual re-matching from the file list (Phase 03)
- Column mapping configuration on the page (Phase 03 Wizard)
