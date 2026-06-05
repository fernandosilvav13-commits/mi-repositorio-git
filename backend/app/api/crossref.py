import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.core.auth import require_auth
from app.core.security import validate_upload, sanitize_filename
from app.services.crossref_service import CrossrefService
from pathlib import Path
import aiofiles

router = APIRouter(dependencies=[Depends(require_auth)])
crossref_service = CrossrefService()
upload_dir = Path("uploads/crossref")
upload_dir.mkdir(parents=True, exist_ok=True)
manifest_path = upload_dir / "manifest.json"

PREVIEW_MAX_ROWS = 100


def _load_manifest() -> list[dict]:
    if manifest_path.exists():
        return json.loads(manifest_path.read_text())
    return []


def _save_manifest(entries: list[dict]):
    manifest_path.write_text(json.dumps(entries, indent=2, default=str))


@router.post("/upload")
async def upload_crossref(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    content = await file.read()
    validate_upload(content, file.filename)
    safe_name = sanitize_filename(file.filename)
    file_path = upload_dir / safe_name
    async with aiofiles.open(str(file_path), "wb") as buffer:
        await buffer.write(content)

    try:
        columns, data = crossref_service.parse_file(str(file_path))
    except Exception as e:
        raise HTTPException(400, f"Error al parsear archivo: {e}")

    entry = {
        "id": str(uuid.uuid4()),
        "name": safe_name,
        "file_type": ext,
        "columns": columns,
        "data": data[:PREVIEW_MAX_ROWS],
        "row_count": len(data),
        "status": "unmatched",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    manifest = _load_manifest()
    manifest.insert(0, entry)
    _save_manifest(manifest)

    return {k: entry[k] for k in ("id", "name", "columns", "row_count", "status")}


@router.get("/files")
async def list_files():
    manifest = _load_manifest()
    return [
        {k: e[k] for k in ("id", "name", "file_type", "columns", "row_count", "created_at", "status")}
        for e in manifest
    ]


@router.get("/files/{file_id}")
async def get_file(file_id: str):
    manifest = _load_manifest()
    for entry in manifest:
        if entry["id"] == file_id:
            return entry
    raise HTTPException(404, "Archivo no encontrado")


@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    manifest = _load_manifest()
    for i, entry in enumerate(manifest):
        if entry["id"] == file_id:
            file_path = upload_dir / entry["name"]
            if file_path.exists():
                file_path.unlink()
            manifest.pop(i)
            _save_manifest(manifest)
            return {"ok": True}
    raise HTTPException(404, "Archivo no encontrado")
