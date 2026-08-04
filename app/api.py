from fastapi import APIRouter
from app.agent import agent

router = APIRouter()


@router.post("/agent")
def run_agent(message: str):
    result = agent.run(message)

    return result

