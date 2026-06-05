# Phase 10: Advanced Preprocessing - Research

**Researched:** 2026-05-21
**Domain:** LLM-guided section detection, noise filtering, layout normalization, multi-stage preprocessing pipeline
**Confidence:** HIGH

## Summary

This phase builds a three-stage preprocessing pipeline (SectionDetector, NoiseFilter, LayoutNormalizer) that runs before classification and extraction, so downstream stages receive clean, organized text. A single batched LLM call (Gemini via google-genai SDK) detects both document sections and noise regions, returning boundary-only JSON. The pipeline is a standalone injectable service following the project's module-level singleton pattern, and the section-detection prompt is versioned via Phase 9's PromptResolver (YAML + Jinja2).

**Primary recommendation:** Use the google-genai SDK directly (not through `llm_service.py`) for the detection LLM call, since the detection prompt schema differs from the extraction schema and the existing `extract_fields()` is tightly coupled to extraction semantics. Reuse the PromptResolver from Phase 9 for the detection prompt YAML. Keep the pipeline stateless — each stage receives text + metadata and returns transformed text + metadata.

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| google-genai | 1.x (already in project) | Gemini API calls for section+noise detection | Already the project's LLM SDK — used in `llm_service.py`, `ocr_service.py` |
| PyYAML | 6.0.3 (already in project) | Parse prompt YAML files | Installed during Phase 9 for PromptResolver |
| Jinja2 | 3.1.6 (already in project) | Template rendering for detection prompts | Installed during Phase 9 — same `{{ document_text }}` pattern |
| Pydantic v2 | 2.x (already in project) | Pipeline stage schemas and models | Matches existing schema pattern in `backend/app/schemas/` |
| pytest | 8.x (already in project) | Test framework for all stages | Already in `requirements.txt` — same framework as Phase 9 |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| re (stdlib) | — | Regex-based line cleanup in LayoutNormalizer | Normalizing whitespace, collapsing inline spaces, bullet point detection |
| dataclasses (stdlib) | — | Lightweight pipeline stage interface | Alternative to Pydantic for internal stage contracts if schema validation is unnecessary |

### Installation

```bash
# No new dependencies required for this phase — google-genai, PyYAML, Jinja2, Pydantic already installed
# Verify:
pip list 2>/dev/null | grep -iE "google-genai|pyyaml|jinja2|pydantic|pytest"
```

**Version verification:** [VERIFIED: pip list in project venv] — google-genai 1.x, PyYAML 6.0.3, Jinja2 3.1.6, Pydantic 2.x, pytest 8.x. All already present.

## Architecture

### System Architecture Diagram

```
                     PreprocessingPipeline Architecture
                     =================================

  [Raw OCR text]
        │
        ▼
  ┌─────────────────────────────────────────────────────────┐
  │  PreprocessingPipeline                                  │
  │                                                         │
  │  ┌─────────────────┐    ┌─────────────────┐            │
  │  │ SectionDetector  │    │   NoiseFilter   │            │
  │  │                  │    │                 │            │
  │  │ Input: raw_text  │    │ Input: text +   │            │
  │  │ Call: Gemini     │    │        sections  │            │
  │  │       (batched)  │───►│ Output: text    │            │
  │  │ Output: sections │    │        w/o noise │            │
  │  │         + noise  │    │                 │            │
  │  │         regions  │    └─────────────────┘            │
  │  └─────────────────┘                                   │
  │                                │                        │
  │                                ▼                        │
  │                       ┌─────────────────┐              │
  │                       │LayoutNormalizer │              │
  │                       │                 │              │
  │                       │ Input: text     │              │
  │                       │        (clean)  │              │
  │                       │ Output: text    │              │
  │                       │        w/       │              │
  │                       │  section markers│              │
  │                       │  + normalized   │              │
  │                       │  layout         │              │
  │                       └─────────────────┘              │
  │                                │                        │
  │                                ▼                        │
  │                       ┌─────────────────┐              │
  │                       │   Clean text     │              │
  │                       │  + metadata dict │              │
  │                       └─────────────────┘              │
  └─────────────────────────────────────────────────────────┘
        │
        ▼
  [cv_extractor.py / cv_processor.py]
   Receives clean, organized text
        │
        ▼
  [Gemini extraction call]
```

