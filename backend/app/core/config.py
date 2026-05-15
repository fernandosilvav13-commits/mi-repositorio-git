from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Automatizacion-Ciclo"
    debug: bool = False
    max_upload_size_mb: int = 50
    upload_dir: str = "uploads"
    crossref_upload_dir: str = "uploads/crossref"
    output_dir: str = "outputs"

    supabase_url: str = ""
    supabase_key: str = ""

    google_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    fuzzy_threshold_default: int = 70
    llm_retry_count: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
