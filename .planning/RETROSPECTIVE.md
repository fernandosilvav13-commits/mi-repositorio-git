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

*Last updated: 2026-05-15 after v1.0 milestone*
