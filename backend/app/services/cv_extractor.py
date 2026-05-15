import json
import re
import asyncio
import random
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

# Global semaphore to prevent TPM/RPM spikes
_extraction_semaphore = asyncio.Semaphore(5)

def _build_dynamic_schema(template_columns: list[dict]) -> dict:
    """Convierte la lista de columnas de la plantilla en un esquema JSON para el LLM."""
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
            properties[name] = {"type": "string"} # Default to string for simplicity
    
    return {
        "type": "object",
        "properties": properties
    }

async def extract_cv_data(raw_text: str, is_retry: bool = False, schema: dict | None = None) -> dict | None:
    processed = preprocess_cv_text(raw_text)
    
    # Si no se pasa esquema, usamos uno por defecto (legacy/fallback)
    active_schema = schema or EXTRACTION_SCHEMA
    
    # Seleccionamos el modelo basado en si es un reintento
    model = settings.gemini_model_retry if is_retry else settings.gemini_model_extract
    
    # 1. Check Cache
    cached_result = cache_service.get(processed, active_schema, model)
    if cached_result:
        return cached_result

    # 2. Extract with LLM (with exponential backoff)
    async with _extraction_semaphore:
        for attempt in range(3):
            try:
                result = await extract_fields(processed, active_schema, model=model)
                
                # 3. Save to cache if successful
                if result:
                    cache_service.set(processed, active_schema, model, result)
                return result
            except Exception as e:
                if attempt < 2:
                    # Exponential backoff: 2^attempt * 2 + jitter
                    wait_time = (2 ** attempt) * 2 + random.uniform(0, 1)
                    await asyncio.sleep(wait_time)
                else:
                    print(f"Extraction failed after 3 attempts: {e}")
    return None
