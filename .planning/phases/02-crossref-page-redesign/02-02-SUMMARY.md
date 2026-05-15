---
phase: 02-crossref-page-redesign
plan: 02
subsystem: ui
tags: [pillchip, xhr, upload-progress, apple-design, crossref]

# Dependency graph
requires:
  - phase: 02-crossref-page-redesign
    provides: Status column on crossref_files table (CRSS-01, CRSS-02)
provides:
  - PillChip with non-interactive status badge variant (matched/unmatched/processing)
  - uploadWithProgress XHR helper for per-file upload progress tracking
affects: [02-crossref-page-redesign, 03-wizard-crossref-integration]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Display-only status badges via PillChip variant prop pattern"
    - "XHR-based upload helper for progress reporting alongside fetch-based API"

key-files:
  created: []
  modified:
    - frontend/src/components/apple/PillChip.tsx
    - frontend/src/lib/api.ts

key-decisions:
  - "PillChip variant prop uses 'selectable' as default for backward compatibility"
  - "uploadWithProgress is a standalone function export (not part of api object) for direct use by the page redesign"
  - "XMLHttpRequest chosen over fetch for native upload progress events"

patterns-established:
  - "Variant prop pattern: default preserves existing behavior, new variant adds capability"
  - "Standalone XHR helper coexists with fetch-based api methods — each appropriate for different needs"

requirements-completed: [CRSS-01, CRSS-02]

# Metrics
duration: 2min
completed: 2026-05-15
---

# Phase 02 Plan 02: Frontend Primitives Summary

**PillChip extended with display-only status badge variant (matched/unmatched/processing) and XHR-based uploadWithProgress helper for per-file progress tracking**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-05-15T03:54:18Z
- **Completed:** 2026-05-15T03:54:57Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Extended PillChip with `variant="status"` mode rendering non-interactive colored `<span>` badges with green (matched), amber (unmatched), and blue (processing) colors
- Added `uploadWithProgress(file, onProgress)` XHR helper to api.ts with per-file progress callbacks, error handling, and named export

## Task Commits

Each task was committed atomically:

1. **Task 1: Extend PillChip with status variant** - `1bc47e9` (feat)
2. **Task 2: Add uploadWithProgress XHR helper to api.ts** - `284daf5` (feat)

## Files Created/Modified

- `frontend/src/components/apple/PillChip.tsx` - Extended with `variant` (selectable|status) and `statusType` (matched|unmatched|processing) props; status variant renders as `<span>` with color-coded styling
- `frontend/src/lib/api.ts` - Added `uploadWithProgress` function using XMLHttpRequest with `xhr.upload.onprogress` for per-file progress reporting

## Decisions Made

- **PillChip variant pattern**: Default `"selectable"` ensures backward compatibility — existing code continues to work without changes
- **Standalone XHR helper**: `uploadWithProgress` is a top-level named export (not appended to `api` object) because the page redesign uses it directly and it has a different signature (with progress callback)
- **XMLHttpRequest over fetch**: XHR's native `upload.onprogress` event provides accurate per-file byte-level progress that `fetch` (via `ReadableStream`) does not natively support

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Frontend primitives ready for Plan 03 (crossref page redesign with Tile, FrostedContainer, PillChip, and progress-based upload UX)
- PillChip status variant ready to render match status badges in the file list table
- uploadWithProgress available for upload Tile to show per-file progress during upload

---

*Phase: 02-crossref-page-redesign*
*Completed: 2026-05-15*
