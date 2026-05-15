from fastapi import APIRouter, UploadFile, File, Depends
from pathlib import Path
import aiofiles
from app.core.config import settings
from app.core.auth import require_auth
from app.core.security import validate_upload, sanitize_filename
from app.services.ocr_service import OCRService

router = APIRouter(dependencies=[Depends(require_auth)])
ocr_service = OCRService()

upload_dir = Path(settings.UPLOAD_DIR) if hasattr(settings, 'UPLOAD_DIR') else Path("uploads")
upload_dir.mkdir(exist_ok=True)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    content = await file.read()
    validate_upload(content, file.filename)
    safe_name = sanitize_filename(file.filename)
    file_path = upload_dir / safe_name
    async with aiofiles.open(str(file_path), "wb") as buffer:
        await buffer.write(content)
    return {"files": [str(file_path)], "count": 1}


@router.post("/process")
async def process_files(file_paths: list[str]):
    results = ocr_service.process_batch(file_paths)
    return {"results": results}
