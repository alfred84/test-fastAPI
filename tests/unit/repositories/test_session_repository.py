"""Unit-like tests for session repository behavior."""

import pytest

from app.repositories.session_repository import SessionRepository


@pytest.mark.asyncio
async def test_repository_class_exists():
    """Smoke test for repository construction."""
    repo = SessionRepository()
    assert repo is not None
