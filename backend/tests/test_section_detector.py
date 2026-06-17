"""
Unit tests for SectionDetector.

These tests verify the class structure and logic that does NOT require
actual Gemini API calls. The Gemini call path is tested via integration
tests in Plan 03.
"""

import pytest

from app.services.section_detector import (
    SectionDetector,
    DEFAULT_MODEL,
    DEFAULT_PROMPT_VERSION,
    _prompt_resolver,
    _client,
)
from app.schemas.preprocessing import DetectionResponse


class TestSectionDetector:
    """Tests for SectionDetector class structure and non-API logic."""

    def test_detector_instantiation(self):
        """Create SectionDetector(). Verify it has attribute 'detect' that is callable."""
        sd = SectionDetector()
        assert hasattr(sd, 'detect')
        assert callable(sd.detect)

    def test_detector_default_constants(self):
        """Verify DEFAULT_MODEL and DEFAULT_PROMPT_VERSION constants."""
        assert DEFAULT_MODEL == "fast"
        assert DEFAULT_PROMPT_VERSION == "^v1.0.0"

    def test_detector_has_module_singletons(self):
        """Verify module-level singletons exist."""
        # _prompt_resolver should be a PromptResolver instance (not None)
        assert _prompt_resolver is not None

        # _client is lazy-initialized, so it should be None until first API call
        # The key is that the module-level variable exists
        from app.services import section_detector
        assert hasattr(section_detector, '_client')

    def test_detector_rejects_none_text(self):
        """Verify detect() returns can_identify=False for empty/None/whitespace text.

        This test verifies the empty text edge case handling without making API calls.
        """
        sd = SectionDetector()

        # Empty string
        result1 = sd.detect("")
        assert isinstance(result1, DetectionResponse)
        assert result1.can_identify is False
        assert result1.sections == {}
        assert result1.noisy_lines == []

        # None
        result2 = sd.detect(None)
        assert isinstance(result2, DetectionResponse)
        assert result2.can_identify is False

        # Whitespace-only
        result3 = sd.detect("   \n\n  \t  \n ")
        assert isinstance(result3, DetectionResponse)
        assert result3.can_identify is False
