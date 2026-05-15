# External Integrations

**Analysis Date:** 2026-05-15

## APIs & External Services

**AI & LLM:**
- Google Gemini API - Used for data extraction, document legibility checks, and cross-referencing logic.
  - SDK/Client: `google-genai`
  - Auth: `google_api_key` (env var)
  - Models: `gemini-2.5-flash-lite`, `gemini-2.5-flash`

## Data Storage

**Databases:**
- Supabase (PostgreSQL)
  - Connection: `supabase_url`, `supabase_key`
  - Client: `supabase-py` (Backend), `@supabase/supabase-js` (Frontend)

**File Storage:**
- Local filesystem - Temporary storage for uploads and outputs.
  - Paths: `backend/uploads/`, `backend/outputs/`
- Supabase Storage - Intended for persistent file hosting.

**Caching:**
- None detected (in-memory caching potentially used in specific services)

## Authentication & Identity

**Auth Provider:**
- Supabase Auth
  - Implementation: JWT-based authentication using `supabase_jwt_secret`.

## Monitoring & Observability

**Error Tracking:**
- None (Basic logging implemented in `backend/app/utils/logger.py`)

**Logs:**
- Standard Python logging with custom setup in `backend/app/utils/logger.py`.

## CI/CD & Deployment

**Hosting:**
- Vercel (Frontend - inferred from Next.js)
- Docker (Supported via `docker-compose.yml` in subdirectories)

**CI Pipeline:**
- None detected

## Environment Configuration

**Required env vars:**
- `supabase_url`: Supabase project URL
- `supabase_key`: Supabase anon/service key
- `supabase_jwt_secret`: Secret for JWT verification
- `google_api_key`: Google AI Studio API key

**Secrets location:**
- `.env` (Backend root)
- `.env.local` (Frontend root)

## Webhooks & Callbacks

**Incoming:**
- None detected

**Outgoing:**
- None detected

---

*Integration audit: 2026-05-15*
