# Coding Conventions

**Analysis Date:** 2026-05-15

## Naming Patterns

**Files:**
- **Backend**: snake_case (e.g., `cv_processor.py`, `extraction.py`)
- **Frontend**: kebab-case for directories/routes (e.g., `extraction/page.tsx`), PascalCase for components (e.g., `button.tsx`)

**Functions:**
- **Backend**: snake_case (e.g., `extract_single`, `setup_logger`)
- **Frontend**: camelCase for helpers/hooks, PascalCase for components (e.g., `Button`)

**Variables:**
- **Backend**: snake_case (e.g., `active_rules`, `template_id`)
- **Frontend**: camelCase (e.g., `buttonVariants`, `className`)

**Types:**
- **Backend**: PascalCase for Pydantic models (e.g., `ExtractionRequest`, `ExtractionResult` in `backend/app/schemas/extraction.py`) and classes (e.g., `CVProcessor`, `OCRService`).
- **Frontend**: PascalCase for interfaces/types (e.g., `VariantProps`).

## Code Style

**Formatting:**
- **Backend**: `ruff` is mentioned in `AGENTS.md` but config is not explicitly present.
- **Frontend**: `eslint` with Next.js presets.

**Linting:**
- **Backend**: `ruff check .` (referenced in `AGENTS.md`)
- **Frontend**: `eslint` config in `frontend/eslint.config.mjs` using `next-config-next/core-web-vitals` and `typescript`.

## Import Organization

**Order:**
1. Built-in modules (e.g., `os`, `asyncio`)
2. Third-party libraries (e.g., `fastapi`, `pandas`, `react`)
3. Internal modules using absolute paths or aliases (e.g., `app.services`, `@/components`)

**Path Aliases:**
- **Frontend**: `@/` maps to `src/` as seen in `frontend/tsconfig.json` and imports (e.g., `@/lib/utils`).

## Error Handling

**Patterns:**
- **Backend**: Extensive use of `try-except` blocks in API endpoints (`backend/app/api/extraction.py`) and services. Errors are typically caught and returned as status messages in the response or raised via `HTTPException`.
- **Frontend**: Not explicitly observed in sample files, but typical Next.js patterns are expected.

## Logging

**Framework:** Standard Python `logging` module.

**Patterns:**
- Centralized configuration in `backend/app/utils/logger.py`.
- `setup_logger(name)` function returns a configured logger with `StreamHandler` and specific format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.

## Comments

**When to Comment:**
- Section headers in complex files (e.g., `# Obtener reglas habilitadas` in `extraction.py`).
- Clarification of logic or TODOs.

**JSDoc/TSDoc:**
- Minimal usage observed in components.

## Function Design

**Size:** Most functions are focused but some API handlers handle multiple steps (extraction + rules + database).

**Parameters:** 
- **Backend**: Uses `dict` for body data in endpoints, or explicit types in service methods.
- **Frontend**: Props destructuring for components with type safety.

**Return Values:**
- **Backend**: JSON responses (dicts/lists) or Pydantic models (implied).
- **Frontend**: React elements or typed helper returns.

## Module Design

**Exports:**
- **Backend**: Named exports and singletons (e.g., `cv_processor = CVProcessor()`).
- **Frontend**: Named exports for components and variants (e.g., `export { Button, buttonVariants }`).

**Barrel Files:**
- Used for grouping API routes and services (`__init__.py` files in backend folders).

---

*Convention analysis: 2026-05-15*
