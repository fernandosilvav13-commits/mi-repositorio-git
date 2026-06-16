from app.services.preprocessor import preprocessing_pipeline
from app.services.classifier import doc_classifier
from pathlib import Path
from app.services.prompt_resolver import PromptResolver
from app.services.llm_service import extract_fields
from app.services.cv_extractor import EXTRACTION_SCHEMA
from app.utils.logger import setup_logger

logger = setup_logger("extraction_pipeline")

prompt_resolver = PromptResolver(Path(__file__).resolve().parent.parent.parent / "prompts")


class ExtractionPipeline:
    async def process(self, raw_text: str) -> dict:
        if not raw_text or not raw_text.strip():
            return {"classification_warning": True, "category": "non-cv", "extraction": None}

        preprocessed = preprocessing_pipeline.process(raw_text)
        if not preprocessed.cleaned_text:
            return {"classification_warning": True, "category": "non-cv", "extraction": None}

        classification = doc_classifier.classify(preprocessed.cleaned_text)
        logger.info("Classification: %s (%.4f)", classification.category, classification.confidence)

        if classification.category != "cv":
            return {
                "classification_warning": True,
                "category": classification.category,
                "confidence": classification.confidence,
                "extraction": None,
            }

        prompt_version = prompt_resolver.get("cv-extraction", "^v1.0.0")
        prompt_text = None
        prompt_tag = None
        if prompt_version:
            prompt_text = prompt_resolver.render(
                prompt_version,
                document_text=preprocessed.cleaned_text,
            )
            prompt_tag = prompt_version.tag_name
            logger.info("Resolved prompt: %s", prompt_tag)
        else:
            logger.warning("No cv-extraction prompt found, using default prompt")

        extraction = await extract_fields(
            text=preprocessed.cleaned_text,
            schema=EXTRACTION_SCHEMA,
            prompt_override=prompt_text,
        )

        return {
            "classification_warning": False,
            "category": classification.category,
            "confidence": classification.confidence,
            "prompt_version": prompt_tag,
            "extraction": extraction,
        }


extraction_pipeline = ExtractionPipeline()
