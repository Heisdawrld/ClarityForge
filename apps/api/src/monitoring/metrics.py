"""
Metrics Collection for ClarityForge API

Implements Prometheus-compatible metrics for observability.
"""

import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


@dataclass
class MetricValue:
    name: str
    value: float
    labels: dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class MetricsCollector:
    def __init__(self):
        self._counters: dict[str, float] = defaultdict(float)
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = defaultdict(list)
        self._histogram_buckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]

    def counter(self, name: str, value: float = 1, labels: dict[str, str] | None = None) -> None:
        key = self._make_key(name, labels)
        self._counters[key] += value

    def gauge(self, name: str, value: float, labels: dict[str, str] | None = None) -> None:
        key = self._make_key(name, labels)
        self._gauges[key] = value

    def histogram(self, name: str, value: float, labels: dict[str, str] | None = None) -> None:
        key = self._make_key(name, labels)
        self._histograms[key].append(value)
        if len(self._histograms[key]) > 10000:
            self._histograms[key] = self._histograms[key][-5000:]

    def _make_key(self, name: str, labels: dict[str, str] | None) -> str:
        if not labels:
            return name
        label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def get_prometheus_format(self) -> str:
        lines = []

        lines.append("# HELP api_requests_total Total number of API requests")
        lines.append("# TYPE api_requests_total counter")
        for key, value in self._counters.items():
            if "requests" in key:
                lines.append(f"{key} {value}")

        lines.append("")
        lines.append("# HELP api_request_duration_seconds Request duration in seconds")
        lines.append("# TYPE api_request_duration_seconds histogram")
        for key, values in self._histograms.items():
            if "duration" in key:
                lines.append(f"{key}_sum {sum(values)}")
                lines.append(f"{key}_count {len(values)}")
                for bucket in self._histogram_buckets:
                    bucket_count = len([v for v in values if v <= bucket])
                    bucket_key = f"{key}_bucket{{le=\"{bucket}\"}}"
                    lines.append(f"{bucket_key} {bucket_count}")
                lines.append(f"{key}_bucket{{le=\"+Inf\"}} {len(values)}")

        lines.append("")
        lines.append("# HELP api_in_flight Current number of requests being processed")
        lines.append("# TYPE api_in_flight gauge")
        for key, value in self._gauges.items():
            if "in_flight" in key:
                lines.append(f"{key} {value}")

        return "\n".join(lines)

    def get_summary(self) -> dict:
        return {
            "total_requests": sum(v for k, v in self._counters.items() if "requests" in k),
            "total_errors": sum(v for k, v in self._counters.items() if "error" in k),
            "avg_duration_ms": self._calculate_avg_duration(),
            "requests_by_endpoint": self._get_requests_by_endpoint(),
        }

    def _calculate_avg_duration(self) -> float:
        all_durations = []
        for key, values in self._histograms.items():
            if "duration" in key:
                all_durations.extend(values)
        return sum(all_durations) / len(all_durations) if all_durations else 0

    def _get_requests_by_endpoint(self) -> dict[str, int]:
        result = defaultdict(int)
        for key in self._counters.keys():
            if "requests" in key:
                parts = key.split("{")
                if len(parts) > 1:
                    endpoint = parts[0]
                    result[endpoint] += self._counters[key]
        return dict(result)


metrics = MetricsCollector()


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()
        metrics.gauge("api_in_flight", 1)

        try:
            response = await call_next(request)
            status_code = str(response.status_code)
        except Exception:
            status_code = "500"
            raise
        finally:
            metrics.gauge("api_in_flight", 0)
            duration = time.perf_counter() - start_time

            labels = {
                "method": request.method,
                "endpoint": self._normalize_path(request.url.path),
                "status": status_code,
            }

            metrics.counter("api_requests_total", 1, labels)
            metrics.histogram("api_request_duration_seconds", duration, labels)

            if status_code.startswith("5"):
                metrics.counter("api_errors_total", 1, labels)

        return response

    def _normalize_path(self, path: str) -> str:
        path = path.split("/api/v1/")[-1] if "/api/v1/" in path else path
        return path.split("/")[0] if path else "root"


class MetricsEndpoint:
    @staticmethod
    async def get_metrics() -> Response:
        from fastapi import Response
        return Response(
            content=metrics.get_prometheus_format(),
            media_type="text/plain",
        )

    @staticmethod
    async def get_summary() -> dict:
        return metrics.get_summary()
