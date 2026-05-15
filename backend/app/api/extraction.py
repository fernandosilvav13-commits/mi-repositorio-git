from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import require_auth
from app.core.config import settings
from app.services.cv_processor import cv_processor
from app.services.ocr_service import OCRService
from app.services.cv_extractor import _build_dynamic_schema
from app.services.rules_engine import RulesEngine
from app.core.database import require_supabase
import os

router = APIRouter(dependencies=[Depends(require_auth)])
ocr_service = OCRService()
rules_engine = RulesEngine()


@router.post("/")
async def extract_single(data: dict):
    file_paths = data.get("file_paths", [])
    template_id = data.get("template_id")
    is_retry = data.get("is_retry", False)
    
    supabase = require_supabase()
    
    # Obtener plantilla
    schema = None
    if template_id:
        template_res = supabase.table("templates").select("columns").eq("id", template_id).execute()
        if template_res.data:
            schema = _build_dynamic_schema(template_res.data[0]["columns"])

    # Obtener reglas habilitadas
    rules_res = supabase.table("rules").select("*").eq("enabled", True).execute()
    active_rules = rules_res.data if rules_res.data else []

    results = []
    for fp in file_paths:
        try:
            if not os.path.exists(fp):
                results.append({"filename": os.path.basename(fp), "status": "error", "data": {}, "error": "Archivo no encontrado"})
                continue
            
            text = ocr_service.process_document(fp)
            extracted = await cv_processor.process(text, is_retry=is_retry, schema=schema)
            
            if not extracted:
                results.append({"filename": os.path.basename(fp), "status": "error", "data": {}, "error": "Error al extraer datos"})
                continue
            
            # Evaluar reglas
            triggered_rules = rules_engine.evaluate_rules(active_rules, extracted)
            
            # Guardar en Supabase
            save_res = supabase.table("extraction_results").insert({
                "template_id": template_id,
                "filename": os.path.basename(fp),
                "status": "ok",
                "data": extracted
            }).execute()
            
            results.append({
                "id": save_res.data[0]["id"] if save_res.data else None,
                "filename": os.path.basename(fp),
                "status": "ok", 
                "data": extracted,
                "rules": triggered_rules
            })
        except Exception as e:
            results.append({"filename": os.path.basename(fp), "status": "error", "data": {}, "error": str(e)})
    return results


@router.post("/extract/candidate")
async def extract_candidate(data: dict):
    files = data.get("files", [])
    template_id = data.get("template_id")
    is_retry = data.get("is_retry", False)
    
    supabase = require_supabase()
    schema = None
    if template_id:
        template_res = supabase.table("templates").select("columns").eq("id", template_id).execute()
        if template_res.data:
            schema = _build_dynamic_schema(template_res.data[0]["columns"])

    combined = []
    for fp in files:
        try:
            text = ocr_service.process_document(fp)
            combined.append(text)
        except:
            continue
    full_text = "\n\n".join(combined)
    result = await cv_processor.process(full_text, is_retry=is_retry, schema=schema)
    
    if not result:
        raise HTTPException(500, "Error al extraer datos")
    
    # Evaluar reglas
    rules_res = supabase.table("rules").select("*").eq("enabled", True).execute()
    triggered_rules = rules_engine.evaluate_rules(rules_res.data or [], result)

    # Guardar resultado combinado
    supabase.table("extraction_results").insert({
        "template_id": template_id,
        "filename": "Candidato_Combinado",
        "status": "ok",
        "data": result
    }).execute()
    
    return {"data": result, "rules": triggered_rules}


@router.post("/extract/batch")
async def extract_batch(data: dict):
    file_paths = data.get("file_paths", [])
    template_id = data.get("template_id")
    is_retry = data.get("is_retry", False)
    
    supabase = require_supabase()
    schema = None
    if template_id:
        template_res = supabase.table("templates").select("columns").eq("id", template_id).execute()
        if template_res.data:
            schema = _build_dynamic_schema(template_res.data[0]["columns"])

    # Obtener reglas habilitadas
    rules_res = supabase.table("rules").select("*").eq("enabled", True).execute()
    active_rules = rules_res.data if rules_res.data else []

    texts = []
    valid_files = []
    errors = []
    for fp in file_paths:
        try:
            if not os.path.exists(fp):
                errors.append({"file": fp, "error": "Archivo no encontrado"})
                continue
            text = ocr_service.process_document(fp)
            texts.append(text)
            valid_files.append(fp)
        except Exception as e:
            errors.append({"file": fp, "error": str(e)})
            continue
    
    results_data = await cv_processor.process_many(texts, is_retry=is_retry, schema=schema)
    
    output = []
    for i, extracted in enumerate(results_data):
        filename = os.path.basename(valid_files[i])
        
        # Evaluar reglas
        triggered_rules = rules_engine.evaluate_rules(active_rules, extracted)

        # Guardar en Supabase
        save_res = supabase.table("extraction_results").insert({
            "template_id": template_id,
            "filename": filename,
            "status": "ok",
            "data": extracted
        }).execute()
        
        output.append({
            "id": save_res.data[0]["id"] if save_res.data else None,
            "file": valid_files[i],
            "status": "ok",
            "data": extracted,
            "rules": triggered_rules
        })
            
    return {"results": output, "errors": errors if errors else None}
