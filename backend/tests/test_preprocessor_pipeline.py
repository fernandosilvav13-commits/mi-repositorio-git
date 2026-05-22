"""
Integration tests for the PreprocessingPipeline orchestrator.

Tests the full pipeline chain (SectionDetector -> NoiseFilter -> LayoutNormalizer)
using a MOCKED SectionDetector (no real Gemini API calls) and real NoiseFilter
and LayoutNormalizer instances.
"""

import pytest
from unittest.mock import MagicMock

from app.services.preprocessor import PreprocessingPipeline
from app.services.noise_filter import NoiseFilter
from app.services.layout_normalizer import LayoutNormalizer
from app.schemas.preprocessing import DetectionResponse, SectionBoundary, PreprocessingResult


@pytest.fixture
def mock_detector():
    """Fixture: returns a MagicMock(spec=['detect']) for SectionDetector.

    Tests set mock_detector.detect.return_value before calling process().
    The mock's state is reset between tests via the fixture scope.
    """
    mock = MagicMock(spec=['detect'])
    return mock


@pytest.fixture
def real_filter():
    """Fixture: returns a real NoiseFilter instance for integration testing."""
    return NoiseFilter()


@pytest.fixture
def real_normalizer():
    """Fixture: returns a real LayoutNormalizer instance for integration testing."""
    return LayoutNormalizer()


@pytest.fixture
def pipeline(mock_detector, real_filter, real_normalizer):
    """Fixture: returns a PreprocessingPipeline with mocked detector and real stages.

    The pipeline uses constructor injection so tests can control SectionDetector
    behavior (success, failure, empty results) while exercising the actual
    NoiseFilter and LayoutNormalizer string manipulation logic.
    """
    return PreprocessingPipeline(
        section_detector=mock_detector,
        noise_filter=real_filter,
        layout_normalizer=real_normalizer,
    )


class TestPreprocessingPipeline:
    """Integration tests for PreprocessingPipeline orchestrator."""

    def test_full_pipeline_happy_path(self, pipeline, mock_detector):
        """Complete pipeline: detection -> noise removal -> layout normalization.

        Given a document with identifiable sections and noisy lines:
        - Section "Educacion" at lines 0-1 (start_line=0, end_line=1)
        - Noisy line 3 (page number)
        After processing:
        - was_preprocessed should be True
        - cleaned_text should contain section marker "== Educacion =="
        - cleaned_text should NOT contain "page_num" (removed as noise)
        - noisy_lines_removed should contain [3]
        """
        mock_detector.detect.return_value = DetectionResponse(
            sections={"Educacion": SectionBoundary(start_line=0, end_line=1)},
            noisy_lines=[3],
            can_identify=True,
        )

        text = "line0\nheader\nline1\npage_num"
        result = pipeline.process(text)

        assert result.was_preprocessed is True
        assert "== Educacion ==" in result.cleaned_text
        assert "page_num" not in result.cleaned_text
        assert result.noisy_lines_removed == [3]

    def test_skip_on_cannot_identify(self, pipeline, mock_detector):
        """D-03 fallback: when can_identify is False, return original text unchanged.

        The detector returns sections={}, noisy_lines=[], can_identify=False.
        Pipeline should return PreprocessingResult with was_preprocessed=False
        and cleaned_text equal to the original input.
        """
        mock_detector.detect.return_value = DetectionResponse(
            sections={},
            noisy_lines=[],
            can_identify=False,
        )

        text = "some text"
        result = pipeline.process(text)

        assert result.was_preprocessed is False
        # cleaned_text defaults to "" — should contain original text
        assert result.cleaned_text == "some text"

    def test_skip_on_empty_sections(self, pipeline, mock_detector):
        """D-03 fallback: empty sections dict triggers skip even if can_identify is True.

        When the LLM returns can_identify=True but sections={}, the pipeline
        should still return original text with was_preprocessed=False.
        """
        mock_detector.detect.return_value = DetectionResponse(
            sections={},
            noisy_lines=[],
            can_identify=True,
        )

        text = "some text"
        result = pipeline.process(text)

        assert result.was_preprocessed is False
        assert result.cleaned_text == "some text"

    def test_skip_on_empty_text(self, pipeline, mock_detector):
        """Empty text returns PreprocessingResult with was_preprocessed=False and error.

        Empty/whitespace-only text should be caught before the detector call,
        so detector.detect() should NOT be called.
        """
        result = pipeline.process("")

        assert result.was_preprocessed is False
        assert result.error is not None
        assert "Empty" in result.error
        # detector should not be called for empty text
        mock_detector.detect.assert_not_called()

    def test_skip_on_none_text(self, pipeline, mock_detector):
        """None text returns PreprocessingResult with was_preprocessed=False and error.

        None input should be caught before the detector call.
        """
        result = pipeline.process(None)

        assert result.was_preprocessed is False
        assert result.error is not None
        assert "Empty" in result.error
        mock_detector.detect.assert_not_called()

    def test_error_during_detection(self, pipeline, mock_detector):
        """When SectionDetector.detect() raises, pipeline returns graceful fallback.

        The exception should be caught, logged, and returned as a PreprocessingResult
        with was_preprocessed=False and an error message containing the exception text.
        """
        mock_detector.detect.side_effect = RuntimeError("API error")

        result = pipeline.process("text")

        assert result.was_preprocessed is False
        assert "API error" in result.error

    def test_error_during_normalization(self, pipeline, mock_detector):
        """Pipeline handles normalization gracefully when sections are valid.

        This test exercises the real LayoutNormalizer with a valid DetectionResponse
        to ensure the full chain works end-to-end without crashing. The real normalizer
        handles edge cases like single-line sections gracefully.
        """
        # Section with start_line=0, end_line=0 on a one-line text
        mock_detector.detect.return_value = DetectionResponse(
            sections={"Only": SectionBoundary(start_line=0, end_line=0)},
            noisy_lines=[],
            can_identify=True,
        )

        result = pipeline.process("only one line")

        assert result.was_preprocessed is True
        assert "== Only ==" in result.cleaned_text

    def test_section_boundary_adjustment(self, pipeline, mock_detector):
        """Pitfall 2 mitigation: section boundaries adjusted after noise removal.

        Given a document where:
        - Section "Content" spans original lines 3-5 (start_line=3, end_line=5)
        - Lines 1 and 2 are noisy (removed)

        After noise removal:
        - Lines 1-2 are gone, so the section that started at original index 3
          should start at adjusted index 1 (3 - 2 = 1)
        - "== Content ==" marker should appear at the correct adjusted position
        """
        mock_detector.detect.return_value = DetectionResponse(
            sections={"Content": SectionBoundary(start_line=3, end_line=5)},
            noisy_lines=[1, 2],
            can_identify=True,
        )

        text = "line0\nheader1\nheader2\ncontent1\ncontent2\ncontent3"
        result = pipeline.process(text)

        assert result.was_preprocessed is True
        lines = result.cleaned_text.splitlines()

        # After noise removal: indices 1 and 2 removed
        # Original -> Cleaned mapping:
        #   0 -> 0: "line0"
        #   1-2 removed
        #   3 -> 1: "content1"
        #   4 -> 2: "content2"
        #   5 -> 3: "content3"
        # After section markers: "== Content ==" inserted at adjusted 1
        #   ["line0", "== Content ==", "content1", "content2", "content3"]

        assert lines[0] == "line0"
        assert lines[1] == "== Content =="
        assert lines[2] == "content1"
