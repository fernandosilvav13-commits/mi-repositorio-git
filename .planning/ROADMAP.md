# Roadmap — CicloAI

## Milestones

- ✅ **v1.0 MVP** — Phase 1 (shipped 2026-05-15)
- ✅ **v1.1 Cross-Reference Integration** — Phases 2–4 (shipped 2026-05-15)
- ✅ **v1.2 Wizard Reordering** — Phase 5 (shipped 2026-05-17)
- ✅ **v1.3 Bugfix Pipeline de Extracción** — Phases 6–8 (shipped 2026-05-19)

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
**Plans**: TBD

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
