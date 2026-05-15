# Phase 02: Crossref Page Redesign — Pattern Map

**Mapped:** 2026-05-14
**Files analyzed:** 5 new/modified
**Analogs found:** 5 / 5

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `frontend/src/app/crossref/page.tsx` | page | request-response (CRUD) | `frontend/src/app/extraction/page.tsx` | exact (same role + same pattern) |
| `frontend/src/components/apple/PillChip.tsx` | component | UI display | `frontend/src/components/apple/PillChip.tsx` (self — extend existing) | exact (modifying same file) |
| `frontend/src/lib/api.ts` | utility | request-response (file upload) | `frontend/src/lib/api.ts` (self — add `uploadWithProgress` helper) | exact (modifying same file) |
| `supabase/migration.sql` | migration | schema | `supabase/migration.sql` (self — append new migration) | exact (modifying same file) |
| `backend/app/api/crossref.py` | controller | CRUD | `backend/app/api/crossref.py` (self — add status field) | exact (modifying same file) |

## Pattern Assignments

### `frontend/src/app/crossref/page.tsx` (page, request-response)

**Analog:** `frontend/src/app/extraction/page.tsx` — Museum gallery page pattern with hero Tile → content → action section

**Imports pattern** (lines 1-18):
```typescript
"use client";

import React, { useState, useEffect, useRef } from "react";
import Tile from "@/components/apple/Tile";
import ProductCard from "@/components/apple/ProductCard";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { FileText, Download, Play, Plus, ArrowLeft } from "lucide-react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import Link from "next/link";
```

**Page layout pattern** (lines 30-36, 80-230):
The page follows a museum gallery layout with three sections:
1. **Hero Tile (white)** — title, controls, call-to-action
2. **Content Tile (dark/parchment)** — data display (gallery grid or table)
3. **Action Tile (parchment)** — secondary CTA

```typescript
export default function ExtractionGalleryPage() {
  const [files, setFiles] = useState<...>([]);
  const [results, setResults] = useState<...>([]);
  const [loading, setLoading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Load initial data
    api.templates.list().then(setTemplates).catch(() => {});
  }, []);

  // ...handlers...

  return (
    <div className="flex flex-col w-full bg-white">
      {/* Floating Back Button */}
      <div className="fixed top-8 left-8 z-50">...</div>

      {/* Hero Section - White Tile */}
      <Tile variant="white" className="pt-32 pb-20">
        <h2 className="text-[21px] font-semibold tracking-[0.011em] text-ink/60 mb-2 uppercase">Collection</h2>
        <h1 className="apple-tight text-[56px] md:text-[72px] lg:text-[80px] text-ink leading-[1.05] mb-12 text-center">
          Extracted Insights
        </h1>
        {/* Controls bar */}
        <div className="flex flex-wrap ... rounded-full bg-near-black/5 backdrop-blur-xl border border-white/20 shadow-sm">
          {/* ...select, buttons... */}
        </div>
      </Tile>

      {/* Gallery Grid - Dark Tile */}
      <Tile variant="dark" className="min-h-[800px] !items-start overflow-visible">
        {/* content */}
      </Tile>

      {/* Export Section - Parchment Tile */}
      <Tile variant="parchment" className="border-t border-near-black/5">
        {/* action content */}
      </Tile>
    </div>
  );
}
```

**Animation pattern** (lines 149, 164):
```typescript
// Fade-in slide animation for status messages
<p className="mt-6 text-[14px] font-medium text-ink/40 animate-in fade-in slide-in-from-top-2 duration-500">

// Staggered entrance for list items
<div key={result.id || idx}
  className="animate-in fade-in zoom-in-95 duration-700 ease-out fill-mode-both"
  style={{ animationDelay: `${idx * 50}ms` }}
>
```

**Typographic pattern** (Apple design tokens, lines 93-97):
```typescript
<h2 className="text-[21px] font-semibold tracking-[0.011em] text-ink/60 mb-2 uppercase">
  Collection
</h2>
<h1 className="apple-tight text-[56px] md:text-[72px] lg:text-[80px] text-ink leading-[1.05] mb-12 text-center">
  Extracted Insights
</h1>
```

