"""
AI Agent core module.

The agent workflow:

User request
    ↓
Memory
    ↓
Planner
    ↓
Decision
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
- Structured AgentState output


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
from app.models.agent_state import AgentState
from app.logger import logger


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
        """

        self.name = AGENT_NAME
        self.tools = TOOLS



    def run_tool(self, tool_name: str, argument: str):
        """
        Execute an available tool.

        Args:
            tool_name (str):
                Name of the tool.

            argument (str):
                Input for the tool.

        Returns:
            dict:
                Tool execution result.
        """


        if tool_name in self.tools:

            return self.tools[tool_name](argument)


        logger.error(
            f"Tool not found: {tool_name}"
        )

        return {
            "error": f"Tool {tool_name} not found"
        }


    def run(self, user_input: str):
        """
        Main agent execution function.

        Steps:
        1. Save user message.
        2. Ask planner for decision.
        3. Execute tool or use LLM.
        4. Save assistant response.
        5. Return AgentState object.

        Args:
            user_input (str):
                User request.

        Returns:
            AgentState:
                Structured agent response.
        """

        logger.info(
            f"Received user request: {user_input}"
        )

        # Save user message.
        memory.add_message(
            "user",
            user_input
        )


        # Ask planner what action to take.
        plan = planner.decide(
            user_input
        )

        logger.info(
            f"Planner decision: {plan}"
        )

        # ==================================
        # TOOL EXECUTION PATH
        # ==================================

        if plan["action"] == "tool":

            tool_name = plan["tool"]


            if tool_name == "calculator":

                logger.info(
                    f"Executing tool: {tool_name}"
                )

                # Convert natural language into expression.
                #
                # Example:
                # Calculate 25 times 40
                #
                # becomes:
                # 25 * 40

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

                logger.info(
                    f"Tool result: {tool_result}"
                )

                response = (
                    f"I used the {tool_name} tool. "
                    f"The result is {tool_result['result']}."
                )


                # Save AI response.
                memory.add_message(
                    "assistant",
                    response
                )


                # Return structured model.
                return AgentState(
                    agent=self.name,
                    plan=plan,
                    tool_used=tool_name,
                    tool_result=tool_result,
                    response=response,
                    memory=memory.get_history()
                )



        # ==================================
        # LLM RESPONSE PATH
        # ==================================


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

        logger.info(
            "Sending request to Ollama LLM"
        )

        response = ollama_client.generate(
            prompt
        )

        logger.info(
            "LLM response generated successfully"
        )

        # Save AI response.
        memory.add_message(
            "assistant",
            response
        )


        # Return structured model.
        return AgentState(
            agent=self.name,
            plan=plan,
            response=response,
            memory=memory.get_history()
        )



# Shared agent instance.
agent = AIAgent()
