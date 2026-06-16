# Phase 10: Advanced Preprocessing - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-21
**Phase:** 10-advanced-preprocessing
**Areas discussed:** Section Detection Strategy, Noise Filtering Criteria, Layout Normalization Strategy, Pipeline Architecture

---

## Section Detection Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Extend regex patterns | More SECTIONS entries with careful patterns. Matches existing codebase pattern. | |
| ML classifier per line | TF-IDF + SVM to classify each line as section-header vs content | |
| LLM-guided detection | Ask Gemini to identify sections before extraction | ✓ |

**User's choice:** LLM-guided detection

| Option | Description | Selected |
|--------|-------------|----------|
| Markup in text | Gemini adds [SECTION: Education] markers inline | |
| Boundary-only JSON | Returns section boundaries as JSON | ✓ |
| Structured format | Reformat entire CV into structured sections | |

**User's choice:** Boundary-only JSON

| Option | Description | Selected |
|--------|-------------|----------|
| Fallback to regex | Graceful degradation to regex if LLM fails | |
| Return as single section | Treat whole doc as one section | |
| Skip preprocessing for that doc | Pass raw text directly to extraction | ✓ |

**User's choice:** Skip preprocessing for that doc

| Option | Description | Selected |
|--------|-------------|----------|
| Separate call before extraction | Dedicated LLM call for section detection | ✓ |
| Part of extraction prompt | Same prompt handles both detection and extraction | |

**User's choice:** Separate call before extraction

---

## Noise Filtering Criteria

| Option | Description | Selected |
|--------|-------------|----------|
| Heuristic rules | Line-position heuristics, pattern matching | |
| Include in section detection LLM call | Combined JSON with sections and noise | |
| Dedicated noise detection LLM call | Separate call just for noise | ✓ |

**User's choice:** Dedicated noise detection LLM call

| Option | Description | Selected |
|--------|-------------|----------|
| Keep separate, but batch | One call returns both sections and noise | ✓ |
| Keep fully separate | 3 calls total | |
| Hybrid approach | LLM for sections, heuristics for noise | |

**User's choice:** Keep separate, but batch (2 calls total: batched detection + extraction)

**Selected noise types:** Page headers/running heads, Page numbers, Footers/disclaimers, Document metadata artifacts

---

## Layout Normalization Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Preserve paragraph breaks | Collapse internal whitespace but keep double-newlines | |
| Collapse everything | All whitespace → single space (current behavior) | |
| Intelligent structure | Preserve paragraph breaks + section markers from LLM | ✓ |

**User's choice:** Intelligent structure

| Option | Description | Selected |
|--------|-------------|----------|
| Normalize to consistent format | Convert all bullet variants to standard marker | ✓ |
| Remove bullets, keep text | Strip bullets, keep text | |
| Keep as-is | Preserve original bullet characters | |

**User's choice:** Normalize to consistent format

---

## Pipeline Architecture

| Option | Description | Selected |
|--------|-------------|----------|
| Single service, composed methods | AdvancedPreprocessor class with detect_sections(), filter_noise(), normalize_layout() | |
| Multi-stage pipeline | Separate classes: SectionDetector, NoiseFilter, LayoutNormalizer | ✓ |
| Layered approach | Pluggable steps within single Preprocessor class | |

**User's choice:** Multi-stage pipeline

| Option | Description | Selected |
|--------|-------------|----------|
| Replace existing preprocess_cv_text() | Same integration point, better internals | |
| New pipeline in cv_processor.py | Step in CVProcessor.process() | |
| Separate service, injected into extraction | Injectable dependency | ✓ |

**User's choice:** Separate service, injected into extraction

| Option | Description | Selected |
|--------|-------------|----------|
| Extend existing test_preprocessor.py | Add to existing test file | |
| New test file per stage | test_section_detector.py, test_noise_filter.py, etc. | ✓ |
| Single new test file for pipeline | test_advanced_preprocessor.py | |

**User's choice:** New test file per stage

---

## the agent's Discretion

- Specific LLM prompt templates for the batched section+noise detection call
- Bullet point normalization implementation details
- Paragraph break threshold
- Error handling strategy for LLM failures in the preprocessing pipeline

## Deferred Ideas

None
