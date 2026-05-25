# Phase 13: Two-Pass Pipeline - Context

**Gathered:** 2026-05-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Wire classifier output into the extraction pipeline so the LLM receives a type-specific prompt tailored to the document's detected category. Implements PIPE-01.

</domain>

<decisions>
## Implementation Decisions

### Pipeline Architecture
- **D-01:** Create `backend/app/services/extraction_pipeline.py` as the orchestrator. Chains: PreprocessingPipeline → DocClassifier → LLM extraction with type-specific prompt.
- **D-02:** The pipeline returns a dict with: extraction data + classification result + prompt version used.

### Prompt Selection
- **D-03:** For "cv" classification, use PromptResolver to get `cv-extraction` prompt (default version ^v1.0.0).
- **D-04:** For "non-cv" classification, return an error/warning message rather than attempting extraction with a CV-specific prompt. Let the calling code handle the routing decision.

### Non-CV Handling
- **D-05:** Non-CV documents are flagged in the result with a `classification_warning` field. The existing extraction flow (cv_extractor) is bypassed.
- **D-06:** The pipeline logs classification decision and prompt version for traceability.

### Integration Points
- **D-07:** The pipeline replaces the direct call to `extract_cv_data()` in `cv_processor.py` for the two-pass flow.
- **D-08:** Existing single-pass extraction remains available for backward compatibility.

</decisions>

<canonical_refs>
## Canonical References

### Existing Code
- backend/app/services/preprocessor.py — PreprocessingPipeline (Phase 10)
- backend/app/services/classifier.py — DocClassifier (Phase 11)
- backend/app/services/prompt_resolver.py — PromptResolver (Phase 9)
- backend/app/services/cv_processor.py — Existing extraction consumer

</canonical_refs>

---

*Phase: 13-Two-Pass Pipeline*
*Context gathered: 2026-05-24*
