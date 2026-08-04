from fastapi import APIRouter

from app.models.request import AgentRequest
from app.services.agent_service import agent_service



router = APIRouter(
    prefix="/api/v1",
    tags=["Agent"]
)



@router.post("/agent")
def run_agent(
    request: AgentRequest
):

    result = agent_service.run(
        request.message
    )

    return result