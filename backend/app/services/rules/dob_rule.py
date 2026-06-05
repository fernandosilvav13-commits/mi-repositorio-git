import re
from app.services.rules.base_rule import BaseRule
from app.services.rules.registry import rule_registry


class DateOfBirthRule(BaseRule):
    name = "date_of_birth"
    description = "Infer date of birth from document text"
    field = "FECHA_NACIMIENTO"

    def evaluate(self, text: str, current_data: dict) -> str | None:
        existing = current_data.get("FECHA_NACIMIENTO", "")
        if existing and existing != "NO ENCONTRADO":
            return None

        dob_patterns = [
            r"(?:fecha\s+de\s+)?naci(?:mient[oa])?\s*:?\s*(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})",
            r"(?:fecha\s+de\s+)?naci(?:mient[oa])?\s*:?\s*(\d{1,2})\s+de\s+([a-záéíóúñ]+)\s+de\s+(\d{4})",
            r"(?:fecha\s+de\s+)?nacimiento\s*:?\s*(\d{1,2})\.(\d{1,2})\.(\d{4})",
            r"(?:fecha\s+de\s+)?nac\.?\s*:?\s*(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})",
        ]

        text_lower = text.lower()
        for pattern in dob_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if len(match.groups()) == 3:
                    dd, mm, yyyy = match.groups()
                    if len(yyyy) == 2:
                        yyyy = "19" + yyyy if int(yyyy) > 25 else "20" + yyyy
                    return f"{dd.zfill(2)}/{mm.zfill(2)}/{yyyy}"
                elif len(match.groups()) == 3:
                    dd, month_str, yyyy = match.groups()
                    month_map = {
                        "enero": "01", "febrero": "02", "marzo": "03",
                        "abril": "04", "mayo": "05", "junio": "06",
                        "julio": "07", "agosto": "08", "septiembre": "09",
                        "octubre": "10", "noviembre": "11", "diciembre": "12",
                    }
                    mm = month_map.get(month_str, "01")
                    return f"{dd.zfill(2)}/{mm}/{yyyy}"

        return None


rule_registry.register(DateOfBirthRule())
