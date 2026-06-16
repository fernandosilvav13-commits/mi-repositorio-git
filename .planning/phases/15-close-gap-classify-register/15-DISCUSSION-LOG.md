# Phase 15: Close Gap — Register /api/classify in main.py — Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-13
**Phase:** 15-Close Gap — Register /api/classify in main.py
**Areas discussed:** Two-pass activation strategy, Classify route, Preprocessing consistency, Path fix

---

## Two-Pass Activation Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Change default to True | Set use_two_pass=True as default. Simplest. Immediate effect. | ✓ |
| Add API-level parameter | Expose use_two_pass as query param. Gradual rollout but needs frontend changes. | |
| Separate endpoint | Dedicated POST /api/extraction/v2. Clean separation but doubles maintenance. | |

**User's choice:** Change default to True
**Notes:** User chose the simplest activation path. No preference for gradual rollout.

## Legacy Path Handling

| Option | Description | Selected |
|--------|-------------|----------|
| Keep as use_two_pass=False option | Preserve backward compat via parameter | ✓ |
| Remove single-pass entirely | Delete the legacy code path | |
| Deprecate with warning | Log deprecation warning, remove later | |

**User's choice:** Keep as use_two_pass=False option

## Classify Route Registration

| Option | Description | Selected |
|--------|-------------|----------|
| Standalone /api/classify prefix | Matches existing structure — independent classification | ✓ |
| Nest under /api/extraction | Group with extraction since it's a precursor step | |

**User's choice:** Standalone /api/classify prefix

## Preprocessing Consistency

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, add preprocessing | Match pipeline behavior — clean text before classifying | ✓ |
| No, keep raw | Simpler endpoint. Results may differ from pipeline. | |

**User's choice:** Yes, add preprocessing

## PromptResolver Path Fix

| Option | Description | Selected |
|--------|-------------|----------|
| Align to absolute path | Change extraction_pipeline.py to use Path(__file__) pattern | ✓ |
| Create shared constant | Put prompts path in shared config/settings module | |

**User's choice:** Align to absolute path pattern

---

## Agent's Discretion

- Import sorting, router tag naming, and error handling details for classify registration

## Deferred Ideas

- Full PaddleOCR 3.0 integration (OCR-01, OCR-02 gaps) — future phase
- Phase 9 missing VERIFICATION.md — separate process gap
- Nyquist VALIDATION.md creation — not addressed by this phase
