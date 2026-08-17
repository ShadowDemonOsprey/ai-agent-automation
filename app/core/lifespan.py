"""
Application lifecycle management.

Runs startup and shutdown tasks:
- Creates database tables
- Initializes the RAG vector store
- Cleans up resources on shutdown
"""


from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.connection import (
    close_database,
    init_database,
)
from app.logger import logger
from app.models.document import Document  # noqa: F401
from app.models.memory import MemoryRecord  # noqa: F401
from app.models.message import Message  # noqa: F401

# Import models so all tables are registered on the
# SQLAlchemy metadata before create_all runs.
from app.models.session import ConversationSession  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application starting...")

    await init_database()

    logger.info("Database tables ready")

    yield

    # Shutdown
    logger.info("Application shutting down...")

    await close_database()
