# Database ORM foundation.
# Used by all SQLAlchemy models.
from app.database.base import Base

# Async database engine lifecycle management.
# init_database creates tables on startup.
# close_database releases database resources.
from app.database.connection import (
    async_engine,
    close_database,
    init_database,
    sync_engine,
)

# FastAPI database dependency.
# Provides an AsyncSession to API routes/services.
from app.database.session import (
    async_session_factory,
    get_session,
    get_sync_session,
    sync_session_factory,
)

# Public exports for the database package.
# Other parts of the application can import from:
# "app.database"
# instead of importing individual files.
__all__ = [
    "Base",
    "async_engine",
    "sync_engine",
    "init_database",
    "close_database",
    "async_session_factory",
    "sync_session_factory",
    "get_sync_session",
    "get_session",
]
