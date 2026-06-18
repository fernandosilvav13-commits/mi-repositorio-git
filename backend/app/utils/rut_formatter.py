import re


class RUTFormatter:
    FORMATS = {
        "con_puntos_y_guion": r"^\d{1,3}(?:\.\d{3})*-[\dkK]$",
        "solo_guion": r"^\d+-[\dkK]$",
        "sin_formato": r"^\d{7,8}[\dkK]$",
    }

    @staticmethod
    def format(value: str, fmt: str = "con_puntos_y_guion") -> str:
        digits = re.sub(r"[^\dkK]", "", value)
        if not digits or len(digits) < 8:
            return value
        body = digits[:-1]
        dv = digits[-1]
        match fmt:
            case "con_puntos_y_guion":
                body_fmt = f"{int(body):,}".replace(",", ".")
                return f"{body_fmt}-{dv}"
            case "solo_guion":
                return f"{body}-{dv}"
            case "sin_formato":
                return f"{body}{dv}"
            case _:
                return f"{body}-{dv}"

    @staticmethod
    def validate(value: str) -> bool:
        clean = re.sub(r"[^0-9kK]", "", value)
        if not clean or len(clean) < 8:
            return False
        body = clean[:-1]
        dv = clean[-1].upper()
        weights = [2, 3, 4, 5, 6, 7]
        total = 0
        for i, digit in enumerate(reversed(body)):
            total += int(digit) * weights[i % len(weights)]
        remainder = 11 - (total % 11)
        if remainder == 11:
            expected = "0"
        elif remainder == 10:
            expected = "K"
        else:
            expected = str(remainder)
        return dv == expected

    @staticmethod
    def extract(text: str) -> list[str]:
        pattern = r"\b\d{7,8}-?[\dkK]\b|\b\d{1,3}(?:\.\d{3})*-[\dkK]\b"
        return re.findall(pattern, text)
