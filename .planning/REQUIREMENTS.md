# Requirements: CicloAI

**Defined:** 2026-05-19
**Core Value:** Extract structured CV data with a beautiful, intuitive interface and export-ready results.

## v1.4 Requirements

Requirements for v1.4 — Extraccion Inteligente. Each maps to roadmap phases.

### Prompt Infrastructure

- [x] **PROMPT-01**: System supports version-controlled prompt registry with YAML files, resolver, and Git tracking

### Document Classification

- [x] **CLASS-01**: System classifies documents using TF-IDF + SVM (scikit-learn) to detect document type before extraction

### Post-Processing Rules

- [x] **RULES-01**: System expands field coverage with pattern-based inference rules beyond gender/phone/RUT
- [x] **RULES-02**: New post-processing rules deploy in shadow mode with 90% precision floor before activation

### Advanced Preprocessing

- [x] **PREP-01**: System applies structural cleanup (section detection, layout normalization) before extraction
- [x] **PREP-02**: System filters noise (page headers, page numbers, artifacts) before extraction

### OCR Augmentation

- [ ] **OCR-01**: System integrates PaddleOCR 3.0 as alternative OCR backend for image-based documents
- [ ] **OCR-02**: System fuses Tesseract + PaddleOCR results with per-line confidence scoring
- [ ] **OCR-03**: System applies layout analysis (PP-StructureV3) for reading order recovery

### Two-Pass Pipeline

- [x] **PIPE-01**: System wires classifier output into extraction with type-specific prompts

## Out of Scope

| Feature | Reason |
|---------|--------|
| Field-level confidence scoring UI | Deferred to v1.5 — design data model now, implement later |
| Fine-tuned LLM | Prompt engineering + schema optimization sufficient for current needs |
| Cloud OCR APIs | Cost-prohibitive at scale — PaddleOCR self-hosted is sufficient |
| Real-time extraction streaming | Batch extraction is the workflow |
| Mobile app | Web-first PWA approach maintained |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PROMPT-01 | Phase 9 | Complete |
| CLASS-01 | Phase 11 | Complete |
| RULES-01 | Phase 12 | Complete |
| RULES-02 | Phase 12 | Complete |
| PREP-01 | Phase 10 | Complete |
| PREP-02 | Phase 10 | Complete |
| OCR-01 | Phase 14 | Pending |
| OCR-02 | Phase 14 | Pending |
| OCR-03 | Phase 14 | Pending |
| PIPE-01 | Phase 13 | Complete |

**Coverage:**
- v1.4 requirements: 10 total
- Mapped to phases: 10 ✓
- Unmapped: 0

---

*Requirements defined: 2026-05-19*
*Last updated: 2026-06-14 after milestone gap closure*

