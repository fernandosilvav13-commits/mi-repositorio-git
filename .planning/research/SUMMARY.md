# Research Summary: v1.4 Extracción Inteligente

**Project:** CicloAI
**Date:** 2026-05-19
**Confidence:** HIGH

---

## Key Findings

### 1. Schema descriptions are the #1 missed optimization
Google explicitly recommends using `description` fields in `response_schema` — the current code has empty descriptions on every property. **Zero code changes, highest ROI.**

### 2. Two-pass pipeline (classify → extract) is the dominant IDP architecture
AWS, Google, and Microsoft all use this pattern. Classify document type first, then extract with type-specific schema and prompt. Enables better accuracy but doubles LLM calls.

### 3. One-shot prompting beats zero-shot consistently
2025 peer-reviewed research shows Gemini 2.5 Pro with 1-shot consistently achieves highest accuracy across tested LLMs.

### 4. OCR quality is about layout + fusion, not engine replacement
PaddleOCR 3.0 PP-StructureV3's layout analysis (reading order recovery) matters as much as character accuracy. Run Tesseract + PaddleOCR in parallel with confidence-based fusion.

### 5. Post-processing rules need a registry pattern
Expand beyond gender/phone/RUT with decorator-registered rule modules (declared dependencies, priority ordering). Each rule independently testable. **Highest-risk feature** — field suitability triage is critical.

---

## Stack Recommendations

| Addition | Version | Purpose | Priority |
|----------|---------|---------|----------|
| PaddleOCR 3.0 | 3.0+ | OCR for scanned/image PDFs (94.5% score) | Phase 5 |
| spaCy + EntityRuler | 3.8+ | Token-pattern matching for post-processing rules | Phase 4 |
| scikit-learn | 1.6+ | TF-IDF + SVM document classifier | Phase 3 |
| Promptfoo | latest | Prompt optimization with regression harness | Phase 1 |

**What NOT to add:** json-repair, BERT/transformers, cloud OCR APIs, Redis

---

## Feature Priority

| Priority | Feature | Effort | Risk |
|----------|---------|--------|------|
| P0 | Schema description optimization | 1-2h | Very low |
| P0 | Prompt restructuring (Task/Format/Constraints) | 1h | Very low |
| P1 | Prompt versioning scaffolding | 4h | Low |
| P1 | Document classifier (keyword + TF-IDF) | 2-3d | Medium |
| P1 | Two-pass pipeline wiring | 1d | Medium |
| P1 | Post-processing rule registry | 2-3d | High |
| P2 | PaddleOCR integration | 3-5d | Medium |
| P2 | LLM classifier tier | 2-3d | Medium |

---

## Architecture Overview

```
Before: preprocessor → extract (LLM) → post_process (3 rules)
After:  preprocessor → advanced_preprocessor → classifier → extract (type-specific prompt) → post_process (rule registry)
```

Key components:
- **`advanced_preprocessor.py`** — New module, structural cleanup, optional stage
- **`classifier_service.py`** — Three-tier: keywords → TF-IDF → LLM fallback
- **`prompts/`** — Versioned YAML prompt files with registry
- **`rules/`** — Decorator-registered rules with dependency DAG
- **`ocr_service.py`** — Enhanced with PaddleOCR dual-engine fusion

---

## Critical Pitfalls

1. **OCR over-processing** strips Spanish diacritics — per-step CER testing required
2. **Prompt over-optimization** on small samples creates brittle extraction — regression harness needed
3. **Classifier errors are systemic** — harder documents fail at both classification AND extraction
4. **Post-processing false positives** — only apply rules to pattern-based fields (not semantic)
5. **Error propagation** without trace IDs makes debugging impossible — structured logging with trace IDs
6. **Cache invalidation** — include prompt version hash in cache key

---

## Recommended Phase Order

| Phase | Name | Dependencies | Risk |
|-------|------|-------------|------|
| 1 | Prompt Infrastructure & Foundation | None | Low |
| 2 | Schema Descriptions & Prompt Refinement | Phase 1 | Very low |
| 3 | Document Classification | Phase 2 | Medium |
| 4 | Post-Processing Rules Expansion | Phase 1 | High |
| 5 | OCR Augmentation | None (parallel) | Medium |
| 6 | Field-Level Confidence (v1.5 stretch) | Phase 4 | Medium |

---

## Open Questions

- How many CV uploads happen daily? (determines if PaddleOCR latency is acceptable)
- What's the current breakdown of PDF types? (scanned vs digital — affects OCR strategy ROI)
- Is there an existing set of labeled CVs for classifier training?
- What non-CV document types are being uploaded? (determines classifier category scope)
- What's the current per-document extraction latency baseline?
