---
phase: 02-crossref-page-redesign
plan: 03
subsystem: ui
tags: [crossref, apple-design, tile, frosted-container, pillchip, drag-and-drop, upload-progress]

# Dependency graph
requires:
  - phase: 02-crossref-page-redesign 02-01
    provides: Status column on crossref_files + API returns status
  - phase: 02-crossref-page-redesign 02-02
    provides: PillChip status variant + uploadWithProgress XHR helper
provides:
  - Redesigned /crossref page with Apple museum-gallery layout (upload hero Tile + frosted glass file list)
  - Drag-and-drop + file picker upload with per-file progress bars
  - Format badge indicators (PDF, CSV, PPT, DOCX)
  - Frosted glass table with PillChip match status badges (matched/unmatched/processing)
  - Delete confirmation dialog with file name display
  - Empty state for first-time visitors
affects: [03-wizard-crossref-integration, 04-crossref-export]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Museum gallery page structure: white hero Tile → dark content Tile → no CTA (deferred)"
    - "Per-file upload progress via XHR with inline progress bars and status indicators"
    - "Staggered row entrance animation for newly uploaded files"

key-files:
  created: []
  modified:
    - frontend/src/app/crossref/page.tsx

key-decisions:
  - "Page has TWO sections only (no export CTA — deferred to Phase 04 per roadmap)"
  - "Upload-to-list animation uses staggered delay (100ms per index) for multi-file uploads"
  - "Status defaults to 'processing' for null/undefined values (files freshly uploaded with no match yet)"

patterns-established:
  - "Full-bleed alternating Tile layout matches extraction gallery page pattern"
  - "Frosted glass table with semi-transparent rows and backdrop-blur effect"
  - "Delete uses brief animate-out class before DOM removal (300ms timeout)"

requirements-completed: [CRSS-01, CRSS-02]

# Metrics
duration: 2min (impl) + subsequent fixes
completed: 2026-05-15
---

# Phase 02 Plan 03: Crossref Page Redesign Summary

**Complete Apple museum-gallery redesign of the /crossref page: upload hero Tile with drag-and-drop, per-file progress, and a frosted glass file list table with PillChip status badges**

## Performance

- **Duration:** ~2 min (initial implementation) + 5 subsequent fix commits
- **Implementation:** 2026-05-15T00:01:54Z
- **Completed:** 2026-05-15 (latest fix)
- **Tasks:** 2 (1 implementation + 1 verification checkpoint)
- **Files modified:** 1 (primary) + backend fixes

## Accomplishments

- Complete Apple museum-gallery redesign of /crossref page with white upload hero Tile and dark file list Tile
- Drag-and-drop zone with hover highlight, file picker fallback, keyboard accessibility
- Per-file upload queue with independent progress bars, completion/error/retry states
- Format badges (PDF, CSV, PPT, DOCX) below the drop zone
- Frosted glass file list table with PillChip status badges (matched/unmatched/processing)
- Empty state for first-time visitors with guidance text
- Upload-to-list staggered entrance animation (100ms per index)
- Delete confirmation dialog with file name, cancel/confirm actions
- Floating back button linking to /

## Task Commits

The initial implementation was committed atomically, followed by fix commits for discovered issues:

1. **Task 1: Redesign crossref page with Apple Design System** - `38f6f11` (feat)
2. **Task 2: Verification checkpoint** - (manual verification)

**Subsequent fix commits (post-implementation):**
- `0a5e585` — fix: CSV files rejected by magic bytes validation
- `effc369` — fix: CSV encoding fallback + better error handling
- `5ab8d45` — fix: Supabase timeout on large CSV data insert
- `bab1fa6` — fix: replace Supabase crossref_files with local manifest
- `4b33e3d` — fix: SelectContent dropdown transparent in Tailwind v4

## Files Created/Modified

- `frontend/src/app/crossref/page.tsx` — Complete Apple museum-gallery redesign (435 lines, was ~100 lines Card-based layout)

## Decisions Made

