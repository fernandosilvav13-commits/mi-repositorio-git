from pathlib import Path
from PIL import Image
from app.utils.file_parser import FileParser
from app.services.layout_analyzer import layout_analyzer
from app.schemas.layout import LayoutResult
from app.core.config import settings
from app.utils.logger import setup_logger

logger = setup_logger("ocr_service")


class OCRService:
    def __init__(self):
        self.parser = FileParser()

    def process_document(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        return self.parser.extract_text(file_path)

    def process_batch(self, file_paths: list[str]) -> dict[str, str]:
        results = {}
        for fp in file_paths:
            try:
                results[fp] = self.process_document(fp)
            except Exception as e:
                results[fp] = f"ERROR: {e}"
        return results

    def extract_with_layout(self, file_path: str) -> LayoutResult:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        image = Image.open(file_path)
        return layout_analyzer.analyze(image)

    def extract_with_fallback(self, file_path: str) -> str:
        if not settings.ocr_enabled:
            return self.process_document(file_path)
        try:
            text = self.process_document(file_path)
            if text and len(text.strip()) > 20:
                return text
        except Exception as e:
            logger.warning("Primary extraction failed: %s, falling back to OCR", e)
        try:
            layout = self.extract_with_layout(file_path)
            if layout.full_text:
                return layout.full_text
        except Exception as e:
            logger.error("OCR fallback also failed: %s", e)
        return ""


ocr_service = OCRService()
