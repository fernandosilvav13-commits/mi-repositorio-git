import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.extraction_pipeline import ExtractionPipeline


@pytest.fixture
def pipeline():
    return ExtractionPipeline()


class MockPreprocessingResult:
    def __init__(self, cleaned_text):
        self.cleaned_text = cleaned_text
        self.sections_detected = {}
        self.noisy_lines_removed = []


@pytest.mark.asyncio
async def test_pipeline_returns_warning_for_empty_text(pipeline):
    result = await pipeline.process("")
    assert result["classification_warning"] is True
    assert result["category"] == "non-cv"
    assert result["extraction"] is None


@pytest.mark.asyncio
async def test_pipeline_returns_warning_for_whitespace_text(pipeline):
    result = await pipeline.process("   \n  \t  ")
    assert result["classification_warning"] is True


@pytest.mark.asyncio
async def test_pipeline_non_cv_classification(pipeline):
    with (
        patch("app.services.extraction_pipeline.preprocessing_pipeline") as mock_pre,
        patch("app.services.extraction_pipeline.doc_classifier") as mock_cls,
    ):
        mock_pre.process.return_value = MockPreprocessingResult("some non-cv text")
        mock_cls.classify.return_value = MagicMock(
            category="non-cv", confidence=0.8, top_categories=[]
        )
        result = await pipeline.process("some non-cv text")
        assert result["classification_warning"] is True
        assert result["category"] == "non-cv"


@pytest.mark.asyncio
async def test_pipeline_cv_classification_no_prompt(pipeline):
    with (
        patch("app.services.extraction_pipeline.preprocessing_pipeline") as mock_pre,
        patch("app.services.extraction_pipeline.doc_classifier") as mock_cls,
        patch("app.services.extraction_pipeline.prompt_resolver") as mock_pr,
        patch("app.services.extraction_pipeline.extract_fields") as mock_ext,
    ):
        mock_pre.process.return_value = MockPreprocessingResult("cv text here")
        mock_cls.classify.return_value = MagicMock(
            category="cv", confidence=0.95, top_categories=[]
        )
        mock_pr.get.return_value = None
        mock_ext.return_value = {"NOMBRES": "Juan"}
        result = await pipeline.process("cv text here")
        assert result["classification_warning"] is False
        assert result["extraction"] == {"NOMBRES": "Juan"}
        assert result["prompt_version"] is None


@pytest.mark.asyncio
async def test_pipeline_cv_classification_with_prompt(pipeline):
    mock_pv = MagicMock()
    mock_pv.tag_name = "prompt/cv-extraction/v1.0.0"

    with (
        patch("app.services.extraction_pipeline.preprocessing_pipeline") as mock_pre,
        patch("app.services.extraction_pipeline.doc_classifier") as mock_cls,
        patch("app.services.extraction_pipeline.prompt_resolver") as mock_pr,
        patch("app.services.extraction_pipeline.extract_fields") as mock_ext,
    ):
        mock_pre.process.return_value = MockPreprocessingResult("cv text with prompt")
        mock_cls.classify.return_value = MagicMock(
            category="cv", confidence=0.99, top_categories=[]
        )
        mock_pr.get.return_value = mock_pv
        mock_pr.render.return_value = "Rendered prompt content"
        mock_ext.return_value = {"NOMBRES": "Maria", "APELLIDOS": "Garcia"}
        result = await pipeline.process("cv text with prompt")
        assert result["classification_warning"] is False
        assert result["category"] == "cv"
        assert result["confidence"] == 0.99
        assert result["prompt_version"] == "prompt/cv-extraction/v1.0.0"
        assert result["extraction"]["NOMBRES"] == "Maria"


@pytest.mark.asyncio
async def test_pipeline_passes_prompt_override_to_extract(pipeline):
    mock_pv = MagicMock()
    mock_pv.tag_name = "prompt/cv-extraction/v1.0.0"

    with (
        patch("app.services.extraction_pipeline.preprocessing_pipeline") as mock_pre,
        patch("app.services.extraction_pipeline.doc_classifier") as mock_cls,
        patch("app.services.extraction_pipeline.prompt_resolver") as mock_pr,
        patch("app.services.extraction_pipeline.extract_fields") as mock_ext,
    ):
        mock_pre.process.return_value = MockPreprocessingResult("cv text")
        mock_cls.classify.return_value = MagicMock(
            category="cv", confidence=0.95, top_categories=[]
        )
        mock_pr.get.return_value = mock_pv
        mock_pr.render.return_value = "Custom prompt"
        mock_ext.return_value = {}
        await pipeline.process("cv text")
        mock_ext.assert_called_once()
        _, kwargs = mock_ext.call_args
        assert kwargs["prompt_override"] == "Custom prompt"
