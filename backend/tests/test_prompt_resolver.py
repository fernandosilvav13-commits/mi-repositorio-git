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


from app.services.prompt_resolver import PromptResolver, _match_version, EXTRACTION_PROMPT_FALLBACK, EXTRACTION_SCHEMA_FALLBACK


class TestPromptResolver:
    def _make_yaml(self, path, type="cv-extraction", version="1.0.0", system_prompt="Extract data.", schema=None, **kw):
        data = {
            "type": type, "version": version, "description": "test", "author": "tester",
            "system_prompt": system_prompt,
            "schema": schema or {"name": ""},
            "model_params": {"model": "gemini", "temperature": 0.1},
            "tags": ["test"],
            **kw,
        }
        path.write_text(yaml.dump(data))

    def test_resolver_scan_and_get_exact(self, tmp_path):
        v1 = tmp_path / "cv-extraction" / "v1.0.0.yaml"
        v2 = tmp_path / "cv-extraction" / "v2.0.0.yaml"
        v1.parent.mkdir(parents=True)
        self._make_yaml(v1, version="1.0.0")
        self._make_yaml(v2, version="2.0.0")
        r = PromptResolver(str(tmp_path))
        pv = r.get("cv-extraction", "1.0.0")
        assert pv is not None
        assert pv.version == "1.0.0"

    def test_resolver_caret_match(self, tmp_path):
        d = tmp_path / "cv-extraction"
        d.mkdir(parents=True)
        self._make_yaml(d / "v1.0.0.yaml", version="1.0.0")
        self._make_yaml(d / "v1.5.0.yaml", version="1.5.0")
        self._make_yaml(d / "v2.0.0.yaml", version="2.0.0")
        r = PromptResolver(str(tmp_path))
        pv = r.get("cv-extraction", "^1.0.0")
        assert pv is not None
        assert pv.version == "1.5.0"

    def test_resolver_tilde_match(self, tmp_path):
        d = tmp_path / "cv-extraction"
        d.mkdir(parents=True)
        self._make_yaml(d / "v1.0.0.yaml", version="1.0.0")
        self._make_yaml(d / "v1.1.0.yaml", version="1.1.0")
        self._make_yaml(d / "v1.2.0.yaml", version="1.2.0")
        r = PromptResolver(str(tmp_path))
        pv = r.get("cv-extraction", "~1.0.0")
        assert pv is not None
        assert pv.version == "1.0.0"

    def test_resolver_gte_match(self, tmp_path):
        d = tmp_path / "cv-extraction"
        d.mkdir(parents=True)
        self._make_yaml(d / "v1.0.0.yaml", version="1.0.0")
        self._make_yaml(d / "v2.0.0.yaml", version="2.0.0")
        self._make_yaml(d / "v3.0.0.yaml", version="3.0.0")
        r = PromptResolver(str(tmp_path))
        pv = r.get("cv-extraction", ">=2.0.0")
        assert pv is not None
        assert pv.version == "3.0.0"

    def test_resolver_no_match_returns_none(self, tmp_path):
        d = tmp_path / "cv-extraction"
        d.mkdir(parents=True)
        self._make_yaml(d / "v1.0.0.yaml", version="1.0.0")
        r = PromptResolver(str(tmp_path))
        pv = r.get("cv-extraction", "2.0.0")
        assert pv is None

    def test_resolver_fallback_on_empty(self, tmp_path):
        r = PromptResolver(str(tmp_path))
        pv = r.get("cv-extraction", "1.0.0")
        assert pv is None

    def test_resolver_render_jinja(self, tmp_path):
        d = tmp_path / "cv-extraction"
        d.mkdir(parents=True)
        self._make_yaml(d / "v1.0.0.yaml", version="1.0.0", system_prompt="Hello {{ name }}")
        r = PromptResolver(str(tmp_path))
        pv = r.get("cv-extraction", "1.0.0")
        assert pv is not None
        result = r.render(pv, name="World")
        assert result == "Hello World"

    def test_resolver_render_with_schema(self, tmp_path):
        d = tmp_path / "cv-extraction"
        d.mkdir(parents=True)
        self._make_yaml(d / "v1.0.0.yaml", version="1.0.0",
                        system_prompt="Schema: {{ schema | tojson }}",
                        schema={"key": "val"})
        r = PromptResolver(str(tmp_path))
        pv = r.get("cv-extraction", "1.0.0")
        assert pv is not None
        result = r.render(pv)
        assert '"key"' in result
        assert '"val"' in result

    def test_resolver_invalid_yaml_on_init(self, tmp_path):
        d = tmp_path / "cv-extraction"
        d.mkdir(parents=True)
        bad = d / "bad.yaml"
        bad.write_text("not: valid: yaml: [content")
        with pytest.raises((ValueError, Exception)):
            PromptResolver(str(tmp_path))

    def test_resolver_missing_field_yaml(self, tmp_path):
        d = tmp_path / "cv-extraction"
        d.mkdir(parents=True)
        bad = d / "missing.yaml"
        bad.write_text("""
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
""")
        with pytest.raises((ValueError, Exception)):
            PromptResolver(str(tmp_path))

    def test_match_version_edge_cases(self):
        from semver import Version
        assert _match_version("^0.1.0", Version.parse("0.1.5"))
        assert not _match_version("^0.1.0", Version.parse("0.2.0"))
        assert _match_version("1.0.0", Version.parse("1.0.0"))
        assert not _match_version("1.0.0", Version.parse("1.0.1"))
        assert _match_version(">=1.0.0", Version.parse("5.0.0"))
