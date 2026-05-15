# AGENTS.md — Proyecto-Prueba

Sistema de extracción de datos de CVs con exportación a Excel.

## Commands
- Backend: `uvicorn app.main:app --reload` (desde `backend/`)
- Frontend: `npm run dev` (desde `frontend/`)
- Instalar nuevas dependencias: `pip install -r requirements.txt` (backend)
- Lint: `ruff check .` (backend, si está instalado)

## Arquitectura

### Backend (`backend/`) — FastAPI + Supabase
| Ruta | Propósito |
|------|-----------|
| `app/main.py` | Entrypoint FastAPI |
| `app/api/` | Endpoints: ingest, templates, extraction, rules, export, crossref |
| `app/services/excel_service.py` | Genera .xlsx con openpyxl |
| `app/services/consolidator.py` | Agrupa filas duplicadas por RUT al exportar |
| `app/services/crossref_service.py` | Cruce de datos externos (PDF/CSV/PPT/DOCX) |
| `app/services/rules_engine.py` | Evalúa reglas condicionales por fila |
| `app/services/llm_service.py` | Extrae campos con Gemini |
| `app/services/ocr_service.py` | OCR con tesserocr |
| `app/services/fuzzy_service.py` | Fuzzy matching con rapidfuzz |
| `app/core/database.py` | Cliente Supabase singleton |
| `app/schemas/` | Pydantic models: extraction, rules, template, crossref |
| `app/utils/rut_formatter.py` | Normalización/formateo de RUT chileno |

### Frontend (`frontend/`) — Next.js 16 App Router
- Páginas: `/export`, `/extraction`, `/rules`, `/templates`, `/crossref`, `/wizard`
- Wizard: flujo guiado paso a paso (upload → crossref → template → rules → extract → export → review)
- UI: Tailwind v4, @base-ui/react, lucide-react, shadcn

### Supabase
- Tablas: `templates`, `rules`, `extraction_results`, `crossref_files`
- RLS por usuario, índices en created_by y template_id

## Convenciones
- Backend: FastAPI, Pydantic schemas, servicios con clase
- Consolidación por RUT ocurre en el backend durante exportación (no modifica Supabase)
- Crossref: archivos se almacenan en `uploads/crossref/`, datos parseados en Supabase
- Formatos soportados para cruce: PDF, CSV, PPT, DOCX
