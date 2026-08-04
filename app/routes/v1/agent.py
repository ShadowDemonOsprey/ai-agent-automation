"""
Agent API routes.

Provides:
- Normal agent execution endpoint
- Streaming AI response endpoint using SSE

Flow:

Client
  ↓
FastAPI Route
  ↓
Agent Service
  ↓
AI Agent
  ↓
Ollama LLM
"""


from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.models.request import AgentRequest
from app.models.response import AgentResponse
from app.services.agent_service import AgentService
from app.dependencies.services import get_agent_service
from app.agent import agent
from app.logger import logger



router = APIRouter(
    prefix="/api/v1",
    tags=["Agent"]
)



@router.post(
    "/agent",
    response_model=AgentResponse
)
def run_agent(
    request: AgentRequest,
    service: AgentService = Depends(get_agent_service)
):
    """
    Execute normal non-streaming agent request.
    """

    result = service.run(
        request.message
    )

    return result



@router.get(
    "/chat/stream"
)
def stream_chat(
    message: str
):
    """
    Stream AI responses using Server Sent Events.

    Example:

    GET /api/v1/chat/stream?message=hello


    Response:

    data: Hello

    data: how

    data: can

    data: I help?
    """


    def event_generator():
        """
        Convert agent text chunks into SSE format.
        """

        try:

            for chunk in agent.stream_run(message):

                yield (
                    f"data: {chunk}\n\n"
                )


        except Exception as error:

            logger.error(
                f"Streaming API error: {error}"
            )

            yield (
                f"data: [ERROR] {str(error)}\n\n"
            )



    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )