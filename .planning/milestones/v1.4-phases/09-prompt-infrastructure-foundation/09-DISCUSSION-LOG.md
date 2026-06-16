# Phase 09: Prompt Infrastructure & Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-05-19
**Phase:** 09-prompt-infrastructure-foundation
**Areas discussed:** Migracion desde prompt hardcoded, Estructura YAML del prompt, Esquema de versionado, API del PromptResolver

---

## Migracion desde prompt hardcoded

| Option | Description | Selected |
|--------|-------------|----------|
| Corte directo | Migrar todo de una: EXTRACTION_PROMPT y schemas a YAMLs | |
| Dual por defecto | Ambos coexisten: registry con fallback a hardcoded | ✓ |
| Feature flag | Arranca con ENABLE_PROMPT_REGISTRY=false | |

**User's choice:** Dual por defecto
**Notes:** Fallback al hardcoded si el YAML no existe

| Option | Description | Selected |
|--------|-------------|----------|
| Migrarlos como YAMLs iniciales | Primer commit con cv-extraction@v1.0 baseline | ✓ |
| Dejarlos como hardcoded | Solo nuevos prompts van al registry | |

**User's choice:** Migrarlos como YAMLs iniciales
**Notes:** Los prompts actuales son el baseline, no legacy

| Option | Description | Selected |
|--------|-------------|----------|
| Raiz del proyecto | prompts/ en la raiz | |
| Dentro del backend | backend/prompts/ cerca del codigo | ✓ |

**User's choice:** Dentro del backend
**Notes:** backend/prompts/

| Option | Description | Selected |
|--------|-------------|----------|
| En el log nomas | Logger existente registra la version | |
| En la base de datos | Campo en extraction_results | |
| Ambos | Log + campo DB | ✓ |

**User's choice:** Ambos
**Notes:** Logger para debugging en vivo, DB para analisis historico

---

## Estructura YAML del prompt

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal | Solo type, version, system_prompt, model_params | |
| Completa | Todo: type, version, description, author, system_prompt, schema, model_params, tags | ✓ |
| Modular | system_prompt + schema referenciado por ID | |

**User's choice:** Completa
**Notes:** Todo auto-contenido en un YAML

| Option | Description | Selected |
|--------|-------------|----------|
| Un archivo por prompt | cv-extraction@v1.0.yaml plano | |
| Carpetas por tipo | backend/prompts/cv-extraction/v1.0.yaml | ✓ |
| Archivo unico multi-doc | Un solo prompts.yaml | |

**User's choice:** Carpetas por tipo de documento
**Notes:** Facilita agregar versiones sin editar archivos existentes

| Option | Description | Selected |
|--------|-------------|----------|
| Jinja2 | Template engine completo con condicionales y filtros | ✓ |
| Variables simples | Solo {{variable}} con string.Template | |
| No, concatenacion directa | El prompt YAML es el prompt final | |

**User's choice:** Jinja2
**Notes:** Para {{document_text}}, {{schema}}, y futuros templates

---

## Esquema de versionado

| Option | Description | Selected |
|--------|-------------|----------|
| Semver estricto | v1.0.0, v1.1.0, v2.0.0 | ✓ |
| Semver simplificado | v1, v2, v1.2 (major.minor) | |
| Date-based | v2026-05-19 | |

**User's choice:** Semver estricto
**Notes:** Major = schema incompatible, minor = mejora prompt, patch = bugfix

| Option | Description | Selected |
|--------|-------------|----------|
| Tag exacto obligatorio | Solo devuelve si existe exactamente | |
| Tag exacto + latest | latest resuelve al mayor semver | |
| Rangos semver | ^v1.0.0, ~v1.0.0, >= v1.0.0 | ✓ |

**User's choice:** Rangos semver
**Notes:** Como package.json, maxima flexibilidad

| Option | Description | Selected |
|--------|-------------|----------|
| Independientes | YAML filename es el version | |
| Git tags sync | prompt/cv-extraction/v1.0.0 como git tag | ✓ |
| Git tags como source of truth | Resolver usa git describe | |

**User's choice:** Git tags sync
**Notes:** Cada version de prompt tiene un git tag asociado

---

## API del PromptResolver

| Option | Description | Selected |
|--------|-------------|----------|
| Clase simple sincrona | PromptResolver().get(type, version) | ✓ |
| Clase con cache | Con LRU cache interno | |
| Async con factory | Preparado para registry remoto | |

**User's choice:** Clase simple sincrona
**Notes:** Sin async overhead, simple de testear

| Option | Description | Selected |
|--------|-------------|----------|
| Pydantic model | PromptVersion validado con Pydantic | ✓ |
| TypedDict | Tipado sin validacion | |
| Dict plano | Sin estructura | |

**User's choice:** Pydantic model
**Notes:** Consistente con el resto del proyecto que ya usa Pydantic

| Option | Description | Selected |
|--------|-------------|----------|
| Validacion al cargar | Escanea y valida todos los YAML al instanciar | ✓ |
| Validacion bajo demanda | Solo valida cuando piden un prompt | |
| Sin validacion | Confia en YAMLs bien formados | |

**User's choice:** Validacion al cargar
**Notes:** Error temprano si hay YAML mal formados

---

## the agent's Discretion

- Mecanismo de cache interno (LRU o sin cache)
- Estrategia de error cuando el YAML no se encuentra (raise vs None vs default)

## Deferred Ideas

None