**Empty state pattern** (lines 198-206):
```typescript
{results.length > 0 ? (
  // content
) : (
  <div className="flex flex-col items-center justify-center py-60 w-full text-white/20">
    <div className="w-20 h-20 rounded-3xl bg-white/5 flex items-center justify-center mb-8">
      <FileText size={32} />
    </div>
    <p className="text-[24px] font-medium tracking-tight mb-2">Collection is currently empty.</p>
    <p className="text-[17px] max-w-sm text-center">Add artifacts and choose a template to begin the museum extraction.</p>
  </div>
)}
```

**Error handling pattern** (lines 66-68):
```typescript
try {
  // ...
} catch (e: any) {
  toast.error(e.message || "Error during extraction");
}
```

**Apple floating control bar pattern** (lines 100-146):
```typescript
<div className="flex flex-wrap items-center justify-center gap-3 p-2 rounded-full bg-near-black/5 backdrop-blur-xl border border-white/20 shadow-sm">
  {/* Controls inside: select, buttons */}
  <Button
    variant="ghost"
    onClick={() => fileRef.current?.click()}
    className="rounded-full bg-white/80 hover:bg-white text-ink border-none shadow-sm h-11 px-5 active-scale transition-all flex items-center gap-2"
  >
    <Plus size={18} />
    <span className="text-[14px] font-medium">Add Artifacts</span>
  </Button>
  <input ref={fileRef} type="file" multiple className="hidden" onChange={handleFileChange} />
</div>
```

---

### `frontend/src/components/apple/PillChip.tsx` (component, UI display)

**Analog:** `frontend/src/components/apple/PillChip.tsx` (self — extend with status variant)

**Current source** (lines 1-31):
```typescript
import React from "react";
import { cn } from "@/lib/utils";

interface PillChipProps {
  selected: boolean;
  onClick: () => void;
  children: React.ReactNode;
  className?: string;
}

const PillChip = ({
  selected,
  onClick,
  children,
  className,
}: PillChipProps) => (
  <button
    onClick={onClick}
    className={cn(
      "rounded-full px-6 py-3 text-[14px] font-medium transition-all duration-300 active-scale",
      selected
        ? "border-2 border-action-blue text-action-blue bg-white"
        : "border border-[#e0e0e0] text-ink bg-white hover:border-[#7a7a7a]",
      className
    )}
  >
    {children}
  </button>
);

export default PillChip;
```

**Extension pattern** (status variant as recommended by RESEARCH.md):
The component needs a `variant` prop (`"selectable" | "status"`). In `"status"` mode:
- Render as a `<span>` instead of `<button>` (non-interactive, accessible)
- Accept a `statusType` prop (`"matched"` | `"unmatched"` | `"processing"`)
- Apply status colors:
  - matched: `bg-[#34c759]/10 text-[#34c759] border-[#34c759]/20`
  - unmatched: `bg-[#ff9500]/10 text-[#ff9500] border-[#ff9500]/20`
  - processing: `bg-[#007aff]/10 text-[#007aff] border-[#007aff]/20`

---

### `frontend/src/lib/api.ts` (utility, request-response)

**Analog:** `frontend/src/lib/api.ts` (self — add `uploadWithProgress` helper)

**Current pattern** (lines 1-101):
```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const isFormData = options?.body instanceof FormData;
  const res = await fetch(`${API_BASE}${path}`, {
    headers: isFormData ? {} : { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err);
  }
  return res.json();
}

export const api = {
  // ... namespaced API methods ...
  crossref: {
    upload: (file: File) => {
      const form = new FormData();
      form.append("file", file);
      return request<any>("/api/crossref/upload", {
        method: "POST",
        body: form,
      });
    },
    list: () => request<any[]>("/api/crossref/files"),
    get: (id: string) => request<any>(`/api/crossref/files/${id}`),
    delete: (id: string) =>
      request<any>(`/api/crossref/files/${id}`, { method: "DELETE" }),
  },
};
```

