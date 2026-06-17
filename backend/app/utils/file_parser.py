from pathlib import Path
from app.utils.logger import setup_logger

logger = setup_logger("file_parser")
import re
import pdfplumber
from PIL import Image
from docx import Document as DocxDocument
import pandas as pd
import os
import pytesseract
from app.core.config import settings

# Set tesseract environment for local install
_tess_dir = os.path.dirname(os.path.dirname(getattr(settings, "tesseract_cmd", "")))
_lib_dir = os.path.join(os.path.dirname(_tess_dir), "lib")
_tessdata_dir = getattr(settings, "tesseract_data_dir", "")
if _lib_dir and os.path.isdir(_lib_dir):
    os.environ.setdefault("LD_LIBRARY_PATH", _lib_dir)
    os.environ.setdefault("TESSDATA_PREFIX", _tessdata_dir or os.path.join(os.path.dirname(_lib_dir), "tessdata"))
if _tessdata_dir:
    os.environ["TESSDATA_PREFIX"] = _tessdata_dir


class FileParser:
    @staticmethod
    def extract_text(file_path: str) -> str:
        path = Path(file_path)
        ext = path.suffix.lower()

        match ext:
            case ".pdf":
                return FileParser._parse_pdf(file_path)
            case ".docx":
                return FileParser._parse_docx(file_path)
            case ".doc":
                return FileParser._parse_doc(file_path)
            case ".csv":
                return FileParser._parse_csv(file_path)
            case ".jpg" | ".jpeg" | ".png" | ".tiff" | ".bmp":
                return FileParser._ocr_image(file_path)
            case _:
                raise ValueError(f"Formato no soportado: {ext}")

    @staticmethod
    def _parse_pdf(file_path: str) -> str:
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        result = "\n".join(text_parts).strip()
        if not result:
            return FileParser._ocr_image(file_path)
        return result

    @staticmethod
    def _parse_docx(file_path: str) -> str:
        doc = DocxDocument(file_path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        if text.strip():
            return text
        try:
            import subprocess, tempfile, os
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                pdf_path = tmp.name
            subprocess.run(
                ["libreoffice", "--headless", "--convert-to", "pdf", file_path,
                 "--outdir", os.path.dirname(pdf_path)],
                capture_output=True, timeout=30, check=True
            )
            pdf_result = os.path.join(os.path.dirname(pdf_path),
                                       os.path.splitext(os.path.basename(file_path))[0] + ".pdf")
            if os.path.exists(pdf_result):
                text = FileParser._parse_pdf(pdf_result)
                os.unlink(pdf_result)
                return text.strip()
        except Exception:
            pass
        return text

    @staticmethod
    def _parse_doc_ole(file_path: str) -> str:
        with open(file_path, "rb") as f:
            magic = f.read(8)
        if magic[:8] not in (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",):
            raise ValueError("No es un archivo OLE2 valido")
        import olefile
        with olefile.OleFileIO(file_path) as ole:
            if ole.exists("WordDocument"):
                data = ole.openstream("WordDocument").read()
            else:
                data = ole.openstream(ole.listdir()[0][0]).read()
        text = ""
        i = 0
        while i < len(data) - 1:
            if data[i] == 0:
                i += 1
                continue
            if i + 1 < len(data) and data[i + 1] == 0:
                c = chr(data[i])
                if 32 <= ord(c) <= 255 or ord(c) in (10, 13, 9):
                    text += c
                i += 2
            else:
                c = chr(data[i])
                if 32 <= ord(c) <= 255 or ord(c) in (10, 13, 9):
                    text += c
                i += 1
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        result = "\n".join(lines)
        if len(result) > 30:
            return result
        raise ValueError("No se encontro texto legible en el .doc")

    @staticmethod
    def _parse_doc(file_path: str) -> str:
        try:
            return FileParser._parse_docx(file_path)
        except Exception:
            pass
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            body_match = re.search(r"<body[^>]*>(.*?)</body>", content, re.DOTALL | re.IGNORECASE)
            if body_match:
                text = body_match.group(1)
            else:
                text = content
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            if len(text) > 20:
                return text
        except Exception:
            pass
        try:
            return FileParser._parse_doc_ole(file_path)
        except Exception:
            pass
        raise ValueError(
            "No se pudo extraer texto del archivo .doc. "
            "Conviértelo a .docx (Word > Guardar como) y vuelve a subirlo."
        )

    @staticmethod
    def _parse_csv(file_path: str) -> str:
        df = pd.read_csv(file_path)
        return df.to_string(index=False)

    @staticmethod
    def _ocr_image(file_path: str) -> str:
        image = Image.open(file_path)
        if hasattr(settings, "tesseract_cmd") and settings.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd
        lang = getattr(settings, "ocr_lang", "spa+eng")
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
