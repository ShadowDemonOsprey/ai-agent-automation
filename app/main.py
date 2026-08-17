"""
Main FastAPI application.

Creates the API application,
registers routes,
handles global errors,
and adds request logging.

Registered routes:
- Agent API
- Streaming AI responses
- Conversation sessions
- Long-term memory
- Knowledge base (RAG)
- Monitoring metrics
- Web chat UI
"""


from typing import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response

from app.core.constants import API_VERSION
from app.core.lifespan import lifespan
from app.docs.api_docs import API_DESCRIPTION, TAGS_METADATA
from app.middleware import log_requests, metrics
from app.models.error import ErrorResponse
from app.routes.v1.agent import router
from app.routes.v1.knowledge import router as knowledge_router
from app.routes.v1.sessions import router as sessions_router

# Create FastAPI application.
#
# This is the main application object
# that starts the AI Agent platform.
app = FastAPI(
    lifespan=lifespan,
    title="AI Agent Automation API",
    description=API_DESCRIPTION,
    version=API_VERSION,
    openapi_tags=TAGS_METADATA,
)



# Request logging middleware.
#
# Tracks incoming requests and responses
# and collects monitoring metrics.
@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
):

    return await log_requests(
        request,
        call_next
    )



# Register agent routes.
#
# Provides:
# - POST /api/v1/agent
# - GET /api/v1/chat/stream
app.include_router(
    router
)



# Register session routes.
#
# Provides:
# - POST /api/v1/sessions
# - GET /api/v1/sessions/{session_id}
# - DELETE /api/v1/sessions/{session_id}
# - Message history
# - Long-term memory management
app.include_router(
    sessions_router
)



# Register knowledge routes (RAG).
#
# Provides:
# - POST /api/v1/knowledge/documents
# - GET /api/v1/knowledge/documents
# - DELETE /api/v1/knowledge/documents/{document_id}
# - POST /api/v1/knowledge/search
app.include_router(
    knowledge_router
)



# Global exception handler.
#
# Converts unexpected exceptions into
# consistent API error responses.
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    error_response = ErrorResponse(
        error="Agent execution failed",
        message=str(exc)
    )


    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )



@app.get("/")
def home():
    """
    Root endpoint.

    Confirms API availability.
    """

    return {
        "message": "AI Agent Automation API is running",
        "version": API_VERSION,
        "docs": "/docs",
        "ui": "/ui",
    }



@app.get("/health")
def health_check():
    """
    Health endpoint.

    Used for service monitoring.
    """

    return {
        "status": "healthy",
        "agent": "Business Automation Agent"
    }



@app.get("/metrics")
def metrics_endpoint():
    """
    Monitoring metrics.

    Returns request counters and latency
    collected by the logging middleware.
    """

    return metrics.snapshot()



# Serve the static web chat UI.
app.mount(
    "/ui",
    StaticFiles(
        directory="app/static",
        html=True,
    ),
    name="ui",
)
