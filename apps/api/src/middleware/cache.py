"""
Caching middleware for ClarityForge API
"""

import hashlib
import json
import logging
from datetime import timedelta
from functools import wraps
from typing import Any, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class CacheEntry:
    def __init__(self, data: Any, ttl: int):
        from datetime import datetime, timezone
        self.data = data
        self.expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)

    def is_expired(self) -> bool:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc) > self.expires_at


class InMemoryCache:
    def __init__(self):
        self._cache: dict[str, CacheEntry] = {}

    def get(self, key: str) -> Any | None:
        entry = self._cache.get(key)
        if entry is None:
            return None
        if entry.is_expired():
            del self._cache[key]
            return None
        return entry.data

    def set(self, key: str, data: Any, ttl: int = 300) -> None:
        self._cache[key] = CacheEntry(data, ttl)

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        self._cache.clear()

    def generate_key(self, prefix: str, *args: Any, **kwargs: Any) -> str:
        key_data = {
            "args": args,
            "kwargs": kwargs,
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        hash_obj = hashlib.sha256(key_str.encode())
        return f"{prefix}:{hash_obj.hexdigest()[:16]}"


cache = InMemoryCache()


def cached(ttl: int = 300, key_prefix: str = "default"):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key = cache.generate_key(key_prefix, *args, **kwargs)
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_result

            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cache miss, stored: {cache_key}")
            return result
        return wrapper
    return decorator


class CacheMiddleware(BaseHTTPMiddleware):
    CACHEABLE_PATHS = {
        "/api/v1/health",
        "/api/v1/reasoning/biases",
    }
    CACHE_TTL = 300  # 5 minutes

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path not in self.CACHEABLE_PATHS:
            return await call_next(request)

        cache_key = f"http:{request.url.path}"
        cached_response = cache.get(cache_key)

        if cached_response:
            logger.debug(f"Serving cached response for {request.url.path}")
            return Response(
                content=cached_response["content"],
                media_type="application/json",
                headers={
                    "X-Cache": "HIT",
                    "Cache-Control": f"public, max-age={self.CACHE_TTL}",
                },
            )

        response = await call_next(request)

        if response.status_code == 200:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            cache_data = {"content": body.decode()}
            cache.set(cache_key, cache_data, self.CACHE_TTL)

            return Response(
                content=body,
                media_type="application/json",
                headers={
                    "X-Cache": "MISS",
                    "Cache-Control": f"public, max-age={self.CACHE_TTL}",
                },
            )

        return response
