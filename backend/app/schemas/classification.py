from pydantic import BaseModel, Field
from typing import Literal

DocumentCategory = Literal["cv", "non-cv"]

class ClassificationResult(BaseModel):
    category: DocumentCategory
    confidence: float = Field(ge=0.0, le=1.0)
    top_categories: list[dict] = Field(default_factory=list)
