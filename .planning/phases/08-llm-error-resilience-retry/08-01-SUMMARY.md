---
phase: 08-llm-error-resilience-retry
plan: 01
type: execute
subsystem: backend
tags: [llm, resilience, retry, json-repair]
key-files:
  - backend/app/services/llm_service.py
  - backend/app/services/cv_extractor.py
metrics:
  files_changed: 2
  lines_added: 93
  lines_removed: 43
---

# Phase 08-01 Summary: LLM Error Resilience & Retry

## Commits

- `feat(phase-08): LLM error resilience with JSON repair, retry, schema fallback`
  - 2 files changed, +93/-43

## What Changed

### backend/app/services/llm_service.py

| Change | Detail |
|--------|--------|
| _repair_json() | Strips markdown fences, removes trailing commas, replaces single quotes |
| _track_tpm() | Sliding window token counter with adaptive delay at 600K TPM limit |
| extract_fields() | Now accepts fallback_schema + fallback_model. Retry with backoff + schema fallback |
| Logger | Uses setup_logger("llm_service") for structured WARNING logging |

### backend/app/services/cv_extractor.py

- Removed retry loop from extract_cv_data() -- moved to llm_service
- Calls extract_fields() with fallback_schema=EXTRACTION_SCHEMA
- Semaphore, cache, preprocessing stay in cv_extractor

## Decisions Implemented

| Decision | Detail |
|----------|--------|
| D-01 | Regex-only JSON repair (trailing commas, single quotes) |
| D-02 | Retry on parse failure only, not network errors |
| D-05 | Exponential backoff 2^n * 2 + random(0,1) |
| D-06 | Simple TPM token counter with sliding window |
| D-07 | Semaphore(5) stays in cv_extractor |
| D-08 | 3 attempts dynamic schema, then 2 with EXTRACTION_SCHEMA |
| D-13 | Structured WARNING logging for retries, fallback, failures |
| D-14 | Uses existing setup_logger from app.utils.logger |
