# Testing Patterns

**Analysis Date:** 2026-05-15

## Test Framework

**Runner:**
- **Backend**: None detected in `requirements.txt`. Recommend `pytest`.
- **Frontend**: None detected in `package.json`. Recommend `vitest`.

**Assertion Library:**
- **Backend**: `pytest` assertions recommended.
- **Frontend**: `vitest` or `jest` (standard with Next.js) recommended.

**Run Commands:**
```bash
# Recommended commands (not currently implemented)
pytest                 # Backend tests
npm test               # Frontend tests
```

## Test File Organization

**Location:**
- **Backend**: Recommend a top-level `tests/` directory in `backend/` or co-located `test_*.py` files.
- **Frontend**: Recommend co-located `.test.tsx` files or a `__tests__/` directory.

**Naming:**
- **Backend**: `test_*.py`
- **Frontend**: `*.test.ts`, `*.test.tsx`, or `*.spec.ts`

**Structure:**
```
[backend]/
└── tests/
    ├── api/
    └── services/

[frontend]/
└── src/
    └── components/
        └── ui/
            └── button.test.tsx
```

## Test Structure

**Suite Organization:**
*(Example of recommended pattern)*
```typescript
describe("ComponentName", () => {
  it("should render correctly", () => {
    // test logic
  });
});
```

**Patterns:**
- **Setup/Teardown**: Use fixtures (pytest) or `beforeEach`/`afterEach` (vitest).
- **Assertions**: Descriptive assertions with clear error messages.

## Mocking

**Framework:** 
- **Backend**: `unittest.mock` or `pytest-mock`.
- **Frontend**: `vitest` mocks or `msw` for API mocking.

**Patterns:**
*(No patterns observed in codebase yet)*
- Recommend mocking external dependencies like Supabase and LLM APIs.

**What to Mock:**
- Database calls (`supabase-js`).
- External API calls (Gemini AI, OCR).
- File system operations.

**What NOT to Mock:**
- Internal pure logic and utility functions.

## Fixtures and Factories

**Test Data:**
*(No pattern observed)*
- Recommend using `pytest.fixture` for backend and mock data constants for frontend.

**Location:**
- `backend/tests/conftest.py` for shared fixtures.
- `frontend/src/tests/fixtures/` for frontend data.

## Coverage

**Requirements:** None enforced.

**View Coverage:**
```bash
# Recommended (if tools are added)
pytest --cov=app      # Backend
vitest run --coverage # Frontend
```

## Test Types

**Unit Tests:**
- Focus on services (`cv_processor.py`) and utilities (`rut_formatter.py`).

**Integration Tests:**
- Focus on API endpoints (`backend/app/api/`) verifying the flow from request to database.

**E2E Tests:**
- Not used. Recommend `Playwright` for critical flows like the extraction wizard.

## Common Patterns

**Async Testing:**
- Use `pytest-asyncio` for backend async services.
- Use `async/await` with `testing-library` for frontend components.

**Error Testing:**
- Verify that `HTTPException` is raised on invalid input in the backend.
- Verify that error states are rendered in the UI on failed extractions.

---

*Testing analysis: 2026-05-15*
