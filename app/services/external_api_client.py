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

    async def _request(
        self,
        method: str,
        path: str,
        *,
        token: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> tuple[int, dict[str, Any]]:
        headers: dict[str, str] = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        attempts = max(1, self._settings.httpx_retry_attempts)
        backoff = self._settings.httpx_retry_backoff_ms / 1000

        for attempt in range(attempts):
            try:
                async with httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout) as client:
                    response = await client.request(method=method, url=path, json=payload, headers=headers)
                try:
                    data = response.json()
                except ValueError:
                    data = {}
                if response.status_code >= 400:
                    message = data.get("message") if isinstance(data, dict) else "Upstream request failed."
                    raise UpstreamRejectedError(message=message or "Upstream request failed.", status_code=response.status_code)
                return response.status_code, data if isinstance(data, dict) else {"data": data}
            except httpx.TimeoutException as exc:
                if attempt + 1 >= attempts:
                    raise UpstreamTimeoutError() from exc
            except httpx.ConnectError as exc:
                if attempt + 1 >= attempts:
                    raise UpstreamUnavailableError() from exc
            await asyncio.sleep(backoff * (2**attempt))

        raise UpstreamUnavailableError()

    async def login(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        return await self._request("POST", "login", payload=payload)

    async def list_clients(self, token: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        return await self._request("POST", "clients/list", token=token, payload=payload)

    async def create_client(self, token: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        return await self._request("POST", "clients/create", token=token, payload=payload)

    async def update_client(self, token: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        return await self._request("PUT", "clients/update", token=token, payload=payload)

    async def delete_client(self, token: str, client_id: str) -> tuple[int, dict[str, Any]]:
        return await self._request("DELETE", f"clients/{client_id}", token=token)

    async def get_client(self, token: str, client_id: str) -> tuple[int, dict[str, Any]]:
        return await self._request("GET", f"clients/{client_id}", token=token)
