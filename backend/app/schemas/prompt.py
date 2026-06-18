from pydantic import BaseModel, model_validator
from typing import Any
import re


SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
TYPE_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class PromptVersion(BaseModel):
    type: str
    version: str
    description: str
    author: str
    system_prompt: str
    prompt_schema: dict[str, Any]
    model_params: dict[str, Any]
    tags: list[str]

    @property
    def tag_name(self) -> str:
        return f"prompt/{self.type}/v{self.version}"

    @model_validator(mode="after")
    def _validate_fields(self):
        if not SEMVER_PATTERN.match(self.version):
            raise ValueError(f"version must be strict semver (e.g. '1.0.0'), got '{self.version}'")
        if not TYPE_PATTERN.match(self.type):
            raise ValueError(f"type must match pattern '^[a-z0-9]+(-[a-z0-9]+)*$', got '{self.type}'")
        if not isinstance(self.prompt_schema, dict) or len(self.prompt_schema) == 0:
            raise ValueError("prompt_schema must be a non-empty dict")
        if not self.system_prompt or not self.system_prompt.strip():
            raise ValueError("system_prompt must be non-empty")
        return self
