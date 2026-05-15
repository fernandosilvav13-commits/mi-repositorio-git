---
phase: 04
slug: cross-reference-export
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-05-15
---

# Phase 04 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (backend) |
| **Config file** | Wave 0 installs |
| **Quick run command** | `pytest backend/tests/` |
| **Full suite command** | `pytest backend/` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest -x` on the relevant test file
- **After every plan wave:** Run `pytest backend/tests/`
- **Before /gsd-verify-work:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 04-00-01 | 00 | 0 | N/A | — | N/A | config | `pytest --version` | ✅ | ⬜ pending |
| 04-00-02 | 00 | 0 | EXP-01, EXP-02 | — | N/A | test-init | `pytest backend/tests/test_crossref_merge.py` | ✅ | ⬜ pending |
| 04-00-03 | 00 | 0 | EXP-01, EXP-02 | — | N/A | test-init | `pytest backend/tests/test_export_api.py` | ✅ | ⬜ pending |
| 04-01-01 | 01 | 1 | EXP-01 | T-04-01 | Key Norm | unit | `pytest backend/tests/test_crossref_merge.py -k test_schema` | ✅ | ⬜ pending |
| 04-01-02 | 01 | 1 | EXP-01 | T-04-01 | Key Norm | unit | `pytest backend/tests/test_crossref_merge.py -k test_merge_data` | ✅ | ⬜ pending |
| 04-02-01 | 02 | 1 | EXP-02 | — | N/A | unit | `pytest backend/tests/test_excel_styling.py` | ✅ | ⬜ pending |
| 04-03-01 | 03 | 2 | EXP-01, EXP-02 | — | N/A | integration | `pytest backend/tests/test_export_api.py` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `backend/tests/test_crossref_merge.py` — unit tests for compound key merging
- [x] `backend/tests/test_excel_styling.py` — unit tests for Excel row highlighting
- [x] `backend/tests/test_export_api.py` — integration tests for export API
- [x] `pip install pytest pytest-asyncio` — ensure test framework is available

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Excel row color | EXP-02 | Visual inspection of .xlsx file required | Export data with unmatched rows, open Excel, verify amber/yellow fill on unmatched rows |
| [REF] column prefixing | EXP-01 | Header visual check | Export data, verify cross-reference columns are prefixed with [REF] |

---

## Validation Sign-Off

- [x] All tasks have automated verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
