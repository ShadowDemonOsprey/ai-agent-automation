# Database ORM foundation.
# Used by all SQLAlchemy models.
from app.database.base import Base


# Async database engine lifecycle management.
# init_database starts database resources.
# close_database releases database resources.
from app.database.connection import (
    engine,
    init_database,
    close_database,
)


# FastAPI database dependency.
# Provides an AsyncSession to API routes/services.
from app.database.session import (
    async_session_factory,
    get_session,
)


# Public exports for the database package.
# Other parts of the application can import from:
# "app.database"
# instead of importing individual files.
__all__ = [
    "Base",
    "engine",
    "init_database",
    "close_database",
    "async_session_factory",
    "get_session",
]
