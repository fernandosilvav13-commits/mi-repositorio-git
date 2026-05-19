import pytest
import yaml
from pydantic import ValidationError
from app.schemas.prompt import PromptVersion


class TestPromptVersion:
    def test_prompt_version_valid(self):
        p = PromptVersion(
            type="cv-extraction",
            version="1.0.0",
            description="test",
            author="dev",
            system_prompt="Extract data according to schema.",
            schema={"fields": ["name"]},
            model_params={"model": "gemini", "temperature": 0.1, "tags": ["cv"]},
            tags=["cv"],
        )
        assert p.type == "cv-extraction"
        assert p.version == "1.0.0"
        assert p.tag_name == "prompt/cv-extraction/v1.0.0"

    def test_prompt_version_invalid_version(self):
        for bad in ["v1.0.0", "1.0", "1", "1.0.0.0"]:
            with pytest.raises(ValueError, match="version must be strict semver"):
                PromptVersion(
                    type="cv-extraction",
                    version=bad,
                    description="test",
                    author="dev",
                    system_prompt="test",
                    schema={"fields": ["name"]},
                    model_params={"model": "gemini", "temperature": 0.1, "tags": ["cv"]},
                    tags=["cv"],
                )

    def test_prompt_version_empty_system_prompt(self):
        with pytest.raises(ValueError, match="system_prompt must be non-empty"):
            PromptVersion(
                type="cv-extraction",
                version="1.0.0",
                description="test",
                author="dev",
                system_prompt="",
                schema={"fields": ["name"]},
                model_params={"model": "gemini", "temperature": 0.1, "tags": ["cv"]},
                tags=["cv"],
            )

    def test_prompt_version_empty_schema(self):
        with pytest.raises(ValueError, match="schema must be a non-empty dict"):
            PromptVersion(
                type="cv-extraction",
                version="1.0.0",
                description="test",
                author="dev",
                system_prompt="test",
                schema={},
                model_params={"model": "gemini", "temperature": 0.1, "tags": ["cv"]},
                tags=["cv"],
            )

    def test_yaml_load_and_parse(self, tmp_path):
        yaml_content = """
type: cv-extraction
version: 1.0.0
description: Test prompt
author: tester
system_prompt: Extract data.
schema:
  name: ""
  age: ""
model_params:
  model: gemini-test
  temperature: 0.0
tags:
  - test
"""
        f = tmp_path / "test.yaml"
        f.write_text(yaml_content)
        data = yaml.safe_load(f.read_text())
        p = PromptVersion(**data)
        assert p.type == "cv-extraction"
        assert p.version == "1.0.0"
        assert p.tag_name == "prompt/cv-extraction/v1.0.0"

    def test_yaml_missing_required_field(self, tmp_path):
        yaml_content = """
type: cv-extraction
version: 1.0.0
description: Missing system_prompt
author: tester
schema:
  name: ""
model_params:
  model: gemini
  temperature: 0.0
tags:
  - test
"""
        f = tmp_path / "missing.yaml"
        f.write_text(yaml_content)
        data = yaml.safe_load(f.read_text())
        with pytest.raises((ValueError, ValidationError)):
            PromptVersion(**data)

    def test_yaml_invalid_schema_type(self, tmp_path):
        yaml_content = """
type: cv-extraction
version: 1.0.0
description: Invalid schema
author: tester
system_prompt: Extract.
schema: "not a dict"
model_params:
  model: gemini
  temperature: 0.0
tags:
  - test
"""
        f = tmp_path / "bad_schema.yaml"
        f.write_text(yaml_content)
        data = yaml.safe_load(f.read_text())
        with pytest.raises((ValueError, ValidationError)):
            PromptVersion(**data)
