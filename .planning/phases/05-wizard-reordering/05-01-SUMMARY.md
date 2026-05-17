---
phase: 05-wizard-reordering
plan: 01
type: execute
subsystem: frontend
tags: [wizard, navigation, reorder]
key-files:
  - frontend/src/app/wizard/page.tsx
metrics:
  files_changed: 1
  edits_made: 10
  lines_changed: 40
---

# Phase 05-01 Summary: Wizard Reordering

## Commits

- `feat: reorder wizard steps (template before crossref) + D-01/D-03 guard`
  - 1 file changed, ~10 edits across 6 locations in `wizard/page.tsx`
  - STEPS array reordered, all 6 hardcoded navigation targets updated
  - D-01: `window.confirm` warning on template change with existing crossref mapping
  - D-02: Same-template re-selection preserves mapping, updates templateColumns
  - D-03: `setMatchKeys([])` + `setOutputColumns([])` on confirmed template switch

## What Changed

### `frontend/src/app/wizard/page.tsx` — 6 locations, ~10 edits

| Change | Location | Before | After |
|--------|----------|--------|-------|
| STEPS array order | line 27-35 | crossref → template | template → crossref |
| goNext() crossref bypass | line 116 | `setCurrentStep("template")` | `setCurrentStep("rules")` |
| goNext() template auto-advance | line 128 | `setCurrentStep("rules")` | `setCurrentStep("crossref")` |
| handleCreateTemplate target | line 260 | `setCurrentStep("rules")` | `setCurrentStep("crossref")` |
| Template "Seleccionar" onClick | line 679 | `"rules"` + no guards | D-01/D-02/D-03 + `"crossref"` |
| CrossRef "No, omitir" onClick | line 521 | `setCurrentStep("template")` | `setCurrentStep("rules")` |

## Decisions Implemented

| Decision | Implementation |
|----------|---------------|
| **D-01** — Warning on template change | `window.confirm` when `matchKeys.length > 0` before changing template |
| **D-02** — Auto-advance on template select | "Seleccionar" immediately navigates to crossref step |
| **D-03** — Clear mapping on confirmed change | `setMatchKeys([])` + `setOutputColumns([])` before advancing |

## Verification Results

### Automated Checks (passed)

- ✅ STEPS array: `template` before `crossref`
- ✅ 0 remaining `setCurrentStep("template")` calls
- ✅ 2x `setCurrentStep("rules")` (bypass + omitir)
- ✅ 4x `setCurrentStep("crossref")` (goNext + handleCreate + 2x Seleccionar)
- ✅ D-01: `window.confirm` present
- ✅ D-03: `setMatchKeys([])` + `setOutputColumns([])` present
- ✅ TypeScript: no new errors (`npx tsc --noEmit`)

## UAT Scenarios (Manual)

Open `http://localhost:3000/wizard` and verify:

| # | Scenario | Expected |
|---|----------|----------|
| 1 | Step order | Upload (Inicio) → Template (Estructura) → CrossRef (Referencia) → Rules → Extract → Export → Review |
| 2 | Template auto-advance | Select a template → advances to CrossRef step |
| 3 | "No, omitir" bypass | Click "No, omitir" on CrossRef → advances to Rules step |
| 4 | Same-template re-select | Select template A, go back, select A again → no warning, advances to CrossRef |
| 5 | Different-template with mapping | Map crossref, go back, select different template → warning appears; cancel → stays; confirm → clears mapping |

## Deviations

None.
