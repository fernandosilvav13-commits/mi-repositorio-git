# Requirements — v1.5 Consolidación de Extracción

## Overview

Stabilize and polish the extraction pipeline. Phase 16 (llm-provider) implemented a multi-provider LLM abstraction but was never UAT-tested or committed. This milestone closes that gap, deduplicates parallel extraction logic, cleans up legacy config, validates with real documents, and refines post-processing.

## Scoped Requirements

### R-01: Phase 16 UAT signoff

| ID | Requirement | Phase | Verification |
|----|-------------|-------|-------------|
| R-01.1 | All 6 UAT tests pass: code compiles, provider auto-detection, config loading, factory, section detector, model resolution | 17 | UAT report |
| R-01.2 | All Phase 16 changes committed to main with coherent commit messages | 17 | git log |
| R-01.3 | HANDOFF.json archived and removed from untracked files | 17 | file check |

### R-02: Extraction logic deduplication

| ID | Requirement | Phase | Verification |
|----|-------------|-------|-------------|
| R-02.1 | `batch_process.py` uses `llm_service.extract_fields()` instead of its own hardcoded prompt and schema | 18 | code review |
| R-02.2 | No duplicate extraction schemas between batch_process and service layer | 18 | grep check |
| R-02.3 | Batch process output matches service-layer extraction output for same input | 18 | comparison test |

### R-03: Config cleanup

| ID | Requirement | Phase | Verification |
|----|-------------|-------|-------------|
| R-03.1 | Legacy `gemini_model_*` fields removed from Settings | 19 | code review |
| R-03.2 | Unused `llm_provider = "auto"` field removed from Settings | 19 | code review |
| R-03.3 | No references to removed config fields in any service or endpoint | 19 | grep check |

### R-04: Real-document validation

| ID | Requirement | Phase | Verification |
|----|-------------|-------|-------------|
| R-04.1 | Pipeline processes 5+ real CVs through the wizard without errors | 20 | session log |
| R-04.2 | No "NO ENCONTRADO" for basic fields (name, RUT, phone, email) on well-formed CVs | 20 | extraction output |
| R-04.3 | Two-pass mode (classify → extract) correctly handles CV and non-CV documents | 20 | classification results |
| R-04.4 | Any bugs discovered during testing are fixed and verified | 20 | issue log |

### R-05: Post-processing refinement

| ID | Requirement | Phase | Verification |
|----|-------------|-------|-------------|
| R-05.1 | Gender inference accuracy reviewed and improved if < 90% on test CVs | 21 | accuracy check |
| R-05.2 | Phone normalization handles Chilean (+56) and international formats | 21 | unit test |
| R-05.3 | RUT formatting consistent across all output paths | 21 | unit test |
| R-05.4 | Shadow rules (nationality, DOB, experience, education, email) evaluated for promotion to active | 21 | precision report |

## Out of Scope

- PaddleOCR 3.0 integration
- Tesseract + PaddleOCR fusion
- PP-StructureV3 layout analysis
- Field-level confidence scoring UI
- Frontend provider selection UI
- Streaming LLM responses
- Any new extraction features beyond stabilization
