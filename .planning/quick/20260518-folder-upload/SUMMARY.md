---
status: complete
---

## Goal
Agregar soporte para subir carpetas completas a la extracción de archivos (CVs, documentos).

## Changes
- Backend: ingest.py accepts folder paths via `folders` Form field, preserves subdirectory structure in `uploads/`
- Frontend API: `api.ingest.upload()` accepts `{file, folder}[]` instead of `File[]`
- Gallery, Extraction, Wizard pages: Added "Subir Carpeta" button with `webkitdirectory` input
- Filtering of hidden/system files (Thumbs.db, .DS_Store, desktop.ini)
- Error resilience: backend skips invalid files per-file instead of failing entire batch
- Error reporting: alerts user about skipped files with reasons

## Files
- `backend/app/api/ingest.py` — folder-aware upload, per-file error handling
- `frontend/src/lib/api.ts` — updated type signature
- `frontend/src/app/(gallery)/page.tsx` — folder upload + filtering
- `frontend/src/app/extraction/page.tsx` — folder upload + filtering
- `frontend/src/app/wizard/page.tsx` — folder upload + filtering
