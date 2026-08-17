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
from datetime import UTC, datetime


class JSONFormatter(logging.Formatter):
    """
    Formats log records as JSON objects.
    """


    def format(self, record: logging.LogRecord) -> str:
        """
        Convert a log record into JSON.

        Includes:
        - timestamp
        - log level
        - message
        - logger name
        - exception information
        - request id (when attached by middleware)
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

        if record.exc_info:

            log_data["exception"] = self.formatException(
                record.exc_info
            )

        return json.dumps(log_data)


# Application logger creation.
logger = logging.getLogger("ai-agent")

logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)

handler.setFormatter(JSONFormatter())

# Prevent duplicate handlers when modules are reloaded.
if not logger.handlers:

    logger.addHandler(handler)

# Prevent logs from propagating to the root logger.
logger.propagate = False