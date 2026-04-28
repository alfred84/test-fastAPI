"""Repository for session persistence logic."""

from datetime import UTC, datetime

from app.domain.entities.session import SessionEntity
from app.repositories.models.session_document import SessionDocument


class SessionRepository:
    """Persistence access for sesiones collection."""

    @staticmethod
    def _ensure_utc(dt: datetime) -> datetime:
        """Normalize persisted datetimes so comparisons are always timezone-safe."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC)

    async def create_session(self, token: str, userid: str, username: str) -> SessionEntity:
        """Persist a new authenticated session."""
        document = SessionDocument(
            token=token,
            userid=userid,
            username=username,
            login_timestamp=datetime.now(UTC),
            expires_at=SessionDocument.build_expiration(),
        )
        await document.insert()
        return SessionEntity(
            token=document.token,
            userid=document.userid,
            username=document.username,
            login_timestamp=document.login_timestamp,
        )

    async def get_by_token(self, token: str) -> SessionEntity | None:
        """Resolve session by token if exists and non-expired."""
        document = await SessionDocument.find_one(SessionDocument.token == token)
        if document is None:
            return None
        expires_at = self._ensure_utc(document.expires_at) if document.expires_at else None
        if expires_at and expires_at < datetime.now(UTC):
            await document.delete()
            return None
        return SessionEntity(
            token=document.token,
            userid=document.userid,
            username=document.username,
            login_timestamp=document.login_timestamp,
        )

    async def delete_by_token(self, token: str) -> bool:
        """Delete active session by token."""
        document = await SessionDocument.find_one(SessionDocument.token == token)
        if document is None:
            return False
        await document.delete()
        return True
