"""
Agent service layer.

Separates API routes from
AI agent business logic.
"""


from app.agent import agent



class AgentService:
    """
    Service responsible for
    executing agent operations.
    """


    def run(
        self,
        message: str
    ):
        """
        Execute the AI agent.

        Args:
            message:
                User input.

        Returns:
            Agent response.
        """


        return agent.run(
            message
        )



agent_service = AgentService()

