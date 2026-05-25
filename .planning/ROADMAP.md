# Roadmap — CicloAI

## Milestones

- ✅ **v1.0 MVP** — Phase 1 (shipped 2026-05-15)
- ✅ **v1.1 Cross-Reference Integration** — Phases 2–4 (shipped 2026-05-15)
- ✅ **v1.2 Wizard Reordering** — Phase 5 (shipped 2026-05-17)
- ✅ **v1.3 Bugfix Pipeline de Extracción** — Phases 6–8 (shipped 2026-05-19)
- 🔄 **v1.4 Extracción Inteligente** — Phases 9–14 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phase 1) — SHIPPED 2026-05-15</summary>

- [x] Phase 1: Frontend Overhaul (Apple Design) (4/4 plans) — completed 2026-05-14
</details>

<details>
<summary>✅ v1.1 Cross-Reference Integration (Phases 2-4) — SHIPPED 2026-05-15</summary>

- [x] Phase 2: Crossref Page Redesign (3/3 plans) — completed 2026-05-15
- [x] Phase 3: Wizard Cross-Reference Integration (3/3 plans) — completed 2026-05-15
- [x] Phase 4: Cross-Reference Export (4/4 plans) — completed 2026-05-15
</details>

<details>
<summary>✅ v1.2 Wizard Reordering (Phase 5) — SHIPPED 2026-05-17</summary>

- [x] Phase 5: Wizard Reordering (1/1 plans) — completed 2026-05-17
</details>

### ✅ v1.3 Bugfix Pipeline de Extracción (Shipped)

- [x] **Phase 6: Preprocessor Proper Noun Fix** — clean_text() preserves proper noun casing instead of blanket lowercasing
- [x] **Phase 7: Post-Processing Pipeline** — CVProcessor applies gender inference, phone normalization, and RUT formatting after LLM extraction
- [x] **Phase 8: LLM Error Resilience & Retry** — Robust JSON parsing, schema fallback, and bounded retries within TPM limits

### 🔄 v1.4 Extracción Inteligente (In Progress)

- [ ] **Phase 9: Prompt Infrastructure & Foundation** — Version-controlled prompt registry with YAML files, resolver, and Git tracking
- [x] **Phase 10: Advanced Preprocessing** — Structural cleanup (section detection, layout normalization) and noise filtering before extraction (completed 2026-05-22)
- [x] **Phase 11: Document Classification** — TF-IDF + SVM document classifier using scikit-learn (completed 2026-05-24)
- [x] **Phase 12: Post-Processing Rules Expansion** — Pattern-based inference rules beyond gender/phone/RUT with shadow-mode deployment (completed 2026-05-24)
- [ ] **Phase 13: Two-Pass Pipeline** — Classifier output wired into extraction with type-specific prompts
- [ ] **Phase 14: OCR Augmentation** — PaddleOCR 3.0 integration, dual-engine fusion, and PP-StructureV3 layout analysis

## Phase Details

### Phase 6: Preprocessor Proper Noun Fix
**Goal**: clean_text() preserves proper noun casing instead of blanket lowercasing, so extracted names are correctly cased
**Depends on**: Nothing
**Requirements**: PREP-01
**Success Criteria** (what must be TRUE):
  1. User uploads a CV and all proper nouns (names, cities, surnames) in the output maintain correct casing
  2. User uploads a CV with all-caps names like "MARÍA GARCÍA" — output shows "María García" not "maría garcía"
  3. User uploads a CV and existing text normalization (whitespace, special characters) still works correctly
**Plans**: 1 plan
Plans:
- [x] 06-01-PLAN.md — Fix clean_text() proper noun casing + add tests

### Phase 7: Post-Processing Pipeline
**Goal**: CVProcessor applies gender inference, phone normalization, and RUT formatting after LLM extraction, only overriding fields the LLM couldn't find
**Depends on**: Nothing
**Requirements**: POST-01, POST-02, POST-03, POST-04
**Success Criteria** (what must be TRUE):
  1. User extracts a CV and the output includes inferred gender based on NOMBRES field
  2. User extracts a CV with phone variants (+56 X, 09 X, 569 X) — all normalize to consistent format
  3. User extracts a CV and RUT field is formatted consistently as XX.XXX.XXX-X
  4. When LLM successfully extracted a field, post-processing does NOT override it
  5. When LLM returns "NO ENCONTRADO" or empty for a field, post-processing fills the field automatically
**Plans**: 1 plan
Plans:
- [x] 07-01-PLAN.md — Wire post-processing pipeline into CVProcessor.process() + add tests

