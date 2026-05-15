from pydantic import BaseModel
from typing import Optional


class ColumnMapping(BaseModel):
    match_column: str
    crossref_match_column: str
    output_columns: list[str]
