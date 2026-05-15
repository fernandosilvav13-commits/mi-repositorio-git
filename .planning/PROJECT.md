# CicloAI

## What This Is

A CV data extraction system with Apple-inspired frontend design, multi-step ingestion wizard, and Excel export. Extracts structured data from CVs using AI (Gemini), applies conditional rules, and exports to formatted Excel files.

## Core Value

Extract structured CV data with a beautiful, intuitive interface and export-ready results.

## Requirements

### Validated

- ✓ Apple Color System (Action Blue, Parchment, Near-Black) — v1.0
- ✓ SF Pro / Inter Typographic Hierarchy — v1.0
- ✓ Full-Bleed Tile Layout components — v1.0
- ✓ Global Nav and Frosted Sub-Nav — v1.0
- ✓ Wizard flow as a Product Configurator — v1.0
- ✓ Extraction Results as a Museum Gallery — v1.0

### Active

- [ ] Backend Integration Refinement — optimize data fetching and state management
- [ ] Cross-reference data from external files (PDF/CSV/PPT/DOCX)

### Out of Scope

- Mobile app — web-first PWA approach
- Real-time collaboration — single-user workflow

## Context

Shipped v1.0 with ~42,654 LOC (TSX/TS/CSS/Python).
Tech stack: Next.js 16, FastAPI, Supabase, Tailwind v4, Gemini AI.
Frontend redesigned with Apple "museum gallery" design language.

## Key Decisions

| Decision | Outcome | Status |
| -------- | ------- | ------ |
| Apple Design System with Tailwind v4 | Consistent, elegant UI | ✓ Good |
| Dual-navigation shell (44px + 52px) | Clear information hierarchy | ✓ Good |
| Museum Gallery artifact presentation | Intuitive data visualization | ✓ Good |
| Pill-shaped buttons and pill chips | Cohesive Apple aesthetic | ✓ Good |

## Constraints

- All new UI components must follow Apple design tokens in `globals.css`
- RUT consolidation occurs server-side during export, not in Supabase
- Single-command launch via `./start.sh`

---

*Last updated: 2026-05-15 after v1.0 milestone*