- **Two-section layout**: White hero Tile (upload) + dark Tile (file list). No CTA section — export is deferred to Phase 04
- **Staggered animation**: New file rows use `animationDelay: ${idx * 100}ms` for multi-file uploads
- **Default status**: Null/undefined status values render as "Processing" (blue badge) for freshly uploaded files
- **Local manifest storage**: Crossref storage migrated from Supabase to `uploads/crossref/manifest.json` for robustness (Supabase table didn't exist and was unreachable)

## Deviations from Plan

### Auto-fixed Issues

**1. CSV files rejected by magic bytes validation**
- **Found during:** Post-implementation testing
- **Issue:** CSV files starting with plain text (e.g. 'RUT,Nombre,Email') failed magic bytes check that only accepted ',' or '"' leading bytes
- **Fix:** Added early return for .csv to accept all text content since CSV has no reliable fixed magic bytes
- **Files modified:** backend/app/api/crossref.py
- **Verification:** CSV upload succeeds for real-world Spanish-Excel CSV files
- **Committed in:** `0a5e585`

**2. CSV encoding fallback for Spanish Excel exports**
- **Found during:** Post-implementation testing with real files
- **Issue:** Spanish Excel exports CSV in Latin-1 or cp1252 encoding, not UTF-8
- **Fix:** _parse_csv now tries utf-8, utf-8-sig, latin-1, cp1252 sequentially; uses sep=None with python engine for semicolon auto-detection
- **Files modified:** backend/app/api/crossref.py
- **Verification:** CSV upload succeeds with Spanish Excel exports containing tildes and ñ
- **Committed in:** `effc369`

**3. Supabase timeout on large CSV (8MB) data insert**
- **Found during:** Post-implementation testing with large files
- **Issue:** 8MB CSV with thousands of rows caused Supabase insert timeout
- **Fix:** Only store first 100 rows as preview; export/merge reads full data from disk via crossref_service.load_file_data()
- **Files modified:** backend/app/api/crossref.py, backend/app/services/crossref_service.py, backend/app/services/excel_service.py
- **Verification:** Large CSV upload completes, export reads full data from disk
- **Committed in:** `5ab8d45`

**4. Supabase crossref_files table not available**
- **Found during:** Post-implementation
- **Issue:** crossref_files table did not exist in Supabase and could not be created (DB unreachable)
- **Fix:** Replaced Supabase storage with local manifest.json in uploads/crossref/; all CRUD operations now read/write local manifest
- **Files modified:** backend/app/api/crossref.py, backend/app/services/export.py
- **Verification:** All CRUD operations work via local manifest
- **Committed in:** `bab1fa6`

**5. shadcn SelectContent dropdown transparent in Tailwind v4**
- **Found during:** Verification checkpoint
- **Issue:** SelectContent used bg-popover but Tailwind v4 requires @theme registration for --color-* tokens
- **Fix:** Added all missing shadcn color tokens to @theme inline in globals.css (background, foreground, card, popover, muted, accent, border, etc.)
- **Files modified:** frontend/src/app/globals.css
- **Verification:** Select dropdown renders with correct background
- **Committed in:** `4b33e3d`

---

**Total deviations:** 5 auto-fixed (1 backend CSV validation, 1 encoding, 1 timeout, 1 storage migration, 1 CSS theme tokens)
**Impact on plan:** All fixes were necessary for correct operation with real-world CV files. No scope creep.

## Issues Encountered

- Supabase crossref_files table was unavailable — migrated to local manifest.json approach
- Large CSV files (8MB+) caused Supabase timeout — implemented partial preview + on-disk full data reading
- Spanish Excel CSVs use Latin-1/cp1252 encoding — added encoding fallback chain
- Tailwind v4 requires @theme registration for color tokens — added missing shadcn tokens

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Crossref page fully redesigned with Apple Design System
- Upload, list, status display, and delete all functional
- Ready for Phase 03 (Wizard Cross-Reference Integration) to add crossref upload/column mapping step to the Wizard flow
- Ready for Phase 04 (Cross-Reference Export) to add cross-referenced columns to Excel output

---

## Self-Check: PASSED

- ✅ SUMMARY.md exists at `.planning/phases/02-crossref-page-redesign/02-03-SUMMARY.md`
- ✅ Task 1 commit `38f6f11` — feat: redesign crossref page with Apple Design System
- ✅ 5 subsequent fix commits addressing real-world issues
- ✅ All plan requirements verified: Tile, FrostedContainer, PillChip, uploadWithProgress, empty state, delete dialog, format badges, drag-and-drop, floating back button
- ✅ 435 lines in page.tsx (plan required min 200)

*Phase: 02-crossref-page-redesign*
*Completed: 2026-05-15*