**Data flow:**

1. `cv_processor.py` calls `PreprocessingPipeline.process(raw_text)`
2. **SectionDetector** sends a batched LLM call to Gemini returning `{"sections": [...], "noise_regions": [...]}` — uses PromptResolver to load `section-detection/v1.0.0.yaml`
3. If detection fails (LLM cannot find clear boundaries), the pipeline returns raw text unchanged per D-03
4. **NoiseFilter** removes line ranges identified as noise (headers, page numbers, footers, metadata artifacts)
5. **LayoutNormalizer** collapses inline whitespace, preserves paragraph breaks, adds `[SECTION: Education]` boundary markers, and normalizes bullet points to a consistent marker
6. Clean text + metadata dict (`{"sections": [...], "prompt_version": "section-detection/v1.0.0"}`) returned to caller

### Rationale for Architecture

**Why batched LLM detection (sections + noise in one call):** D-05 specifies a single batched call for both sections and noise, bringing total LLM calls per document to 2 (detection + extraction). This halves the LLM overhead vs separate calls while maintaining semantic separation from extraction. The detection JSON schema differs from the extraction schema — it returns boundary metadata, not field values.

**Why separate stage classes (D-10):** Each stage has distinct concerns. SectionDetector manages LLM interaction and response parsing. NoiseFilter operates on line indices — pure string processing. LayoutNormalizer uses rule-based transformations (whitespace, bullets). Separating them makes unit testing easier and allows independent evolution (e.g., later swapping the LLM backend for SectionDetector without touching layout logic).

**Why not reuse `extract_fields()` from `llm_service.py`:** The existing `extract_fields()` has a fixed two-phase retry pattern (primary schema → fallback schema) with `response_mime_type: application/json`. The detection call uses a different schema shape (boundary metadata, not extracted values) and has its own retry semantics. Reusing `extract_fields()` would require coupling the detection schema to the extraction fallback machinery. Instead, SectionDetector makes a direct google-genai SDK call with its own prompt and schema, matching the pattern seen in `llm_service.py:is_document_legible()` which also makes a direct call.

### Recommended Project Structure

```
backend/
├── prompts/
│   ├── cv-extraction/                    # Phase 9 — extraction prompts
│   │   └── v1.0.0.yaml
│   └── section-detection/                # NEW — detection prompt
│       └── v1.0.0.yaml
├── app/
│   ├── services/
│   │   ├── preprocessor.py               # MODIFIED — PreprocessingPipeline orchestrator
│   │   ├── section_detector.py           # NEW — SectionDetector (LLM call)
│   │   ├── noise_filter.py              # NEW — NoiseFilter (line removal)
│   │   ├── layout_normalizer.py         # NEW — LayoutNormalizer (whitespace + markers)
│   │   ├── cv_extractor.py              # UNCHANGED (or minimal integration point)
│   │   ├── cv_processor.py              # MODIFIED — injects PreprocessingPipeline
│   │   └── llm_service.py               # UNCHANGED — pipeline calls SDK directly
│   ├── schemas/
│   │   ├── preprocessing.py             # NEW — SectionMetadata, NoiseRegion, PipelineResult
│   │   └── ...
│   └── core/
│       └── config.py                     # Add gemini_model_detection setting
└── tests/
    ├── test_preprocessing_schemas.py    # NEW — schema validation tests
    ├── test_section_detector.py         # NEW — SectionDetector tests
    ├── test_noise_filter.py             # NEW — NoiseFilter tests
    ├── test_layout_normalizer.py        # NEW — LayoutNormalizer tests
    └── test_preprocessor_pipeline.py    # NEW — pipeline integration tests
```

