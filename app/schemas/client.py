"""Client API schemas for BFF endpoints."""

from typing import Any

from pydantic import BaseModel, Field


class ClientIdPath(BaseModel):
    """Path param model for client resource."""

    id: str = Field(min_length=1)


class ClientPayload(BaseModel):
    """Generic passthrough payload for upstream client operations."""

    data: dict[str, Any]


class ClientResponse(BaseModel):
    """Generic wrapper for upstream payload."""

    data: dict[str, Any]
    status: int
