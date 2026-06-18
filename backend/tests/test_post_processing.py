"""Tests for post-processing pipeline — _titlecase_name and _post_process."""

from app.services.cv_processor import CVProcessor, _titlecase_name


# ── Unit tests for _titlecase_name() ──────────────────────────────────────────


def test_titlecase_all_caps_with_accent():
    assert _titlecase_name("MARÍA GARCÍA") == "María García"


def test_titlecase_lowercase_with_accent():
    assert _titlecase_name("juan pérez") == "Juan Pérez"


def test_titlecase_unchanged():
    assert _titlecase_name("María García") == "María García"


def test_titlecase_no_encontrado():
    assert _titlecase_name("NO ENCONTRADO") == "NO ENCONTRADO"


# ── Unit tests for _post_process() — gender ──────────────────────────────────


def test_post_process_gender_inferred_when_missing():
    processor = CVProcessor()
    data = {"GENERO": "", "NOMBRES": "MARÍA", "APELLIDOS": ""}
    result = processor._post_process(data)
    assert result["GENERO"] == "FEMENINO"


def test_post_process_gender_not_overridden():
    processor = CVProcessor()
    data = {"GENERO": "MASCULINO", "NOMBRES": "MARÍA", "APELLIDOS": ""}
    result = processor._post_process(data)
    assert result["GENERO"] == "MASCULINO"


# ── Unit tests for _post_process() — phone ───────────────────────────────────


def test_post_process_phone_normalized():
    processor = CVProcessor()
    data = {
        "GENERO": "MASCULINO",
        "NOMBRES": "Juan",
        "APELLIDOS": "Pérez",
        "TELEFONO_CELULAR": "09 1234 5678",
        "TELEFONO_FIJO": "",
        "RUT": "",
    }
    result = processor._post_process(data)
    assert result["TELEFONO_CELULAR"] == "+56912345678"


# ── Unit tests for _post_process() — RUT ─────────────────────────────────────


def test_post_process_rut_formatted():
    processor = CVProcessor()
    data = {
        "GENERO": "MASCULINO",
        "NOMBRES": "Juan",
        "APELLIDOS": "Pérez",
        "TELEFONO_CELULAR": "",
        "TELEFONO_FIJO": "",
        "RUT": "12345678-9",
    }
    result = processor._post_process(data)
    assert result["RUT"] == "12.345.678-9"
    # 12345678-9: expected DV is 5, actual is 9 → invalid
    assert result["RUT_VALIDO"] == "NO"


def test_post_process_rut_already_formatted():
    processor = CVProcessor()
    data = {
        "GENERO": "MASCULINO",
        "NOMBRES": "Juan",
        "APELLIDOS": "Pérez",
        "TELEFONO_CELULAR": "",
        "TELEFONO_FIJO": "",
        "RUT": "12.345.678-9",
    }
    result = processor._post_process(data)
    assert result["RUT"] == "12.345.678-9"
    # 12345678-9: expected DV is 5, actual is 9 → invalid
    assert result["RUT_VALIDO"] == "NO"


# ── Unit tests for _post_process() — name capitalize ─────────────────────────


def test_post_process_name_capitalized():
    processor = CVProcessor()
    data = {
        "GENERO": "",
        "NOMBRES": "MARÍA GARCÍA",
        "APELLIDOS": "LÓPEZ",
        "TELEFONO_CELULAR": "",
        "TELEFONO_FIJO": "",
        "RUT": "",
    }
    result = processor._post_process(data)
    assert result["NOMBRES"] == "María García"
    assert result["APELLIDOS"] == "López"


# ── Integration tests ────────────────────────────────────────────────────────


def test_process_full_pipeline():
    """Test _post_process with realistic EXTRACTION_SCHEMA-shaped data."""
    processor = CVProcessor()
    data = {
        "NOMBRES": "MARÍA FERNANDA",
        "APELLIDOS": "GARCÍA LÓPEZ",
        "RUT": "18765432-7",
        "GENERO": "NO ENCONTRADO",
        "TELEFONO_CELULAR": "09 8765 4321",
        "TELEFONO_FIJO": "",
        "EMAIL": "maria@example.com",
    }
    result = processor._post_process(data)
    assert result["GENERO"] == "FEMENINO"
    assert result["GENERO_CONFIANZA"] == "1.0"
    assert result["GENERO_FUENTE"] in ("compound", "name_map")
    assert result["TELEFONO_CELULAR"] == "+56987654321"
    assert result["RUT"] == "18.765.432-7"
    # 18765432-7: expected DV is 7, body 18765432
    assert result["RUT_VALIDO"] == "SI"
    assert result["NOMBRES"] == "María Fernanda"
    assert result["APELLIDOS"] == "García López"


def test_process_llm_fields_not_overridden():
    """Prove that post-processing does NOT override valid LLM output."""
    processor = CVProcessor()
    data = {
        "NOMBRES": "Juan",
        "APELLIDOS": "Pérez",
        "RUT": "12.345.678-9",
        "GENERO": "MASCULINO",
        "TELEFONO_CELULAR": "+56912345678",
        "TELEFONO_FIJO": "",
    }
    result = processor._post_process(data)
    assert result["GENERO"] == "MASCULINO"
    assert result["TELEFONO_CELULAR"] == "+56912345678"
    assert result["RUT"] == "12.345.678-9"
