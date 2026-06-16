# Phase 01: Frontend Overhaul (Apple Design) - UI Spec

## 1. Objective
Implement the Apple "museum gallery" design language. UI should recede, making the CV extraction data (the "product") the center of attention.

## 2. Core Styles (from apple/DESIGN.md)

### Colors
- **Action Blue**: #0066cc (Primary accent for all interactive elements)
- **Pure White**: #ffffff (Main canvas)
- **Parchment**: #f5f5f7 (Alternating tiles, footer)
- **Near-Black**: #272729 (Dark product tiles)
- **Ink**: #1d1d1f (Headlines and body)

### Typography
- **Headlines**: SF Pro Display 600, negative letter-spacing (-0.28px to -0.374px).
- **Body**: SF Pro Text 400, 17px, line-height 1.47.
- **Micro-interaction**: `transform: scale(0.95)` on all button active states.

## 3. Component Overhaul

### Navbars
- **Global Nav**: 44px height, pure black, white nav-links (12px).
- **Sub-Nav**: 52px height, frosted glass (Parchment 80% + backdrop-blur), tagline 21px/600 on left, primary CTA on right.

### Product Tiles (Full-Bleed)
- Use for main landing and extraction results.
- Vertical padding: 80px.
- Center-aligned typography stack.
- Single soft drop-shadow on product images.

### Wizard Flow
- Styled as a "Product Configurator".
- Use white utility cards (18px radius, 1px hairline border).
- Pill-shaped option chips.

## 4. Layout
- Section rhythm: White Hero -> Dark Tile -> Parchment Utility -> Dark Tile -> Footer.
- No borders or gradients between sections.

## 5. Mobile
- Transition to 1-column stack at 834px.
- Global nav collapses to hamburger.
- Hero typography scales down to 28px on small phones.
