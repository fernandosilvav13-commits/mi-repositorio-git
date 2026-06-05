"""
PreprocessingPipeline — multi-stage structural cleanup orchestrator.

Chains SectionDetector → NoiseFilter → LayoutNormalizer in sequence per D-10.
Provides a single process(text) entry point that returns PreprocessingResult.
Handles error recovery per stage and adjusts section boundaries after noise
removal to prevent marker misalignment (Pitfall 2 mitigation).

NOTE: The legacy preprocess_cv_text() function and helpers are preserved in
this module for backward compatibility (imported by cv_extractor.py).
"""

import logging
import re

from app.schemas.preprocessing import PreprocessingResult, DetectionResponse, SectionBoundary
from app.services.section_detector import SectionDetector
from app.services.noise_filter import NoiseFilter
from app.services.layout_normalizer import LayoutNormalizer

logger = logging.getLogger(__name__)

# =============================================================================
# Legacy preprocess_cv_text — preserved for backward compatibility
# =============================================================================

SECTIONS = {
    "nombres": r"(?:nombres|nombre|apellidos|apellido|datos personales)[:\s]*([A-Za-záéíóúñÁÉÍÓÚÑ\s]+)",
    "rut": r"(?:rut|run|cedula|cédula)[:\s]*([0-9.]+-[0-9kK])",
    "telefono": r"(?:tel[ée]fono|celular|movil|móvil|contacto)[:\s]*([+\d\s\-()]{7,20})",
    "correo": r"(?:correo|email|e-mail)[:\s]*([\w.+-]+@[\w-]+\.[\w.]+)",
    "nacionalidad": r"(?:nacionalidad)[:\s]*([A-Za-záéíóúñÁÉÍÓÚÑ\s]+)",
    "titulos": r"(?:titulo|título|títulos|títulos|grado|profesión|profesion)[:\s]*(.+?)(?=\n\s*\n|\Z)",
    "experiencia": r"(?:experiencia|experiencia laboral|antecedentes)[:\s]*(.+?)(?=\n\s*\n\s*(?:formacion|formación|educación|educacion|estudios| capacitación|certificaciones|idiomas|\Z))",
}

# Redundant phrases to remove to save tokens
REDUNDANT_PHRASES = [
    r"curriculum vitae", r"currículum vitae", r"hoja de vida",
    r"resumen profesional", r"perfil profesional",
    r"referencias laborales disponibles a solicitud",
    r"disponibilidad inmediata",
]


