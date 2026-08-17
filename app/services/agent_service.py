"""
Agent service layer.

Separates API routes from
AI agent business logic.
"""


from app.agent import agent
from app.models.agent_state import AgentState


class AgentService:
    """
    Service responsible for
    executing agent operations.
    """


    def run(
        self,
        message: str,
        session_id: str | None = None
    ) -> AgentState:
        """
        Execute the AI agent.

        Args:
            message:
                User input.
            session_id:
                Optional conversation session for
                persistent memory.

        Returns:
            Agent response.
        """

        return agent.run(
            message,
            session_id=session_id
        )



agent_service = AgentService()
