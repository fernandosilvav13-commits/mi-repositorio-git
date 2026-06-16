---
phase: "01"
phase_name: "frontend-apple-design"
status: "needs-fixes"
depth: "standard"
files_reviewed: 12
critical: 0
warning: 4
info: 4
total: 8
reviewed: "2026-05-15"
---

# Code Review: Phase 01 — frontend-apple-design

## Summary

**12 files reviewed** at **standard** depth. **8 findings** total (0 critical, 4 warnings, 4 info).

The Apple design system implementation is structurally sound with consistent theming, component architecture, and visual adherence to the museum gallery spec. Issues are primarily around Next.js best practices, CSS layering conflicts, and UX polish.

---

## Warnings

### WR-01: `<img>` tag instead of Next.js `Image` component

**File:** `frontend/src/components/apple/ProductCard.tsx:27`

**Issue:** Uses a native `<img>` tag which bypasses Next.js automatic image optimization, lazy loading, and responsive sizing.

```tsx
<img src={imageUrl} alt={title} className="..." />
```

**Recommendation:** Import and use `next/image`:

```tsx
import Image from "next/image";

<Image src={imageUrl} alt={title} className="..." width={400} height={400} />
```

**Severity:** Warning — impacts performance (no lazy loading), but ProductCard's `imageUrl` prop is optional and primarily uses the `FileText` icon placeholder in current usage.

---

### WR-02: Body style conflict between Apple theme and shadcn CSS layers

**File:** `frontend/src/app/globals.css:31-34`, `globals.css:149-151`

**Issue:** Two `@layer base` blocks set competing body styles:

1. Line 31-34: `body { @apply bg-white text-ink ... }`
2. Line 149-151: `body { @apply bg-background text-foreground }` (shadcn default)

The shadcn layer may override the Apple body colors depending on CSS cascade and layer ordering. This can cause flash of incorrect colors or theme inconsistencies.

**Recommendation:** Remove the shadcn body override at line 149-151, or unify into a single `@layer base` block:

```css
body {
  @apply bg-background text-foreground;
  font-family: var(--font-display);
}
```

And ensure `--background` / `--foreground` tokens are aliased to Apple colors (`--color-white`, `--color-ink`).

**Severity:** Warning — visual bug risk in production when shadcn components read `bg-background`.

---

### WR-03: `rounded-pill` is not a standard Tailwind v4 utility

**Files:**
- `frontend/src/components/layout/SubNav.tsx:28`
- `frontend/src/components/ui/button.tsx:7`

**Issue:** Uses `rounded-pill` class which does not exist in standard Tailwind CSS. The `globals.css` defines `--radius-pill: 9999px`, but Tailwind v4 does not auto-generate a `rounded-pill` utility from arbitrary theme tokens — it would need to be `rounded-[--radius-pill]` or `rounded-full`.

This class silently does nothing, so buttons fall back to default border-radius (likely `rounded-md` from shadcn or browser default).

**Recommendation:** Replace with `rounded-full`:

```tsx
// Before
"rounded-pill px-4 py-1.5"

// After
"rounded-full px-4 py-1.5"
```

**Severity:** Warning — visual defect. Buttons lose the Apple pill shape.

---

### WR-04: `alert()` for error handling across multiple pages

**Files:**
- `frontend/src/app/(gallery)/page.tsx:65`
- `frontend/src/app/extraction/page.tsx:66`
- `frontend/src/app/wizard/page.tsx:145,179,204`

**Issue:** Uses browser-native `alert()` for error display, which:
- Blocks the main thread
- Provides no user-friendly context
- Cannot be styled to match the Apple design system
- Does not persist for review

**Recommendation:** Implement a toast notification system or inline error banners using the existing shadcn `Toaster` or a lightweight alternative:

```tsx
// Instead of alert("Error: " + e.message)
toast.error("Extraction failed. Please check your files and try again.");
```

**Severity:** Warning — UX quality issue. Breaks the museum gallery immersion with a browser-native dialog.

---

## Info

