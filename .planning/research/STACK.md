# Stack Research: v1.4 Extracción Inteligente

## Current Stack

- **Backend:** FastAPI, Python 3.12
- **LLM:** Gemini 2.5 Flash Lite (extraction), Gemini 2.5 Flash (retry/crossref)
- **OCR:** Tesseract (tesserocr), pdfplumber
- **Document parsing:** python-docx, python-pptx
- **Storage:** Supabase
- **Frontend:** Next.js 16, Tailwind v4, Apple Design System

## Recommended Additions

### 1. PaddleOCR 3.0 (for scanned/image PDFs)

- **Version:** PaddleOCR 3.0 / PP-Structure v3
- **Why:** 94.5% OmniDocBench score vs Tesseract ~85% on scanned docs. Built-in layout analysis (PP-StructureV3) recovers reading order and detects tables/headers automatically.
- **Cost:** Self-hosted ~$0.09/1K pages vs $1-15 for cloud APIs
- **License:** Apache 2.0
- **Integration:** Run in parallel with Tesseract for scanned PDFs, fuse results by per-line confidence. Keep Tesseract as lightweight CPU fallback for clean text-based PDFs.
- **Risks:** CUDA 12.x GPU recommended for production throughput. PaddlePaddle has Windows/Linux support but verify tensorrt compatibility with existing deployment.

### 2. spaCy + EntityRuler (for advanced post-processing)

- **Version:** spaCy 3.8+, `es_core_news_sm` Spanish model
- **Why:** Token-pattern matching (not regex) that understands POS tags and dependency relations. Far more maintainable than raw regex for fields like RUT, phone, email, education, job titles.
- **Integration:** New `rules/` module with decorator-registered rule modules. Each rule independently testable.

### 3. scikit-learn (for document classification)

- **Version:** scikit-learn 1.6+
- **Why:** TF-IDF + LinearSVC achieves >96% accuracy on resume categorization. <50ms inference, no GPU needed. Far more practical than BERT for this task.
- **Integration:** Lightweight classifier service before LLM extraction step.

### 4. Promptfoo (for prompt optimization)

- **Version:** Open-source (MIT-licensed)
- **Why:** Native Gemini provider support, YAML test suites, CI/CD integration, regression detection.
- **Integration:** Test suite with labeled CV examples. Run prompt iterations against regression harness.

## What NOT to Add

- **json-repair / json5:** Avoid new JSON dependencies — existing regex-based repair handles production patterns.
- **BERT/transformers for classification:** Overkill for document type detection. TF-IDF + SVM matches accuracy at fraction of cost.
- **Cloud OCR (Google Vision, AWS Textract):** Cost-prohibitive at scale. PaddleOCR self-hosted is sufficient.
- **Redis/Memcached:** Existing in-memory cache is sufficient for current scale.

## Integration Points

| Library | Existing File | Change |
|---------|--------------|--------|
| PaddleOCR | `backend/app/services/ocr_service.py` | Add as alternative OCR backend with confidence-based fusion |
| spaCy + EntityRuler | `backend/app/services/cv_processor.py` | New rule registry module, called from post-processing |
| scikit-learn | `backend/app/services/classifier_service.py` (new) | New service, called after preprocessing but before LLM |
| Promptfoo | `prompts/` (new directory) | Version-controlled prompt files with test suite |
