from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.core.auth import require_auth
from app.core.security import validate_upload, sanitize_filename
from app.services.crossref_service import CrossrefService
from app.core.database import require_supabase
from pathlib import Path
import aiofiles

router = APIRouter(dependencies=[Depends(require_auth)])
crossref_service = CrossrefService()
upload_dir = Path("uploads/crossref")
upload_dir.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_crossref(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    content = await file.read()
    validate_upload(content, file.filename)
    safe_name = sanitize_filename(file.filename)
    file_path = upload_dir / safe_name
    async with aiofiles.open(str(file_path), "wb") as buffer:
        await buffer.write(content)

    columns, data = crossref_service.parse_file(str(file_path))

    supabase = require_supabase()
    result = supabase.table("crossref_files").insert({
        "name": safe_name,
        "file_type": ext,
        "columns": columns,
        "data": data,
        "row_count": len(data),
    }).execute()

    return {
        "id": result.data[0]["id"],
        "name": safe_name,
        "columns": columns,
        "row_count": len(data),
    }


@router.get("/files")
async def list_files():
    supabase = require_supabase()
    result = supabase.table("crossref_files")\
        .select("id,name,file_type,columns,row_count,created_at")\
        .order("created_at", desc=True).execute()
    return result.data


@router.get("/files/{file_id}")
async def get_file(file_id: str):
    supabase = require_supabase()
    result = supabase.table("crossref_files").select("*").eq("id", file_id).execute()
    if not result.data:
        raise HTTPException(404, "Archivo no encontrado")
    return result.data[0]


@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    supabase = require_supabase()
    supabase.table("crossref_files").delete().eq("id", file_id).execute()
    return {"ok": True}
