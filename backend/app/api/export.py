from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.excel_service import ExcelService
from app.services.rules_engine import RulesEngine
from app.services.consolidator import Consolidator
from app.services.crossref_service import CrossrefService
from app.core.database import require_supabase

router = APIRouter()
excel_service = ExcelService()
rules_engine = RulesEngine()
consolidator = Consolidator()
crossref_service = CrossrefService()


@router.post("/")
async def export_to_excel(data: dict):
    template_id = data.get("template_id")
    rows = data.get("rows", [])
    crossref_file_id = data.get("crossref_file_id")
    column_mapping = data.get("column_mapping")

    if not template_id or not rows:
        raise HTTPException(400, "template_id y rows son requeridos")

    supabase = require_supabase()
    template_data = (
        supabase.table("templates").select("*").eq("id", template_id).execute()
    )
    if not template_data.data:
        raise HTTPException(404, "Plantilla no encontrada")

    columns = [c["name"] for c in template_data.data[0].get("columns", [])]
    
    # Agregar columna 'Carpeta' si viene en los datos
    if rows and "Carpeta" in rows[0] and "Carpeta" not in columns:
        columns.insert(0, "Carpeta")

    consolidated_rows, _ = consolidator.consolidate(columns, rows)

    if crossref_file_id and column_mapping:
        crossref_result = (
            supabase.table("crossref_files")
            .select("name")
            .eq("id", crossref_file_id)
            .execute()
        )
        if not crossref_result.data:
            raise HTTPException(404, "Archivo de cruce no encontrado")

        full_data = crossref_service.load_file_data(crossref_result.data[0]["name"])
        merged_rows = crossref_service.merge_data(
            rows=consolidated_rows,
            crossref_rows=full_data,
            match_column=column_mapping["match_column"],
            crossref_match_column=column_mapping["crossref_match_column"],
            output_columns=column_mapping["output_columns"],
        )
        all_columns = list(columns)
        for col in column_mapping["output_columns"]:
            if col not in all_columns:
                all_columns.append(col)
        columns = all_columns
        final_rows = merged_rows
    else:
        final_rows = consolidated_rows

    rules = supabase.table("rules").select("*").eq("enabled", True).execute()

    rules_triggered = []
    for row in final_rows:
        triggered = rules_engine.evaluate_rules(rules.data, row)
        rules_triggered.append(triggered)

    file_path = excel_service.generate(columns, final_rows, rules_triggered)
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="resultado.xlsx",
    )
