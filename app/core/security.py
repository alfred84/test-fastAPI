"""Security helpers for extracting authentication tokens."""

from fastapi import Header

from app.core.exceptions import UnauthorizedError


async def extract_bearer_token(authorization: str | None = Header(default=None)) -> str:
    """Parse Bearer token from Authorization header."""
    if not authorization:
        raise UnauthorizedError("Missing Authorization header.")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise UnauthorizedError("Invalid Authorization header format.")
    return token.strip()
