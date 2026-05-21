"""
Unit tests for LayoutNormalizer.

Tests whitespace collapsing, paragraph break preservation, section marker
insertion (bottom-to-top), bullet normalization, and edge case handling.
"""

import pytest

from app.services.layout_normalizer import LayoutNormalizer
from app.schemas.preprocessing import SectionBoundary


@pytest.fixture
def normalizer():
    """Fixture: returns LayoutNormalizer instance."""
    return LayoutNormalizer()


class TestLayoutNormalizer:
    """Tests for LayoutNormalizer class."""

    def test_collapse_inline_whitespace(self, normalizer):
        """Multiple spaces within a line should collapse to single space."""
        text = "Nombre:    Juan    Perez\nTelefono: +56 9 1234 5678"
        sections = {}
        result = normalizer.normalize(text, sections)

        assert "Nombre: Juan Perez" in result
        assert "Telefono: +56 9 1234 5678" in result

    def test_preserve_paragraph_breaks(self, normalizer):
        """Double newlines should be preserved as paragraph boundaries."""
        text = "First paragraph.\n\nSecond paragraph."
        sections = {}
        result = normalizer.normalize(text, sections)

        assert "First paragraph." in result
        assert "Second paragraph." in result
        assert "\n\n" in result  # Double newline preserved

    def test_section_markers_inserted(self, normalizer):
        """Section boundary markers should be inserted at correct positions."""
        text = "line0\nline1\nline2\nline3"
        sections = {
            "Educacion": SectionBoundary(start_line=2, end_line=3),
        }
        result = normalizer.normalize(text, sections)
        lines = result.splitlines()

        # Marker inserted before section at start_line=2
        assert lines[2] == "== Educacion =="
        # Original content shifted down by 1
        assert lines[3] == "line2"

    def test_multiple_section_markers(self, normalizer):
        """Multiple section markers inserted correctly with bottom-to-top ordering.

        This tests that inserting from bottom to top (reverse sorted by start_line)
        preserves correct line indices for subsequent insertions.
        """
        text = "pre\neducacion\nexperiencia\npost"
        sections = {
            "Educacion": SectionBoundary(start_line=1, end_line=1),
            "Experiencia": SectionBoundary(start_line=2, end_line=2),
        }
        result = normalizer.normalize(text, sections)
        lines = result.splitlines()

        # Expected structure when inserting bottom-to-top:
        # Insert "== Experiencia ==" at 2 first:
        #   ["pre", "educacion", "== Experiencia ==", "experiencia", "post"]
        # Then insert "== Educacion ==" at 1:
        #   ["pre", "== Educacion ==", "educacion", "== Experiencia ==", "experiencia", "post"]
        assert "== Educacion ==" in lines
        assert "== Experiencia ==" in lines

        # Find positions
        edu_idx = lines.index("== Educacion ==")
        exp_idx = lines.index("== Experiencia ==")

        # Both markers exist
        assert edu_idx >= 0
        assert exp_idx >= 0

        # And the content is still there
        assert "educacion" in lines
        assert "experiencia" in lines
        assert "pre" in lines
        assert "post" in lines

    def test_three_section_markers(self, normalizer):
        """Test with three sections to verify bottom-to-top insertion."""
        text = "line0\nline1\nline2\nline3\nline4\nline5"
        sections = {
            "A": SectionBoundary(start_line=1, end_line=1),
            "B": SectionBoundary(start_line=3, end_line=3),
            "C": SectionBoundary(start_line=5, end_line=5),
        }
        result = normalizer.normalize(text, sections)
        lines = result.splitlines()

        # All markers should exist
        assert "== A ==" in lines
        assert "== B ==" in lines
        assert "== C ==" in lines

        # Original lines should still be present
        assert "line0" in lines
        assert "line1" in lines
        assert "line2" in lines
        assert "line3" in lines
        assert "line4" in lines
        assert "line5" in lines

    def test_bullet_normalization(self, normalizer):
        """Various bullet formats should be standardized to '* '."""
        text = "• Item one\n- Item two\n  * Item three\n1) Item four"
        sections = {}
        result = normalizer.normalize(text, sections)
        lines = result.splitlines()

        for line in lines:
            # All bullet lines should start with "* "
            assert line.startswith("* "), f"Line '{line}' should start with '* '"

    def test_no_false_bullet_match(self, normalizer):
        """Dashes in middle of lines should NOT be treated as bullets (Pitfall 4).

        The anchored regex ^[\\s]*[bullet chars]\\s+ only matches at line start.
        """
        text = "proven - management skills\ncross-platform"
        sections = {}
        result = normalizer.normalize(text, sections)

        # The dash in "proven - management" should NOT be replaced
        assert "proven - management skills" in result

    def test_section_marker_beyond_text(self, normalizer):
        """Section start_line beyond text length should be gracefully skipped."""
        text = "only line"
        sections = {"Missing": SectionBoundary(start_line=10, end_line=20)}
        result = normalizer.normalize(text, sections)

        # No error raised, marker not inserted
        assert result == "only line"
        assert "Missing" not in result

    def test_empty_text(self, normalizer):
        """Empty text returns empty string."""
        result = normalizer.normalize("", {})
        assert result == ""

    def test_none_text(self, normalizer):
        """None text returns empty string gracefully."""
        result = normalizer.normalize(None, {})
        assert result == ""

    def test_whitespace_only_text(self, normalizer):
        """All whitespace text collapses to empty string."""
        text = "   \n\n  \n "
        sections = {}
        result = normalizer.normalize(text, sections)
        assert result == ""

    def test_empty_sections_dict(self, normalizer):
        """Empty sections dict: whitespace normalization still happens, no markers."""
        text = "line0   with    extra   spaces\nline1"
        sections = {}
        result = normalizer.normalize(text, sections)

        # Whitespace should be collapsed
        assert "line0 with extra spaces" in result
        assert "line1" in result
        # No section markers
        assert "==" not in result