### Phase 8: LLM Error Resilience & Retry
**Goal**: llm_service handles malformed JSON gracefully with schema fallback and bounded retries within TPM limits
**Depends on**: Nothing
**Requirements**: LLM-01, LLM-02, RETR-01, RETR-02
**Success Criteria** (what must be TRUE):
  1. When Gemini returns JSON wrapped in markdown code fences, the parser strips fences and extracts valid JSON
  2. When Gemini returns malformed JSON, llm_service logs a warning and retries instead of crashing
  3. When dynamic schema extraction fails after retries, system falls back to EXTRACTION_SCHEMA
  4. Retry backoff never exceeds configured TPM limits
  5. User sees extracted data regardless of transient JSON formatting issues from Gemini
**Plans**: 3 plans
Plans:
- [x] 10-01-PLAN.md — Pydantic schemas + section-detection prompt YAML
- [x] 10-02-PLAN.md — SectionDetector, NoiseFilter, LayoutNormalizer + unit tests
- [x] 10-03-PLAN.md — PreprocessingPipeline orchestrator + integration tests

### Phase 9: Prompt Infrastructure & Foundation
**Goal**: Version-controlled prompt registry that tracks every prompt change, enables reproducible extractions, and decouples prompt engineering from code changes
**Depends on**: Nothing
**Requirements**: PROMPT-01
**Success Criteria** (what must be TRUE):
  1. Developer can create a new prompt version by adding a YAML file to `prompts/` with type, schema descriptions, and model parameters
  2. `PromptResolver` returns the correct prompt version for a given document type and version tag (e.g., `cv-extraction@v1.2`)
  3. Git tracking shows clean diffs when a prompt YAML changes — code and prompt changes are independently traceable
  4. System logs which prompt version was used for each extraction, enabling A/B comparison of prompt versions
**Plans**: 2 plans
Plans:
- [x] 09-01-PLAN.md — PromptVersion Pydantic model + YAML baseline
- [x] 09-02-PLAN.md — PromptResolver with semver, fallback, Jinja2, git tags
**UI hint**: no

### Phase 10: Advanced Preprocessing
**Goal**: Structural cleanup and noise removal applied before classification and extraction, so downstream stages receive clean, organized text
**Depends on**: Phase 9
**Requirements**: PREP-01, PREP-02
**Success Criteria** (what must be TRUE):
  1. System detects and preserves document sections (Education, Experience, Skills) while stripping non-content headers/footers
  2. Page headers, page numbers, footers, and document artifacts are removed from document text before extraction
  3. Layout normalization collapses inconsistent whitespace and line breaks into a uniform structure regardless of original formatting
  4. An uploaded CV with mixed content (body + artifacts) yields clean text with only meaningful sections preserved
**Plans**: 3 plans
Plans:
- [ ] 10-01-PLAN.md — Pydantic schemas + section-detection prompt YAML
- [ ] 10-02-PLAN.md — SectionDetector, NoiseFilter, LayoutNormalizer + unit tests
- [ ] 10-03-PLAN.md — PreprocessingPipeline orchestrator + integration tests
**UI hint**: no

### Phase 11: Document Classification
**Goal**: Classify document type using TF-IDF + SVM before extraction, enabling type-specific prompt selection and handling
**Depends on**: Phase 10
**Requirements**: CLASS-01
**Success Criteria** (what must be TRUE):
  1. System classifies a CV document as "CV" with >90% confidence using TF-IDF vectorization and SVM inference
  2. Classification completes in under 2 seconds per document (dominated by TF-IDF transform time)
  3. Classifier output includes confidence score and top-3 category predictions for downstream decision-making
  4. Non-CV documents are flagged and routed to appropriate handling or rejection with clear messaging
**Plans**: 3 plans
Plans:
- [x] 11-01-PLAN.md — Classification schemas + training data + TF-IDF vectorizer
- [x] 11-02-PLAN.md — DocClassifier with LinearSVC, prediction, confidence scoring
- [x] 11-03-PLAN.md — Integration tests and API endpoint
**UI hint**: no

### Phase 12: Post-Processing Rules Expansion
**Goal**: Expand pattern-based field inference beyond gender/phone/RUT with a registry of independently deployable rules, each validated in shadow mode before activation
**Depends on**: Phase 9
**Requirements**: RULES-01, RULES-02
**Success Criteria** (what must be TRUE):
  1. System infers at least 5 new fields using pattern-based rules (e.g., nationality, date of birth, email domain, education level, years of experience)
  2. New rules run in shadow mode by default — results are logged but not applied to extraction output
  3. A rule auto-activates only when shadow-mode evaluation shows ≥90% precision over 100+ samples
  4. Each rule operates independently — one rule failure does not cascade or block other rules
  5. System logs per-rule precision, recall, count, and activation status for monitoring and debugging
