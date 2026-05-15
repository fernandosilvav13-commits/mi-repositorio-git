# Phase 02: Crossref Page Redesign — Research

**Researched:** 2026-05-14
**Domain:** Frontend redesign (Apple Design System), file upload UX, artifact-based file management
**Confidence:** HIGH

## Summary

This phase redesigns the Crossref file upload and management page using the Apple Design System components built in Phase 01 (Tile, FrostedContainer, PillChip, ProductCard). The page follows the established museum gallery pattern demonstrated in the extraction page: hero Tile → controls/content → data display → action section.

The current crossref page (`frontend/src/app/crossref/page.tsx`) uses basic shadcn Card + Table + Badge components. It needs a complete in-place redesign to replace its layout with Apple-styled hero upload section + frosted glass enriched table.

**Key architectural insight:** The `crossref_files` Supabase table has NO status column — match status is currently not stored. A small migration is needed to add a `status` column, or status must be computed on the frontend. The CONTEXT.md flags this, and since CRSS-02 requires match status indicators, this must be resolved during implementation. Adding a `status` column (default: `'unmatched'`) is the cleaner approach — Phase 03 will update it to `'matched'`.

**Primary recommendation:** Replace `frontend/src/app/crossref/page.tsx` with an Apple-designed page using: a white Tile for the upload section (drag-and-drop + file picker with per-file progress), a frosted glass table (using FrostedContainer-wrapped shadcn Table components) for the file list, and status-display variants of PillChip for match indicators. Add a `status` column to the Supabase `crossref_files` table. Returns `status` in the API response.

## User Constraints (from CONTEXT.md)

