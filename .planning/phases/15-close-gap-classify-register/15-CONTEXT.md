# Phase 15: Close Gap — Register /api/classify in main.py — Context

**Gathered:** 2026-06-13
**Status:** Ready for planning

<domain>
## Phase Boundary

Wire the existing classify router and two-pass pipeline into the production FastAPI application. Closes CLASS-01 and PIPE-01 blockers identified in v1.4 audit — the code already exists, it just needs to be connected and activated.

</domain>

<decisions>
## Implementation Decisions

### Two-Pass Pipeline Activation
- **D-01:** Change `CVProcessor` default to `use_two_pass=True` in `backend/app/services/cv_processor.py:23`. The pipeline (preprocess → classify → type-specific extract) becomes the standard extraction path.
- **D-02:** Keep `use_two_pass=False` as an explicit opt-out parameter for backward compatibility. The constructor argument remains, just the default flips.
- **D-03:** No separate endpoint or API-level parameter — simplest activation path.

### Classify Router Registration
- **D-04:** Register `classify` router under standalone prefix `/api/classify` in `backend/app/main.py`. Add to the imports and `include_router` calls.
- **D-05:** The classify endpoint preprocesses text before classification by calling `preprocessing_pipeline.process()` for consistency with the two-pass pipeline behavior.

### PromptResolver Path
- **D-06:** Align `extraction_pipeline.py` to use the absolute path pattern (`Path(__file__).resolve().parent.parent / "prompts"`) matching `section_detector.py:21`. Replace the current default relative path `"backend/prompts"`.

### the agent's Discretion
- Agent has discretion on import sorting, router tag naming, and error handling details for classify registration.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Core Files to Modify
- `backend/app/main.py` — FastAPI app, router registration (add classify import and include_router)
- `backend/app/services/cv_processor.py` — Change use_two_pass default to True (line 23)
- `backend/app/services/extraction_pipeline.py` — Fix PromptResolver path (line 10)
- `backend/app/api/classify.py` — Classify router (exists, needs registration + preprocessing)

### Supporting Code
- `backend/app/services/section_detector.py:21` — Absolute path pattern for PromptResolver (reference for D-06)
- `backend/app/services/preprocessor.py` — PreprocessingPipeline singleton (for D-05 classify preprocessing)
- `backend/app/services/classifier.py` — DocClassifier (used by both classify endpoint and extraction pipeline)
- `backend/app/services/prompt_resolver.py` — PromptResolver (path fix target)

### Audit / Requirements
- `.planning/v1.4-MILESTONE-AUDIT.md` — Full audit report with blocker details (B1, B2)
- `.planning/REQUIREMENTS.md` — CLASS-01, PIPE-01 requirement definitions

### Prior Phase Context
- `backend/app/services/cv_processor.py` — CVProcessor with use_two_pass flag (Phase 13)
- `backend/app/services/extraction_pipeline.py` — ExtractionPipeline orchestrator (Phase 13)
- `backend/app/services/classifier.py` — DocClassifier (Phase 11)
- `backend/app/api/classify.py` — classify router (Phase 11)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `PreprocessingPipeline` singleton (`preprocessing_pipeline`) — ready to import in classify.py for D-05
- `PromptResolver` class — used by both section_detector and extraction_pipeline, path pattern fix needed
- `doc_classifier` module-level singleton — used by extraction_pipeline, needed by classify endpoint

### Established Patterns
- Module-level service singletons (cv_processor, ocr_service, doc_classifier, preprocessing_pipeline)
- FastAPI APIRouter per domain (ingest, extraction, templates, rules, export, crossref)
- Backward compat via optional parameters (legacy path preserved alongside new)

### Integration Points
- `backend/app/main.py` — router registration list (add classify to imports + include_router)
- `backend/app/services/cv_processor.py:23` — use_two_pass default toggle
- `backend/app/services/extraction_pipeline.py:10` — PromptResolver path fix

</code_context>

<specifics>
## Specific Ideas

- Activation should be safe: all existing tests (184+) verify both paths continue to work
- Classify endpoint should produce identical results to what the pipeline produces internally for the same input

</specifics>

<deferred>
## Deferred Ideas

- Full PaddleOCR 3.0 integration (OCR-01, OCR-02 gaps) — deferred to future phase (separate from this gap closure)
- Phase 9 missing VERIFICATION.md — not addressed by this phase (separate process gap)
- Nyquist VALIDATION.md creation — not addressed by this phase

</deferred>

---

*Phase: 15-Close Gap — Register /api/classify in main.py*
*Context gathered: 2026-06-13*
