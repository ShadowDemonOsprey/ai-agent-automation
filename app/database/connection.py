from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings


engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)


async def init_database() -> None:
    """
    Initialize database resources.
    """
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)


async def close_database() -> None:
    """
    Close database resources.
    """
    await engine.dispose()