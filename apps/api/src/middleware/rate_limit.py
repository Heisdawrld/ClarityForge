"""
Rate Limiting Middleware for ClarityForge API
"""

import logging
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RateLimitExceeded(Exception):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")


class RateLimiter:
    def __init__(self):
        self._requests: dict[str, list[datetime]] = defaultdict(list)
        self._window_seconds = 60
        self._max_requests = 60

    def check_rate_limit(self, client_id: str) -> tuple[bool, int]:
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(seconds=self._window_seconds)

        requests = self._requests[client_id]
        recent_requests = [req for req in requests if req > window_start]
        self._requests[client_id] = recent_requests

        if len(recent_requests) >= self._max_requests:
            oldest_in_window = min(recent_requests)
            retry_after = int((oldest_in_window + timedelta(seconds=self._window_seconds) - now).total_seconds())
            return False, max(1, retry_after)

        self._requests[client_id].append(now)
        return True, 0

    def get_remaining(self, client_id: str) -> int:
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(seconds=self._window_seconds)
        recent_count = len([r for r in self._requests.get(client_id, []) if r > window_start])
        return max(0, self._max_requests - recent_count)


rate_limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    EXEMPT_PATHS = {
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
    }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if any(request.url.path.startswith(path) for path in self.EXEMPT_PATHS):
            return await call_next(request)

        client_id = self._get_client_id(request)
        allowed, retry_after = rate_limiter.check_rate_limit(client_id)

        if not allowed:
            logger.warning(
                "rate_limit_exceeded",
                extra={
                    "client_id": client_id,
                    "path": request.url.path,
                    "retry_after": retry_after,
                },
            )
            return Response(
                content='{"error": "Rate limit exceeded"}',
                status_code=429,
                media_type="application/json",
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(rate_limiter._max_requests),
                    "X-RateLimit-Remaining": str(rate_limiter.get_remaining(client_id)),
                    "X-RateLimit-Reset": str(int(time.time()) + retry_after),
                },
            )

        response = await call_next(request)

        remaining = rate_limiter.get_remaining(client_id)
        response.headers["X-RateLimit-Limit"] = str(rate_limiter._max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

    def _get_client_id(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        if request.client:
            return f"{request.client.host}:{request.client.port}"

        return "unknown"
