"""
API routes for the AI agent.

This module exposes HTTP endpoints
that allow users to communicate
with the AI agent.
"""


from fastapi import APIRouter

from app.agent import agent
from app.models.agent_state import AgentState
from app.models.request import AgentRequest



# Create API router.
router = APIRouter()



@router.post(
    "/agent",
    response_model=AgentState
)
def run_agent(
    request: AgentRequest
):
    """
    Run the AI agent.

    Args:
        request (AgentRequest):
            Validated user request.

    Returns:
        AgentState:
            Structured AI agent response.
    """


    # Send user message to agent.
    result = agent.run(
        request.message
    )


    # FastAPI converts this Pydantic
    # model into JSON automatically.
    return result

