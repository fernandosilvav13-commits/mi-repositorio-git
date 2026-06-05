from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
import jwt

security = HTTPBearer(auto_error=False)


async def verify_token(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> dict:
    if settings.environment == "development" and not credentials:
        return {"sub": "dev-user", "email": "dev@localhost", "role": "dev"}
    if not credentials:
        raise HTTPException(401, detail="Token requerido")
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(401, detail="Token inválido")


async def require_auth(request: Request):
    auth_header = request.headers.get("Authorization", "")
    if settings.environment == "development" and not auth_header:
        request.state.user = {"sub": "dev-user", "email": "dev@localhost"}
        return
    if not auth_header.startswith("Bearer "):
        raise HTTPException(401, detail="Token requerido")
    token = auth_header.replace("Bearer ", "")
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
        request.state.user = payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(401, detail="Token inválido")
