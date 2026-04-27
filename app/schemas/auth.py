"""Auth request/response schemas."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Credentials payload proxied to external API."""

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    """BFF response for successful login."""

    token: str
    userid: str
    username: str


class LogoutResponse(BaseModel):
    """Logout operation response."""

    message: str
