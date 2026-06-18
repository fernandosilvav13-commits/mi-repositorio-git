"""Tests for Consolidator — fill_gaps, last_wins, smart modes."""
from app.services.consolidator import Consolidator


COLUMNS = ["RUT", "NOMBRES", "GENERO", "TELEFONO"]
NO_ENCONTRADO = "NO ENCONTRADO"


class TestConsolidatorFillGaps:
    def test_fill_gaps_default_mode(self):
        c = Consolidator()
        assert c.merge_mode == "fill_gaps"

    def test_fill_completes_missing(self):
        c = Consolidator()
        rows = [
            {"RUT": "12.345.678-5", "NOMBRES": "JUAN", "GENERO": NO_ENCONTRADO, "TELEFONO": ""},
            {"RUT": "12.345.678-5", "NOMBRES": NO_ENCONTRADO, "GENERO": "MASCULINO", "TELEFONO": "+56912345678"},
        ]
        result, _, _ = c.consolidate(COLUMNS, rows)
        assert len(result) == 1
        assert result[0]["NOMBRES"] == "JUAN"
        assert result[0]["GENERO"] == "MASCULINO"
        assert result[0]["TELEFONO"] == "+56912345678"

    def test_fill_does_not_override_valid(self):
        c = Consolidator()
        rows = [
            {"RUT": "12.345.678-5", "NOMBRES": "JUAN", "GENERO": "MASCULINO", "TELEFONO": ""},
            {"RUT": "12.345.678-5", "NOMBRES": "PEDRO", "GENERO": NO_ENCONTRADO, "TELEFONO": ""},
        ]
        result, _, _ = c.consolidate(COLUMNS, rows)
        assert result[0]["NOMBRES"] == "JUAN"

    def test_no_rut_column(self):
        c = Consolidator()
        rows = [{"NOMBRE": "JUAN", "EDAD": "30"}]
        result, _, _ = c.consolidate(["NOMBRE", "EDAD"], rows)
        assert len(result) == 1

    def test_rut_no_encontrado_standalone(self):
        c = Consolidator()
        rows = [
            {"RUT": "12.345.678-5", "NOMBRES": "JUAN", "GENERO": "", "TELEFONO": ""},
            {"RUT": NO_ENCONTRADO, "NOMBRES": "PEDRO", "GENERO": "", "TELEFONO": ""},
        ]
        result, _, _ = c.consolidate(COLUMNS, rows)
        assert len(result) == 2


class TestConsolidatorLastWins:
    def test_last_wins_overwrites(self):
        c = Consolidator(merge_mode="last_wins")
        rows = [
            {"RUT": "12.345.678-5", "NOMBRES": "JUAN", "GENERO": "MASCULINO", "TELEFONO": ""},
            {"RUT": "12.345.678-5", "NOMBRES": "PEDRO", "GENERO": NO_ENCONTRADO, "TELEFONO": ""},
        ]
        result, _, _ = c.consolidate(COLUMNS, rows)
        assert result[0]["NOMBRES"] == "PEDRO"

    def test_last_wins_multiple_rows(self):
        c = Consolidator(merge_mode="last_wins")
        rows = [
            {"RUT": "12.345.678-5", "NOMBRES": "A", "GENERO": "M", "TELEFONO": ""},
            {"RUT": "12.345.678-5", "NOMBRES": "B", "GENERO": "F", "TELEFONO": ""},
            {"RUT": "12.345.678-5", "NOMBRES": "C", "GENERO": "", "TELEFONO": ""},
        ]
        result, _, _ = c.consolidate(COLUMNS, rows)
        assert result[0]["NOMBRES"] == "C"
        assert result[0]["GENERO"] == ""


class TestConsolidatorSmart:
    def test_smart_no_conflict(self):
        c = Consolidator(merge_mode="smart")
        rows = [
            {"RUT": "12.345.678-5", "NOMBRES": "JUAN", "GENERO": NO_ENCONTRADO, "TELEFONO": ""},
            {"RUT": "12.345.678-5", "NOMBRES": NO_ENCONTRADO, "GENERO": "MASCULINO", "TELEFONO": ""},
        ]
        result, _, conflicts = c.consolidate(COLUMNS, rows)
        assert len(result) == 1
        assert result[0]["NOMBRES"] == "JUAN"
        assert result[0]["GENERO"] == "MASCULINO"
        assert len(conflicts) == 0

    def test_smart_detects_conflict(self):
        c = Consolidator(merge_mode="smart")
        rows = [
            {"RUT": "12.345.678-5", "NOMBRES": "JUAN", "GENERO": "MASCULINO", "TELEFONO": ""},
            {"RUT": "12.345.678-5", "NOMBRES": "PEDRO", "GENERO": "MASCULINO", "TELEFONO": ""},
        ]
        result, _, conflicts = c.consolidate(COLUMNS, rows)
        assert len(conflicts) == 1
        assert conflicts[0]["field"] == "NOMBRES"
        assert conflicts[0]["value_a"] == "JUAN"
        assert conflicts[0]["value_b"] == "PEDRO"

    def test_smart_inherits_fill_gaps(self):
        c = Consolidator(merge_mode="smart")
        rows = [
            {"RUT": "12.345.678-5", "NOMBRES": "JUAN", "GENERO": "MASCULINO", "TELEFONO": ""},
            {"RUT": "12.345.678-5", "NOMBRES": NO_ENCONTRADO, "GENERO": NO_ENCONTRADO, "TELEFONO": "+56912345678"},
        ]
        result, _, conflicts = c.consolidate(COLUMNS, rows)
        assert result[0]["TELEFONO"] == "+56912345678"
        assert len(conflicts) == 0


class TestConsolidatorInvalidMode:
    def test_invalid_mode_raises(self):
        try:
            Consolidator(merge_mode="invalid")
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestConsolidatorNormalizeRut:
    def test_normalize_with_dots_and_dash(self):
        assert Consolidator.normalize_rut("12.345.678-5") == "123456785"

    def test_normalize_no_encontrado(self):
        assert Consolidator.normalize_rut(NO_ENCONTRADO) == NO_ENCONTRADO

    def test_normalize_empty(self):
        assert Consolidator.normalize_rut("") == ""
