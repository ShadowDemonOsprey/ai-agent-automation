"""
API request models.

Defines the structure of data
received by FastAPI endpoints.
"""


from typing import Optional

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """
    Request model for AI agent input.
    """

    message: str = Field(
        ..., min_length=1,
        description="Non-empty user message.",
        examples=["What is 6 times 7?"],
    )
    """
    User message sent to the AI agent.
    """

    session_id: Optional[str] = None
    """
    Optional conversation session.

    When provided, the agent loads and persists
    conversation history for that session.
    """



class MemoryRequest(BaseModel):
    """
    Request model for storing a long-term memory fact.
    """

    key: str
    """
    Memory key. Example: "user_name".
    """

    value: str
    """
    Memory value. Example: "Alex".
    """



class KnowledgeDocumentRequest(BaseModel):
    """
    Request model for ingesting a knowledge document.
    """

    filename: str = "untitled"
    """
    Name of the source file.
    """

    title: str = ""
    """
    Human readable document title.
    """

    content: str
    """
    Document text to index.
    """



class KnowledgeSearchRequest(BaseModel):
    """
    Request model for querying the knowledge base.
    """

    query: str
    """
    Search query.
    """

    top_k: int = 3
    """
    Number of results to return.
    """
