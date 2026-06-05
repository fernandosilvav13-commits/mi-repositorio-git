from pydantic import BaseModel, Field
from typing import Optional


class TextBlock(BaseModel):
    text: str
    bbox: tuple[int, int, int, int]
    block_type: str = "body"

    class Config:
        frozen = True


class LayoutResult(BaseModel):
    blocks: list[TextBlock] = Field(default_factory=list)
    full_text: str = ""
    column_count: int = 1
    reading_order: list[int] = Field(default_factory=list)
