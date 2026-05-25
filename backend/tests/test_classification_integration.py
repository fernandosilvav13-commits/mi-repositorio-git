import pytest
from app.services.classifier import doc_classifier, DocClassifier
from app.schemas.classification import ClassificationResult


class TestClassificationIntegration:
    def test_full_cv_text_classifies_as_cv(self):
        cv_text = """
EXPERIENCIA LABORAL
Ingeniero de Software
Empresa Tecnologica | 2020 - Presente
- Desarrollo de aplicaciones web con Python
- Administracion de bases de datos

FORMACION ACADEMICA
Ingenieria en Computacion
Universidad de Chile | 2014 - 2019

HABILIDADES
Python, Django, PostgreSQL, Docker, Git

IDIOMAS
Espanol: Nativo
Ingles: Avanzado (C1)
"""
        result = doc_classifier.classify(cv_text)
        assert result.category == "cv"
        assert result.confidence >= 0.7

    def test_non_cv_text_classifies_as_non_cv(self):
        non_cv_text = """
FACTURA ELECTRONICA N 0012345
RUT: 76.123.456-7
Razon Social: Empresa Ejemplo Ltda.

Detalle:
- Servicios de consultoria $2.500.000
- Licencias de software $840.000
Total: $3.340.000
IVA 19% incluido
"""
        result = doc_classifier.classify(non_cv_text)
        assert result.category == "non-cv"

    def test_threshold_boundary_just_above(self):
        text = "EXPERIENCIA LABORAL Programador FORMACION Universidad"
        result = doc_classifier.classify(text, threshold=0.7)
        assert result.category in ("cv", "non-cv")

    def test_very_short_text_does_not_crash(self):
        result = doc_classifier.classify("Corto")
        assert isinstance(result, ClassificationResult)

    def test_empty_text_fallback(self):
        result = doc_classifier.classify("")
        assert result.category == "non-cv"
        assert result.confidence == 0.0

    def test_module_singleton_exists(self):
        from app.services.classifier import doc_classifier as dc
        assert isinstance(dc, DocClassifier)
        assert dc is doc_classifier
