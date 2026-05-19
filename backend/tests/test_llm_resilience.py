"""Tests for llm_service.py — JSON repair, TPM tracking, retry logic."""

from app.services.llm_service import _repair_json
import json


# ── Unit tests for _repair_json() ─────────────────────────────────────────────


def test_repair_strips_code_fences():
    raw = "```json\n{\"key\": \"value\"}\n```"
    assert json.loads(_repair_json(raw)) == {"key": "value"}


def test_repair_strips_fences_without_lang():
    raw = "```\n{\"key\": \"value\"}\n```"
    assert json.loads(_repair_json(raw)) == {"key": "value"}


def test_repair_removes_trailing_comma_object():
    raw = '{"a": 1, "b": 2,}'
    assert json.loads(_repair_json(raw)) == {"a": 1, "b": 2}


def test_repair_removes_trailing_comma_array():
    raw = '{"items": [1, 2, 3,]}'
    result = json.loads(_repair_json(raw))
    assert result["items"] == [1, 2, 3]


def test_repair_replaces_single_quotes():
    raw = "{'key': 'value'}"
    assert json.loads(_repair_json(raw)) == {"key": "value"}


def test_repair_single_quotes_with_nested():
    raw = "{'a': {'b': 'c'}}"
    assert json.loads(_repair_json(raw)) == {"a": {"b": "c"}}


def test_repair_combined_fences_trailing_comma_single_quotes():
    raw = "```\n{'a': 1, 'b': [2, 3,],}\n```"
    assert json.loads(_repair_json(raw)) == {"a": 1, "b": [2, 3]}


def test_repair_valid_json_unchanged():
    raw = '{"a": 1, "b": "hello"}'
    assert json.loads(_repair_json(raw)) == {"a": 1, "b": "hello"}


def test_repair_empty_object():
    assert json.loads(_repair_json("{}")) == {}


def test_repair_whitespace_only():
    result = _repair_json("   ")
    assert result == ""


def test_repair_no_encontrado_value():
    raw = '{"NOMBRES": "NO ENCONTRADO"}'
    assert json.loads(_repair_json(raw)) == {"NOMBRES": "NO ENCONTRADO"}


# ── Tests for extract_fields edge cases (without API calls) ───────────────────

def test_repair_apostrophe_inside_string():
    """Single quotes inside a string value should survive repair."""
    raw = '{"name": "D\'Artagnan"}'
    assert json.loads(_repair_json(raw)) == {"name": "D'Artagnan"}
