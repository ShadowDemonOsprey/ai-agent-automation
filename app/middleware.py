"""
API request logging middleware.

Tracks:
- HTTP method
- Request path
- Response status code
- Processing time
"""


import time

from fastapi import Request

from app.logger import logger



async def log_requests(
    request: Request,
    call_next
):
    """
    Log every incoming API request.

    Args:
        request (Request):
            Incoming HTTP request.

        call_next:
            Next middleware or route handler.

    Returns:
        Response:
            API response.
    """


    start_time = time.time()


    logger.info(
        f"Incoming request: "
        f"{request.method} {request.url.path}"
    )


    response = await call_next(
        request
    )


    process_time = (
        time.time()
        - start_time
    )


    logger.info(
        f"Completed request: "
        f"{request.method} {request.url.path} "
        f"Status={response.status_code} "
        f"Time={process_time:.4f}s"
    )


    return response