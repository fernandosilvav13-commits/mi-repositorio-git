# Roadmap — CicloAI

## Milestones

- ✅ **v1.0 MVP** — Phase 1 (shipped 2026-05-15)
- ✅ **v1.1 Cross-Reference Integration** — Phases 2–4 (shipped 2026-05-15)
- ✅ **v1.2 Wizard Reordering** — Phase 5 (shipped 2026-05-17)
- ✅ **v1.3 Bugfix Pipeline de Extracción** — Phases 6–8 (shipped 2026-05-19)
- ✅ **v1.4 Extracción Inteligente** — Phases 9–15 (shipped 2026-06-16)

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

**Deferred to v1.5:** OCR-01 (PaddleOCR 3.0), OCR-02 (Tesseract+PaddleOCR fusion), OCR-03 (PP-StructureV3 layout)

See: `.planning/milestones/v1.4-ROADMAP.md` for full archive

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
| 15. Close Gap — Register /api/classify in main.py | v1.4 | 2/2 | Shipped | 2026-06-16 |
