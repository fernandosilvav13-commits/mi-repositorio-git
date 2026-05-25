import sys
sys.path.insert(0, ".")
from app.services.rules.registry import rule_registry
rules = rule_registry.get_all()
print(f"Rules registered: {len(rules)}")
for r in rules:
    print(f"  - {r.name} -> {r.field}")
