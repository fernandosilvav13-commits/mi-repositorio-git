# Phase 09: Prompt Infrastructure & Foundation - Research

**Researched:** 2026-05-19
**Domain:** Version-controlled prompt registry, YAML-based prompt files, Jinja2 template rendering, semver versioning, Git tag automation
**Confidence:** HIGH

## Summary

This phase builds a version-controlled prompt registry that decouples prompt engineering from code changes. The current `llm_service.py` has hardcoded prompts (`EXTRACTION_PROMPT`, `EXTRACTION_SCHEMA`, fallback schema) — these become YAML files under `backend/prompts/`. A synchronous `PromptResolver` class provides version-aware prompt retrieval with semver range support (`^`, `~`, `>=`). Jinja2 renders dynamic templates with variables like `{{ document_text }}` and `{{ schema }}`. Git tags (`prompt/{document-type}/v{major}.{minor}.{patch}`) provide traceability. Each extraction logs the prompt version to both the existing logger and the `prompt_version` field in Supabase's `extraction_results` table.

**Primary recommendation:** Use PyYAML 6.0.3 for YAML loading (`yaml.safe_load`), Jinja2 3.1.6 for template rendering, `semver` 3.0.4 for version parsing (with a custom thin shim for `^`/`~` range support), and `subprocess` (NOT GitPython) for Git tag creation — GitPython 3.1.50 is in maintenance mode, and the tag operations this phase needs (create, list, delete) are trivially handled by `subprocess.run(["git", ...])` with fewer failure modes.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Migracion desde prompt hardcoded
- **D-01:** Dual por defecto - PromptResolver usa fallback a constantes hardcoded de llm_service.py si no encuentra el YAML solicitado
- **D-02:** Los prompts actuales (EXTRACTION_PROMPT, EXTRACTION_SCHEMA, fallback schema) se migran como YAMLs iniciales: cv-extraction@v1.0 como baseline
- **D-03:** El directorio de prompts va en backend/prompts/, no en la raiz del proyecto
- **D-04:** Cada extraccion registra la version de prompt usada en dos lugares: log del logger existente + campo prompt_version en la tabla extraction_results de Supabase

#### Estructura YAML del prompt
- **D-05:** Formato completo auto-contenido: type, version, description, author, system_prompt, schema (inline como dict), model_params (model, temperature, etc.), tags
- **D-06:** Organizacion por carpetas: backend/prompts/{document-type}/{version}.yaml
- **D-07:** Template variables con Jinja2

#### Esquema de versionado
- **D-08:** Semver estricto: v1.0.0, v1.1.0, v2.0.0
- **D-09:** El resolver soporta rangos semver: ^v1.0.0, ~v1.0.0, >= v1.0.0, y tag exacto
- **D-10:** Cada version de prompt tiene un git tag: prompt/{document-type}/v{major}.{minor}.{patch}

#### API del PromptResolver
- **D-11:** Clase simple sincrona: PromptResolver(prompts_dir).get(type, version)
- **D-12:** PromptVersion es un Pydantic model con todos los campos
- **D-13:** Validacion al cargar: escanea y valida todos los YAML al instanciar

### the agent's Discretion
- Mecanismo de cache interno - el planner decide segun performance
- Estrategia de error cuando el YAML no se encuentra - el planner elige

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PROMPT-01 | System supports version-controlled prompt registry with YAML files, resolver, and Git tracking | Complete — PyYAML for YAML loading, Jinja2 for templates, semver for versioning, subprocess for Git tags, Pydantic v2 for PromptVersion model |

