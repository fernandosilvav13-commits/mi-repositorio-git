"""
SectionDetector — uses Gemini API to detect document sections and noisy lines.

Orchestrates the batched LLM call for section detection and noise identification
using the google-genai SDK with structured Pydantic output.
"""

import logging
from pathlib import Path

from google import genai
from google.genai import types

from app.schemas.preprocessing import DetectionResponse
from app.services.prompt_resolver import PromptResolver

logger = logging.getLogger(__name__)

# Module-level singleton (matching existing PromptResolver pattern)
# Points to backend/prompts/ by going up from services/ → app/ → backend/ → prompts/
_prompt_resolver = PromptResolver(Path(__file__).resolve().parent.parent.parent / "prompts")
_client: genai.Client | None = None  # Lazy-initialized — uses GEMINI_API_KEY or GOOGLE_API_KEY env var

DEFAULT_MODEL = "gemini-2.5-flash-lite"
DEFAULT_PROMPT_VERSION = "^v1.0.0"


def _get_client() -> genai.Client:
    """Get or create the lazy-initialized genai.Client.

    The client validates the API key at construction time, so we defer
    creation until the first detect() call. This allows the module to be
    imported and tested without an API key being present.

    Returns:
        genai.Client instance configured from environment variables.
    """
    global _client
    if _client is None:
        _client = genai.Client()  # Reads GEMINI_API_KEY or GOOGLE_API_KEY from env
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
        rendered = _prompt_resolver.render(resolved, {"document_text": text})

        # Call Gemini with structured output schema
        client = _get_client()
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=rendered,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DetectionResponse,
                temperature=0.1,
            ),
        )

        result: DetectionResponse = response.parsed

        if result is None:
            raise RuntimeError(
                "Gemini API returned None for section-detection call. "
                f"Response text: {response.text}"
            )

        logger.info(
            "Detected %d sections, %d noisy lines, can_identify=%s",
            len(result.sections),
            len(result.noisy_lines),
            result.can_identify,
        )

        return result
