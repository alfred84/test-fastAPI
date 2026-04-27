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
        token = upstream_data.get("token")
        user_id = str(upstream_data.get("userid", ""))
        resolved_username = str(upstream_data.get("username", username))
        if not token or not user_id:
            raise UnauthorizedError("Upstream login payload is missing token or userid.")
        await self._session_repo.create_session(token=token, userid=user_id, username=resolved_username)
        return {"token": token, "userid": user_id, "username": resolved_username}

    async def logout(self, token: str) -> bool:
        """Invalidate local session."""
        return await self._session_repo.delete_by_token(token)
