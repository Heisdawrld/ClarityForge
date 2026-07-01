import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request.state.correlation_id = request_id

        start_time = time.perf_counter()

        logger.info(
            "request_started",
            extra={
                "correlation_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_host": request.client.host if request.client else None,
            },
        )

        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time

            logger.info(
                "request_completed",
                extra={
                    "correlation_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time_ms": round(process_time * 1000, 2),
                },
            )

            response.headers["X-Correlation-ID"] = request_id
            response.headers["X-Process-Time-Ms"] = str(round(process_time * 1000, 2))

            return response

        except Exception as exc:
            process_time = time.perf_counter() - start_time

            logger.error(
                "request_failed",
                extra={
                    "correlation_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(exc),
                    "process_time_ms": round(process_time * 1000, 2),
                },
            )
            raise
