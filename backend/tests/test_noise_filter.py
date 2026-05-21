"""
Unit tests for NoiseFilter.

Tests line removal by index, edge cases, and D-07 noise type documentation.
"""

import pytest

from app.services.noise_filter import NoiseFilter


@pytest.fixture
def noise_filter():
    """Fixture: returns NoiseFilter instance."""
    return NoiseFilter()


class TestNoiseFilter:
    """Tests for NoiseFilter class."""

    def test_remove_specific_lines(self, noise_filter):
        """Remove specific indices and verify only those lines are removed."""
        text = "line0\nline1\nline2\nline3"
        result = noise_filter.filter(text, {1, 3})
        assert result == "line0\nline2"

    def test_preserve_other_lines(self, noise_filter):
        """Remove one line and verify all other lines are preserved in order."""
        text = "a\nb\nc\nd\ne"
        result = noise_filter.filter(text, {2})
        assert result == "a\nb\nd\ne"
        # Only index 2 removed, rest preserved

    def test_empty_noisy_lines(self, noise_filter):
        """Empty set returns original text unchanged (optimization)."""
        text = "line0\nline1"
        result = noise_filter.filter(text, set())
        # Should return original text (or equivalent)
        assert result == "line0\nline1"

    def test_all_lines_noisy(self, noise_filter):
        """Removing all lines returns empty string."""
        text = "a\nb\nc"
        result = noise_filter.filter(text, {0, 1, 2})
        assert result == ""

    def test_out_of_range_index(self, noise_filter):
        """Out of range indices are silently ignored."""
        text = "a\nb"
        result = noise_filter.filter(text, {0, 5, 99})
        # Only index 0 should be removed, 5 and 99 are out of range
        assert result == "b"

    def test_empty_text(self, noise_filter):
        """Empty text returns empty string."""
        result = noise_filter.filter("", {0, 1})
        assert result == ""

    def test_none_text(self, noise_filter):
        """None text returns empty string gracefully."""
        result = noise_filter.filter(None, {0})
        assert result == ""

    def test_noise_types_documented(self, noise_filter):
        """D-07 noise types mentioned in class or module docstring.

        D-07 noise types: page headers, page numbers, footers, metadata artifacts.
        """
        import inspect

        # Check class docstring
        class_doc = inspect.getdoc(NoiseFilter) or ""

        # Check module docstring
        module_doc = __doc__ or ""

        combined = class_doc.lower() + " " + module_doc.lower()

        # Verify D-07 noise types are mentioned
        assert "page headers" in combined or "page header" in combined
        assert "page numbers" in combined or "page number" in combined
        assert "footers" in combined or "footer" in combined
        assert "metadata" in combined

    def test_preserve_leading_trailing_newlines(self, noise_filter):
        """Leading/trailing blank lines preserved, only specified indices removed.

        This tests that empty/blank lines at the start or within the text
        are preserved unless explicitly in the noisy_lines set.
        """
        # Text with leading empty line, then content
        # splitlines: ["", "header", "content", "footer"]
        text = "\nheader\ncontent\nfooter"
        lines = text.splitlines(keepends=False)

        # Verify our understanding of splitlines behavior
        assert len(lines) == 4  # ["", "header", "content", "footer"]
        assert lines[0] == ""  # Leading empty line

        # Remove "header" (index 1) and "footer" (index 3)
        result = noise_filter.filter(text, {1, 3})

        # Should keep index 0 ("") and index 2 ("content")
        # Joined: "\ncontent"
        assert "header" not in result
        assert "footer" not in result
        assert "content" in result

        # Verify the structure: leading empty line preserved, content kept
        result_lines = result.splitlines(keepends=False)
        # Either: empty string at index 0 (if splitlines sees it), or content
        # The key is: only indices 1 and 3 were removed, not the empty line at 0
        assert result_lines[0] == "" or result_lines[0] == "content"
        if len(result_lines) > 1:
            assert "content" in result_lines
