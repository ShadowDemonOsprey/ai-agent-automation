"""
Database session management.

Provides:
- Async SQLAlchemy session factory
- Sync SQLAlchemy session factory
- FastAPI database dependency

Flow:

FastAPI Request
      |
      v
get_session()
      |
      v
AsyncSession
      |
      v
Database Operations
"""


from collections.abc import AsyncGenerator
from contextlib import contextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import Session, sessionmaker

from app.database.connection import async_engine, sync_engine

# Creates reusable async database sessions.
#
# Every API request that needs database access
# receives a separate AsyncSession instance.
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Creates reusable sync database sessions.
#
# Used by the AI agent and its tools, which run
# synchronously outside the FastAPI request cycle.
sync_session_factory = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
)


@contextmanager
def get_sync_session():
    """
    Synchronous database session context manager.

    Used by repositories that run outside
    the FastAPI async request cycle.
    """

    session = sync_session_factory()

    try:

        yield session

    finally:

        session.close()



async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency.

    Creates a database session,
    provides it to API endpoints,
    and closes it automatically.
    """

    async with async_session_factory() as session:

        yield session
