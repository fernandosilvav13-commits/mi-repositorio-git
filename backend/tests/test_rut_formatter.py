"""Tests for RUTFormatter — format, validate, extract."""
from app.utils.rut_formatter import RUTFormatter


class TestRUTFormatterValidate:
    def test_valid_rut_with_dots(self):
        assert RUTFormatter.validate("12.345.678-5") is True

    def test_valid_rut_no_format(self):
        assert RUTFormatter.validate("12345678-5") is True

    def test_invalid_dv(self):
        assert RUTFormatter.validate("12.345.678-9") is False

    def test_valid_rut_k_dv(self):
        assert RUTFormatter.validate("16.666.666-K") is True

    def test_valid_rut_lowercase_k(self):
        assert RUTFormatter.validate("16.666.666-k") is True

    def test_empty_string(self):
        assert RUTFormatter.validate("") is False

    def test_short_string(self):
        assert RUTFormatter.validate("123") is False

    def test_garbage_string(self):
        assert RUTFormatter.validate("abcdef") is False

    def test_known_valid_rut_140180122(self):
        assert RUTFormatter.validate("14.018.012-2") is True

    def test_known_valid_rut_103386861(self):
        assert RUTFormatter.validate("10.338.686-1") is True

    def test_known_valid_rut_187654321(self):
        assert RUTFormatter.validate("18.765.432-7") is True

    def test_known_valid_rut_no_dots(self):
        assert RUTFormatter.validate("14018012-2") is True

    def test_dv_zero_rut(self):
        assert RUTFormatter.validate("1.000.013-0") is True

    def test_rut_with_leading_zeros(self):
        assert RUTFormatter.validate("1.234.567-4") is True

    def test_random_invalid_rut(self):
        assert RUTFormatter.validate("1.111.111-1") is False

    def test_rut_with_spaces(self):
        assert RUTFormatter.validate(" 12.345.678-5 ") is True


class TestRUTFormatterFormat:
    def test_format_with_dots_and_dash(self):
        assert RUTFormatter.format("12345678-5") == "12.345.678-5"

    def test_format_already_formatted(self):
        assert RUTFormatter.format("12.345.678-5") == "12.345.678-5"

    def test_format_solo_guion(self):
        assert RUTFormatter.format("12.345.678-5", fmt="solo_guion") == "12345678-5"

    def test_format_sin_formato(self):
        assert RUTFormatter.format("12.345.678-5", fmt="sin_formato") == "123456785"

    def test_format_k_dv(self):
        assert RUTFormatter.format("12345678K") == "12.345.678-K"

    def test_format_short_returns_original(self):
        assert RUTFormatter.format("123") == "123"


class TestRUTFormatterExtract:
    def test_extract_single_rut(self):
        ruts = RUTFormatter.extract("Mi RUT es 12.345.678-5")
        assert "12.345.678-5" in ruts

    def test_extract_no_rut(self):
        ruts = RUTFormatter.extract("No hay RUT aquí")
        assert ruts == []

    def test_extract_multiple_ruts(self):
        ruts = RUTFormatter.extract("RUT 1: 12.345.678-5, RUT 2: 18.765.432-1")
        assert len(ruts) == 2

    def test_extract_rut_no_format(self):
        ruts = RUTFormatter.extract("RUN 12345678-5")
        assert len(ruts) >= 1
        assert "12345678-5" in ruts or "12.345.678-5" in ruts
