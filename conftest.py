"""
Shared pytest configuration.

Sets up a dedicated test database before any
application module is imported, and initializes
the database tables once for the whole session.

Also ensures tests never require a live Ollama server
by enabling the offline fallback model.
"""


import os

# Must be set before any application import so the
# settings singleton picks up the test configuration.
os.environ.setdefault(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./test_ai_agent.db",
)

os.environ.setdefault(
    "VECTOR_STORE_PATH",
    "data/test_chroma",
)

os.environ.setdefault(
    "ENABLE_OFFLINE_FALLBACK",
    "true",
)


import asyncio  # noqa: E402

import pytest  # noqa: E402

from app.database.connection import (  # noqa: E402
    close_database,
    init_database,
)


@pytest.fixture(scope="session", autouse=True)
def database_setup():
    """
    Create database tables once for the test session.
    """

    asyncio.run(init_database())

    yield

    asyncio.run(close_database())
