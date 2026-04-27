"""Client proxy endpoints."""

from fastapi import APIRouter, Depends, Response

from app.core.dependencies import get_client_service, get_current_session
from app.schemas.client import ClientPayload
from app.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/list")
async def list_clients(
    payload: ClientPayload,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
):
    """Proxy list clients endpoint."""
    _, data = await service.list_clients(token=session["token"], payload=payload.data)
    return data


@router.post("/create")
async def create_client(
    payload: ClientPayload,
    response: Response,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
):
    """Proxy create client endpoint and audit operation."""
    status, data = await service.create_client(token=session["token"], payload=payload.data, user=session["username"])
    response.status_code = status
    return data


@router.put("/update")
async def update_client(
    payload: ClientPayload,
    response: Response,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
):
    """Proxy update client endpoint and audit operation."""
    status, data = await service.update_client(token=session["token"], payload=payload.data, user=session["username"])
    response.status_code = status
    return data


@router.delete("/{id}")
async def delete_client(
    id: str,
    response: Response,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
):
    """Proxy delete client endpoint and audit operation."""
    status, data = await service.delete_client(token=session["token"], client_id=id, user=session["username"])
    response.status_code = status
    return data


@router.get("/{id}")
async def get_client(
    id: str,
    response: Response,
    session: dict[str, str] = Depends(get_current_session),
    service: ClientService = Depends(get_client_service),
):
    """Proxy get client by id endpoint."""
    status, data = await service.get_client(token=session["token"], client_id=id)
    response.status_code = status
    return data
