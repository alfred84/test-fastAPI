"""Unit tests for client schemas."""

from app.schemas.client import ClientListRequest


def test_client_list_default_mode_sets_empty_identificacion():
    """When no filters are provided, upstream must receive identificacion as empty string."""
    payload = ClientListRequest.model_validate({"usuarioId": "u1"})

    assert payload.to_upstream_payload() == {"nombre": None, "identificacion": "", "usuarioId": "u1"}


def test_client_list_identificacion_filter_is_preserved():
    """Identification search must send nombre null and provided identificacion."""
    payload = ClientListRequest.model_validate(
        {"identificacion": "84081921688", "nombre": None, "usuarioId": "u1"}
    )

    assert payload.to_upstream_payload() == {
        "nombre": None,
        "identificacion": "84081921688",
        "usuarioId": "u1",
    }


def test_client_list_name_filter_keeps_identificacion_null():
    """Name search must keep identificacion as null when explicitly null."""
    payload = ClientListRequest.model_validate({"identificacion": None, "nombre": "alfredo", "usuarioId": "u1"})

    assert payload.to_upstream_payload() == {"nombre": "alfredo", "identificacion": None, "usuarioId": "u1"}
