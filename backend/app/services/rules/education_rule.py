import re
from app.services.rules.base_rule import BaseRule
from app.services.rules.registry import rule_registry


EDUCATION_LEVELS = [
    (r"\bdoctorado\b|\bphd\b|\bph\.d\b|\bph\.d\.\b|\bd\.\s*phil\b", "DOCTORADO"),
    (r"\bmag[íi]ster\b|\bmaestr[íi]a\b|\bmaster\b|\bmsc\b|\bm\.?\s*sc\b|\bm\.?\s*eng\b", "MAGISTER"),
    (r"\bpostgrad[oa]\b|\bdiplomad[oa]\b|\bespecializaci[óo]n\b|\b(?:curs[oa]|curso)\s+de\s+(?:post|pos)grado\b", "POSTGRADO"),
    (r"\b(?:ingenier[íi]a|licenciatura|título)\s+(?:en\s+)?\w|\(?pregrado\)?|\bbachelor\b|\bb\.?\s*a\b|\bb\.?\s*eng\b|\bb\.?\s*sc\b", "PREGRADO"),
    (r"\bt[eé]cnic[oa]\s+(?:en\s+)?\w|\(?t[eé]cnico\)?|\bt[eé]cnolog[íi]o\b|\bt[eé]cnico\s+superior\b", "TECNICO"),
]

LEVEL_ORDER = ["DOCTORADO", "MAGISTER", "POSTGRADO", "PREGRADO", "TECNICO"]


class EducationLevelRule(BaseRule):
    name = "education_level"
    description = "Detect highest education level from document text"
    field = "NIVEL_EDUCACION"

    def evaluate(self, text: str, current_data: dict) -> str | None:
        existing = current_data.get("NIVEL_EDUCACION", "")
        if existing and existing != "NO ENCONTRADO":
            return None

        text_lower = text.lower()
        detected_levels = set()
        for pattern, level in EDUCATION_LEVELS:
            if re.search(pattern, text_lower):
                detected_levels.add(level)

        if not detected_levels:
            for line in text.split("\n"):
                line = line.strip()
                if re.search(r"(?:universidad|instituto|escuela)\s+(?:de\s+)?\w", line.lower()):
                    detected_levels.add("PREGRADO")
                    break

        for level in LEVEL_ORDER:
            if level in detected_levels:
                return level

        return None


rule_registry.register(EducationLevelRule(enabled=True))
