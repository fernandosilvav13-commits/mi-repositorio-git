# Phase 09: Prompt Infrastructure & Foundation - Context

**Gathered:** 2026-05-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Version-controlled prompt registry that tracks every prompt change, enables reproducible extractions, and decouples prompt engineering from code changes. Implements PROMPT-01: YAML-based prompt files, PromptResolver, Git tracking, and extraction version logging.

</domain>

<decisions>
## Implementation Decisions

### Migracion desde prompt hardcoded
- **D-01:** Dual por defecto - PromptResolver usa fallback a constantes hardcoded de llm_service.py si no encuentra el YAML solicitado
- **D-02:** Los prompts actuales (EXTRACTION_PROMPT, EXTRACTION_SCHEMA, fallback schema) se migran como YAMLs iniciales: cv-extraction@v1.0 como baseline
- **D-03:** El directorio de prompts va en backend/prompts/, no en la raiz del proyecto
- **D-04:** Cada extraccion registra la version de prompt usada en dos lugares: log del logger existente + campo prompt_version en la tabla extraction_results de Supabase

### Estructura YAML del prompt
- **D-05:** Formato completo auto-contenido: type, version, description, author, system_prompt, schema (inline como dict), model_params (model, temperature, etc.), tags
- **D-06:** Organizacion por carpetas: backend/prompts/{document-type}/{version}.yaml
- **D-07:** Template variables con Jinja2

### Esquema de versionado
- **D-08:** Semver estricto: v1.0.0, v1.1.0, v2.0.0
- **D-09:** El resolver soporta rangos semver: ^v1.0.0, ~v1.0.0, >= v1.0.0, y tag exacto
- **D-10:** Cada version de prompt tiene un git tag: prompt/{document-type}/v{major}.{minor}.{patch}

### API del PromptResolver
- **D-11:** Clase simple sincrona: PromptResolver(prompts_dir).get(type, version)
- **D-12:** PromptVersion es un Pydantic model con todos los campos
- **D-13:** Validacion al cargar: escanea y valida todos los YAML al instanciar

### the agent's Discretion
- Mecanismo de cache interno - el planner decide segun performance
- Estrategia de error cuando el YAML no se encuentra - el planner elige

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Code
- backend/app/services/llm_service.py - Current EXTRACTION_PROMPT and schema patterns
- backend/app/core/config.py - Pydantic Settings pattern for PromptVersion
- backend/app/services/cv_processor.py - Consumer of llm_service

### Architecture
- .planning/codebase/STACK.md - Python 3.10+, FastAPI, Pydantic
- .planning/codebase/ARCHITECTURE.md - Service layer patterns
- .planning/codebase/INTEGRATIONS.md - Gemini API config pattern

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Pydantic models pattern in backend/app/core/config.py
- Service singleton pattern (module-level instances)
- Logger utility in backend/app/utils/logger.py

### Established Patterns
- Service-based architecture with singletons
- Pydantic Settings for configuration
- .env files for environment config
- JSON-based dynamic schema passing

### Integration Points
- llm_service.py constants and extract_fields()
- cv_processor.py calling llm_service

</code_context>

<specifics>
## Specific Ideas

- El resolver usa backend/prompts/ como source of truth
- YAMLs deben ser legibles como diffs de Git
- Carpetas por tipo facilitan agregar nuevas versiones
- Jinja2 para templates mas expresivos

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope

</deferred>

---

*Phase: 09-Prompt Infrastructure & Foundation*
*Context gathered: 2026-05-19*
