import pytest
from app.services.rules.registry import rule_registry


class TestNationalityRule:
    def test_chilean_nationality(self):
        rule = rule_registry.get("nationality")
        result = rule.evaluate("Nacionalidad: Chilena", {})
        assert result == "Chilena"

    def test_argentine_nationality(self):
        rule = rule_registry.get("nationality")
        result = rule.evaluate("Soy argentino y vivo en Buenos Aires", {})
        assert result == "Argentina"

    def test_no_match_returns_none(self):
        rule = rule_registry.get("nationality")
        result = rule.evaluate("Sin información de nacionalidad", {})
        assert result is None

    def test_does_not_override_existing(self):
        rule = rule_registry.get("nationality")
        result = rule.evaluate("Chileno", {"NACIONALIDAD": "Argentina"})
        assert result is None


class TestDateOfBirthRule:
    def test_dob_dd_mm_yyyy(self):
        rule = rule_registry.get("date_of_birth")
        result = rule.evaluate("Fecha de Nacimiento: 15/03/1990", {})
        assert result == "15/03/1990"

    def test_dob_dash_format(self):
        rule = rule_registry.get("date_of_birth")
        result = rule.evaluate("Nacimiento: 01-12-1985", {})
        assert result == "01/12/1985"

    def test_no_match(self):
        rule = rule_registry.get("date_of_birth")
        result = rule.evaluate("Sin fecha de nacimiento", {})
        assert result is None


class TestYearsExperienceRule:
    def test_experience_2020_2026(self):
        rule = rule_registry.get("years_experience")
        text = "Ingeniero | Empresa | 2020 - 2026"
        result = rule.evaluate(text, {})
        assert result is not None
        assert int(result) >= 5

    def test_multiple_jobs_summed(self):
        rule = rule_registry.get("years_experience")
        text = """
        Trabajo 1: Empresa A | 2015 - 2020
        Trabajo 2: Empresa B | 2020 - 2024
        """
        result = rule.evaluate(text, {})
        assert result is not None
        total = int(result)
        assert total >= 8

    def test_single_job(self):
        rule = rule_registry.get("years_experience")
        text = "Analista | Empresa | 2018 - 2023"
        result = rule.evaluate(text, {})
        assert result == "5"

    def test_no_dates_returns_none(self):
        rule = rule_registry.get("years_experience")
        text = "Experiencia laboral: sin fechas especificas"
        result = rule.evaluate(text, {})
        assert result is None

    def test_education_dates_not_counted(self):
        rule = rule_registry.get("years_experience")
        text = """
EXPERIENCIA LABORAL
Ingeniero | Empresa A | 2020 - 2024

FORMACION ACADEMICA
Universidad | 2015 - 2020
        """
        result = rule.evaluate(text, {})
        assert result == "4"

    def test_experience_section_only(self):
        rule = rule_registry.get("years_experience")
        text = """
DATOS PERSONALES
Nombre: Juan Perez

EXPERIENCIA LABORAL
Jefe de Proyecto | Empresa X | 2018 - 2022
Analista | Empresa Y | 2022 - 2026

IDIOMAS
Ingles avanzado
Frances basico
        """
        result = rule.evaluate(text, {})
        assert result == "8"

    def test_no_experience_section_fallback_to_full_text(self):
        rule = rule_registry.get("years_experience")
        text = """
Trabajo como ingeniero desde 2018 hasta 2024 en diversas empresas.
Anteriormente trabaje como analista 2015 - 2018.
        """
        result = rule.evaluate(text, {})
        assert result == "9"

    def test_mixed_sections_only_experience_counted(self):
        rule = rule_registry.get("years_experience")
        text = """
EXPERIENCIA LABORAL
Profesor | Colegio A | 2019 - 2024

FORMACION
Magister | Universidad | 2017 - 2019
Pregrado | Universidad | 2013 - 2017

CURSOS
Curso de Python | 2023 - 2023
        """
        result = rule.evaluate(text, {})
        assert result == "5"

    def test_empty_experience_section_returns_none(self):
        rule = rule_registry.get("years_experience")
        text = """
EXPERIENCIA LABORAL
Sin fechas registradas

FORMACION
Universidad | 2015 - 2020
        """
        result = rule.evaluate(text, {})
        assert result is None


class TestEducationLevelRule:
    def test_doctorado_detected(self):
        rule = rule_registry.get("education_level")
        text = "FORMACION ACADEMICA Doctorado en Ciencias"
        result = rule.evaluate(text, {})
        assert result == "DOCTORADO"

    def test_magister_detected(self):
        rule = rule_registry.get("education_level")
        text = "Magister en Administracion de Empresas"
        result = rule.evaluate(text, {})
        assert result == "MAGISTER"

    def test_highest_level_returned(self):
        rule = rule_registry.get("education_level")
        text = """
        Tecnico en Computacion - DUOC 2015
        Ingenieria en Computacion - Universidad 2018
        Magister en Data Science - 2021
        """
        result = rule.evaluate(text, {})
        assert result == "MAGISTER"

    def test_tecnico_detected(self):
        rule = rule_registry.get("education_level")
        text = "Tecnico en Enfermeria"
        result = rule.evaluate(text, {})
        assert result == "TECNICO"

    def test_no_match_returns_none(self):
        rule = rule_registry.get("education_level")
        text = "Sin educacion formal"
        result = rule.evaluate(text, {})
        assert result is None


class TestEmailDomainRule:
    def test_gmail_detected(self):
        rule = rule_registry.get("email_domain")
        result = rule.evaluate("", {"EMAIL": "user@gmail.com"})
        assert result == "Gmail"

    def test_outlook_detected(self):
        rule = rule_registry.get("email_domain")
        result = rule.evaluate("", {"EMAIL": "user@outlook.com"})
        assert result == "Outlook"

    def test_corporate_domain(self):
        rule = rule_registry.get("email_domain")
        result = rule.evaluate("", {"EMAIL": "user@empresa.cl"})
        assert result == "empresa.cl"

    def test_no_email_returns_none(self):
        rule = rule_registry.get("email_domain")
        result = rule.evaluate("", {"EMAIL": ""})
        assert result is None

    def test_email_in_text(self):
        rule = rule_registry.get("email_domain")
        result = rule.evaluate("mi correo es user@yahoo.com", {"EMAIL": ""})
        assert result == "Yahoo"


class TestRuleRegistry:
    def test_all_five_rules_registered(self):
        rules = rule_registry.get_all()
        assert len(rules) == 5

    def test_get_by_field(self):
        rules = rule_registry.get_by_field("NACIONALIDAD")
        assert len(rules) == 1
        assert rules[0].name == "nationality"
