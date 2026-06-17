# CicloAI

## Current State

**Shipped:** v1.4 Extracción Inteligente (2026-06-16)
**Active:** v1.5 Consolidación de Extracción (started 2026-06-17)

v1.4 dramatically improved extraction accuracy through: version-controlled prompt infrastructure with PromptResolver, advanced preprocessing pipeline (SectionDetector, NoiseFilter, LayoutNormalizer), document classification (TF-IDF + SVM), 5 new post-processing inference rules in shadow mode, two-pass pipeline (classify → type-specific extraction), OCR augmentation with Tesseract + layout analysis, and gap closure wiring the classify router into production. 7 phases, 20 plans, 184+ tests.

v1.5 picks up from Phase 16 (llm-provider) — a multi-provider LLM abstraction (Anthropic, OpenAI, Gemini with auto-detection) that was implemented but never UAT-tested or committed. The milestone stabilizes the extraction pipeline: UAT signoff, deduplication of batch_process.py, config cleanup, real-CV validation, and post-processing refinement.

## Current Milestone: v1.5 Consolidación de Extracción (Active)

**Goal:** Cerrar Phase 16 (llm-provider), consolidar el pipeline de extracción eliminando duplicación y config legacy, validar con documentos reales, y refinar post-procesamiento.

**Target features:**
- ✅ Phase 16 (llm-provider) — code complete (provider abstraction, bugfixes, model resolution)
- ⏳ Phase 17: UAT execution + commit of Phase 16
- ⏳ Phase 18: Deduplicate batch_process.py extraction logic
- ⏳ Phase 19: Config orphans cleanup (remove gemini_model_* legacy vars)
- ⏳ Phase 20: End-to-end validation with real CV documents
- ⏳ Phase 21: Post-processing refinement (gender, phone, RUT, shadow rules)

## What This Is

A CV data extraction system with Apple-inspired frontend design, multi-step ingestion wizard, and Excel export. Extracts structured data from CVs using AI (Gemini), applies conditional rules, and exports to formatted Excel files.

## Core Value

Extract structured CV data with a beautiful, intuitive interface and export-ready results.

## Requirements

### Validated

- ✓ Cross-reference data from external files (PDF/CSV/PPT/DOCX) — Phase 04
- ✓ Apple Color System (Action Blue, Parchment, Near-Black) — v1.0
- ✓ SF Pro / Inter Typographic Hierarchy — v1.0
- ✓ Full-Bleed Tile Layout components — v1.0
- ✓ Global Nav and Frosted Sub-Nav — v1.0
- ✓ Wizard flow as a Product Configurator — v1.0
- ✓ Extraction Results as a Museum Gallery — v1.0
- ✓ Wizard steps reordered: Upload → Template → CrossRef → Rules → Extract → Export → Review — v1.2
- ✓ Warning guard on template change with crossref mapping (D-01/D-03) — v1.2
- ✓ Post-processing pipeline (gender, phone, RUT) — Phase 7 (v1.3)
- ✓ Preprocessor proper noun casing fix — Phase 6 (v1.3)
- ✓ LLM JSON error resilience with schema fallback — Phase 8 (v1.3)
- ✓ TPM-aware bounded retries — Phase 8 (v1.3)
- ✓ Version-controlled prompt registry with PromptResolver — v1.4
- ✓ Advanced preprocessing (SectionDetector, NoiseFilter, LayoutNormalizer) — v1.4
- ✓ Document classification (TF-IDF + SVM, 0.7 confidence threshold) — v1.4
- ✓ 5 inference rules (nationality, DOB, experience, education, email) in shadow mode — v1.4
- ✓ Two-pass pipeline (classify → type-specific extraction) — v1.4
- ✓ OCR augmentation (Tesseract + layout analysis, fallback chain) — v1.4

### Active (v1.5)

- UAT signoff for Phase 16 (llm-provider): provider auto-detection, factory, section detector, model resolution
- Deduplicate extraction logic in batch_process.py — reuse llm_service.extract_fields()
- Remove legacy config orphans (gemini_model_*, unused llm_provider field)
- End-to-end validation with 5+ real CV documents through the wizard
- Improve post-processing precision: gender inference, phone normalization, RUT formatting, shadow rules (nationality, DOB, experience, education, email)

### Deferred (post-v1.5)

- PaddleOCR 3.0 integration (OCR-01)
- Tesseract + PaddleOCR fusion (OCR-02)
- PP-StructureV3 layout analysis (OCR-03)
- Field-level confidence scoring UI

### Out of Scope

- Mobile app — web-first PWA approach
- Real-time collaboration — single-user workflow

## Context

Shipped v1.0–v1.2 with ~42,654 LOC (TSX/TS/CSS/Python).
Tech stack: Next.js 16, FastAPI, Supabase, Tailwind v4, Gemini AI.
Frontend redesigned with Apple "museum gallery" design language.
v1.2: Wizard steps reordered, template-before-crossref with guard on crossref mapping loss.

## Key Decisions

| Decision | Outcome | Status |
| -------- | ------- | ------ |
| Tuple-based composite keys for matching | O(1) matching performance with multiple columns | ✓ Good |
| pytest for backend testing | Better async support and cleaner syntax | ✓ Good |
| Apple Design System with Tailwind v4 | Consistent, elegant UI | ✓ Good |
| Dual-navigation shell (44px + 52px) | Clear information hierarchy | ✓ Good |
| Museum Gallery artifact presentation | Intuitive data visualization | ✓ Good |
| Pill-shaped buttons and pill chips | Cohesive Apple aesthetic | ✓ Good |
| D-01: Warning on template change | Prevents accidental crossref mapping loss | ✓ Good |
| D-02: Same-template auto-advance | Faster flow when re-selecting same template | ✓ Good |
| D-03: Clear mapping on template switch | Prevents ghost state in crossref step | ✓ Good |

## Constraints

- All new UI components must follow Apple design tokens in `globals.css`
- RUT consolidation occurs server-side during export, not in Supabase
- Single-command launch via `./start.sh`

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-06-17 — v1.5 Consolidación de Extracción started*
