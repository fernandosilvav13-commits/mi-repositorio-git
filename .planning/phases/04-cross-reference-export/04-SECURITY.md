---
status: secure
phase: 04-cross-reference-export
threats_open: 0
threats_total: 4
started: 2026-05-15T20:35:00Z
updated: 2026-05-15T20:35:00Z
---

# Phase 04 Security Review

## Threat Register

| Threat ID | Category | Component | Disposition | Status | Evidence |
|-----------|----------|-----------|-------------|--------|----------|
| T-04-00 | Information Disclosure | backend/tests/ | mitigate | CLOSED | `backend/tests/conftest.py` uses mock data without real PII |
| T-04-01 | Tampering | CrossrefService.merge_data | mitigate | CLOSED | `backend/app/services/crossref_service.py` uses `.strip().lower()` in `merge_data` |
| T-04-02 | Information Disclosure | ExcelService.generate | accept | CLOSED | Visual flagging reveals match status, which is the intended feature. Accepted risk. |
| T-04-03 | Denial of Service | api/export.py | accept | CLOSED | Processing large files is single-user context; acceptable for current scope. Accepted risk. |

## Accepted Risks

- **T-04-02 (Information Disclosure):** Visual flagging reveals match status, which is the intended feature.
- **T-04-03 (Denial of Service):** Processing large files is single-user context; acceptable for current scope.

## Audit Trail

### Security Audit 2026-05-15
| Metric | Count |
|--------|-------|
| Threats found | 4 |
| Closed | 4 |
| Open | 0 |
