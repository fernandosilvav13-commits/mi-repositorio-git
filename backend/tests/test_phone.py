"""Tests for phone_service — normalize_phone, extract_phone_from_text."""
from app.services.phone_service import normalize_phone, extract_phone_from_text


class TestNormalizePhoneChilean:
    def test_chilean_mobile_with_09(self):
        _type, formatted = normalize_phone("09 1234 5678")
        assert _type == "TELEFONO_CELULAR"
        assert formatted == "+56912345678"

    def test_chilean_mobile_with_9(self):
        _type, formatted = normalize_phone("9 1234 5678")
        assert _type == "TELEFONO_CELULAR"
        assert formatted == "+56912345678"

    def test_chilean_mobile_plus56(self):
        _type, formatted = normalize_phone("+569 1234 5678")
        assert _type == "TELEFONO_CELULAR"
        assert formatted == "+56912345678"

    def test_chilean_landline_santiago(self):
        _type, formatted = normalize_phone("2 2123 4567")
        assert _type == "TELEFONO_FIJO"
        assert formatted == "+56221234567"

    def test_chilean_landline_concepcion(self):
        _type, formatted = normalize_phone("41 234 5678")
        assert _type == "TELEFONO_FIJO"
        assert formatted == "+56412345678"

    def test_chilean_landline_talca(self):
        _type, formatted = normalize_phone("71 234 5678")
        assert _type == "TELEFONO_FIJO"
        assert formatted == "+56712345678"

    def test_chilean_mobile_cel_prefix(self):
        _type, formatted = normalize_phone("cel: 9 1234 5678")
        assert _type == "TELEFONO_CELULAR"
        assert formatted == "+56912345678"

    def test_chilean_mobile_fono_prefix(self):
        _type, formatted = normalize_phone("fono: 9 8765 4321")
        assert _type == "TELEFONO_CELULAR"
        assert formatted == "+56987654321"


class TestNormalizePhoneInternational:
    def test_us_number(self):
        _type, formatted = normalize_phone("+1 555 123 4567")
        assert _type == "TELEFONO_EXTRANJERO"
        assert "1" in formatted
        assert len(formatted) >= 11

    def test_spain_number(self):
        _type, formatted = normalize_phone("+34 91 123 4567")
        assert _type == "TELEFONO_EXTRANJERO"
        assert formatted.startswith("+34")

    def test_uk_number(self):
        _type, formatted = normalize_phone("+44 20 7946 0958")
        assert _type == "TELEFONO_EXTRANJERO"
        assert formatted.startswith("+44")


class TestNormalizePhoneInvalid:
    def test_empty(self):
        _type, formatted = normalize_phone("")
        assert _type == "NO ENCONTRADO"

    def test_none(self):
        _type, formatted = normalize_phone(None)
        assert _type == "NO ENCONTRADO"

    def test_short_mobile(self):
        _type, formatted = normalize_phone("9 1234")
        assert _type == "FORMATO_INVALIDO"

    def test_garbage(self):
        _type, formatted = normalize_phone("abcdef")
        assert _type == "NO ENCONTRADO"


class TestExtractPhoneFromText:
    def test_extract_mobile(self):
        _type, formatted = extract_phone_from_text("Celular: 9 1234 5678")
        assert _type == "TELEFONO_CELULAR"
        assert formatted == "+56912345678"

    def test_extract_landline(self):
        _type, formatted = extract_phone_from_text("telefono: 2 2123 4567")
        assert _type == "TELEFONO_FIJO"
        assert formatted == "+56221234567"

    def test_extract_no_match(self):
        _type, formatted = extract_phone_from_text("Sin teléfono")
        assert _type == "NO ENCONTRADO"
