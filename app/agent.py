"""
AI Agent core module.

This module controls the reasoning workflow of the agent.

Current flow:
User input
    ↓
AI Agent
    ↓
Ollama local LLM
    ↓
Generated response

Future upgrades:
- Add tools
- Add RAG retrieval
- Add memory
- Add planning
"""


from app.core.constants import AGENT_NAME
from app.llm.ollama_client import ollama_client


class AIAgent:
    """
    Main AI agent class.

    The agent is responsible for receiving tasks
    and generating responses using an LLM.
    """


    def __init__(self):
        """
        Initialize the agent.

        Stores the agent name and prepares
        the connection to the LLM.
        """

        self.name = AGENT_NAME


    def run(self, user_input: str):
        """
        Process a user request.

        Args:
            user_input (str):
                The user's question or task.

        Returns:
            dict:
                Structured response from the AI agent.
        """


        # Create a simple prompt.
        # Later this will include:
        # - memory
        # - retrieved documents
        # - available tools
        prompt = f"""
            You are an AI business automation assistant.

            User request:
            {user_input}

            Provide a helpful response.
            """


        # Send the prompt to the local Ollama model.
        response = ollama_client.generate(prompt)


        # Return structured data for the API.
        return {
            "agent": self.name,
            "input": user_input,
            "response": response
        }


# Create one reusable agent instance.
agent = AIAgent()

