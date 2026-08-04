"""
API request models.

Defines the structure of data
received by FastAPI endpoints.
"""


from pydantic import BaseModel



class AgentRequest(BaseModel):
    """
    Request model for AI agent input.
    """


    message: str
    """
    User message sent to the AI agent.
    """