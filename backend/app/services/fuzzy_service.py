from rapidfuzz import fuzz, process


class FuzzyMatcher:
    def __init__(self, threshold: int = 70):
        self.threshold = threshold

    def match_value(self, value: str, choices: list[str]) -> tuple[str, int]:
        if not choices:
            return value, 100
        best_match, score, _ = process.extractOne(
            value, choices, scorer=fuzz.token_sort_ratio
        )
        if score >= self.threshold:
            return best_match, score
        return value, score

    def match_values_batch(
        self, values: list[str], choices: list[str]
    ) -> list[tuple[str, str, int]]:
        results = []
        for val in values:
            matched, score = self.match_value(val, choices)
            results.append((val, matched, score))
        return results

    def match_dict_fields(
        self, extracted: dict, expected_fields: list[str]
    ) -> dict:
        result = {}
        for field in expected_fields:
            raw_value = extracted.get(field, "NO ENCONTRADO")
            if isinstance(raw_value, str) and raw_value != "NO ENCONTRADO":
                matched, score = self.match_value(raw_value, [])
                result[field] = {
                    "value": matched,
                    "original": raw_value,
                    "score": score,
                    "fuzzy_applied": False,
                }
            else:
                result[field] = {
                    "value": raw_value,
                    "original": raw_value,
                    "score": 100,
                    "fuzzy_applied": False,
                }
        return result
