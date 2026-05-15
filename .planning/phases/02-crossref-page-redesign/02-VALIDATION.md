---
phase: 02
slug: crossref-page-redesign
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-15
---

# Phase 02 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | vitest (frontend) / pytest (backend) |
| **Config file** | Wave 0 installs |
| **Quick run command** | `npm run test -- --run` (frontend) / `pytest -x` (backend) |
| **Full suite command** | `npm run test:ci` (frontend) / `pytest` (backend) |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `npm run test -- --run` (frontend) or `pytest -x` (backend)
- **After every plan wave:** Run full suite for both
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | CRSS-01 | — | N/A | unit | `npm run test -- --run` | ❌ W0 | ⬜ pending |
| 02-01-02 | 01 | 1 | CRSS-01 | — | N/A | unit | `npm run test -- --run` | ❌ W0 | ⬜ pending |
| 02-02-01 | 02 | 2 | CRSS-02 | — | N/A | unit | `npm run test -- --run` | ❌ W0 | ⬜ pending |
| 02-02-02 | 02 | 2 | CRSS-02 | — | N/A | unit | `npm run test -- --run` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `frontend/vitest.config.ts` — vitest configuration
- [ ] `frontend/src/__tests__/` — test directory structure
- [ ] `frontend/src/__tests__/setup.ts` — test setup with testing-library
- [ ] `npm install -D vitest @testing-library/react @testing-library/jest-dom` — dependencies

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Upload-to-list animation | CRSS-01 | Visual animation cannot be automated in unit tests | Open page, upload file, observe animation from upload zone into table |
| Frosted glass table appearance | CRSS-02 | Visual styling requires visual inspection | Open page with files, verify frosted glass rows, backdrop-blur, hairline borders |
| PillChip color accuracy | CRSS-02 | Color rendering requires visual check | Verify green (#34c759), amber (#ff9500), blue (#007aff) match spec |

---

## Validation Sign-Off

- [ ] All tasks have automated verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
