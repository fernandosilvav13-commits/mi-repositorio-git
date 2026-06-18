from fastapi import APIRouter, Depends, Request
from app.core.auth import require_auth

router = APIRouter(dependencies=[Depends(require_auth)])


@router.get("/me")
async def auth_me(request: Request):
    return request.state.user
