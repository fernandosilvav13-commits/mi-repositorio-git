import re
from typing import Any


class RulesEngine:
    def __init__(self):
        self.operators = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: float(a) > float(b),
            "<": lambda a, b: float(a) < float(b),
            ">=": lambda a, b: float(a) >= float(b),
            "<=": lambda a, b: float(a) <= float(b),
            "contains": lambda a, b: str(b).lower() in str(a).lower(),
            "not_contains": lambda a, b: str(b).lower() not in str(a).lower(),
            "count>": lambda a, b: len(str(a).split(",")) > int(b),
            "count<": lambda a, b: len(str(a).split(",")) < int(b),
            "count>=": lambda a, b: len(str(a).split(",")) >= int(b),
            "count<=": lambda a, b: len(str(a).split(",")) <= int(b),
            "is_empty": lambda a, _: not a or str(a).strip() == "",
            "is_not_empty": lambda a, _: bool(a and str(a).strip()),
        }

    def evaluate_condition(self, condition: dict, data: dict) -> bool:
        field = condition["field"]
        operator = condition["operator"]
        expected_value = condition.get("value")
        actual_value = data.get(field, "")

        op_fn = self.operators.get(operator)
        if not op_fn:
            raise ValueError(f"Operador no soportado: {operator}")

        try:
            return op_fn(actual_value, expected_value)
        except (ValueError, TypeError):
            return False

    def evaluate_rules(self, rules: list[dict], data: dict) -> list[dict]:
        triggered = []
        for rule in rules:
            if not rule.get("enabled", True):
                continue
            all_conditions_met = all(
                self.evaluate_condition(c, data) for c in rule.get("conditions", [])
            )
            if all_conditions_met:
                triggered.append(rule)
        return triggered
