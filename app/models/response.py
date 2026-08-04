"""
API response models.

Defines structured responses
returned by the API.
"""


from typing import Any, Optional

from pydantic import BaseModel



class AgentResponse(BaseModel):
    """
    Standard API response model
    for agent execution.
    """


    agent: str

    response: str

    plan: Optional[dict[str, Any]] = None

    tool_used: Optional[str] = None

    tool_result: Optional[dict[str, Any]] = None

    memory: list[dict[str, Any]] = []

