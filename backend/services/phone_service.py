import re

AREA_CODES = {
    "2": "Santiago", "32": "Valparaíso", "33": "Los Andes",
    "34": "San Felipe", "35": "San Antonio", "41": "Concepción",
    "42": "Chillán", "43": "Talcahuano", "45": "Temuco",
    "51": "La Serena", "52": "Copiapó", "53": "Ovalle",
    "55": "Antofagasta", "57": "Iquique", "58": "Arica",
    "61": "Punta Arenas", "63": "Valdivia", "64": "Osorno",
    "65": "Puerto Montt", "66": "Coyhaique", "67": "Rancagua",
    "71": "Talca", "72": "Curicó", "73": "Linares",
    "75": "Rengo", "9": "Móvil",
}

FIXO_AREA_CODES = {k: v for k, v in AREA_CODES.items() if k != "9"}


def normalize_phone(raw: str | None) -> tuple[str, str]:
    if not raw:
        return ("NO ENCONTRADO", "NO ENCONTRADO")

    cleaned = raw.strip()

    cleaned = cleaned.lower()
    prefixes = [
        "cel:", "celular:", "fono:", "tel:", "telefono:",
        "whatsapp:", "wp:", "contacto:", "movil:", "+56", "+56 ",
    ]
    for p in prefixes:
        cleaned = cleaned.replace(p, "")

    cleaned = re.sub(r"[\s\-\.\(\)\/]", "", cleaned)

    if not cleaned:
        return ("NO ENCONTRADO", "NO ENCONTRADO")

    digits = re.sub(r"\D", "", cleaned)

    if not digits:
        return ("NO ENCONTRADO", "NO ENCONTRADO")

    if digits.startswith("09") and len(digits) == 10:
        formatted = "+569" + digits[2:]
        return ("TELEFONO_CELULAR", formatted)

    if digits.startswith("9") and len(digits) == 9:
        formatted = "+569" + digits[1:]
        return ("TELEFONO_CELULAR", formatted)

    if len(digits) == 9 and digits.startswith("9"):
        formatted = "+569" + digits[1:]
        return ("TELEFONO_CELULAR", formatted)

    sorted_codes = sorted(FIXO_AREA_CODES.keys(), key=len, reverse=True)
    for code in sorted_codes:
        if digits.startswith(code):
            rest = digits[len(code):]
            if 6 <= len(rest) <= 8:
                formatted = "+56" + code + rest
                return ("TELEFONO_FIJO", formatted)

    return ("NO ENCONTRADO", "NO ENCONTRADO")


def extract_phone_from_text(text: str) -> tuple[str, str]:
    if not text:
        return ("NO ENCONTRADO", "NO ENCONTRADO")

    patterns = [
        r'(?:cel|celular|movil|móvil|whatsapp|wp|contacto)\s*[:\s]*(\+?56?\s*9\s*[\d\s\-\.]{7,12})',
        r'(?:fono|tel|telefono|teléfono|fijo)\s*[:\s]*(\+?56?\s*[2-9]\s*[\d\s\-\.]{6,11})',
        r'(\+569[\d\s\-\.]{7,9})',
        r'(\+562[\d\s\-\.]{6,8})',
        r'(09[\d\s\-\.]{7,9})',
        r'(9[\s\-\.]?\d[\s\-\.]?\d[\s\-\.]?\d[\s\-\.]?\d[\s\-\.]?\d[\s\-\.]?\d[\s\-\.]?\d[\s\-\.]?\d)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw = match.group(1)
            return normalize_phone(raw)

    return ("NO ENCONTRADO", "NO ENCONTRADO")


def deduplicate_phones(row: dict) -> dict:
    fijo = row.get("TELEFONO_FIJO", "NO ENCONTRADO")
    cel = row.get("TELEFONO_CELULAR", "NO ENCONTRADO")
    if fijo != "NO ENCONTRADO" and fijo == cel:
        row["TELEFONO_FIJO"] = "NO ENCONTRADO"
    return row
