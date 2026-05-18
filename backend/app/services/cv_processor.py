import pandas as pd
import asyncio
from pathlib import Path
from app.services.cv_extractor import extract_cv_data
from app.services.gender_service import infer_gender
from app.services.phone_service import normalize_phone
from app.services.experience_service import get_top_3_experiences
from app.utils.rut_formatter import RUTFormatter
from app.utils.logger import setup_logger

logger = setup_logger("cv_processor")


def _titlecase_name(name: str) -> str:
    if not name or name == "NO ENCONTRADO":
        return name
    return name.strip().title()


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
                logger.warning("Matricula CSV not found at %s", csv_path)
                return {}
        
        try:
            logger.info("Loading matricula data from %s...", path)
            df = pd.read_csv(path, dtype=str)
            df["MAT_TOTAL"] = df["MAT_TOTAL"].fillna("0")
            # Create a lookup by lower-case school name
            # Use vectorized operations instead of iterrows
            df["NOM_RBD_LOWER"] = df["NOM_RBD"].str.strip().str.lower()
            lookup = df.set_index("NOM_RBD_LOWER").to_dict("index")
            logger.info("Loaded %d school records.", len(lookup))
            return lookup
        except Exception as e:
            logger.error("Error loading matricula data: %s", e)
            return {}

    def _post_process(self, data: dict) -> dict:
        genero = data.get("GENERO", "")
        if not genero or genero == "NO ENCONTRADO":
            nombres = data.get("NOMBRES", "")
            if nombres and nombres != "NO ENCONTRADO":
                data["GENERO"] = infer_gender(nombres)

        for phone_field in ("TELEFONO_CELULAR", "TELEFONO_FIJO"):
            val = data.get(phone_field, "")
            if val and val != "NO ENCONTRADO":
                _type, formatted = normalize_phone(val)
                if _type != "NO ENCONTRADO":
                    data[phone_field] = formatted

        rut = data.get("RUT", "")
        if rut and rut != "NO ENCONTRADO":
            data["RUT"] = RUTFormatter.format(rut)

        for field in ("NOMBRES", "APELLIDOS"):
            val = data.get(field, "")
            if val and val != "NO ENCONTRADO":
                data[field] = _titlecase_name(val)

        return data

    async def process(self, raw_text: str, is_retry: bool = False, schema: dict | None = None) -> dict:
        data = await extract_cv_data(raw_text, is_retry=is_retry, schema=schema)
        if not data:
            return {}

        exp_key = next((k for k in data.keys() if "EXPERIENCIA" in k.upper()), None)
        if exp_key:
            experiences = data.get(exp_key, [])
            if experiences and isinstance(experiences, list):
                data[exp_key] = get_top_3_experiences(experiences, self.matricula_lookup)

        data = self._post_process(data)
        return data

    async def process_many(self, texts: list[str], is_retry: bool = False, schema: dict | None = None) -> list[dict]:
        tasks = [self.process(t, is_retry=is_retry, schema=schema) for t in texts]
        return await asyncio.gather(*tasks)

cv_processor = CVProcessor()
