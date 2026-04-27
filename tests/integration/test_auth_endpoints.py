"""Integration tests for auth endpoints."""

import pytest


@pytest.mark.asyncio
async def test_health_endpoint(async_client):
    """Health endpoint should be available."""
    response = await async_client.get("/health")
    assert response.status_code == 200
