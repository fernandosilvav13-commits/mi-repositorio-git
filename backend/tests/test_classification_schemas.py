import pytest
from app.schemas.classification import ClassificationResult, DocumentCategory


class TestClassificationResult:
    def test_valid_cv_category(self):
        result = ClassificationResult(category="cv", confidence=0.95)
        assert result.category == "cv"
        assert result.confidence == 0.95
        assert result.top_categories == []

    def test_valid_non_cv_category(self):
        result = ClassificationResult(category="non-cv", confidence=0.82)
        assert result.category == "non-cv"

    def test_top_categories(self):
        result = ClassificationResult(
            category="cv",
            confidence=0.95,
            top_categories=[
                {"category": "cv", "confidence": 0.95},
                {"category": "non-cv", "confidence": 0.05},
            ],
        )
        assert len(result.top_categories) == 2

    def test_confidence_bounds(self):
        with pytest.raises(ValueError):
            ClassificationResult(category="cv", confidence=1.5)
        with pytest.raises(ValueError):
            ClassificationResult(category="cv", confidence=-0.1)

    def test_invalid_category(self):
        with pytest.raises(ValueError):
            ClassificationResult(category="invalid", confidence=0.5)

    def test_confidence_at_zero(self):
        result = ClassificationResult(category="non-cv", confidence=0.0)
        assert result.confidence == 0.0

    def test_confidence_at_one(self):
        result = ClassificationResult(category="cv", confidence=1.0)
        assert result.confidence == 1.0
