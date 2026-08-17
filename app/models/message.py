"""
Conversation message model.

Stores individual messages belonging to a session.

This is the persistent layer behind the agent's
conversation memory (Phase 4.3).

Session
   |
Messages (this model)
   |
Conversation memory used by the AI agent
"""


from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database.base import Base
from app.utils.time import utcnow


class Message(Base):
    """
    A single conversation message.
    """

    __tablename__ = "messages"


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


    role = Column(
        String,
        nullable=False
    )


    content = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=utcnow,
        nullable=False
    )
