import json
import re
import asyncio
import random
import time
from google import genai
from app.core.config import settings
from app.utils.logger import setup_logger

logger = setup_logger("llm_service")

client: genai.Client | None = None

# TPM tracking
_tpm_lock = asyncio.Lock()
_tpm_tokens: list[tuple[float, int]] = []
TPM_WINDOW = 60
TPM_LIMIT = 600_000


def _get_client() -> genai.Client:
    global client
    if client is None:
        client = genai.Client(api_key=settings.google_api_key)
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


async def _track_tpm(estimated_tokens: int):
    async with _tpm_lock:
        now = time.time()
        _tpm_tokens[:] = [(t, c) for t, c in _tpm_tokens if now - t < TPM_WINDOW]
        window_tokens = sum(c for _, c in _tpm_tokens)
        if window_tokens + estimated_tokens > TPM_LIMIT:
            sleep_time = TPM_WINDOW - (now - _tpm_tokens[0][0]) if _tpm_tokens else 1
            logger.warning("TPM limit approaching (%d/%d), sleeping %.1fs",
                           window_tokens, TPM_LIMIT, sleep_time)
            await asyncio.sleep(min(sleep_time, 5))
        _tpm_tokens.append((time.time(), estimated_tokens))


async def extract_fields(text: str, schema: dict, model: str | None = None,
                         fallback_schema: dict | None = None,
                         fallback_model: str | None = None,
                         prompt_override: str | None = None) -> dict:
    llm_client = _get_client()
    model_name = model or settings.gemini_model_extract
    retry_model = fallback_model or settings.gemini_model_retry
    base_prompt = prompt_override or EXTRACTION_PROMPT

    for phase, current_schema, current_model, max_attempts in [
        ("primary", schema, model_name, settings.llm_retry_count),
        ("fallback", fallback_schema, retry_model, 2),
    ]:
        if current_schema is None:
            continue
        for attempt in range(max_attempts):
            try:
                await _track_tpm(len(text) // 4 + len(json.dumps(current_schema)) // 4)
                prompt = f"{base_prompt}\nSchema: {json.dumps(current_schema)}\nText: {text}"
                response = llm_client.models.generate_content(
                    model=current_model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "temperature": 0.1,
                    },
                )
                raw = response.text.strip()
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
    response = llm_client.models.generate_content(
        model=settings.gemini_model_extract,
        contents=prompt,
        config={"temperature": 0.0},
    )
    return response.text.strip().upper().startswith("SI")
