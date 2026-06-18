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
        ext = path.suffix.lower()
        if ext in (".docx", ".doc"):
            image = self._docx_to_image(file_path)
        else:
            image = Image.open(file_path)
        return layout_analyzer.analyze(image)

    def _docx_to_image(self, file_path: str) -> Image.Image:
        import zipfile, io
        try:
            with zipfile.ZipFile(file_path) as z:
                media_files = sorted(
                    f for f in z.namelist()
                    if f.startswith("word/media/") and f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))
                )
                if not media_files:
                    raise ValueError("No media files found in DOCX")
                images = []
                for mf in media_files:
                    data = z.read(mf)
                    img = Image.open(io.BytesIO(data))
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    images.append(img)
                if len(images) == 1:
                    return images[0]
                total_w = sum(img.width for img in images)
                max_h = max(img.height for img in images)
                composite = Image.new("RGB", (total_w, max_h), (255, 255, 255))
                x_offset = 0
                for img in images:
                    composite.paste(img, (x_offset, 0))
                    x_offset += img.width
                return composite
        except Exception as e:
            raise ValueError(f"Cannot convert DOCX to image: {e}")

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
