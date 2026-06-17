# Roadmap — CicloAI

## Milestones

- ✅ **v1.0 MVP** — Phase 1 (shipped 2026-05-15)
- ✅ **v1.1 Cross-Reference Integration** — Phases 2–4 (shipped 2026-05-15)
- ✅ **v1.2 Wizard Reordering** — Phase 5 (shipped 2026-05-17)
- ✅ **v1.3 Bugfix Pipeline de Extracción** — Phases 6–8 (shipped 2026-05-19)
- ✅ **v1.4 Extracción Inteligente** — Phases 9–15 (shipped 2026-06-16)
- 🏗️ **v1.5 Consolidación de Extracción** — Phases 16–21 (active)

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

### ✅ v1.4 Extracción Inteligente (Phases 9-15) — SHIPPED 2026-06-16

- [x] Phase 9: Prompt Infrastructure & Foundation (2/2 plans) — completed 2026-05-21
- [x] Phase 10: Advanced Preprocessing (3/3 plans) — completed 2026-05-22
- [x] Phase 11: Document Classification (3/3 plans) — completed 2026-05-24
- [x] Phase 12: Post-Processing Rules Expansion (3/3 plans) — completed 2026-05-24
- [x] Phase 13: Two-Pass Pipeline (3/3 plans) — completed 2026-05-24
- [x] Phase 14: OCR Augmentation (4/4 plans) — completed 2026-05-25
- [x] Phase 15: Close Gap — Register /api/classify in main.py (2/2 plans) — completed 2026-06-13

**Deferred after v1.5:** OCR-01 (PaddleOCR 3.0), OCR-02 (Tesseract+PaddleOCR fusion), OCR-03 (PP-StructureV3 layout)

See: `.planning/milestones/v1.4-ROADMAP.md` for full archive

### 🏗️ v1.5 Consolidación de Extracción (Phases 16-21) — Active

- [x] **Phase 16: LLM Provider Abstraction** — Multi-provider abstraction (Gemini, Anthropic, OpenAI) with auto-detection, factory, model resolution, TPM tracking, section_detector.py bugfix, and 6/6 UAT tests. Completed 2026-06-17.
- [x] **Phase 17: Deduplicate batch_process.py** — Refactored to use llm_service.extract_fields(), removed hardcoded prompt/retry/JSON repair. Completed 2026-06-17.
- [ ] **Phase 18: Config Orphans Cleanup** — Remove gemini_model_* legacy vars, unused llm_provider field, sanitize Settings.
- [ ] **Phase 19: Real-CV Validation** — End-to-end test with 5+ real CVs through the wizard, fix discovered bugs.
- [ ] **Phase 20: Post-Processing Refinement** — Improve gender inference, phone normalization, RUT formatting, evaluate shadow rules for promotion.

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
| 9. Prompt Infrastructure & Foundation | v1.4 | 2/2 | Shipped | 2026-05-21 |
| 10. Advanced Preprocessing | v1.4 | 3/3 | Shipped | 2026-05-22 |
| 11. Document Classification | v1.4 | 3/3 | Shipped | 2026-05-24 |
| 12. Post-Processing Rules Expansion | v1.4 | 3/3 | Shipped | 2026-05-24 |
| 13. Two-Pass Pipeline | v1.4 | 3/3 | Shipped | 2026-05-24 |
| 14. OCR Augmentation | v1.4 | 4/4 | Shipped | 2026-05-25 |
| 15. Close Gap — Register /api/classify in main.py | v1.4 | 2/2 | Shipped | 2026-06-13 |
| 16. LLM Provider Abstraction | v1.5 | 6/6 UAT | Complete | 2026-06-17 |
| 17. Deduplicate batch_process.py | v1.5 | 1/1 | Complete | 2026-06-17 |
| 18. Config Orphans Cleanup | v1.5 | — | Pending | — |
| 19. Config Orphans Cleanup | v1.5 | — | Pending | — |
| 20. Real-CV Validation | v1.5 | — | Pending | — |
| 21. Post-Processing Refinement | v1.5 | — | Pending | — |