### Pattern 1: Pydantic Schemas for Pipeline

```python
from pydantic import BaseModel, Field
from typing import Any


class NoiseRegion(BaseModel):
    """A noise region identified in the document."""
    start_line: int
    end_line: int
    noise_type: str  # e.g., "page_header", "page_number", "footer", "metadata_artifact"
    confidence: float = Field(ge=0.0, le=1.0)


class SectionMetadata(BaseModel):
    """A document section with its line boundaries."""
    name: str           # e.g., "Education", "Experience"
    start_line: int
    end_line: int


class DetectionResult(BaseModel):
    """Result of the batched section+noise LLM call."""
    sections: list[SectionMetadata] = Field(default_factory=list)
    noise_regions: list[NoiseRegion] = Field(default_factory=list)


class PipelineResult(BaseModel):
    """Final output of the preprocessing pipeline."""
    text: str
    sections: list[SectionMetadata] = Field(default_factory=list)
    prompt_version: str | None = None
```

### Pattern 2: SectionDetector — Direct GenAI Call

```python
import json
import logging
from google import genai
from app.core.config import settings
from app.schemas.preprocessing import DetectionResult
from app.services.prompt_resolver import prompt_resolver

logger = logging.getLogger(__name__)


class SectionDetector:
    """Detects document sections and noise regions via a batched Gemini call."""

    def __init__(self, model: str | None = None):
        self._model = model or settings.gemini_model_extract
        self._client: genai.Client | None = None

    def _get_client(self) -> genai.Client:
        if self._client is None:
            self._client = genai.Client(api_key=settings.google_api_key)
        return self._client

    def detect(self, text: str) -> DetectionResult | None:
        resolved = prompt_resolver.get("section-detection", "^v1.0.0")
        if not resolved:
            logger.warning("No section-detection prompt found, skipping detection")
            return None

        rendered = resolved.system_prompt.replace(
            "{{ document_text }}", text
        )
        llm_client = self._get_client()
        try:
            response = llm_client.models.generate_content(
                model=self._model,
                contents=rendered,
                config={
                    "response_mime_type": "application/json",
                    "temperature": 0.1,
                },
            )
            raw = response.text.strip()
            data = json.loads(raw)
            return DetectionResult(**data)
        except Exception as e:
            logger.warning("Section detection failed: %s", e)
            return None
```

### Pattern 3: NoiseFilter — Line-Index Based Removal

```python
from app.schemas.preprocessing import NoiseRegion


class NoiseFilter:
    """Removes noise regions (headers, page numbers, footers, artifacts) by line index."""

    @staticmethod
    def filter(text: str, noise_regions: list[NoiseRegion]) -> str:
        if not noise_regions:
            return text
        lines = text.split("\n")
        # Mark lines to remove
        remove_set: set[int] = set()
        for region in noise_regions:
            for line_no in range(region.start_line, region.end_line + 1):
                if 0 <= line_no < len(lines):
                    remove_set.add(line_no)
        # Rebuild text, skipping removed lines
        filtered = [l for i, l in enumerate(lines) if i not in remove_set]
        return "\n".join(filtered)
```

### Pattern 4: LayoutNormalizer — Whitespace + Markers + Bullets

```python
import re
from app.schemas.preprocessing import SectionMetadata


class LayoutNormalizer:
    """Normalizes layout: preserves paragraph breaks, adds section markers, collapses inline space."""

    BULLET_PATTERN = re.compile(r"^[\s]*[•\-\*→>]\s*")
    PARAGRAPH_BREAK = re.compile(r"\n{2,}")

    @staticmethod
    def normalize(text: str, sections: list[SectionMetadata] | None = None) -> str:
        # 1. Normalize paragraph breaks
        text = LayoutNormalizer.PARAGRAPH_BREAK.sub("\n\n", text)
        # 2. Normalize bullet points to standard "- "
        text = LayoutNormalizer.BULLET_PATTERN.sub("- ", text)
        # 3. Collapse inline whitespace within lines
        lines = text.split("\n")
        cleaned = []
        for line in lines:
            if line.strip() == "":
                cleaned.append("")
            else:
                cleaned.append(re.sub(r"[ \t]+", " ", line.strip()))
        text = "\n".join(cleaned)
        # 4. Add section boundary markers
        if sections:
            lines = text.split("\n")
            # Insert markers in reverse to preserve line indices
            for section in sorted(sections, key=lambda s: s.start_line, reverse=True):
                marker = f"[SECTION: {section.name.upper()}]"
                insert_at = min(section.start_line, len(lines))
                lines.insert(insert_at, marker)
            text = "\n".join(lines)
        return text
```