</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Prompt file storage | Backend (service layer) | — | YAML files under `backend/prompts/` are read by PromptResolver, a service-level component |
| Prompt resolution & version matching | Backend (service layer) | — | Synchronous lookup — no async, no I/O beyond filesystem reads at init |
| Template rendering (Jinja2) | Backend (service layer) | — | Called by llm_service at extraction time — prompt is rendered with document_text + schema |
| Git tag creation | Backend (CLI/subprocess) | — | `subprocess.run(["git", "tag", ...])` from Python — no server needs this, it's a dev/maintenance operation |
| Prompt version logging | Backend (service layer) | Database | Two targets: Python logger + Supabase `extraction_results.prompt_version` field |
| Prompt YAML authoring | Developer (manual) | — | Humans write YAML files — no UI component needed |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| PyYAML | 6.0.3 | Parse prompt YAML files | De facto standard for YAML in Python — `yaml.safe_load()` is the safe default |
| Jinja2 | 3.1.6 | Template rendering for dynamic prompts | Industry standard Python template engine — used by Flask, Ansible, Sphinx |
| semver | 3.0.4 | Parse, compare, and bump semver versions | Purpose-built for Semantic Versioning — `semver.Version.parse("1.0.0")` returns structured version objects |
| Pydantic v2 | 2.x (already in project) | PromptVersion data model | Already in project — matches existing schema pattern in `backend/app/schemas/` |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| packaging | 20+ (transitive dep) | PEP 440 version specifier comparison | Alternative to custom ^/~ range logic |
| pytest | 8.x (already in project) | Test PromptResolver with tmp_path | Testing file-based registry operations |
| subprocess (stdlib) | — | Git tag operations | Creating/listing Git tags — no external dependency needed |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| PyYAML | ruamel.yaml 0.19.1 | ruamel.yaml preserves comments and YAML 1.2, but adds complexity. PyYAML suffices since we only READ YAML, never write back. |
| subprocess for Git tags | GitPython 3.1.50 | GitPython is in **maintenance mode** (no new features, security-only fixes). subprocess is simpler, zero-dependency for tag ops. |
| semver | python-semanticversion (semantic_version) | `semantic_version` has built-in `NpmSpec` for `^`/`~`. But `semver` is more widely used (47M+ downloads vs 10M+). Custom `^`/`~` logic with `semver` is ~20 lines. |

**Installation:**
```bash
# Add to backend/requirements.txt:
pyyaml
jinja2
semver
```

**Version verification:** [VERIFIED: pip list in project venv] — PyYAML 6.0.3 (2025-09-25), Jinja2 3.1.6 (2025-03-05), semver 3.0.4 (2025-01-24), GitPython 3.1.50 (2026-04-30).

## Architecture Patterns

### System Architecture Diagram

```
                          PromptResolver Architecture

  [YAML files on disk]
  backend/prompts/
  ├── cv-extraction/
  │   ├── v1.0.0.yaml         ◄── Baseline (from hardcoded constants)
  │   ├── v1.1.0.yaml         ◄── Future: updated prompt
  │   └── ...
  ├── certificate/
  │   └── v1.0.0.yaml         ◄── Future: type-specific prompt (Phase 13)

          │
          ▼
  ┌──────────────────────────┐
  │     PromptResolver       │  ◄── Synchronous, module-level singleton
  │                          │       (existing pattern from llm_service, cv_processor)
  │  ┌────────────────────┐  │
  │  │ __init__(path)     │  │  Scans all YAMLs, validates, stores in
  │  │  scan + validate   │  │  internal dict[type][version]
  │  └────────────────────┘  │
  │  ┌────────────────────┐  │
  │  │ get(type, version) │  │  Returns PromptVersion or None
  │  │  match semver      │  │  Supports: v1.0.0, ^v1.0.0, ~v1.0.0
  │  └────────────────────┘  │
  │  ┌────────────────────┐  │
  │  │ render(pv, context)│  │  Jinja2 template rendering
  │  └────────────────────┘  │
  └──────────┬───────────────┘
             │
             ▼
  ┌──────────────────────────┐
  │    llm_service.py        │  ◄── Consumer
  │  extract_fields(         │
  │   text, schema,          │
  │   prompt_version="^v1"   │  ← NEW param
  │  )                       │
  └──────────┬───────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
  Logger            Supabase
  (existing)        extraction_results
                    prompt_version column

  Git tags (dev operation, NOT called from extraction flow):
  prompt/cv-extraction/v1.0.0
  prompt/cv-extraction/v1.1.0
```

