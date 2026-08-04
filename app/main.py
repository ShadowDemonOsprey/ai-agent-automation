"""
Main FastAPI application.

Creates the API application,
registers routes,
handles global errors,
and adds request logging.
"""


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from app.routes.v1.agent import router
from app.middleware import log_requests
from app.models.error import ErrorResponse
from app.docs.api_docs import API_DESCRIPTION, TAGS_METADATA
from app.core.lifespan import lifespan

# Create FastAPI application.
app = FastAPI(
    lifespan=lifespan,
    title="AI Agent Automation API",
    description=API_DESCRIPTION,
    version="1.0.0",
    openapi_tags=TAGS_METADATA
)

# Register request logging middleware.
@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next
):

    return await log_requests(
        request,
        call_next
    )



# Register API routes.
app.include_router(
    router
)



# Global exception handler.
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    """
    Convert unexpected exceptions
    into structured API responses.
    """


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
    """

    return {
        "message": "AI Agent Automation API is running"
    }



@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "agent": "Business Automation Agent"
    }