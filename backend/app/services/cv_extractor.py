import json
import asyncio
from app.core.config import settings
from app.services.llm_service import extract_fields
from app.services.preprocessor import preprocess_cv_text
from app.services.cache_service import cache_service

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "NOMBRES": {"type": "string"},
        "APELLIDOS": {"type": "string"},
        "RUT": {"type": "string"},
        "GENERO": {"type": "string"},
        "TELEFONO_FIJO": {"type": ["string", "null"]},
        "TELEFONO_CELULAR": {"type": ["string", "null"]},
        "NACIONALIDAD": {"type": "string"},
        "TITULO_PROFESIONAL": {"type": "string"},
        "TITULO_ACADEMICO_1": {"type": ["string", "null"]},
        "TITULO_ACADEMICO_2": {"type": ["string", "null"]},
        "experiencia_laboral": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "establecimiento": {"type": "string"},
                    "duracion": {"type": "string"},
                    "incluye_actualidad": {"type": "boolean"},
                },
            },
        },
    },
}

_extraction_semaphore = asyncio.Semaphore(5)


def _build_dynamic_schema(template_columns: list[dict]) -> dict:
    properties = {}
    for col in template_columns:
        name = col.get("name", "campo")
        col_type = col.get("type", "string")

        if name.lower() == "experiencia_laboral" or col_type.lower() == "array":
            properties[name] = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "establecimiento": {"type": "string"},
                        "duracion": {"type": "string"},
                        "incluye_actualidad": {"type": "boolean"},
                    }
                }
            }
        else:
            properties[name] = {"type": "string"}

    return {
        "type": "object",
        "properties": properties
    }


async def extract_cv_data(raw_text: str, is_retry: bool = False, schema: dict | None = None) -> dict | None:
    processed = preprocess_cv_text(raw_text)

    active_schema = schema or EXTRACTION_SCHEMA
    model = settings.gemini_model_retry if is_retry else settings.gemini_model_extract

    cached_result = cache_service.get(processed, active_schema, model)
    if cached_result:
        return cached_result

    async with _extraction_semaphore:
        result = await extract_fields(
            text=processed,
            schema=active_schema,
            model=model,
            fallback_schema=EXTRACTION_SCHEMA if schema else None,
            fallback_model=settings.gemini_model_retry,
        )

        if result:
            cache_service.set(processed, active_schema, model, result)
        return result or None
