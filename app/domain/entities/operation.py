"""Domain model for auditable write operation."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(slots=True)
class OperationEntity:
    """Represents a CREATE/UPDATE/DELETE operation."""

    accion: Literal["CREAR", "ACTUALIZAR", "ELIMINAR"]
    usuario: str
    cliente_id: str
    timestamp: datetime
    resultado: int
