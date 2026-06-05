import re
from app.services.rules.base_rule import BaseRule
from app.services.rules.registry import rule_registry

NATIONALITIES = {
    "chilen[aio]": "Chilena",
    "argentin[aio]": "Argentina",
    "peruan[aio]": "Peruana",
    "bolivian[aio]": "Boliviana",
    "brasileñ[ao]": "Brasileña",
    "colombian[aio]": "Colombiana",
    "ecuatorian[aio]": "Ecuatoriana",
    "mexican[aio]": "Mexicana",
    "venezolan[aio]": "Venezolana",
    "uruguay[ao]": "Uruguaya",
    "paraguay[ao]": "Paraguaya",
    "costarricense": "Costarricense",
    "hondureñ[ao]": "Hondureña",
    "salvadoreñ[ao]": "Salvadoreña",
    "guatemaltec[ao]": "Guatemalteca",
    "cuban[ao]": "Cubana",
    "dominic[ao]": "Dominicana",
    "español[ao]": "Española",
    "estadounidense": "Estadounidense",
}


class NationalityRule(BaseRule):
    name = "nationality"
    description = "Infer nationality from document text"
    field = "NACIONALIDAD"

    def evaluate(self, text: str, current_data: dict) -> str | None:
        existing = current_data.get("NACIONALIDAD", "")
        if existing and existing != "NO ENCONTRADO":
            return None
        text_lower = text.lower()
        for pattern, nationality in NATIONALITIES.items():
            if re.search(r"\b" + pattern + r"\b", text_lower):
                return nationality
        return None


rule_registry.register(NationalityRule())
