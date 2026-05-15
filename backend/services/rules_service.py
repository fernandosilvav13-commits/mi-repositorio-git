from math import ceil


def apply_rules(row: dict, extracted: dict, columns: list) -> dict:
    return {
        "blue": _blue_flag(extracted),
        "yellow": _yellow_flag(row, extracted),
        "orange": _orange_flag(row, columns),
        "gray": _gray_flags(row, columns),
    }


def _blue_flag(extracted: dict) -> bool:
    experiences = extracted.get("experiencia_laboral", [])
    if not isinstance(experiences, list):
        return False
    current_count = sum(
        1 for exp in experiences if isinstance(exp, dict) and exp.get("incluye_actualidad") is True
    )
    return current_count > 3 or len(experiences) > 5


def _yellow_flag(row: dict, extracted: dict) -> bool:
    for key in ("NOMBRES", "APELLIDOS", "RUT"):
        val = row.get(key, "")
        if not val or val == "NO ENCONTRADO":
            return True
    experiences = extracted.get("experiencia_laboral", [])
    if not isinstance(experiences, list) or len(experiences) == 0:
        return True
    if row.get("TITULO_PROFESIONAL") == "NO ENCONTRADO":
        return True
    return False


def _orange_flag(row: dict, columns: list) -> bool:
    not_found_count = sum(1 for col in columns if row.get(col) == "NO ENCONTRADO")
    threshold = ceil(len(columns) * 0.5)
    return not_found_count >= threshold


def _gray_flags(row: dict, columns: list) -> dict:
    skip_columns = {"EXP1_MATRICULAS", "EXP2_MATRICULAS", "EXP3_MATRICULAS"}
    return {
        col: row.get(col) == "NO ENCONTRADO"
        for col in columns
        if col not in skip_columns
    }
