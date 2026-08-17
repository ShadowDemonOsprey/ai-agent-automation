"""
Agent state models.

This module defines structured data
used by the AI agent.

Using Pydantic models gives:
- Validation
- Type safety
- Better API documentation
"""


from typing import Any, Optional

from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    Represents the current state of an agent execution.
    """


    agent: str
    """
    Name of the AI agent.
    """


    response: str
    """
    Generated response from tool or LLM.
    """


    plan: Optional[dict[str, Any]] = None
    """
    Planner decision.

    Example:
    {
        "action": "tool",
        "tool": "calculator"
    }
    """


    tool_used: Optional[str] = None
    """
    Name of executed tool.
    """


    tool_result: Optional[dict[str, Any]] = None
    """
    Result returned by a tool.
    """


    memory: list[dict[str, Any]] = Field(
        default_factory=list
    )
    """
    Conversation history.
    """


    session_id: Optional[str] = None
    """
    Conversation session associated with this execution.
    """