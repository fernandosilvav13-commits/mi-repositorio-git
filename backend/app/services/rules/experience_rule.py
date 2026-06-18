import re
from app.services.rules.base_rule import BaseRule
from app.services.rules.registry import rule_registry


MONTH_MAP = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}

EXPERIENCE_START = re.compile(
    r"^(?:\s*)(?:EXPERIENCIA|ANTECEDENTES\s+LABORALES|WORK\s+EXPERIENCE|"
    r"LABORAL\s+EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|HISTORIAL\s+LABORAL)",
    re.IGNORECASE,
)

SECTION_END = re.compile(
    r"^(?:\s*)(?:FORMACION|EDUCACION|ESTUDIOS|DATOS\s+PERSONALES|"
    r"NACIONALIDAD|IDIOMAS|HABILIDADES|SKILLS|COMPETENCIAS|CURSOS|"
    r"CERTIFICACIONES|CAPACITACIONES|REFERENCIAS|RESUMEN|PERFIL|"
    r"INFORMACION\s+(?:PERSONAL|ADICIONAL|COMPLEMENTARIA))",
    re.IGNORECASE,
)


def _get_experience_section(text: str) -> str:
    lines = text.split("\n")
    in_section = False
    section_lines = []

    for line in lines:
        if EXPERIENCE_START.search(line):
            in_section = True
        if in_section:
            if SECTION_END.search(line):
                break
            section_lines.append(line)

    if not section_lines:
        return text

    return "\n".join(section_lines)


def _parse_year(text: str) -> int | None:
    text = text.strip()
    if text.isdigit():
        year = int(text)
        if 1900 <= year <= 2099:
            return year
    return None


def _parse_year_from_date_str(date_str: str) -> int | None:
    date_str = date_str.strip()
    if re.match(r"^\d{4}$", date_str):
        return int(date_str)
    if re.match(r"^\d{1,2}/\d{4}$", date_str):
        return int(date_str.split("/")[1])
    if re.match(r"^\d{1,2}[-/]\d{1,2}[-/](\d{4})$", date_str):
        return int(re.search(r"(\d{4})$", date_str).group(1))
    return None


def _normalize_date_range_line(line: str) -> tuple[int | None, int | None]:
    line_clean = re.sub(r"\s+", " ", line.lower())
    date_patterns = [
        r"(\d{4})\s*[-–—a]+\s*(\d{4})",
        r"(\d{1,2}[-/]\d{4})\s*[-–—a]+\s*(\d{1,2}[-/]\d{4})",
        r"(\d{4})\s*[-–—a]+\s*(actualidad|presente|ahora|currently)",
        r"(?:desde\s+)?(\d{4})\s*(?:hasta|a|al?)\s*(\d{4})",
        r"(?:desde\s+)?(\d{1,2}[-/]\d{4})\s*(?:hasta|a|al?)\s*(\d{1,2}[-/]\d{4})",
        r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})\s*[-–—a]+\s*(actualidad|presente)",
    ]

    for pattern in date_patterns:
        m = re.search(pattern, line_clean, re.IGNORECASE)
        if m:
            parts = m.groups()
            if len(parts) == 2:
                if parts[1] in ("actualidad", "presente", "ahora", "currently"):
                    start = _parse_year_from_date_str(parts[0]) if not parts[0].isdigit() else _parse_year(parts[0])
                    return start, 2026
                start = _parse_year_from_date_str(parts[0]) if not parts[0].isdigit() else _parse_year(parts[0])
                end = _parse_year_from_date_str(parts[1]) if not parts[1].isdigit() else _parse_year(parts[1])
                return start, end

    return None, None


class YearsExperienceRule(BaseRule):
    name = "years_experience"
    description = "Calculate total years of professional experience from date ranges"
    field = "ANIOS_EXPERIENCIA"

    def evaluate(self, text: str, current_data: dict) -> str | None:
        existing = current_data.get("ANIOS_EXPERIENCIA", "")
        if existing and existing != "NO ENCONTRADO":
            return None

        experience_text = _get_experience_section(text)

        total_years = 0
        for line in experience_text.split("\n"):
            start, end = _normalize_date_range_line(line)
            if start is not None and end is not None and end > start:
                total_years += end - start

        if total_years > 0:
            return str(int(total_years))
        return None


rule_registry.register(YearsExperienceRule())