### Pattern 5: PreprocessingPipeline Orchestrator

```python
import logging
from app.schemas.preprocessing import PipelineResult
from app.services.section_detector import SectionDetector
from app.services.noise_filter import NoiseFilter
from app.services.layout_normalizer import LayoutNormalizer

logger = logging.getLogger(__name__)


class PreprocessingPipeline:
    """Three-stage preprocessing pipeline orchestrated as an injectable service."""

    def __init__(
        self,
        section_detector: SectionDetector | None = None,
        noise_filter: NoiseFilter | None = None,
        layout_normalizer: LayoutNormalizer | None = None,
    ):
        self._section_detector = section_detector or SectionDetector()
        self._noise_filter = noise_filter or NoiseFilter()
        self._layout_normalizer = layout_normalizer or LayoutNormalizer()

    def process(self, text: str) -> PipelineResult:
        prompt_version: str | None = None
        sections = []

        result = self._section_detector.detect(text)
        if result is None:
            logger.info("Detection skipped — passing raw text through")
            return PipelineResult(text=text)

        prompt_version = "section-detection/v1.0.0"

        # Stage 1: Remove noise (operates on original line indices)
        if result.noise_regions:
            text = self._noise_filter.filter(text, result.noise_regions)

        # Stage 2: Normalize layout
        if result.sections:
            sections = result.sections
            text = self._layout_normalizer.normalize(text, sections)
        else:
            text = self._layout_normalizer.normalize(text)

        return PipelineResult(
            text=text,
            sections=sections,
            prompt_version=prompt_version,
        )


# Module-level singleton (matching cv_processor, ocr_service pattern)
preprocessing_pipeline = PreprocessingPipeline()
```

### Anti-Patterns to Avoid

- **Reusing `extract_fields()` for detection:** The existing extraction function bakes in two-phase retry (primary → fallback schema) and extraction-specific error handling. Section detection has a different schema shape and retry needs. Make a direct genai call instead (like `is_document_legible()` does).
- **Mutating text in SectionDetector:** SectionDetector should only return boundary metadata. Text transformation belongs in NoiseFilter and LayoutNormalizer.
- **Off-by-one in line indexing:** NoiseFilter removes lines, shifting indices for subsequent stages. NoiseFilter must run before LayoutNormalizer, and indices from SectionDetector refer to the original text — NoiseFilter applies them before any line count changes.
- **Making pipeline stateful:** Each `process()` call is independent. Avoid caching text between calls — the pipeline should be stateless for thread safety.
- **Passing raw text to the Jinja2 renderer via PromptResolver:** The detection prompt YAML uses `{{ document_text }}`. Ensure proper escaping — the OCR text may contain special characters. Use Jinja2's `e` filter or raw string interpolation if needed.

## Pitfalls

### Pitfall 1: Line-Number Alignment Between Stages

**What goes wrong:** SectionDetector returns line indices based on the original text. NoiseFilter removes lines (e.g., lines 5-7 are a header). After removal, the line count changes, making the original section indices invalid for LayoutNormalizer.

**Why it happens:** Line indices are positional (absolute), not semantic (relative to content). Any line-removal stage shifts all subsequent indices.

