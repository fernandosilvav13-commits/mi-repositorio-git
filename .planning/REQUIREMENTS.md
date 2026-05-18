# Requirements: CicloAI

**Defined:** 2026-05-18
**Core Value:** Extract structured CV data with a beautiful, intuitive interface and export-ready results.

## v1.3 Requirements

Requirements for v1.3 bugfix milestone. Each maps to roadmap phases.

### Post-Processing

- [ ] **POST-01**: CVProcessor.process() applies gender inference via infer_gender() on extracted NOMBRES
- [ ] **POST-02**: CVProcessor.process() normalizes phone numbers via normalize_phone()
- [ ] **POST-03**: CVProcessor.process() formats RUT via RUTFormatter
- [ ] **POST-04**: Post-processing only overrides LLM output when field is "NO ENCONTRADO" or empty

### Preprocessor

- [ ] **PREP-01**: clean_text() preserves proper noun casing instead of blanket .lower()

### LLM Robustness

- [ ] **LLM-01**: llm_service handles malformed JSON gracefully (logs warning, retries)
- [ ] **LLM-02**: llm_service strips markdown/code fences before JSON parse

### Retry Strategy

- [ ] **RETR-01**: On dynamic schema failure, attempt fallback to EXTRACTION_SCHEMA
- [ ] **RETR-02**: Backoff waits are bounded and respect TPM limits

## Future Requirements

(Deferred — not in current scope)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Frontend UI changes | Purely backend bugs this milestone |
| New extraction fields | Bugfix only, no schema expansion |
| Performance optimization | Only if related to bugs above |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| POST-01 | — | Pending |
| POST-02 | — | Pending |
| POST-03 | — | Pending |
| POST-04 | — | Pending |
| PREP-01 | — | Pending |
| LLM-01 | — | Pending |
| LLM-02 | — | Pending |
| RETR-01 | — | Pending |
| RETR-02 | — | Pending |

**Coverage:**
- v1.3 requirements: 9 total
- Mapped to phases: 0
- Unmapped: 9 ⚠️

---
*Requirements defined: 2026-05-18*
*Last updated: 2026-05-18 after initial definition*
