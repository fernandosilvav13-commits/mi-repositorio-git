import pytest
from app.services.rules.base_rule import BaseRule
from app.services.rules.registry import RuleRegistry, rule_registry
from app.services.rules.evaluator import evaluate_rules


class DummyRule(BaseRule):
    name = "dummy"
    description = "Dummy rule for testing"
    field = "DUMMY_FIELD"

    def evaluate(self, text: str, current_data: dict) -> str | None:
        if "dummy" in text.lower():
            return "dummy_value"
        return None


class TestBaseRule:
    def test_shadow_evaluate_increments_total(self):
        rule = DummyRule()
        assert rule._total == 0
        rule.shadow_evaluate("dummy text", {})
        assert rule._total == 1

    def test_shadow_evaluate_no_match(self):
        rule = DummyRule()
        result = rule.shadow_evaluate("other text", {})
        assert result is None
        assert rule._total == 1

    def test_precision_calculation(self):
        rule = DummyRule()
        for _ in range(4):
            rule.shadow_evaluate("dummy text", {})
            rule.record_hit()
        assert rule.precision == 1.0

    def test_not_ready_for_activation_below_threshold(self):
        rule = DummyRule()
        rule.shadow_evaluate("dummy text", {})
        assert rule.ready_for_activation is False

    def test_enabled_property(self):
        rule = DummyRule()
        assert rule.enabled is False
        rule.enable()
        assert rule.enabled is True
        rule.disable()
        assert rule.enabled is False


class TestRuleRegistry:
    def setup_method(self):
        self.registry = RuleRegistry()

    def test_register_and_get(self):
        rule = DummyRule()
        self.registry.register(rule)
        assert self.registry.get("dummy") is rule

    def test_get_all(self):
        rule = DummyRule()
        self.registry.register(rule)
        rules = self.registry.get_all()
        assert len(rules) == 1

    def test_get_by_field(self):
        rule = DummyRule()
        self.registry.register(rule)
        rules = self.registry.get_by_field("DUMMY_FIELD")
        assert len(rules) == 1

    def test_get_enabled(self):
        rule = DummyRule(enabled=True)
        self.registry.register(rule)
        enabled = self.registry.get_enabled()
        assert len(enabled) == 1

    def test_enable_and_disable(self):
        rule = DummyRule()
        self.registry.register(rule)
        assert self.registry.enable("dummy") is True
        assert rule.enabled is True
        assert self.registry.disable("dummy") is True
        assert rule.enabled is False

    def test_enable_nonexistent(self):
        assert self.registry.enable("nonexistent") is False


class TestEvaluateRules:
    def test_evaluate_enabled_rule(self):
        from app.services.rules.registry import rule_registry as main_registry
        rule = DummyRule(enabled=True)
        main_registry.register(rule)
        try:
            updates = evaluate_rules("dummy text", {})
            assert "DUMMY_FIELD" in updates
            assert updates["DUMMY_FIELD"] == "dummy_value"
        finally:
            pass

    def test_evaluate_disabled_rule(self):
        from app.services.rules.registry import rule_registry as main_registry
        rule = DummyRule(enabled=False)
        main_registry.register(rule)
        try:
            updates = evaluate_rules("dummy text", {})
            assert "DUMMY_FIELD" not in updates
        finally:
            pass
