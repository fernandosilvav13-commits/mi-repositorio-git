# Plan: Automatizacion-Ciclo — Sistema de Automatización Documental para PyMEs

## Visión General
Sistema web que permite a PyMEs subir lotes de documentos (PDF, DOCX, CSV, imágenes), extraer datos estructurados vía IA + OCR + Fuzzy Matching, aplicar reglas de negocio, y exportar a Excel/Google Sheets con formato condicional.

---

## Stack Técnico

| Capa | Tecnología | Propósito |
|------|-----------|-----------|
| Backend | Python 3.12+ (FastAPI) | API REST, lógica de negocio, procesamiento |
| Frontend | Next.js 15 (App Router) + TailwindCSS + shadcn/ui | UI de configuración y dashboard |
| Base de datos | Supabase (PostgreSQL) | Persistencia de usuarios, plantillas, reglas |
| Auth | Supabase Auth | Autenticación |
| IA | Google Gemini (gemini-2.5-flash) vía `google-genai` SDK | Extracción estructurada vía LLM |
| OCR | Tesseract + pytesseract / pdfplumber | Extracción de texto de imágenes y PDFs |
| Fuzzy Matching | RapidFuzz | Corrección y mapeo de datos extraídos |
| Excel | openpyxl | Generación de Excel con formato condicional |
| Rules Engine | json-rules-engine (Python) o expr Evaluator | Motor de reglas de negocio |
| Deploy | Vercel (frontend) + Railway/Render (backend) | Hosting |

---

## Estructura del Proyecto

```
/automatizacion-ciclo/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── ingest.py          # Endpoint subida masiva archivos
│   │   │   ├── templates.py       # CRUD plantillas de extracción
│   │   │   ├── extraction.py      # Ejecutar extracción
│   │   │   ├── rules.py           # CRUD reglas de negocio
│   │   │   └── export.py          # Exportar a Excel
│   │   ├── core/
│   │   │   ├── config.py          # Config global (API keys, etc)
│   │   │   └── database.py        # Conexión Supabase
│   │   ├── services/
│   │   │   ├── ocr_service.py     # OCR (Tesseract + pdfplumber)
│   │   │   ├── llm_service.py     # Extracción vía LLM
│   │   │   ├── fuzzy_service.py   # Fuzzy Matching (RapidFuzz)
│   │   │   ├── rules_engine.py    # Motor de reglas de negocio
│   │   │   └── excel_service.py   # Generación Excel con openpyxl
│   │   ├── schemas/
│   │   │   ├── template.py        # Pydantic schemas
│   │   │   ├── extraction.py
│   │   │   └── rules.py
│   │   └── utils/
│   │       ├── file_parser.py     # Parseo PDF, DOCX, CSV, imágenes
│   │       └── rut_formatter.py   # Formateador RUT chileno (Regex)
│   ├── uploads/                   # Archivos subidos temporalmente
│   ├── outputs/                   # Excel generados
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/login
│   │   │   ├── (auth)/register
│   │   │   ├── dashboard/
│   │   │   ├── templates/
│   │   │   ├── extraction/
│   │   │   ├── rules/
│   │   │   └── api/
│   │   ├── components/
│   │   ├── lib/                   # API client, utils
│   │   └── types/
│   ├── package.json
│   └── next.config.js
├── supabase/
│   └── migrations/
├── .env.example
└── README.md
```

---

## Flujo de Datos

```
[Usuario] → Sube archivos (PDF, DOCX, CSV, JPG, PNG)
     ↓
[File Parser] → Extrae texto plano + OCR si es imagen
     ↓
[Plantilla de Extracción] → Usuario define columnas esperadas y formatos
     ↓
[LLM Service] → GPT-4o extrae datos estructurados JSON según plantilla
     ↓
[Fuzzy Matching] → RapidFuzz mapea valores con typos a columnas correctas (threshold configurable)
     ↓
[Rules Engine] → Evalúa reglas de negocio (ej: si conteo > 4, pintar verde)
     ↓
[Excel Service] → openpyxl genera .xlsx con formato condicional
     ↓
[Usuario] → Descarga Excel o exporta a Google Sheets
```

---

## Requisitos Funcionales Detallados