**How to avoid:** Run NoiseFilter BEFORE LayoutNormalizer. More importantly, LayoutNormalizer receives section metadata BUT uses it only to insert markers at approximate positions — it should use the ORIGINAL indices from SectionDetector (computed before NoiseFilter ran) and map them through a line-offset tracking mechanism, OR accept that markers are approximate. The simplest approach: LayoutNormalizer inserts markers based on section indices from the ORIGINAL (pre-noise-filter) text, then NoiseFilter removes noise lines (which are short headers/page numbers unlikely to span section boundaries). Section markers referencing shifted positions degrade gracefully — they end up a few lines off, which downstream extraction can tolerate.

**Warning signs:** Section markers appearing in the middle of a paragraph, or section markers referencing content outside the section.

### Pitfall 2: LLM Ambiguity in Boundary Detection

**What goes wrong:** Gemini returns inconsistent or overlapping section boundaries — e.g., "Experience" starts at line 20 and "Experience" also ends at line 50 with another section overlapping the same range. Or it returns sections the document doesn't have (e.g., "Languages" for a CV with no language section).

**Why it happens:** LLM outputs are non-deterministic. Documents vary widely in formatting. The prompt may overfit to a specific document structure.

**How to avoid:** Post-process the LLM output:
- Clamp `start_line` and `end_line` to valid range `[0, num_lines)`
- Reject sections where `start_line >= end_line`
- Deduplicate overlapping sections (prefer the one with higher confidence or first occurrence)
- Deduplicate by name — keep the first section with a given name
- If LLM returns empty sections and empty noise_regions, treat as "no clear boundaries found" and skip preprocessing per D-03

**Warning signs:** Sections array contains `start_line` values outside document line count, negative line numbers, or section names that don't match known patterns.

### Pitfall 3: Whitespace Normalization Edge Cases

**What goes wrong:** Collapsing all whitespace destroys meaningful structure — code snippets, bullet intent, table alignment. Aggressive `\s+` → `" "` regex loses paragraph structure.

**Why it happens:** CV text has varying whitespace semantics: inline multiple spaces (bad OCR), paragraph separation (double newlines), bullet indentation (tabs/spaces at line start), table column alignment.

**How to avoid:** Use a tiered approach:
1. First normalize paragraph breaks: `\n{3,}` → `\n\n` (any triple+ newlines become a single paragraph break)
2. THEN collapse inline whitespace: within a line, replace `[ \t]+` with a single space, but ONLY after trimming leading/trailing whitespace per line
3. Do NOT collapse all `\s+` globally — this would merge paragraphs
4. Bullet normalization: detect `•`, `-`, `*`, `→` at line start and replace with consistent `- ` marker

**Warning signs:** Entire document becomes one line, or single newlines within a paragraph are preserved while paragraph breaks are lost.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (already available, in `requirements.txt`) |
| Config file | `backend/pytest.ini` or `backend/pyproject.toml` |
| Quick run command | `pytest backend/tests/test_section_detector.py -x` |
| Stage suite command | `pytest backend/tests/ -k "test_section" -x` |
| Full suite command | `pytest backend/tests/ -x` |
| Watch mode | NOT supported — `pytest-watch` is not installed and not in `requirements.txt` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | File |
|--------|----------|-----------|------|
| PREP-01 | SectionDetector returns DetectionResult with sections for a well-structured CV | unit | `test_section_detector.py` |
| PREP-01 | SectionDetector returns None when LLM cannot identify boundaries | unit | `test_section_detector.py` |
| PREP-01 | SectionDetector handles empty text gracefully | unit | `test_section_detector.py` |
| PREP-01 | LayoutNormalizer adds section markers at correct positions | unit | `test_layout_normalizer.py` |
| PREP-01 | LayoutNormalizer preserves paragraph breaks (double newlines) | unit | `test_layout_normalizer.py` |
| PREP-01 | LayoutNormalizer collapses inline whitespace within lines | unit | `test_layout_normalizer.py` |
| PREP-01 | LayoutNormalizer normalizes bullet markers (•, *, → → -) | unit | `test_layout_normalizer.py` |
| PREP-01 | LayoutNormalizer handles empty sections list | unit | `test_layout_normalizer.py` |
| PREP-02 | NoiseFilter removes specified line ranges | unit | `test_noise_filter.py` |
| PREP-02 | NoiseFilter handles overlapping noise regions | unit | `test_noise_filter.py` |
| PREP-02 | NoiseFilter returns text unchanged for empty noise_regions | unit | `test_noise_filter.py` |
| PREP-02 | NoiseFilter handles out-of-bounds line indices | unit | `test_noise_filter.py` |
| PREP-01/PREP-02 | Pipeline runs all three stages end-to-end | integration | `test_preprocessor_pipeline.py` |
| PREP-01/PREP-02 | Pipeline returns raw text when detection fails | integration | `test_preprocessor_pipeline.py` |
| PREP-01/PREP-02 | Pipeline metadata includes sections and prompt_version | integration | `test_preprocessor_pipeline.py` |
| — | Preprocessing Pydantic schemas validate correctly | unit | `test_preprocessing_schemas.py` |
| — | Preprocessing schemas reject invalid data | unit | `test_preprocessing_schemas.py` |

