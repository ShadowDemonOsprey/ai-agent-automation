"""
Application dependencies.

Provides reusable service instances
for FastAPI dependency injection.
"""


from app.services.agent_service import AgentService


def get_agent_service():
    """
    Provide AgentService instance.

    Used by API routes through
    FastAPI dependency injection.
    """


    return AgentService()