"""Authentication use cases."""

from app.core.exceptions import UnauthorizedError
from app.repositories.session_repository import SessionRepository
from app.services.external_api_client import ExternalApiClient


class AuthService:
    """Coordinates upstream auth and session persistence."""

    def __init__(self, external_api: ExternalApiClient, session_repo: SessionRepository) -> None:
        self._external_api = external_api
        self._session_repo = session_repo

    async def login(self, username: str, password: str) -> dict[str, str]:
        """Authenticate user against upstream and store session."""
        _, upstream_data = await self._external_api.login({"username": username, "password": password})
        if not isinstance(upstream_data, dict):
            raise UnauthorizedError("Upstream login response is invalid.")
        token = upstream_data.get("token")
        user_id = str(upstream_data.get("userid", ""))
        resolved_username = str(upstream_data.get("username", username))
        expiration = str(upstream_data.get("expiration", ""))
        if not token or not user_id:
            raise UnauthorizedError("Upstream login payload is missing token or userid.")
        await self._session_repo.create_session(token=token, userid=user_id, username=resolved_username)
        return {
            "token": str(token),
            "expiration": expiration,
            "userid": user_id,
            "username": resolved_username,
        }

    async def register(self, username: str, email: str, password: str) -> dict[str, str]:
        """Register user via upstream (no local session)."""
        _, upstream_data = await self._external_api.register(
            {"username": username, "email": email, "password": password}
        )
        if not isinstance(upstream_data, dict):
            return {"status": "", "message": ""}
        return {
            "status": str(upstream_data.get("status", "")),
            "message": str(upstream_data.get("message", "")),
        }

    async def logout(self, token: str) -> bool:
        """Invalidate local session."""
        return await self._session_repo.delete_by_token(token)
