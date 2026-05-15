from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import ingest, templates, extraction, rules, export, crossref

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingesta"])
app.include_router(templates.router, prefix="/api/templates", tags=["Plantillas"])
app.include_router(extraction.router, prefix="/api/extraction", tags=["Extracción"])
app.include_router(rules.router, prefix="/api/rules", tags=["Reglas"])
app.include_router(export.router, prefix="/api/export", tags=["Exportación"])
app.include_router(crossref.router, prefix="/api/crossref", tags=["Cruzar Datos"])


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name}
