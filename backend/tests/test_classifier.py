import pytest
from app.services.classifier import DocClassifier, CLASSIFICATION_THRESHOLD, CATEGORIES
from app.schemas.classification import ClassificationResult


@pytest.fixture
def classifier():
    clf = DocClassifier()
    clf._fit()
    return clf


class TestDocClassifier:
    def test_predict_returns_valid_category(self, classifier):
        text = "EXPERIENCIA LABORAL Analista de Sistemas FORMACION Universitaria HABILIDADES Python"
        result = classifier.predict(text)
        assert result in CATEGORIES

    def test_classify_returns_classification_result(self, classifier):
        text = "EXPERIENCIA LABORAL Analista FORMACION Universidad HABILIDADES Python IDIOMAS Ingles"
        result = classifier.classify(text)
        assert isinstance(result, ClassificationResult)
        assert result.category in CATEGORIES
        assert 0.0 <= result.confidence <= 1.0

    def test_confidence_scores_in_range(self, classifier):
        text = "EXPERIENCIA LABORAL Programador FORMACION Ingenieria"
        probs = classifier.predict_proba(text)
        for cat in CATEGORIES:
            assert cat in probs
            assert 0.0 <= probs[cat] <= 1.0

    def test_cv_text_gets_high_cv_confidence(self, classifier):
        cv_text = """
EXPERIENCIA LABORAL
Ingeniero de Software
Empresa Tecnologica | 2020 - Presente
- Desarrollo de aplicaciones web
- Python, Django, PostgreSQL

FORMACION ACADEMICA
Ingenieria en Computacion
Universidad de Chile | 2014 - 2019

HABILIDADES
Python, Django, SQL, Git, Docker

IDIOMAS
Espanol: Nativo
Ingles: Avanzado
"""
        result = classifier.classify(cv_text)
        assert result.category == "cv"

    def test_non_cv_text_gets_non_cv_category(self, classifier):
        non_cv_text = """
FACTURA ELECTRONICA N 12345
RUT: 76.123.456-7
Fecha: 15 marzo 2025

Detalle:
- Servicios de consultoria $1.500.000
- Licencias de software $840.000

Total: $2.340.000
IVA incluido
"""
        result = classifier.classify(non_cv_text)
        assert result.category == "non-cv"

    def test_threshold_filtering_below_threshold(self, classifier):
        short_text = "texto corto sin estructura clara de documento"
        result = classifier.classify(short_text, threshold=0.95)
        assert result.category == "non-cv"

    def test_cv_text_with_top_categories(self, classifier):
        cv_text = "EXPERIENCIA LABORAL Ingeniero FORMACION Universidad HABILIDADES Python"
        result = classifier.classify(cv_text)
        assert len(result.top_categories) > 0
        assert result.top_categories[0]["category"] == "cv"

    def test_empty_text_returns_non_cv(self, classifier):
        result = classifier.classify("")
        assert result.category == "non-cv"

    def test_very_short_text(self, classifier):
        result = classifier.classify("Hola mundo")
        assert isinstance(result, ClassificationResult)

    def test_predict_proba_returns_dict(self, classifier):
        text = "EXPERIENCIA LABORAL Programador"
        probs = classifier.predict_proba(text)
        assert isinstance(probs, dict)
        assert "cv" in probs
        assert "non-cv" in probs
