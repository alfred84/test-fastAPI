"""Unit tests for auth service."""

from unittest.mock import AsyncMock

import pytest

from app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_login_persists_session():
    """Auth service should persist session after successful login."""
    external = AsyncMock()
    external.login.return_value = (200, {"token": "tkn", "userid": "u1", "username": "john"})
    repo = AsyncMock()
    service = AuthService(external_api=external, session_repo=repo)

    result = await service.login("john", "secret")

    assert result["token"] == "tkn"
    repo.create_session.assert_awaited_once()
