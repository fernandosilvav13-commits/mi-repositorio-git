---
phase: 09
slug: prompt-infrastructure-foundation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-19
---

# Phase 09 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (Python 3.12) |
| **Config file** | backend/pyproject.toml or pytest.ini |
| **Quick run command** | `pytest backend/tests/test_prompt_resolver.py -x` |
| **Full suite command** | `pytest backend/tests/ -x` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest backend/tests/test_prompt_resolver.py -x`
- **After every plan wave:** Run `pytest backend/tests/ -x`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 09-01-01 | 01 | 1 | PROMPT-01 | T-09-01 | yaml.safe_load prevents injection | unit | `pytest tests/test_prompt_resolver.py::test_prompt_version_valid -x` | ❌ W0 | ⬜ pending |
| 09-01-02 | 01 | 1 | PROMPT-01 | T-09-01 | YAML validated on load | unit | `pytest tests/test_prompt_resolver.py::test_yaml_load_and_parse -x` | ❌ W0 | ⬜ pending |
| 09-01-03 | 01 | 1 | PROMPT-01 | — | — | unit | `pytest tests/test_prompt_resolver.py -x` | ❌ W0 | ⬜ pending |
| 09-02-01 | 02 | 2 | PROMPT-01 | T-09-04, T-09-05, T-09-06 | safe_load, version validation, BaseLoader | unit | `pytest tests/test_prompt_resolver.py::test_resolver_scan_and_get_exact -x` | ❌ W0 | ⬜ pending |
| 09-02-02 | 02 | 2 | PROMPT-01 | T-09-04, T-09-05, T-09-06 | safe_load, version validation, BaseLoader | unit | `pytest tests/test_prompt_resolver.py -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_prompt_resolver.py` — stubs for PROMPT-01
- [ ] `backend/tests/conftest.py` — shared fixtures
- [ ] `pip install pyyaml jinja2 semver` — if not already in requirements.txt

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Git tag creation | PROMPT-01 (D-10) | git tag modifies repo state, cannot be automated in unit tests | Run `python3 -c "from app.services.prompt_resolver import PromptResolver; PromptResolver.create_prompt_tag('cv-extraction', '1.0.0', 'test')"` then verify with `git tag -l prompt/cv-extraction/*` |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
