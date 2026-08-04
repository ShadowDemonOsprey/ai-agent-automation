from fastapi import APIRouter, Depends

from app.models.request import AgentRequest
from app.services.agent_service import AgentService
from app.dependencies.services import get_agent_service



router = APIRouter(
    prefix="/api/v1",
    tags=["Agent"]
)



@router.post("/agent")
def run_agent(
    request: AgentRequest,
    service: AgentService = Depends(get_agent_service)
):

    result = service.run(
        request.message
    )

    return result