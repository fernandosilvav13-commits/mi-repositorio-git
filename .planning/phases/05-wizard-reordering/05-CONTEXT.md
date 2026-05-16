# Phase 05: Wizard Reordering - Context

**Gathered:** 2026-05-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix the cross-reference mapping issue by reordering the Wizard steps so Template Selection happens before Cross-Reference. Update Wizard navigation and state management to support the new sequence.
</domain>

<decisions>
## Implementation Decisions

### State preservation on backward navigation
- **D-01:** Show a prompt/warning before allowing the user to change the selected template if a cross-reference mapping already exists.

### Template step auto-advance
- **D-02:** Keep the existing auto-advance behavior. Clicking "Seleccionar" on a template should immediately auto-advance the user to the next step (which will now be Cross-Reference).

### Match preview invalidation
- **D-03:** If the user ignores the warning and changes the template anyway, clear the mapped `matchKeys` and `outputColumns` completely to force remapping.

### the agent's Discretion
- Logic for implementing the warning modal or dialog before changing the template.
- Exact sub-step bypass logic when clicking "No, omitir" on the Cross-Reference step (it should likely go straight to the Rules step).
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Plans
- `.planning/ROADMAP.md` — Defines the phase boundary and sequence

### Frontend Implementation
- `frontend/src/app/wizard/page.tsx` — Wizard flow UI and state management

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `STEPS` array: Defines the order of steps. Can be reordered easily.
- `goNext` and `goBack` functions: Centralize navigation logic.
- `ConfiguratorCard` and `PillChip`: Used for UI consistency.

### Established Patterns
- State management uses `currentStep` (string) and `subStep` (number) with a `stepHistory` stack.
- The `enableCrossref` boolean state controls the bypass path.

### Integration Points
- `goNext` logic: Hardcoded rules for `currentStep === "crossref"` and `currentStep === "template"` need to be adjusted for the new order.
- `computeSuggestedMatchKeys` and `computeSuggestedOutputColumns`: Rely on both `crossrefColumns` and `templateColumns`. Moving Template before CrossRef ensures `templateColumns` are populated correctly when these run.
</code_context>

<specifics>
## Specific Ideas

No specific UI design changes beyond updating the flow order.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope
</deferred>

---

*Phase: 05-Wizard Reordering*
*Context gathered: 2026-05-16*
