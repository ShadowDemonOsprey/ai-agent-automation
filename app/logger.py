"""
Application logging module.

Provides centralized structured logging
for the AI Agent Automation Platform.

Features:
- JSON formatted logs
- timestamps
- log levels
- request ID support
- exception tracking
"""


import json
import logging
import sys
from datetime import datetime, UTC


# ============================================================
# ADDED:
# JSON formatter.
#
# Converts normal log records into JSON format
# for production log systems.
#
# Example output:
# {
#   "timestamp": "...",
#   "level": "INFO",
#   "message": "Agent started"
# }
# ============================================================

class JSONFormatter(logging.Formatter):
    """
    Formats log records as JSON objects.
    """


    def format(self, record):
        """
        Convert a log record into JSON.

        Includes:
        - timestamp
        - log level
        - message
        - logger name
        - exception information
        """

        log_data = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(
                record,
                "request_id",
                None
            ),
        }
        
        # ====================================================
        # ADDED:
        # Exception tracking.
        #
        # Adds traceback information
        # when logger.exception() is used.
        # ====================================================

        if record.exc_info:
            log_data["exception"] = self.formatException(
                record.exc_info
            )

        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        return json.dumps(log_data)



# ============================================================
# Application logger creation.
# ============================================================

logger = logging.getLogger(
    "ai-agent"
)



# ============================================================
# Logging level.
#
# INFO:
# Normal application events.
#
# ============================================================

logger.setLevel(
    logging.INFO
)



# ============================================================
# ADDED:
# JSON console handler.
#
# Production systems usually send
# stdout logs to:
# - Docker
# - Kubernetes
# - Cloud logging systems
# ============================================================

handler = logging.StreamHandler(
    sys.stdout
)


handler.setFormatter(
    JSONFormatter()
)



# ============================================================
# Prevent duplicate handlers.
# ============================================================

if not logger.handlers:

    logger.addHandler(
        handler
    )



# ============================================================
# ADDED:
# Prevent logs from propagating
# to the root logger.
# ============================================================

logger.propagate = False