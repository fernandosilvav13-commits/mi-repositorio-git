"""Tests for preprocessor.py — clean_text() and preprocess_cv_text()."""

from app.services.preprocessor import clean_text, preprocess_cv_text


# ── Unit tests for clean_text() ──────────────────────────────────────────────


def test_clean_text_all_caps_preserved():
    """D-01: All-caps proper noun preservation — no blanket .lower()."""
    result = clean_text("MARÍA GARCÍA")
    assert "MARÍA" in result
    assert "GARCÍA" in result


def test_clean_text_redundant_phrase_ignorcase():
    """D-02: Redundant phrase removal with IGNORECASE (mixed case)."""
    result = clean_text("Hoja de Vida - María García")
    assert "María García" in result


def test_clean_text_redundant_phrase_all_caps():
    """D-02: Redundant phrase removal with IGNORECASE (all caps)."""
    result = clean_text("CURRICULUM VITAE")
    assert result == ""


def test_clean_text_redundant_phrase_accented():
    """D-03: Redundant phrase with diacritic (lowercase)."""
    result = clean_text("currículum vitae")
    assert result == ""


def test_clean_text_whitespace_normalized():
    """Existing behavior: whitespace normalization unchanged."""
    result = clean_text("  spaced   text  ")
    assert result == "spaced text"


def test_clean_text_empty_input():
    """Empty and blank input return empty string."""
    assert clean_text("") == ""
    assert clean_text("   ") == ""


def test_clean_text_mixed_casing_survives():
    """Proper noun casing survives alongside redundant phrase removal."""
    result = clean_text("Curriculum Vitae - Juan Pérez LÓPEZ")
    assert "Juan" in result
    assert "Pérez" in result
    assert "LÓPEZ" in result


# ── Integration tests for preprocess_cv_text() ────────────────────────────────


def test_preprocess_preserves_casing_sections_found():
    """D-07: Full pipeline preserves casing when sections are matched."""
    text = "CURRICULUM VITAE\nNOMBRES: MARÍA GARCÍA LÓPEZ\nRUT: 12.345.678-9"
    result = preprocess_cv_text(text)
    assert "#NOMBRES:" in result
    assert "MARÍA" in result
    assert "GARCÍA" in result


def test_preprocess_fallback_no_sections():
    """Fallback path: no sections matched, raw text returned with casing preserved."""
    text = "some random text without any keyword headers"
    result = preprocess_cv_text(text)
    # Should contain the raw cleaned text
    assert "random" in result
    assert result == text  # No modification expected


def test_preprocess_typical_cv_header():
    """Typical CV: redundant phrase removed, name casing preserved, RUT extracted."""
    text = "Hoja de Vida\nNOMBRES: Juan Pérez\nRUT: 12.345.678-9"
    result = preprocess_cv_text(text)
    assert "Hoja de Vida" not in result  # Redundant phrase removed
    assert "#NOMBRES:" in result
    assert "Juan" in result
    assert "Pérez" in result
    assert "12.345.678-9" in result