### IF-01: Extensive `any` types throughout pages

**Files:**
- `frontend/src/app/(gallery)/page.tsx:33,53,58,95,106`
- `frontend/src/app/extraction/page.tsx:33,53,58,95,106`
- `frontend/src/app/wizard/page.tsx:61,68,74,78,82,163,172,190`

**Issue:** Widespread use of `any` type for API responses, template data, rules, and crossref data. This bypasses TypeScript type checking and makes refactoring error-prone.

**Recommendation:** Define proper interfaces for API response types:

```tsx
interface Template {
  id: string;
  name: string;
  columns: Array<{ name: string; data_type: string }>;
}
```

**Severity:** Info — no runtime impact, but reduces TypeScript's value.

---

### IF-02: Near-duplicate code between gallery and extraction pages

**Files:**
- `frontend/src/app/(gallery)/page.tsx`
- `frontend/src/app/extraction/page.tsx`

**Issue:** Both pages share ~90% identical code (file selection, extraction logic, controls bar, artifact grid). Only differences are the back button and import of `ArrowLeft` / `Link`.

**Recommendation:** Extract shared logic into a `useGallery` hook or shared component:

```tsx
// frontend/src/hooks/useGallery.ts
export function useGallery() { ... }
```

Then both pages become thin wrappers.

**Severity:** Info — maintainability concern. Future changes must be duplicated across both files.

---

### IF-03: Inline `PillChip` component in wizard

**File:** `frontend/src/app/wizard/page.tsx:24-47`

**Issue:** The `PillChip` button component is defined locally inside the wizard page file. It's used 7+ times across the wizard steps and could be reused elsewhere (e.g., gallery controls).

**Recommendation:** Extract to `src/components/apple/PillChip.tsx` as a reusable Apple component:

```tsx
// frontend/src/components/apple/PillChip.tsx
export function PillChip({ selected, onClick, children }: PillChipProps) { ... }
```

**Severity:** Info — design pattern consistency.

---

### IF-04: Native `<select>` instead of shadcn `Select` component

**File:** `frontend/src/app/wizard/page.tsx:342-348`

**Issue:** The crossref field mapping step uses a native HTML `<select>` with `appearance-none`, while the rest of the codebase uses the shadcn `Select` component (see gallery page line 91-101). This creates visual inconsistency.

**Recommendation:** Replace with shadcn `Select`:

```tsx
<Select value={crossrefMatchColumn} onValueChange={setCrossrefMatchColumn}>
  <SelectTrigger><SelectValue placeholder="Select field" /></SelectTrigger>
  <SelectContent>
    {crossrefData?.columns?.map((c) => (
      <SelectItem key={c} value={c}>{c}</SelectItem>
    ))}
  </SelectContent>
</Select>
```

**Severity:** Info — visual inconsistency.

---

## Files Reviewed

1. `frontend/src/app/globals.css`
2. `frontend/src/app/layout.tsx`
3. `frontend/src/components/layout/GlobalNav.tsx`
4. `frontend/src/components/layout/SubNav.tsx`
5. `frontend/src/components/ui/button.tsx`
6. `frontend/src/components/apple/Tile.tsx`
7. `frontend/src/components/apple/ProductCard.tsx`
8. `frontend/src/components/apple/FrostedContainer.tsx`
9. `frontend/src/app/(gallery)/page.tsx`
10. `frontend/src/app/extraction/page.tsx`
11. `frontend/src/components/apple/ConfiguratorCard.tsx`
12. `frontend/src/app/wizard/page.tsx`

---

## Next Steps

1. **Fix WR-03** (`rounded-pill` → `rounded-full`) — quickest fix, visible visual impact
2. **Fix WR-02** (body style conflict) — prevents future theming bugs
3. **Fix WR-01** (use Next.js `Image`) — when ProductCard gains image support
4. **Fix WR-04** (replace `alert()`) — depends on toast infrastructure
5. Address IF items as time permits

Run `/gsd-code-review 01 --fix` to auto-apply fixes, or fix manually.