**Data flow for extraction with versioned prompts:**
1. `extract_fields()` receives optional `prompt_version` (defaults to `"^v1.0.0"`)
2. `PromptResolver.get("cv-extraction", "^v1.0.0")` matches highest compatible version
3. Returns `PromptVersion` with system_prompt, schema, model_params
4. `render()` runs Jinja2 with `{document_text, schema}` context
5. Rendered prompt sent to Gemini API
6. After extraction, version_tag logged + stored in Supabase

### Recommended Project Structure
```
backend/
├── prompts/                              # NEW — prompt registry root
│   ├── cv-extraction/
│   │   ├── v1.0.0.yaml                   # Initial baseline
│   │   └── v1.1.0.yaml                   # Future
│   └── certificate/
│       └── v1.0.0.yaml
├── app/
│   ├── services/
│   │   ├── llm_service.py                # MODIFIED
│   │   ├── prompt_resolver.py            # NEW
│   ├── schemas/
│   │   ├── prompt.py                     # NEW — PromptVersion model
│   └── core/
│       └── config.py                     # Add prompts_dir
└── tests/
    ├── test_prompt_resolver.py           # NEW
    └── conftest.py
```

### Pattern 1: PromptVersion Pydantic Model

**What:** A Pydantic v2 `BaseModel` for a single prompt YAML's contents.

**When to use:** Every YAML prompt file deserialized into this model at resolver init.

**Example** [VERIFIED: project patterns in backend/app/schemas/]:
```python
from pydantic import BaseModel, Field
from typing import Any
from semver import Version


class PromptVersion(BaseModel):
    """Single versioned prompt with all metadata."""
    type: str
    version: str                                       # e.g. "1.0.0"
    description: str = ""
    author: str = ""
    system_prompt: str                                 # Jinja2 template
    schema: dict[str, Any]                             # JSON schema (inline)
    model_params: dict[str, Any] = Field(default_factory=lambda: {
        "model": "gemini-2.5-flash-lite",
        "temperature": 0.1,
    })
    tags: list[str] = []

    @property
    def semver(self) -> Version:
        return Version.parse(self.version)

    @property
    def tag_name(self) -> str:
        return f"prompt/{self.type}/v{self.version}"
```

### Pattern 2: Git Tag via Subprocess

**What:** Create and list Git tags using `subprocess.run`.

**When to use:** Git tag operations from Python.

**Example** [VERIFIED: subprocess is stdlib; GitPython maintenance mode on GitHub]:
```python
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def create_prompt_tag(tag_name: str, message: str) -> None:
    result = subprocess.run(
        ["git", "tag", "-a", tag_name, "-m", message],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create tag: {result.stderr}")

def list_prompt_tags(doc_type: str | None = None) -> list[str]:
    pattern = f"prompt/{doc_type}/v*" if doc_type else "prompt/*"
    result = subprocess.run(
        ["git", "tag", "-l", pattern],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    return result.stdout.strip().split("\n") if result.stdout.strip() else []
```

### Pattern 3: Semver Range Matching (^, ~, >=)

**What:** Resolve npm-style semver ranges to concrete versions.

**When to use:** Inside `PromptResolver.get()`.

