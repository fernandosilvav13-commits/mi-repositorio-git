# Phase 05: Wizard Reordering - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-16
**Phase:** 05-Wizard Reordering
**Areas discussed:** State preservation on backward navigation, Template step auto-advance, Match preview invalidation

---

## State preservation on backward navigation

| Option | Description | Selected |
|--------|-------------|----------|
| Clear mapping completely | Safest approach, avoids mismatched columns | |
| Attempt to preserve mapping | Tries to keep mapped keys if the new template has the same column names | |
| Warn before changing | Show a prompt before allowing template change if mapping exists | ✓ |

**User's choice:** Warn before changing
**Notes:** Decided to add a warning prompt if the user tries to change the template after configuring a cross-reference map.

---

## Template step auto-advance

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, keep auto-advance | Fastest flow, immediate transition | ✓ |
| No, require 'Siguiente' click | User must click 'Siguiente' explicitly, allowing time to edit the template if needed | |

**User's choice:** Yes, keep auto-advance
**Notes:** Flow speed prioritized. The transition to Cross-Reference will happen immediately upon template selection.

---

## Match preview invalidation

| Option | Description | Selected |
|--------|-------------|----------|
| Clear match keys and output columns | Reset mapping arrays to empty, forcing the user to remap | ✓ |
| Filter out invalid columns | Keep them, but filter out columns that no longer exist in the new template | |

**User's choice:** Clear match keys and output columns
**Notes:** If the warning is ignored and the template changes, mappings will be fully cleared.

---

## the agent's Discretion

- Logic for implementing the warning modal or dialog before changing the template.
- Exact sub-step bypass logic when clicking "No, omitir" on the Cross-Reference step.

## Deferred Ideas

None