def clean_text(text: str) -> str:
    """Basic cleaning to remove double spaces and redundant phrases."""
    for phrase in REDUNDANT_PHRASES:
        text = re.sub(phrase, "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_sections(text: str) -> dict[str, str]:
    result = {}
    for key, pattern in SECTIONS.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            value = match.group(1).strip()
            value = re.sub(r"\s+", " ", value)
            if len(value) > 5:
                result[key] = value[:1500]
    return result


def compress_experience(text: str, max_lines: int = 20) -> str:
    lines = text.split("\n")
    kept = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(kw in stripped.lower() for kw in ["experiencia", "establecimiento", "empresa", "cargo", "función", "funcion", "desde", "hasta", "actualidad", "años", "meses"]):
            kept.append(stripped)
        elif re.match(r"^\d{4}", stripped):
            kept.append(stripped)
        elif len(stripped) > 30 and len(kept) < max_lines:
            kept.append(stripped)
        if len(kept) >= max_lines:
            break
    return "\n".join(kept)


def preprocess_cv_text(raw_text: str) -> str:
    # First, do a very basic cleaning
    cleaned_raw = clean_text(raw_text)

    sections = extract_sections(raw_text)
    parts = []
    for section_name in ["nombres", "rut", "telefono", "correo", "nacionalidad", "titulos"]:
        if section_name in sections:
            parts.append(f"#{section_name.upper()}: {sections[section_name]}")

    if "experiencia" in sections:
        exp = compress_experience(sections["experiencia"])
        if exp:
            parts.append(f"#EXP:\n{exp}")

    if not parts:
        return cleaned_raw[:4000]

    final_text = "\n".join(parts)
    return final_text[:6000]


# =============================================================================
# PreprocessingPipeline — Phase 10 orchestrator
# =============================================================================


class PreprocessingPipeline:
    """Multi-stage preprocessing pipeline: SectionDetector → NoiseFilter → LayoutNormalizer per D-10.

    Provides a single entry point for document preprocessing with per-stage
    error recovery. The constructor accepts stage instances, allowing tests
    to inject mocks. Used via the module-level singleton for production.
    """

    def __init__(
        self,
        section_detector: SectionDetector,
        noise_filter: NoiseFilter,
        layout_normalizer: LayoutNormalizer,
    ) -> None:
        """Constructor accepts stage instances for testability (mock injection).

        Args:
            section_detector: Detection stage (LLM call).
            noise_filter: Line removal stage.
            layout_normalizer: Whitespace + markers + bullets stage.
        """
        self._detector = section_detector
        self._filter = noise_filter
        self._normalizer = layout_normalizer

    def process(self, document_text: str | None) -> PreprocessingResult:
        """Run full preprocessing pipeline on a document.

        The pipeline follows this sequence per D-10 architecture:
        1. Empty/None check — return PreprocessingResult with error immediately
        2. Section detection via SectionDetector.detect() — wrapped in try/except
        3. can_identify check (D-03) — return fallback if False or empty sections
        4. Noise removal via NoiseFilter.filter()
        5. Section boundary adjustment (Pitfall 2 mitigation)
        6. Layout normalization via LayoutNormalizer.normalize()
        7. Return PreprocessingResult with was_preprocessed=True

        Args:
            document_text: Raw text from OCR/PDF extraction.

        Returns:
            PreprocessingResult — either preprocessed text with metadata,
            or original text (fallback) with was_preprocessed=False.
        """
        # Step 1 — Empty/None check
        if not document_text or not document_text.strip():
            return PreprocessingResult(
                cleaned_text=document_text or "",
                was_preprocessed=False,
                error="Empty document text",
            )

        # Step 2 — Section detection (wrapped)
        try:
            detection: DetectionResponse = self._detector.detect(document_text)
        except Exception as exc:
            logger.warning("Section detection failed: %s", exc)
            return PreprocessingResult(
                cleaned_text=document_text,
                was_preprocessed=False,
                error=f"Section detection failed: {exc}",
            )

        # Step 3 — D-03 check: skip if LLM cannot identify clear sections
        if not detection.can_identify or not detection.sections:
            logger.info(
                "Skipping preprocessing: can_identify=%s, sections=%d",
                detection.can_identify,
                len(detection.sections),
            )
            return PreprocessingResult(
                cleaned_text=document_text,
                was_preprocessed=False,
            )

        # Step 4 — Noise removal
        cleaned_after_noise = self._filter.filter(
            text=document_text,
            noisy_lines=set(detection.noisy_lines),
        )

        # Step 5 — Section boundary adjustment (Pitfall 2 mitigation)
        adjusted_sections = self._adjust_section_boundaries(
            detection.sections,
            detection.noisy_lines,
        )

        # Step 6 — Layout normalization (with adjusted sections)
        try:
            normalized_text = self._normalizer.normalize(
                text=cleaned_after_noise,
                sections=adjusted_sections,
            )
        except Exception as exc:
            logger.warning("Layout normalization failed: %s", exc)
            return PreprocessingResult(
                cleaned_text=cleaned_after_noise,
                sections_detected=detection.sections,
                noisy_lines_removed=detection.noisy_lines,
                was_preprocessed=False,
                error=f"Layout normalization failed: {exc}",
            )

        # Step 7 — Return success
        return PreprocessingResult(
            cleaned_text=normalized_text,
            sections_detected=detection.sections,
            noisy_lines_removed=detection.noisy_lines,
            was_preprocessed=True,
        )

    def _adjust_section_boundaries(
        self,
        sections: dict[str, SectionBoundary],
        noisy_lines: list[int],
    ) -> dict[str, SectionBoundary]:
        """Adjust section boundaries after noise removal (Pitfall 2 mitigation).

        After NoiseFilter removes lines, the line numbers in the original
        section boundaries are no longer accurate. This method computes new
        boundaries by subtracting the count of noisy lines that appear before
        each section boundary in the original text.

        Args:
            sections: Original section boundaries from DetectionResponse.
            noisy_lines: List of noisy line indices that will be removed.

        Returns:
            Adjusted section boundaries with start_line and end_line
            corrected for the post-noise-removal text.
        """
        sorted_noisy = sorted(noisy_lines)
        adjusted_sections: dict[str, SectionBoundary] = {}

        for section_name, boundary in sections.items():
            # Count noisy lines removed before this section's start
            before_start = sum(1 for nl in sorted_noisy if nl < boundary.start_line)
            # Count noisy lines removed before or at this section's end
            before_end = sum(1 for nl in sorted_noisy if nl <= boundary.end_line)

            new_start = max(0, boundary.start_line - before_start)
            new_end = max(new_start, boundary.end_line - before_end)

            adjusted_sections[section_name] = SectionBoundary(
                start_line=new_start,
                end_line=new_end,
            )

        return adjusted_sections


# Module-level singleton (matching PromptResolver pattern)
_section_detector = SectionDetector()
_noise_filter = NoiseFilter()
_layout_normalizer = LayoutNormalizer()

preprocessing_pipeline = PreprocessingPipeline(
    section_detector=_section_detector,
    noise_filter=_noise_filter,
    layout_normalizer=_layout_normalizer,
)
