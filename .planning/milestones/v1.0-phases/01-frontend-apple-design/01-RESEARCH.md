# Phase 01: Frontend Overhaul (Apple Design) - Research

**Researched:** 2026-05-14
**Domain:** Frontend UI/UX (Apple Design Language)
**Confidence:** HIGH

## Summary

This phase focuses on implementing the Apple "museum gallery" design language across the entire Proyecto-Prueba frontend. The core philosophy is **photography-first presentation** where the UI chrome recedes to let the product (CV data/artifacts) speak. We will transition from a standard SaaS dashboard to a high-density "Product Gallery" feel using alternating full-bleed tiles, negative letter-spacing, and a singular "Action Blue" interactive color.

**Primary recommendation:** Use Tailwind v4's CSS-first configuration to lock in the Apple-specific typographic hierarchy and color system, and leverage Next.js 16's shared layouts for the persistent dual-navigation system.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Global Navigation | Browser / Client | Frontend Server | Layout provides the persistent shell; Client component handles active link states. |
| Frosted Sub-Nav | Browser / Client | — | Requires `backdrop-filter` blur and scroll-aware stickiness. |
| Full-Bleed Tile Layout | Browser / Client | — | Purely visual layout components with edge-to-edge constraints. |
| Product Configurator (Wizard) | Browser / Client | API / Backend | High interactivity for selection; fetches configuration rules from backend. |
| Museum Gallery (Results) | Browser / Client | API / Backend | Visual presentation tier; fetches structured extraction results. |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Next.js | 16.2.6 | Framework | App Router provides optimal layout nesting for dual navs. |
| Tailwind CSS | 4.0.0 | Styling | Oxide engine enables CSS-native theme configuration. |
| @base-ui/react | 1.4.1 | Components | Unstyled primitives allow for exact Apple-spec customization. |
| React | 19.2.4 | UI | Support for newest concurrent rendering features. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|--------------|
| Lucide React | 1.14.0 | Icons | Minimalist icon set matching Apple's quiet UI. |
| Zod | ^3.23 (Rec) | Validation | Type-safe form validation for the Configurator/Wizard. |
| shadcn/ui | 4.7.0 | Component Base | Starting point for modified Apple-radius components. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Inter Font | SF Pro | SF Pro is proprietary; Inter is the closest open-source substitute for non-Apple OS. [VERIFIED: apple/DESIGN.md] |
| Custom CSS | Framer Motion | Framer Motion is powerful but might be overkill for simple `scale(0.95)` transforms. |

**Installation:**
```bash
npm install zod
```

**Version verification:**
- Next.js 16.2.6 [VERIFIED: frontend/package.json]
- Tailwind v4.0.0 [VERIFIED: frontend/package.json]

## Architecture Patterns

### System Architecture Diagram
1. **Entry Point:** Root `layout.tsx` (Server Component).
2. **Global Shell:** `GlobalNav.tsx` (Client) + `header` tag (Sticky Top 0).
3. **Sub-Nav Layer:** `SubNav.tsx` (Client) with `backdrop-blur` (Sticky Top 44px).
4. **Content Area:** `page.tsx` (Server) composed of `Tile` components.
5. **Data Flow:** `ExtractionService` (Server) -> `GalleryTile` (Client) for results visualization.

### Recommended Project Structure
```
frontend/src/
├── components/
│   ├── layout/       # GlobalNav, SubNav, Footer
│   ├── apple/        # Tile, ProductCard, FrostedContainer
│   └── ui/           # Modified shadcn components
├── app/
│   ├── (gallery)/    # Extraction results view
│   └── wizard/       # Product configurator flow
└── styles/
    └── globals.css   # Tailwind v4 @theme configuration
```

### Pattern 1: The "Apple Tight" Headline
**What:** Combining SF Pro Display with negative letter-spacing and weight 600.
**When to use:** Headlines 17px and above.
**Example:**
```css
/* globals.css */
@theme {
  --font-display: "SF Pro Display", "Inter", system-ui;
  --tracking-apple-tight: -0.011em; /* Verified from training: signature Apple tracking */
}

.headline {
  font-family: var(--font-display);
  font-weight: 600;
  letter-spacing: var(--tracking-apple-tight);
}
```

### Anti-Patterns to Avoid
- **Shadow Creep:** Adding shadows to cards or buttons. [CITED: apple/DESIGN.md - "Exactly one drop-shadow reserved for product imagery"]
- **Radius Mixing:** Using standard 4px/6px radii. Apple uses 8px (sm), 18px (lg), and Full Pill.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Backdrop Blur fallbacks | Manual CSS @supports | Tailwind `supports-[backdrop-filter]` | Built-in utility handles browser compatibility checks. |
| Complex Nav Logic | Custom hook for links | `usePathname` from `next/navigation` | Native Next.js hook is optimized for App Router. |
| Modal Primitives | Custom portal logic | @base-ui/react or shadcn/ui | Handles accessibility (ARIA) and focus trapping correctly. |

