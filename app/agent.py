"""
AI Agent core module.

This module controls the AI agent workflow.

Current flow:

User input
    ↓
Agent memory
    ↓
Prompt with conversation history
    ↓
Ollama LLM
    ↓
AI response
    ↓
Store response in memory


Future upgrades:
- Add RAG retrieval
- Add external tools
- Add planning
"""


from app.core.constants import AGENT_NAME
from app.llm.ollama_client import ollama_client
from app.memory import memory



class AIAgent:
    """
    Main AI agent class.

    Handles:
    - User requests
    - Conversation history
    - LLM communication
    """


    def __init__(self):
        """
        Initialize the agent.

        Stores the agent name.
        """

        self.name = AGENT_NAME



    def run(self, user_input: str):
        """
        Process a user request.

        Args:
            user_input (str):
                The user's message.

        Returns:
            dict:
                Agent response with memory context.
        """


        # Save the user's message first.
        memory.add_message(
            "user",
            user_input
        )


        # Retrieve previous conversation.
        history = memory.get_history()


        # Convert conversation history into text.
        # This gives the LLM context.
        conversation = "\n".join(
            [
                f"{message['role']}: {message['content']}"
                for message in history
            ]
        )


        prompt = f"""
            You are an AI business automation assistant.

            Conversation history:
            {conversation}

            Answer the user's latest request clearly.
        """


        # Ask Ollama to generate a response.
        response = ollama_client.generate(prompt)


        # Save AI response into memory.
        memory.add_message(
            "assistant",
            response
        )


        return {
            "agent": self.name,
            "input": user_input,
            "response": response,
            "memory": memory.get_history()
        }



# Create one shared agent instance.
agent = AIAgent()
