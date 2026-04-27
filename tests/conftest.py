"""Test fixtures."""

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def test_app() -> FastAPI:
    """Return FastAPI app for integration tests."""
    return app


@pytest.fixture
async def async_client(test_app: FastAPI):
    """Create async HTTP client over ASGI app."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
