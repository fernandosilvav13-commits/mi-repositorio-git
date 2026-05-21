"""
Preprocessing pipeline Pydantic models.

Defines the data contracts for the three-stage preprocessing pipeline:
SectionDetector, NoiseFilter, and LayoutNormalizer. These models are used
for structured output parsing from Gemini API calls and for passing data
between pipeline stages.
"""

from pydantic import BaseModel, Field


class SectionBoundary(BaseModel):
    """Single section boundary with 0-indexed line numbers.

    Represents the start and end lines of a document section as detected
    by the LLM. Both indices are 0-indexed and end_line is inclusive.
    """

    start_line: int = Field(description="First line of the section, 0-indexed")
    end_line: int = Field(description="Last line of the section, inclusive, 0-indexed")


class DetectionResponse(BaseModel):
    """Response from the batched section-detection + noise-detection LLM call.

    Returned by SectionDetector.detect() as the result of the first Gemini
    call. Contains identified section boundaries, noisy line indices, and
    a flag indicating whether document structure was confidently identified.
    """

    sections: dict[str, SectionBoundary] = Field(
        description="Map of section names (e.g. Educacion, Experiencia_Laboral, "
        "Idiomas) to their line boundaries"
    )
    noisy_lines: list[int] = Field(
        description="0-indexed line numbers of noisy content: page headers, "
        "page numbers, footers, document metadata artifacts"
    )
    can_identify: bool = Field(
        description="True if the LLM could confidently identify document section "
        "structure. False if document is ambiguous (triggers D-03 skip)."
    )


class PreprocessingResult(BaseModel):
    """Result of running the full PreprocessingPipeline on a document.

    Represents the output of the complete three-stage pipeline:
    SectionDetector -> NoiseFilter -> LayoutNormalizer. This model is
    consumed by downstream extraction flow components.
    """

    cleaned_text: str = Field(
        default="",
        description="The preprocessed document text after noise removal and normalization",
    )
    sections_detected: dict = Field(
        default_factory=dict,
        description="Section map from detection, keyed by section name",
    )
    noisy_lines_removed: list[int] = Field(
        default_factory=list,
        description="Line numbers that were removed as noise",
    )
    was_preprocessed: bool = Field(
        default=False,
        description="True if the pipeline ran successfully; False if skipped",
    )
    error: str | None = Field(
        default=None,
        description="Error message if preprocessing failed, None otherwise",
    )
