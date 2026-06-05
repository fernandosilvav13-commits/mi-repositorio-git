import re

MONTHS = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
    "ene": 1, "feb": 2, "mar": 3, "abr": 4,
    "may": 5, "jun": 6, "jul": 7, "ago": 8,
    "sep": 9, "oct": 10, "nov": 11, "dic": 12,
}

STOP_WORDS = {"de", "la", "el", "del", "los", "las", "y", "e", "a",
              "en", "con", "por", "para", "un", "una", "san", "santa",
              "don", "doña"}

PREFIXES = [
    "liceo politecnico ", "escuela basica ", "liceo ", "colegio ",
    "escuela ", "instituto ", "centro ", "high school ",
]


def _parse_year_from_string(text: str) -> int | None:
    if not text:
        return None

    # "2020-2023" -> 2023
    m = re.search(r"(\d{4})\s*[-–]\s*(\d{4})", text)
    if m:
        return int(m.group(2))

    # "Enero 2020 - Diciembre 2022"
    m = re.search(r"[-–]\s*(?:[a-zA-ZñÑáéíóú]+)\s+(\d{4})", text)
    if m:
        return int(m.group(1))

    # "Mar 2018" or "2018"
    m = re.search(r"(\d{4})", text)
    if m:
        return int(m.group(1))

    return None


def _sort_key(exp: dict) -> tuple:
    # Group 0: currently working (True -> 0, False -> 1)
    group = 0 if exp.get("incluye_actualidad") else 1

    # Parse fecha_termino
    ft = exp.get("fecha_termino")
    year = _parse_year_from_string(ft) if ft else None

    if year is not None:
        return (group, -year, 0)

    # Try duracion
    dur = exp.get("duracion")
    year = _parse_year_from_string(dur) if dur else None
    if year is not None:
        return (group, -year, 1)

    # No date info -> bottom
    return (group, 0, 2)


def sort_experiences(exps: list) -> list:
    return sorted(exps, key=_sort_key)


def _normalize(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def _match_exact(name: str, lookup: dict) -> str | None:
    norm = _normalize(name)
    for key in lookup:
        if key == norm:
            return key
    return None


def _match_strip_prefixes(name: str, lookup: dict) -> str | None:
    norm = _normalize(name)
    for prefix in PREFIXES:
        if norm.startswith(prefix):
            stripped = norm[len(prefix):]
            for key in lookup:
                if key == stripped:
                    return key
    return None


def _match_substring(name: str, lookup: dict) -> str | None:
    norm = _normalize(name)
    for key in lookup:
        if norm in key or key in norm:
            return key
    return None


def _significant_words(name: str) -> list[str]:
    return [w for w in _normalize(name).split() if w not in STOP_WORDS]


def _match_first_two_words(name: str, lookup: dict) -> str | None:
    words = _significant_words(name)
    if len(words) < 2:
        return None
    candidate = f"{words[0]} {words[1]}"
    for key in lookup:
        if candidate in key:
            return key
    return None


def _match_fuzzy(name: str, lookup: dict) -> str | None:
    try:
        from rapidfuzz import fuzz
    except ImportError:
        return None
    norm = _normalize(name)
    best_score = 0
    best_key = None
    for key in lookup:
        score = fuzz.partial_ratio(norm, key)
        if score > best_score:
            best_score = score
            best_key = key
    if best_score >= 75:
        return best_key
    return None


def crossref_experiences(exps: list, me_lookup: dict) -> list:
    result = []
    for exp in exps:
        name = exp.get("establecimiento", "")
        match_key = (
            _match_exact(name, me_lookup)
            or _match_strip_prefixes(name, me_lookup)
            or _match_substring(name, me_lookup)
            or _match_first_two_words(name, me_lookup)
            or _match_fuzzy(name, me_lookup)
        )
        if match_key:
            exp["matricula"] = str(me_lookup[match_key]["MAT_TOTAL"])
        else:
            exp["matricula"] = "NO ENCONTRADO"
        result.append(exp)
    return result[:3]


def get_top_3_experiences(exps: list, me_lookup: dict) -> list:
    sorted_exps = sort_experiences(exps)
    return crossref_experiences(sorted_exps, me_lookup)
