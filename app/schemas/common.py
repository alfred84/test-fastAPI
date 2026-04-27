"""Shared API schemas."""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Standardized error envelope."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """Top-level error response."""

    error: ErrorDetail