**XHR upload with progress pattern** (to add to api.ts, per RESEARCH.md lines 240-268):
```typescript
// New standalone helper — NOT inside the `api` object since it returns a Promise,
// not using the request() helper (needs XHR for progress events)
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

**Usage pattern for multi-file upload with per-file progress:**
```typescript
// Concurrent upload with progress tracking per file
const uploadFiles = async (files: File[]) => {
  const uploads = files.map((file) => {
    const progress = useProgress(file.name); // or state per file
    return uploadWithProgress(file, (pct) => {
      setProgresses(prev => ({ ...prev, [file.name]: pct }));
    });
  });
  return Promise.all(uploads);
};
```

---

### `supabase/migration.sql` (migration, schema)

**Analog:** `supabase/migration.sql` (self — append crossref_files status column)

**Existing crossref_files table schema** (lines 100-110):
```sql
-- Tabla: crossref_files (archivos de cruce de datos)
create table if not exists crossref_files (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  file_type text not null,
  columns jsonb not null default '[]',
  data jsonb not null default '[]',
  row_count int default 0,
  created_by uuid references auth.users(id),
  created_at timestamptz default now()
);
```

**Migration pattern** (to append to file):
```sql
-- Add status column to crossref_files for match tracking
alter table crossref_files
  add column if not exists status text not null default 'unmatched';

