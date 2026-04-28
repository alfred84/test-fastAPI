"""Integration tests placeholder for clients endpoints."""

import pytest


@pytest.mark.asyncio
async def test_clients_requires_auth(async_client):
    """Clients endpoint should reject requests without bearer token."""
    response = await async_client.post("/api/Cliente/Listado", json={"identificacion": "", "usuarioId": "u1"})
    assert response.status_code == 401
