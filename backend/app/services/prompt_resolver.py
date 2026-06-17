import glob
import os
import subprocess
from pathlib import Path
from typing import Optional

import yaml
from jinja2 import Environment, BaseLoader
from semver import Version

from app.schemas.prompt import PromptVersion
from app.utils.logger import setup_logger

logger = setup_logger("prompt_resolver")

EXTRACTION_PROMPT_FALLBACK = """Extrae datos del texto según el esquema JSON.
Responde SOLO con el JSON. Si falta algo, usa "NO ENCONTRADO".
No inventes datos. Respeta nombres de claves."""

EXTRACTION_SCHEMA_FALLBACK = {
    "nombres": "", "apellidos": "", "rut": "", "telefono": "",
    "email": "", "direccion": "", "fecha_nacimiento": "", "nacionalidad": "",
    "estado_civil": "", "profesion": "", "resumen_profesional": "",
    "educacion": [], "experiencia_laboral": [], "idiomas": [], "habilidades": [],
}


def _match_version(version_expr: str, candidate: Version) -> bool:
    expr = version_expr.strip()
    prefix = ""
    for p in ("^", "~", ">="):
        if expr.startswith(p):
            prefix = p
            expr = expr[len(p):]
            break
    expr = expr.lstrip("v")
    if prefix == "^":
        base = Version.parse(expr)
        if base.major == 0:
            return candidate.major == 0 and candidate.minor == base.minor and candidate.patch >= base.patch
        return candidate.major == base.major and candidate >= base
    elif prefix == "~":
        base = Version.parse(expr)
        return candidate.major == base.major and candidate.minor == base.minor and candidate.patch >= base.patch
    elif prefix == ">=":
        return candidate >= Version.parse(expr)
    else:
        return candidate == Version.parse(expr)


class PromptResolver:
    def __init__(self, prompts_dir: str = "backend/prompts"):
        self.prompts_dir = Path(prompts_dir)
        self._cache: dict[str, PromptVersion] = {}
        self._jinja_env = Environment(loader=BaseLoader(), autoescape=True)
        self._scan_all()

    def _scan_all(self):
        self._cache.clear()
        for yaml_path in glob.glob(str(self.prompts_dir / "*" / "*.yaml"), recursive=False):
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            pv = PromptVersion(**data)
            key = f"{pv.type}@{pv.version}"
            self._cache[key] = pv

    def get(self, doc_type: str, version_expr: str) -> Optional[PromptVersion]:
        candidates = []
        for key, pv in self._cache.items():
            if pv.type == doc_type:
                try:
                    candidate_ver = Version.parse(pv.version)
                    if _match_version(version_expr, candidate_ver):
                        candidates.append((candidate_ver, pv))
                except ValueError:
                    continue

        if not candidates:
            logger.warning("No YAML match for %s@%s — using fallback constants", doc_type, version_expr)
            return None

        candidates.sort(key=lambda x: x[0], reverse=True)
        selected = candidates[0][1]

        logger.info("Resolved prompt: %s@%s -> %s@%s (file: %s)",
                    doc_type, version_expr, selected.type, selected.version, selected.tag_name)
        return selected

    def render(self, pv: PromptVersion, document_text: str = "", **extra_context) -> str:
        context = {
            "document_text": document_text,
            "schema": pv.schema,
            **extra_context,
        }
        template = self._jinja_env.from_string(pv.system_prompt)
        return template.render(**context)

    @staticmethod
    def create_prompt_tag(doc_type: str, version: str, message: str = "") -> str:
        tag_name = f"prompt/{doc_type}/v{version}"
        msg = message or f"Prompt {doc_type} version {version}"
        subprocess.run(["git", "tag", "-a", tag_name, "-m", msg], check=True)
        logger.info("Created git tag: %s", tag_name)
        return tag_name

    @staticmethod
    def list_prompt_tags(doc_type: str = "") -> list[str]:
        pattern = f"prompt/{doc_type}/*" if doc_type else "prompt/*"
        result = subprocess.run(
            ["git", "tag", "-l", pattern],
            capture_output=True, text=True, check=True
        )
        return [t.strip() for t in result.stdout.splitlines() if t.strip()]

    @staticmethod
    def create_prompt_version_tag(pv: PromptVersion) -> str:
        return PromptResolver.create_prompt_tag(
            pv.type, pv.version,
            message=f"Prompt {pv.type} version {pv.version}"
        )

    def build_fallback_prompt(self, schema: Optional[dict] = None) -> dict:
        return {
            "system_prompt": EXTRACTION_PROMPT_FALLBACK,
            "schema": schema or EXTRACTION_SCHEMA_FALLBACK,
            "model_params": {"model": "gemini-2.5-flash-lite", "temperature": 0.1},
            "version": "0.0.0-fallback",
            "tag_name": "prompt/fallback/v0.0.0",
        }
