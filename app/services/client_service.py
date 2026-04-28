"""Client use cases and operation audit orchestration."""

import logging
from datetime import UTC, datetime
from typing import Any

from app.domain.entities.operation import OperationEntity
from app.repositories.operation_repository import OperationRepository
from app.services.external_api_client import ExternalApiClient

logger = logging.getLogger(__name__)


class ClientService:
    """Orchestrates client proxy operations and audit logs."""

    def __init__(self, external_api: ExternalApiClient, operation_repo: OperationRepository) -> None:
        self._external_api = external_api
        self._operation_repo = operation_repo

    async def list_clients(self, token: str, payload: dict[str, Any]) -> tuple[int, Any]:
        return await self._external_api.list_clients(token=token, payload=payload)

    async def list_interests(self, token: str) -> tuple[int, Any]:
        return await self._external_api.list_interests(token=token)

    async def get_client(self, token: str, client_id: str) -> tuple[int, Any]:
        return await self._external_api.get_client(token=token, client_id=client_id)

    async def create_client(self, token: str, payload: dict[str, Any], user: str) -> tuple[int, Any]:
        status, data = await self._external_api.create_client(token=token, payload=payload)
        client_id = ""
        if isinstance(data, dict):
            client_id = str(data.get("id", payload.get("id", "")))
        await self._safe_log("CREAR", user, client_id, status)
        return status, data

    async def update_client(self, token: str, payload: dict[str, Any], user: str) -> tuple[int, Any]:
        status, data = await self._external_api.update_client(token=token, payload=payload)
        client_id = ""
        if isinstance(data, dict):
            client_id = str(data.get("id", payload.get("id", "")))
        await self._safe_log("ACTUALIZAR", user, client_id, status)
        return status, data

    async def delete_client(self, token: str, client_id: str, user: str) -> tuple[int, Any]:
        status, data = await self._external_api.delete_client(token=token, client_id=client_id)
        await self._safe_log("ELIMINAR", user, client_id, status)
        return status, data

    async def _safe_log(self, action: str, user: str, client_id: str, status: int) -> None:
        """Best-effort audit persistence without breaking main flow."""
        try:
            await self._operation_repo.log_operation(
                OperationEntity(
                    accion=action,  # type: ignore[arg-type]
                    usuario=user,
                    cliente_id=client_id,
                    timestamp=datetime.now(UTC),
                    resultado=status,
                )
            )
        except Exception:
            logger.exception("Failed to persist operation audit log")
