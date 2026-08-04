from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application starting...")

    # Initialize resources here later:
    # database connections
    # model loading
    # tool registry

    yield

    # Shutdown
    logger.info("Application shutting down...")

    # Cleanup resources here later:
    # close database
    # release resources
