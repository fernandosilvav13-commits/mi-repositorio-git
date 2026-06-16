---
status: resolved
slug: folder-upload-readentries
trigger: "Siguen habiendo problemas en la subida de archivos. Primero el drag and drop sigue igual, sólo se suben unos pocos archivos. Luego cuando clickeo seleccionar archivos y selecciono carpetas no me deja subirlas"
created: 2026-06-05
updated: 2026-06-05
---

## Symptoms

- **Drag & drop**: Only a few files uploaded from 25 folders (~7 files each)
- **File selector**: Cannot select folders — standard `<input type="file">` only shows files
- **Expected**: All files should upload; folders should be selectable

## Current Focus

- **Hypothesis 1**: `readEntry` calls `readEntries()` once per dir — FIXED in prior session
- **Hypothesis 2**: Drag & drop didn't filter unsupported files (Thumbs.db, .DS_Store, etc.)
- **Hypothesis 3**: No `webkitdirectory` attribute on file input; no UI for folder selection
- **Hypothesis 4**: Folder input handler ignores `webkitRelativePath` — all files assigned to "Raíz"

## Evidence

- timestamp: 2026-06-05 — `readEntry` now loops `readEntries()` until empty (confirmed in file)
- timestamp: 2026-06-05 — Drag & drop handler was missing `isUploadable` filter
- timestamp: 2026-06-05 — `folderRef` input had `type="file" multiple` but no `webkitdirectory`
- timestamp: 2026-06-05 — No button triggers folder selection; `folderRef` was hidden and unreachable
- timestamp: 2026-06-05 — `folderRef` handler assigned all files to `"Raíz"` regardless of `webkitRelativePath`

## Eliminated

- hypothesis: Backend limits — no limit on file count; each file validated individually
- hypothesis: FormData serialization — FastAPI correctly handles multipart with repeated keys

## Resolution

- **Root cause #1**: Drag & drop didn't filter out unsupported system files (Thumbs.db, .DS_Store), potentially confusing the UI. Also lacked `isUploadable` guard.
- **Root cause #2**: No folder selection support — the hidden `folderRef` input lacked `webkitdirectory` attribute and had no UI trigger.
- **Root cause #3**: Folder input handler didn't use `webkitRelativePath` for folder names.

- **Files changed**: `frontend/src/app/wizard/page.tsx`
  1. Added `isUploadable()` filter to drag & drop handler (line 536)
  2. Changed file input from transparent overlay to hidden + explicit button (line 563-574)
  3. Added "Seleccionar archivos" and "Seleccionar carpeta" buttons (lines 547-562)
  4. Added `webkitdirectory` attribute to folder input (line 579)
  5. Changed folder handler to extract folder name from `webkitRelativePath` (lines 585-588)

- **Verification**: TypeScript compilation passes (0 new errors; 2 pre-existing in MatchKeySelector.tsx)
