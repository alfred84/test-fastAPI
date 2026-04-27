"""Custom application exceptions and FastAPI handlers."""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base application exception with stable API error payload."""

    def __init__(self, code: str, message: str, status_code: int) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class UnauthorizedError(AppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid or expired session.") -> None:
        super().__init__("UNAUTHORIZED", message, status.HTTP_401_UNAUTHORIZED)


class UpstreamTimeoutError(AppException):
    """Raised when upstream timeout occurs."""

    def __init__(self) -> None:
        super().__init__("UPSTREAM_TIMEOUT", "External service timeout.", status.HTTP_504_GATEWAY_TIMEOUT)


class UpstreamUnavailableError(AppException):
    """Raised when upstream service is unavailable."""

    def __init__(self) -> None:
        super().__init__("UPSTREAM_UNAVAILABLE", "External service unavailable.", status.HTTP_503_SERVICE_UNAVAILABLE)


class UpstreamRejectedError(AppException):
    """Raised for explicit upstream errors with known status."""

    def __init__(self, message: str, status_code: int) -> None:
        super().__init__("UPSTREAM_REJECTED", message, status_code)


async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    """Handle known app exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors with explicit payload."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": {"code": "VALIDATION_ERROR", "message": "Invalid request.", "details": exc.errors()}},
    )


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions with controlled payload."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "INTERNAL_ERROR", "message": "Unexpected internal error."}},
    )