**Example** [VERIFIED: semver 3.0.4 docs — Version comparison]:
```python
from semver import Version

def match_version(expr: str, available: list[str]) -> str | None:
    raw = expr.lstrip("v")
    versions = sorted(
        [Version.parse(v.lstrip("v")) for v in available], reverse=True,
    )
    if "^" in expr:
        target = Version.parse(raw.lstrip("^"))
        upper = Version(target.major + 1, 0, 0) if target.major > 0 else Version(0, target.minor + 1, 0)
        candidates = [v for v in versions if target <= v < upper]
    elif "~" in expr:
        target = Version.parse(raw.lstrip("~"))
        upper = Version(target.major, target.minor + 1, 0)
        candidates = [v for v in versions if target <= v < upper]
    elif ">=" in expr:
        target = Version.parse(raw.lstrip(">="))
        candidates = [v for v in versions if v >= target]
    else:
        target = Version.parse(raw)
        return available[versions.index(target)] if target in versions else None
    if candidates:
        ver = candidates[0]
        for key in available:
            if Version.parse(key.lstrip("v")) == ver:
                return key.lstrip("v")
    return None
```

### Anti-Patterns to Avoid
- **`yaml.load()` without Loader:** Always use `yaml.safe_load()` — prevents arbitrary code execution. [CITED: PyYAML docs]
- **GitPython for simple tags:** GitPython in maintenance mode. subprocess is simpler for git tag ops.
- **Async PromptResolver:** CPU-bound (YAML parse + Jinja compile), not I/O. Matches existing sync pattern.
- **Cache without invalidation:** If caching added, must handle hot-reload of YAML files.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YAML parsing | Custom parser | PyYAML 6.0.3 (safe_load) | YAML spec is complex — anchors, aliases, multi-doc |
| Template rendering | .format() concatenation | Jinja2 3.1.6 | Conditionals, loops, filters, safe escaping |
| Semver parsing | Manual string split | semver 3.0.4 | Edge cases: pre-release, build metadata |
| Git tag creation | Custom git objects | subprocess + git CLI | CLI is the stable API for git |

**Key insight:** Every problem has a well-established library. New code is only the orchestration layer (PromptResolver) connecting libraries.

## Common Pitfalls

### Pitfall 1: YAML File Encoding
**What:** Non-UTF-8 YAML files cause parse errors.
**Why:** Different OS encoding defaults.
**Avoid:** Enforce `encoding="utf-8"` when opening. Add `.gitattributes` with `*.yaml text eol=lf`.
**Signs:** `yaml.scanner.ScannerError` with unexpected characters.

### Pitfall 2: Jinja2 Delimiter Conflicts
**What:** Prompt text with `{{` or `{%` interpreted as Jinja2 syntax.
**Why:** Jinja2 uses `{{ }}` for expressions, `{% %}` for statements.
**Avoid:** Use `{% raw %}...{% endraw %}` blocks in YAML prompts. Or configure custom delimiters.
**Signs:** `jinja2.exceptions.TemplateSyntaxError`.

### Pitfall 3: Semver Range Boundaries
**What:** `^v1.0.0` incorrectly matches v2.0.0 or `~v1.2.3` matches v1.3.0.
**Why:** npm semver range semantics are subtle.
**Avoid:** Write explicit boundary tests for each operator.
**Signs:** Resolver returns wrong version.

### Pitfall 4: Git Tag Collisions
**What:** Creating duplicate tags fails (tags are immutable).
**Why:** Two devs create same prompt version.
**Avoid:** Check `git tag -l "prompt/*/v1.0.0"` first. Use annotated tags.
**Signs:** `git: tag '...' already exists`.

### Pitfall 5: Stale Registry at Runtime
**What:** New YAML files added to disk while server runs are invisible.
**Why:** PromptResolver scans only at init.
**Avoid:** Document that server restart is needed. If caching added, implement TTL or reload().

## Code Examples

