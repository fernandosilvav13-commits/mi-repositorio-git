import pytest
from app.services.cv_processor import CVProcessor
from app.services.rules.registry import rule_registry


@pytest.fixture
def processor():
    return CVProcessor()


class TestRulesIntegration:
    def test_nationality_rule_in_post_process(self, processor):
        data = {
            "NOMBRES": "Juan",
            "APELLIDOS": "Perez",
            "RUT": "",
            "GENERO": "",
            "TELEFONO_CELULAR": "",
            "TELEFONO_FIJO": "",
            "NACIONALIDAD": "NO ENCONTRADO",
        }
        text = "Nacionalidad: Chilena. Experiencia laboral..."
        result = processor._post_process(data, raw_text=text)
        assert result.get("NACIONALIDAD") is not None

    def test_nationality_rule_does_not_override_llm(self, processor):
        data = {
            "NOMBRES": "Juan",
            "APELLIDOS": "Perez",
            "RUT": "",
            "GENERO": "",
            "TELEFONO_CELULAR": "",
            "TELEFONO_FIJO": "",
            "NACIONALIDAD": "Argentina",
        }
        text = "Soy Chileno y vivo en Santiago"
        result = processor._post_process(data, raw_text=text)
        assert result["NACIONALIDAD"] == "Argentina"

    def test_rules_dont_crash_on_empty_text(self, processor):
        data = {
            "NOMBRES": "Maria",
            "APELLIDOS": "Garcia",
            "RUT": "",
            "GENERO": "",
            "TELEFONO_CELULAR": "",
            "TELEFONO_FIJO": "",
        }
        result = processor._post_process(data, raw_text="")
        assert result is not None

    def test_rules_all_run_in_shadow(self, processor):
        data = {
            "NOMBRES": "Maria",
            "APELLIDOS": "Garcia",
            "RUT": "12345678-9",
            "GENERO": "FEMENINO",
            "TELEFONO_CELULAR": "",
            "TELEFONO_FIJO": "",
            "EMAIL": "",
        }
        text = """
EXPERIENCIA LABORAL
Profesora | Colegio San Javier | 2018 - Presente
Jefa de Departamento | Colegio Los Andes | 2015 - 2018

FORMACION
Magister en Educacion - Universidad de Chile 2020
Profesora de Educacion Basica - Universidad Metropolitana 2015

DATOS PERSONALES
Nacionalidad: Chilena
Fecha de Nacimiento: 15/03/1985
        """
        result = processor._post_process(data, raw_text=text)
        assert result["RUT"] == "12.345.678-9"
