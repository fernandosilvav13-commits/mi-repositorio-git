import json
import re
import random
from app.core.config import settings
from app.utils.logger import setup_logger
from app.services.llm_provider import get_client, resolve_api_key, ModelClient

logger = setup_logger("llm_service")

client: ModelClient | None = None


def _get_client() -> ModelClient:
    global client
    if client is None:
        api_key = resolve_api_key(settings)
        client = get_client(api_key)
    return client


EXTRACTION_PROMPT = """Extrae datos del texto según el esquema JSON.
Responde SOLO con el JSON. Si falta algo, usa "NO ENCONTRADO".
No inventes datos. Respeta nombres de claves."""


def _repair_json(raw: str) -> str:
    raw = raw.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    raw = re.sub(r",\s*([}\]])", r"\1", raw)
    raw = re.sub(r"(?<=[{,:\[ ])'|'(?=[,:}\] \n])", '"', raw)
    return raw

async def extract_fields(text: str, schema: dict, model: str | None = None,
                         fallback_schema: dict | None = None,
                         fallback_model: str | None = None,
                         prompt_override: str | None = None) -> dict:
    llm_client = _get_client()
    model_name = model or settings.llm_model_extract
    retry_model = fallback_model or settings.llm_model_retry
    base_prompt = prompt_override or EXTRACTION_PROMPT

    for phase, current_schema, current_model, max_attempts in [
        ("primary", schema, model_name, settings.llm_retry_count),
        ("fallback", fallback_schema, retry_model, 2),
    ]:
        if current_schema is None:
            continue
        for attempt in range(max_attempts):
            try:
                estimated = len(text) // 4 + len(json.dumps(current_schema)) // 4
                llm_client.track_tpm(estimated)
                prompt = f"{base_prompt}\nSchema: {json.dumps(current_schema)}\nText: {text}"
                raw = llm_client.generate(
                    contents=prompt,
                    schema=current_schema,
                    model=current_model,
                    config={"temperature": 0.1},
                )
                raw = _repair_json(raw)
                result = json.loads(raw)
                return result
            except (json.JSONDecodeError, Exception) as e:
                if attempt < max_attempts - 1:
                    wait = (2 ** attempt) * 2 + random.uniform(0, 1)
                    logger.warning(
                        "LLM %s attempt %d/%d failed: %s. Retrying in %.1fs",
                        phase, attempt + 1, max_attempts, e, wait,
                    )
                    import asyncio
                    await asyncio.sleep(wait)
                else:
                    logger.warning(
                        "LLM %s exhausted after %d attempts: %s",
                        phase, max_attempts, e,
                    )
    logger.error("LLM extraction failed completely with all schemas")
    return {}


async def is_document_legible(text: str) -> bool:
    if not text or len(text.strip()) < 10:
        return False
    llm_client = _get_client()
    prompt = f"El siguiente texto fue extraído de un documento. Responde SOLO 'SI' si el texto tiene contenido legible y coherente, o 'NO' si es basura, ilegible o está vacío.\n\n---\n{text[:1000]}"
    response = llm_client.generate(
        contents=prompt,
        model=settings.llm_model_extract,
        config={"temperature": 0.0},
    )
    return response.upper().startswith("SI")
