from fastapi import APIRouter, HTTPException
from app.schemas.rules import RuleCreate, RuleResponse
from app.core.database import require_supabase
from app.services.rules_engine import RulesEngine

router = APIRouter()
engine = RulesEngine()


@router.post("/", response_model=RuleResponse)
async def create_rule(data: RuleCreate):
    supabase = require_supabase()
    result = supabase.table("rules").insert(data.model_dump()).execute()
    return result.data[0]


@router.get("/", response_model=list[RuleResponse])
async def list_rules():
    supabase = require_supabase()
    result = supabase.table("rules").select("*").execute()
    return result.data


@router.post("/evaluate")
async def evaluate_rules(data: dict):
    supabase = require_supabase()
    rules = supabase.table("rules").select("*").eq("enabled", True).execute()
    triggered = engine.evaluate_rules(rules.data, data)
    return {"triggered": triggered}
