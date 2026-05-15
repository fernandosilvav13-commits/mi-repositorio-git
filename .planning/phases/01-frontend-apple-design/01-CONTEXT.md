# Phase 01: Frontend Overhaul (Apple Design) - Context

**Gathered:** 2026-05-14
**Status:** Ready for planning
**Source:** PRD Express Path (apple/DESIGN.md)

<domain>
## Phase Boundary

Transform the existing "Proyecto-Prueba" frontend into a photography-first, "museum gallery" interface following Apple's design language. This involves a complete visual overhaul of the UI components, layout, and styling.

</domain>

<decisions>
## Implementation Decisions

### Colors & Atmosphere
- **Accent**: Use Action Blue (#0066cc) for all interactive elements (links, pill CTAs).
- **Surfaces**: Alternate between Pure White (#ffffff), Parchment (#f5f5f7), and Near-Black (#272729) tiles.
- **Pure Black**: Reserve for global-nav and true void areas.
- **No Gradients**: Eliminate all decorative CSS gradients; rely on photography for atmosphere.
- **Shadows**: Exactly one drop-shadow (`rgba(0, 0, 0, 0.22) 3px 5px 30px`) reserved ONLY for product imagery.

### Typography
- **Font Stack**: Primary `SF Pro Display` (macOS) or `Inter` (others) with negative letter-spacing for headlines.
- **Body**: Default at 17px / 400 weight / 1.47 line-height.
- **Headlines**: Weight 600 (not 700). Negative letter-spacing (`-0.28` to `-0.374px`) for that "Apple tight" feel.
- **Weights**: Ladder is 300 / 400 / 600 / 700. No weight 500.

### Layout & Spacing
- **Rhythm**: Edge-to-edge full-bleed tiles. The color change IS the divider.
- **Whitespace**: High density of air; section vertical padding at 80px.
- **Radius**: 
  - `none` (0px) for tiles.
  - `sm` (8px) for dark utility buttons.
  - `lg` (18px) for utility cards.
  - `pill` (9999px) for primary actions.

### Components
- **Global Nav**: Thin (44px) black bar.
- **Sub-Nav**: Frosted glass (backdrop-blur) pinned below global nav (52px).
- **Buttons**: All buttons use `transform: scale(0.95)` on active/press state.
- **Cards**: White utility cards with 1px hairline border and 18px radius.

### the agent's Discretion
- Mapping specific "CV Extraction" data to "Product" representations (e.g., CV files as museum artifacts).
- Implementation of the responsive collapsing strategy for the existing dashboard.
- Transition effects between the alternating tiles.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Design System
- `apple/DESIGN.md` — Full design specification (colors, type, components)

### Current Frontend State
- `frontend/src/app/globals.css` — Root styles to be overhauled
- `frontend/src/app/layout.tsx` — Main layout structure (Global Nav, Sub-Nav)
- `frontend/package.json` — Dependencies (Next.js, Tailwind v4, shadcn)

</canonical_refs>

<specifics>
## Specific Ideas

- The "Wizard" flow should feel like an Apple "Shop" or "Configure" experience.
- Extraction results should be displayed in a museum-like gallery view (Product Tiles).

</specifics>

<deferred>
## Deferred Ideas

- Dark mode counterparts for store/accessories cards (not in current scope).
- Complex form validation animations (out of initial visual overhaul scope).

</deferred>

---

*Phase: 01-frontend-apple-design*
*Context gathered: 2026-05-14 via PRD Express Path*
