"""Unit tests for auth service."""

from unittest.mock import AsyncMock

import pytest

from app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_login_persists_session():
    """Auth service should persist session after successful login."""
    external = AsyncMock()
    external.login.return_value = (
        200,
        {"token": "tkn", "expiration": "2022-04-28T03:39:32Z", "userid": "u1", "username": "john"},
    )
    repo = AsyncMock()
    service = AuthService(external_api=external, session_repo=repo)

    result = await service.login("john", "secret")

    assert result["token"] == "tkn"
    assert result["expiration"] == "2022-04-28T03:39:32Z"
    assert result["userid"] == "u1"
    repo.create_session.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_returns_upstream_fields():
    """Register should return upstream status and message."""
    external = AsyncMock()
    external.register.return_value = (200, {"status": "Success", "message": "Usuario creado correctamente"})
    repo = AsyncMock()
    service = AuthService(external_api=external, session_repo=repo)

    result = await service.register("newuser", "new@example.com", "secret")

    assert result["status"] == "Success"
    assert "creado" in result["message"]
    external.register.assert_awaited_once_with(
        {"username": "newuser", "email": "new@example.com", "password": "secret"}
    )
