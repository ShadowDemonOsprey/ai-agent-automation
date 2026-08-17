"""
Conversation session model.

This module defines the database model for managing
multiple AI conversations.

Each session represents an independent conversation
between a user and the AI agent.
"""


from sqlalchemy import Column, DateTime, Integer, String

from app.database.base import Base
from app.utils.time import utcnow


class ConversationSession(Base):
    """
    Database model for conversation sessions.

    Purpose:
    - Create separate conversations
    - Track session lifecycle
    - Connect future messages and memory records

    Connection to AI agent system:

    User
      |
    Session
      |
    Messages
      |
    AI Agent Memory
    """


    __tablename__ = "conversation_sessions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    session_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )


    created_at = Column(
        DateTime,
        default=utcnow
    )


    updated_at = Column(
        DateTime,
        default=utcnow,
        onupdate=utcnow
    )