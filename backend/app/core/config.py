import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Automatizacion-Ciclo"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    max_upload_size_mb: int = 50
    upload_dir: str = "uploads"
    crossref_upload_dir: str = "uploads/crossref"
    output_dir: str = "outputs"

    supabase_url: str = ""
    supabase_key: str = ""
    supabase_jwt_secret: str = ""

    google_api_key: str = ""
    gemini_model_extract: str = "gemini-2.5-flash-lite"
    gemini_model_crossref: str = "gemini-2.5-flash"
    gemini_model_retry: str = "gemini-2.5-flash"

    fuzzy_threshold_default: int = 70
    llm_retry_count: int = 3
    
    rate_limit_max: int = 60
    rate_limit_window: int = 60

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
