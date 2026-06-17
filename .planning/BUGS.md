# BUGS.md — Phase 19: Real-CV Validation Findings

> Generated: 2026-06-17
> CVs tested: 6 (3 DOCX, 3 DOC)
> Pipeline success rate: 1/6 (CV 140180122 — all fields correct)
> Pipeline partial success: 1/6 (CV 12447146K — text garbled, no usable extraction)
> Pipeline failure: 4/6

## BUG-001: Classifier false negatives on real CVs (Critical)

**Affected component:** `app/services/classifier.py` (TF-IDF + SVM)
**Trigger:** Any real CV formatted differently than training samples
**CV affected:** 103386861 (Patricio Parra), possibly others

**Evidence:**
- CV text clearly contains: RUT, experiencia laboral, formación académica, datos personales
- Classifier reports: `non-cv (0.8541)` — 85% confident it's NOT a CV
- Pipeline returns empty result (line 93): `if pipeline_result.get("classification_warning"): return {}`

**Root cause:**
- Training data (`app/data/training_samples.py`) has only 50 synthetic samples (40 CV, 10 non-CV)
- Real CVs contain section headers like "EXPERIENCIA DIRECTIVA-LIDERAZGO" that differ from training format "EXPERIENCIA LABORAL"
- The 40 synthetic CV training samples lack the diversity of real-world CV formats

**Severity:** Critical — causes false pipeline skip on valid CVs

**Suggested fix:**
1. Add real CV texts to `TRAINING_SAMPLES` to improve classifier accuracy
2. OR lower `CLASSIFICATION_THRESHOLD` from 0.5 to allow more through
3. OR add confidence-banding: if confidence is 50-85%, still attempt extraction with a warning flag

## BUG-002: DOC binary parser loses accented characters (Critical)

**Affected component:** `app/utils/file_parser.py:75-89` (`_parse_doc_ole`)
**Trigger:** Any .doc file with Spanish text
**CVs affected:** 106071497, 12447146K, 136173219 (all 3 .doc files)

**Evidence:**
- Stage 3 OLE2 parser only extracts ASCII chars in range 32-126 plus CR/LF/tab
- Accented characters (á, é, í, ó, ú, ñ, ü) are outside this range (decimal 160+)
- Result: text is garbled binary with few readable words

**Code (file_parser.py:80-87):**
```python
if 32 <= ord(c) <= 126 or ord(c) in (10, 13, 9):
    text += c
```

**Severity:** Critical — renders ALL .doc files unusable for Spanish CVs

**Suggested fix:**
1. Extend character range to include Latin-1 supplement (160-255): `32 <= ord(c) <= 255`
2. OR install `antiword` or `catdoc` CLI tools for proper .doc parsing
3. OR use LibreOffice headless conversion: `soffice --convert-to docx`
4. OR activate `extract_with_fallback()` to OCR the document as image

## BUG-003: OCR fallback never called in production (Major)

**Affected component:** `app/services/ocr_service.py:38-53`
**Trigger:** Any document where text extraction fails (binary .doc, image-only .docx)
**CVs affected:** 106071497, 12447146K, 127944113, 136173219 (4/6)

**Evidence:**
- `extract_with_fallback()` method exists (ocr_service.py:38) with full OCR fallback logic
- However, `process_document()` (line 16) calls `parser.extract_text()` directly — no fallback
- No production code calls `extract_with_fallback()`

**Code path:**
```
extraction.py:63 → ocr_service.process_document()  ← no fallback
                  ocr_service.extract_with_fallback() ← exists but never called
```

**Severity:** Major — leaves a working OCR fallback unused

**Suggested fix:**
- Replace `process_document()` with `extract_with_fallback()` in the extraction API endpoint

## BUG-004: DOCX with embedded images yields 0 text (Major)

**Affected component:** `app/utils/file_parser.py:58-61` (`_parse_docx`)
**Trigger:** DOCX file where text is in images (scanned document saved as DOCX)
**CV affected:** 127944113 (1.6MB DOCX, 0 chars extracted)

**Evidence:**
- `python-docx` only extracts text from paragraph elements
- Scanned/image DOCX has no text paragraphs → returns empty string
- No fallback to OCR for DOCX with no extractable text

**Severity:** Major — common scenario for scanned CVs

**Suggested fix:**
- In `_parse_docx()`, if `len(text.strip()) == 0`, fall back to OCR via pytesseract
- Or handle at OCRService level: if `process_document` returns < 20 chars, try OCR

## BUG-005: FileParser DOC fallback not attempted for DOCX (Minor)

**Affected component:** `app/utils/file_parser.py:27-43`
**Trigger:** DOCX with no text
**CV affected:** 127944113

**Evidence:**
- `extract_text()` routes `.docx` to `_parse_docx()` only — no cascade fallback
- Unlike `.doc` which has 3-stage fallback, `.docx` has a single attempt

**Severity:** Minor — covered if BUG-004 is fixed

## BUG-006: Antiword/catdoc available in batch_process but not FileParser (Minor)

**Affected component:** `app/utils/file_parser.py` vs `batch_process.py`
**Trigger:** N/A — architectural observation

**Evidence:**
- `batch_process.py:90-162` has richer `.doc` parsing with `antiword` and `catdoc` CLI fallbacks
- `file_parser.py`'s `_parse_doc()` doesn't use these tools

**Severity:** Minor — suggests code duplication between pipelines

---

## Summary Table

| ID | Bug | Severity | CVs affected | Component |
|----|-----|----------|-------------|-----------|
| 001 | Classifier false negatives | **Critical** | 1/6 (likely more) | classifier.py |
| 002 | DOC parser loses accents | **Critical** | 3/6 (all .doc) | file_parser.py |
| 003 | OCR fallback not wired | **Major** | 4/6 | ocr_service.py |
| 004 | DOCX images → 0 text | **Major** | 1/6 | file_parser.py |
| 005 | DOCX no fallback cascade | **Minor** | 1/6 | file_parser.py |
| 006 | antiword not in FileParser | **Minor** | — | file_parser.py vs batch_process.py |

## Working CV (success)
- **140180122** (Rodrigo René Pardo Inzulza) — DOCX, 21KB — ALL fields extracted correctly ✅
  - RUT: 14.018.012-2 ✓ (matches folder name)
  - NOMBRES: Rodrigo René ✓
  - APELLIDOS: Pardo Inzulza ✓
  - GENERO: Masculino ✓
  - Phone: +56712224935 / +56983391450 ✓
  - TITULO_PROFESIONAL: Profesor de Educación General Básica ✓
  - experiencia_laboral: parsed ✓
