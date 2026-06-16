# Milestones

## v1.4 Extracción Inteligente (Shipped: 2026-06-16)

**Phases completed:** 7 phases (9–15), 20 plans

**Key accomplishments:**

- Phase 9: Version-controlled prompt registry with PromptVersion model, YAML baseline, and PromptResolver with semver range matching, Jinja2 templates, and git tag integration
- Phase 10: Advanced preprocessing pipeline — SectionDetector (LLM-guided), NoiseFilter, LayoutNormalizer, and PreprocessingPipeline orchestrator (43 tests)
- Phase 11: Document classification — binary CV vs Non-CV with LinearSVC + TF-IDF, 0.7 confidence threshold, synthetic training data, API endpoint (27 tests)
- Phase 12: Post-processing rules expansion — 5 inference rules (nationality, DOB, experience, education, email), shadow mode with auto-activation at precision >= 0.9 (52 tests)
- Phase 13: Two-pass pipeline — ExtractionPipeline chaining preprocess → classify → type-specific extraction with PromptResolver prompts
- Phase 14: OCR augmentation — Tesseract 5.3.4 local install, pytesseract integration, LayoutAnalyzer with coordinate-based column detection via KMeans, OCRService with fallback chain (11 tests)
- Phase 15: Gap closure — registered /api/classify router in main.py, activated two-pass pipeline by default (use_two_pass=True), fixed PromptResolver path

**Known deferred items at close:** 3 (OCR-01 PaddleOCR 3.0, OCR-02 fusion, OCR-03 PP-StructureV3 layout — see STATE.md Deferred Items)

---

## v1.3 Bugfix Pipeline de Extracción (Shipped: 2026-05-19)

**Phases completed:** 3 phases (6–8), 3 plans, 3 tasks

**Key accomplishments:**

- Phase 6: Preprocessor proper noun casing fix — clean_text() uses IGNORECASE re.sub() instead of blanket .lower()
- Phase 7: Post-processing pipeline — gender inference, phone normalization, RUT formatting (only overrides "NO ENCONTRADO")
- Phase 8: LLM error resilience — JSON repair (fences, trailing commas, single quotes), two-phase retry (dynamic schema → EXTRACTION_SCHEMA fallback), TPM-aware bounded backoff, structured logging

---

## v1.2 Wizard Reordering (Shipped: 2026-05-17)

**Phases completed:** 1 phases, 1 plans, 0 tasks

**Key accomplishments:**

- (none recorded)

---

## v1.0 MVP (Shipped: 2026-05-15)

**Phases completed:** 1 phases, 4 plans, 12 tasks

**Key accomplishments:**

- Foundational Apple Design System established with Tailwind v4 theme and a persistent, frosted dual-navigation shell.
- Modular Apple-spec layout components (Tile, ProductCard, FrostedContainer) implemented with Tailwind v4.
- Extraction results view transformed into a high-end "Museum Gallery" using Apple-spec layout primitives and artifact-centric data mapping.
- Wizard flow overhauled as a "Product Configurator" using Apple's white utility cards and pill chip controls, creating a high-end setup experience.

---
