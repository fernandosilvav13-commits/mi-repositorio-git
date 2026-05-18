# Security Audit Report

**Phase:** 04 — cross-reference-export
**Closed:** 2/4 | **Open:** 2/4
**ASVS Level:** 1

### Closed
| Threat ID | Category | Disposition | Evidence |
|-----------|----------|-------------|----------|
| T-04-00 | Information Disclosure | mitigate | `backend/tests/conftest.py` uses mock data without real PII |
| T-04-01 | Tampering | mitigate | `backend/app/services/crossref_service.py` uses `.strip().lower()` |

### Open
| Threat ID | Category | Mitigation Expected | Files Searched |
|-----------|----------|---------------------|----------------|
| T-04-02 | Information Disclosure | Entry present in SECURITY.md accepted risks log | SECURITY.md |
| T-04-03 | Denial of Service | Entry present in SECURITY.md accepted risks log | SECURITY.md |

## Accepted Risks Log
*(Document accepted risks here to close them in the next audit)*
