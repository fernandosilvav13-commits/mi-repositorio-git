import json
from google import genai
from app.core.config import settings


client: genai.Client | None = None


def _get_client() -> genai.Client:
    global client
    if client is None:
        client = genai.Client(api_key=settings.google_api_key)
    return client


EXTRACTION_PROMPT = """Extrae datos del texto según el esquema JSON.
Responde SOLO con el JSON. Si falta algo, usa "NO ENCONTRADO".
No inventes datos. Respeta nombres de claves."""


async def extract_fields(text: str, schema: dict, model: str | None = None) -> dict:
    llm_client = _get_client()
    model_name = model or settings.gemini_model_extract
    prompt = f"{EXTRACTION_PROMPT}\nSchema: {json.dumps(schema)}\nText: {text}"
    response = llm_client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "temperature": 0.1,
        },
    )
    raw = response.text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)


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
