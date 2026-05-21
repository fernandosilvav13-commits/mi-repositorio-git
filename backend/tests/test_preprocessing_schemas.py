"""
Tests for preprocessing pipeline Pydantic schema models.

Validates creation, field requirements, defaults, and validation errors
for SectionBoundary, DetectionResponse, and PreprocessingResult models.
"""

import pytest
from pydantic import BaseModel, ValidationError

from app.schemas.preprocessing import DetectionResponse, SectionBoundary, PreprocessingResult


class TestSectionBoundary:
    """Tests for the SectionBoundary model."""

    def test_section_boundary_creation(self):
        """Create SectionBoundary with explicit start/end lines."""
        sb = SectionBoundary(start_line=0, end_line=45)
        assert sb.start_line == 0
        assert sb.end_line == 45
        assert isinstance(sb, BaseModel)

    def test_section_boundary_required_fields(self):
        """SectionBoundary requires both start_line and end_line."""
        with pytest.raises(ValidationError):
            SectionBoundary()

    def test_section_boundary_zero_indexed(self):
        """A single-line section (start=0, end=0) is valid."""
        sb = SectionBoundary(start_line=0, end_line=0)
        assert sb.start_line == 0
        assert sb.end_line == 0


class TestDetectionResponse:
    """Tests for the DetectionResponse model."""

    def test_detection_response_creation(self):
        """Create DetectionResponse with all fields populated."""
        dr = DetectionResponse(
            sections={"Educacion": SectionBoundary(start_line=0, end_line=45)},
            noisy_lines=[1, 2, 100],
            can_identify=True,
        )
        assert dr.sections["Educacion"].end_line == 45
        assert dr.noisy_lines == [1, 2, 100]
        assert dr.can_identify is True

    def test_detection_response_required_fields(self):
        """DetectionResponse requires sections, noisy_lines, and can_identify."""
        with pytest.raises(ValidationError):
            DetectionResponse()

    def test_detection_response_can_identify_false(self):
        """DetectionResponse stores can_identify=False correctly."""
        dr = DetectionResponse(sections={}, noisy_lines=[], can_identify=False)
        assert dr.can_identify is False
        assert dr.sections == {}
        assert dr.noisy_lines == []

    def test_detection_response_with_section_boundary_dict(self):
        """DetectionResponse holds multiple sections with correct boundaries."""
        dr = DetectionResponse(
            sections={
                "Educacion": SectionBoundary(start_line=0, end_line=45),
                "Experiencia_Laboral": SectionBoundary(start_line=47, end_line=120),
                "Idiomas": SectionBoundary(start_line=122, end_line=130),
            },
            noisy_lines=[1, 2, 100],
            can_identify=True,
        )
        assert len(dr.sections) == 3
        assert dr.sections["Educacion"].start_line == 0
        assert dr.sections["Educacion"].end_line == 45
        assert dr.sections["Experiencia_Laboral"].start_line == 47
        assert dr.sections["Experiencia_Laboral"].end_line == 120
        assert dr.sections["Idiomas"].start_line == 122
        assert dr.sections["Idiomas"].end_line == 130


class TestPreprocessingResult:
    """Tests for the PreprocessingResult model."""

    def test_preprocessing_result_defaults(self):
        """PreprocessingResult has correct default values."""
        pr = PreprocessingResult()
        assert pr.cleaned_text == ""
        assert pr.sections_detected == {}
        assert pr.noisy_lines_removed == []
        assert pr.was_preprocessed is False
        assert pr.error is None

    def test_preprocessing_result_full(self):
        """PreprocessingResult accepts all fields."""
        pr = PreprocessingResult(
            cleaned_text="text",
            sections_detected={"Educacion": SectionBoundary(start_line=0, end_line=5)},
            noisy_lines_removed=[1],
            was_preprocessed=True,
            error=None,
        )
        assert pr.cleaned_text == "text"
        assert pr.sections_detected["Educacion"].end_line == 5
        assert pr.noisy_lines_removed == [1]
        assert pr.was_preprocessed is True
        assert pr.error is None

    def test_preprocessing_result_with_error(self):
        """PreprocessingResult stores error message without changing was_preprocessed."""
        pr = PreprocessingResult(
            cleaned_text="original",
            was_preprocessed=False,
            error="Section detection failed",
        )
        assert pr.error == "Section detection failed"
        assert pr.was_preprocessed is False
