from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import httpx

# Monkeypatch httpx for compatibility with supabase-py
original_init = httpx.Client.__init__
def new_init(self, *args, **kwargs):
    if 'proxies' in kwargs:
        kwargs['proxy'] = kwargs.pop('proxies')
    return original_init(self, *args, **kwargs)
httpx.Client.__init__ = new_init

from app.core.config import settings
from app.core.ratelimit import limiter
from app.api import ingest, templates, extraction, rules, export, crossref, classify, auth_endpoint

app = FastAPI(title=settings.app_name, version="0.1.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [settings.frontend_url] if settings.environment == "production" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
app.include_router(classify.router, prefix="/api/classify", tags=["Clasificación"])
app.include_router(auth_endpoint.router, prefix="/api/auth", tags=["Autenticación"])


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name}