### Sampling Rate

- **Per stage commit:** `pytest backend/tests/test_section_detector.py -x`
- **Per wave merge:** `pytest backend/tests/ -k "preprocessing" -x`
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps

- [ ] `backend/app/schemas/preprocessing.py` — SectionMetadata, NoiseRegion, DetectionResult, PipelineResult
- [ ] `backend/app/services/section_detector.py` — SectionDetector class
- [ ] `backend/app/services/noise_filter.py` — NoiseFilter class
- [ ] `backend/app/services/layout_normalizer.py` — LayoutNormalizer class
- [ ] `backend/app/services/preprocessor.py` — PreprocessingPipeline orchestrator
- [ ] `backend/prompts/section-detection/v1.0.0.yaml` — Detection prompt YAML via PromptResolver
- [ ] `backend/tests/test_preprocessing_schemas.py`
- [ ] `backend/tests/test_section_detector.py`
- [ ] `backend/tests/test_noise_filter.py`
- [ ] `backend/tests/test_layout_normalizer.py`
- [ ] `backend/tests/test_preprocessor_pipeline.py`

### Integration Points with Existing Tests

The existing `backend/tests/test_preprocessor.py` (10 tests for current regex-based `preprocess_cv_text()`) must continue to pass. The new pipeline does NOT replace `preprocess_cv_text()` — it runs alongside it (the pipeline is injected into the extraction flow, not replacing the inline call). The existing tests validate the regex fallback path; the new tests validate the LLM-guided pipeline path.

## Key Files

| File | Role | New/Existing |
|------|------|--------------|
| `backend/app/schemas/preprocessing.py` | Pydantic models for pipeline data flow | NEW |
| `backend/app/services/section_detector.py` | LLM-guided section+noise detection (batched Gemini call) | NEW |
| `backend/app/services/noise_filter.py` | Line-index-based noise region removal | NEW |
| `backend/app/services/layout_normalizer.py` | Whitespace normalization + section markers + bullet standardization | NEW |
| `backend/app/services/preprocessor.py` | PreprocessingPipeline orchestrator — injectable service | MODIFIED |
| `backend/app/core/config.py` | Add `gemini_model_detection` setting for detection call model | MODIFIED |
| `backend/prompts/section-detection/v1.0.0.yaml` | Versioned detection prompt YAML loaded via PromptResolver | NEW |
| `backend/tests/test_preprocessing_schemas.py` | Schema validation tests | NEW |
| `backend/tests/test_section_detector.py` | SectionDetector unit tests (mocked LLM) | NEW |
| `backend/tests/test_noise_filter.py` | NoiseFilter unit tests | NEW |
| `backend/tests/test_layout_normalizer.py` | LayoutNormalizer unit tests | NEW |
| `backend/tests/test_preprocessor_pipeline.py` | Pipeline integration tests | NEW |

