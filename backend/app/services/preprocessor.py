import re
from typing import Optional

SECTIONS = {
    "nombres": r"(?:nombre|nombres|apellido|apellidos|datos personales)[:\s]*([A-Za-záéíóúñÁÉÍÓÚÑ\s]+)",
    "rut": r"(?:rut|run|cedula|cédula)[:\s]*([0-9.]+-[0-9kK])",
    "telefono": r"(?:tel[ée]fono|celular|movil|móvil|contacto)[:\s]*([+\d\s\-()]{7,20})",
    "correo": r"(?:correo|email|e-mail)[:\s]*([\w.+-]+@[\w-]+\.[\w.]+)",
    "nacionalidad": r"(?:nacionalidad)[:\s]*([A-Za-záéíóúñÁÉÍÓÚÑ\s]+)",
    "titulos": r"(?:titulo|título|títulos|títulos|grado|profesión|profesion)[:\s]*(.+?)(?=\n\s*\n|\Z)",
    "experiencia": r"(?:experiencia|experiencia laboral|antecedentes)[:\s]*(.+?)(?=\n\s*\n\s*(?:formacion|formación|educación|educacion|estudios| capacitación|certificaciones|idiomas|\Z))",
}

# Redundant phrases to remove to save tokens
REDUNDANT_PHRASES = [
    r"curriculum vitae", r"currículum vitae", r"hoja de vida",
    r"resumen profesional", r"perfil profesional",
    r"referencias laborales disponibles a solicitud",
    r"disponibilidad inmediata",
]

def clean_text(text: str) -> str:
    """Basic cleaning to remove double spaces and redundant phrases."""
    for phrase in REDUNDANT_PHRASES:
        text = re.sub(phrase, "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_sections(text: str) -> dict[str, str]:
    result = {}
    for key, pattern in SECTIONS.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            value = match.group(1).strip()
            value = re.sub(r"\s+", " ", value)
            if len(value) > 5: # Slightly more lenient
                result[key] = value[:1500] # Reduced from 2000 to save tokens
    return result

def compress_experience(text: str, max_lines: int = 20) -> str: # Reduced from 30 to 20
    lines = text.split("\n")
    kept = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Only keep lines with high information density
        if any(kw in stripped.lower() for kw in ["experiencia", "establecimiento", "empresa", "cargo", "función", "funcion", "desde", "hasta", "actualidad", "años", "meses"]):
            kept.append(stripped)
        elif re.match(r"^\d{4}", stripped):
            kept.append(stripped)
        elif len(stripped) > 30 and len(kept) < max_lines:
            kept.append(stripped)
        if len(kept) >= max_lines:
            break
    return "\n".join(kept)

def preprocess_cv_text(raw_text: str) -> str:
    # First, do a very basic cleaning
    cleaned_raw = clean_text(raw_text)
    
    sections = extract_sections(raw_text) # Use original for extraction as regex might prefer it
    parts = []
    for section_name in ["nombres", "rut", "telefono", "correo", "nacionalidad", "titulos"]:
        if section_name in sections:
            parts.append(f"#{section_name.upper()}: {sections[section_name]}") # Compact format
            
    if "experiencia" in sections:
        exp = compress_experience(sections["experiencia"])
        if exp:
            parts.append(f"#EXP:\n{exp}")
            
    if not parts:
        return cleaned_raw[:4000] # Reduced from 5000 to 4000
        
    final_text = "\n".join(parts)
    return final_text[:6000] # Hard limit on total tokens sent
