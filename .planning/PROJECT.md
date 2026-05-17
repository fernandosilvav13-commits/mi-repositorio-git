# CicloAI

## Current State

**Shipped:** v1.2 Wizard Reordering (2026-05-17)

The Wizard flow now executes Template Selection before Cross-Reference, fixing the crossref mapping auto-suggestion issue. All navigation targets updated, with D-01 warning guard on template change and D-03 mapping invalidation on confirmed switch.

## Next Milestone

## What This Is

A CV data extraction system with Apple-inspired frontend design, multi-step ingestion wizard, and Excel export. Extracts structured data from CVs using AI (Gemini), applies conditional rules, and exports to formatted Excel files.

## Core Value

Extract structured CV data with a beautiful, intuitive interface and export-ready results.

## Requirements

### Validated

- ✓ Cross-reference data from external files (PDF/CSV/PPT/DOCX) — Phase 04
- ✓ Apple Color System (Action Blue, Parchment, Near-Black) — v1.0
- ✓ SF Pro / Inter Typographic Hierarchy — v1.0
- ✓ Full-Bleed Tile Layout components — v1.0
- ✓ Global Nav and Frosted Sub-Nav — v1.0
- ✓ Wizard flow as a Product Configurator — v1.0
- ✓ Extraction Results as a Museum Gallery — v1.0
- ✓ Wizard steps reordered: Upload → Template → CrossRef → Rules → Extract → Export → Review — v1.2
- ✓ Warning guard on template change with crossref mapping (D-01/D-03) — v1.2

### Active

- [ ] Backend Integration Refinement — optimize data fetching and state management

### Out of Scope

- Mobile app — web-first PWA approach
- Real-time collaboration — single-user workflow

## Context

Shipped v1.0–v1.2 with ~42,654 LOC (TSX/TS/CSS/Python).
Tech stack: Next.js 16, FastAPI, Supabase, Tailwind v4, Gemini AI.
Frontend redesigned with Apple "museum gallery" design language.
v1.2: Wizard steps reordered, template-before-crossref with guard on crossref mapping loss.

## Key Decisions

| Decision | Outcome | Status |
| -------- | ------- | ------ |
| Tuple-based composite keys for matching | O(1) matching performance with multiple columns | ✓ Good |
| pytest for backend testing | Better async support and cleaner syntax | ✓ Good |
| Apple Design System with Tailwind v4 | Consistent, elegant UI | ✓ Good |
| Dual-navigation shell (44px + 52px) | Clear information hierarchy | ✓ Good |
| Museum Gallery artifact presentation | Intuitive data visualization | ✓ Good |
| Pill-shaped buttons and pill chips | Cohesive Apple aesthetic | ✓ Good |
| D-01: Warning on template change | Prevents accidental crossref mapping loss | ✓ Good |
| D-02: Same-template auto-advance | Faster flow when re-selecting same template | ✓ Good |
| D-03: Clear mapping on template switch | Prevents ghost state in crossref step | ✓ Good |

## Constraints

- All new UI components must follow Apple design tokens in `globals.css`
- RUT consolidation occurs server-side during export, not in Supabase
- Single-command launch via `./start.sh`

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-17 after v1.2 milestone*
