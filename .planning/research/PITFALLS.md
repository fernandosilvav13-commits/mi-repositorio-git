# Pitfalls Research: v1.4 Extracción Inteligente

## OCR Pitfalls

### P1: Aggressive preprocessing strips Spanish diacritics
- **Problem:** Despeckling/binarization silently strips tildes and diacritics (José → Jose, Ingeniería → Ingenieria)
- **Prevention:** Per-step A/B testing with character error rate (CER) before adding any preprocessing step
- **Phase:** OCR augmentation (Phase 6)

### P2: PaddleOCR latency in sync pipeline
- **Problem:** PaddleOCR is GPU-accelerated but adds 2-5s per page vs Tesseract's 0.5-1s
- **Prevention:** Keep Tesseract as default for clean PDFs. Only route to PaddleOCR when image-based document detected. Async processing for batch operations.

### P3: Layout analysis over-fitting
- **Problem:** PP-StructureV3 layout models trained on English/Chinese docs may misparse Spanish CV layouts
- **Prevention:** Evaluate on a sample of real CVs before enabling layout-aware extraction

## Prompt Engineering Pitfalls

### P4: Over-optimization on small sample
- **Problem:** Tuning prompts against 5-10 CVs produces brittle extraction that breaks when format distribution shifts
- **Prevention:** Version-controlled prompt registry with per-field regression harness. Test against minimum 30 diverse CVs.

### P5: Breaking existing working extractions
- **Problem:** New prompt improves field X but breaks previously working field Y
- **Prevention:** Regression test suite covering all fields. Run full suite before deploying any prompt change.

### P6: Schema drift between prompt and code
- **Problem:** Prompt references field names that don't match the code's EXTRACTION_SCHEMA
- **Prevention:** Single source of truth for field names. Auto-generate prompt schema section from code schema.

## Document Classification Pitfalls

### P7: Over-classification creates maintenance burden
- **Problem:** Too many document type categories (10+) that are hard to distinguish, leading to constant threshold tuning
- **Prevention:** Start with 3-5 broad categories (CV, Cover Letter, Certificate, Other). Only split when accuracy requires it.

### P8: Classifier errors are systemic
- **Problem:** Harder-to-classify documents are also harder to extract from — classifier errors compound
- **Prevention:** Uncertainty propagation. When classifier confidence is low, use generic extraction rather than wrong-type extraction.

### P9: Cold start — no labeled data
- **Problem:** TF-IDF classifier needs 200+ labeled examples for reliable accuracy
- **Prevention:** Start with keyword tier (50ms, no training needed). Collect labeled data from production. Train TF-IDF model when sufficient data exists.

## Post-Processing Rules Pitfalls

### P10: False positives from aggressive pattern matching
- **Problem:** Pattern-matching fields that are semantic, not pattern-based (salary, seniority, education level) produces wrong data that looks right
- **Prevention:** Field suitability triage: pattern-based (RUT, phone, email) vs semantic (cargo, seniority). Only apply rules to pattern-based fields. 90% precision floor enforced.

### P11: Rules masking real LLM failures
- **Problem:** Post-processing rules fill "NO ENCONTRADO" fields, hiding the fact that the LLM is failing on those fields
- **Prevention:** Log provenance per field: `{value, source: "llm"|"rule", rule_name}`. Monitor LLM coverage rate separately.

### P12: Circular dependencies between rules
- **Problem:** Rule A depends on field X that Rule B sets, Rule B depends on field Y that Rule A sets
- **Prevention:** Rule registry with declared dependencies. DAG validation at registration time. Fail on circular dependency.

## Multi-Step Pipeline Pitfalls

### P13: Error propagation without traceability
- **Problem:** A failure in step 2 produces garbage in step 5, but logs show step 5 failing — root cause is invisible
- **Prevention:** Structured logging with trace IDs per document. Each step logs: input_trace_id, output_trace_id, step_name, duration, status.

### P14: Latency accumulation
- **Problem:** 2-pass pipeline doubles LLM calls. Classifier (100ms) + PaddleOCR (3s) + two Gemini calls (6s) = 9s+ per document
- **Prevention:** Measure per-step latency in production. Implement async processing for batch operations. Set SLA targets per document type.

### P15: Backward compatibility breaks
- **Problem:** New pipeline adds provenance tags, confidence scores, and intermediate fields that break existing API contracts (extraction_results table, Excel export)
- **Prevention:** Backward-compatible output schemas. Feature flags for new pipeline. Shadow-mode deployment before switching.

## Integration Pitfalls

### P16: Phase ordering mistakes
- **Problem:** Starting OCR without prompt versioning means no baseline to measure improvement against
- **Prevention:** Prompt scaffolding first (Phase 1) before any quality improvement. Measure baseline, then improve.

### P17: Cache invalidation
- **Problem:** Cache_service stores results by (text, schema, model). Prompt changes don't invalidate cache. Users see old extraction results with new prompts.
- **Prevention:** Include prompt version hash in cache key. Bump cache on prompt deployment.

### P18: Testing complexity
- **Problem:** Multi-step pipeline is harder to test. Integration tests need end-to-end golden dataset.
- **Prevention:** Unit tests per step + integration tests for end-to-end pipeline. Golden dataset with 50+ annotated CVs.
