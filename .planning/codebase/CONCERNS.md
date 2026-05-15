# Codebase Concerns

**Analysis Date:** 2026-05-15

## Tech Debt

**Duplicate Service Architecture:**
- Issue: There are two parallel service directories: `backend/services/` and `backend/app/services/`. The root directory seems to be an older or alternative version used by `batch_process.py`, while `app/services/` is used by the FastAPI app.
- Files: `backend/services/`, `backend/app/services/`
- Impact: Extreme confusion for developers, risk of bug fixes only being applied to one version, and increased bundle/package size.
- Fix approach: Consolidate all services into `backend/app/services/` and update `batch_process.py` to use the app-level services.

**Hardcoded Local Paths:**
- Issue: Multiple files contain hardcoded absolute paths or rely on specific local directory structures that won't exist in other environments.
- Files: `backend/batch_process.py`, `backend/app/utils/file_parser.py`, `backend/app/services/cv_processor.py`
- Impact: The application fails to run in CI/CD or different developer machines without manual path modification.
- Fix approach: Use environment variables via `BaseSettings` for all external paths and use relative paths derived from the project root.

**God Component in Frontend:**
- Issue: The Wizard flow is implemented as a single massive component that manages state for 7 different complex steps.
- Files: `frontend/src/app/wizard/page.tsx`
- Impact: Very high cognitive load, difficult to test, and prone to "state spaghetti" bugs.
- Fix approach: Split the wizard into sub-components for each step and use a state management library (like Zustand) or a custom hook to manage the multi-step state.

## Known Bugs

**Fragile .doc Parsing:**
- Issue: The `.doc` (not docx) parsing logic uses a mix of regex on HTML and custom OLE stream reading which is extremely prone to failure with different Word versions.
- Files: `backend/app/utils/file_parser.py`
- Impact: High failure rate for legacy documents.
- Fix approach: Use a robust library like `python-magic` to detect file types and a specialized converter like `pandoc` or `libreoffice` (headless) for legacy formats.

**PDF OCR Fallback Crash:**
- Issue: If PDF text extraction fails, it attempts to call `_ocr_image` with the PDF path. PIL's `Image.open` cannot open PDF files without additional plugins/helpers.
- Files: `backend/app/utils/file_parser.py`
- Impact: Application crash when processing image-only PDFs.
- Fix approach: Use `pdf2image` to convert PDF pages to images before passing them to the OCR engine.

## Security Considerations

**Authentication Bypass:**
- Risk: Authentication is completely bypassed if `ENVIRONMENT` is set to `development`. If a production environment is accidentally misconfigured or if this flag is toggled, the entire system is exposed.
- Files: `backend/app/core/auth.py`
- Impact: Potential data breach.
- Fix approach: Implement a proper mock authentication provider for development that still requires a "mock" token, or use local development credentials that match the production flow.

**Path Traversal / LFI:**
- Risk: The extraction endpoints accept a list of `file_paths` directly from the client and check for existence using `os.path.exists`.
- Files: `backend/app/api/extraction.py`
- Impact: A malicious user could probe for the existence of files on the server or trigger OCR/Processing on sensitive system files.
- Fix approach: Never accept absolute paths from the client. Use internal IDs or strictly validated relative paths within the `uploads/` directory.

## Performance Bottlenecks

**Blocking Async Event Loop:**
- Problem: Synchronous, CPU-bound (OCR) and I/O-bound (LLM, Excel generation) tasks are called directly inside `async` endpoints.
- Files: `backend/app/api/extraction.py`, `backend/app/services/llm_service.py`, `backend/app/services/ocr_service.py`
- Cause: Using synchronous libraries (`tesserocr`, `google-genai` synchronous client) without offloading to a thread pool or task queue.
- Improvement path: Use `run_in_executor` to offload blocking tasks or move to a background task worker like Celery or FastAPI BackgroundTasks.

## Fragile Areas

**Silent Failures in Services:**
- Files: `backend/app/services/cv_processor.py`, `backend/app/api/extraction.py`
- Why fragile: Methods return empty dicts `{}` or `continue` inside loops on error without proper logging or exception propagation.
- Safe modification: Implement a custom Exception hierarchy and use a proper logging framework (e.g., `loguru` or standard `logging`).
- Test coverage: Non-existent.

## Test Coverage Gaps

**Zero Project Tests:**
- What's not tested: Everything. No unit tests for services, no integration tests for API endpoints, no E2E tests for the frontend.
- Files: Entire codebase.
- Risk: High regression rate, difficult to refactor the "duplicate services" or "god component" without breaking features.
- Priority: High

---

*Concerns audit: 2026-05-15*
