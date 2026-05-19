# Features Research: v1.4 Extracción Inteligente

## Feature Landscape

### Table Stakes (must-have for a quality extraction system)

1. **Schema description optimization** — Google explicitly recommends iterating on schema `description` fields first. Current code has empty descriptions on every schema property. This is the highest-leverage, lowest-effort improvement.
2. **One-shot prompting** — 2025 peer-reviewed research shows 1-shot extraction consistently outperforms zero-shot across all tested LLMs. Providing an example in the prompt improves accuracy measurably.
3. **Structured prompt format** — Clear Task / Format / Constraints / Examples sections. Current prompt is a single paragraph.
4. **Reading order recovery** — Layout analysis (what PaddleOCR PP-StructureV3 provides) ensures text is passed to LLM in correct reading order.
5. **Multi-engine OCR fusion** — Combining Tesseract (clean PDFs) + PaddleOCR (scanned docs) with per-line confidence scoring.

### Differentiators (features that set the system apart)

1. **Two-pass pipeline (classify → extract)** — Dominant IDP architecture (AWS, Google, Microsoft). Classify document type first, then extract with type-specific schema and prompt. Doubles LLM calls but dramatically improves accuracy.
2. **Rule registry for post-processing** — Decorator-registered rule modules with declared dependencies and priority ordering. Each rule independently testable. Enables expanding beyond gender/phone/RUT without spaghetti code.
3. **Prompt versioning with regression harness** — Git-tracked YAML prompt files with per-field regression detection. Prevents "fix one CV, break another" syndrome.
4. **Field-level confidence scoring** — Each extracted field tagged with confidence (regex match → HIGH, pattern heuristic → MEDIUM, pure LLM → LOW). Enables threshold-based fallback. (v1.5 candidate but worth designing for now.)

### Anti-Features (avoid)

1. **Real-time ocr streaming** — Not needed. Batch extraction is the workflow.
2. **Fine-tuned LLM** — Gemini fine-tuning not available/needed. Prompt engineering + schema optimization is sufficient.
3. **Full BERT-based document classification** — Overkill. TF-IDF + SVM matches accuracy at fraction of cost.
4. **Cloud OCR APIs** — Cost-prohibitive at scale. Self-hosted PaddleOCR is sufficient.
5. **Confidence scores in v1.4** — Defer to v1.5. Design data model now but don't implement.

## Feature Complexity & Dependencies

| Feature | Complexity | Dependencies | Risk |
|---------|-----------|--------------|------|
| Schema description optimization | Low (1-2h) | None | Very low |
| Prompt restructuring | Low (1h) | Prompt versioning | Very low |
| Prompt versioning scaffolding | Medium (4h) | None | Low |
| Advanced preprocessing | Medium (1-2d) | Prompt versioning | Medium |
| Document classifier (keyword + TF-IDF) | Medium (2-3d) | Advanced preprocessing | Medium |
| Two-pass pipeline | Medium (1d) | Document classifier | Medium |
| Rule registry for post-processing | Medium (2-3d) | None (parallel) | High |
| OCR augmentation (PaddleOCR) | High (3-5d) | None (parallel) | Medium |

## Recommendations by Priority

**P0 (immediate, this week):**
- Schema description optimization — 1-2h, biggest ROI
- Prompt restructuring with Task/Format/Constraints — 1h

**P1 (v1.4 core):**
- Prompt versioning scaffolding — 4h
- Document classifier (keyword + TF-IDF tier) — 2-3d
- Two-pass pipeline — 1d
- Post-processing rule registry — 2-3d

**P2 (defer or optional):**
- PaddleOCR integration — 3-5d
- LLM-based classifier tier — 2-3d
- Confidence scoring — v1.5
