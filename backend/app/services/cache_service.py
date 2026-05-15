import json
import hashlib
import os
from pathlib import Path
from typing import Any, Optional
from app.core.config import settings

class CacheService:
    def __init__(self, cache_dir: str = ".cache/extraction"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_hash(self, text: str, schema: dict, model: str) -> str:
        # Create a unique key based on text content, schema structure and model
        schema_str = json.dumps(schema, sort_keys=True)
        combined = f"{text}|{schema_str}|{model}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def get(self, text: str, schema: dict, model: str) -> Optional[dict]:
        cache_key = self._get_hash(text, schema, model)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def set(self, text: str, schema: dict, model: str, result: dict):
        cache_key = self._get_hash(text, schema, model)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            with open(cache_file, "w") as f:
                json.dump(result, f)
        except Exception as e:
            print(f"Error saving to cache: {e}")

cache_service = CacheService()
