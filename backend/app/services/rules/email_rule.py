import re
from app.services.rules.base_rule import BaseRule
from app.services.rules.registry import rule_registry


DOMAIN_CATEGORIES = {
    r"(?:gmail|googlemail)\.\w+": "Gmail",
    r"(?:outlook|hotmail|live|msn)\.\w+": "Outlook",
    r"yahoo\.\w+": "Yahoo",
    r"correo\.\w+": "Correo.cl",
    r"(?:icloud|me\.\w+)": "iCloud",
    r"proton(?:mail)?\.\w+": "ProtonMail",
    r"(?:zohomail|zoho)\.\w+": "Zoho",
}


class EmailDomainRule(BaseRule):
    name = "email_domain"
    description = "Categorize email domain type"
    field = "DOMINIO_EMAIL"

    def evaluate(self, text: str, current_data: dict) -> str | None:
        existing = current_data.get("DOMINIO_EMAIL", "")
        if existing and existing != "NO ENCONTRADO":
            return None

        email = current_data.get("EMAIL", "")
        if not email or email == "NO ENCONTRADO":
            email_pattern = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
            if email_pattern:
                email = email_pattern.group(0)
            else:
                return None

        for pattern, category in DOMAIN_CATEGORIES.items():
            if re.search(pattern, email, re.IGNORECASE):
                return category

        domain = email.split("@")[-1].lower() if "@" in email else ""
        if domain:
            return domain

        return None


rule_registry.register(EmailDomainRule(enabled=True))
