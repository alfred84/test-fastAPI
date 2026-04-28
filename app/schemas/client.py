"""Client API schemas aligned with React wire DTOs (test-react infrastructure DTOs)."""

from typing import Literal

from pydantic import BaseModel, Field


class ClientListRequest(BaseModel):
    """Body for POST /api/Cliente/Listado."""

    identificacion: str
    nombre: str = ""
    usuarioId: str = Field(min_length=1)


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
