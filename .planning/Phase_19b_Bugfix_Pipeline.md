# PLAN — Phase 19b: Bugfix Pipeline (sub-fase de Phase 19)

> Basado en bugs descubiertos en Phase 19 (Real-CV Validation): `.planning/BUGS.md`

## Objetivo

Arreglar los 4 bugs críticos/mayores descubiertos durante la validación con CVs reales para que el pipeline procese correctamente archivos .doc y DOCX con imágenes, y reduzca los falsos negativos del clasificador.

## Priorización

| Prioridad | Bug | CVs afectados | Esfuerzo |
|-----------|-----|---------------|----------|
| **P0** | BUG-002: DOC parser pierde acentos | 3/6 | ⚡ 1 tarea |
| **P1** | BUG-001: Clasificador falsos negativos | 1/6+ | ⚡ 2 tareas |
| **P2** | BUG-003: OCR fallback no conectado | 4/6 | ⚡ 1 tarea |
| **P3** | BUG-004: DOCX con imágenes → 0 texto | 1/6 | ⚡ 1 tarea |
| **P4** | BUG-005/006: Mejoras menores | — | ⚡ 1 tarea |

## Tareas

### Task 1: Fix DOC parser accent handling (P0 — BUG-002)

**Archivo:** `app/utils/file_parser.py:80-87`

**Qué:** Expandir el rango de caracteres en `_parse_doc_ole()` para incluir Latin-1 Supplement (160-255):

```python
# Antes:
if 32 <= ord(c) <= 126 or ord(c) in (10, 13, 9):
# Después:
if 32 <= ord(c) <= 255 or ord(c) in (10, 13, 9):
```

**Verificación:** Re-ejecutar `validate_cv.py` en los 3 CVs .doc y verificar que los acentos aparecen.

### Task 2: Fix classifier false negatives (P1 — BUG-001)

**Archivos:** `app/data/training_samples.py`, `app/services/classifier.py`

**Opción recomendada (2a):** Agregar textos de CVs reales (extractos de los CVs validados) a `TRAINING_SAMPLES` — 5-10 muestras etiquetadas como "cv". Esto mejora la diversidad del training set.

**Opción alternativa (2b):** Si el fix 2a no es suficiente, bajar `CLASSIFICATION_THRESHOLD` de 0.5 a 0.3 — pero esto puede aumentar falsos positivos.

**Verificación:** Re-clasificar CV 103386861 y confirmar que ahora pasa como "cv".

### Task 3: Wire OCR fallback into extraction API (P2 — BUG-003)

**Archivo:** `app/services/ocr_service.py` + `app/api/extraction.py`

**Qué:** Reemplazar `ocr_service.process_document()` con `ocr_service.extract_with_fallback()` en la API de extracción (`extraction.py:63`).

**Verificación:** CV 127944113 (DOCX con 0 texto) ahora debería extraer texto vía OCR.

### Task 4: Handle DOCX with no text (P3 — BUG-004)

**Archivo:** `app/utils/file_parser.py:58-61`

**Qué:** En `_parse_docx()`, si `len(text.strip()) == 0` después de extraer párrafos, caer a OCR via `pytesseract.image_to_string()` convirtiendo las páginas a imágenes.

**Nota:** Requiere que `python-pptx` o `pdf2image` esté disponible para convertir páginas DOCX. Alternativa más simple: instalar `libreoffice-writer` y usar `soffice --convert-to pdf` + PDF OCR.

**Verificación:** CV 127944113 extrae texto después del fix.

## Criterios de éxito

1. ✅ Todos los CVs .doc existentes producen texto legible con acentos correctos
2. ✅ CV 103386861 clasificado como "cv" y extraído correctamente
3. ✅ CV 127944113 extrae texto (vía OCR si es necesario)
4. ✅ Tests existentes siguen pasando (182+ tests)
5. ✅ Commit con todos los fixes

## Orden de ejecución

```
Task 1 (DOC accents) ──→ Task 2 (Classifier) ──→ Task 3 (OCR fallback) ──→ Task 4 (DOCX OCR)
       verify                 verify                    verify                   verify
         │                       │                        │                       │
         ▼                       ▼                        ▼                       ▼
      Commit                  Commit                   Commit                  Commit
```
