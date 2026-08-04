from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.connection import engine


# Creates a reusable async database session factory.
# The application will use this factory whenever it needs database access.
async_session_factory = async_sessionmaker(
    # Connects sessions to the configured async database engine.
    bind=engine,

    # Uses SQLAlchemy asynchronous sessions.
    class_=AsyncSession,

    # Keeps ORM objects usable after committing changes.
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session.

    A new session is created for each request.
    The session is automatically closed after the request finishes.
    """

    # Opens a database session from the factory.
    async with async_session_factory() as session:

        # Provides the session to the API endpoint/service.
        yield session

