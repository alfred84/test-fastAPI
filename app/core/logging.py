"""Logging utilities and middleware helpers."""

import logging
import time
import uuid

from fastapi import Request


def configure_logging() -> None:
    """Configure root logging format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


async def request_context_middleware(request: Request, call_next):
    """Attach trace id and request timing for observability."""
    trace_id = request.headers.get("X-Trace-Id", str(uuid.uuid4()))
    request.state.trace_id = trace_id
    started_at = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    response.headers["X-Trace-Id"] = trace_id
    response.headers["X-Response-Time-Ms"] = str(elapsed_ms)
    return response
