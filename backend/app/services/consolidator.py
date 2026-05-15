import re
from typing import Any

NO_ENCONTRADO = "NO ENCONTRADO"

RUT_COLUMN_PATTERNS = re.compile(
    r"^(rut|run|rut\s*candidato|documento)$", re.IGNORECASE
)


class Consolidator:
    def detect_rut_column(self, columns: list[str]) -> str | None:
        for col in columns:
            if RUT_COLUMN_PATTERNS.match(col.strip()):
                return col
        return None

    @staticmethod
    def normalize_rut(value: str) -> str:
        if not value or value == NO_ENCONTRADO:
            return value
        return re.sub(r"[^a-zA-Z0-9]", "", value).upper()

    def consolidate(
        self,
        columns: list[str],
        rows: list[dict],
        rules_triggered: list[list[dict]] | None = None,
    ) -> tuple[list[dict], list[list[dict]]]:
        rut_col = self.detect_rut_column(columns)
        if rut_col is None:
            return rows, (rules_triggered or [[] for _ in rows])

        groups: dict[str, dict] = {}
        rules_map: dict[str, list[dict]] = {}
        standalone_rows: list[dict] = []
        standalone_rules: list[list[dict]] = []

        for idx, row in enumerate(rows):
            raw_rut = row.get(rut_col, "")
            normalized = self.normalize_rut(raw_rut)

            if not normalized or normalized == self.normalize_rut(NO_ENCONTRADO):
                standalone_rows.append(row)
                if rules_triggered is not None:
                    standalone_rules.append(rules_triggered[idx])
                continue

            if normalized not in groups:
                groups[normalized] = dict(row)
                if rules_triggered is not None:
                    rules_map[normalized] = list(rules_triggered[idx])
            else:
                existing = groups[normalized]
                for col in columns:
                    if existing.get(col, "") == NO_ENCONTRADO:
                        val = row.get(col, NO_ENCONTRADO)
                        if val != NO_ENCONTRADO:
                            existing[col] = val
                if rules_triggered is not None:
                    existing_rules = rules_map[normalized]
                    for rule in rules_triggered[idx]:
                        if rule not in existing_rules:
                            existing_rules.append(rule)

        consolidated_rows: list[dict] = list(groups.values()) + standalone_rows

        if rules_triggered is not None:
            consolidated_rules: list[list[dict]] = (
                list(rules_map.values()) + standalone_rules
            )
        else:
            consolidated_rules = [[] for _ in consolidated_rows]

        return consolidated_rows, consolidated_rules
