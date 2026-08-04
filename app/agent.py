"""
AI Agent core module.

The agent workflow:

User request
    ↓
Memory
    ↓
Tool decision
    ↓
Ollama LLM
    ↓
Response
    ↓
Memory update


Current tool:
- Calculator

Future tools:
- RAG search
- File analysis
- Database access
"""


from app.core.constants import AGENT_NAME
from app.llm.ollama_client import ollama_client
from app.memory import memory
from app.tools import TOOLS



class AIAgent:
    """
    Main AI agent class.

    Responsible for:
    - Understanding user requests
    - Calling tools
    - Communicating with the LLM
    """


    def __init__(self):
        """
        Initialize the AI agent.
        """

        self.name = AGENT_NAME
        self.tools = TOOLS



    def run_tool(self, tool_name: str, argument: str):
        """
        Execute a tool.

        Args:
            tool_name (str):
                Name of the requested tool.

            argument (str):
                Input for the tool.

        Returns:
            dict:
                Tool result.
        """


        if tool_name in self.tools:

            return self.tools[tool_name](argument)


        return {
            "error": f"Tool {tool_name} not found"
        }

    def detect_tool(self, user_input: str):
        """
        Detect whether the user request requires a tool.

        Args:
            user_input (str):
                User message.

        Returns:
            str or None:
                Tool name if a tool is needed.
        """


        # Convert input to lowercase
        # so detection is not case-sensitive.
        text = user_input.lower()


        # If the request contains calculation words,
        # use the calculator tool.
        if any(
            word in text
            for word in [
                "calculate",
                "multiply",
                "times",
                "+",
                "-",
                "*",
                "/"
            ]
        ):
            return "calculator"


        # No tool needed.
        return None

    def run(self, user_input: str):
        """
        Process a user request.

        Args:
            user_input (str):
                User message.

        Returns:
            dict:
                Agent response.
        """


        memory.add_message(
            "user",
            user_input
        )

        # Check if the request needs a tool.
        tool_name = self.detect_tool(user_input)


        if tool_name == "calculator":

            # Extract only numbers and operators.
            # Example:
            # "Calculate 25 * 40"
            # becomes:
            # "25 * 40"

            expression = (
                user_input
                .lower()
                .replace("calculate", "")
                .replace("times", "*")
            )


            tool_result = self.run_tool(
                "calculator",
                expression.strip()
            )


            response = (
                f"I used the calculator tool. "
                f"The result is {tool_result['result']}."
            )


            memory.add_message(
                "assistant",
                response
            )


            return {
                "agent": self.name,
                "response": response,
                "tool_used": "calculator",
                "tool_result": tool_result,
                "memory": memory.get_history()
            }

        history = memory.get_history()


        conversation = "\n".join(
            [
                f"{m['role']}: {m['content']}"
                for m in history
            ]
        )


        prompt = f"""
            You are an AI business automation assistant.

            Available tools:
            - calculator

            Conversation:
            {conversation}

            User request:
            {user_input}

            If a tool is needed, explain what tool should be used.
            Otherwise answer normally.
            """


        response = ollama_client.generate(prompt)


        memory.add_message(
            "assistant",
            response
        )


        return {
            "agent": self.name,
            "response": response,
            "memory": memory.get_history()
        }



agent = AIAgent()