**Plans**: 3 plans
Plans:
- [ ] 10-01-PLAN.md — Pydantic schemas + section-detection prompt YAML
- [ ] 10-02-PLAN.md — SectionDetector, NoiseFilter, LayoutNormalizer + unit tests
- [ ] 10-03-PLAN.md — PreprocessingPipeline orchestrator + integration tests
**UI hint**: no

### Phase 13: Two-Pass Pipeline
**Goal**: Wire classifier output into the extraction pipeline so the LLM receives a type-specific prompt tailored to the document's detected category
**Depends on**: Phase 9, Phase 11
**Requirements**: PIPE-01
**Success Criteria** (what must be TRUE):
  1. System classifies document first, then selects the corresponding type-specific prompt from the prompt registry before extraction
  2. A CV document classified as "CV-Ecuadorian" receives a prompt optimized for Ecuadorian CV formats (e.g., cédula instead of RUT)
  3. Two-pass extraction (classify → extract) shows ≥5% improvement in field detection rate over single-pass baseline
  4. Pipeline logs both the classification decision and the prompt version used, enabling end-to-end traceability per extraction
**Plans**: 3 plans
Plans:
- [ ] 10-01-PLAN.md — Pydantic schemas + section-detection prompt YAML
- [ ] 10-02-PLAN.md — SectionDetector, NoiseFilter, LayoutNormalizer + unit tests
- [ ] 10-03-PLAN.md — PreprocessingPipeline orchestrator + integration tests
**UI hint**: no

### Phase 14: OCR Augmentation
**Goal**: Improve OCR quality for scanned/image-based CVs through dual-engine fusion and layout recovery, reducing OCR-related extraction failures
**Depends on**: Phase 10
**Requirements**: OCR-01, OCR-02, OCR-03
**Success Criteria** (what must be TRUE):
  1. System processes image-based PDFs through PaddleOCR 3.0 as a fallback when Tesseract confidence is below threshold
  2. Dual-engine fusion combines Tesseract and PaddleOCR outputs, selecting the higher-confidence text per line
  3. PP-StructureV3 layout analysis recovers correct reading order for multi-column or complex-layout CVs
  4. OCR-augmented documents show measurably lower "NO ENCONTRADO" rate than Tesseract-only processing
  5. Spanish diacritics (tildes, ñ, accents) are preserved through OCR processing with <1% loss rate
**Plans**: 3 plans
Plans:
- [ ] 10-01-PLAN.md — Pydantic schemas + section-detection prompt YAML
- [ ] 10-02-PLAN.md — SectionDetector, NoiseFilter, LayoutNormalizer + unit tests
- [ ] 10-03-PLAN.md — PreprocessingPipeline orchestrator + integration tests
**UI hint**: no

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Frontend Overhaul (Apple Design) | v1.0 | 4/4 | Complete | 2026-05-14 |
| 2. Crossref Page Redesign | v1.1 | 3/3 | Complete | 2026-05-15 |
| 3. Wizard Cross-Reference Integration | v1.1 | 3/3 | Complete | 2026-05-15 |
| 4. Cross-Reference Export | v1.1 | 4/4 | Complete | 2026-05-15 |
| 5. Wizard Reordering | v1.2 | 1/1 | Complete | 2026-05-17 |
| 6. Preprocessor Proper Noun Fix | v1.3 | 1/1 | Complete | 2026-05-18 |
| 7. Post-Processing Pipeline | v1.3 | 1/1 | Complete | 2026-05-18 |
| 8. LLM Error Resilience & Retry | v1.3 | 1/1 | Complete | 2026-05-19 |
| 9. Prompt Infrastructure & Foundation | v1.4 | 2/2 | Complete | 2026-05-21 |
| 10. Advanced Preprocessing | v1.4 | 3/3 | Complete    | 2026-05-22 |
| 11. Document Classification | v1.4 | 3/3 | Complete | 2026-05-24 |
| 12. Post-Processing Rules Expansion | v1.4 | 3/3 | Complete | 2026-05-24 |
| 13. Two-Pass Pipeline | v1.4 | 0/0 | Not started | - |
| 14. OCR Augmentation | v1.4 | 0/0 | Not started | - |
