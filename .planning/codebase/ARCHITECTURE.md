<!-- refreshed: 2026-05-15 -->
# Architecture

**Analysis Date:** 2026-05-15

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                      Next.js Frontend                       │
├──────────────────┬──────────────────┬───────────────────────┤
│    Pages/Routes  │   Components     │    API Client         │
│  `frontend/src/app`│ `frontend/src/components`│ `frontend/src/lib/api.ts` │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│         `backend/app`                                        │
└──────────────────┬──────────────────┬───────────────────────┤
│    API Routers   │    Services      │    Core/Infra         │
│ `backend/app/api`│`backend/app/services`│ `backend/app/core` │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Supabase / Gemini API / Filesystem                         │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Next.js App | User Interface and Route management | `frontend/src/app` |
| API Client | Centralized communication with the backend | `frontend/src/lib/api.ts` |
| FastAPI App | API entry point and router inclusion | `backend/app/main.py` |
| CV Processor | Orchestrates document processing flow | `backend/app/services/cv_processor.py` |
| LLM Service | Interface for Gemini API interactions | `backend/app/services/llm_service.py` |
| Rules Engine | Evaluates conditional logic on extracted data | `backend/app/services/rules_engine.py` |
| Supabase Client | Direct interaction with Supabase DB | `backend/app/core/database.py` |

## Pattern Overview

**Overall:** Service-Oriented Architecture (SOA) with a clear separation between frontend (Next.js) and backend (FastAPI).

**Key Characteristics:**
- **Decoupled Frontend/Backend:** Communicates via REST API.
- **Service-Based Logic:** Backend business logic is encapsulated in the `services/` layer.
- **Stateless API:** Backend relies on Supabase for persistence and tokens for auth.

## Layers

**Frontend Layer:**
- Purpose: User interface and client-side logic.
- Location: `frontend/src`
- Contains: React components, App Router pages, Tailwind styles.
- Depends on: Backend API.
- Used by: End users.

**API Layer (Backend):**
- Purpose: Request routing, validation, and documentation.
- Location: `backend/app/api`
- Contains: FastAPI APIRouters.
- Depends on: Services, Core/Infra.
- Used by: Frontend.

**Service Layer (Backend):**
- Purpose: Core business logic and external integrations (Gemini, OCR, Excel).
- Location: `backend/app/services`
- Contains: Python classes/functions for data processing.
- Depends on: Core/Infra, Schemas.
- Used by: API Routers.

**Core/Infrastructure Layer (Backend):**
- Purpose: Global configuration, DB connections, security.
- Location: `backend/app/core`
- Contains: Configuration (Pydantic), Supabase client, Auth logic.
- Depends on: Environment variables.
- Used by: API Routers, Services.

## Data Flow

### Primary Request Path (Extraction)

1. **Client Request:** User uploads CVs via `frontend/src/app/wizard/page.tsx`.
2. **File Ingestion:** `backend/app/api/ingest.py` saves files to `uploads/`.
3. **Extraction Trigger:** Frontend calls `/api/extraction/`.
4. **Processing:** `backend/app/api/extraction.py` calls `OCRService` to get text.
5. **LLM Extraction:** `cv_processor.py` uses `llm_service.py` to extract fields via Gemini.
6. **Enrichment:** `cv_processor.py` normalizes RUT, Phone, and enriches School info from `mineduc_matricula.csv`.
7. **Rules:** `rules_engine.py` checks extracted data against user-defined rules.
8. **Persistence:** Data is saved to Supabase (`extraction_results` table).
9. **Response:** Processed data and triggered rules returned to frontend.

### State Management:
- **Server State:** Handled by Supabase.
- **Client State:** React state within page components and shared via Wizard context (if any).

## Key Abstractions

**Service Singletons:**
- Purpose: Reusable instances for processing (e.g., `cv_processor`, `ocr_service`).
- Examples: `backend/app/services/cv_processor.py`
- Pattern: Module-level singletons.

**Pydantic Schemas:**
- Purpose: Data validation and documentation for API inputs/outputs.
- Examples: `backend/app/schemas/extraction.py`
- Pattern: Data Transfer Objects (DTO).

## Entry Points

**Backend Entry Point:**
- Location: `backend/app/main.py`
- Triggers: Uvicorn/FastAPI server start.
- Responsibilities: CORS, Middleware, Router inclusion.

**Frontend Entry Point:**
- Location: `frontend/src/app/page.tsx`
- Triggers: Browser loading the root URL.
- Responsibilities: Main landing page and redirection to wizard.

## Architectural Constraints

- **Single-threaded Event Loop:** FastAPI (ASGI) handles concurrency, but some services might be CPU-bound (processing).
- **Filesystem dependency:** `uploads/` and `outputs/` directories are used for temporary storage before/after DB persistence.
- **Sync/Async split:** Some services use `async` (LLM calls), others are synchronous (OCR, openpyxl).

## Error Handling

**Strategy:** Exception-based handling with FastAPI HTTPExceptions for the API layer.

**Patterns:**
- **Try/Except blocks:** In API routes to catch processing errors and return 400/500 status codes.
- **Schema validation:** Pydantic automatically returns 422 for invalid request bodies.

---

*Architecture analysis: 2026-05-15*