### M1: Módulo de Ingesta de Archivos
- Endpoint POST `/api/ingest/upload`
- Acepta: archivos individuales, carpetas ZIP, múltiples archivos en lote
- Formatos: PDF, DOC, DOCX, CSV, JPG, PNG, TIFF
- OCR automático en imágenes vía Tesseract
- Extracción de texto de PDFs con pdfplumber (fallback a OCR si es PDF escaneado)
- Validación de tipo/tamaño de archivo

### M2: Configuración Dinámica (Schema Definition)
- CRUD de "Plantillas de Extracción"
- Definir columnas dinámicamente (nombre, tipo de dato, formato de salida)
- Dropdown de formato para campos especiales (RUT, fechas, teléfonos)
- Persistencia en Supabase

### M3: Extracción por IA + Fuzzy Matching
- LLM recibe: texto extraído + schema de plantilla → devuelve JSON estructurado
- Fuzzy Matching con RapidFuzz para corregir typos vs valores esperados
- Threshold configurable (slider 0-100% en frontend)
- Fallback: si LLM falla → "NO ENCONTRADO" en celdas individuales, fila roja si falla completo

### M4: Motor de Reglas de Negocio
- Reglas tipo: `IF variable operador valor THEN accion`
- Ej: `IF titulos_academicos COUNT > 4 THEN fill_row GREEN`
- Motor evaluador de expresiones (json-rules-engine o expr)
- Acciones: pintar fila/columna, resaltar celda, ocultar fila

### M5: Exportación a Excel
- openpyxl con control total de formato
- Celdas "NO ENCONTRADO" para datos faltantes
- Filas con fondo rojo si falla crítica
- Aplicar reglas de negocio (colores condicionales)
- Formato RUT chileno configurable (Regex)
- Exportar también a Google Sheets (opcional v2)

---

## Estados y Manejo de Errores

| Situación | Comportamiento |
|-----------|---------------|
| Dato no encontrado por IA | Celda → "NO ENCONTRADO" |
| Documento ilegible/falla total | Fila completa → **fondo rojo** |
| Error de conexión con LLM | Reintentar 3 veces, luego fila roja |
| Archivo corrupto | Rechazar con mensaje claro al usuario |
| Umbral Fuzzy no alcanzado | Usar valor original, marcar con comentario |

---

## MCPs Instalados

| MCP | Paquete | Estado |
|-----|---------|--------|
| Tavily Search | `@tavily/mcp-server` | ✅ Configurado |
| Supabase | `@modelcontextprotocol/server-supabase` | ✅ Configurado |
| Filesystem | `@modelcontextprotocol/server-filesystem` | ✅ Instalado + Configurado |
| Shell | `@mkusaka/mcp-shell-server` | ✅ Instalado + Configurado |

### Archivos de configuración:
- `~/.config/opencode/opencode.json` — Config principal de OpenCode
- `~/.opencode/mcp_config.json` — Formato Claude Desktop (compatibilidad)

**Nota:** El paquete `@mako10k/mcp-shell-server` requería `make` para compilar `node-pty`. Se usó `@mkusaka/mcp-shell-server` como alternativa compatible.

---

## Skills Disponibles (ya instalados)

| Skill | Aplicación en este proyecto |
|-------|---------------------------|
| `firecrawl` | Scraping de documentación técnica si es necesario |
| `scraper-builder` | Si se requiere recolectar datos de sitios web externos |
| `frontend-design` | Diseño UI del dashboard |
| `shadcn` | Componentes del frontend |
| `supabase-postgres-best-practices` | Schema y queries óptimas |
| `webapp-testing` | Tests del frontend |
| `deploy-to-vercel` | Deploy del frontend |

---

## Próximos Pasos (Build Mode)

1. ~~Configurar MCPs faltantes (shell, filesystem)~~ ✅
2. Inicializar repositorio y estructura de carpetas
3. Implementar backend FastAPI (requirements.txt, config, database)
4. Implementar file_parser + OCR service
5. Implementar LLM service para extracción
6. Implementar fuzzy matching service
7. Implementar rules engine
8. Implementar excel export service
9. Construir frontend (Next.js + shadcn)
10. Integrar frontend con backend
11. Tests y deploy
