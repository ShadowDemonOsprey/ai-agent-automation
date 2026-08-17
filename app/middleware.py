"""
API request logging middleware.

Tracks:
- HTTP method
- Request path
- Response status code
- Processing time
- Request ID

Also collects lightweight monitoring metrics
exposed at GET /metrics.
"""


import re
import time
import uuid
from collections import defaultdict
from typing import Awaitable, Callable

from fastapi import Request
from starlette.responses import Response

from app.logger import logger


class MetricsCollector:
    """
    In-memory request metrics.
    """


    def __init__(self):
        """
        Initialize metric counters.
        """

        self.total_requests = 0

        self.total_errors = 0

        self.total_latency = 0.0

        self.by_method = defaultdict(int)

        self.by_path = defaultdict(int)

        self.by_status = defaultdict(int)



    def record(
        self,
        method: str,
        path: str,
        status_code: int,
        latency: float
    ) -> None:
        """
        Record one completed request.
        """

        self.total_requests += 1

        self.total_latency += latency

        self.by_method[method] += 1

        normalized = self._normalize_path(path)
        self.by_path[normalized] += 1

        self.by_status[status_code] += 1

        if status_code >= 500:

            self.total_errors += 1


    @staticmethod
    def _normalize_path(path: str) -> str:
        """
        Replace dynamic path segments with placeholders
        to prevent unbounded cardinality.
        """

        path = re.sub(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}"
            r"-[0-9a-f]{4}-[0-9a-f]{12}",
            "{id}",
            path,
            flags=re.IGNORECASE,
        )

        path = re.sub(r"/\d+", "/{n}", path)

        return path



    def snapshot(self) -> dict:
        """
        Return a metrics dictionary.
        """

        average_latency = (
            self.total_latency / self.total_requests
            if self.total_requests else 0.0
        )

        return {
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "error_rate": round(
                self.total_errors / self.total_requests,
                4
            ) if self.total_requests else 0.0,
            "average_latency_ms": round(
                average_latency * 1000,
                2
            ),
            "by_method": dict(self.by_method),
            "by_path": dict(self.by_path),
            "by_status": {
                str(code): count
                for code, count in self.by_status.items()
            },
        }



metrics = MetricsCollector()



async def log_requests(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
):
    """
    Log every incoming API request.

    Creates a unique request ID and attaches
    it to all related log messages.

    Args:
        request (Request):
            Incoming HTTP request.

        call_next:
            Next middleware or route handler.

    Returns:
        Response:
            API response.
    """

    request_id = str(uuid.uuid4())

    start_time = time.time()

    logger.info(
        "Incoming request",
        extra={
            "request_id": request_id
        }
    )

    response = await call_next(
        request
    )

    process_time = (
        time.time()
        - start_time
    )

    logger.info(
        "Completed request",
        extra={
            "request_id": request_id
        }
    )

    # Record monitoring metrics.
    metrics.record(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        latency=process_time,
    )

    # Return request ID in response headers.
    response.headers["X-Request-ID"] = request_id

    return response