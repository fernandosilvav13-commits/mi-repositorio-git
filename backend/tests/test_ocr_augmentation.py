import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from PIL import Image
from app.schemas.layout import TextBlock, LayoutResult


class TestTextBlock:
    def test_text_block_creation(self):
        tb = TextBlock(text="Hello", bbox=(0, 0, 100, 20), block_type="header")
        assert tb.text == "Hello"
        assert tb.bbox == (0, 0, 100, 20)
        assert tb.block_type == "header"

    def test_text_block_default_type(self):
        tb = TextBlock(text="body text", bbox=(10, 50, 200, 80))
        assert tb.block_type == "body"


class TestLayoutResult:
    def test_empty_layout(self):
        lr = LayoutResult()
        assert lr.blocks == []
        assert lr.full_text == ""
        assert lr.column_count == 1
        assert lr.reading_order == []

    def test_layout_with_blocks(self):
        blocks = [
            TextBlock(text="Header", bbox=(0, 0, 100, 20), block_type="header"),
            TextBlock(text="Body", bbox=(0, 30, 100, 60), block_type="body"),
        ]
        lr = LayoutResult(blocks=blocks, full_text="Header Body", column_count=1, reading_order=[0, 1])
        assert len(lr.blocks) == 2
        assert lr.full_text == "Header Body"


class TestLayoutAnalyzer:
    @patch("app.services.layout_analyzer._HAS_SKLEARN", False)
    @patch("app.services.layout_analyzer.Image.open")
    @patch("app.services.layout_analyzer.pytesseract.image_to_data")
    def test_analyze_empty(self, mock_itd, mock_open):
        mock_itd.return_value = {
            "text": [], "left": [], "top": [],
            "width": [], "height": [],
        }
        from app.services.layout_analyzer import LayoutAnalyzer
        analyzer = LayoutAnalyzer()
        result = analyzer.analyze(MagicMock())
        assert result.blocks == []
        assert result.full_text == ""
        assert result.column_count == 1

    @patch("app.services.layout_analyzer._HAS_SKLEARN", False)
    @patch("app.services.layout_analyzer.Image.open")
    @patch("app.services.layout_analyzer.pytesseract.image_to_data")
    def test_analyze_single_line(self, mock_itd, mock_open):
        mock_itd.return_value = {
            "text": ["Hello", "World"], "left": [0, 50], "top": [10, 10],
            "width": [40, 50], "height": [15, 15],
        }
        from app.services.layout_analyzer import LayoutAnalyzer
        analyzer = LayoutAnalyzer()
        result = analyzer.analyze(MagicMock())
        assert len(result.blocks) == 1
        assert "Hello" in result.blocks[0].text

    @patch("app.services.layout_analyzer._HAS_SKLEARN", False)
    @patch("app.services.layout_analyzer.Image.open")
    @patch("app.services.layout_analyzer.pytesseract.image_to_data")
    def test_analyzer_analyze_file(self, mock_itd, mock_open):
        mock_itd.return_value = {
            "text": ["test"], "left": [0], "top": [0],
            "width": [10], "height": [10],
        }
        from app.services.layout_analyzer import LayoutAnalyzer
        analyzer = LayoutAnalyzer()
        with patch("PIL.Image.open") as mock_img_open:
            mock_img_open.return_value = MagicMock()
            result = analyzer.analyze_file("/fake/path.png")
            assert result.full_text == "test"


class TestOCRService:
    @patch("app.services.ocr_service.Path.exists", return_value=True)
    @patch("app.services.ocr_service.settings")
    @patch("app.services.ocr_service.FileParser")
    def test_process_document(self, MockFP, mock_settings, mock_exists):
        mock_settings.ocr_enabled = True
        mock_fp = MockFP.return_value
        mock_fp.extract_text.return_value = "extracted text"
        from app.services.ocr_service import OCRService
        svc = OCRService()
        result = svc.process_document("/fake/path.pdf")
        assert result == "extracted text"

    @patch("app.services.ocr_service.Path.exists", return_value=True)
    @patch("app.services.ocr_service.settings")
    @patch("app.services.ocr_service.layout_analyzer")
    @patch("app.services.ocr_service.Image.open")
    def test_extract_with_layout(self, mock_open, mock_la, mock_settings, mock_exists):
        mock_settings.ocr_enabled = True
        mock_la.analyze.return_value = LayoutResult(
            blocks=[TextBlock(text="test", bbox=(0, 0, 10, 10))],
            full_text="test",
            column_count=1,
            reading_order=[0],
        )
        from app.services.ocr_service import OCRService
        svc = OCRService()
        mock_open.return_value = MagicMock()
        result = svc.extract_with_layout("/fake/path.png")
        assert result.full_text == "test"

    @patch("app.services.ocr_service.Path.exists", return_value=True)
    @patch("app.services.ocr_service.settings")
    def test_extract_with_fallback_disabled(self, mock_settings, mock_exists):
        mock_settings.ocr_enabled = False
        from app.services.ocr_service import OCRService
        svc = OCRService()
        with patch.object(svc.parser, "extract_text", return_value="primary text"):
            result = svc.extract_with_fallback("/fake/path.pdf")
            assert result == "primary text"

    @patch("app.services.ocr_service.Image.open")
    @patch("app.services.ocr_service.Path.exists", return_value=True)
    @patch("app.services.ocr_service.settings")
    @patch("app.services.ocr_service.layout_analyzer")
    def test_extract_with_fallback_primary_fails(self, mock_la, mock_settings, mock_exists, mock_img):
        mock_settings.ocr_enabled = True
        mock_la.analyze.return_value = LayoutResult(full_text="ocr fallback text")
        mock_img.return_value = MagicMock()
        from app.services.ocr_service import OCRService
        svc = OCRService()
        with patch.object(svc.parser, "extract_text", side_effect=Exception("fail")):
            result = svc.extract_with_fallback("/fake/path.pdf")
            assert result == "ocr fallback text"
