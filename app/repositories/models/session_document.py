"""Beanie document for session persistence."""

from datetime import UTC, datetime, timedelta

from beanie import Document, Indexed
from pydantic import Field
from pymongo import IndexModel

from app.core.config import get_settings


class SessionDocument(Document):
    """Mongo collection for user sessions."""

    token: Indexed(str, unique=True)  # type: ignore[valid-type]
    userid: str
    username: str
    login_timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime | None = None

    class Settings:
        """Beanie collection metadata."""

        name = "sesiones"
        indexes = [
            [("userid", 1), ("login_timestamp", -1)],
            IndexModel([("expires_at", 1)], expireAfterSeconds=0),
        ]

    @classmethod
    def build_expiration(cls) -> datetime:
        """Compute session expiration based on settings."""
        ttl_hours = get_settings().session_ttl_hours
        return datetime.now(UTC) + timedelta(hours=ttl_hours)
