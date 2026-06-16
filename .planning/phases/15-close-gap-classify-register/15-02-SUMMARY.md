---
phase: 15-close-gap-classify-register
plan: 02
---
# Plan 15-02 Summary

**Phase:** 15 - Close Gap: Register /api/classify in main.py
**Plan:** 02
**Status:** Complete

## Completed Tasks

- **Task 1:** Changed  default from  to . The  parameter remains available as explicit opt-out for backward compatibility.
- **Task 2:** Changed  instantiation in  from relative path  to absolute path , matching the pattern used by 

## Files Changed

-  — flipped default on line 23
-  — fixed PromptResolver path, added 

## Verification

- Syntax validated on all modified files
- Two-pass pipeline now activates by default in production
- Legacy single-pass path preserved via 
- PromptResolver resolves prompts correctly from any working directory

