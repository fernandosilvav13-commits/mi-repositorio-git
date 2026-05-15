import re
from pathlib import Path
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

MAGIC_BYTES: dict[str, list[bytes]] = {
    ".pdf": [b"%PDF"],
    ".docx": [b"PK\x03\x04"],
    ".doc": [b"\xd0\xcf\x11\xe0"],
    ".xlsx": [b"PK\x03\x04"],
    ".csv": [b"", b",", b"\""],
    ".jpg": [b"\xff\xd8\xff"],
    ".jpeg": [b"\xff\xd8\xff"],
    ".png": [b"\x89PNG"],
    ".ppt": [b"\xd0\xcf\x11\xe0"],
    ".pptx": [b"PK\x03\x04"],
}

MAX_UPLOAD_SIZE = 50 * 1024 * 1024

SENSITIVE_PATTERNS = [
    re.compile(r"sk_(live|test)_[0-9a-zA-Z]+"),
    re.compile(r"ghp_[0-9a-zA-Z]+"),
    re.compile(r"github_pat_[0-9a-zA-Z_]+"),
    re.compile(r"AQ\.[0-9a-zA-Z]+"),
    re.compile(r"AIza[0-9A-Za-z_-]+"),
]


def validate_magic_bytes(content: bytes, ext: str) -> bool:
    expected = MAGIC_BYTES.get(ext.lower())
    if expected is None:
        return False
    return any(content.startswith(m) for m in expected if m)


def validate_upload(file_content: bytes, filename: str) -> None:
    ext = Path(filename).suffix.lower()
    if ext not in MAGIC_BYTES:
        raise HTTPException(400, f"Formato no soportado: {ext}")
    if len(file_content) > MAX_UPLOAD_SIZE:
        raise HTTPException(400, "Archivo excede el límite de 50MB")
    if not validate_magic_bytes(file_content, ext):
        raise HTTPException(400, f"El archivo no parece un {ext} válido")


def sanitize_filename(filename: str) -> str:
    clean = re.sub(r"[^\w\.\-]", "_", filename)
    return clean[:255]


def contains_sensitive_data(text: str) -> bool:
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            return True
    return False


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = __import__("time").time()
        window_start = now - self.window_seconds
        if client_ip in self.requests:
            self.requests[client_ip] = [t for t in self.requests[client_ip] if t > window_start]
            if len(self.requests[client_ip]) >= self.max_requests:
                raise HTTPException(429, detail="Demasiadas solicitudes. Intenta de nuevo en 60 segundos.")
            self.requests[client_ip].append(now)
        else:
            self.requests[client_ip] = [now]
        return await call_next(request)
