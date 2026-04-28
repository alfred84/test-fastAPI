"""Async HTTPX adapter for Innovasoft external API."""

import asyncio
from typing import Any

import httpx

from app.core.config import Settings
from app.core.exceptions import UpstreamRejectedError, UpstreamTimeoutError, UpstreamUnavailableError


class ExternalApiClient:
    """Adapter that encapsulates all upstream HTTP calls."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._timeout = httpx.Timeout(timeout=settings.httpx_timeout_seconds)
        self._base_url = settings.external_api_url

    @staticmethod
    def _upstream_path(path: str) -> str:
        """Build upstream relative path under /api namespace."""
        normalized = path.lstrip("/")
        return normalized if normalized.startswith("api/") else f"api/{normalized}"

    async def _request(
        self,
        method: str,
        path: str,
        *,
        token: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> tuple[int, Any]:
        headers: dict[str, str] = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        attempts = max(1, self._settings.httpx_retry_attempts)
        backoff = self._settings.httpx_retry_backoff_ms / 1000

        for attempt in range(attempts):
            try:
                request_kwargs: dict[str, Any] = {"method": method, "url": path, "headers": headers}
                if payload is not None:
                    request_kwargs["json"] = payload
                async with httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout) as client:
                    response = await client.request(**request_kwargs)
                try:
                    data: Any = response.json()
                except ValueError:
                    data = {} if not response.content else None
                if response.status_code >= 400:
                    if isinstance(data, dict):
                        message = str(data.get("message") or "Upstream request failed.")
                    else:
                        message = "Upstream request failed."
                    raise UpstreamRejectedError(message=message, status_code=response.status_code)
                if data is None:
                    data = {}
                return response.status_code, data
            except httpx.TimeoutException as exc:
                if attempt + 1 >= attempts:
                    raise UpstreamTimeoutError() from exc
            except httpx.ConnectError as exc:
                if attempt + 1 >= attempts:
                    raise UpstreamUnavailableError() from exc
            await asyncio.sleep(backoff * (2**attempt))

        raise UpstreamUnavailableError()

    async def login(self, payload: dict[str, Any]) -> tuple[int, Any]:
        return await self._request("POST", self._upstream_path("Authenticate/login"), payload=payload)

    async def register(self, payload: dict[str, Any]) -> tuple[int, Any]:
        return await self._request("POST", self._upstream_path("Authenticate/register"), payload=payload)

    async def list_clients(self, token: str, payload: dict[str, Any]) -> tuple[int, Any]:
        return await self._request("POST", self._upstream_path("Cliente/Listado"), token=token, payload=payload)

    async def create_client(self, token: str, payload: dict[str, Any]) -> tuple[int, Any]:
        return await self._request("POST", self._upstream_path("Cliente/Crear"), token=token, payload=payload)

    async def update_client(self, token: str, payload: dict[str, Any]) -> tuple[int, Any]:
        return await self._request(
            "POST",
            self._upstream_path("Cliente/Actualizar"),
            token=token,
            payload=payload,
        )

    async def delete_client(self, token: str, client_id: str) -> tuple[int, Any]:
        return await self._request("DELETE", self._upstream_path(f"Cliente/Eliminar/{client_id}"), token=token)

    async def get_client(self, token: str, client_id: str) -> tuple[int, Any]:
        return await self._request("GET", self._upstream_path(f"Cliente/Obtener/{client_id}"), token=token)

    async def list_interests(self, token: str) -> tuple[int, Any]:
        return await self._request("GET", self._upstream_path("Intereses/Listado"), token=token)
