"""Client API schemas aligned with React wire DTOs (test-react infrastructure DTOs)."""

from typing import Literal

from pydantic import BaseModel, Field


class ClientListRequest(BaseModel):
    """Body for POST /api/Cliente/Listado."""

    identificacion: str | None = None
    nombre: str | None = None
    usuarioId: str = Field(min_length=1)

    def to_upstream_payload(self) -> dict[str, str | None]:
        """Build explicit upstream payload preserving null/empty-string semantics."""
        nombre = self.nombre
        identificacion = self.identificacion
        if nombre is None and identificacion is None:
            identificacion = ""
        return {
            "nombre": nombre,
            "identificacion": identificacion,
            "usuarioId": self.usuarioId,
        }


class ClientCreateRequest(BaseModel):
    """Body for POST /api/Cliente/Crear."""

    nombre: str
    apellidos: str
    identificacion: str
    celular: str
    otroTelefono: str
    direccion: str
    fNacimiento: str
    fAfiliacion: str
    sexo: Literal["F", "M"]
    resennaPersonal: str
    imagen: str
    interesFK: str
    usuarioId: str


class ClientUpdateRequest(BaseModel):
    """Body for POST /api/Cliente/Actualizar."""

    id: str = Field(min_length=1)
    nombre: str
    apellidos: str
    identificacion: str
    celular: str
    otroTelefono: str
    direccion: str
    fNacimiento: str
    fAfiliacion: str
    sexo: Literal["F", "M"]
    resennaPersonal: str
    imagen: str
    interesFK: str
    usuarioId: str