-- Index on status for Phase 03 filtering
create index if not exists idx_crossref_files_status on crossref_files(status);
```

**Existing SQL conventions to follow:**
- `if not exists` guards (lines 2, 13, 26, 101, 114+)
- Comment headers with Spanish descriptions (line 1, 12, 25, 37, 100, 126)
- RLS policies after table creation (lines 112-124)
- Indexes at bottom of file (lines 127-130)
- `timestamptz default now()` for timestamp columns (line 109)

---

### `backend/app/api/crossref.py` (controller, CRUD)

**Analog:** `backend/app/api/crossref.py` (self — add `status` to response, upload handler, and SELECT)

**Current upload endpoint** (lines 15-41) — needs `status` added to insert and response:
```python
@router.post("/upload")
async def upload_crossref(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    content = await file.read()
    validate_upload(content, file.filename)
    safe_name = sanitize_filename(file.filename)
    file_path = upload_dir / safe_name
    async with aiofiles.open(str(file_path), "wb") as buffer:
        await buffer.write(content)

    columns, data = crossref_service.parse_file(str(file_path))

    supabase = require_supabase()
    result = supabase.table("crossref_files").insert({
        "name": safe_name,
        "file_type": ext,
        "columns": columns,
        "data": data,
        "row_count": len(data),
        # ADD: "status": "unmatched",
    }).execute()

    return {
        "id": result.data[0]["id"],
        "name": safe_name,
        "columns": columns,
        "row_count": len(data),
        # ADD: "status": "unmatched",
    }
```

**Current list endpoint** (lines 44-50) — needs `status` added to SELECT:
```python
@router.get("/files")
async def list_files():
    supabase = require_supabase()
    result = supabase.table("crossref_files")\
        .select("id,name,file_type,columns,row_count,created_at")\
        # CHANGE TO: .select("id,name,file_type,columns,row_count,created_at,status")\
        .order("created_at", desc=True).execute()
    return result.data
```

**Pattern — auth dependency** (lines 1, 9):
```python
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.core.auth import require_auth
from app.core.security import validate_upload, sanitize_filename
from app.services.crossref_service import CrossrefService
from app.core.database import require_supabase

router = APIRouter(dependencies=[Depends(require_auth)])
```

**Pattern — file handling** (lines 16-24):
```python
@router.post("/upload")
async def upload_crossref(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    content = await file.read()
    validate_upload(content, file.filename)
    safe_name = sanitize_filename(file.filename)
    file_path = upload_dir / safe_name
    async with aiofiles.open(str(file_path), "wb") as buffer:
        await buffer.write(content)
```

**Pattern — Supabase CRUD** (lines 28-34):
```python
supabase = require_supabase()
result = supabase.table("crossref_files").insert({...}).execute()
```

---

## Shared Patterns

### Upload-to-List Animation
**Source:** `frontend/src/app/extraction/page.tsx` (lines 149, 164)
**Apply to:** `frontend/src/app/crossref/page.tsx`

```typescript
// tw-animate-css classes for upload completion feedback
"animate-in fade-in slide-in-from-top-2 duration-500"

// Staggered entrance for new rows in table
"animate-in fade-in zoom-in-95 duration-700 ease-out fill-mode-both"
style={{ animationDelay: `${idx * 50}ms` }}
```

### Frosted Table Row Styling
**Source:** `frontend/src/components/apple/FrostedContainer.tsx` + RESEARCH.md pattern
**Apply to:** `frontend/src/app/crossref/page.tsx` — file list table

```typescript
// FrostedContainer wraps the entire Table
<FrostedContainer variant="white" className="rounded-xl overflow-hidden">
  <Table>
    {/* ... */}
  </Table>
</FrostedContainer>

// Per-row glass effect applied via className on shadcn TableRow
<TableRow
  className={cn(
    "bg-white/40 backdrop-blur-md border-b border-white/20",
    "hover:bg-white/60 transition-colors duration-300"
  )}
/>

// Header row: more opaque
<TableRow className="bg-white/70 backdrop-blur-md border-b border-white/20">
```

### Status Badge Color Tokens
**Source:** RESEARCH.md (lines 288-291) / Apple Design System (#34c759, #ff9500, #007aff)
**Apply to:** `frontend/src/components/apple/PillChip.tsx` (status variant)

```
Matched:    bg-[#34c759]/10 text-[#34c759] border-[#34c759]/20
Unmatched:  bg-[#ff9500]/10 text-[#ff9500] border-[#ff9500]/20
Processing: bg-[#007aff]/10 text-[#007aff] border-[#007aff]/20
```

### cn() Utility
**Source:** `frontend/src/lib/utils.ts`
**Apply to:** All frontend components

```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Toast Error Handling
**Source:** `frontend/src/app/extraction/page.tsx` line 67 / `frontend/src/app/crossref/page.tsx` lines 45, 56
**Apply to:** All async operations in crossref/page.tsx

```typescript
import { toast } from "sonner";

try {
  // async operation
} catch (e: any) {
  toast.error(e.message || "Error description");
}
```

### File Input Pattern (hidden + ref)
**Source:** `frontend/src/app/extraction/page.tsx` (lines 36, 123-129) / `frontend/src/app/crossref/page.tsx` (lines 23, 87-93)
**Apply to:** crossref/page.tsx upload section

```typescript
const fileRef = useRef<HTMLInputElement>(null);

// Trigger file picker on click
<Button onClick={() => fileRef.current?.click()}>Select Files</Button>

// Hidden input
<input
  ref={fileRef}
  type="file"
  multiple
  className="hidden"
  accept=".pdf,.csv,.ppt,.pptx,.doc,.docx"
  onChange={handleFileChange}
/>
```

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| — | — | — | All 5 files have direct analogs (3 self-analogs for in-place modification, 1 close pattern match, 1 migration SQL pattern) |

## Metadata

**Analog search scope:**
- `frontend/src/app/extraction/page.tsx` — museum gallery page pattern (primary analog)
- `frontend/src/components/apple/Tile.tsx` — Tile component API
- `frontend/src/components/apple/FrostedContainer.tsx` — FrostedContainer API
- `frontend/src/components/apple/PillChip.tsx` — PillChip current interface (to extend)
- `frontend/src/components/apple/ProductCard.tsx` — ProductCard pattern (for reference)
- `frontend/src/lib/api.ts` — API helper pattern (to extend)
- `frontend/src/lib/utils.ts` — cn() utility pattern
- `frontend/src/components/ui/table.tsx` — shadcn Table API
- `backend/app/api/crossref.py` — Crossref API endpoints (to modify)
- `backend/app/schemas/crossref.py` — Crossref Pydantic schemas
- `supabase/migration.sql` — Migration SQL conventions
- `backend/app/core/database.py` — Supabase client pattern

**Files scanned:** 12
**Pattern extraction date:** 2026-05-14
