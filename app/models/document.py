"""
RAG document model.

Stores metadata for documents ingested into the
knowledge base (Phase 4.4). The actual text lives
in the vector store as searchable chunks.
"""


from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database.base import Base
from app.utils.time import utcnow


class Document(Base):
    """
    Metadata for an ingested knowledge document.
    """

    __tablename__ = "documents"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    document_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )


    filename = Column(
        String,
        default="untitled"
    )


    title = Column(
        String,
        default=""
    )


    source = Column(
        String,
        default="text"
    )


    chunk_count = Column(
        Integer,
        default=0
    )


    content = Column(
        Text,
        default=""
    )


    created_at = Column(
        DateTime,
        default=utcnow,
        nullable=False
    )
