"""Repository for operation audit persistence."""

from app.domain.entities.operation import OperationEntity
from app.repositories.models.operation_document import OperationDocument


class OperationRepository:
    """Persistence access for operaciones collection."""

    async def log_operation(self, operation: OperationEntity) -> None:
        """Persist one auditable operation."""
        document = OperationDocument(
            accion=operation.accion,
            usuario=operation.usuario,
            cliente_id=operation.cliente_id,
            timestamp=operation.timestamp,
            resultado=operation.resultado,
        )
        await document.insert()
