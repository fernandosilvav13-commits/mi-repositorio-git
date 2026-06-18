import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Automatizacion-Ciclo"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    frontend_url: str = "http://localhost:3000"
    max_upload_size_mb: int = 50
    upload_dir: str = "uploads"
    crossref_upload_dir: str = "uploads/crossref"
    output_dir: str = "outputs"

    supabase_url: str = ""
    supabase_key: str = ""
    supabase_jwt_secret: str = ""

    llm_api_key: str = ""

    google_api_key: str = ""
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    llm_model_extract: str = "fast"
    llm_model_retry: str = "accurate"
    llm_model_crossref: str = "accurate"

    fuzzy_threshold_default: int = 70
    llm_retry_count: int = 3
    
    tesseract_cmd: str = "/home/fernandosilvav/Proyecto-Prueba/.tesseract/bin/tesseract"
    tesseract_data_dir: str = "/home/fernandosilvav/Proyecto-Prueba/.tesseract/tessdata"
    ocr_lang: str = "spa+eng"
    ocr_enabled: bool = True

    rate_limit_max: int = 60
    rate_limit_window: int = 60

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
