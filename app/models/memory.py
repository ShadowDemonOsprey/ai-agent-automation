"""
Long-term memory model.

Stores key-value facts per session so the agent
can remember user preferences across conversations.

This is the persistent memory system (Phase 4.3).
"""


from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database.base import Base
from app.utils.time import utcnow


class MemoryRecord(Base):
    """
    A persistent fact associated with a session.
    """

    __tablename__ = "memory_records"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    session_id = Column(
        String,
        nullable=False,
        index=True
    )


    key = Column(
        String,
        nullable=False
    )


    value = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=utcnow,
        nullable=False
    )


    updated_at = Column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False
    )
