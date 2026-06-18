"""Tests for gender_service — GenderResult, compound names, confidence."""
from app.services.gender_service import (
    infer_gender,
    infer_gender_scored,
    infer_gender_from_text,
    infer_gender_from_text_scored,
    GenderResult,
)


class TestInferGenderScored:
    def test_male_name_in_map(self):
        result = infer_gender_scored("JUAN")
        assert result.gender == "MASCULINO"
        assert result.confidence == 1.0
        assert result.source == "name_map"

    def test_female_name_in_map(self):
        result = infer_gender_scored("MARIA")
        assert result.gender == "FEMENINO"
        assert result.confidence == 1.0

    def test_empty_name(self):
        result = infer_gender_scored(None)
        assert result.gender == "NO ENCONTRADO"
        assert result.confidence == 0.0

    def test_name_not_in_map(self):
        result = infer_gender_scored("XYZUNKNOWN")
        assert result.gender == "NO ENCONTRADO"
        assert result.confidence == 0.0

    def test_compound_maria_jose(self):
        result = infer_gender_scored("MARIA JOSE")
        assert result.gender == "FEMENINO"
        assert result.confidence == 1.0
        assert result.source == "compound"

    def test_compound_jose_maria(self):
        result = infer_gender_scored("JOSE MARIA")
        assert result.gender == "MASCULINO"
        assert result.confidence == 1.0
        assert result.source == "compound"

    def test_compound_juan_carlos(self):
        result = infer_gender_scored("JUAN CARLOS")
        assert result.gender == "MASCULINO"
        assert result.source == "compound"

    def test_compound_three_word(self):
        result = infer_gender_scored("MARIA DE LOS ANGELES")
        assert result.gender == "FEMENINO"
        assert result.source == "compound"
        assert result.confidence == 1.0

    def test_compound_with_accents(self):
        result = infer_gender_scored("María José")
        assert result.gender == "FEMENINO"
        assert result.confidence == 1.0


class TestInferGenderLegacy:
    def test_legacy_returns_string(self):
        assert infer_gender("JUAN") == "MASCULINO"
        assert infer_gender("MARIA") == "FEMENINO"
        assert infer_gender("") == "NO ENCONTRADO"
        assert infer_gender(None) == "NO ENCONTRADO"


class TestInferGenderFromTextScored:
    def test_sexo_masculino(self):
        result = infer_gender_from_text_scored("Sexo: Masculino")
        assert result.gender == "MASCULINO"
        assert result.confidence == 0.7
        assert result.source == "text_sexo"

    def test_sexo_femenino(self):
        result = infer_gender_from_text_scored("Sexo: Femenino")
        assert result.gender == "FEMENINO"
        assert result.confidence == 0.7

    def test_honorific_sr(self):
        result = infer_gender_from_text_scored("Sr. Juan Pérez")
        assert result.gender == "MASCULINO"
        assert result.confidence == 0.6
        assert result.source == "text_honorific"

    def test_honorific_dona(self):
        result = infer_gender_from_text_scored("Doña María López")
        assert result.gender == "FEMENINO"
        assert result.confidence == 0.6

    def test_no_match(self):
        result = infer_gender_from_text_scored("Sin información")
        assert result.gender == "NO ENCONTRADO"
        assert result.confidence == 0.0
