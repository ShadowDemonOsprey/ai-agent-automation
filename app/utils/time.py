"""
Time utilities.

Provides timezone-aware UTC helpers used across
the application for database timestamps.
"""


from datetime import datetime, timezone


def utcnow() -> datetime:
    """
    Return the current UTC time.

    Returns a naive datetime object (no timezone info)
    so it stores cleanly in SQLite while always
    representing UTC.

    This replaces the deprecated datetime.utcnow().
    """

    return (
        datetime.now(timezone.utc)
        .replace(tzinfo=None)
    )


def isoformat() -> str:
    """
    Return the current UTC time as an ISO 8601 string.
    """

    return (
        datetime.now(timezone.utc)
        .isoformat()
    )
