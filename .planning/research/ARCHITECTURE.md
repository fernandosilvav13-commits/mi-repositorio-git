# Architecture Research: v1.4 Extracción Inteligente

## Current Pipeline (Before)

```
raw_text → preprocessor.py → cv_extractor.py (llm_service.py) → cv_processor.py → output
                                  ↑                              ↑
                              EXTRACTION_SCHEMA             _post_process()
                              or dynamic schema             (gender, phone, RUT only)
```

## Proposed Pipeline (After)

```
raw_text → preprocessor.py → advanced_preprocessor.py (NEW) → classifier_service.py (NEW)
                                                                    ↓
                                                            document_type
                                                                    ↓
                              ┌───────────────────────────────────┘
                              ↓
                    cv_extractor.py (with type-specific prompt)
                              ↓
                    cv_processor.py (with rule registry)
                              ↓
                         output + provenance
```

## Component Architecture

### 1. Advanced Preprocessor (`advanced_preprocessor.py`)
- **New module**, parallel to existing `preprocessor.py`, NOT a modification
- Optional pipeline stage: structural cleanup, section detection, noise filtering
- Called after basic preprocessor, before classifier
- Configurable via feature flags

### 2. Document Classifier (`classifier_service.py`)
- **Three-tier approach:**
  1. **Keyword tier** (~50ms) — Fast keyword matching for obvious document types
  2. **TF-IDF + SVM tier** (~100ms) — scikit-learn model for ambiguous cases
  3. **LLM tier** (fallback only) — Gemini call when both above are uncertain
- Called AFTER preprocessing, BEFORE LLM extraction
- Returns: `document_type` + `confidence` + `classification_method`
- Training: 200-500 labeled CV examples needed for TF-IDF model

### 3. Prompt Version System (`prompts/`)
- **File-based:** YAML files in `prompts/versions/` directory
- **Registry:** `registry.yaml` maps document_type → active prompt version
- **Resolver:** `prompt_version_resolver.py` loads active prompt by type
- **Git-tracked:** Prompt changes are code changes (reviewable, revertable)
- No external tooling at current scale

### 4. Rule Registry for Post-Processing (`rules/`)
- **Pattern:** Decorator-registered rule modules with declared dependencies
- Each rule: `@rule(name="gender", depends_on=["NOMBRES"], priority=10)`
- Priority ordering: higher priority runs first
- Dependencies: rule only runs if its dependency fields exist
- Simple standalone rules keep using `cv_processor._post_process()`
- Complex multi-field rules move to `rules/` module

### 5. OCR Augmentation (`ocr_service.py`)
- **Augment, not replace:** Run Tesseract + PaddleOCR in parallel for scanned PDFs
- **Fusion:** Per-line confidence scoring, pick highest-confidence result per line
- **Layout analysis:** PaddleOCR PP-StructureV3 recovers reading order
- **Fallback:** Tesseract for clean text-based PDFs (faster, no GPU needed)
- Feature-gated: Existing OCR path unchanged until PaddleOCR verified

## Data Flow

```
1. raw_text → preprocessor.clean_text()          (existing)
2. clean_text → advanced_preprocessor.enhance()   (NEW — structural cleanup)
3. enhanced_text → classifier.classify()           (NEW — returns doc_type)
4. enhanced_text + doc_type → extract_fields()     (modified — type-specific prompt)
5. extracted_data → post_process()                 (extended — rule registry)
6. post_processed → output                         (existing — with provenance tags)
```

## Integration Points

| Component | Existing File | Change |
|-----------|--------------|--------|
| Advanced preprocessor | `backend/app/services/preprocessor.py` | New file parallel to existing |
| Classifier service | `backend/app/services/cv_extractor.py` | New file, called before extraction |
| Prompt versioning | `backend/app/services/llm_service.py` | New prompts/ directory, resolver |
| Rule registry | `backend/app/services/cv_processor.py` | New rules/ module, called from _post_process |
| OCR augmentation | `backend/app/services/ocr_service.py` | Add PaddleOCR as alternative backend |

## Build Order (Dependency-Aware)

1. **Phase 1: Prompt scaffolding** — Prompts directory, registry, resolver. Non-invasive, enables everything else.
2. **Phase 2: Advanced preprocessing** — New module, integrates cleanly, improves text quality for all downstream steps.
3. **Phase 3: Document classification** — Keyword tier first, then TF-IDF. Enables two-pass pipeline.
4. **Phase 4: Post-processing rules** — Rule registry pattern. Can proceed in parallel with Phase 2-3.
5. **Phase 5: Two-pass pipeline** — Wire classifier output into extraction with type-specific prompts.
6. **Phase 6 (optional): OCR augmentation** — PaddleOCR integration. Independent of other changes.
