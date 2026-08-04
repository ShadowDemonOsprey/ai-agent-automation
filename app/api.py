"""
API routes for the AI agent.

This module exposes HTTP endpoints
that allow users to interact with the agent.
"""


from fastapi import APIRouter
from app.agent import agent
from app.models.agent_state import AgentState



# Create API router.
# The main application imports this router.
router = APIRouter()



@router.post(
    "/agent",
    response_model=AgentState
)
def run_agent(message: str):
    """
    Run the AI agent.

    Args:
        message (str):
            User input message.

    Returns:
        AgentState:
            Structured AI agent response.
    """


    # Execute agent workflow.
    result = agent.run(
        message
    )


    # Return Pydantic model.
    # FastAPI converts it automatically to JSON.
    return result
