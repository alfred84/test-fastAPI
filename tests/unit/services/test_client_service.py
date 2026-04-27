"""Unit tests for client service."""

from unittest.mock import AsyncMock

import pytest

from app.services.client_service import ClientService


@pytest.mark.asyncio
async def test_create_client_logs_operation():
    """Create should call operation repository with audit payload."""
    external = AsyncMock()
    external.create_client.return_value = (201, {"id": "c1"})
    repo = AsyncMock()
    service = ClientService(external_api=external, operation_repo=repo)

    status, payload = await service.create_client("tkn", {"name": "Acme"}, "john")

    assert status == 201
    assert payload["id"] == "c1"
    repo.log_operation.assert_awaited_once()
