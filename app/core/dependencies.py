"""Dependency providers for routers and services."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import Depends, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import Settings, get_settings
from app.core.exceptions import UnauthorizedError
from app.core.security import extract_bearer_token
from app.repositories.models.operation_document import OperationDocument
from app.repositories.models.session_document import SessionDocument
from app.repositories.operation_repository import OperationRepository
from app.repositories.session_repository import SessionRepository
from app.services.auth_service import AuthService
from app.services.client_service import ClientService
from app.services.external_api_client import ExternalApiClient

_mongo_client: AsyncIOMotorClient | None = None


@asynccontextmanager
async def lifespan_context(app: FastAPI) -> AsyncIterator[None]:
    """Initialize and close Mongo/Beanie lifecycle resources."""
    global _mongo_client
    settings = get_settings()
    _mongo_client = AsyncIOMotorClient(settings.mongodb_url)
    database = _mongo_client.get_default_database()
    if database is None:
        database = _mongo_client["test_fastapi"]
    await init_beanie(database=database, document_models=[SessionDocument, OperationDocument])
    yield
    _mongo_client.close()


def get_external_api(settings: Settings = Depends(get_settings)) -> ExternalApiClient:
    """Create external API adapter instance."""
    return ExternalApiClient(settings=settings)


def get_session_repository() -> SessionRepository:
    """Provide session repository."""
    return SessionRepository()


def get_operation_repository() -> OperationRepository:
    """Provide operation repository."""
    return OperationRepository()


def get_auth_service(
    external_api: ExternalApiClient = Depends(get_external_api),
    session_repo: SessionRepository = Depends(get_session_repository),
) -> AuthService:
    """Provide auth service."""
    return AuthService(external_api=external_api, session_repo=session_repo)


def get_client_service(
    external_api: ExternalApiClient = Depends(get_external_api),
    operation_repo: OperationRepository = Depends(get_operation_repository),
) -> ClientService:
    """Provide client service."""
    return ClientService(external_api=external_api, operation_repo=operation_repo)


async def get_current_session(
    token: str = Depends(extract_bearer_token),
    session_repo: SessionRepository = Depends(get_session_repository),
) -> dict[str, str]:
    """Resolve authenticated user context from persisted session."""
    session = await session_repo.get_by_token(token)
    if not session:
        raise UnauthorizedError()
    return {"token": session.token, "userid": session.userid, "username": session.username}
