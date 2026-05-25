import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.rules.base_rule import BaseRule

logger = logging.getLogger(__name__)


class RuleRegistry:
    def __init__(self):
        self._rules: dict[str, "BaseRule"] = {}

    def register(self, rule: "BaseRule") -> None:
        self._rules[rule.name] = rule
        logger.info("Rule registered: %s (field=%s, enabled=%s)", rule.name, rule.field, rule.enabled)

    def get_all(self) -> list["BaseRule"]:
        return list(self._rules.values())

    def get_by_field(self, field: str) -> list["BaseRule"]:
        return [r for r in self._rules.values() if r.field == field]

    def get_enabled(self) -> list["BaseRule"]:
        return [r for r in self._rules.values() if r.enabled]

    def get_ready_for_activation(self) -> list["BaseRule"]:
        return [r for r in self._rules.values() if r.ready_for_activation]

    def enable(self, name: str) -> bool:
        if name in self._rules:
            self._rules[name].enable()
            return True
        return False

    def disable(self, name: str) -> bool:
        if name in self._rules:
            self._rules[name].disable()
            return True
        return False

    def get(self, name: str) -> "BaseRule | None":
        return self._rules.get(name)


rule_registry = RuleRegistry()
