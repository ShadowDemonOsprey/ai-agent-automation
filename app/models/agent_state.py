"""
Agent state models.

This module defines structured data
used by the AI agent.

Using Pydantic models gives:
- Validation
- Type safety
- Better API documentation
"""


from typing import Optional, List, Dict
from pydantic import BaseModel



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


    plan: Optional[Dict] = None
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


    tool_result: Optional[Dict] = None
    """
    Result returned by a tool.
    """


    memory: List[Dict]
    """
    Conversation history.
    """