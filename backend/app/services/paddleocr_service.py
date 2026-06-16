from pathlib import Path
from PIL import Image
try:
    from paddleocr import PaddleOCR as PaddleOCRClient
    _HAS_PADDLE = True
except ImportError:
    _HAS_PADDLE = False

from app.schemas.layout import TextBlock, LayoutResult
from app.core.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(" paddleocr_service)
