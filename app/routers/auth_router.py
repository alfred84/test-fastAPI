"""Auth endpoints for session lifecycle."""

from fastapi import APIRouter, Depends

from app.core.dependencies import get_auth_service
from app.core.security import extract_bearer_token
from app.schemas.auth import LoginRequest, LoginResponse, LogoutResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> LoginResponse:
    """Proxy login and persist local session."""
    result = await service.login(username=payload.username, password=payload.password)
    return LoginResponse(**result)


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    token: str = Depends(extract_bearer_token),
    service: AuthService = Depends(get_auth_service),
) -> LogoutResponse:
    """Invalidate current session token."""
    await service.logout(token=token)
    return LogoutResponse(message="Session closed.")
