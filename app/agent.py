"""
AI Agent core module.

The agent workflow:

User request
    ↓
Memory
    ↓
Planner
    ↓
Decision:
    ├── Tool execution
    │       ↓
    │   Tool result
    │
    └── LLM reasoning
            ↓
        AI response

    ↓
Memory update


Current capabilities:
- Local LLM with Ollama
- Conversation memory
- Tool calling
- Agent planning


Current tools:
- Calculator


Future tools:
- RAG search
- File analysis
- Database access
- Web search
"""


from app.core.constants import AGENT_NAME
from app.llm.ollama_client import ollama_client
from app.memory import memory
from app.tools import TOOLS
from app.planner import planner



class AIAgent:
    """
    Main AI agent class.

    Responsible for:
    - Receiving user requests
    - Planning actions
    - Calling tools
    - Communicating with LLM
    - Managing memory
    """


    def __init__(self):
        """
        Initialize the AI agent.

        Stores:
        - Agent name
        - Available tools
        """

        self.name = AGENT_NAME
        self.tools = TOOLS



    def run_tool(self, tool_name: str, argument: str):
        """
        Execute an available tool.

        Args:
            tool_name (str):
                Name of the tool to execute.

            argument (str):
                Input sent to the tool.

        Returns:
            dict:
                Tool execution result.
        """


        if tool_name in self.tools:

            return self.tools[tool_name](argument)


        return {
            "error": f"Tool {tool_name} not found"
        }



    def run(self, user_input: str):
        """
        Main agent execution function.

        Workflow:
        1. Store user message.
        2. Ask planner for a decision.
        3. Execute tool or call LLM.
        4. Store assistant response.
        5. Return result.

        Args:
            user_input (str):
                User request.

        Returns:
            dict:
                Agent response.
        """


        # Store user message in memory.
        memory.add_message(
            "user",
            user_input
        )


        # Ask planner what action to take.
        plan = planner.decide(
            user_input
        )


        # ============================
        # TOOL EXECUTION PATH
        # ============================

        if plan["action"] == "tool":

            tool_name = plan["tool"]


            # Currently calculator is supported.
            if tool_name == "calculator":


                # Convert natural language into expression.
                #
                # Example:
                # "Calculate 25 times 40"
                #
                # becomes:
                # "25 * 40"

                expression = (
                    user_input
                    .lower()
                    .replace("calculate", "")
                    .replace("times", "*")
                )


                tool_result = self.run_tool(
                    tool_name,
                    expression.strip()
                )


                response = (
                    f"I used the {tool_name} tool. "
                    f"The result is {tool_result['result']}."
                )


                # Store AI response.
                memory.add_message(
                    "assistant",
                    response
                )


                return {
                    "agent": self.name,
                    "plan": plan,
                    "tool_used": tool_name,
                    "tool_result": tool_result,
                    "response": response,
                    "memory": memory.get_history()
                }



        # ============================
        # LLM RESPONSE PATH
        # ============================


        history = memory.get_history()


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


            User request:
            {user_input}


            Provide a helpful answer.
            """


        response = ollama_client.generate(
            prompt
        )


        # Save AI response.
        memory.add_message(
            "assistant",
            response
        )


        return {
            "agent": self.name,
            "plan": plan,
            "response": response,
            "memory": memory.get_history()
        }



# Shared agent instance.
# The API uses this object.
agent = AIAgent()