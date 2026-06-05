from pydantic import BaseModel
from typing import Optional


class MatchKey(BaseModel):
    extractionKey: str
    crossrefKey: str


class ColumnMapping(BaseModel):
    matchKeys: list[MatchKey]
    output_columns: list[str]
