# Phase 7: Post-Processing Pipeline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-18
**Phase:** 07-post-processing-pipeline
**Areas discussed:** Post-processing location, Override behavior per field, RUT output format, Name capitalization (D-05)

---

## Post-processing Location

| Option | Description | Selected |
|--------|-------------|----------|
| Inside CVProcessor.process() | Wire infer_gender, normalize_phone, RUTFormatter into existing process() method | ✓ |
| New method on CVProcessor | Create CVProcessor._post_process(data) to keep process() clean | |
| New PostProcessor service | A new class/function in a new file, keeping cv_processor.py unchanged | |

**User's choice:** Inside CVProcessor.process()
**Notes:** The imports already exist in cv_processor.py, just need to call them.

---

## Override Behavior Per Field

| Option | Description | Selected |
|--------|-------------|----------|
| Per-field check | Check each field individually. Only override when NO ENCONTRADO/empty | ✓ |
| Only if ALL fields missing | Only run post-processing if none of the target fields were found | |
| Always normalize phones and RUT | Always normalize phone/RUT format, gender override only when missing | |

**User's choice:** Per-field check
**Notes:** POST-04 applied at individual field granularity.

---

## RUT Output Format

| Option | Description | Selected |
|--------|-------------|----------|
| Con puntos y guion | 12.345.678-9 — Chilean standard format | ✓ |
| Solo guion | 12345678-9 — compact, no dots | |
| Sin formato | 123456789 — digits only | |

**User's choice:** Con puntos y guion (12.345.678-9)
**Notes:** This is already RUTFormatter's default format.

---

## Name Capitalization (D-05)

| Option | Description | Selected |
|--------|-------------|----------|
| Include in this phase | Add title-casing for NOMBRES/APELLIDOS as part of post-processing | ✓ |
| Defer to future phase | Keep this phase focused on POST-01..04 only | |
| LLM should handle it | Phase 06 fix already preserves casing; let Gemini handle name casing | |

**User's choice:** Include in this phase
**Notes:** Name capitalization was deferred from Phase 06 (D-05). Now included as part of the post-processing pipeline.

---

## the agent's Discretion

- Phone extraction scope: normalize_phone() on LLM-extracted phones is mandatory; extract_phone_from_text() on raw text is optional
- Name capitalization function name and implementation approach
- Experience enrichment — keep existing behavior unchanged

## Deferred Ideas

None — discussion stayed within phase scope.