### Locked Decisions
- Upload via dedicated Upload section Tile (hero-style, not floating button)
- Supports drag-and-drop + file picker
- Multi-file upload with progress per file
- Accepted file types shown as compact badge line below drop zone
- File animates from upload zone into file list below
- Files displayed in enriched table with artifact styling (frosted glass table)
- Minimal columns: file name, match status, actions (delete only)
- Frosted glass table: semi-transparent rows, backdrop-blur, hairline borders
- Files sorted newest first
- Match status via PillChip badges: green (#34c759) "Matched", amber (#ff9500) "Unmatched", blue (#007aff) "Processing"

### the agent's Discretion
- Exact layout of hero Tile (content, heading, subtext)
- Animation implementation for upload-to-list transition
- Empty state copy and illustration approach
- Frosted table exact styling (column widths, row height, responsive breakpoints)

### Deferred Ideas (OUT OF SCOPE)
- View file contents/columns in a detail pane or modal (Phase 03)
- Download matched output per file (Phase 04 Export)
- Trigger manual re-matching from file list (Phase 03)
- Column mapping configuration on the page (Phase 03 Wizard)
- Wizard integration (Phase 03)
- Export with cross-referenced data (Phase 04)

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CRSS-01 | User can upload and manage cross-reference files in an Apple-designed page with Tile, FrostedContainer, and PillChip components | All three Apple components exist from Phase 01. Upload needs a new drop zone component or inline implementation. PillChip needs a status-only variant (currently only supports interactive selectable mode). |
| CRSS-02 | User can view uploaded cross-reference files in a clean artifact-based list with match status indicators | Existing `GET /api/crossref/files` endpoint returns file list sorted newest first. Crossref_files table lacks status column — needs migration to add `status` (default: `'unmatched'`). Status API response field must be added. |

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| File upload UI | Browser/Client | — | Drag-and-drop + file picker are entirely client-side interactions. Progress tracking via XHR/fetch. |
| Upload API | API/Backend | — | POST /api/crossref/upload persists file to disk and Supabase. Already exists. |
| File list data | API/Backend | — | GET /api/crossref/files returns sorted list from Supabase. Already exists. |
| File deletion | API/Backend | — | DELETE /api/crossref/files/{id}. Already exists. |
| Match status display | Browser/Client | — | PillChip rendering of status from API response data. |
| Match status storage | Database/Storage | — | Needs `status` column on `crossref_files` table. Phase 03 will update it. |
| Upload-to-list animation | Browser/Client | — | CSS transitions/animation after upload completes. |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Next.js + React | 16.2.6 / 19.2.4 | App framework | Project standard [VERIFIED: package.json] |
| Tailwind CSS | v4 | Utility CSS | Project standard [VERIFIED: package.json + globals.css] |
| shadcn/ui | v4 | Base UI primitives | Project standard — Table, Button, Badge [VERIFIED: package.json, components/ui/] |
| @base-ui/react | ^1.4.1 | Headless UI primitives | Project standard — Button uses it [VERIFIED: package.json] |
| lucide-react | ^1.14.0 | Icons | Project standard [VERIFIED: package.json] |
| tw-animate-css | ^1.4.0 | CSS animations | Project standard — `animate-in`, `fade-in`, `slide-in-from-bottom-4` [VERIFIED: package.json, extraction page usage] |

### Apple Design System Components (from Phase 01)
| Component | Purpose | Where |
|-----------|---------|-------|
| Tile | Upload hero section + file list section containers | `frontend/src/components/apple/Tile.tsx` |
| FrostedContainer | Frosted glass table wrapper | `frontend/src/components/apple/FrostedContainer.tsx` |
| PillChip | Match status badges (needs status-only variant) | `frontend/src/components/apple/PillChip.tsx` |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Native drag-and-drop | react-dropzone | Native DnD avoids adding a dependency. The use case (file upload only) is simple enough for native HTML5 DnD API. react-dropzone adds ~5KB but handles edge cases (multiple browsers, directory selection). |
| CSS animations | Framer Motion | tw-animate-css already in use. CSS transitions are sufficient for the upload-to-list animation. Framer Motion adds ~30KB. |
| shadcn Table | Custom frosted table | shadcn Table provides accessible table markup. Apply frosted styling via FrostedContainer wrapper + per-row styling. |

## Architecture Patterns

### Page Layout Pattern (Museum Gallery)

Following the extraction page pattern established in `frontend/src/app/extraction/page.tsx`:

```
┌─────────────────────────────────────────┐
│  White Tile: Upload Hero Section        │
│  ┌───────────────────────────────────┐  │
│  │  Title (h1) + Subtitle            │  │
│  │                                   │  │
│  │  ┌───────────────────────────┐    │  │
│  │  │   Drop Zone               │    │  │
│  │  │   (drag & drop area)      │    │  │
│  │  │   [Click to browse]       │    │  │
│  │  └───────────────────────────┘    │  │
│  │  [PDF] [CSV] [PPT] [DOCX]        │  │  ← compact badge line
│  │                                   │  │
│  │  When files selected:             │  │
│  │  ┌─ File 1 ████████░ 80% ─┐      │  │
│  │  └──────────────────────────┘      │  │
│  │  ┌─ File 2 ██████████ 100% ─┐     │  │
│  │  └──────────────────────────┘      │  │
│  └───────────────────────────────────┘  │
├─────────────────────────────────────────┤
│  Dark/Parchment Tile: File List         │
│  ┌───────────────────────────────────┐  │
│  │  FrostedContainer wrapper         │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Table (shadcn)             │  │  │
│  │  │  ┌─────────┬──────┬──────┐ │  │  │
│  │  │  │ Name    │Match │Actions│ │  │  │
│  │  │  ├─────────┼──────┼──────┤ │  │  │
│  │  │  │ file.x  │ ✓    │ 🗑   │ │  │  │
│  │  │  │ file.y  │ ○    │ 🗑   │ │  │  │
│  │  │  └─────────┴──────┴──────┘ │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Pattern 1: Upload Tile with Drag-and-Drop
**What:** A prominent upload section as the page hero, acting as the focal call-to-action. Uses a white Tile with a styled drop zone inside it.
**When to use:** When file upload is the primary action on the page (as per U-01 decision: hero-style, not floating button).
**Key implementation details:**
- Tile variant="white" with custom content
- Hidden file input triggered by click on drop zone
- Native HTML5 DnD: onDragOver (preventDefault + visual feedback), onDrop (preventDefault + process files)
- Per-file progress bar using XMLHttpRequest (supports `upload.onprogress`)
- Compact badge line below drop zone showing accepted formats

### Pattern 2: Frosted Glass Table
**What:** The file list displayed as an enriched table within a FrostedContainer for the signature Apple frosted glass effect.
**When to use:** For the file list section. Wraps the shadcn Table component inside FrostedContainer. Applies semi-transparent row backgrounds with backdrop-blur, hairline borders, and subtle hover effects.
**Key implementation details:**
- FrostedContainer wraps the entire Table
- Custom class overrides on shadcn TableRow for glass effect: `bg-white/40 backdrop-blur-md border-b border-white/20`
- Header row more opaque: `bg-white/70`
- Softer background for dark Tile context if needed

### Pattern 3: Status-only PillChip Variant
**What:** The existing PillChip component is designed for interactive selection (selected/clickable). A new variant is needed for display-only status badges.
**When to use:** For match status indicators in the table (matched/unmatched/processing).
**Implementation options:**
- **Option A (recommended):** Add a `variant` prop to PillChip (`"selectable" | "status"`). In status mode, omit the `button` wrapper, render as a `<span>`, and accept a `statusType` prop (`"matched" | "unmatched" | "processing"`) that sets the color.
- **Option B:** Build a standalone `StatusBadge` component. Simpler, doesn't couple with PillChip.
- **Option A is recommended** since PillChip conceptually IS the status badge — it just needs a non-interactive display mode.

### Anti-Patterns to Avoid
- **Floating upload button**: U-01 explicitly decided against this. Upload must be hero-section Tile, not a floating FAB.
- **Single file upload**: U-03 requires multi-file. Don't limit to one-at-a-time.
- **Too many table columns**: F-02 limits to 3 columns (name, status, actions). Don't add columns like "type", "rows", "columns" like the current page does.
- **Custom upload progress library**: The use case (file upload progress bars) is simple enough for native XHR events. Avoid adding a progress bar library.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Drag-and-drop file upload | Custom DnD from scratch | Native HTML5 DnD API (onDragOver, onDrop) | The use case is simple single/multi-file upload. Native API handles it well. react-dropzone is an option if edge cases arise but adds ~5KB. |
| Upload progress bars | Custom progress bar | Native XHR `upload.onprogress` event | XMLHttpRequest provides `loaded`/`total` for percentage. No library needed. |
| Supabase client | Custom Supabase wrapper | Existing `@supabase/supabase-js` via `backend/app/core/database.py` | Already set up. This phase only needs a migration SQL file, no new client code. |

**Key insight:** This phase is primarily a frontend redesign. The backend already has working upload/list/delete endpoints. Changes to backend are minimal (add status column, return status in response).

## Runtime State Inventory

> Not applicable — this is a page redesign and minor backend migration. No renames, refactors, or string replacements.

## Common Pitfalls

### Pitfall 1: PillChip Designed for Interaction
**What goes wrong:** The existing PillChip component is a `<button>` with `selected`/`onClick` props. Using it directly for non-interactive status badges creates click-handler confusion and accessibility issues.
**Why it happens:** PillChip was built for the Wizard's configurator chips (selectable options), not for display-only status.
**How to avoid:** Add a `variant` prop (`"selectable"` | `"status"`). In `"status"` mode, render as a `<span>` and accept a `color` prop or `statusType` prop with predefined colors.
**Warning signs:** Clicking a status badge triggers unexpected behavior; screen readers announce badges as buttons.

### Pitfall 2: No Match Status in Database
**What goes wrong:** The frontend displays match status but the backend has nowhere to store it. After upload, all files show as "processing" forever.
**Why it happens:** The `crossref_files` table was created before the match status feature was designed. It only stores `id`, `name`, `file_type`, `columns`, `data`, `row_count`, `created_by`, `created_at`.
**How to avoid:** Add a migration adding `status` column to `crossref_files` with default `'unmatched'`. Update the upload handler to set status. Update the GET /files response to include status.
**Warning signs:** API response has no `status` field; all files appear with no status or incorrect status.

### Pitfall 3: Multi-File Upload Without Progress
**What goes wrong:** User uploads 5 files but gets no feedback on individual progress. The UI shows a single spinner until all complete.
**Why it happens:** The current `api.crossref.upload()` uses `fetch()` which doesn't support upload progress events.
**How to avoid:** Use XMLHttpRequest for individual uploads so per-file progress can be tracked via `xhr.upload.onprogress`. Use `fetch()` is fine for simple uploads but progress requires XHR. Or use `fetch` with the Response body as a stream but that doesn't give upload progress — only download progress.
**Warning signs:** Users see no per-file progress during multi-upload.

### Pitfall 4: Upload API Takes One File
**What goes wrong:** U-03 requires multi-file upload, but the backend endpoint `/api/crossref/upload` accepts a single `UploadFile`.
**How to avoid:** Frontend sends multiple concurrent XHR requests (one per file). The backend endpoint already works correctly for single files — no backend change needed for this. Each file gets its own progress bar.
**Warning signs:** Attempting to send all files in a single FormData `files[]` field but the backend only reads `file` (singular).

## Code Examples

### New API response with status

The upload endpoint response should include `status`:
```typescript
// Backend: POST /api/crossref/upload response
{
  "id": "uuid",
  "name": "safe_filename.csv",
  "columns": ["RUT", "Nombre", "Curso"],
  "row_count": 150,
  "status": "unmatched"  // NEW: default after upload
}
```

The list endpoint response should include `status`:
```typescript
// Backend: GET /api/crossref/files response
[
  {
    "id": "uuid",
    "name": "file.csv",
    "file_type": ".csv",
    "columns": ["RUT", "Nombre"],
    "row_count": 150,
    "created_at": "2026-05-14T...",
    "status": "unmatched"   // NEW
  }
]
```

### Upload with progress tracking (frontend pattern)

```typescript
// Source: Common XHR upload with progress pattern
const uploadWithProgress = (
  file: File,
  onProgress: (percent: number) => void
): Promise<any> => {
  return new Promise((resolve, reject) => {
    const form = new FormData();
    form.append("file", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${API_BASE}/api/crossref/upload`);

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) {
        onProgress(Math.round((e.loaded / e.total) * 100));
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(new Error(xhr.responseText));
      }
    };

    xhr.onerror = () => reject(new Error("Upload failed"));
    xhr.send(form);
  });
};
```

### PillChip status variant

```typescript
// Extension to existing PillChip component
// New: variant="status" for display-only badges
interface PillChipProps {
  variant?: "selectable" | "status";
  // For selectable mode (existing)
  selected?: boolean;
  onClick?: () => void;
  // For status mode (new)
  statusType?: "matched" | "unmatched" | "processing";
  children: React.ReactNode;
  className?: string;
}

// Status badge colors:
// Matched:   bg-[#34c759]/10 text-[#34c759] border-[#34c759]/20
// Unmatched: bg-[#ff9500]/10 text-[#ff9500] border-[#ff9500]/20
// Processing: bg-[#007aff]/10 text-[#007aff] border-[#007aff]/20
```

### Frosted table row styling

```typescript
// FrostedTableRow wraps shadcn TableRow with glass effect
<TableRow
  className={cn(
    "bg-white/40 backdrop-blur-md border-b border-white/20",
    "hover:bg-white/60 transition-colors duration-300",
    className
  )}
/>
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| shadcn Card for upload section | Tile(variant="white") with custom upload content | This phase | Aligns with Apple design language established in Phase 01 |
| shadcn Table (basic) | FrostedContainer + shadcn Table with glass styling | This phase | Visual upgrade from plain table to Apple frosted aesthetic |
| Badge variant="outline" for file type | PillChip status badges for match status | This phase | Match indicators are a new capability (CRSS-02) |
| Single file upload | Multi-file upload with per-file progress | This phase | UX improvement from U-03/U-04 decisions |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The `status` column should default to `'unmatched'` for newly uploaded files | Common Pitfalls | Phase 03 may need a different default. Fine to change in Phase 03 since it will update the status anyway. |
| A2 | Concurrent XHR requests for multi-file upload (one per file) is acceptable | Code Examples | If backend has rate limiting or connection limits, sequential uploads with queue may be better. Mitigation: start with concurrent (max 3 parallel) with sequential fallback. |
| A3 | CSS transitions are sufficient for upload-to-list animation | Architecture | If animation requirements become complex (spring physics, staggered entrance), Framer Motion may be needed. Mitigation: start with CSS, add Framer Motion only if needed. |

## Open Questions

1. **Animation gateway timing**
   - What we know: File should animate from upload zone into file list after upload completes
   - What's unclear: The exact mechanism — should the file's row appear at the top of the table and "fly in" from the upload zone position? Or should the whole table re-render with a slide-in effect on the new row?
   - Recommendation: Use a staggered entrance: when upload completes, the new row appears at the top of the table with `animate-in fade-in slide-in-from-top-2 duration-500`. This is simpler than position-tracking between two sections.

2. **Error state for upload failure**
   - What we know: `sonner` toast is used for errors in the current page (via `toast.error()`)
   - What's unclear: Should upload failure be shown inline (on the failed file's progress bar) or as a toast notification?
   - Recommendation: Both. Inline error on the file card itself + a subtle toast. The toast closes automatically; the inline error persists until dismissed.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Node.js | Frontend dev | ✓ | v22.22.2 | — |
| npm | Package management | ✓ | 10.9.7 | — |
| Next.js | App framework | ✓ | 16.2.6 (in node_modules) | — |
| Tailwind CSS | Styling | ✓ | v4 | — |
| shadcn/ui | UI primitives | ✓ | v4 | — |
| Python 3 | Backend (not needed for this phase) | ✓ | (from project) | — |

**Missing dependencies with no fallback:** None.

## Validation Architecture

> `workflow.nyquist_validation` is not explicitly set in config.json. Treating as enabled per protocol.

### Test Framework

Currently, the frontend has no test infrastructure (no test config files, test directories, or test scripts in package.json). This phase is primarily a frontend page redesign. Two approaches:

| Option | Description | Tradeoffs |
|--------|-------------|-----------|
| **A: No tests** | Accept that Phase 02 is UI-only with no existing test infra | Fastest. Risk: visual regressions caught manually. |
| **B: Add Playwright e2e** | Use the existing `webapp-testing` skill to add basic e2e tests | Covers the full upload-display-delete flow. Requires browser setup. |

**Recommendation:** Option A for this phase (no test infrastructure exists; adding it would increase scope). Manual verification per success criteria is sufficient for a page redesign.

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Notes |
|--------|----------|-----------|-------|
| CRSS-01 | Upload files via Apple-designed page | Manual | Verify Tile, FrostedContainer usage in page source and visual inspection |
| CRSS-01 | Multi-file upload with progress | Manual | Upload 3+ files simultaneously, verify progress bars |
| CRSS-01 | Drag-and-drop upload | Manual | Drag file onto drop zone, verify upload |
| CRSS-02 | File list with artifact styling | Manual | Verify frosted glass table styling in browser |
| CRSS-02 | Match status badges (matched/unmatched/processing) | Manual | Verify PillChip variants display correct colors |
| CRSS-02 | Delete file from list | Manual | Click delete, verify file removed from list |
| CRSS-02 | Empty state | Manual | Visit page with no files, verify empty state renders |

### Sampling Rate
- Per task commit: Visual check in browser (npm run dev)
- Phase gate: All success criteria in ROADMAP.md verified true via manual testing

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V5 Input Validation | yes | File extension validation already in backend `validate_upload()` function. Drag-and-drop doesn't bypass server-side validation since all uploads go through the same API endpoint. |
| V12 File Uploads | yes | Backend already handles: file extension check (`validate_upload`), sanitized filename (`sanitize_filename`), max size (in `validate_upload`). No changes needed. |

### Known Threat Patterns

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Malicious file upload | Tampering | Backend `validate_upload()` checks file type and content. Frontend accepts PDF/CSV/PPT/DOCX only. No change needed — this phase touches frontend only. |
| XSS via file name | Injection | Backend uses `sanitize_filename()`. Display in table cell is React-rendered (auto-escaped). No raw HTML insertion. |

## Sources

### Primary (HIGH confidence)
- Phase 01 Apple Design System components (Tile, FrostedContainer, PillChip, ProductCard) — read from source files
- Current crossref page (`frontend/src/app/crossref/page.tsx`) — read source
- Extraction page pattern (`frontend/src/app/extraction/page.tsx`) — read source
- Backend API (`backend/app/api/crossref.py`) — read source endpoints
- Supabase migration (`supabase/migration.sql`) — verified crossref_files table schema, no status column
- State/Context files (CONTEXT.md, STATE.md, ROADMAP.md, REQUIREMENTS.md) — read and verified decisions
- AGENTS.md — read project guidelines
- DESIGN.md (Apple design system spec) — read full spec
- globals.css — verified Tailwind v4 theme tokens

### Secondary (MEDIUM confidence)
- tw-animate-css animation utilities — confirmed via extraction page usage (animate-in, fade-in, slide-in-from-bottom-4)

### Tertiary (LOW confidence)
- None — all claims verified from project source files or official Phase 01 artifacts.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — All components verified from project source code.
- Architecture: HIGH — The museum gallery pattern is well-established in the extraction page.
- Pitfalls: HIGH — Based on direct code analysis of current page vs. requirements.
- Backend changes: HIGH — Migration scope is small and well-understood from examining `crossref_files` table schema.

**Research date:** 2026-05-14
**Valid until:** 2026-06-14 (stable project, no fast-moving dependencies)
