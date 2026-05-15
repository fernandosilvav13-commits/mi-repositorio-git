from pydantic import BaseModel
from typing import Optional, Any


class RuleCondition(BaseModel):
    field: str
    operator: str
    value: Any


class RuleAction(BaseModel):
    type: str
    params: dict


class RuleCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    conditions: list[RuleCondition]
    action: RuleAction
    enabled: bool = True


class RuleResponse(BaseModel):
    id: str
    name: str
    description: str
    conditions: list[RuleCondition]
    action: RuleAction
    enabled: bool
