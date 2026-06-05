# Milestones

## v1.3 Bugfix Pipeline de Extracción (Shipped: 2026-05-19)

**Phases completed:** 3 phases (6–8), 3 plans, 3 tasks

**Key accomplishments:**

- Phase 6: Preprocessor proper noun casing fix — clean_text() uses IGNORECASE re.sub() instead of blanket .lower()
- Phase 7: Post-processing pipeline — gender inference, phone normalization, RUT formatting (only overrides "NO ENCONTRADO")
- Phase 8: LLM error resilience — JSON repair (fences, trailing commas, single quotes), two-phase retry (dynamic schema → EXTRACTION_SCHEMA fallback), TPM-aware bounded backoff, structured logging

---

## v1.2 Wizard Reordering (Shipped: 2026-05-17)

**Phases completed:** 1 phases, 1 plans, 0 tasks

**Key accomplishments:**

- (none recorded)

---

## v1.0 MVP (Shipped: 2026-05-15)

**Phases completed:** 1 phases, 4 plans, 12 tasks

**Key accomplishments:**

- Foundational Apple Design System established with Tailwind v4 theme and a persistent, frosted dual-navigation shell.
- Modular Apple-spec layout components (Tile, ProductCard, FrostedContainer) implemented with Tailwind v4.
- Extraction results view transformed into a high-end "Museum Gallery" using Apple-spec layout primitives and artifact-centric data mapping.
- Wizard flow overhauled as a "Product Configurator" using Apple's white utility cards and pill chip controls, creating a high-end setup experience.

---
