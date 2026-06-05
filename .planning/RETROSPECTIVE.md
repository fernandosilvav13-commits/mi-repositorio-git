# Retrospective

## Milestone: v1.0 — MVP

**Shipped:** 2026-05-15
**Phases:** 1 | **Plans:** 4

### What Was Built

- Apple Design System foundations (colors, typography, radii) with Tailwind v4
- Dual-navigation shell: 44px Global Nav + 52px Frosted Sub-Nav
- Modular layout components: Tile, ProductCard, FrostedContainer
- Extraction results as Museum Gallery with artifact-centric data mapping
- Wizard redesigned as Product Configurator with utility cards and pill chips

### What Worked

- Single phase with 4 parallel waves was efficient for a pure frontend overhaul
- Apple design spec was well-defined upfront, reducing ambiguity
- UAT verified all 8 tests passed with 0 issues

### What Was Inefficient

- Back-and-forth on Tailwind v4 `rounded-pill` vs `rounded-full` — resolved by checking actual utility names
- Initial `alert()` usage replaced late with sonner toasts — should have been done from start

### Patterns Established

- Apple Design System tokens centralized in `globals.css` @theme block
- Dual-navigation shell as default for all pages
- Museum Gallery artifact presentation for extraction data
- Pill-shaped buttons and selection chips for all interactive elements

### Key Lessons

- Define all radius tokens upfront in the design spec to avoid confusion
- Use sonner for all error/toast UI from the start — don't fall back to `alert()`
- Single-command launch scripts (start.sh) improve iteration speed

### Cost Observations

- **Duration:** ~1 day for full phase (4 plans, 4 waves)
- **Commits:** 24 commits for milestone phase
- **Notable:** High efficiency due to well-defined SPEC and design reference

---

---

## Milestone: v1.2 — Wizard Reordering

**Shipped:** 2026-05-17
**Phases:** 1 | **Plans:** 1

### What Was Built

- Reordered Wizard steps: Template Selection now happens before Cross-Reference
- D-01 warning guard on template change when crossref mapping exists
- D-02 same-template re-selection preserves mapping, updates columns
- D-03 clears matchKeys/outputColumns on confirmed template switch

### What Worked

- Phase context was already gathered (05-CONTEXT.md), making execution straightforward
- Single file change (wizard/page.tsx), 10 edits across 6 locations — precise and contained
- Plan was thorough with exact code references and verification steps

### What Was Inefficient

- Phase 05 was planned but never executed in the original session — had to come back and apply the changes
- SUMMARY.md was pre-written with "TODO" for commits (planning artifact, not execution artifact)

### Patterns Established

- `window.confirm` for simple warning dialogs (keeps code minimal for agent's discretion items)
- D-01/D-03 guard pattern: warn first, clear downstream state, then navigate

### Key Lessons

- Always verify that planned changes were actually applied to code, not just documented in SUMMARY.md
- Pre-written SUMMARY.md files should include a clear execution/commit section to distinguish planning from execution

### Cost Observations

- **Duration:** ~15min for execution (phase was fully planned, just needed code application + commit)
- **Commits:** 4 commits for milestone (Phase 05, ROADMAP update, archive, requirements removal)

---

*Last updated: 2026-05-17 after v1.2 milestone*
