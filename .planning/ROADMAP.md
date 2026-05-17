# Roadmap — CicloAI

## Milestones

- ✅ **v1.0 MVP** — Phase 1 (shipped 2026-05-15)
- 🚧 **v1.1 Cross-Reference Integration** — Phases 2–4 (in progress)
- 📅 **v1.2 Wizard Reordering** — Phase 05 (planned)

## Phases

<details>
<summary>✅ v1.0 MVP (Phase 1) — SHIPPED 2026-05-15</summary>

### Phase 01: Frontend Overhaul (Apple Design)
**Goal**: The full Apple Design System with dual navigation, museum gallery components, and product configurator wizard
**Plans**: 4 plans

Plans:
- [x] 01-01: Foundation Setup (globals.css, Tailwind v4, theme tokens)
- [x] 01-02: Navigation Shell (44px global nav + 52px frosted sub-nav)
- [x] 01-03: Museum Gallery (extraction results as artifact-based view)
- [x] 01-04: Product Configurator (Wizard flow as Apple configurator)

</details>

### 🚧 v1.1 Cross-Reference Integration (In Progress)

**Milestone Goal:** Polish and integrate the cross-reference data matching feature into the Apple design system and Wizard flow.

- [x] **Phase 02: Crossref Page Redesign** — Redesign the cross-reference page with Apple Design System components (Tile, FrostedContainer, PillChip) (completed 2026-05-15)
- [x] **Phase 03: Wizard Cross-Reference Integration** — Integrate cross-reference upload, column mapping, and preview into the Wizard flow (completed 2026-05-15)
- [x] **Phase 04: Cross-Reference Export** — Exported Excel includes cross-referenced columns with unmatched rows flagged (in progress) (completed 2026-05-15)

### 📅 v1.2 Wizard Reordering (Planned)

**Milestone Goal:** Fix the cross-reference mapping issue by reordering the Wizard steps so Template Selection happens before Cross-Reference.

- [x] **Phase 05: Wizard Reordering** — Reorder Wizard steps and add warning guard

## Phase Details

### Phase 02: Crossref Page Redesign
**Goal**: Users can upload and manage cross-reference files through an Apple-designed page with artifact-based file list and match indicators
**Depends on**: Phase 01
**Requirements**: CRSS-01, CRSS-02
**Success Criteria** (what must be TRUE):
  1. User can navigate to the cross-reference page and see it styled with Apple Design System components (Tile, FrostedContainer, PillChip)
  2. User can upload a cross-reference file (PDF/CSV/PPT/DOCX) from the redesigned page
  3. User can see all uploaded cross-reference files in a clean artifact-based list view
  4. Each file in the list shows a match status indicator (matched, unmatched, processing)
**Plans**: 3 plans

Plans:
- [x] 02-01-PLAN.md — Add status column to crossref_files + return status in API responses
- [x] 02-02-PLAN.md — Extend PillChip with status variant + add uploadWithProgress helper
- [x] 02-03-PLAN.md — Redesign crossref page with Apple Design System components
**UI hint**: yes

### Phase 03: Wizard Cross-Reference Integration
**Goal**: Users can include cross-reference data in their extraction workflow through dedicated Wizard steps (upload, column mapping, preview)
**Depends on**: Phase 02
**Requirements**: WIZ-01, WIZ-02, WIZ-03
**Success Criteria** (what must be TRUE):
   1. User can upload a cross-reference file as a dedicated step within the Wizard flow
   2. User can configure column mapping between extraction result fields and cross-reference fields within the Wizard
   3. User can preview matched vs unmatched results within the Wizard before finalizing export
   4. The Wizard cross-reference step connects to the existing backend CrossrefService for merging and semantic matching
**Plans**: 3 plans
**UI hint**: yes

Plans:
- [x] 03-01-PLAN.md — Crossref upload step enhancement (upload/selection/error states in Wizard)
- [x] 03-02-PLAN.md — Column mapping UI (compound match keys, auto-suggest, output picker)
- [x] 03-03-PLAN.md — Match preview in review step (summary bar, expandable tables)

### Phase 04: Cross-Reference Export
**Goal**: Exported Excel files include matched cross-reference data with clear unmatched row indicators
**Depends on**: Phase 03
**Requirements**: EXP-01, EXP-02
**Success Criteria** (what must be TRUE):
  1. When exporting after cross-reference, the Excel file includes columns from the matched reference data
  2. Rows that did not match any cross-reference data are visually flagged in the exported output
  3. The export provides a clear indication of which columns originated from cross-reference data
**Plans**: 4 plans

Plans:
- [x] 04-00-PLAN.md — Setup testing infrastructure and failing tests
- [x] 04-01-PLAN.md — Refactor cross-reference merge logic (compound keys, O(1) tuples)
- [ ] 04-02-PLAN.md — Excel visual styling (row highlighting, header prefixes)
- [ ] 04-03-PLAN.md — Export API orchestration and integration
**UI hint**: yes

### Phase 05: Wizard Reordering
**Goal**: Fix the cross-reference mapping issue by reordering the Wizard steps so Template Selection happens before Cross-Reference.
**Depends on**: Phase 04
**Requirements**: WIZ-04, WIZ-05
**Success Criteria** (what must be TRUE):
   1. User sees "Template Selection" before "Cross-Reference" in the Wizard flow.
   2. In the "Cross-Reference" step, the dropdown for "Select template field" correctly displays the columns from the previously selected template.
**Plans**: 1 plan

Plans:
- [x] 05-01-PLAN.md — Reorder Wizard steps + navigation targets + D-01/D-03 guard
**UI hint**: yes

Plans:
- [ ] 05-01-PLAN.md — Reorder Wizard steps + navigation targets + D-01/D-03 guard

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Frontend Overhaul (Apple Design) | v1.0 | 4/4 | Complete | 2026-05-14 |
| 2. Crossref Page Redesign | v1.1 | 3/3 | Complete | 2026-05-15 |
| 3. Wizard Cross-Reference Integration | v1.1 | 3/3 | Complete | 2026-05-15 |
| 4. Cross-Reference Export | v1.1 | 4/4 | Complete | 2026-05-15 |
| 5. Wizard Reordering | v1.2 | 1/1 | Complete | 2026-05-17 |
