from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import require_auth
from app.core.config import settings
from app.services.cv_extractor import extract_cv_data, extract_many
from app.services.ocr_service import OCRService
import os, json

router = APIRouter(dependencies=[Depends(require_auth)])
ocr_service = OCRService()


@router.post("/")
async def extract_single(data: dict):
    file_paths = data.get("file_paths", [])
    results = []
    for fp in file_paths:
        try:
            if not os.path.exists(fp):
                results.append({"filename": os.path.basename(fp), "status": "error", "data": {}, "error": "Archivo no encontrado"})
                continue
            text = ocr_service.process_document(fp)
            extracted = await extract_cv_data(text)
            if extracted is None:
                results.append({"filename": os.path.basename(fp), "status": "error", "data": {}, "error": "Error al extraer datos"})
                continue
            results.append({"filename": os.path.basename(fp), "status": "ok", "data": extracted})
        except Exception as e:
            results.append({"filename": os.path.basename(fp), "status": "error", "data": {}, "error": str(e)})
    return results


@router.post("/extract/batch")
async def extract_batch(file_paths: list[str]):
    texts = []
    errors = []
    for fp in file_paths:
        try:
            if not os.path.exists(fp):
                errors.append({"file": fp, "error": "Archivo no encontrado"})
                continue
            text = ocr_service.process_document(fp)
            texts.append(text)
        except Exception as e:
            errors.append({"file": fp, "error": str(e)})
            continue
    results = await extract_many(texts)
    output = []
    for i, fp in enumerate(file_paths):
        if i < len(results) and results[i]:
            output.append({"file": fp, "status": "ok", "data": results[i]})
        else:
            output.append({"file": fp, "status": "error"})
    return {"results": output, "errors": errors if errors else None}


@router.post("/extract/candidate")
async def extract_candidate(files: list[str]):
    combined = []
    for fp in files:
        try:
            text = ocr_service.process_document(fp)
            combined.append(text)
        except:
            continue
    full_text = "\n\n".join(combined)
    result = await extract_cv_data(full_text)
    if result is None:
        raise HTTPException(500, "Error al extraer datos")
    return result
