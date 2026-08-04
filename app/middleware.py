"""
API request logging middleware.

Tracks:
- HTTP method
- Request path
- Response status code
- Processing time
- Request ID
"""


# ============================================================
# ADDED:
# uuid generates unique request identifiers.
# ============================================================

import time
import uuid


from fastapi import Request


from app.logger import logger



async def log_requests(
    request: Request,
    call_next
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



    # ========================================================
    # ADDED:
    # Generate unique ID for this request.
    #
    # Example:
    # 8f3c2b7e-....
    #
    # This allows tracing one request
    # through multiple services later.
    # ========================================================

    request_id = str(
        uuid.uuid4()
    )



    start_time = time.time()



    # ========================================================
    # ADDED:
    # Attach request_id to logger record.
    #
    # logger.py reads this value:
    # record.request_id
    # ========================================================

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



    # ========================================================
    # CHANGED:
    # Structured logging instead of string formatting.
    # ========================================================

    logger.info(
        "Completed request",
        extra={
            "request_id": request_id
        }
    )



    # ========================================================
    # ADDED:
    # Return request ID in response headers.
    #
    # Useful for:
    # - debugging
    # - tracing errors
    # - production monitoring
    # ========================================================

    response.headers["X-Request-ID"] = request_id



    return response