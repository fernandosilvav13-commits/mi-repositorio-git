"""
SectionDetector — uses an LLM to detect document sections and noisy lines.

Uses the LLM provider abstraction (llm_provider) for auto-detected API key
format. The provider can be Gemini, Anthropic, or OpenAI.
"""

import logging
from pathlib import Path

from app.core.config import settings
from app.schemas.preprocessing import DetectionResponse
from app.services.prompt_resolver import PromptResolver
from app.services.llm_provider import get_client, resolve_api_key, ModelClient

logger = logging.getLogger(__name__)

_prompt_resolver = PromptResolver(Path(__file__).resolve().parent.parent.parent / "prompts")
_client: ModelClient | None = None

DEFAULT_MODEL = "fast"
DEFAULT_PROMPT_VERSION = "^v1.0.0"


def _get_client() -> ModelClient:
    global _client
    if _client is None:
        api_key = resolve_api_key(settings)
        _client = get_client(api_key)
    return _client


class SectionDetector:
    """Detects document sections and noisy lines via batched Gemini call.

    Uses the google-genai SDK's structured output mode with a Pydantic
    response_schema to guarantee valid DetectionResponse output from the LLM.
    """

    def detect(
        self,
        text: str,
        prompt_version: str = DEFAULT_PROMPT_VERSION,
    ) -> DetectionResponse:
        """Run batched section + noise detection on document text.

        Makes a single Gemini API call that identifies both section boundaries
        and noisy lines simultaneously (D-05 batched detection). Uses
        structured output via response_schema to guarantee valid JSON.

        Args:
            text: Raw document text (before normalization).
            prompt_version: Semver expression for the section-detection prompt.

        Returns:
            DetectionResponse with sections, noisy_lines, can_identify.

        Raises:
            RuntimeError: If the LLM call fails or returns invalid data.
        """
        # Handle empty text edge case — skip API call (T-10-10 mitigation)
        if text is None or not text.strip():
            logger.debug("Empty/whitespace-only text — returning can_identify=False")
            return DetectionResponse(
                sections={},
                noisy_lines=[],
                can_identify=False,
            )

        # Resolve and render prompt template via PromptResolver
        resolved = _prompt_resolver.get("section-detection", prompt_version)
        if resolved is None:
            logger.warning("No matching section-detection prompt for %s — using inline fallback", prompt_version)
            rendered = f"Analyze the following document and identify its sections and noisy lines:\n\n{text}"
        else:
            rendered = _prompt_resolver.render(resolved, document_text=text)

        # Call LLM with structured output schema
        client = _get_client()
        schema_dict = DetectionResponse.model_json_schema()
        response_text = client.generate(
            contents=rendered,
            schema=schema_dict,
            model=DEFAULT_MODEL,
            config={"temperature": 0.1},
        )

        result = DetectionResponse.model_validate_json(response_text)

        logger.info(
            "Detected %d sections, %d noisy lines, can_identify=%s",
            len(result.sections),
            len(result.noisy_lines),
            result.can_identify,
        )

        return result