### Full PromptResolver Implementation
```python
"""PromptResolver — version-controlled prompt registry."""
import logging
from pathlib import Path
import yaml
import json
from jinja2 import Environment, BaseLoader
from pydantic import ValidationError
from app.schemas.prompt import PromptVersion

logger = logging.getLogger(__name__)


class PromptResolver:
    """Synchronous resolver for versioned YAML prompt files."""

    def __init__(self, prompts_dir: str | Path) -> None:
        self._prompts_dir = Path(prompts_dir)
        self._jinja = Environment(loader=BaseLoader(), autoescape=False)
        self._registry: dict[str, dict[str, PromptVersion]] = {}
        self._scan_all()

    def _scan_all(self) -> None:
        if not self._prompts_dir.is_dir():
            logger.warning("Prompts directory not found: %s", self._prompts_dir)
            return
        for yaml_path in self._prompts_dir.rglob("*.yaml"):
            if yaml_path.parent == self._prompts_dir:
                continue
            doc_type = yaml_path.parent.name
            version_stem = yaml_path.stem
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict):
                logger.warning("Invalid YAML: %s", yaml_path)
                continue
            try:
                prompt = PromptVersion(**data)
            except ValidationError as exc:
                logger.warning("Validation failed: %s: %s", yaml_path, exc)
                continue
            version_key = version_stem.lstrip("v")
            if prompt.version != version_key:
                prompt.version = version_key
            self._registry.setdefault(doc_type, {})[version_key] = prompt
        logger.info(
            "Loaded %d prompt types, %d total versions",
            len(self._registry),
            sum(len(v) for v in self._registry.values()),
        )

    def get(self, doc_type: str, version_expr: str = "^v1.0.0") -> PromptVersion | None:
        available = self._registry.get(doc_type)
        if not available:
            logger.warning("No prompts for type '%s'", doc_type)
            return None
        matched = _match_version(version_expr, list(available.keys()))
        if matched is None:
            logger.warning("No version matched: type=%s expr=%s", doc_type, version_expr)
            return None
        return available[matched]


def _match_version(expr: str, available: list[str]) -> str | None:
    from semver import Version
    raw = expr.lstrip("v")
    versions = sorted(
        [Version.parse(v.lstrip("v")) for v in available], reverse=True,
    )
    if "^" in expr:
        target = Version.parse(raw.lstrip("^"))
        upper = Version(target.major + 1, 0, 0) if target.major > 0 else Version(0, target.minor + 1, 0)
        candidates = [v for v in versions if target <= v < upper]
    elif "~" in expr:
        target = Version.parse(raw.lstrip("~"))
        upper = Version(target.major, target.minor + 1, 0)
        candidates = [v for v in versions if target <= v < upper]
    elif ">=" in expr:
        target = Version.parse(raw.lstrip(">="))
        candidates = [v for v in versions if v >= target]
    else:
        target = Version.parse(raw)
        return available[versions.index(target)] if target in versions else None
    if candidates:
        ver = candidates[0]
        for key in available:
            if Version.parse(key.lstrip("v")) == ver:
                return key.lstrip("v")
    return None
```

### YAML Prompt File (v1.0.0 baseline)
```yaml
# backend/prompts/cv-extraction/v1.0.0.yaml
type: cv-extraction
version: 1.0.0
description: Baseline CV extraction prompt from hardcoded EXTRACTION_PROMPT
author: system

system_prompt: |
  Extrae datos del texto segun el esquema JSON.
  Responde SOLO con el JSON. Si falta algo, usa "NO ENCONTRADO".
  No inventes datos. Respeta nombres de claves.

  Schema: {{ schema | tojson }}

  Text:
  {{ document_text }}

schema:
  type: object
  properties:
    NOMBRES:
      type: string
      description: "Nombre completo de la persona"
    APELLIDO_PATERNO: { type: string }
    APELLIDO_MATERNO: { type: string }
    RUT: { type: string }
    FECHA_NACIMIENTO: { type: string }
    NACIONALIDAD: { type: string }
    TELEFONO: { type: string }
    EMAIL: { type: string }
    DIRECCION: { type: string }
    PROFESION: { type: string }
    EDUCACION:
      type: array
      items:
        type: object
        properties:
          institucion: { type: string }
          titulo: { type: string }
          ano_inicio: { type: string }
          ano_termino: { type: string }
    EXPERIENCIA_LABORAL:
      type: array
      items:
        type: object
        properties:
          empresa: { type: string }
          cargo: { type: string }
          ano_inicio: { type: string }
          ano_termino: { type: string }
          funciones: { type: string }
    IDIOMAS:
      type: array
      items:
        type: object
        properties:
          idioma: { type: string }
          nivel: { type: string }

model_params:
  model: gemini-2.5-flash-lite
  temperature: 0.1
  response_mime_type: application/json

tags:
  - baseline
  - cv
```

