"""
Application logging module.

Provides centralized logging
for the AI agent system.

Logs:
- Agent actions
- Tool execution
- Errors
- Debug information
"""


import logging



# Create application logger.
logger = logging.getLogger(
    "ai-agent"
)


# Set logging level.
logger.setLevel(
    logging.INFO
)



# Create console output handler.
handler = logging.StreamHandler()


# Define log message format.
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)


handler.setFormatter(
    formatter
)


# Add handler only once.
if not logger.handlers:

    logger.addHandler(
        handler
    )