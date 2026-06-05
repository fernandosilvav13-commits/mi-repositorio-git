# Phase 14: OCR Augmentation - Context

**Gathered:** 2026-05-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Enhance document ingestion with Tesseract OCR fallback and coordinate-based layout analysis. Implements OCR-01, OCR-02, OCR-03.

</domain>

<analysis>
## Current State

- `FileParser` in `app/utils/file_parser.py` already has:
  - `tesserocr`-based `_ocr_image()` for images and PDF fallback
  - PDF text extraction via pdfplumber with OCR fallback
- `OCRService` in `app/services/ocr_service.py` — thin wrapper around FileParser
- **Missing:** layout analysis, coordinate extraction, text ordering

## Needed

1. **OCR-01:** Tesseract via `pytesseract` (simpler than `tesserocr` which requires C headers)
2. **OCR-02:** Fallback when pdfplumber yields no text (already done) 
3. **OCR-03:** Layout analysis using Tesseract word-level bounding boxes to detect columns, sections, and reading order

</analysis>

<decisions>
## Implementation Decisions

### OCR Engine
- **D-01:** Keep `pytesseract` as the Python wrapper (simpler install than `tesserocr`)
- **D-02:** Fallback chain: pdfplumber → Tesseract OCR (when PDF is scanned/image-only)

### Layout Analysis (OCR-03)
- **D-03:** Create `LayoutAnalyzer` class in `app/services/layout_analyzer.py`
- **D-04:** Uses Tesseract word-level bounding box data to:
  - Detect column count (cluster word x-coordinates)
  - Detect headers (bold-ish via height/width ratios or position)
  - Reorder text in natural reading order (top-to-bottom, left-to-right)
- **D-05:** Output: `LayoutResult` with structured sections

### Integration
- **D-06:** `_ocr_image()` in FileParser returns plain text (backward compat)
- **D-07:** New `ocr_with_layout()` method in OCRService returns LayoutResult
- **D-08:** `pytesseract` replaces `tesserocr` in FileParser

</decisions>

<canonical_refs>
## Canonical References

- `backend/app/utils/file_parser.py` — current OCR code
- `backend/app/services/ocr_service.py` — current OCR service (thin wrapper)

</canonical_refs>

---

*Phase: 14-OCR Augmentation*
*Context gathered: 2026-05-24*
