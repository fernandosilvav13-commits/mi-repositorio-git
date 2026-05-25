# Phase 12: Post-Processing Rules Expansion - Context

**Gathered:** 2026-05-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Expand pattern-based field inference beyond gender/phone/RUT with a registry of independently deployable rules, each validated in shadow mode before activation. Implements RULES-01 and RULES-02.

</domain>

<decisions>
## Implementation Decisions

### Fields to Infer
- **D-01:** Five new inference rules: NACIONALIDAD, FECHA_NACIMIENTO, ANIOS_EXPERIENCIA (years of experience), NIVEL_EDUCACION (education level), DOMINIO_EMAIL (email domain/type).
- **D-02:** Each rule is an independent Python class inheriting from a BaseRule abstract class.

### Rule Registry
- **D-03:** RuleRegistry singleton that holds all registered rules. Rules are discovered via a registry dict, not auto-discovery.
- **D-04:** Each rule has a unique name, description, and `evaluate(text: str, current_data: dict) -> str|None` method.

### Shadow Mode
- **D-05:** All new rules start in shadow mode (`enabled=False` by default).
- **D-06:** Shadow mode: rule runs and logs its output via logger.info() but does NOT override extraction fields.
- **D-07:** Each rule maintains a precision counter (hits/total). Precision >= 0.90 over 100+ evaluations triggers "ready for activation" status.
- **D-08:** Auto-activation requires manual review (developer checks precision log, sets `enabled=True`).

### Architecture
- **D-09:** Rules live in `backend/app/services/rules/` directory, one file per rule.
- **D-10:** RuleRegistry injected into post-processing pipeline (cv_processor.py) similar to how PreprocessingPipeline is used.
- **D-11:** Rules receive both the raw text and the current extraction data dict for context-aware inference.

</decisions>

<canonical_refs>
## Canonical References

### Existing Code
- backend/app/services/post_processing.py — Existing gender/phone/RUT rules (pattern to follow)
- backend/app/services/preprocessor.py — Singleton pattern

</canonical_refs>

---

*Phase: 12-Post-Processing Rules Expansion*
*Context gathered: 2026-05-24*
