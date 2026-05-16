# Requirements: CicloAI

**Defined:** 2026-05-15
**Core Value:** Extract structured CV data with a beautiful, intuitive interface and export-ready results.

## v1.1 Requirements

Requirements for v1.1 Cross-Reference Integration. Each maps to roadmap phases.

### Crossref Page Redesign

- [x] **CRSS-01**: User can upload and manage cross-reference files in an Apple-designed page with Tile, FrostedContainer, and PillChip components
- [x] **CRSS-02**: User can view uploaded cross-reference files in a clean artifact-based list with match status indicators

### Wizard Integration

- [ ] **WIZ-01**: User can upload a cross-reference file as a step in the Wizard flow
- [ ] **WIZ-02**: User can configure column mapping between extraction results and cross-reference fields in the Wizard
- [x] **WIZ-03**: User can preview matched vs unmatched results within the Wizard before finalizing export

### Export with Cross-Reference

- [x] **EXP-01**: Exported Excel includes cross-referenced data columns from matched rows
- [x] **EXP-02**: Unmatched rows are visually flagged in the exported output

## v1.2 Requirements

Requirements for v1.2 Wizard Reordering.

### Wizard Reordering

- [ ] **WIZ-04**: Change the Wizard steps sequence to: Upload -> Template -> CrossRef -> Rules -> Extract -> Export
- [ ] **WIZ-05**: Ensure Wizard back/next navigation handles the new state dependencies correctly

## v2 Requirements

Deferred to future release.

### Authentication & Multi-user

- **AUTH-01**: User can log in with email and password
- **AUTH-02**: User sessions persist across browser refresh
- **AUTH-03**: Extraction results are scoped per user

### Backend Refinement

- **PERF-01**: Optimize data fetching and state management

## Out of Scope

| Feature | Reason |
|---------|--------|
| Mobile app | Web-first PWA approach, confirmed in v1.0 |
| Real-time collaboration | Single-user workflow |
| OAuth/SSO login | Not needed for current deployment |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CRSS-01 | Phase 02 | Complete |
| CRSS-02 | Phase 02 | Complete |
| WIZ-01 | Phase 03 | Pending |
| WIZ-02 | Phase 03 | Pending |
| WIZ-03 | Phase 03 | Complete |
| EXP-01 | Phase 04 | Complete |
| EXP-02 | Phase 04 | Complete |
| WIZ-04 | Phase 05 | Pending |
| WIZ-05 | Phase 05 | Pending |

**Coverage:**
- v1.1 requirements: 7 total
- v1.2 requirements: 2 total
- Mapped to phases: 9 ✓
- Unmapped: 0

---

*Requirements defined: 2026-05-15*
*Last updated: 2026-05-15 after initial definition*
