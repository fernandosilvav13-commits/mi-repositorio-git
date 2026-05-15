from fastapi import APIRouter, Depends
from app.core.auth import require_auth
from app.core.database import require_supabase

router = APIRouter(dependencies=[Depends(require_auth)])


@router.get("/")
async def list_templates():
    supabase = require_supabase()
    result = supabase.table("templates").select("*").execute()
    return result.data


@router.post("/")
async def create_template(data: dict):
    supabase = require_supabase()
    result = supabase.table("templates").insert(data).execute()
    return result.data[0]


@router.get("/{template_id}")
async def get_template(template_id: str):
    supabase = require_supabase()
    result = supabase.table("templates").select("*").eq("id", template_id).execute()
    if not result.data:
        return {"error": "not found"}
    return result.data[0]


@router.put("/{template_id}")
async def update_template(template_id: str, data: dict):
    supabase = require_supabase()
    result = supabase.table("templates").update(data).eq("id", template_id).execute()
    return result.data[0]


@router.delete("/{template_id}")
async def delete_template(template_id: str):
    supabase = require_supabase()
    supabase.table("templates").delete().eq("id", template_id).execute()
    return {"ok": True}
