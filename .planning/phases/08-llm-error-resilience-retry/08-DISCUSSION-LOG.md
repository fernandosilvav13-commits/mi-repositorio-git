# Phase 8: LLM Error Resilience & Retry - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-17
**Phase:** 8-llm-error-resilience-retry
**Areas discussed:** JSON Repair Strategy, Retry Configuration, Schema Fallback Mechanics, Error UX, Logging & Monitoring

---

## JSON Repair Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Regex fixes only | Handle known patterns: trailing commas, unquoted keys, single quotes | ✓ |
| Use json-repair library | Robust repair via PyPI — handles truncation, missing brackets | |
| Both — regex first, library fallback | Fast regex fixes, fall back to json-repair | |

**User's choice:** Regex fixes only
**Notes:** No new dependencies wanted. Handles trailing commas and single quotes.

## Retry Configuration

| Option | Description | Selected |
|--------|-------------|----------|
| JSON parse failures only | Only retry when Gemini returns malformed JSON | ✓ |
| All errors including network | Retry on network timeouts, API errors, AND JSON parse failures | |

**User's choice:** JSON parse failures only

---

| Option | Description | Selected |
|--------|-------------|----------|
| Simple counter + delay | Count tokens consumed per window, add delay when approaching limits | ✓ |
| Use google-genai rate limiter | SDK's built-in rate limiting | |
| No TPM tracking | Rely on existing semaphore(5) and retry backoff | |

**User's choice:** Simple counter + delay

---

| Option | Description | Selected |
|--------|-------------|----------|
| Keep current: exponential + jitter | 2^attempt * 2 + random(0,1)s. Max ~8s for 3 attempts | ✓ |
| More conservative: linear + jitter | Fixed 3s + random(0,1)s between attempts | |

**User's choice:** Keep current exponential + jitter

## Schema Fallback Mechanics

| Option | Description | Selected |
|--------|-------------|----------|
| Same retries, then fallback | 3 retries with dynamic schema, on failure 2 more with EXTRACTION_SCHEMA | ✓ |
| Retry 2x dynamic → fallback → retry 2x fallback | 2 dynamic attempts, switch to EXTRACTION_SCHEMA for 2 more | |
| One dynamic → fallback immediately | Fastest but loses dynamic schema advantage | |

**User's choice:** Same retries, then fallback

---

| Option | Description | Selected |
|--------|-------------|----------|
| Return whatever we got | EXTRACTION_SCHEMA result better than None | ✓ |
| Return None if fallback used | Signal complete failure | |

**User's choice:** Return whatever we got

## Error UX

| Option | Description | Selected |
|--------|-------------|----------|
| No visual change | Retries happen server-side in <2s | ✓ |
| Show retry indicator | Small 'Retrying extraction...' message | |

**User's choice:** No visual change during retries

---

| Option | Description | Selected |
|--------|-------------|----------|
| Show extraction error | Clear error banner with retry suggestion | ✓ |
| Show partial data with warning | Display data with warning about missing fields | |
| Show generic error | Simple 'Extraction failed' | |

**User's choice:** Show extraction error with helpful message

---

| Option | Description | Selected |
|--------|-------------|----------|
| Show data with info note | Display data with subtle note about missing fields | ✓ |
| Show as normal | Don't differentiate full vs partial extraction | |

**User's choice:** Show data with info note on partial extraction

## Logging & Monitoring

| Option | Description | Selected |
|--------|-------------|----------|
| Structured logging | Log with structured data (attempt, error type, model) | ✓ |
| Minimal logging | Just print() statements | |

**User's choice:** Structured logging to file

---

| Option | Description | Selected |
|--------|-------------|----------|
| Retry warning + fallback + failure | WARNING-level: retries, fallback, failures only | ✓ |
| Log everything including success | Full observability but more noise | |

**User's choice:** Retry warning + fallback + failure

---

## the agent's Discretion

- Exact regex patterns for JSON repair (trailing comma and single-quote replacement)
- TPM counter implementation details (window size, delay formula)
- Error banner component implementation (frontend team builds per design system)
- Function naming for new helper functions in `llm_service.py`

## Deferred Ideas

None — discussion stayed within phase scope.
