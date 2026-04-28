"""REST routes under /api matching the React SPA wire contract (proxied to EXTERNAL_API_URL)."""

from typing import Any

from fastapi import APIRouter, Depends, Response

from app.core.dependencies import get_auth_service, get_client_service, get_current_session
from app.core.security import extract_bearer_token
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.schemas.client import ClientCreateRequest, ClientListRequest, ClientUpdateRequest
from app.services.auth_service import AuthService
from app.services.client_service import ClientService

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/Authenticate/login", response_model=LoginResponse)
async def authenticate_login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> LoginResponse:
    """Proxy login to upstream and persist BFF session."""
    result = await service.login(username=payload.username, password=payload.password)
    return LoginResponse(**result)


@router.post("/Authenticate/register", response_model=RegisterResponse)
async def authenticate_register(
    payload: RegisterRequest, service: AuthService = Depends(get_auth_service)
) -> RegisterResponse:
    """Proxy registration to upstream (no local session)."""
    result = await service.register(username=payload.username, email=payload.email, password=payload.password)
    return RegisterResponse(**result)


@router.post("/Authenticate/logout", response_model=LogoutResponse)
async def authenticate_logout(
    token: str = Depends(extract_bearer_token),
    service: AuthService = Depends(get_auth_service),
) -> LogoutResponse:
    """Invalidate current BFF session token."""
    await service.logout(token=token)
    return LogoutResponse(message="Session closed.")


@router.post("/Cliente/Listado")
async def cliente_listado(
    payload: ClientListRequest,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
) -> Any:
    """Proxy client list filter to upstream."""
    _, data = await service.list_clients(token=session["token"], payload=payload.to_upstream_payload())
    return data


@router.delete("/Cliente/Eliminar/{id_cliente}")
async def cliente_eliminar(
    id_cliente: str,
    response: Response,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
) -> Any:
    """Proxy delete client to upstream."""
    status, data = await service.delete_client(token=session["token"], client_id=id_cliente, user=session["username"])
    response.status_code = status
    return data


@router.get("/Intereses/Listado")
async def intereses_listado(
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
) -> Any:
    """Proxy interests catalog to upstream."""
    _, data = await service.list_interests(token=session["token"])
    return data


@router.get("/Cliente/Obtener/{id_cliente}")
async def cliente_obtener(
    id_cliente: str,
    response: Response,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
) -> Any:
    """Proxy get client detail to upstream."""
    status, data = await service.get_client(token=session["token"], client_id=id_cliente)
    response.status_code = status
    return data


@router.post("/Cliente/Crear")
async def cliente_crear(
    payload: ClientCreateRequest,
    response: Response,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
) -> Any:
    """Proxy create client to upstream."""
    status, data = await service.create_client(
        token=session["token"], payload=payload.model_dump(), user=session["username"]
    )
    response.status_code = status
    return data


@router.post("/Cliente/Actualizar")
async def cliente_actualizar(
    payload: ClientUpdateRequest,
    response: Response,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
) -> Any:
    """Proxy update client to upstream."""
    status, data = await service.update_client(
        token=session["token"], payload=payload.model_dump(), user=session["username"]
    )
    response.status_code = status
    return data
