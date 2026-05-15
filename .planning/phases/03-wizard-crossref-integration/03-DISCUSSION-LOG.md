# Phase 03 Discussion Log

**Phase:** 03 — Wizard Cross-Reference Integration
**Date:** 2026-05-15
**Status:** Complete (all gray areas resolved)

## Overview

Discussed 5 gray areas for integrating cross-reference matching into the Wizard flow. All decisions documented in `03-CONTEXT.md`.

## Gray Areas Discussed

### 1. Preview UX for Match Results

**Question:** How should matched/unmatched results be displayed in preview?

| Option | Verdict |
|--------|---------|
| Summary with drill-down | ✅ **Selected** |
| Full table always visible | ❌ |
| Just counts (no drill-down) | ❌ |

**Question:** How should rows be displayed?

| Option | Verdict |
|--------|---------|
| Two separate sections (Matched / Unmatched) | ✅ **Selected** |
| Single merged table with status column | ❌ |

**Question:** What determines a match?

| Option | Verdict |
|--------|---------|
| Any extraction column chosen by user | ✅ **Selected** |
| Fixed primary key (RUT only) | ❌ |

### 2. Column Mapping UX

**Question:** How should output columns be selected?

| Option | Verdict |
|--------|---------|
| Smart suggestion with override | ✅ **Selected** |
| Manual from dropdown | ❌ |

**Question:** How should match key be configured?

| Option | Verdict |
|--------|---------|
| Single shared field with auto-map | ✅ **Selected** |
| Two separate dropdowns | ❌ |

**Question:** Should compound matching be supported?

| Option | Verdict |
|--------|---------|
| Multiple match keys | ✅ **Selected** |
| Single match key only | ❌ |

### 3. Wizard Flow Position

**Question:** Where in the Wizard flow should crossref integration live?

| Option | Verdict |
|--------|---------|
| Keep at step 2 (current position) | ✅ **Selected** |
| Move after extraction | ❌ |
| Both positions | ❌ |

**Question:** When should column mapping happen?

| Option | Verdict |
|--------|---------|
| At step 2 with file selection | ✅ **Selected** |
| After extraction, before preview | ❌ |

### 4. Semantic vs Exact Matching

**Question:** What matching strategy should be used?

| Option | Verdict |
|--------|---------|
| Always semantic (Gemini AI) | ✅ **Selected** |
| Auto: exact first, semantic fallback | ❌ |
| User choice | ❌ |

**Question:** When should matching run?

| Option | Verdict |
|--------|---------|
| During extraction | ✅ **Selected** |
| During Wizard (before preview) | ❌ |
| On demand / lazy | ❌ |

### 5. Match Preview Timing

**Question:** Where should the user see match results?

| Option | Verdict |
|--------|---------|
| Part of review step | ✅ **Selected** |
| Separate preview step | ❌ |
| Inline in export step | ❌ |

**Question:** What happens when user changes mapping?

| Option | Verdict |
|--------|---------|
| Re-run matching on change (auto) | ✅ **Selected** |
| Manual re-match button required | ❌ |
