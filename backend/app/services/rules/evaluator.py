import logging
from app.services.rules.registry import rule_registry

logger = logging.getLogger(__name__)


def evaluate_rules(text: str, current_data: dict) -> dict:
    updates = {}
    for rule in rule_registry.get_all():
        try:
            result = rule.shadow_evaluate(text, current_data)
            if result is not None:
                if rule.enabled:
                    updates[rule.field] = result
                    rule.record_hit()
                    logger.info("Rule %s applied: %s = %s", rule.name, rule.field, result)
                else:
                    logger.info(
                        "Rule %s (shadow): would set %s = %s (precision=%.2f, total=%d)",
                        rule.name, rule.field, result, rule.precision, rule._total,
                    )
            else:
                logger.debug("Rule %s: no match", rule.name)
        except Exception as e:
            logger.warning("Rule %s failed: %s", rule.name, e)
    return updates
