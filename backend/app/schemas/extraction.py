from pydantic import BaseModel
from typing import Optional


class ExtractionRequest(BaseModel):
    template_id: str
    file_paths: list[str]
    fuzzy_threshold: int = 70


class ExtractionResult(BaseModel):
    filename: str
    status: str
    data: dict
    error: Optional[str] = None