### Integrating PromptResolver into llm_service.py
```python
from app.services.prompt_resolver import PromptResolver

prompt_resolver = PromptResolver("backend/prompts")

async def extract_fields(
    text: str, schema: dict,
    model: str | None = None,
    fallback_schema: dict | None = None,
    fallback_model: str | None = None,
    prompt_version: str | None = "^v1.0.0",
) -> dict:
    resolved = prompt_resolver.get("cv-extraction", prompt_version)
    if resolved:
        rendered = prompt_resolver._jinja.from_string(resolved.system_prompt).render(
            document_text=text, schema=json.dumps(schema),
        )
        prompt_text = rendered
        version_tag = resolved.tag_name
        effective_model = resolved.model_params.get("model", model or settings.gemini_model_extract)
        temperature = resolved.model_params.get("temperature", 0.1)
    else:
        prompt_text = f"{EXTRACTION_PROMPT}\nSchema: {json.dumps(schema)}\nText: {text}"
        version_tag = "hardcoded-fallback"
        effective_model = model or settings.gemini_model_extract
        temperature = 0.1

    # ... LLM call with rendered prompt, effective_model, temperature ...
    logger.info("Extraction with prompt version: %s", version_tag)
    # Return version_tag with result for Supabase persistence
```

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (already in requirements.txt) |
| Config file | backend/pyproject.toml or pytest.ini |
| Quick run | `pytest backend/tests/test_prompt_resolver.py -x` |
| Full suite | `pytest backend/tests/ -x` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PROMPT-01 | Load valid YAML files from disk | unit | `pytest tests/test_prompt_resolver.py::test_load_valid_yaml -x` | ❌ Wave 0 |
| PROMPT-01 | Reject invalid YAML with ValidationError | unit | `pytest tests/test_prompt_resolver.py::test_reject_invalid_yaml -x` | ❌ Wave 0 |
| PROMPT-01 | Exact version match | unit | `pytest tests/test_prompt_resolver.py::test_exact_version -x` | ❌ Wave 0 |
| PROMPT-01 | ^ caret range operator | unit | `pytest tests/test_prompt_resolver.py::test_caret_range -x` | ❌ Wave 0 |
| PROMPT-01 | ~ tilde range operator | unit | `pytest tests/test_prompt_resolver.py::test_tilde_range -x` | ❌ Wave 0 |
| PROMPT-01 | >= range operator | unit | `pytest tests/test_prompt_resolver.py::test_gte_range -x` | ❌ Wave 0 |
| PROMPT-01 | No match returns None | unit | `pytest tests/test_prompt_resolver.py::test_no_match -x` | ❌ Wave 0 |
| PROMPT-01 | Jinja2 rendering with context | unit | `pytest tests/test_prompt_resolver.py::test_jinja_rendering -x` | ❌ Wave 0 |
| PROMPT-01 | Fallback to hardcoded when YAML missing | unit | `pytest tests/test_prompt_resolver.py::test_fallback -x` | ❌ Wave 0 |
| PROMPT-01 | Filename/version mismatch warning | unit | `pytest tests/test_prompt_resolver.py::test_filename_version_mismatch -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tests/test_prompt_resolver.py -x`
- **Per wave merge:** `pytest backend/tests/ -x`
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/test_prompt_resolver.py` — covers PROMPT-01
- [ ] `backend/tests/conftest.py` — may need updates for tmp_path fixtures

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V5 Input Validation | yes | PyYAML safe_load prevents YAML tag injection; Pydantic validates PromptVersion fields |
| V6 Cryptography | no | Not applicable — prompt files are plain text |

### Known Threat Patterns

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| YAML tag injection | Tampering | `yaml.safe_load()` — never `yaml.load()` with default Loader |
| Jinja2 SSTI | Elevation of Privilege | Templates authored by devs, not users. Context passed as render data, not template code. |

**Key:** Prompt YAMLs are committed to Git by developers. Defense-in-depth: use `safe_load()` and pass context as data, not template code.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| PyYAML 5.x safe_load default | PyYAML 6.x requires explicit Loader | 2021 | Must use `yaml.safe_load(data)` |
| GitPython active development | GitPython maintenance mode | ~2024 | Prefer subprocess for new Git ops |
| semver 2.x parse() API | semver 3.x Version.parse() | 2022 | Use `Version.parse()` not `parse()` |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | PyYAML safe_load preserves dict key order in Python 3.12 | Standard Stack | LOW — Python 3.7+ dicts preserve insertion order |
| A2 | PromptResolver module-level singleton pattern | Code Examples | LOW — matches existing cv_processor, ocr_service |
| A3 | Jinja2 autoescape=False safe for prompt templates | Code Examples | LOW — dev-authored content, not user input |
| A4 | semver Version comparison works with ^/~ shim boundaries | Architecture Patterns | MEDIUM — pre-release edge cases |

## Open Questions (RESOLVED)

1. **Should Git tag creation be automatic (CLI script) or manual (documented git command)?** — RESOLVED: Plan 02 implements `create_prompt_tag()` and `list_prompt_tags()` as static methods on PromptResolver, scriptable via `python3 -c` or import.

2. **Module-level singleton or dependency injection for PromptResolver?** — RESOLVED: Plan 02 creates a sync class with `prompts_dir` constructor arg for testability. Singleton instantiation deferred to llm_service.py integration (future phase).

3. **Does adding prompt_version to extraction_results require a Supabase migration?** — RESOLVED: D-04 is partially addressed in Plan 02 via `tag_name` property for logging. Actual Supabase schema migration for the `prompt_version` column is deferred to the phase that wires PromptResolver into llm_service.py (Phase 13 or Phase 9 follow-up).

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.12 | All code | ✓ | 3.12.3 | — |
| git CLI | Git tag operations | ✓ | 2.43.0 | — |
| PyYAML | YAML parsing | ✓ (installed) | 6.0.3 | — |
| Jinja2 | Template rendering | ✓ (installed) | 3.1.6 | — |
| semver | Version parsing | ✓ (installed) | 3.0.4 | — |

**Missing with fallback:** None.
**Missing blocking:** None.

## Sources

### Primary (HIGH confidence)
- [PyPI: PyYAML 6.0.3](https://pypi.org/project/PyYAML/) — verified 2025-09-25
- [PyPI: Jinja2 3.1.6](https://pypi.org/project/Jinja2/) — verified 2025-03-05
- [PyPI: semver 3.0.4](https://pypi.org/project/semver/) — verified 2025-01-24
- [PyPI: GitPython 3.1.50](https://pypi.org/project/GitPython/) — verified 2026-05-05
- [Jinja2 API docs](https://jinja.palletsprojects.com/en/stable/api/)
- [PyYAML docs](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [semver 3.0.4 docs](https://python-semver.readthedocs.io/en/stable/)
- Existing code: llm_service.py, config.py, logger.py, conftest.py

### Secondary (MEDIUM confidence)
- WebSearch: safe_load is recommended PyYAML default
- WebSearch: npm semver range semantics (^, ~) cross-verified

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all versions verified against PyPI and installed in venv
- Architecture: HIGH — patterns match existing codebase conventions
- Pitfalls: MEDIUM — based on known patterns, context-specific

**Research date:** 2026-05-19
**Valid until:** 2026-06-19 (30 days)
