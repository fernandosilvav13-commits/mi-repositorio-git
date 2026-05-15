# Codebase Structure

**Analysis Date:** 2026-05-15

## Directory Layout

```
[project-root]/
├── backend/            # FastAPI Backend application
│   ├── app/            # Main application source code
│   │   ├── api/        # REST API routes
│   │   ├── core/       # Config, DB, Auth, Security
│   │   ├── schemas/    # Pydantic models (DTOs)
│   │   ├── services/   # Business logic and external services
│   │   └── utils/      # Shared helper functions
│   ├── uploads/        # Temp storage for uploaded CVs
│   ├── outputs/        # Generated Excel/reports
│   └── requirements.txt# Python dependencies
├── frontend/           # Next.js Frontend application
│   ├── src/
│   │   ├── app/        # App Router pages and layouts
│   │   ├── components/ # React components (UI/Shared)
│   │   └── lib/        # API client and utilities
│   ├── public/         # Static assets
│   └── package.json    # Node dependencies
└── supabase/           # Database migrations and config
```

## Directory Purposes

**backend/app/api:**
- Purpose: Handles HTTP requests and response formatting.
- Contains: FastAPI router files.
- Key files: `backend/app/api/extraction.py`, `backend/app/api/ingest.py`, `backend/app/api/templates.py`.

**backend/app/services:**
- Purpose: Implements the "meat" of the application.
- Contains: Extraction logic, OCR, Rules engine, Excel generation.
- Key files: `backend/app/services/cv_processor.py`, `backend/app/services/llm_service.py`, `backend/app/services/rules_engine.py`, `backend/app/services/excel_service.py`.

**frontend/src/app:**
- Purpose: Defines the frontend routes and page structure.
- Contains: Next.js page components and layouts.
- Key files: `frontend/src/app/wizard/page.tsx`, `frontend/src/app/extraction/page.tsx`.

**frontend/src/components/ui:**
- Purpose: Reusable UI components (buttons, cards, etc.).
- Contains: Shadcn/UI inspired components.

## Key File Locations

**Entry Points:**
- `backend/app/main.py`: Main FastAPI entry point.
- `frontend/src/app/page.tsx`: Main frontend entry point.

**Configuration:**
- `backend/app/core/config.py`: Backend settings and environment variable mapping.
- `frontend/next.config.ts`: Next.js configuration.
- `.env`: (Not committed) Environment secrets.

**Core Logic:**
- `backend/app/services/cv_processor.py`: CV processing orchestration.
- `backend/app/services/rules_engine.py`: Rules evaluation logic.

**Testing:**
- (Not explicitly found in current exploration, typically in `tests/` or alongside files).

## Naming Conventions

**Files:**
- Backend: Snake case (`cv_processor.py`).
- Frontend: Kebab case for directories, PascalCase or kebab-case for components/files (`page.tsx`, `Button.tsx`).

**Directories:**
- Consistent kebab-case or snake-case based on language ecosystem.

## Where to Add New Code

**New Feature (Extraction related):**
- API endpoint: `backend/app/api/`
- Processing logic: `backend/app/services/`
- Frontend page: `frontend/src/app/`

**New Component/Module:**
- Backend Service: `backend/app/services/`
- Frontend UI: `frontend/src/components/`

**Utilities:**
- Shared helpers: `backend/app/utils/` (Backend) or `frontend/src/lib/` (Frontend).

## Special Directories

**uploads/:**
- Purpose: Storage for raw CV files before processing.
- Generated: Yes
- Committed: No

**outputs/:**
- Purpose: Storage for generated Excel files.
- Generated: Yes
- Committed: No

---

*Structure analysis: 2026-05-15*
