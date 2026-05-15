import pandas as pd
import asyncio
from pathlib import Path
from typing import Optional
from app.services.cv_extractor import extract_cv_data
from app.services.gender_service import infer_gender
from app.services.phone_service import normalize_phone
from app.services.experience_service import get_top_3_experiences
from app.utils.rut_formatter import RUTFormatter

class CVProcessor:
    def __init__(self, matricula_csv: str = "mineduc_matricula.csv"):
        self.matricula_csv = matricula_csv
        self._matricula_lookup = None

    @property
    def matricula_lookup(self):
        if self._matricula_lookup is None:
            self._matricula_lookup = self._load_matricula(self.matricula_csv)
        return self._matricula_lookup

    def _load_matricula(self, csv_path: str) -> dict:
        path = Path(csv_path)
        if not path.exists():
            # Try in parent if running from app/
            path = Path("backend") / csv_path
            if not path.exists():
                print(f"Matricula CSV not found at {csv_path}")
                return {}
        
        try:
            print(f"Loading matricula data from {path}...")
            df = pd.read_csv(path, dtype=str)
            df["MAT_TOTAL"] = df["MAT_TOTAL"].fillna("0")
            # Create a lookup by lower-case school name
            # Use vectorized operations instead of iterrows
            df["NOM_RBD_LOWER"] = df["NOM_RBD"].str.strip().str.lower()
            lookup = df.set_index("NOM_RBD_LOWER").to_dict("index")
            print(f"Loaded {len(lookup)} school records.")
            return lookup
        except Exception as e:
            print(f"Error loading matricula data: {e}")
            return {}

    async def process(self, raw_text: str, is_retry: bool = False, schema: dict | None = None) -> dict:
        # ...
        # 5. Experience Processing
        exp_key = next((k for k in data.keys() if "EXPERIENCIA" in k.upper()), None)
        if exp_key:
            experiences = data.get(exp_key, [])
            if experiences and isinstance(experiences, list):
                data[exp_key] = get_top_3_experiences(experiences, self.matricula_lookup)

        return data

    async def process_many(self, texts: list[str], is_retry: bool = False, schema: dict | None = None) -> list[dict]:
        tasks = [self.process(t, is_retry=is_retry, schema=schema) for t in texts]
        return await asyncio.gather(*tasks)

cv_processor = CVProcessor()