## Open Questions (RESOLVED)

### Q1: "When will llm_service.py be created?" → RESOLVED

**Question:** `llm_service.py` already exists. Will the SectionDetector use `extract_fields()` from it, or call the SDK directly?

**Resolution:** SectionDetector calls the Google GenAI SDK directly, NOT through `llm_service.py`. The existing `extract_fields()` is tightly coupled to extraction semantics (two-phase retry with primary/fallback schemas, fixed JSON schema shape). Section detection has a different schema (boundary metadata, not field values) and its own retry semantics. Making direct SDK calls follows the pattern already established by `llm_service.py:is_document_legible()` which also makes a direct call. The google-genai client lazy-init pattern (`_client = None; if None: _client = Client(...)`) should be reused.

### Q2: "Should the section-detection prompt be a new YAML or hardcoded?" → RESOLVED

**Question:** The section detection prompt could be a hardcoded string in `section_detector.py` or a versioned YAML file loaded via PromptResolver from Phase 9.

**Resolution:** Full YAML prompt under `backend/prompts/section-detection/v1.0.0.yaml`, loaded via `PromptResolver.get("section-detection", "^v1.0.0")`. This provides traceability (Git tags), versioning, and decouples prompt changes from code changes. The YAML follows the same structure as `cv-extraction/v1.0.0.yaml` (type, version, description, system_prompt, schema, model_params, tags) but the `schema` field defines the boundary detection output schema rather than the extraction output schema. The `PromptResolver.render()` or manual Jinja2 rendering replaces `{{ document_text }}` at call time.

### Q3: "Pipeline injection pattern — singleton or DI?" → RESOLVED

**Question:** Should `PreprocessingPipeline` be a module-level singleton (matching `cv_processor = CVProcessor()`, `ocr_service`, etc.) or always dependency-injected?

**Resolution:** Module-level singleton for production use, with constructor injection for tests. The class `PreprocessingPipeline` accepts optional stage instances in its constructor (`SectionDetector | None`, `NoiseFilter | None`, etc.), defaulting to real implementations. This allows tests to inject mocked/configured stages while production uses the module-level `preprocessing_pipeline = PreprocessingPipeline()`. This matches the existing pattern: `CVProcessor.__init__()` accepts `matricula_csv` for testability, while `cv_processor = CVProcessor()` is the module-level singleton.

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V5 Input Validation | yes | Pydantic models validate detection JSON before use; prompt YAMLs use `yaml.safe_load()` via PromptResolver |
| V7 Error Handling | yes | LLM failure returns None (graceful degradation), not an exception cascade |

