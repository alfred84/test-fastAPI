"""Beanie document for auditable write operations."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document
from pydantic import Field


class OperationDocument(Document):
    """Mongo collection for CRUD operation logs."""

    accion: Literal["CREAR", "ACTUALIZAR", "ELIMINAR"]
    usuario: str
    cliente_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    resultado: int

    class Settings:
        """Beanie collection metadata."""

        name = "operaciones"
        indexes = [
            [("usuario", 1), ("timestamp", -1)],
            [("cliente_id", 1)],
            [("accion", 1)],
        ]
