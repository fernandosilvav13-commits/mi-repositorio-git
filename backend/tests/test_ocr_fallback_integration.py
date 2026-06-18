"""Integration test: OCR fallback & OLE2 noise fix."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "manual"

from app.services.ocr_service import ocr_service
from app.utils.file_parser import FileParser


def test_scanned_docx():
    docx = FIXTURES / "127944113_2328_cv_2026033122717.docx"
    text = ocr_service.extract_with_fallback(str(docx))
    print(f"\n=== Scanned DOCX ===")
    print(f"Length: {len(text)}")
    keywords = ["MIGUEL", "CARO", "EXPERIENCIA", "PROFESIONAL", "EDUCACION"]
    found = [kw for kw in keywords if kw.lower() in text.lower()]
    print(f"Keywords found: {found}")
    assert len(text) > 1000, f"Too little text: {len(text)}"
    return text


def test_large_doc():
    doc = FIXTURES / "106071497_2052_cv_20260107105327.doc"
    text = FileParser.extract_text(str(doc))
    print(f"\n=== 12MB .doc ===")
    print(f"Length: {len(text)}")
    assert len(text) < 100000, f"Still too much noise: {len(text)}"
    assert len(text) > 100, f"Too little text: {len(text)}"
    print(f"First 800 chars:\n{text[:800]}")
    return text


if __name__ == "__main__":
    t1 = test_scanned_docx()
    print(f"\nScanned DOCX: {len(t1)} chars ✅")
    t2 = test_large_doc()
    print(f"\n12MB .doc: {len(t2)} chars ✅")
