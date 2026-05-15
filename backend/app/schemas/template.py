from pydantic import BaseModel
from typing import Optional


class ColumnDefinition(BaseModel):
    name: str
    display_name: str
    data_type: str = "string"
    output_format: Optional[str] = None


class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    columns: list[ColumnDefinition]


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    columns: Optional[list[ColumnDefinition]] = None


class TemplateResponse(BaseModel):
    id: str
    name: str
    description: str
    columns: list[ColumnDefinition]
    created_by: Optional[str] = None
