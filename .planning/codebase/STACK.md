# Technology Stack

**Analysis Date:** 2026-05-15

## Languages

**Primary:**
- Python 3.10+ - Backend logic and services (`backend/`)
- TypeScript 5.x - Frontend application and UI components (`frontend/`)

**Secondary:**
- CSS (Tailwind 4) - UI styling
- SQL - Supabase/PostgreSQL database migrations and queries

## Runtime

**Environment:**
- Python 3.10+
- Node.js 20+

**Package Manager:**
- pip - Backend dependencies (`backend/requirements.txt`)
- npm - Frontend dependencies (`frontend/package.json`)
- Lockfile: `package-lock.json` present

## Frameworks

**Core:**
- FastAPI - Backend API framework
- Next.js 16 - Frontend React framework (App Router)

**Testing:**
- Not detected (infrastructure ready for Pytest/Jest)

**Build/Dev:**
- Uvicorn - ASGI server for FastAPI
- Next.js Build System - Frontend compilation and bundling
- Tailwind CSS 4 - Utility-first styling framework

## Key Dependencies

**Critical:**
- `fastapi` - Web framework
- `google-genai` - Gemini LLM integration
- `@supabase/supabase-js` / `supabase` - Database and Authentication
- `pydantic` / `pydantic-settings` - Data validation and configuration

**Infrastructure:**
- `tesserocr` - Optical Character Recognition (OCR)
- `pdfplumber` - PDF parsing
- `openpyxl` / `XlsxWriter` - Excel generation and manipulation
- `rapidfuzz` - Fast fuzzy string matching

## Configuration

**Environment:**
- `.env` files for backend and frontend
- Pydantic Settings for backend configuration management (`backend/app/core/config.py`)

**Build:**
- `next.config.ts` - Next.js configuration
- `tsconfig.json` - TypeScript configuration
- `postcss.config.mjs` - Tailwind/PostCSS configuration

## Platform Requirements

**Development:**
- Python 3.10+
- Node.js 20+
- Tesseract OCR engine (local installation)

**Production:**
- Supabase (Database, Auth, Storage)
- Google Cloud (Gemini API)
- Hosting: Vercel (Frontend), Docker/VPS (Backend)

---

*Stack analysis: 2026-05-15*