### Known Threat Patterns

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| LLM prompt injection via document text | Tampering | Document text is truncated to 4000-6000 tokens before pipeline input (existing behavior in `preprocess_cv_text`). Detection prompt instructs Gemini to return structured JSON only. The document text appears as a data variable in the Jinja2 template, not as executable prompt code. |
| Malformed detection JSON causing crashes | Tampering | Pydantic `DetectionResult` validation rejects malformed responses. Unexpected shapes return None from `SectionDetector.detect()`, and the pipeline passes raw text through. |

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Regex-only preprocessing (`preprocessor.py` SECTIONS dict) | LLM-guided section + noise detection with regex fallback | This phase | Regex still exists for fallback in `preprocess_cv_text()`. New pipeline adds LLM-guided detection as the primary path. |
| Single `preprocess_cv_text()` function | Multi-stage pipeline with distinct stage classes | This phase | Better separation of concerns, easier to test, simpler to evolve individual stages. |
| Hardcoded extraction prompts | Versioned prompt YAMLs via PromptResolver | Phase 9 | Detection prompt benefits from same infrastructure: Git tagging, semver, Jinja2 rendering. |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Gemini can reliably detect section boundaries in Spanish CV text | Architecture | MEDIUM — well-structured CVs with standard headers (Educación, Experiencia, etc.) should work; non-standard or scanned documents may fail. If detection fails, raw text passes through per D-03. |
| A2 | Noise regions (headers, page numbers) are consistently on distinct lines | Pitfalls | LOW — headers and footers appear on separate lines by nature. Page numbers are typically standalone. Even if a noise region overlaps content, losing a few lines is tolerable. |
| A3 | Line indices from LLM detection are 0-based | Architecture | MEDIUM — LLM output format must specify 0-based indexing. The prompt YAML must explicitly define the convention. Mismatch would shift all boundaries by 1. |
| A4 | Section markers inserted by LayoutNormalizer do not confuse downstream extraction | Architecture | LOW — extraction LLM receives `[SECTION: EDUCATION]` markers as hints. The extraction prompt should be updated (Phase 13) to recognize these markers. |
| A5 | The `google-genai` SDK's `generate_content` pattern is stable across versions | SectionDetector | LOW — SDK is already in active use in `llm_service.py`. The same API surface is used. |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.12 | All code | ✓ | 3.12.3 | — |
| google-genai | SectionDetector (LLM calls) | ✓ | 1.x | — |
| PyYAML | PromptResolver (prompt loading) | ✓ (Phase 9) | 6.0.3 | — |
| Jinja2 | PromptResolver (template render) | ✓ (Phase 9) | 3.1.6 | — |
| Pydantic v2 | Schema models | ✓ (Phase 9) | 2.x | — |
| pytest | Test framework | ✓ | 8.x | — |
| ruff | Linting | ✓ (if installed) | — | — |

**Missing dependencies with no fallback:** None — all libraries already in project.

## Sources

### Primary (HIGH confidence)

- Existing code: `backend/app/services/llm_service.py` — google-genai SDK call pattern, TPM tracking, `_get_client()` lazy-init, `is_document_legible()` direct call pattern
- Existing code: `backend/app/services/preprocessor.py` — current regex-based preprocessing, `clean_text()`, `SECTIONS` dict
- Existing code: `backend/app/services/cv_processor.py` — module-level singleton pattern (`cv_processor = CVProcessor()`)
- Existing code: `backend/app/services/cv_extractor.py` — preprocessor integration point (`preprocess_cv_text(raw_text)` before LLM extraction)
- Phase 9 RESEARCH.md — PromptResolver, prompt YAML structure, Jinja2 patterns, validation architecture template
- Phase 10 CONTEXT.md — D-01 through D-12 decisions, integration points, agent discretion items
- Phase 10 DISCUSSION-LOG.md — alternatives considered, rationale for batched detection, multi-stage pipeline, singleton pattern
- `.planning/ROADMAP.md` — Phase 10 plans structured as 3 plans (schemas+YAML, stages+tests, pipeline+integration)
- `.planning/REQUIREMENTS.md` — PREP-01 and PREP-02 requirement text
- `.planning/codebase/CONVENTIONS.md` — Backend naming (snake_case), module-level singletons, pytest fixtures, ruff linting
- `backend/app/schemas/prompt.py` — PromptVersion Pydantic model with validation patterns
- `backend/app/schemas/extraction.py` — ExtractionRequest/ExtractionResult Pydantic model patterns
- `backend/app/core/config.py` — Settings model with `gemini_model_*` fields
- `AGENTS.md` — Project conventions, backend architecture, service patterns

### Secondary (MEDIUM confidence)

- Google GenAI SDK documentation — `generate_content` API surface, `response_mime_type` config
- Pydantic v2 `Field` constraints for float range validation (`ge=0.0, le=1.0`)

### Tertiary (LOW confidence)

- None — all technical claims verified against existing codebase patterns

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries already installed and verified in project venv
- Architecture: HIGH — patterns directly match existing codebase conventions (singletons, Pydantic schemas, direct SDK calls)
- Pitfalls: MEDIUM — line-index shifting between stages is a known problem but the specific impact depends on actual CV structure

**Research date:** 2026-05-21
**Valid until:** 2026-06-21 (30 days — all libraries are stable, no expected version changes)