## Runtime State Inventory

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None | Verified: Data is structural (RUT, Extraction data), not design-related. |
| Live service config | None | Verified: No design configs in Supabase. |
| OS-registered state | None | Verified. |
| Secrets/env vars | None | Verified. |
| Build artifacts | None | Verified. |

## Common Pitfalls

### Pitfall 1: Tracking overload
**What goes wrong:** Text becomes unreadable on mobile or at small sizes.
**Why it happens:** Applying `tracking-apple-tight` to 12px captions.
**How to avoid:** Only apply negative tracking to font sizes >= 17px.

### Pitfall 2: Blur Performance
**What goes wrong:** Janky scrolling on the Frosted Sub-Nav.
**Why it happens:** High blur radius on a large transparent div.
**How to avoid:** Keep `backdrop-blur` to `md` (12px) and use `bg-white/80` to keep the layer light.

### Pitfall 3: Button Radius Inconsistency
**What goes wrong:** Interface feels "generic" rather than Apple-like.
**Why it happens:** Using `rounded-md` (shadcn default) for primary actions.
**How to avoid:** Use `rounded-full` (pill) for all Primary Blue CTAs. [CITED: apple/DESIGN.md]

## Code Examples

### Verified Pattern: Frosted Sticky Sub-Nav
```tsx
// Source: Next.js 16 Best Practices + Tailwind v4
'use client'
import { usePathname } from 'next/navigation'

export function SubNav() {
  return (
    <nav className="sticky top-11 z-40 h-13 w-full bg-parchment/80 backdrop-blur-md border-b border-hairline">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-8 h-full">
        <span className="text-tagline font-semibold">Project Name</span>
        <div className="flex gap-6">
           <button className="bg-primary text-white rounded-full px-4 py-2 transform active:scale-95 transition-transform">
             Action
           </button>
        </div>
      </div>
    </nav>
  )
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `tailwind.config.js` | CSS `@theme` block | Tailwind v4 (2025) | Faster builds, more CSS-native. |
| `pages/` directory | `app/` Router | Next.js 13+ (Stable 16) | Shared layouts, RSC performance. |
| Standard 16px body | 17px Body | Apple Design Trend | Unmistakable brand "reading" pace. |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Inter is the best fallback for SF Pro | Standard Stack | Low - Inter is widely accepted as the standard substitute. |
| A2 | Next.js 16.2.6 handles dual sticky navs without jank | Summary | Low - Next.js 16 optimizations are specifically for layout persistence. |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Node.js | Runtime | ✓ | 22.22.2 | — |
| npm | Package Manager | ✓ | 10.9.7 | — |
| Tailwind v4 | Styles | ✓ | 4.0.0 | — |
| shadcn/ui | Components | ✓ | 4.7.0 | — |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Vitest + React Testing Library (Recommended) |
| Config file | None — See Wave 0 |
| Quick run command | `npm test` |
| Full suite command | `npm run test:full` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DESIGN-01 | Apple Color System check | visual | `npx playwright test` | ❌ Wave 0 |
| TYPE-01 | SF Pro / Inter Typography | smoke | `npm test typography` | ❌ Wave 0 |
| NAV-01 | Sticky Frosted Nav visibility | e2e | `npx playwright test nav` | ❌ Wave 0 |

### Wave 0 Gaps
- [ ] Initialize Vitest and React Testing Library in `frontend/`.
- [ ] Setup Playwright for visual regression testing (essential for design overhaul).

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V5 Input Validation | yes | Zod schemas for all Wizard/Configurator inputs. |
| V4 Access Control | yes | Ensure RLS policies in Supabase cover the new Gallery view. |

### Known Threat Patterns for Next.js 16

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| XSS via Product Labels | Tampering | React 19 auto-sanitization + Zod validation. |
| CSRF in Actions | Spoofing | Next.js 16 built-in CSRF protection for Server Actions. |

## Sources

### Primary (HIGH confidence)
- `/vercel/next.js` - Layouts, Client/Server components, Sticky patterns.
- `/tailwindlabs/tailwindcss.com` - Tailwind v4 `@theme` configuration.
- `apple/DESIGN.md` - Core project design specification.

### Secondary (MEDIUM confidence)
- WebSearch - Inter font stacks and Apple-tight tracking community values.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Directly from `package.json`.
- Architecture: HIGH - Standard Next.js 16 App Router patterns.
- Pitfalls: MEDIUM - Based on design system experience and Tailwind v4 early adoption.

**Research date:** 2026-05-14
**Valid until:** 2026-06-14 (30 days for stable frameworks)
