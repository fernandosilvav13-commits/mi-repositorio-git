# Phase 01: Frontend Overhaul (Apple Design) - Pattern Map

**Mapped:** 2026-05-14
**Files analyzed:** 9
**Analogs found:** 7 / 9

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `frontend/src/app/globals.css` | config | N/A | (Self) | exact |
| `frontend/src/app/layout.tsx` | layout | request-response | (Self) | exact |
| `frontend/src/components/layout/GlobalNav.tsx` | component | request-response | `frontend/src/app/layout.tsx` | role-match |
| `frontend/src/components/layout/SubNav.tsx` | component | request-response | (New Pattern) | N/A |
| `frontend/src/components/apple/Tile.tsx` | component | request-response | `frontend/src/components/ui/card.tsx` | role-match |
| `frontend/src/components/apple/ProductCard.tsx` | component | request-response | `frontend/src/components/ui/card.tsx` | role-match |
| `frontend/src/components/apple/FrostedContainer.tsx` | component | request-response | (New Pattern) | N/A |
| `frontend/src/app/wizard/page.tsx` | page | request-response | `frontend/src/app/wizard/page.tsx` | exact |
| `frontend/src/app/(gallery)/page.tsx` | page | CRUD | `frontend/src/app/extraction/page.tsx` | role-match |

## Pattern Assignments

### `frontend/src/app/globals.css` (config)

**Analog:** `frontend/src/app/globals.css` (Current)

**Tailwind v4 Theme Pattern** (to be overhauled):
```css
/* Old Luxury Pattern */
@theme inline {
  --font-heading: var(--font-heading), serif;
  --font-body: var(--font-body), sans-serif;
  --color-luxury-bg: #FDFCFB;
  --radius-luxury: 2.5rem;
}

/* New Apple Pattern (Referenced from RESEARCH.md) */
@theme {
  --font-display: "SF Pro Display", "Inter", system-ui;
  --tracking-apple-tight: -0.011em;
  --color-action-blue: #0066cc;
  --color-parchment: #f5f5f7;
  --color-near-black: #272729;
  --radius-sm: 8px;
  --radius-lg: 18px;
  --radius-pill: 9999px;
  --shadow-product: rgba(0, 0, 0, 0.22) 3px 5px 30px;
}
```

---

### `frontend/src/components/layout/GlobalNav.tsx` (component, request-response)

**Analog:** `frontend/src/app/layout.tsx` (contains current body shell)

**Layout structure to extract** (lines 30-34):
```tsx
<body className="min-h-screen bg-[#FDFCFB] text-[#1A1A1A] font-body selection:bg-[#1A1A1A] selection:text-white">
  {children}
</body>
```

**New Pattern (Global Nav 44px):**
```tsx
export function GlobalNav() {
  return (
    <header className="sticky top-0 z-50 h-[44px] w-full bg-black text-white px-8 flex items-center">
      {/* Apple-style minimalist nav */}
    </header>
  )
}
```

---

### `frontend/src/components/apple/Tile.tsx` (component, request-response)

**Analog:** `frontend/src/components/ui/card.tsx`

**Card structure pattern** (lines 7-18):
```typescript
function Card({
  className,
  size = "default",
  ...props
}: React.ComponentProps<"div"> & { size?: "default" | "sm" }) {
  return (
    <div
      data-slot="card"
      className={cn(
        "group/card flex flex-col gap-4 overflow-hidden rounded-xl bg-card py-4",
        className
      )}
      {...props}
    />
  )
}
```

**New Tile Pattern:**
- **Full-bleed:** No container padding.
- **Radius:** 0px (none).
- **Division:** Color change (Pure White vs Parchment vs Near-Black).

---

### `frontend/src/app/wizard/page.tsx` (page, request-response)

**Analog:** `frontend/src/app/wizard/page.tsx` (Self)

**Step Logic pattern** (lines 40-75):
```typescript
const [currentStep, setCurrentStep] = useState<Step>("upload");
const [subStep, setSubStep] = useState(0);

const goNext = () => {
  // Logic for step transitions
};
```

**Overhaul Direction:**
- Retain state logic for CV ingestion/extraction.
- Replace UI with Apple-style "Product Configurator" (White cards, 18px radius, pill buttons).

---

### `frontend/src/app/(gallery)/page.tsx` (page, CRUD)

**Analog:** `frontend/src/app/extraction/page.tsx`

**Data Fetching pattern** (lines 50-55):
```typescript
useEffect(() => {
  api.templates.list().then(setTemplates).catch(() => {});
}, []);
```

**Result Rendering pattern** (lines 200-240):
```typescript
{results.map((r, i) => (
  <TableRow key={i} ...>
    <TableCell>{r.filename}</TableCell>
    {/* ... data cells ... */}
  </TableRow>
))}
```

**New Gallery Pattern:**
- Replace Table with **Tile Gallery**.
- Each extraction result is a "Product Tile" (Photography-first or clean artifact representation).

---

## Shared Patterns

### Typography (Apple Tight)
**Source:** `01-RESEARCH.md`
**Apply to:** All headlines and body text
```css
.headline {
  font-family: var(--font-display);
  font-weight: 600;
  letter-spacing: -0.011em; /* Negative letter-spacing for >17px */
  line-height: 1.1;
}
.body {
  font-size: 17px;
  font-weight: 400;
  line-height: 1.47;
}
```

### Interactive Scale
**Source:** `01-CONTEXT.md`
**Apply to:** All buttons and interactive cards
```css
.interactive-action:active {
  transform: scale(0.95);
  transition: transform 0.2s ease-out;
}
```

### Frosted Surface
**Source:** `01-RESEARCH.md`
**Apply to:** `SubNav` and overlays
```tsx
<div className="bg-white/80 backdrop-blur-md border-b border-white/20">
  {/* Content */}
</div>
```

## No Analog Found

Files with no close match in the codebase:

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `SubNav.tsx` | component | request-response | Existing app has no secondary sticky navigation layer. |
| `FrostedContainer.tsx` | component | request-response | Backdrop blur patterns are new to this phase. |

## Metadata

**Analog search scope:** `frontend/src/components/ui/`, `frontend/src/app/`
**Files scanned:** 15
**Pattern extraction date:** 2026-05-14
