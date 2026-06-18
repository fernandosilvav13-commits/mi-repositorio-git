# CicloAI

## Current State

**Shipped:** v1.5 Consolidación de Extracción (2026-06-18)
**Active:** v1.6 (planning)

v1.4 dramatically improved extraction accuracy through: version-controlled prompt infrastructure with PromptResolver, advanced preprocessing pipeline (SectionDetector, NoiseFilter, LayoutNormalizer), document classification (TF-IDF + SVM), 5 new post-processing inference rules in shadow mode, two-pass pipeline (classify → type-specific extraction), OCR augmentation with Tesseract + layout analysis, and gap closure wiring the classify router into production. 7 phases, 20 plans, 184+ tests.

v1.5 stabilized the extraction pipeline: multi-provider LLM abstraction (Anthropic, OpenAI, Gemini) with full UAT signoff, deduplication of batch_process.py, config orphans cleanup, real-CV validation (6 CVs, 4 bugs fixed), post-processing refinement (gender, phone, RUT, shadow rules promotion), and authentication infrastructure (backend auth hardening + frontend login/signup). 7 phases, 269 tests.

## Current Milestone: v1.6 (Planning)

**Goal:** TBD — next milestone starts with requirements definition.

**Candidate areas:**
- Performance optimization (caching, query pagination)
- Deployment/DevOps (Docker, CI/CD)
- Enhanced analytics dashboard
- Multi-tenancy / organization support

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
- ✓ Multi-provider LLM abstraction (Anthropic, OpenAI, Gemini) with factory, auto-detection, model resolution — v1.5
- ✓ Deduplicated batch_process.py extraction logic — uses llm_service.extract_fields() — v1.5
- ✓ Config orphans cleanup (gemini_model_*, llm_provider removed) — v1.5
- ✓ Real-CV validation: 6 CVs tested, 4 critical/major bugs fixed — v1.5
- ✓ Gender inference with confidence scoring + 50+ compound name overrides — v1.5
- ✓ Phone normalization (Chilean +56 & international) — v1.5
- ✓ RUT formatting with módulo 11 validation and RUT_VALIDO flag — v1.5
- ✓ 4 shadow rules promoted to active (nationality, DOB, education, email) — v1.5
- ✓ Backend auth hardening: require_auth on rules/export/classify/auth_endpoint — v1.5
- ✓ Frontend auth pages: login, signup, AuthContext, AuthGuard, GlobalNav auth links — v1.5
- ✓ Rate limiting with slowapi (60 req/60s, production only) — v1.5

### Active (v1.6)

_TBD — next milestone requirements to be defined._

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
*Last updated: 2026-06-18 — v1.5 Consolidación de Extracción shipped*
