"""
Database engine management.

Creates both:
- an async engine used by FastAPI routes
- a sync engine used by agent tools and repositories

Both engines point to the same SQLite database.
"""


from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings
from app.database.base import Base

async_engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)


# Sync engine for SQLite.
# Convert "sqlite+aiosqlite://" to "sqlite://"
sync_engine: Engine = create_engine(
    settings.DATABASE_URL.replace("+aiosqlite", ""),
    echo=settings.DEBUG,
)



async def init_database() -> None:
    """
    Initialize database resources.

    Creates all tables on application startup.
    """

    Base.metadata.create_all(
        bind=sync_engine
    )



async def close_database() -> None:
    """
    Close database resources.
    """

    await async_engine.dispose()

    sync_engine.dispose()
